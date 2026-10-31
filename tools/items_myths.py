"""The wonders of the three worlds added in 0.14 (relics of the myths, runes, the gifts of Nav), drawn at 32x32.

Registered into gen_art32_items.py next to items_relics.py; same art32 toolkit (see art32.py).
"""
import math

from art32 import Diagonal, Sprite, bands, combine, grain, mat, noise

from items_relics import DARK_GOLD, DARK_WOOD, GOLD, SAPPHIRE, STEEL, WOOD, at, gem

D = Diagonal()

# Items whose picture is also a block texture (a flower is drawn the same in the hand and on the ground).
BLOCK_TEXTURES = ["fern_flower"]
# Icons of the mod's status effects, 18x18 (textures/mob_effect).
EFFECT_ICONS = {}

RED_WOOL = mat(0xB8282E, spread=0.4, glint=False)
LINEN = mat(0xEDE6D2, spread=0.25, glint=False)
EMBROIDERY = mat(0xC8202A, spread=0.3, glint=False)
FERN = mat(0x3E7A2E, spread=0.45, glint=False)
FIRE_PETAL = mat(0xFF7A1E, spread=0.4)
FIRE_HEART = mat(0xFFE070, spread=0.3)
YARN = mat(0xD8B060, spread=0.4, glint=False)
RUNESTONE = mat(0x6E7480, spread=0.42, glint=False)
RUNE_GLOW = mat(0x6EC8FF, spread=0.25)
LAUREL = mat(0x5A8A3A, spread=0.45, glint=False)
BERRY = mat(0x2A2A5A, spread=0.3)

# Elder Futhark: the strokes of each rune on a 10x14 grid, (x0, y0, x1, y1).
RUNES = {
    "fehu": [(3, 1, 3, 13), (3, 6, 8, 2), (3, 9, 8, 5)],
    "uruz": [(3, 1, 3, 13), (3, 1, 8, 5), (8, 5, 8, 13)],
    "thurisaz": [(3, 1, 3, 13), (3, 4, 8, 7), (8, 7, 3, 10)],
    "ansuz": [(3, 1, 3, 13), (3, 2, 8, 6), (3, 6, 8, 10)],
    "raidho": [(3, 1, 3, 13), (3, 1, 8, 4), (8, 4, 3, 7), (3, 7, 8, 13)],
    "algiz": [(5.5, 1, 5.5, 13), (5.5, 7, 1.5, 2), (5.5, 7, 9.5, 2)],
}


