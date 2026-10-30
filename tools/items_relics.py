"""The relics, trophies, foods, potions and books, drawn at 32x32 (see gen_art32_items.py and art32.py)."""
import math

from art32 import Diagonal, Sprite, bands, combine, fur, grain, mat, noise, scales

D = Diagonal()

WOOD = mat(0x7A5230, spread=0.38, glint=False)
DARK_WOOD = mat(0x4E3220, spread=0.35, glint=False)
LEATHER = mat(0x6B3A24, spread=0.4, glint=False)
GOLD = mat(0xE8B43C)
DARK_GOLD = mat(0xB0802A)
SILVER = mat(0xC9CED8)
BONE = mat(0xE6DCC4, spread=0.42)
IVORY = mat(0xEDE2C2, spread=0.4)
PAPER = mat(0xEFE3C6, spread=0.25, glint=False)
GLASS = mat(0xD8ECF4, spread=0.3)
CORK = mat(0xB08458, spread=0.35, glint=False)
LEAF = mat(0x4E8A2E, spread=0.45, glint=False)
RED = mat(0xC0262E)
BLOOD = mat(0x8A1A1E, spread=0.4, glint=False)
EMERALD = mat(0x2FB36A)
RUBY = mat(0xD8283A)
SAPPHIRE = mat(0x3A6AE0)
AMBER = mat(0xF0A22A)
ICE = mat(0xA8E4F8, spread=0.4)
FIRE = mat(0xF07A1E, spread=0.45)
STEEL = mat(0xB8C4D0, spread=0.5)
DARK_STEEL = mat(0x4C5262, spread=0.5)
LION = mat(0xC8963E, spread=0.45, glint=False)
LION_MANE = mat(0x8A5A22, spread=0.4, glint=False)
GREY_FUR = mat(0x8A8C90, spread=0.45, glint=False)
CYAN = mat(0x56D2F2)


def at(x, y, r):
    return (x - r, y - r, x + r, y + r)


def gem(s, x, y, r, material):
    s.ellipse(at(x, y, r), material)


# ---------------------------------------------------------------- shared shapes

def book(name, cover, accent, emblem):
    s = Sprite(name)
    s.poly([(7, 5), (26, 4), (27, 26), (8, 28)], PAPER, bevel=1.2, pattern=bands("y", 2, 0.08))
    s.poly([(4, 6), (24, 4.5), (25, 26.5), (5, 28.5)], cover, bevel=2.2, pattern=noise(0.06, len(name)))
    s.poly([(4, 6), (8, 5.6), (9, 28.2), (5, 28.5)], mat(cover.tones[2]), bevel=1.2)
    for y in (9, 24):
        s.stroke([(4.5, y), (8.5, y - 0.3)], 1.1, accent, bevel=0.5)
    emblem(s)
    return s


def bottle(name, liquid, glow=None, round_=True):
    s = Sprite(name)
    if round_:
        s.ellipse((6, 11, 26, 30), GLASS, contrast=0.6)
        s.ellipse((8, 15, 24, 28.5), liquid)
    else:
        s.poly([(10, 12), (22, 12), (25, 16), (25, 29), (7, 29), (7, 16)], GLASS, bevel=2, contrast=0.6)
        s.poly([(8.5, 18), (23.5, 18), (23.5, 28), (8.5, 28)], liquid, bevel=2)
    s.rect((12.5, 5, 19.5, 12.5), GLASS, bevel=1.2, contrast=0.6)
    s.rect((12, 2.5, 20, 6.5), CORK, bevel=1.2, pattern=noise(0.08, 5))
    s.stroke([(10, 18), (10.5, 23)], 1.2, mat(0xFFFFFF), bevel=0.3, edge=False)
    if glow:
        s.pixel(18, 21, glow)
        s.pixel(14, 24, glow)
    return s


def horn(name, material, path, base=1.0, tip_r=0.6, rings=(), ring_mat=None, mouth=None):
    """A horn along {@code path} (t -> x, y), thin at t=0 and {@code base} times as wide at the mouth."""
    s = Sprite(name)
    pts = []
    for i in range(21):
        t = i / 20
        x, y = path(t)
        x2, y2 = path(min(1, t + 0.05)) if t < 1 else path(t)
        x1, y1 = path(max(0, t - 0.05))
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy) or 1
        w = tip_r + 5.0 * base * t ** 0.9
        pts.append((x, y, -dy / n * w, dx / n * w))
    s.poly([(x + nx, y + ny) for x, y, nx, ny in pts] + [(x - nx, y - ny) for x, y, nx, ny in pts[::-1]], material,
           bevel=3, pattern=bands("x", 4, 0.08))
    for k in rings:
        x, y, nx, ny = pts[k]
        s.stroke([(x + nx, y + ny), (x - nx, y - ny)], 1.4, ring_mat, bevel=0.6)
    if mouth:
        x, y, nx, ny = pts[-1]
        s.stroke([(x + nx * 0.8, y + ny * 0.8), (x - nx * 0.8, y - ny * 0.8)], 2.2, mouth, bevel=1, edge=False)
    return s


def fang(name, base, tip=None, curve=1.0, root=None):
    """A fang or claw: a cone from its sharp tip (bottom left) curving up to its root (top right)."""
    s = horn(name, base, lambda t: (6 + 18 * t + 4 * curve * math.sin(math.pi * t), 27 - 21 * t + 3 * curve
                                    * math.sin(math.pi * t)), base=0.85, tip_r=0.5,
             rings=(20,) if root else (), ring_mat=root)
    if tip:
        s.stroke([(7.2, 26.2), (10, 23)], 1.3, tip, bevel=0.5)
    return s


