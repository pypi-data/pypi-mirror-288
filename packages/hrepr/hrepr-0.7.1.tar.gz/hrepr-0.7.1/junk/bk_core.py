from collections import Counter

from ovld import OvldMC, ovld

from . import std
from .h import HTML, Tag, css_hrepr

SHORT = object()


class Config:
    def __init__(self, cfg={}, parent=None):
        self._parent = parent
        self.__dict__.update(cfg)

    def __call__(self, **cfg):
        return self.with_config(cfg)

    def with_config(self, cfg):
        # rval = copy(self)
        # rval.__dict__.update(cfg)
        # return rval
        if not cfg:
            return self
        elif self.__dict__.keys() == cfg.keys():
            return Config(cfg, self._parent)
        else:
            return Config(cfg, self)

    def __getattr__(self, attr):
        # Only triggers for attributes not in __dict__
        if attr.startswith("_"):
            return getattr(super(), attr)
        elif self._parent:
            return getattr(self._parent, attr)
        return None

    def __hrepr__(self, H, hrepr):
        return hrepr.stdrepr_object("Config", self.__dict__.items())


# class ResourceAccumulator:
#     def __init__(self, acq):
#         self.consulted = set()
#         self.resources = set()
#         self.spent = set()
#         self.acq = acq

#     def acquire(self, cls):
#         if cls not in self.consulted:
#             self.consulted.add(cls)
#             resources = self.acq(cls)
#             resources -= self.spent
#             self.resources |= resources

#     def dump(self):
#         rval = self.resources
#         self.spent |= self.resources
#         self.resources.clear()
#         return rval


class HreprState:
    def __init__(self, resources=set()):
        self.types_seen = set()
        self.resources = set(resources)
        self.stack = Counter()
        self.registry = {}
        self.depth = -1
        self.refs = {}

    def get_ref(self, objid):
        return self.refs.setdefault(objid, len(self.refs) + 1)

    def registered(self, objid):
        return objid in self.registry

    def register(self, objid, value):
        self.registry[objid] = value

    def make_refmap(self):
        rval = {}
        for objid, label in self.refs.items():
            rval[id(self.registry[objid])] = label
        return rval