def register(items):
    def item(name):
        def wrap(fn):
            items[name] = fn
            return fn
        return wrap

    # ---------------------------------------------------------------- Hellas

    @item("ariadne_thread")
    def _():
        s = Sprite("ariadne_thread")
        s.ellipse((5, 9, 23, 27), RED_WOOL, pattern=combine(grain((1, 1), 2.2, 0.16, 3), noise(0.05, 3)))
        for k in range(4):                                               # wound turns of the thread
            s.stroke([(7 + k * 4, 11 + k), (12 + k * 3, 25 - k)], 0.9, mat(0x8A1A1E, glint=False), bevel=0.3, edge=False)
        s.rect((12, 5, 16, 10), GOLD, bevel=1.2)                         # the golden spindle
        s.stroke([(22, 18), (25, 22), (27, 27), (29, 30)], 1.1, RED_WOOL, bevel=0.4)   # the loose end
        return s

    @item("delphic_laurel")
    def _():
        s = Sprite("delphic_laurel")
        s.stroke([(5, 29), (13, 19), (21, 10), (27, 3)], 1.4, DARK_WOOD, bevel=0.5)
        for t, side in ((0.12, 1), (0.28, -1), (0.44, 1), (0.6, -1), (0.76, 1), (0.9, -1)):
            x, y = 5 + 22 * t, 29 - 26 * t
            # A pointed oval leaf sticking out to one side of the twig.
            dx, dy = (5.5, 4.0) if side > 0 else (-4.0, -5.5)
            mid = (x + dx * 0.55, y + dy * 0.55)
            px, py = -dy * 0.28, dx * 0.28
            s.poly([(x, y), (mid[0] + px, mid[1] + py), (x + dx * 1.25, y + dy * 1.25), (mid[0] - px, mid[1] - py)], LAUREL,
                   bevel=1.6, pattern=noise(0.06, int(t * 10)))
        gem(s, 10, 24, 1.6, BERRY)
        gem(s, 20, 13, 1.6, BERRY)
        return s

    # ---------------------------------------------------------------- Nav

    @item("fern_flower")
    def _():
        s = Sprite("fern_flower")
        for a in (-0.9, 0.9):                                            # fern fronds
            s.stroke([(16, 30), (16 + 9 * math.sin(a), 18), (16 + 13 * math.sin(a), 10)], 1.6, FERN, bevel=0.6)
        s.stroke([(16, 31), (16, 16)], 1.4, FERN, bevel=0.6)
        for k in range(5):                                               # five fiery petals
            a = -math.pi / 2 + k * 2 * math.pi / 5
            x, y = 16 + 6 * math.cos(a), 11 + 6 * math.sin(a)
            s.ellipse(at(x, y, 3.3), FIRE_PETAL)
        gem(s, 16, 11, 2.6, FIRE_HEART)
        for x, y in ((6, 5), (26, 6), (25, 18), (7, 17)):
            s.pixel(x, y, (255, 230, 140))
        return s

    @item("samobranka")
    def _():
        s = Sprite("samobranka")
        s.poly([(3, 12), (29, 9), (29, 26), (3, 29)], LINEN, bevel=1.6, pattern=bands("x", 3, 0.05))
        for y0 in (13, 23):                                              # red embroidered borders
            s.stroke([(4, y0 + 0.5), (28, y0 - 2.5)], 1.2, EMBROIDERY, bevel=0.4)
        for x in (7, 13, 19, 25):
            s.poly([(x, 18.5 - (x - 3) * 0.11), (x + 2, 16.5 - (x - 3) * 0.11), (x + 4, 18.5 - (x - 3) * 0.11),
                    (x + 2, 20.5 - (x - 3) * 0.11)], EMBROIDERY, bevel=0.6)
        s.ellipse((11, 4, 21, 12), mat(0xC8863A, spread=0.4, glint=False))   # a round loaf on it
        s.stroke([(13, 7), (19, 7)], 0.8, mat(0x8A5A22, glint=False), bevel=0.3, edge=False)
        return s

    @item("gusli")
    def _():
        s = Sprite("gusli")
        s.poly([(3, 24), (7, 8), (16, 4), (29, 9), (27, 22), (17, 29)], WOOD, bevel=2.2,
               pattern=combine(grain((1, 0.2), 3, 0.12, 5), noise(0.04, 5)))
        s.poly([(7, 22), (10, 10), (17, 7), (25, 11), (24, 20), (17, 25)], mat(0x5A3A20, glint=False), bevel=1.4)
        s.ellipse((14, 13, 19, 18), mat(0x1E120A, glint=False), round_=False)
        for k in range(5):                                               # the singing strings
            s.stroke([(9 + k * 2.2, 10 - k * 0.4), (13 + k * 2.4, 24 - k * 0.6)], 0.9, mat(0xF2ECD8), bevel=0.2, edge=False)
        for x, y in ((6, 21), (24, 8)):
            gem(s, x, y, 1.3, GOLD)
        return s

    @item("klubok")
    def _():
        s = Sprite("klubok")
        s.ellipse((6, 6, 26, 26), YARN, pattern=combine(grain((1, -1), 2.0, 0.18, 11), noise(0.05, 11)))
        for k in range(3):
            s.stroke([(8 + k * 3, 9 + k * 5), (24 - k * 2, 14 + k * 4)], 0.9, mat(0xA07A30, glint=False), bevel=0.3, edge=False)
        s.stroke([(24, 22), (27, 26), (30, 28)], 1.0, YARN, bevel=0.4)
        s.pixel(13, 11, (255, 236, 170))
        return s

    # ---------------------------------------------------------------- Jotunheim

    def rune(name):
        def draw():
            s = Sprite(name)
            s.poly([(8, 3), (25, 4), (27, 27), (6, 28), (5, 15)], RUNESTONE, bevel=2.4,
                   pattern=combine(noise(0.08, len(name)), grain((1, 1), 4, 0.06, len(name))))
            for x0, y0, x1, y1 in RUNES[name]:
                s.stroke([(10 + x0 * 1.2, 7 + y0 * 1.3), (10 + x1 * 1.2, 7 + y1 * 1.3)], 1.6, RUNE_GLOW, bevel=0.5, edge=False)
            return s
        return draw

    for name in RUNES:
        items[f"rune_{name}"] = rune(name)

    @item("draupnir")
    def _():
        s = Sprite("draupnir")
        ring = [(16 + 10 * math.cos(a), 17 + 9.5 * math.sin(a)) for a in [math.pi * i / 18 for i in range(37)]]
        s.stroke(ring, 4.2, GOLD, bevel=1.6)
        for k in range(8):                                               # the eight rings it drips
            a = k * math.pi / 4 + 0.3
            s.pixel(int(16 + 10 * math.cos(a)), int(17 + 9.5 * math.sin(a)), (255, 240, 170))
        s.ellipse((13, 26, 19, 31), DARK_GOLD)                          # a drop about to fall
        return s

    @item("gungnir")
    def _():
        s = Sprite("gungnir")
        s.stroke([D(-2, 0), D(27, 0)], 1.8, DARK_WOOD, bevel=0.8)
        for t in (6, 11, 16):                                            # runes carved on the shaft
            s.stroke([D(t, -1), D(t + 1.2, 1)], 0.7, RUNE_GLOW, bevel=0.2, edge=False)
        s.poly(D.pts([(26, -2.2), (29, -2.2), (29, 2.2), (26, 2.2)]), GOLD, bevel=1)
        s.poly(D.pts([(28.5, -2.6), (36.5, 0), (28.5, 2.6)]), STEEL, bevel=1.4)
        gem(s, *D(27.3, 0), 1.1, SAPPHIRE)
        return s


# ---------------------------------------------------------------- status effect icons (18x18)

def _dance():
    s = Sprite("effect_dance", size=18)
    s.stroke([(6, 14), (6, 4), (14, 2), (14, 12)], 1.4, GOLD, bevel=0.5)       # two beamed notes
    s.ellipse((2, 12, 8, 17), GOLD)
    s.ellipse((10, 10, 16, 15), GOLD)
    return s


def _thurisaz():
    s = Sprite("effect_thurisaz", size=18)
    s.stroke([(6, 2), (6, 16)], 1.8, RUNE_GLOW, bevel=0.5, edge=False)
    s.stroke([(6, 5), (12, 9), (6, 13)], 1.8, RUNE_GLOW, bevel=0.5, edge=False)
    return s


EFFECT_ICONS.update(dance=_dance, thurisaz=_thurisaz)
