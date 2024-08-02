import sys
import time
from collections import deque

from hrepr import H
from hrepr.h import Tag

# from hrepr.h2 import H


class Gorgle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


# def biggo():
#     t = time.time()
#     things = []
#     for i in range(200):
#         for j in range(200):
#             # things.append(didi := H.div(str(i), str(j), class_="yo"))
#             things.append(didi := H.div["yo"](str(i), str(j)))
#             # things.append(Gorgle(i, j, i * j))
#             # things.append([i, j])
#     divvo = H.div(things)
#     print(int((time.time() - t) * 1000))

#     t = time.time()
#     str(divvo)
#     print(int((time.time() - t) * 1000))
#     return None


def auto_require_ids(node, counts):
    q = deque()
    q.append(node)
    while q:
        node = q.popleft()
        if isinstance(node, (list, tuple)):
            q.extend(node)
        elif isinstance(node, Tag):
            # if node._frozen:
            #     print(node)
            if id(node) in counts:
                counts[id(node)][0] -= 1
                continue
            else:
                counts[id(node)] = [sys.getrefcount(node) - 3, node]
                q.append(node._parent)
                q.append(node._children)

    # print({x: n for x, (n, node) in counts.items() if n > 0})
    for _, (n, node) in counts.items():
        if n > 0 and not node._constructed:
            node.require_id()


def biggo():
    t = time.time()
    divvo = H.div()
    for i in range(75):
        for j in range(75):
            divvo = divvo(H.div["yo"](str(i), str(j)))
    print(int((time.time() - t) * 1000))
    hoy = H.div("hoy!")
    divvo = divvo(hoy)

    t = time.time()
    # auto_require_ids(divvo, {})
    # print(str(divvo))
    str(divvo)
    print(int((time.time() - t) * 1000))
    return None


def main():
    biggo()


if __name__ == "__main__":
    main()


# import json
# from pathlib import Path
# import time


# chardata = {}
# chardata_path = Path("chardata.json")
# if chardata_path.exists():
#     chardata = json.load(fp=open(chardata_path, "r", encoding="utf8"))


# bgmap = """
# gggggggggggggggggggg
# gggggggggggggggggggg
# gggggggggggggggggggg
# ggMMMMMMMMgggggggggg
# ggMMMMMMMMgggggggggg
# ggMMMMMMMMgggggggggg
# ggMMMMMMMMgggggggggg
# ggMMMMMMMMgggggggggg
# ggMMMMMMMMgggggggggg
# ggMMMMMMMMgggggggggg
# ggMMMMMMMMgggggggggg
# gggggggggggggggggggg
# gggggggggggggggggggg
# gggggggggggggggggggg
# gggggggggggggggggggg
# gggggggggggggggggggg
# gggggggggggggggggggg
# gggggggggggggggggggg
# gggggggggggggggggggg
# gggggggggggggggggggg
# """


# testmap = """
# RRRRRRRRRRRRRRRARRAR
# RARRRR      RRRRRRRR
# RRRR             RRR
# Rz            EE  RR
# R  GG  GG    FFEE  R
# R  GG  GG   TEFFF  R
# R             EE   R
# R         T    P P R
# R  GG  GG       P  g
# R  GG  GG    b    RR
# RR   B             R
# RRR     b          R
# RR     B     OO    R
# R           OOOO   R
# R  EE   @   OOOO   R
# R  EEE       OO   AR
# RR  EE            RR
# RRRR              RR
# SSARRRRR      R RRRR
# SSRRRRRRRgggRRRRRRRR
# """