def feather(name, vane, shaft, stripes=None, seed=0):
    s = Sprite(name)
    left, right = [], []
    for i in range(15):
        t = i / 14
        cx, cy = 26 - 19 * t, 4 + 22 * t
        w = 6.5 * math.sin(math.pi * min(1, t * 1.15)) + 0.6
        left.append((cx - w * 0.75, cy - w * 0.66))
        right.append((cx + w * 0.75, cy + w * 0.66))
    s.poly(left + right[::-1], vane, bevel=2.5, pattern=combine(grain((1, 1), 2, 0.12, seed), stripes or noise(0.02)))
    for k in (0.35, 0.6):
        i = int(k * 14)
        s.stroke([left[i], (left[i][0] - 1.5, left[i][1] + 2.2)], 1, mat(vane.tones[0]), bevel=0.3, edge=False)
    s.stroke([(27, 3), (6.5, 27.5), (4, 30)], 1.0, shaft, bevel=0.5, edge=False)
    return s


def egg(name, shell, pattern=None, marks=None):
    s = Sprite(name)
    s.ellipse((7, 4, 25, 29), shell, pattern=pattern)
    if marks:
        marks(s)
    return s


# ---------------------------------------------------------------- the items

def register(items):
    def item(name):
        def wrap(fn):
            items[name] = fn
            return fn
        return wrap

    @item("ambrosia")
    def _():
        s = Sprite("ambrosia")
        s.ellipse((4, 14, 28, 29), mat(0xE8C26A, spread=0.35, hue_shift=0.02), dome=(16, 21, 12, 7))
        s.ellipse((6, 9, 26, 22), mat(0xF6E2A0, spread=0.3, hue_shift=0.02), dome=(16, 15, 10, 6))
        s.ellipse((11, 5, 21, 13), mat(0xFFF4CC, spread=0.25, hue_shift=0.01))
        for x, y in ((9, 15), (22, 13), (16, 19), (13, 11), (24, 20)):
            s.pixel(x, y, (255, 255, 240))
        return s

    @item("barrow_crown")
    def _():
        s = Sprite("barrow_crown")
        s.poly([(3, 26), (3, 12), (8, 18), (12, 8), (16, 16), (20, 8), (24, 18), (29, 12), (29, 26)], DARK_GOLD,
               bevel=2.5, pattern=noise(0.1, 7))
        s.rect((3, 21, 29, 27), GOLD, bevel=1.5)
        for x, g in ((8, RUBY), (16, SAPPHIRE), (24, EMERALD)):
            gem(s, x, 24, 1.8, g)
        for x in (3, 12, 20, 29):
            gem(s, x, 11 if x in (3, 29) else 8, 1.4, GOLD)
        return s

    @item("bident_of_hades")
    def _():
        s = Sprite("bident")
        s.stroke([D(-1, 0), D(26, 0)], 2.0, DARK_STEEL, bevel=1)
        s.poly(D.pts([(24, -6), (27, -6), (27, 6), (24, 6)]), DARK_STEEL, bevel=1.5)
        for side in (-4.5, 4.5):
            s.poly(D.pts([(26.5, side - 1.3), (34, side - 0.6), (35.5, side), (34, side + 0.6), (26.5, side + 1.3)]),
                   STEEL, bevel=1.2)
        gem(s, *D(25.5, 0), 1.6, CYAN)
        for t in (6, 12, 18):
            s.stroke([D(t, -1), D(t + 1, 1)], 0.8, mat(0x2C3040), bevel=0.3, edge=False)
        return s

    @item("brisingamen")
    def _():
        s = Sprite("brisingamen")
        pts = [(16 + 12 * math.cos(a), 8 + 10 * math.sin(a)) for a in [math.pi * i / 16 for i in range(17)]]
        s.stroke(pts, 1.8, GOLD, bevel=0.8)
        for i in range(1, 16, 3):
            gem(s, *pts[i], 1.5, AMBER)
        s.poly([(11, 17), (21, 17), (16, 29)], GOLD, bevel=2)
        gem(s, 16, 21, 3, AMBER)
        return s

    @item("cerberus_fang")
    def _():
        return fang("cerberus_fang", BONE, tip=BLOOD, root=mat(0x5A1E1E, glint=False))

    @item("fenrir_fang")
    def _():
        return fang("fenrir_fang", mat(0xD8DCE6), tip=mat(0x8FB0E0), curve=1.2, root=GREY_FUR)

    @item("garm_fang")
    def _():
        return fang("garm_fang", mat(0xD6CDB6), tip=BLOOD, curve=0.7, root=mat(0x3A2A2A, glint=False))

    @item("upyr_fang")
    def _():
        return fang("upyr_fang", mat(0xF0ECE4), tip=RED, curve=0.4)

    @item("troll_tusk")
    def _():
        return fang("troll_tusk", mat(0xD8CBA6, spread=0.45), curve=1.5, root=mat(0x6E7A4A, glint=False))

    @item("codex")
    def _():
        def emblem(s):
            gem(s, 15.5, 16, 5, GOLD)
            gem(s, 15.5, 16, 2.5, AMBER)
            for a in range(8):
                x, y = 15.5 + 7.5 * math.cos(a * math.pi / 4), 16 + 7.5 * math.sin(a * math.pi / 4)
                s.pixel(int(x), int(y), (255, 214, 90))
            s.rect((24, 13, 27.5, 19), GOLD, bevel=1)
        return book("codex", mat(0x7A1E22, spread=0.4, glint=False), GOLD, emblem)

    def journal(name, cover, emblem_colour, complete):
        def emblem(s):
            s.rect((12, 9, 21, 12), mat(emblem_colour), bevel=1)
            s.rect((12, 20, 21, 22), mat(emblem_colour), bevel=1)
            s.stroke([(14, 14), (19, 14), (19, 17), (14, 17)], 1.2, mat(emblem_colour), bevel=0.5)
            if complete:
                for x, y in ((11, 7), (22, 7), (11, 24), (22, 24)):
                    s.pixel(x, y, (255, 240, 170))
        return lambda: book(name, mat(cover, spread=0.4, glint=False), GOLD, emblem)

    for vol, (cover, cover_done) in {"greek": (0x6E4A2A, 0x4A2E7A), "norse": (0x4A5A6E, 0x8A2228),
                                     "slavic": (0x8A2228, 0x23407A)}.items():
        items[f"{vol}_journal"] = journal(f"{vol}_journal", cover, 0xE8B43C, False)
        items[f"{vol}_journal_complete"] = journal(f"{vol}_journal_complete", cover_done, 0xF4CF5A, True)

    @item("cyclops_eye")
    def _():
        s = Sprite("cyclops_eye")
        s.ellipse((4, 4, 28, 28), mat(0xF2ECE6, spread=0.35))
        s.ellipse((10, 10, 22, 22), mat(0x7A4A1E, spread=0.45))
        s.ellipse((13, 13, 19, 19), mat(0x140C08, spread=0.2, glint=False), round_=False)
        for x0, y0, x1, y1 in ((5, 15, 10, 14), (22, 18, 27, 20), (14, 5, 13, 9), (18, 27, 19, 23)):
            s.stroke([(x0, y0), (x1, y1)], 0.6, mat(0xC04040, glint=False), bevel=0.2, edge=False)
        s.pixel(14, 13, (255, 255, 255))
        return s

    @item("heimdall_eye")
    def _():
        s = Sprite("heimdall_eye")
        for a in range(8):
            ang = a * math.pi / 4
            s.stroke([(16 + 9 * math.cos(ang), 16 + 9 * math.sin(ang)), (16 + 14 * math.cos(ang), 16 + 14 * math.sin(ang))],
                     1.6, GOLD, bevel=0.6)
        s.poly([(3, 16), (9, 10), (16, 8), (23, 10), (29, 16), (23, 22), (16, 24), (9, 22)], mat(0xF6F0E2), bevel=2.5)
        s.ellipse((10.5, 10.5, 21.5, 21.5), AMBER)
        s.ellipse((14, 12, 18, 20), mat(0x1A0E06, glint=False), round_=False)
        s.pixel(13, 13, (255, 255, 255))
        return s

    @item("dead_water")
    def _():
        return bottle("dead_water", mat(0x3E2A6A, spread=0.45), glow=(150, 120, 220))

    @item("living_water")
    def _():
        return bottle("living_water", mat(0x3A8AE8, spread=0.45), glow=(220, 245, 255))

    @item("growth_potion")
    def _():
        return bottle("growth_potion", mat(0x4CC23A, spread=0.45), glow=(220, 255, 180))

    @item("mead")
    def _():
        s = Sprite("mead")
        s.poly([(8, 8), (24, 8), (25, 28), (7, 28)], WOOD, bevel=2, pattern=bands("x", 4, 0.12))
        for y in (10, 25):
            s.rect((7, y, 25, y + 2.2), DARK_STEEL, bevel=1)
        s.stroke([(24, 12), (29, 13), (29, 21), (24, 23)], 2, WOOD, bevel=1)
        s.ellipse((8, 5, 24, 11), mat(0xF7E6B0, spread=0.3), round_=False)
        s.ellipse((10, 6, 22, 10), mat(0xE2A43A, spread=0.3), round_=False)
        return s

    @item("family_whistle")
    def _():
        s = Sprite("family_whistle")
        s.stroke([(11, 8), (6, 4), (3, 9), (8, 13)], 1.0, mat(0xC0262E, glint=False), bevel=0.3)
        s.stroke([D(6, 0), D(24, 0)], 6.5, GOLD, bevel=2.5)
        s.ellipse((*[c - 3.4 for c in D(24.5)], *[c + 3.4 for c in D(24.5)]), DARK_GOLD)
        s.ellipse((*[c - 1.8 for c in D(24.5)], *[c + 1.8 for c in D(24.5)]), mat(0x2A1A10, glint=False),
                  round_=False)
        s.poly(D.pts([(12, 2.2), (17, 2.2), (16, 3.4), (13, 3.4)]), mat(0x2A1A10, glint=False), bevel=0.5)
        s.stroke([D(6, 0), D(9, 0)], 6.8, mat(0xC0262E), bevel=1.5)
        return s

    @item("firebird_feather")
    def _():
        return feather("firebird_feather", FIRE, mat(0xFFE07A), stripes=bands("y", 4, 0.12), seed=3)

    @item("harpy_feather")
    def _():
        return feather("harpy_feather", mat(0x9A7A5A, spread=0.42, glint=False), mat(0xE8DCC4),
                       stripes=bands("y", 5, 0.16), seed=4)

    @item("raven_feather")
    def _():
        return feather("raven_feather", mat(0x2A2A3A, spread=0.5), mat(0x5A5A7A), seed=5)

    @item("frost_heart")
    def _():
        s = Sprite("frost_heart")
        s.poly([(16, 29), (4, 16), (3, 10), (6, 5), (11, 4), (16, 8), (21, 4), (26, 5), (29, 10), (28, 16)], ICE,
               bevel=3.5)
        for a, b in (((16, 9), (16, 26)), ((8, 10), (16, 18)), ((24, 10), (16, 18))):
            s.stroke([a, b], 0.8, mat(0xF2FCFF), bevel=0.3, edge=False)
        return s

    @item("girdle_of_hippolyta")
    def _():
        s = Sprite("girdle")
        belt = s.ellipse((3, 8, 29, 26), GOLD, round_=False, bevel=2)
        belt.mask &= ~s._mask(lambda d, k: d.ellipse([7 * k, 12 * k, 25 * k - 1, 22 * k - 1], fill=255))
        s.rect((12, 5, 20, 12), GOLD, bevel=1.5)
        gem(s, 16, 8.5, 2.2, RUBY)
        for x in (6, 26):
            gem(s, x, 17, 1.4, mat(0x7A1E22))
        return s

    @item("gleipnir")
    def _():
        s = Sprite("gleipnir")
        pts = [(4 + i * 1.6, 16 + 9 * math.sin(i * 0.55)) for i in range(16)]
        s.stroke(pts, 3.0, mat(0xD8C8F0, spread=0.35), bevel=1.2)
        pts2 = [(6 + i * 1.5, 15 + 7 * math.cos(i * 0.5 + 1)) for i in range(15)]
        s.stroke(pts2, 1.6, mat(0xB0A0E0, spread=0.35), bevel=0.8)
        for x, y in ((8, 9), (20, 24), (26, 12)):
            s.pixel(x, y, (250, 245, 255))
        return s

    @item("harpe")
    def _():
        s = Sprite("harpe")
        s.poly(D.pts([(1.5, -1.5), (9, -1.5), (9, 1.5), (1.5, 1.5)]), mat(0x8A1E2A, glint=False), bevel=1,
               pattern=bands("x", 2, 0.12))
        gem(s, *D(1.2), 2, GOLD)
        s.poly(D.pts([(8.5, -3.8), (10.5, -3.8), (10.5, 3.8), (8.5, 3.8)]), GOLD, bevel=1.2)
        # A straight blade with a sickle hook bending back from its tip.
        s.poly(D.pts([(10.5, -2.4), (25, -2.6), (30, -3.4), (33.5, -1), (34, 3), (32, 7.5), (28.5, 10), (26, 10),
                      (28.5, 7), (29.5, 3.5), (28, 2.4), (10.5, 2.4)]), mat(0xC8CED6, spread=0.5), bevel=2)
        s.stroke([D(12, -0.2), D(27, -0.4)], 0.8, mat(0x8A929E), bevel=0.3, edge=False)
        return s

    @item("heimdall_helmet")
    def _():
        s = Sprite("heimdall_helmet")
        for side in (-1, 1):
            s.poly([(16 + side * 9, 12), (16 + side * 15, 3), (16 + side * 14, 10), (16 + side * 11, 15)],
                   mat(0xF2F0EA, spread=0.35), bevel=1.8, pattern=bands("y", 3, 0.08))
        s.poly([(6, 18), (6, 12), (9, 7), (16, 4.5), (23, 7), (26, 12), (26, 18)], GOLD, bevel=3)
        s.rect((5.5, 16, 26.5, 19.5), DARK_GOLD, bevel=1.4)
        s.poly([(14.5, 18), (17.5, 18), (17.5, 27), (14.5, 27)], GOLD, bevel=1)
        s.poly([(8, 19.5), (14, 19.5), (14, 25), (9, 24)], mat(0x8A6A20), bevel=1.2)
        s.poly([(18, 19.5), (24, 19.5), (23, 24), (18, 25)], mat(0x8A6A20), bevel=1.2)
        gem(s, 16, 10, 2, mat(0x56C8F2))
        return s

    @item("hephaestus_coal")
    def _():
        s = Sprite("hephaestus_coal")
        s.poly([(5, 15), (9, 7), (17, 4), (25, 8), (28, 16), (24, 25), (14, 28), (7, 23)], mat(0x2A2426, spread=0.35),
               bevel=4, pattern=noise(0.14, 8))
        for a, b in (((10, 12), (15, 16)), ((15, 16), (14, 22)), ((15, 16), (22, 14)), ((20, 20), (23, 23))):
            s.stroke([a, b], 1.0, mat(0xFF7A1E, spread=0.3), bevel=0.3, edge=False, base=0.8)
        s.pixel(15, 16, (255, 230, 120))
        return s

    @item("muspel_ember")
    def _():
        s = Sprite("muspel_ember")
        s.poly([(16, 2), (27, 14), (16, 30), (5, 14)], mat(0xB8260E, spread=0.4), bevel=4)
        s.poly([(16, 7), (22.5, 14.5), (16, 24), (9.5, 14.5)], mat(0xF27A1E, spread=0.4), bevel=3)
        s.poly([(16, 11), (19.5, 15), (16, 19.5), (12.5, 15)], mat(0xFFE07A, spread=0.3), bevel=2)
        return s

    @item("horn_of_themiscyra")
    def _():
        return horn("horn_of_themiscyra", IVORY, lambda t: (4 + 22 * t, 27 - 16 * t - 7 * math.sin(math.pi * t)),
                    rings=(7, 13, 19), ring_mat=GOLD, mouth=mat(0x3A2A1A, glint=False))

    @item("horn_of_vingolf")
    def _():
        s = horn("horn_of_vingolf", mat(0x6A5038, spread=0.45),
                 lambda t: (4 + 22 * t, 6 + 14 * t + 7 * math.sin(math.pi * t)), rings=(8, 15), ring_mat=SILVER,
                 mouth=mat(0x2A1E14, glint=False))
        s.stroke([(7, 9), (15, 6), (24, 13)], 0.8, LEATHER, bevel=0.3)
        return s

    @item("hydra_egg")
    def _():
        def marks(s):
            for x, y in ((12, 10), (19, 14), (13, 19), (20, 23), (16, 26)):
                gem(s, x, y, 1.6, mat(0x1E5A2A, glint=False))
        return egg("hydra_egg", mat(0x58B24A, spread=0.45), pattern=scales(3, 0.12), marks=marks)

    @item("koschei_egg")
    def _():
        def marks(s):
            s.stroke([(7.5, 18), (10, 15.5), (13, 18), (16, 15.5), (19, 18), (22, 15.5), (24.5, 18)], 1.0,
                     mat(0x3A1E5A), bevel=0.3, edge=False)
            for x in (10, 16, 22):
                s.pixel(x, 21, (120, 60, 160))
            s.stroke([(10, 9), (22, 9)], 0.8, mat(0x6A3A8A), bevel=0.3, edge=False)
        return egg("koschei_egg", mat(0xEDE8EE, spread=0.35), marks=marks)

    @item("hydra_scale")
    def _():
        s = Sprite("hydra_scale")
        s.poly([(16, 3), (27, 13), (24, 26), (16, 30), (8, 26), (5, 13)], mat(0x2E8A42, spread=0.45), bevel=4)
        s.stroke([(16, 6), (16, 27)], 1.0, mat(0x7ADA6A), bevel=0.4, edge=False)
        return s

    @item("zmey_scale")
    def _():
        s = Sprite("zmey_scale")
        s.poly([(16, 3), (28, 9), (27, 21), (16, 30), (5, 21), (4, 9)], mat(0xC0402A, spread=0.4), bevel=2)
        s.poly([(16, 5.5), (25.5, 10.5), (24.5, 20), (16, 27), (7.5, 20), (6.5, 10.5)], mat(0x3A7A3A, spread=0.45),
               bevel=3.5, pattern=scales(4, 0.14))
        return s

    @item("idunn_apple")
    def _():
        s = Sprite("idunn_apple")
        s.ellipse((5, 8, 27, 29), mat(0xF2C232))
        s.stroke([(16, 9), (17, 4)], 1.6, WOOD, bevel=1)
        s.poly([(17, 6), (22, 3), (26, 4), (22, 8)], LEAF, bevel=1.5)
        for x, y in ((11, 13), (21, 21)):
            s.pixel(x, y, (255, 250, 210))
        return s

    @item("pomegranate")
    def _():
        s = Sprite("pomegranate")
        s.ellipse((4, 8, 28, 30), mat(0xB0202A))
        s.poly([(12, 9), (13, 3), (15, 6), (16, 2), (17, 6), (19, 3), (20, 9)], mat(0x8A1820, glint=False), bevel=1)
        return s

    @item("olives")
    def _():
        s = Sprite("olives")
        s.stroke([(4, 6), (14, 12), (27, 14)], 1.4, WOOD, bevel=0.6)
        for pts in (((8, 8), (5, 2), (12, 5)), ((19, 13), (22, 6), (26, 9)), ((24, 14), (29, 20), (25, 19))):
            s.poly(pts, mat(0x6E8A3A, spread=0.4, glint=False), bevel=1.5)
        for x, y in ((10, 17), (15, 22), (20, 19), (14, 15)):
            s.ellipse((x - 3, y - 4, x + 3, y + 4), mat(0x3A2A4A, spread=0.5))
        return s

    @item("world_tree_acorn")
    def _():
        s = Sprite("world_tree_acorn")
        s.ellipse((8, 11, 24, 30), mat(0x9A6A30))
        s.poly([(6, 14), (8, 8), (16, 5.5), (24, 8), (26, 14)], mat(0x6A4A24, glint=False), bevel=2,
               pattern=scales(2, 0.2))
        s.stroke([(16, 6), (17, 2)], 1.4, WOOD, bevel=0.6)
        s.poly([(17, 3), (24, 1), (27, 4), (21, 6)], mat(0x5AB040, spread=0.45), bevel=1.5)
        for x, y in ((12, 18), (19, 22), (15, 25)):
            s.pixel(x, y, (150, 230, 255))
        return s

    @item("karavai")
    def _():
        s = Sprite("karavai")
        s.ellipse((3, 10, 29, 28), mat(0xC07A34, spread=0.42), dome=(16, 19, 13, 9))
        s.ellipse((7, 8, 25, 18), mat(0xDA9A48, spread=0.4))
        for x in (10, 16, 22):
            s.stroke([(x - 2, 13), (x + 2, 11)], 1.0, mat(0x8A4A1A), bevel=0.3, edge=False)
        s.ellipse((13, 5, 19, 10), mat(0xF2E6C8, spread=0.3))
        return s

    @item("karkinos_claw")
    def _():
        s = Sprite("karkinos_claw")
        s.poly([(4, 26), (8, 18), (14, 13), (20, 6), (27, 4), (24, 10), (19, 13), (25, 13), (28, 17), (22, 19),
                (16, 21), (10, 27)], mat(0xC8402A, spread=0.45), bevel=3)
        s.stroke([(9, 21), (13, 17)], 0.8, mat(0x7A1A10), bevel=0.3, edge=False)
        for x, y in ((14, 16), (20, 11)):
            s.pixel(x, y, (250, 200, 170))
        return s

    @item("nemean_claw")
    def _():
        s = fang("nemean_claw", mat(0x3A2E26, spread=0.5), curve=1.8, root=LION)
        return s

    @item("nemean_claw_dagger")
    def _():
        s = Sprite("nemean_claw_dagger")
        s.poly(D.pts([(1.5, -1.6), (10, -1.6), (10, 1.6), (1.5, 1.6)]), LEATHER, bevel=1, pattern=bands("x", 2, 0.12))
        gem(s, *D(1.2), 2, GOLD)
        s.poly(D.pts([(9.5, -4), (12, -4), (12, 4), (9.5, 4)]), LION, bevel=1.4, pattern=fur(0.12, 1))
        s.poly(D.pts([(12, -2.6), (22, -3.2), (30, -1.5), (34, 1.5), (28, 2.2), (20, 2.6), (12, 2.4)]),
               mat(0x4A3E36, spread=0.55), bevel=2)
        return s

    @item("nemean_pelt")
    def _():
        s = Sprite("nemean_pelt")
        s.poly([(4, 8), (9, 5), (13, 8), (19, 8), (23, 5), (28, 8), (27, 15), (29, 25), (24, 28), (20, 24), (12, 24),
                (8, 28), (3, 25), (5, 15)], LION, bevel=3, pattern=fur(0.14, 3))
        s.ellipse((10, 9, 22, 21), LION_MANE, pattern=fur(0.12, 4))
        return s

    @item("volkolak_pelt")
    def _():
        s = Sprite("volkolak_pelt")
        s.poly([(4, 8), (9, 5), (13, 8), (19, 8), (23, 5), (28, 8), (27, 15), (29, 25), (24, 28), (20, 24), (12, 24),
                (8, 28), (3, 25), (5, 15)], GREY_FUR, bevel=3, pattern=fur(0.16, 6))
        s.stroke([(16, 9), (16, 22)], 3, mat(0x5A5C62, glint=False), bevel=1, pattern=fur(0.1, 7))
        return s

    def nemean(piece):
        def draw():
            s = Sprite("nemean_" + piece)
            if piece == "helmet":  # the lion's head worn as a hood: muzzle, ears and a dark face opening
                s.ellipse((3, 4, 29, 30), LION_MANE, pattern=fur(0.16, 8), round_=False, bevel=4)
                s.ellipse((7, 6, 25, 24), LION, pattern=fur(0.1, 9))
                for x in (8, 24):
                    s.ellipse((x - 3, 3, x + 3, 9), LION)
                s.poly([(10, 15), (22, 15), (21, 24), (11, 24)], mat(0x22140C, glint=False), bevel=1, base=0.2,
                       edge=False)
                s.poly([(13, 9), (19, 9), (18, 14), (14, 14)], mat(0xA87430, glint=False), bevel=1.5)
                s.pixel(13, 11, (40, 24, 10))
                s.pixel(18, 11, (40, 24, 10))
                for x in (11, 20):
                    s.poly([(x, 15), (x + 1.6, 15), (x + 0.8, 18.5)], IVORY, bevel=0.6)
            elif piece == "chestplate":
                s.poly([(3, 7), (9, 4), (12, 6), (20, 6), (23, 4), (29, 7), (28.5, 14), (25, 14), (25, 28), (7, 28),
                        (7, 14), (3.5, 14)], LION, bevel=3, pattern=fur(0.12, 10))
                s.stroke([(8, 5), (16, 12), (24, 5)], 2.4, LION_MANE, bevel=1, pattern=fur(0.1, 11))
                for x in (10, 16, 22):
                    s.poly([(x - 1.5, 13), (x + 1.5, 13), (x, 17)], IVORY, bevel=0.6)
                s.rect((7, 23, 25, 25.5), LEATHER, bevel=1)
            elif piece == "leggings":
                s.poly([(7, 4), (25, 4), (26.5, 28), (19.5, 28), (16.5, 12), (15.5, 12), (12.5, 28), (5.5, 28)], LION,
                       bevel=2.6, pattern=fur(0.12, 12))
                s.rect((6.5, 4, 25.5, 7.5), LEATHER, bevel=1.2)
                s.rect((14.5, 4.5, 17.5, 7), GOLD, bevel=1)
            else:
                for x0 in (3, 17):
                    s.poly([(x0 + 1, 8), (x0 + 9, 8), (x0 + 9, 22), (x0 + 12, 24), (x0 + 12, 28), (x0, 28), (x0, 18)],
                           LION, bevel=2.4, pattern=fur(0.12, 13 + x0))
                    s.rect((x0 + 0.5, 8, x0 + 9.5, 11), LION_MANE, bevel=1, pattern=fur(0.1, 1))
                    s.rect((x0, 26.5, x0 + 12, 28.5), LEATHER, bevel=1)
            return s
        return draw

    for piece in ("helmet", "chestplate", "leggings", "boots"):
        items["nemean_" + piece] = nemean(piece)

    @item("kladenets")
    def _():
        s = Sprite("kladenets")
        s.poly(D.pts([(1.5, -1.5), (9, -1.5), (9, 1.5), (1.5, 1.5)]), mat(0x2E4C8E, glint=False), bevel=1,
               pattern=bands("x", 2, 0.14))
        gem(s, *D(1.2), 2.2, GOLD)
        s.poly(D.pts([(8.5, -6.5), (10, -7), (11.2, -5), (10.5, 5), (11.2, 7), (10, 7), (8.5, 6.5)]), GOLD, bevel=1.2)
        s.poly(D.pts([(11, -2.6), (31, -2.6), (35, 0), (31, 2.6), (11, 2.6)]), mat(0xDCE6F2, spread=0.45), bevel=2.4)
        s.stroke([D(12, 0), D(30, 0)], 0.9, mat(0x8ACBF2), bevel=0.3, edge=False, base=0.75)
        gem(s, *D(9.7), 1.4, RUBY)
        return s

    @item("surtr_sword")
    def _():
        s = Sprite("surtr_sword")
        s.poly(D.pts([(1.5, -1.5), (9, -1.5), (9, 1.5), (1.5, 1.5)]), mat(0x2A1E1A, glint=False), bevel=1,
               pattern=bands("x", 2, 0.14))
        gem(s, *D(1.2), 2, mat(0x8A2A14))
        s.poly(D.pts([(8.5, -5), (11, -4), (11, 4), (8.5, 5)]), mat(0x3A2A26), bevel=1.2)
        s.poly(D.pts([(11, -3.4), (18, -2.2), (24, -3.6), (31, -1.8), (35, 0), (31, 2.4), (24, 3.4), (18, 2.4),
                      (11, 3.2)]), FIRE, bevel=2.6, pattern=noise(0.12, 2))
        s.stroke([D(12, 0), D(31, 0)], 1.2, mat(0xFFE07A, spread=0.3), bevel=0.3, edge=False, base=0.8)
        return s

    @item("mjolnir")
    def _():
        s = Sprite("mjolnir")
        s.stroke([D(-1, 0), D(17, 0)], 2.6, LEATHER, bevel=1, pattern=bands("x", 2, 0.14))
        s.stroke([D(-2.5, 0), D(-0.5, 0)], 1.4, LEATHER, bevel=0.5)
        s.poly(D.pts([(15, -8.5), (29, -8.5), (30.5, -7), (30.5, 7), (29, 8.5), (15, 8.5), (13.5, 7), (13.5, -7)]),
               mat(0x8E96A4, spread=0.5), bevel=3.5, pattern=noise(0.06, 6))
        for t in (16.5, 27.5):
            s.stroke([D(t, -8), D(t, 8)], 1.1, mat(0x5A6070), bevel=0.4, edge=False)
        s.stroke([D(22, -4), D(22, 4)], 1.0, CYAN, bevel=0.3, edge=False, base=0.8)
        s.stroke([D(20, 0), D(24, 0)], 1.0, CYAN, bevel=0.3, edge=False, base=0.8)
        return s

    @item("koschei_needle")
    def _():
        s = Sprite("koschei_needle")
        s.stroke([D(1, 0), D(33, 0)], 1.8, mat(0xD8DCE4, spread=0.5), bevel=0.8)
        s.ellipse((*[c - 2.2 for c in D(4)], *[c + 2.2 for c in D(4)]), mat(0xD8DCE4), round_=False)
        s.ellipse((*[c - 0.9 for c in D(4)], *[c + 0.9 for c in D(4)]), mat(0x2A1E3A, glint=False), round_=False)
        s.stroke([D(6, 0), D(10, 1.5), D(14, -1), D(18, 1)], 0.8, mat(0x7A3AAA), bevel=0.3, edge=False)
        return s

    @item("medusa_head")
    def _():
        # A woman's face as the mod draws them: large eyes, long hair (here snakes), no mouth and no blush.
        s = Sprite("medusa_head")
        hair = mat(0x2E6A2E, spread=0.45, glint=False)
        s.poly([(7, 9), (10, 4), (16, 2.5), (22, 4), (25, 9), (26, 20), (27, 29), (21, 27), (11, 27), (5, 29), (6, 20)],
               hair, bevel=3, pattern=bands("x", 2, 0.12))
        snake = mat(0x5A9A44, spread=0.45)
        for pts in (((9, 5), (6, 2), (3, 3)), ((23, 5), (26, 2), (29, 3)), ((13, 3), (12, 0.5), (9.5, 0.5)),
                    ((19, 3), (20, 0.5), (22.5, 0.5))):
            s.stroke(list(pts), 1.8, snake, bevel=0.8)
            s.pixel(int(pts[-1][0]), int(pts[-1][1]), (200, 40, 40))
        s.ellipse((9.5, 7, 22.5, 27), mat(0xD2E0C2, spread=0.3, glint=False), dome=(16, 17, 6.5, 10))
        s.poly([(9.5, 8), (16, 5.5), (22.5, 8), (22, 12), (16, 9.5), (10, 12)], hair, bevel=1.5)
        for x in (10.5, 17.5):
            s.rect((x, 14, x + 4, 19), mat(0xF8F4E0, glint=False), bevel=0.5, edge=False)
            s.rect((x + 1, 14.5, x + 4, 19), mat(0xE0B82A, glint=False), bevel=0.5, edge=False)
            s.rect((x + 2, 15.5, x + 3, 18), mat(0x1A1208, glint=False), bevel=0.5, edge=False)
            s.pixel(int(x + 1), 15, (255, 255, 240))
            s.rect((x, 13, x + 4, 14), mat(0x1E3A1E, glint=False), bevel=0.5, edge=False)
        s.pixel(16, 21, (170, 190, 150))
        return s

    @item("minotaur_horn")
    def _():
        s = Sprite("minotaur_horn")
        pts = []
        for i in range(15):
            t = i / 14
            pts.append((5 + 20 * t + 3 * math.sin(t * math.pi), 27 - 12 * t - 10 * t * t, 4.5 * (1 - t) + 0.5))
        s.poly([(x - w, y - w * 0.3) for x, y, w in pts] + [(x + w * 0.6, y + w) for x, y, w in pts[::-1]],
               mat(0xE2D6B6, spread=0.45), bevel=3, pattern=bands("x", 4, 0.1))
        s.ellipse((1, 22, 10, 31), mat(0x5A3A24, glint=False), pattern=fur(0.12, 2))
        return s

    @item("necklace_of_harmonia")
    def _():
        s = Sprite("necklace_of_harmonia")
        pts = [(16 + 12 * math.cos(a), 6 + 12 * math.sin(a)) for a in [math.pi * i / 16 for i in range(17)]]
        s.stroke(pts, 1.6, GOLD, bevel=0.6)
        for i in (2, 5, 11, 14):
            gem(s, *pts[i], 1.4, mat(0x3A8AE0))
        s.poly([(10, 16), (16, 13), (22, 16), (20, 22), (16, 28), (12, 22)], GOLD, bevel=2.5)
        s.poly([(12.5, 17.5), (16, 15.5), (19.5, 17.5), (18.5, 21), (16, 25), (13.5, 21)], EMERALD, bevel=2)
        return s

    @item("promethean_torch")
    def _():
        s = Sprite("promethean_torch")
        s.stroke([D(1, 0), D(21, 0)], 2.4, WOOD, bevel=1, pattern=grain((1, -1), 2.5, 0.12, 4))
        s.poly(D.pts([(18, -2.8), (24, -3.2), (24, 3.2), (18, 2.8)]), GOLD, bevel=1.5)
        s.poly(D.pts([(23.5, -4.4), (28, -5.5), (33, -3), (36, 0), (32, 1), (34, 4), (28, 5), (23.5, 4.4)]), FIRE,
               bevel=2.5, pattern=noise(0.1, 3))
        s.poly(D.pts([(24.5, -2.2), (29, -2.5), (31.5, 0), (29, 2.5), (24.5, 2.2)]), mat(0xFFE07A, spread=0.3),
               bevel=1.5, base=0.75)
        return s

    @item("rune_igniter")
    def _():
        s = Sprite("rune_igniter")
        s.poly([(9, 3), (23, 3), (25, 8), (25, 25), (22, 29), (10, 29), (7, 25), (7, 8)], mat(0x5A5E6A, spread=0.45),
               bevel=3.5, pattern=noise(0.08, 3))
        colours = [0xE84A4A, 0xF2A23A, 0xF2E24A, 0x5AD25A, 0x4AA8F2, 0x8A5AE8]
        pts = [(16, 7), (16, 25), (16, 13), (21, 9), (16, 17), (21, 21)]
        for i in range(len(pts) - 1):
            s.stroke([pts[i], pts[i + 1]] if i % 2 == 0 else [pts[i], pts[i + 1]], 1.4, mat(colours[i]), bevel=0.4,
                     edge=False, base=0.75)
        return s

    @item("shapka_nevidimka")
    def _():
        s = Sprite("shapka_nevidimka")
        s.poly([(6, 22), (7, 13), (11, 7), (16, 5), (21, 7), (25, 13), (26, 22)], mat(0xA8202A, spread=0.42), bevel=4,
               pattern=bands("x", 4, 0.08))
        s.ellipse((3, 18, 29, 29), mat(0x6A4A2E, spread=0.42, glint=False), round_=False, bevel=3, pattern=fur(0.16, 3))
        s.stroke([(16, 6), (16, 18)], 1.2, GOLD, bevel=0.5)
        gem(s, 16, 12, 2.2, mat(0x7AE0F2))
        for x in (10, 22):
            gem(s, x, 14, 1.2, GOLD)
        return s

    @item("skorokhody")
    def _():
        s = Sprite("skorokhody")
        red = mat(0xA8202A, spread=0.42)
        for x0 in (3, 17):
            s.poly([(x0 + 1, 6), (x0 + 9, 6), (x0 + 9, 21), (x0 + 12, 23), (x0 + 12, 28), (x0, 28), (x0, 16)], red,
                   bevel=2.5)
            s.rect((x0 + 0.5, 6, x0 + 9.5, 9), GOLD, bevel=1)
            for y in (13, 18):
                s.stroke([(x0 + 2, y), (x0 + 5, y + 2), (x0 + 8, y)], 0.9, GOLD, bevel=0.3, edge=False)
            s.rect((x0, 26.5, x0 + 12, 28.5), DARK_WOOD, bevel=1)
        return s

    @item("talaria")
    def _():
        s = Sprite("talaria")
        wing = mat(0xF4F2EC, spread=0.35)
        for x0 in (2, 16):
            s.poly([(x0 + 2, 18), (x0 + 1, 10), (x0 - 1, 4), (x0 + 3, 7), (x0 + 6, 13)], wing, bevel=1.5,
                   pattern=bands("y", 3, 0.1))
            s.poly([(x0 + 4, 12), (x0 + 11, 12), (x0 + 11, 22), (x0 + 14, 24), (x0 + 14, 28), (x0 + 3, 28)], LEATHER,
                   bevel=2)
            for y in (15, 19, 23):
                s.stroke([(x0 + 4, y), (x0 + 11, y)], 1.0, GOLD, bevel=0.4)
            s.rect((x0 + 3, 26.5, x0 + 14, 28.5), DARK_WOOD, bevel=1)
        return s

    @item("titan_breastplate")
    def _():
        s = Sprite("titan_breastplate")
        s.poly([(3, 7), (9, 4), (12, 6), (20, 6), (23, 4), (29, 7), (28.5, 14), (25, 14), (25, 28), (7, 28), (7, 14),
                (3.5, 14)], mat(0xC07A3A), bevel=3.5)
        s.poly([(10, 10), (22, 10), (22, 22), (16, 25), (10, 22)], mat(0x1E2A5A, spread=0.4), bevel=2)
        for x, y in ((13, 13), (19, 12), (16, 17), (12, 20), (20, 19), (17, 22)):
            s.pixel(x, y, (255, 240, 180))
        s.stroke([(12, 6.5), (16, 9), (20, 6.5)], 1.0, GOLD, bevel=0.5)
        s.stroke([(7, 26), (25, 26)], 1.2, GOLD, bevel=0.5)
        return s

    @item("wedding_ring")
    def _():
        s = Sprite("wedding_ring")
        ring = s.ellipse((5, 9, 27, 30), GOLD, round_=False, bevel=2.5)
        ring.mask &= ~s._mask(lambda d, k: d.ellipse([10 * k, 14 * k, 22 * k - 1, 25 * k - 1], fill=255))
        s.poly([(12, 9), (16, 2), (20, 9), (16, 12)], mat(0xD8F4FF, spread=0.3), bevel=2)
        return s

    @item("wings_of_daedalus")
    def _():
        s = Sprite("wings_of_daedalus")
        wing = mat(0xF2EEE4, spread=0.35)
        for side in (-1, 1):
            pts = [(16 + side * 2, 8), (16 + side * 14, 4), (16 + side * 15, 10), (16 + side * 13, 20),
                   (16 + side * 9, 27), (16 + side * 3, 22)]
            s.poly(pts, wing, bevel=2.5, pattern=bands("y" if side < 0 else "y", 4, 0.12, offset=side))
            for k in range(3):
                y = 12 + k * 5
                s.stroke([(16 + side * 3, y), (16 + side * (12 - k * 1.5), y + 3)], 0.8, mat(0xB8A88A), bevel=0.3,
                         edge=False)
        s.rect((14, 6, 18, 24), WOOD, bevel=1.2)
        s.stroke([(14, 10), (18, 10)], 1.0, mat(0xE8C878), bevel=0.3)
        return s

