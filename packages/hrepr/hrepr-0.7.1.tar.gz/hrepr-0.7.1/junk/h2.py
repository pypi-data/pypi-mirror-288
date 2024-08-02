from types import SimpleNamespace


class Tag:
    __slots__ = ["parent", "attributes", "children", "resources"]

    def __init__(self, parent, attributes=None, children=None, resources=None):
        self.parent = parent
        self.attributes = attributes
        self.children = children
        self.resources = resources

    def fill(self, children=None, attributes=None, resources=None):
        if not children and not attributes and not resources:
            return self

        if isinstance(resources, Tag):
            resources = (resources,)

        return type(self)(
            parent=self,
            attributes=attributes,
            children=children,
            resources=resources,
        )

    def __call__(self, *children, **attributes):
        # if "__constructor" in attributes:
        #     if "id" not in attributes and "id" not in self.attributes:
        #         attributes["id"] = _nextid()
        attributes = {
            attr.replace("_", "-"): value for attr, value in attributes.items()
        }
        if len(children) > 0 and isinstance(children[0], dict):
            attributes = {**children[0], **attributes}
            children = children[1:]
        return self.fill(children, attributes)

    def __getitem__(self, items):
        if not isinstance(items, tuple):
            items = (items,)
        if items:
            if self.attributes:
                items = [*(self.attributes or {}).get("class", ()), *items]
                return self.fill(attributes={"class": items})
            else:
                return self.fill(attributes={"class": items})
        return self

    # def __getitem__(self, items):
    #     if not isinstance(items, tuple):
    #         items = (items,)
    #     assert all(isinstance(item, str) for item in items)
    #     attributes = {}
    #     classes = [it for it in items if not it.startswith("#")]
    #     if classes:
    #         attributes["class"] = [*(self.attributes or {}).get("class", ()), *classes]

    #     # ids = [it for it in items if it.startswith("#")]
    #     # if ids:
    #     #     the_id = ids[-1][1:]
    #     #     if the_id == "":
    #     #         the_id = f"AID_{next(current_autoid)}"
    #     #     attributes["id"] = the_id

    #     return self.fill(attributes=attributes)


class HTML:
    """
    Tag factory:

    >>> H = HTML()
    >>> H.div()
    <div></div>
    >>> H.a(href="http://cool.cool.cool")("My cool site")
    <a href="http://cool.cool.cool">My cool site</a>
    >>> H.span["cool", "beans"]("How stylish!")
    <span class="cool beans">How stylish!</span>
    """

    def __init__(self, tag_class=Tag, instantiate=True):
        self.tag_class = tag_class
        self.instantiate = instantiate

    def __getattr__(self, tag_name):
        # return self.tag_class(tag_name)
        tag_name = tag_name.replace("_", "-")
        tag_class = self.tag_class
        if hasattr(tag_class, "specialize"):
            tag_class = tag_class.specialize(tag_name)
        if self.instantiate:
            return tag_class(tag_name)
        else:
            return tag_class


H = HTML(tag_class=Tag, instantiate=True)
HType = HTML(tag_class=Tag, instantiate=False)

H = SimpleNamespace(
    div=Tag("div"),
)