# letter_definitions = {
#     "R": {
#         "character": "R",
#         "font": "Bowlby One SC",
#         "foreground": "rgb(100, 100, 100)",
#         "background": "rgb(200, 200, 200)",
#         "rotations": [0, 90, 180, 270],
#     },
#     "A": {
#         "character": "A",
#         "font": "Bowlby One SC",
#         "foreground": "rgb(80, 80, 80)",
#         "background": "rgb(170, 170, 170)",
#         "rotations": [0, 90, 180, 270],
#     },
#     "M": {
#         "character": "G",
#         "font": "Bungee Outline",
#         "foreground": "rgb(255, 230, 210)",
#         "background": "rgb(255, 250, 230)",
#     },
#     "G": {
#         "character": "G",
#         "font": "Bungee Shade",
#         "foreground": "rgb(255, 184, 134)",
#         "background": "rgb(255, 250, 230)",
#     },
#     "S": {
#         "character": "S",
#         "font": "Tilt Prism",
#         "background": "rgb(0,0,255)",
#         "foreground": "rgb(220,220,255)",
#     },
#     "E": {
#         "character": "E",
#         "font": "Rye",
#         "foreground": "rgb(134, 56, 0)",
#         "background": "rgb(255, 184, 134)",
#         "rotations": [0, 90, 180, 270],
#     },
#     "F": {
#         "character": "E",
#         "font": "Sancreek",
#         "foreground": "rgb(224, 146, 90)",
#         "background": "rgb(255, 184, 134)",
#         "rotations": [0, 90, 180, 270],
#     },
#     "O": {
#         "character": "O",
#         "font": "Rye",
#         "foreground": "rgb(114, 36, 0)",
#         "background": "rgb(235, 154, 104)",
#         "rotations": [0, 90, 180, 270],
#     },
#     "g": {
#         "character": "g",
#         "font": "Henny Penny",
#         "foreground": "rgb(180,240,180)",
#         "background": "rgb(220,240,220)",
#         "repeat": 1,
#         "rotations": [0, 90, 180, 270],
#     },
#     "b": {
#         "character": "b",
#         "font": "Babylonica",
#         "foreground": "red",
#         "background": "rgb(0,0,0,0)",
#     },
#     "B": {
#         "character": "B",
#         "font": "Babylonica",
#         "foreground": "blue",
#         "stroke": "rgb(255,150,150)",
#         "background": "rgb(0,0,0,0)",
#     },
#     "z": {
#         "character": "z",
#         "font": "Babylonica",
#         "foreground": "red",
#         "background": "rgb(0,0,0,0)",
#     },
#     "T": {
#         "character": "T",
#         "font": "Parisienne",
#         "foreground": "blue",
#         "stroke": "rgb(200,200,255)",
#         "background": "rgb(0,0,0,0)",
#     },
#     "P": {
#         "character": "P",
#         "font": "Parisienne",
#         "foreground": "rgb(255,0,255)",
#         "stroke": "rgb(255,200,255)",
#         "background": "rgb(0,0,0,0)",
#     },
#     "@": {
#         "character": "@",
#         "font": "Babylonica",
#         "foreground": "violet",
#         "background": "rgb(0,0,0,0)",
#     }
# }


# def layer(m):
#     t = time.time()
#     matrix = [list(line) for line in m.split("\n") if line]
#     n = len(matrix)
#     sz = 100 // n

#     grp = []
#     for row, line in enumerate(matrix):
#         for col, ch in enumerate(line):
#             if ch == " ":
#                 continue

#             char = letter_definitions[ch]
#             char = {**chardata[char["font"]][char["character"]], **char}

#             box = H.rect(
#                 x=col*sz,
#                 y=row*sz,
#                 width=sz,
#                 height=sz,
#                 fill=char["background"],
#             )
#             grp.append(box)

#             tx = char["offsetx"]
#             ty = char["offsety"]
#             repeat = char.get("repeat", 1)
#             scalex = char["scalex"] / 10 * sz / repeat
#             scaley = char["scaley"] / 10 * sz / repeat
#             placex = (col + 1 / (repeat * 2)) * sz
#             placey = (row + 1 / (repeat * 2)) * sz
#             angle = random.choice(char.get("rotations", [0]))
#             for i in range(repeat):
#                 for j in range(repeat):
#                     px = placex + (i * sz / repeat)
#                     py = placey + (j * sz / repeat)
#                     text = H.text["char"](
#                         char["character"],
#                         style={
#                             "font-family": char["font"],
#                             "font-size": "10px",
#                             "text-anchor": "middle",
#                             "dominant-baseline": "middle",
#                         },
#                         stroke=char.get("stroke", "transparent"),
#                         stroke_width=3,
#                         stroke_linejoin="round",
#                         fill=char["foreground"],
#                         paint_order="stroke",
#                         x=0,
#                         y=0,
#                         transform=f"translate({px},{py}),rotate({angle}),scale({scalex},{scaley}),translate({tx},{ty})",
#                     )
#                     grp.append(text)
#     print("layer", time.time() - t)
#     return H.g(grp)