class Hrepr(metaclass=OvldMC):
    def __init__(self, H, config=None, master=None):
        self.H = H
        if config is None:
            config = Config()
        self.config = config
        self.master = master or self
        self.state = (
            master.state if master else HreprState(self.global_resources())
        )

    def with_config(self, config):
        if not config:
            return self
        else:
            cfg = self.config.with_config(config)
            return type(self)(H=self.H, config=cfg, master=self.master)

    def ref(self, obj, loop=False):
        # breakpoint()
        num = self.state.get_ref(id(obj))
        sym = "⟳" if loop else "#"
        ref = self.H.span["hrepr-ref"](sym, num)
        if self.config.shortref:
            return ref
        else:
            short = self.hrepr_short(obj)
            if short is NotImplemented:
                short = self.default_hrepr_short(obj)
            return self.H.div["hrepr-refbox"](ref("="), short)

    def global_resources(self):
        return set()

    # def default_hrepr_resources(self, cls):
    #     return None

    def default_hrepr(self, obj):
        clsn = type(obj).__name__
        return self.H.span[f"hreprt-{clsn}"](str(obj))

    def default_hrepr_short(self, obj):
        clsn = type(obj).__name__
        return self.H.span[f"hreprs-{clsn}"]("<", clsn, ">")

    @ovld
    def hrepr_resources(self, cls: object):
        if hasattr(cls, "__hrepr_resources__"):
            return cls.__hrepr_resources__(self.H)
        # else:
        #     return self.default_hrepr_resources(cls)

    @ovld
    def hrepr(self, obj: object):
        if hasattr(obj, "__hrepr__"):
            return obj.__hrepr__(self, self.H)
        # elif self.state.skip_default:
        #     return NotImplemented
        # else:
        #     return self.default_hrepr(obj)
        else:
            return NotImplemented

    @ovld
    def hrepr_short(self, obj: object):
        if hasattr(obj, "__hrepr_short__"):
            return obj.__hrepr_short__(self, self.H)
        # elif self.state.skip_default:
        #     return NotImplemented
        # else:
        #     # return self.default_hrepr_short(textwrap.shorten(str(obj), 20))
        #     return self.default_hrepr_short(obj)
        else:
            return NotImplemented

    # @ovld
    # def hrepr(self, obj: object):
    #     if hasattr(obj, "__hrepr__"):
    #         return obj.__hrepr__(self, self.H)
    #     elif self.state.skip_default:
    #         return NotImplemented
    #     else:
    #         return self.default_hrepr(obj)

    # @ovld
    # def hrepr_short(self, obj: object):
    #     if hasattr(obj, "__hrepr_short__"):
    #         return obj.__hrepr_short__(self, self.H)
    #     elif self.state.skip_default:
    #         return NotImplemented
    #     else:
    #         # return self.default_hrepr_short(textwrap.shorten(str(obj), 20))
    #         return self.default_hrepr_short(obj)

    def __call__(self, obj, **config):
        self.state.skip_default = False
        runner = self.with_config(config)
        ido = id(obj)
        if self.state.stack[ido]:
            return runner.ref(obj, loop=True)
            # return self.ref(self.state.get_ref(ido), loop=True)

        if self.state.registered(ido) and not runner.config.norefs:
            return runner.ref(obj)
            # return self.ref(self.state.get_ref(ido))

        # Collect resources for this object
        cls = type(obj)
        if cls not in self.state.types_seen:
            self.state.types_seen.add(cls)
            resources = self.hrepr_resources[cls](cls)
            if resources:
                if not isinstance(resources, (tuple, list, set, frozenset)):
                    self.state.resources.add(resources)
                else:
                    self.state.resources.update(resources)

        # Push object on the stack to detect circular references
        self.state.stack[ido] += 1
        self.state.depth += 1

        if (
            runner.config.max_depth is not None
            and self.state.depth > runner.config.max_depth
        ):
            rval = runner.hrepr_short(obj)
        else:
            rval = runner.hrepr(obj)
            if rval is SHORT:
                rval = runner.hrepr_short(obj)
                if rval is NotImplemented:
                    rval = runner.default_hrepr_short(obj)
            elif rval is NotImplemented:
                rval = runner.hrepr_short(obj)
                if rval is NotImplemented:
                    rval = runner.default_hrepr(obj)
                    self.state.register(ido, rval)
            else:
                self.state.register(ido, rval)

            # self.state.skip_default = True
            # rval = runner.hrepr(obj)
            # self.state.skip_default = False
            # if rval is SHORT:
            #     rval = runner.hrepr_short(obj)
            # elif rval is NotImplemented:
            #     self.state.skip_default = True
            #     rval = runner.hrepr_short(obj)
            #     self.state.skip_default = False
            #     if rval is NotImplemented:
            #         rval = runner.hrepr(obj)
            #         self.state.register(ido, rval)
            # else:
            #     self.state.register(ido, rval)

        # Pop object from the stack
        self.state.depth -= 1
        self.state.stack[ido] -= 1
        return rval


class StdHrepr(Hrepr):
    def global_resources(self):
        return {self.H.style(css_hrepr)}

    def hrepr(self, xs: list):
        return std.iterable(self, xs, before="[", after="]")

    # def hrepr(self, x: (int, float)):
    #     return SHORT

    def hrepr_short(self, x: (int, float)):
        return std.standard(self, x)


def inject_reference_numbers(node, refmap):
    if isinstance(node, Tag):
        node.children = [
            inject_reference_numbers(child, refmap) for child in node.children
        ]
        refnum = refmap.get(id(node), None)
        if refnum is not None:
            ref = H.span["hrepr-ref"]("#", refnum)
            return H.div["hrepr-refbox"](ref("="), node)
        else:
            return node
    else:
        return node


H = HTML()


def hrepr(obj, **config):
    hcall = StdHrepr(H=H, config=Config(config))
    rval = hcall(obj)
    rval = inject_reference_numbers(rval, hcall.state.make_refmap())
    rval.resources = hcall.state.resources
    return rval
