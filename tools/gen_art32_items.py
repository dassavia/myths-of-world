"""The item icons, drawn at 32x32 with the renderer of art32.py: the tools, armour and metals of the three
mythologies, the relics, trophies, foods, potions and books.

Run after hd_textures.py (which still enlarges the textures that are not redrawn here, such as entities), and before
gen_3d_gear.py, which builds the 3D weapon models from these icons. Pass item names to draw only those.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from art32 import Diagonal, Sprite, bands, combine, grain, mat, noise, scales  # noqa: E402
from hd_textures import save_marked  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "mythsofworlds", "textures",
                    "item")
D = Diagonal()
ITEMS = {}


def item(name):
    def wrap(fn):
        ITEMS[name] = fn
        return fn
    return wrap


# ---------------------------------------------------------------- materials

WOOD = mat(0x7A5230, spread=0.38, glint=False)
DARK_WOOD = mat(0x4E3220, spread=0.35, glint=False)
LEATHER = mat(0x6B3A24, spread=0.4, glint=False)
RED_LEATHER = mat(0x8A1E2A, spread=0.42, glint=False)
GOLD = mat(0xE8B43C)
CLOTH_RED = mat(0xB02A30, spread=0.42, glint=False)

METALS = {
    # metal: blade, trim (guard, rivets), grip, gem
    "orichalcum": dict(blade=mat(0xDC8A3E), trim=GOLD, grip=RED_LEATHER, gem=mat(0x3CC0A0), dark=mat(0xA85A26)),
    "bulat": dict(blade=mat(0xB7C2CE, spread=0.48), trim=mat(0xC9A24A), grip=LEATHER, gem=mat(0x9ADCF2),
                  dark=mat(0x7D8A99)),
    "dark_iron": dict(blade=mat(0x66707F, spread=0.55), trim=mat(0x8C939F), grip=DARK_WOOD, gem=mat(0x4FC8F0),
                      dark=mat(0x464C59)),
}
# Bulat is patterned (Damascus watering), dark iron etched with runes.
PATTERN = {"orichalcum": None, "bulat": grain((1, -1), period=2.6, amount=0.1, seed=3), "dark_iron": noise(0.06, 9)}


def handle(s, length, grip, width=2.2, start=0.0):
    s.stroke([D(start, 0), D(length, 0)], width, WOOD, bevel=1.2, pattern=grain((1, -1), 2.5, 0.1, 1))
    s.poly(D.pts([(start - 0.2, -1.6), (start + 5, -1.6), (start + 5, 1.6), (start - 0.2, 1.6)]), grip, bevel=1.0,
           pattern=bands("y", 2, 0.12))


def sword(metal):
    m = METALS[metal]
    s = Sprite(metal + "_sword")
    s.poly(D.pts([(1.5, -1.5), (9, -1.5), (9, 1.5), (1.5, 1.5)]), m["grip"], bevel=1.0, pattern=bands("x", 2, 0.14))
    s.ellipse((*[c - 2.1 for c in D(1.2)], *[c + 2.1 for c in D(1.2)]), m["trim"])
    if metal == "bulat":  # a Slavic sword: guard bent towards the blade
        s.poly(D.pts([(8.5, -6), (10.5, -6.5), (11.5, -5), (10.5, 5), (11.5, 6.5), (10.5, 6.5), (8.5, 5)]), m["trim"],
               bevel=1.2)
    elif metal == "dark_iron":  # a Norse sword: a short heavy guard
        s.poly(D.pts([(8.5, -4.6), (11, -4.6), (11, 4.6), (8.5, 4.6)]), m["trim"], bevel=1.4)
    else:  # a Greek xiphos: leaf blade and a crossbar with round ends
        s.poly(D.pts([(8.5, -4.2), (10.8, -4.2), (10.8, 4.2), (8.5, 4.2)]), m["trim"], bevel=1.2)
        for side in (-5, 5):
            s.ellipse((*[c - 1.6 for c in D(9.6, side)], *[c + 1.6 for c in D(9.6, side)]), m["trim"])
    if metal == "orichalcum":
        blade = [(10.8, -2.2), (20, -2.9), (28, -2.6), (34.5, 0), (28, 2.6), (20, 2.9), (10.8, 2.2)]
    else:
        blade = [(10.8, -2.5), (30.5, -2.5), (34.5, 0), (30.5, 2.5), (10.8, 2.5)]
    s.poly(D.pts(blade), m["blade"], bevel=2.4, pattern=PATTERN[metal])
    s.stroke([D(12, 0), D(30, 0)], 0.9, m["dark"] if metal != "orichalcum" else mat(0xF4B477), bevel=0.4, edge=False)
    gem = m["gem"]
    s.ellipse((*[c - 1.2 for c in D(9.6)], *[c + 1.2 for c in D(9.6)]), gem)
    return s


def axe(metal):
    m = METALS[metal]
    s = Sprite(metal + "_axe")
    handle(s, 31, m["grip"])
    if metal == "dark_iron":  # a bearded Norse axe: the edge sweeps down towards the hand
        head = [(23, 1), (29.5, 1), (31, 4), (31, 9.5), (28, 11), (23.5, 10.5), (21, 9), (24, 6), (23, 4)]
    elif metal == "bulat":  # a Slavic axe: a straight high edge
        head = [(22, 1), (29.5, 1), (32, 3), (32.5, 10), (29.5, 10.5), (26.5, 8), (24, 5), (22, 4)]
    else:  # a Greek axe: a crescent edge
        head = [(22, 1), (29.5, 1), (31.5, 4), (33, 9), (30.5, 11.5), (27.5, 9.5), (25, 6.5), (22, 4)]
    s.poly(D.pts(head), m["blade"], bevel=2.2, pattern=PATTERN[metal])
    s.poly(D.pts([(23, -1.2), (28.5, -1.2), (28, -3.6), (23.5, -3.6)]), m["dark"], bevel=1.2)
    s.ellipse((*[c - 1.1 for c in D(25, 0)], *[c + 1.1 for c in D(25, 0)]), m["trim"])
    return s


def pickaxe(metal):
    m = METALS[metal]
    s = Sprite(metal + "_pickaxe")
    handle(s, 29, m["grip"])
    head = [(22.5, -11.5), (26.5, -8), (28.5, -4), (29.5, 0), (28.5, 4), (26.5, 8), (22.5, 11.5), (24.5, 6.5),
            (25.5, 3), (25.5, -3), (24.5, -6.5)]
    s.poly(D.pts(head), m["blade"], bevel=1.8, pattern=PATTERN[metal])
    s.poly(D.pts([(24.2, -2.2), (30.2, -2.2), (30.2, 2.2), (24.2, 2.2)]), m["trim"], bevel=1.4)
    s.ellipse((*[c - 1.1 for c in D(27.2, 0)], *[c + 1.1 for c in D(27.2, 0)]), m["gem"])
    return s


def shovel(metal):
    m = METALS[metal]
    s = Sprite(metal + "_shovel")
    handle(s, 22, m["grip"])
    s.poly(D.pts([(20, -1.8), (23, -1.8), (23, 1.8), (20, 1.8)]), m["trim"], bevel=1.0)
    blade = [(22.5, -4.2), (30, -4.6), (33.5, -2.6), (34.5, 0), (33.5, 2.6), (30, 4.6), (22.5, 4.2)]
    s.poly(D.pts(blade), m["blade"], bevel=2.6, pattern=PATTERN[metal])
    s.stroke([D(24, 0), D(31, 0)], 0.9, m["dark"], bevel=0.3, edge=False)
    return s


def hoe(metal):
    m = METALS[metal]
    s = Sprite(metal + "_hoe")
    handle(s, 30, m["grip"])
    s.poly(D.pts([(28.5, -1.6), (31, -1.6), (31.5, 11.5), (29, 12), (21.5, 11.5), (21.5, 7), (28.5, 6.5)]),
           m["blade"], bevel=1.6, pattern=PATTERN[metal])
    s.poly(D.pts([(26.2, -2.2), (31.5, -2.2), (31.5, 2.2), (26.2, 2.2)]), m["trim"], bevel=1.2)
    return s


# ---------------------------------------------------------------- armour icons

def helmet(metal):
    m = METALS[metal]
    s = Sprite(metal + "_helmet")
    b = m["blade"]
    if metal == "orichalcum":  # Corinthian helmet with a red crest
        s.poly([(5, 10), (8, 6), (13, 4), (19, 4), (24, 6), (27, 10), (27.5, 20), (25, 27), (21, 27), (20, 19),
                (12, 19), (11, 27), (7, 27), (4.5, 20)], b, bevel=3, pattern=PATTERN[metal])
        s.poly([(11, 14), (21, 14), (20, 19), (17, 19), (17, 26), (15, 26), (15, 19), (12, 19)], mat(0x1C1012),
               bevel=1, base=0.2, edge=False)
        s.poly([(5, 9), (8, 3), (14, 1), (22, 1.5), (27, 5), (28, 9), (24, 6.5), (16, 5), (9, 6)], CLOTH_RED, bevel=1.5,
               pattern=bands("x", 2, 0.15))
        s.stroke([(6, 12), (26, 12)], 1.0, m["trim"], bevel=0.5)
    elif metal == "bulat":  # Slavic shishak: pointed with a mail aventail
        s.poly([(16, 2), (18, 6), (24, 10), (26, 16), (6, 16), (8, 10), (14, 6)], b, bevel=3, pattern=PATTERN[metal])
        s.poly([(5, 16), (27, 16), (28, 27), (23, 28), (21, 21), (11, 21), (9, 28), (4, 27)], mat(0x9AA6B4),
               bevel=1.2, pattern=scales(2, 0.25))
        s.rect((5, 15, 27, 18), m["trim"], bevel=1.2)
        s.poly([(15, 18), (17, 18), (17, 24), (15, 24)], m["dark"], bevel=1)
        s.ellipse((14.5, 1, 17.5, 4), m["trim"])
    else:  # Norse: rounded cap, nose guard and spectacle guards
        s.poly([(5, 17), (5, 11), (8, 6), (13, 3.5), (19, 3.5), (24, 6), (27, 11), (27, 17)], b, bevel=3,
               pattern=PATTERN[metal])
        s.rect((4.5, 15, 27.5, 18.5), m["trim"], bevel=1.4)
        s.stroke([(16, 4), (16, 15)], 2.0, m["trim"], bevel=1)
        s.poly([(8, 18), (14, 18), (15, 22), (12, 24.5), (9, 23)], m["dark"], bevel=1.5)
        s.poly([(18, 18), (24, 18), (23, 23), (20, 24.5), (17, 22)], m["dark"], bevel=1.5)
        s.rect((15, 18, 17, 26), m["trim"], bevel=1)
        s.ellipse((14.6, 7.5, 17.4, 10.3), m["gem"])
    return s


def chestplate(metal):
    m = METALS[metal]
    s = Sprite(metal + "_chestplate")
    body = [(3, 7), (9, 4), (12, 6), (20, 6), (23, 4), (29, 7), (28.5, 14), (25, 14), (25, 28), (7, 28), (7, 14),
            (3.5, 14)]
    if metal == "bulat":  # mail shirt with a plate on the breast
        s.poly(body, mat(0x9AA6B4), bevel=2, pattern=scales(2, 0.22))
        s.poly([(10, 9), (22, 9), (21, 20), (16, 23), (11, 20)], m["blade"], bevel=2.5, pattern=PATTERN[metal])
        s.ellipse((14, 13, 18, 17), m["gem"])
        s.rect((7, 24, 25, 26.5), LEATHER, bevel=1)
        s.rect((15, 23.5, 17.5, 27), m["trim"], bevel=1)
    elif metal == "dark_iron":  # lamellar plates in rows
        s.poly(body, m["blade"], bevel=2.6, pattern=combine(bands("y", 4, 0.14), PATTERN[metal]))
        s.poly([(3, 7), (9, 4), (11, 9), (5, 12)], m["trim"], bevel=1.5)
        s.poly([(29, 7), (23, 4), (21, 9), (27, 12)], m["trim"], bevel=1.5)
        s.stroke([(16, 7), (16, 26)], 1.0, m["dark"], bevel=0.5, edge=False)
        s.ellipse((14, 10, 18, 14), m["gem"])
    else:  # muscle cuirass with a gold rim and a pteruges skirt
        s.poly(body[:-4] + [(25, 23), (7, 23)] + body[-2:], m["blade"], bevel=3.2)
        s.stroke([(11, 13), (15, 15)], 1.0, m["dark"], bevel=0.5, edge=False)
        s.stroke([(21, 13), (17, 15)], 1.0, m["dark"], bevel=0.5, edge=False)
        s.stroke([(16, 16), (16, 21)], 1.0, m["dark"], bevel=0.5, edge=False)
        for x in range(7, 25, 3):
            s.rect((x, 23, x + 2.6, 29), CLOTH_RED, bevel=1)
        s.stroke([(7, 22.5), (25, 22.5)], 1.2, m["trim"], bevel=0.6)
        s.stroke([(12, 6.5), (16, 9), (20, 6.5)], 1.0, m["trim"], bevel=0.5)
    return s


def leggings(metal):
    m = METALS[metal]
    s = Sprite(metal + "_leggings")
    shape = [(7, 4), (25, 4), (26.5, 28), (19.5, 28), (16.5, 12), (15.5, 12), (12.5, 28), (5.5, 28)]
    if metal == "bulat":
        s.poly(shape, mat(0x9AA6B4), bevel=2, pattern=scales(2, 0.22))
        s.rect((6.5, 4, 25.5, 7.5), LEATHER, bevel=1.2)
        s.poly([(6.5, 15), (12.5, 15), (12.5, 21), (6, 21)], m["blade"], bevel=1.8)
        s.poly([(19.5, 15), (25.8, 15), (26, 21), (19.5, 21)], m["blade"], bevel=1.8)
    elif metal == "dark_iron":
        s.poly(shape, m["blade"], bevel=2.6, pattern=combine(bands("y", 4, 0.12), PATTERN[metal]))
        s.rect((6.5, 4, 25.5, 7.5), m["trim"], bevel=1.2)
        s.ellipse((14.5, 4.2, 17.5, 7.2), m["gem"])
    else:
        s.poly(shape, CLOTH_RED, bevel=2, pattern=bands("x", 3, 0.1))
        s.rect((6.5, 4, 25.5, 7.5), m["trim"], bevel=1.2)
        s.poly([(5.8, 14), (12.8, 14), (12.6, 27), (5.6, 27)], m["blade"], bevel=2.2)
        s.poly([(19.3, 14), (26.2, 14), (26.4, 27), (19.5, 27)], m["blade"], bevel=2.2)
    return s


def boots(metal):
    m = METALS[metal]
    s = Sprite(metal + "_boots")
    for x0, flip in ((3, 1), (17, 1)):
        shin = [(x0 + 1, 8), (x0 + 9, 8), (x0 + 9, 22), (x0 + 12, 24), (x0 + 12, 28), (x0, 28), (x0, 18)]
        if metal == "bulat":
            s.poly(shin, mat(0x8E2A22, spread=0.4, glint=False), bevel=2, pattern=bands("y", 3, 0.08))
            s.rect((x0 + 0.5, 8, x0 + 9.5, 11), m["trim"], bevel=1)
            s.poly([(x0 + 2, 13), (x0 + 8, 13), (x0 + 8, 21), (x0 + 2, 21)], m["blade"], bevel=1.6)
        elif metal == "dark_iron":
            s.poly(shin, m["blade"], bevel=2.4, pattern=combine(bands("y", 4, 0.12), PATTERN[metal]))
            s.rect((x0 + 0.5, 8, x0 + 9.5, 11), m["trim"], bevel=1)
            s.ellipse((x0 + 3.5, 14, x0 + 6.5, 17), m["gem"])
        else:  # greaves over sandals
            s.poly(shin, LEATHER, bevel=2)
            s.poly([(x0 + 1, 8), (x0 + 9, 8), (x0 + 9, 22), (x0 + 1, 22)], m["blade"], bevel=2.4)
            s.stroke([(x0 + 1.5, 9), (x0 + 8.5, 9)], 1, m["trim"], bevel=0.5)
        s.rect((x0, 26.5, x0 + 12, 28.5), m["dark"], bevel=1)
    return s


def ingot(metal):
    m = METALS[metal]
    s = Sprite(metal + "_ingot")
    s.poly([(3, 23), (9, 14), (29, 14), (29, 16.5), (23, 25), (3, 25)], m["dark"], bevel=1.5)
    s.poly([(3.5, 22.5), (9.5, 14), (28.5, 14), (22.5, 22.5)], m["blade"], bevel=3, pattern=PATTERN[metal])
    s.stroke([(10, 18.5), (20, 18.5)], 0.9, m["dark"], bevel=0.3, edge=False)
    s.ellipse((14, 16.6, 17, 19.6), m["gem"])
    return s


def raw(metal):
    m = METALS[metal]
    s = Sprite("raw_" + metal)
    for box in ((4, 11, 19, 26), (13, 6, 27, 20), (14, 15, 28, 28), (6, 6, 15, 15)):
        s.ellipse(box, m["blade"] if box[0] != 6 else m["dark"], pattern=combine(noise(0.1, box[0]),
                                                                                PATTERN[metal] or noise(0.01)))
    return s


for _metal in METALS:
    for _fn in (sword, axe, pickaxe, shovel, hoe, helmet, chestplate, leggings, boots, ingot):
        ITEMS[f"{_metal}_{_fn.__name__}"] = (lambda f, mm: lambda: f(mm))(_fn, _metal)
    ITEMS["raw_" + _metal] = (lambda mm: lambda: raw(mm))(_metal)


# ---------------------------------------------------------------- main

def main(names):
    from items_relics import register  # noqa: E402  the relics, trophies, foods and books
    register(ITEMS)
    for name in names or sorted(ITEMS):
        # Marked as full resolution, so that hd_textures.py leaves them alone.
        save_marked(ITEMS[name]().render(), os.path.join(ROOT, name + ".png"))
    print(f"items: {len(names or ITEMS)} drawn at 32x32")


if __name__ == "__main__":
    main(sys.argv[1:])
