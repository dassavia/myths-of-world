"""The relics and treasures of the Duat, drawn at 32x32 (see gen_art32_items.py and art32.py). The other items of the
Duat are drawn at 16x16 in textures_egyptian.py and enlarged by hd_textures.py."""
from art32 import Diagonal, Sprite, bands, mat, noise, scales

D = Diagonal()

GOLD = mat(0xE8B43C)
LAPIS = mat(0x2A5AB0, spread=0.42)
TURQUOISE = mat(0x3AB8A8, spread=0.4)
CARNELIAN = mat(0xD0482A)
METEORIC = mat(0x8E9AB0, spread=0.5)
EBONY = mat(0x2A2440, spread=0.4, glint=False)
IVORY = mat(0xF2ECDA, spread=0.3)


def at(x, y, r):
    return (x - r, y - r, x + r, y + r)


def register(items):
    def item(name):
        def wrap(fn):
            items[name] = fn
            return fn
        return wrap

    @item("khopesh")
    def _():
        # The sickle-sword: a straight neck from the hilt, then the blade curving out like a hook.
        s = Sprite("khopesh")
        s.poly(D.pts([(1.5, -1.6), (8.5, -1.6), (8.5, 1.6), (1.5, 1.6)]), EBONY, bevel=1, pattern=bands("x", 2, 0.14))
        for t in (3, 6):
            s.stroke([D(t, -1.5), D(t, 1.5)], 0.9, GOLD, bevel=0.4, edge=False)
        s.ellipse(at(*D(1.2), 2.1), GOLD)
        s.poly(D.pts([(8.5, -2.6), (10.5, -2.6), (10.5, 2.6), (8.5, 2.6)]), GOLD, bevel=1)
        s.poly(D.pts([(10.5, -1.4), (18, -1.4), (18, 1.4), (10.5, 1.4)]), METEORIC, bevel=1.4, pattern=noise(0.08, 3))
        blade = [(17.5, -1.6), (22, -3.5), (27, -4.2), (31.5, -2.6), (34, 0.5), (33, 4.5), (30.5, 2.5), (27, 0.6),
                 (22.5, 0.4), (19, 1.6)]
        s.poly(D.pts(blade), METEORIC, bevel=2.2, pattern=noise(0.08, 5))
        s.stroke([D(21, -1.2), D(27, -2.4), D(31.5, -0.8)], 0.8, mat(0xD8E2F2, spread=0.3), bevel=0.3, edge=False,
                 base=0.8)
        s.ellipse(at(*D(9.5), 1.2), LAPIS)
        return s

    @item("was_sceptre")
    def _():
        # A straight staff of ebony with the head of the Set animal on top and a forked foot.
        s = Sprite("was_sceptre")
        s.stroke([D(3, 0), D(30, 0)], 2.2, EBONY, bevel=1, pattern=bands("x", 3, 0.1))
        s.stroke([D(3, 0), D(0, -3)], 1.8, EBONY, bevel=0.8)
        s.stroke([D(3, 0), D(0, 3)], 1.8, EBONY, bevel=0.8)
        for t in (8, 16, 24):
            s.stroke([D(t, -1.6), D(t, 1.6)], 1.0, GOLD, bevel=0.4, edge=False)
        s.poly(D.pts([(29, -1.6), (33.5, -4.5), (35, -3.2), (32, 0.5), (30, 1.6)]), EBONY, bevel=1.6)
        s.ellipse(at(*D(32.5, -2.6), 0.9), CARNELIAN)
        s.stroke([D(29, -1.2), D(29, 1.2)], 1.2, GOLD, bevel=0.4)
        return s

    @item("ankh")
    def _():
        s = Sprite("ankh")
        loop = s._mask(lambda d, k: d.ellipse([9 * k, 1 * k, 23 * k - 1, 15 * k - 1], fill=255))
        loop &= ~s._mask(lambda d, k: d.ellipse([12.5 * k, 4 * k, 19.5 * k - 1, 12.5 * k - 1], fill=255))
        s.add(loop, GOLD, bevel=2)
        s.rect((4, 14, 28, 18), GOLD, bevel=1.8)
        s.poly([(14, 14), (18, 14), (19, 30), (13, 30)], GOLD, bevel=2)
        s.ellipse(at(16, 16, 1.6), LAPIS)
        return s

    @item("nemes")
    def _():
        # The striped headcloth: gold and lapis, the lappets falling to the chest, the uraeus on the brow.
        s = Sprite("nemes")
        s.poly([(8, 4), (16, 2), (24, 4), (27, 11), (29, 27), (23, 29), (22, 16), (10, 16), (9, 29), (3, 27), (5, 11)],
               GOLD, bevel=3, pattern=bands("y", 3, 0.22))
        for y in (7, 13, 19, 25):
            s.stroke([(4, y), (28, y)], 1.4, LAPIS, bevel=0.5, edge=False)
        s.rect((9, 9, 23, 16), mat(0x14141E, glint=False), bevel=0.5, edge=False)
        s.rect((6, 7.5, 26, 10), GOLD, bevel=1)
        s.poly([(15, 3), (17, 3), (18, 7), (16, 9), (14, 7)], GOLD, bevel=1)
        s.ellipse(at(16, 5.5, 1.2), CARNELIAN)
        return s

    @item("pectoral_of_ra")
    def _():
        # A broad collar in bands of gold, lapis and turquoise with the red sun disc of Ra between two falcon wings.
        s = Sprite("pectoral_of_ra")
        for r, material in ((14, GOLD), (11.5, LAPIS), (9, TURQUOISE), (6.5, GOLD)):
            s.add(s._mask(lambda d, k, r=r: d.chord([(16 - r) * k, (2 - r) * k, (16 + r) * k - 1, (2 + r) * k - 1],
                                                    0, 180, fill=255)), material, bevel=1.4)
        for side in (-1, 1):
            s.poly([(16 + side * 3, 22), (16 + side * 13, 18), (16 + side * 14, 22), (16 + side * 6, 27)], GOLD,
                   bevel=1.6, pattern=bands("x", 2, 0.15))
        s.ellipse(at(16, 22, 5), CARNELIAN)
        s.ellipse(at(14.5, 20.5, 1.6), mat(0xFFB060))
        return s

    @item("eye_of_horus")
    def _():
        s = Sprite("eye_of_horus")
        s.ellipse((4, 9, 27, 21), IVORY)
        s.ellipse(at(15.5, 15, 4.2), mat(0x14141E))
        s.ellipse(at(14.5, 14, 1.2), mat(0xFFFFFF))
        s.stroke([(2, 8), (16, 5.5), (29, 8)], 1.8, LAPIS, bevel=0.6)
        s.stroke([(4, 15), (3, 15), (27, 15), (30, 13)], 1.4, LAPIS, bevel=0.5, edge=False)
        s.stroke([(16, 21), (16, 28)], 1.6, LAPIS, bevel=0.5)
        s.stroke([(22, 21), (26, 26), (23, 29)], 1.6, LAPIS, bevel=0.5)
        s.ellipse(at(29.5, 8, 1.4), GOLD)
        return s

    @item("apep_scale")
    def _():
        s = Sprite("apep_scale")
        s.poly([(16, 2), (28, 11), (25, 26), (16, 30), (7, 26), (4, 11)], mat(0x3A2250, spread=0.45), bevel=3,
               pattern=scales(3, 0.2))
        s.stroke([(16, 5), (16, 27)], 1.0, mat(0x1A0A26), bevel=0.4, edge=False)
        s.stroke([(4, 11), (16, 2), (28, 11)], 1.4, mat(0xC0262E), bevel=0.5)
        return s
