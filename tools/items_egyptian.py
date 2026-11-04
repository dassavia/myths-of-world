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
CROC = mat(0x5A7030, spread=0.45, glint=False)
CREAM = mat(0xE0D4A0, spread=0.3, glint=False)
SILT = mat(0x2E2824, spread=0.35, glint=False)
CLAY = mat(0xB8643A, spread=0.4, glint=False)
LEAF = mat(0x4AA83A, spread=0.45, glint=False)
CEDAR = mat(0x7A5230, spread=0.38, glint=False)
FIRE = mat(0xF07A2A, spread=0.5)
EMBER = mat(0xC8301E, spread=0.5)
SILVER = mat(0xD8DCE8, spread=0.35)
FALCON = mat(0x7A5432, spread=0.4, glint=False)
GREEN = mat(0x3A9A5A, spread=0.42)


def at(x, y, r):
    return (x - r, y - r, x + r, y + r)


def grain_x():
    """Wood grain along a diagonal handle."""
    from art32 import grain
    return grain((1, -1), 2.5, 0.1, 1)


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


    # ------------------------------------------------ the gifts of the Nile and the crocodile

    @item("gift_of_hapi")
    def _():
        # A clay bowl heaped with black silt, white flecks of bone meal and a green shoot of papyrus.
        s = Sprite("gift_of_hapi")
        s.ellipse((4, 15, 28, 30), CLAY, bevel=2.5)
        s.ellipse((5, 12, 27, 21), SILT, bevel=1.5, pattern=noise(0.12, 4))
        for x, y in ((9, 15), (14, 14), (20, 16), (23, 15), (12, 18), (18, 18)):
            s.ellipse(at(x, y, 0.8), IVORY, edge=False)
        s.stroke([(16, 15), (15.5, 9), (17, 4)], 1.4, LEAF, bevel=0.5)
        s.poly([(17, 4), (21, 1.5), (23, 4), (19, 6)], LEAF, bevel=1)
        s.poly([(15.5, 8), (11, 5), (10, 8), (14, 10)], LEAF, bevel=1)
        s.rect((6, 22, 26, 23.5), mat(0x2A5AB0, spread=0.4, glint=False), bevel=0.5, edge=False)
        return s

    @item("crocodile_hide")
    def _():
        # A stretched hide: the dark scaly back down the middle, the pale square scales of the belly at the edges.
        s = Sprite("crocodile_hide")
        s.poly([(8, 3), (24, 3), (27, 9), (29, 22), (24, 29), (16, 27), (8, 29), (3, 22), (5, 9)], CREAM, bevel=2,
               pattern=scales(3, 0.16))
        s.poly([(12, 4), (20, 4), (22, 12), (21, 26), (16, 25), (11, 26), (10, 12)], CROC, bevel=2.2, pattern=scales(3, 0.24))
        for y in (8, 12, 16, 20):
            s.stroke([(13, y), (19, y)], 1.0, mat(0x2A3418, glint=False), bevel=0.3, edge=False)
        return s

    @item("crocodile_tooth")
    def _():
        s = Sprite("crocodile_tooth")
        s.poly([(10, 26), (20, 27), (21, 22), (20, 14), (17, 7), (14, 3), (13, 10), (11, 18)], IVORY, bevel=2.5)
        s.rect((9, 25, 22, 29), mat(0xB89A6A, glint=False), bevel=1)
        return s

    # ------------------------------------------------ the relics of the gods

    @item("sun_disc")
    def _():
        # The red sun disc of Ra in a ring of gold, the cobra rearing in front of it.
        s = Sprite("sun_disc")
        s.ellipse((2, 2, 30, 30), GOLD, bevel=2)
        s.ellipse((5, 5, 27, 27), mat(0xE0402A, spread=0.45), bevel=3)
        s.ellipse(at(12.5, 12.5, 3), mat(0xFFB060), edge=False)
        s.poly([(14, 30), (18, 30), (18, 22), (20, 18), (17, 15), (14, 18), (15, 22)], GOLD, bevel=1.4)
        s.ellipse(at(16.5, 18, 1), LAPIS)
        return s

    @item("djed_of_osiris")
    def _():
        # The djed pillar, the backbone of Osiris: a column with four cross bars at the top, banded green and gold.
        s = Sprite("djed_of_osiris")
        s.poly([(11, 30), (21, 30), (20, 12), (12, 12)], GREEN, bevel=2, pattern=bands("y", 4, 0.12))
        for y in (3, 6.5, 10):
            s.rect((7, y, 25, y + 2.6), GOLD, bevel=1.2)
        s.rect((9, 1, 23, 3), LAPIS, bevel=0.8)
        for y in (16, 22):
            s.rect((11.5, y, 20.5, y + 1.6), LAPIS, bevel=0.6, edge=False)
        return s

    @item("wing_of_isis")
    def _():
        # A wing of the goddess: rows of feathers in carnelian, lapis, turquoise and gold.
        s = Sprite("wing_of_isis")
        rows = [(CARNELIAN, 4), (LAPIS, 9), (TURQUOISE, 14), (GOLD, 19)]
        for material, y in rows:
            s.poly([(2, y), (28, y - 3 + (y - 4) * 0.25), (30, y + 2), (4, y + 7)], material, bevel=1.4,
                   pattern=bands("x", 3, 0.18))
        s.poly([(2, 3), (10, 2), (8, 27), (2, 26)], GOLD, bevel=1.4)
        return s

    @item("falcon_feather")
    def _():
        # A falcon's flight feather, brown barred with cream, on a white quill.
        s = Sprite("falcon_feather")
        s.poly(D.pts([(6, 0), (14, 4.5), (26, 4.2), (33, 0.5), (26, -3.2), (14, -3.6)]), FALCON, bevel=2,
               pattern=bands("x", 3, 0.3))
        s.stroke([D(1, 0), D(31, 0)], 1.1, IVORY, bevel=0.4)
        return s

    @item("feather_of_maat")
    def _():
        # The ostrich feather of Ma'at, white and curling over at the top, set in a quill of gold.
        s = Sprite("feather_of_maat")
        s.poly([(13, 28), (19, 28), (22, 18), (24, 9), (22, 3), (16, 1), (12, 4), (17, 6), (18, 12), (15, 20)],
               IVORY, bevel=2.5, pattern=bands("y", 2, 0.08))
        s.stroke([(16, 29), (17.5, 18), (19, 8)], 0.9, mat(0xC8C0A8, glint=False), bevel=0.3, edge=False)
        s.rect((14, 27, 18.5, 31), GOLD, bevel=1)
        return s

    @item("tablet_of_thoth")
    def _():
        # A tablet of lapis written with words of power, the crescent and disc of the moon above them.
        s = Sprite("tablet_of_thoth")
        s.poly([(5, 6), (27, 4), (28, 28), (6, 29)], LAPIS, bevel=2, pattern=noise(0.06, 2))
        for y in (12, 16.5, 21, 25):
            for x in (9, 14, 19, 24):
                s.ellipse(at(x, y, 1.0), GOLD, edge=False)
        s.ellipse(at(16, 6.5, 4.2), SILVER)
        s.ellipse(at(16, 5, 3.4), LAPIS, edge=False)
        return s

    @item("claw_of_bastet")
    def _():
        s = Sprite("claw_of_bastet")
        s.poly([(8, 28), (17, 29), (21, 22), (22, 14), (20, 7), (15, 2), (16, 9), (15, 17), (11, 23)], EBONY, bevel=2.5)
        s.rect((7, 26, 18, 30), GOLD, bevel=1)
        s.ellipse(at(12.5, 28, 1), TURQUOISE, edge=False)
        return s

    @item("fang_of_sobek")
    def _():
        # A great fang of the crocodile god, green at the root, bound in gold.
        s = Sprite("fang_of_sobek")
        s.poly([(9, 25), (22, 26), (24, 19), (22, 11), (18, 5), (14, 1), (13, 9), (10, 17)], IVORY, bevel=2.8)
        s.poly([(9, 25), (22, 26), (23, 21), (10, 20)], GREEN, bevel=1.5, pattern=scales(2, 0.2))
        s.rect((8, 25, 23, 29.5), GOLD, bevel=1.2)
        return s

    @item("horn_of_hathor")
    def _():
        # A cow's horn, ivory curving upwards, the sun disc of gold at its root.
        s = Sprite("horn_of_hathor")
        s.stroke([(6, 26), (10, 15), (13, 8), (19, 3), (26, 2)], 4.2, IVORY, bevel=1.6, pattern=bands("x", 3, 0.1))
        s.stroke([(23, 2.3), (28, 2.5)], 2.2, mat(0x8A7A5A, glint=False), bevel=0.8)
        s.ellipse(at(8.5, 25, 5), mat(0xE0402A), bevel=2)
        s.ellipse(at(8.5, 25, 6.2), GOLD, bevel=1.4)
        s.ellipse(at(8.5, 25, 4.2), mat(0xE0402A), bevel=2)
        return s

    @item("chisel_of_ptah")
    def _():
        s = Sprite("chisel_of_ptah")
        s.stroke([D(1, 0), D(15, 0)], 4.0, CEDAR, bevel=1.4, pattern=grain_x())
        s.stroke([D(12, 0), D(14, 0)], 4.4, LAPIS, bevel=0.8)
        s.poly(D.pts([(14, -1.4), (29, -1.4), (33, -2.4), (33, 2.4), (29, 1.4), (14, 1.4)]), METEORIC, bevel=1.6,
               pattern=noise(0.08, 6))
        return s

    @item("ember_of_sekhmet")
    def _():
        # A coal of the desert wind, glowing in its cracks, with a tongue of flame above it.
        s = Sprite("ember_of_sekhmet")
        s.poly([(16, 2), (21, 9), (20, 14), (24, 11), (24, 18), (8, 18), (9, 11), (12, 14)], FIRE, bevel=2)
        s.ellipse((5, 13, 27, 30), EMBER, bevel=3, pattern=noise(0.14, 8))
        for a, b in (((10, 20), (16, 24)), ((16, 24), (22, 19)), ((15, 24), (15, 28))):
            s.stroke([a, b], 1.0, mat(0xFFD060), bevel=0.3, edge=False)
        return s

    # ------------------------------------------------ the weapons of the gods

    @item("staff_of_ra")
    def _():
        # A staff of gold banded with lapis, crowned with the red sun disc of Ra in its golden ring.
        s = Sprite("staff_of_ra")
        s.stroke([D(0, 0), D(26, 0)], 2.4, GOLD, bevel=1, pattern=bands("x", 3, 0.12))
        for t in (6, 13, 20):
            s.stroke([D(t, -1.6), D(t, 1.6)], 1.2, LAPIS, bevel=0.4, edge=False)
        s.ellipse(at(*D(31), 6.2), GOLD, bevel=1.6)
        s.ellipse(at(*D(31), 4.6), mat(0xE0402A), bevel=2.4)
        s.ellipse(at(*D(30, 1.5), 1.3), mat(0xFFB060), edge=False)
        return s

    @item("flail_of_osiris")
    def _():
        # The nekhakha, the flail of the king: a handle banded with gold and lapis and three strands of beads.
        s = Sprite("flail_of_osiris")
        s.stroke([D(0, 0), D(17, 0)], 2.6, GOLD, bevel=1, pattern=bands("x", 2, 0.15))
        for t in (4, 8, 12):
            s.stroke([D(t, -1.7), D(t, 1.7)], 1.2, LAPIS, bevel=0.4, edge=False)
        s.ellipse(at(*D(18), 2.2), GOLD)
        x0, y0 = D(18)
        for k in range(3):                                               # three strands falling to the right
            for i in range(5):
                material = (GREEN, GOLD, CARNELIAN, LAPIS)[(i + k) % 4]
                s.ellipse(at(x0 + 2.4 + 2.3 * i, y0 - 3.2 + k * 3.4 + 1.1 * i, 1.05), material, bevel=0.8)
        return s

    @item("sceptre_of_isis")
    def _():
        # The papyrus sceptre of Isis: a turquoise shaft opening into a golden umbel, a wing of the goddess beside it.
        s = Sprite("sceptre_of_isis")
        s.stroke([D(0, 0), D(24, 0)], 2.4, TURQUOISE, bevel=1, pattern=bands("x", 4, 0.12))
        s.poly(D.pts([(23, -1.5), (31, -5.5), (34, -1), (34, 1), (31, 5.5), (23, 1.5)]), GOLD, bevel=1.6,
               pattern=bands("y", 2, 0.12))
        s.poly(D.pts([(14, 2), (24, 9), (26, 4), (18, 1.5)]), CARNELIAN, bevel=1)
        s.poly(D.pts([(13, 1.6), (22, 6), (23, 3), (17, 1.4)]), LAPIS, bevel=0.8)
        s.ellipse(at(*D(3), 1.8), GOLD)
        return s

    @item("glaive_of_anubis")
    def _():
        # A long shaft of ebony banded with gold, the long curved blade of meteoric iron, a jackal's head at the joint.
        s = Sprite("glaive_of_anubis")
        s.stroke([D(0, 0), D(23, 0)], 2.2, EBONY, bevel=1, pattern=bands("x", 3, 0.1))
        for t in (5, 11, 17):
            s.stroke([D(t, -1.5), D(t, 1.5)], 1.0, GOLD, bevel=0.4, edge=False)
        s.poly(D.pts([(21, -1.4), (29, -2.8), (35, -0.5), (33, 2.2), (27, 3.2), (21, 1.4)]), METEORIC, bevel=1.8,
               pattern=noise(0.08, 5))
        s.stroke([D(23, 1.4), D(32, 0.4)], 0.8, mat(0xD8E2F2, spread=0.3), bevel=0.3, edge=False)
        s.poly(D.pts([(19, -2.4), (23, -2.4), (24, -4.5), (21.5, -3.2), (19, -4.5)]), EBONY, bevel=1)
        s.ellipse(at(*D(21, -1.8), 0.8), GOLD, edge=False)
        return s

    @item("staff_of_thoth")
    def _():
        # A staff of ebony with the crescent and the full moon of Thoth in silver on top, banded with turquoise.
        s = Sprite("staff_of_thoth")
        s.stroke([D(0, 0), D(25, 0)], 2.2, EBONY, bevel=1, pattern=bands("x", 3, 0.1))
        for t in (6, 12, 18):
            s.stroke([D(t, -1.5), D(t, 1.5)], 1.0, TURQUOISE, bevel=0.4, edge=False)
        cx, cy = D(30.5)
        s.add(s._mask(lambda d, k: d.chord([(cx - 6) * k, (cy - 6) * k, (cx + 6) * k - 1, (cy + 6) * k - 1], 20, 250,
                                           fill=255)), SILVER, bevel=1.4)
        s.ellipse(at(cx + 0.8, cy - 0.8, 3.6), mat(0xF4F6FF, spread=0.3), bevel=2)
        return s

    @item("dagger_of_bastet")
    def _():
        # A short curved dagger: a hilt of gold with a cat's head for a pommel, a blade of meteoric iron.
        s = Sprite("dagger_of_bastet")
        s.poly(D.pts([(3, -1.4), (10, -1.4), (10, 1.4), (3, 1.4)]), EBONY, bevel=1, pattern=bands("x", 2, 0.14))
        s.ellipse(at(*D(2.5), 2.6), GOLD)
        s.poly(D.pts([(0.5, -2.2), (1.2, -3.8), (2.4, -2.4)]), GOLD, bevel=0.5)
        s.poly(D.pts([(0.5, 2.2), (1.2, 3.8), (2.4, 2.4)]), GOLD, bevel=0.5)
        s.poly(D.pts([(9.5, -3.2), (12, -3.2), (12, 3.2), (9.5, 3.2)]), GOLD, bevel=1.2)
        s.poly(D.pts([(12, -2), (19, -2.6), (24, -1.5), (27, 1.2), (19, 2), (12, 2)]), METEORIC, bevel=1.8,
               pattern=noise(0.08, 7))
        s.ellipse(at(*D(10.8), 1.0), TURQUOISE, edge=False)
        return s

    @item("khopesh_of_sobek")
    def _():
        # The sickle-sword of Sobek: a green-bronze hooked blade set with crocodile teeth along the edge.
        s = Sprite("khopesh_of_sobek")
        s.poly(D.pts([(1.5, -1.6), (8.5, -1.6), (8.5, 1.6), (1.5, 1.6)]), CROC, bevel=1, pattern=scales(2, 0.2))
        s.ellipse(at(*D(1.2), 2.1), GOLD)
        s.poly(D.pts([(8.5, -2.6), (10.5, -2.6), (10.5, 2.6), (8.5, 2.6)]), GOLD, bevel=1)
        bronze = mat(0x6A9A6A, spread=0.5)
        s.poly(D.pts([(10.5, -1.4), (18, -1.4), (18, 1.4), (10.5, 1.4)]), bronze, bevel=1.4, pattern=noise(0.08, 3))
        blade = [(17.5, -1.6), (22, -3.5), (27, -4.2), (31.5, -2.6), (34, 0.5), (33, 4.5), (30.5, 2.5), (27, 0.6),
                 (22.5, 0.4), (19, 1.6)]
        s.poly(D.pts(blade), bronze, bevel=2.2, pattern=noise(0.08, 5))
        for t, w in ((21, -3.6), (25, -4.4), (29, -4.0)):
            s.poly([D(t - 0.8, w + 0.4), D(t + 0.8, w + 0.4), D(t, w - 1.6)], IVORY, bevel=0.5)
        return s

    @item("sceptre_of_hathor")
    def _():
        # A sceptre crowned with a sistrum: the loop of gold with its jingling bars between the cow horns of Hathor.
        s = Sprite("sceptre_of_hathor")
        s.stroke([D(0, 0), D(20, 0)], 2.2, CEDAR, bevel=1, pattern=bands("x", 3, 0.1))
        s.stroke([D(18, -1.6), D(18, 1.6)], 1.4, TURQUOISE, bevel=0.4)
        cx, cy = D(27.5)
        loop = s._mask(lambda d, k: d.ellipse([(cx - 5) * k, (cy - 6) * k, (cx + 5) * k - 1, (cy + 6) * k - 1], fill=255))
        loop &= ~s._mask(lambda d, k: d.ellipse([(cx - 3) * k, (cy - 4) * k, (cx + 3) * k - 1, (cy + 4) * k - 1], fill=255))
        s.add(loop, GOLD, bevel=1.6)
        for dy in (-2, 0, 2):
            s.stroke([(cx - 3.5, cy + dy), (cx + 3.5, cy + dy)], 0.8, SILVER, bevel=0.3, edge=False)
        s.stroke([D(21, -6), D(23, -3), D(22, 0)], 1.6, IVORY, bevel=0.6)
        s.stroke([D(21, 6), D(23, 3), D(22, 0)], 1.6, IVORY, bevel=0.6)
        return s

    @item("axe_of_ptah")
    def _():
        # The epsilon axe of the craftsman: a haft banded with lapis and green, a wide half-moon edge of meteoric iron
        # lashed to it, the chisel of Ptah set in the blade.
        s = Sprite("axe_of_ptah")
        s.stroke([D(0, 0), D(31, 0)], 2.4, CEDAR, bevel=1.2, pattern=grain_x())
        for t in (3, 9, 15):
            s.stroke([D(t, -1.6), D(t, 1.6)], 1.2, LAPIS if t != 9 else GREEN, bevel=0.4, edge=False)
        head = [(20.5, 1), (30, 1), (33.5, 5), (33.5, 12), (30.5, 13), (26.5, 12), (23.5, 8.5), (20.5, 5)]
        s.poly(D.pts(head), METEORIC, bevel=2.2, pattern=noise(0.09, 17))
        s.poly(D.pts([(22.5, -1.2), (28.5, -1.2), (28, -3.6), (23, -3.6)]), GOLD, bevel=1.2)
        s.stroke([D(25, 3), D(30, 8)], 1.0, GOLD, bevel=0.3, edge=False)
        s.ellipse(at(*D(27.5, 6), 1.1), LAPIS, edge=False)
        return s

    @item("spear_of_sekhmet")
    def _():
        # A spear with a shaft of red-lacquered wood, a leaf blade glowing like a coal, and a tassel of red.
        s = Sprite("spear_of_sekhmet")
        s.stroke([D(0, 0), D(26, 0)], 2.0, mat(0x8A2A1E, spread=0.4, glint=False), bevel=1, pattern=bands("x", 3, 0.1))
        for t in (4, 24):
            s.stroke([D(t, -1.5), D(t, 1.5)], 1.2, GOLD, bevel=0.4, edge=False)
        s.poly(D.pts([(24, -1.8), (29, -2.8), (35, 0), (29, 2.8), (24, 1.8)]), FIRE, bevel=1.8, pattern=noise(0.1, 9))
        s.stroke([D(25.5, 0), D(32, 0)], 0.9, mat(0xFFE080), bevel=0.3, edge=False)
        s.poly(D.pts([(22, 1.6), (21, 6), (19, 6.5), (20.5, 1.6)]), EMBER, bevel=0.8)
        return s

    def bow(stage):
        # The recurved bow of Horus: limbs of dark wood bound with gold, falcon feathers at the grip, a string of
        # gut; drawn, an arrow with a falcon fletching lies on the string.
        name = "bow_of_horus" + ("" if stage is None else f"_pulling_{stage}")
        s = Sprite(name)
        apex = 22.0
        limb = [D(apex - (t / 13) ** 2 * 10, t) for t in range(-13, 14)]
        s.stroke(limb, 2.4, EBONY, bevel=1, pattern=bands("x", 3, 0.1))
        for side in (-1, 1):                                             # the recurved tips
            s.stroke([D(apex - 10, side * 13), D(apex - 9, side * 14.5)], 1.8, EBONY, bevel=0.6)
        for t in (-12, -7, 7, 12):
            s.ellipse(at(*D(apex - (t / 13) ** 2 * 10, t), 1.4), GOLD, edge=False)
        s.poly(D.pts([(apex - 2.2, -2.4), (apex + 1.2, -2.4), (apex + 1.2, 2.4), (apex - 2.2, 2.4)]), GOLD, bevel=1)
        s.poly(D.pts([(apex - 4.5, 2.4), (apex - 1.5, 7.5), (apex, 6), (apex - 1, 2.4)]), FALCON, bevel=0.8)
        pull = {None: 0.0, 0: 3.0, 1: 5.0, 2: 7.0}[stage]
        nock = apex - 10 - pull
        string = mat(0xE8E0C8, spread=0.3, glint=False)
        s.stroke([D(apex - 10, -13), D(nock, 0), D(apex - 10, 13)], 0.8, string, bevel=0.2, edge=False)
        if stage is not None:
            s.stroke([D(nock, 0), D(nock + 20, 0)], 1.0, CEDAR, bevel=0.3)
            s.poly(D.pts([(nock + 19, -1.6), (nock + 23, 0), (nock + 19, 1.6)]), METEORIC, bevel=0.8)
            s.poly(D.pts([(nock, 0), (nock + 3, -1.8), (nock + 4, 0), (nock + 3, 1.8)]), FALCON, bevel=0.5)
        return s

    for stage in (None, 0, 1, 2):
        items["bow_of_horus" + ("" if stage is None else f"_pulling_{stage}")] = (lambda st: lambda: bow(st))(stage)
