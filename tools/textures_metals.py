"""Textures of the metals and fuels (see gen_metals.py): ores, metal blocks, items, tools and armour layers."""
from PIL import Image, ImageDraw

from textures import box_faces, fill_rect, item, jitter, mix, rgb, save, scale  # noqa: F401

STONE = 0x7E7E7E


def scale_hex(colour, factor):
    r, g, b, _ = scale(rgb(colour), factor)
    return (r << 16) | (g << 8) | b


def stone(rng):
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(STONE), rng, 10)
    for _ in range(14):
        x, y = rng.randrange(16), rng.randrange(16)
        img.putpixel((x, y), jitter(rgb(0x686868), rng, 6))
    for _ in range(10):
        x, y = rng.randrange(16), rng.randrange(16)
        img.putpixel((x, y), jitter(rgb(0x969696), rng, 6))
    return img


def ore(rng, colours, glow=False, lumps=False):
    """Stone with five or six clusters of the mineral, each a light, a mid and a dark pixel or two."""
    light, mid, dark = (rgb(c) for c in colours)
    img = stone(rng)
    spots = [(2, 2), (9, 1), (12, 6), (4, 8), (10, 11), (2, 13), (7, 5)]
    for x, y in spots[:6 if lumps else 5]:
        x = min(13, max(0, x + rng.randint(-1, 1)))
        y = min(13, max(0, y + rng.randint(-1, 1)))
        cells = [(0, 0), (1, 0), (0, 1), (1, 1)] + ([(2, 1), (1, 2)] if lumps else [(2, 0)])
        for i, (dx, dy) in enumerate(cells):
            c = light if i == 0 else mid if i < 3 else dark
            if glow and i == 0:
                c = rgb(0xFFE08A)
            img.putpixel((x + dx, y + dy), jitter(c, rng, 8))
        img.putpixel((x + 1, y + 2 if lumps else y + 1), jitter(rgb(0x4A4A4A), rng, 6))
    return img


def metal_block(rng, colours, style):
    light, mid, dark = (rgb(c) for c in colours)
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, mid, rng, 6)
    fill_rect(img, 0, 0, 16, 1, light, rng, 4)
    fill_rect(img, 0, 0, 1, 16, light, rng, 4)
    fill_rect(img, 0, 15, 16, 1, dark, rng, 4)
    fill_rect(img, 15, 0, 1, 16, dark, rng, 4)
    if style == "greek":   # a key pattern band across the middle
        for x in range(1, 15):
            img.putpixel((x, 6), dark)
            img.putpixel((x, 9), dark)
        for x in range(1, 15, 4):
            for y in (7, 8):
                img.putpixel((x, y), dark)
                img.putpixel((x + 2, y - 1 if y == 7 else y), light)
    else:                  # riveted plates
        for y in (7, 8):
            fill_rect(img, 1, y, 14, 1, dark if y == 8 else light, rng, 4)
        for x, y in ((3, 3), (12, 3), (3, 12), (12, 12)):
            img.putpixel((x, y), light)
            img.putpixel((x + 1, y + 1), dark)
    return img


def icon(draw, rng):
    return item(draw, rng)


GOLD, GOLD_DARK, RED = 0xE2B33C, 0x9A6E1E, 0xC0262E
OLIVE_WOOD, OLIVE_DARK = 0x8A6440, 0x5A3E26
LEATHER, LEATHER_LIGHT = 0x4A2E1A, 0x7A5432
RUNE = 0x7AD8FF


def _blade(img, start, length, light, mid, dark, widen=()):
    """A blade along the diagonal from start (bottom left) up to the top right; widen: steps where it is broader."""
    x, y = start
    for i in range(length):
        cx, cy = x + i, y - i
        img.putpixel((cx, cy), mid)
        if i < length - 1:
            img.putpixel((cx + 1, cy), light)
            img.putpixel((cx, cy + 1), dark)
        if i in widen:
            img.putpixel((cx + 1, cy + 1), mid)
            if cx + 2 < 16:
                img.putpixel((cx + 2, cy + 1), light)
            img.putpixel((cx + 1, cy + 2), dark)


def _grip(img, base, length, colours):
    """A grip down and left from base, its colours repeating (wood grain or a leather wrap)."""
    x, y = base
    for i in range(length):
        img.putpixel((x - i, y + i), rgb(colours[i % len(colours)]))


def _haft(img, top, length, style):
    """A tool's haft running down and left from top: olive wood with gold rings, or ash wrapped in leather."""
    x, y = top
    for i in range(length):
        px, py = x - i, y + i
        if style == "greek":
            c = GOLD if i in (2, length - 2) else (OLIVE_WOOD if i % 3 else OLIVE_DARK)
        else:
            c = LEATHER_LIGHT if i >= length - 4 and i % 2 else LEATHER if i >= length - 4 else 0x8A6A4A
        img.putpixel((px, py), rgb(c))
        if py + 1 < 16:
            img.putpixel((px, py + 1), scale(rgb(c), 0.7))


def metal_items(colours, style):
    """Item icons. Greek: a leaf-bladed xiphos, a double labrys, olive wood with gold rings, a crested helmet, a muscle
    cuirass with leather strips, greaves and sandals. Norse: a broad sword with a lobed pommel, a bearded axe, ash
    wrapped in leather with glowing runes, a spectacled helmet, a mail shirt, fur-topped boots."""
    light, mid, dark = (rgb(c) for c in colours)
    greek = style == "greek"
    accent = rgb(GOLD if greek else RUNE)

    def raw(img, d, rng):
        d.polygon([(4, 5), (8, 3), (12, 5), (13, 9), (10, 13), (5, 12), (3, 9)], fill=mid)
        d.polygon([(5, 6), (8, 4), (10, 6), (7, 8)], fill=light)
        for x, y in ((9, 10), (6, 10), (11, 8)):
            img.putpixel((x, y), dark)

    def ingot(img, d, rng):
        d.polygon([(2, 10), (6, 6), (14, 6), (10, 10)], fill=light)
        d.polygon([(2, 10), (10, 10), (10, 12), (2, 12)], fill=mid)
        d.polygon([(10, 10), (14, 6), (14, 8), (10, 12)], fill=dark)
        if greek:
            for x in (4, 6, 8):
                img.putpixel((x, 11), dark)
        else:
            img.putpixel((5, 11), accent)
            img.putpixel((6, 11), accent)

    def sword(img, d, rng):
        if greek:   # xiphos: a short leaf-shaped blade, a gold crossbar, a wooden grip, a round pommel
            _blade(img, (5, 10), 9, light, mid, dark, widen=(4, 5, 6))
            for dx, dy in ((-2, -2), (-1, -1), (1, 1), (2, 2)):
                img.putpixel((4 + dx + 1, 11 + dy - 1), rgb(GOLD))
            img.putpixel((4, 11), rgb(GOLD_DARK))
            _grip(img, (3, 12), 2, (OLIVE_WOOD, OLIVE_DARK))
            img.putpixel((1, 14), rgb(GOLD))
            img.putpixel((0, 15), rgb(GOLD_DARK))
            img.putpixel((1, 15), rgb(GOLD_DARK))
        else:       # broad Viking sword: a long blade with a fuller, a straight guard, a leather grip, a lobed pommel
            _blade(img, (5, 10), 10, light, mid, dark)
            for i in range(1, 8):
                img.putpixel((5 + i, 10 - i), scale(mid, 0.75))
            for dx, dy in ((-2, -2), (-1, -1), (0, 0), (1, 1), (2, 2)):
                img.putpixel((4 + dx + 1, 11 + dy - 1), dark if dx else mid)
            _grip(img, (3, 12), 2, (LEATHER_LIGHT, LEATHER))
            for x, y in ((1, 13), (2, 14), (0, 14), (1, 15)):
                img.putpixel((x, y), mid)
            img.putpixel((1, 14), light)

    def pickaxe(img, d, rng):
        _haft(img, (10, 5), 9, style)
        if greek:   # a bronze pick with gold-capped points
            d.line([(5, 2), (8, 1), (11, 1), (14, 4), (14, 9)], fill=mid)
            d.line([(5, 1), (8, 0), (11, 0), (15, 4)], fill=light)
            img.putpixel((4, 2), rgb(GOLD))
            img.putpixel((14, 10), rgb(GOLD))
        else:       # a heavy iron pick with a rune on the head
            d.line([(3, 4), (6, 1), (11, 1), (14, 4), (14, 10)], fill=mid, width=2)
            d.line([(4, 2), (7, 0), (11, 0), (15, 4)], fill=light)
            img.putpixel((10, 3), accent)
            img.putpixel((11, 2), accent)

    def axe(img, d, rng):
        _haft(img, (10, 5), 9, style)
        if greek:   # labrys: the double axe of Crete, two crescent blades
            d.polygon([(10, 4), (9, 0), (7, 0), (6, 2), (6, 4)], fill=mid)       # upper-left wing
            d.polygon([(11, 5), (15, 6), (15, 8), (13, 9), (11, 9)], fill=mid)  # lower-right wing
            d.line([(7, 0), (6, 2), (6, 4)], fill=light)
            d.line([(15, 6), (15, 8), (13, 9)], fill=dark)
            img.putpixel((10, 5), rgb(GOLD))
            img.putpixel((11, 4), rgb(GOLD))
        else:       # bearded axe: a long blade hanging below the head
            d.polygon([(10, 2), (12, 1), (15, 1), (15, 6), (13, 9), (12, 6), (10, 5)], fill=mid)
            d.line([(15, 1), (15, 6), (13, 9)], fill=light)
            d.line([(10, 2), (12, 1)], fill=dark)
            img.putpixel((12, 3), accent)

    def shovel(img, d, rng):
        _haft(img, (10, 5), 9, style)
        if greek:
            d.polygon([(10, 3), (12, 1), (15, 1), (15, 4), (13, 6)], fill=mid)
            d.line([(12, 1), (15, 1)], fill=light)
            img.putpixel((10, 4), rgb(GOLD))
        else:
            d.polygon([(9, 4), (12, 0), (15, 1), (15, 4), (11, 7)], fill=mid)
            d.line([(12, 0), (15, 1)], fill=light)
            img.putpixel((13, 3), accent)

    def hoe(img, d, rng):
        _haft(img, (11, 4), 10, style)
        if greek:   # a sickle-shaped blade
            d.line([(8, 1), (11, 0), (13, 1), (14, 3)], fill=mid)
            d.line([(8, 2), (11, 1)], fill=light)
            img.putpixel((11, 3), rgb(GOLD))
        else:
            d.polygon([(8, 2), (13, 2), (15, 4), (12, 4)], fill=mid)
            d.line([(8, 2), (13, 2)], fill=light)
            img.putpixel((12, 3), accent)

    def helmet(img, d, rng):
        if greek:   # Corinthian helmet with a tall red horsehair crest
            d.rectangle([3, 4, 12, 12], fill=mid)
            d.rectangle([3, 4, 12, 5], fill=light)
            d.rectangle([4, 0, 11, 3], fill=rgb(RED))
            d.line([(4, 0), (11, 0)], fill=rgb(0xE85A5A))
            d.rectangle([5, 7, 10, 8], fill=(0, 0, 0, 0))
            d.rectangle([7, 9, 8, 12], fill=(0, 0, 0, 0))
            d.line([(3, 12), (12, 12)], fill=dark)
        else:       # spectacled helmet: a round cap, eye rings and a mail curtain
            d.ellipse([3, 1, 12, 10], fill=mid)
            d.line([(5, 2), (10, 2)], fill=light)
            d.line([(7, 1), (7, 7)], fill=light)
            d.rectangle([3, 7, 12, 8], fill=dark)
            d.rectangle([4, 8, 6, 9], fill=(0, 0, 0, 0))
            d.rectangle([9, 8, 11, 9], fill=(0, 0, 0, 0))
            for x in range(3, 13):
                for y in range(10, 13):
                    if (x + y) % 2 == 0:
                        img.putpixel((x, y), scale(mid, 0.8))

    def chestplate(img, d, rng):
        if greek:   # muscle cuirass with leather strips (pteruges) below
            d.polygon([(2, 2), (6, 2), (7, 4), (8, 4), (9, 2), (13, 2), (13, 6), (11, 6), (11, 11), (4, 11), (4, 6), (2, 6)], fill=mid)
            for px, py in ((5, 5), (6, 6), (9, 5), (10, 6), (7, 8), (8, 8), (7, 10), (8, 10)):
                img.putpixel((px, py), light)
            for x in range(4, 12):
                c = rgb(0x8A5A30) if x % 2 else rgb(0x6A4024)
                for y in range(12, 15):
                    img.putpixel((x, y), c)
                img.putpixel((x, 11), rgb(GOLD))
        else:       # mail shirt with a leather belt
            d.polygon([(2, 3), (6, 2), (9, 2), (13, 3), (13, 8), (11, 8), (11, 14), (4, 14), (4, 8), (2, 8)], fill=mid)
            for y in range(4, 14, 2):
                for x in range(3, 13):
                    if img.getpixel((x, y))[3] and (x + y // 2) % 2:
                        img.putpixel((x, y), dark)
            d.line([(4, 10), (11, 10)], fill=rgb(LEATHER))
            img.putpixel((7, 10), rgb(0xC0C0C8))
            d.line([(6, 2), (9, 2)], fill=rgb(0x9A8070))

    def leggings(img, d, rng):
        if greek:   # bronze greaves with a knee boss
            for x0 in (3, 9):
                d.rectangle([x0, 2, x0 + 3, 14], fill=mid)
                d.line([(x0, 2), (x0, 14)], fill=light)
                img.putpixel((x0 + 1, 6), light)
                img.putpixel((x0 + 2, 6), light)
                d.line([(x0, 14), (x0 + 3, 14)], fill=dark)
        else:       # padded trousers with iron bands
            d.polygon([(4, 2), (11, 2), (12, 14), (9, 14), (8, 6), (7, 6), (6, 14), (3, 14)], fill=mid)
            d.line([(4, 2), (11, 2)], fill=rgb(LEATHER))
            for y in (6, 9, 12):
                d.line([(3, y), (6, y)], fill=dark)
                d.line([(9, y), (12, y)], fill=dark)

    def boots(img, d, rng):
        if greek:   # sandals laced up the shin
            for x0 in (2, 9):
                d.rectangle([x0 + 1, 4, x0 + 3, 11], fill=mid)
                for y in range(5, 11, 2):
                    d.line([(x0 + 1, y), (x0 + 3, y)], fill=rgb(0x8A5A30))
                d.line([(x0, 12), (x0 + 4, 12)], fill=dark)
                img.putpixel((x0 + 2, 4), light)
        else:       # boots with a fur top
            d.polygon([(3, 5), (6, 5), (6, 12), (2, 12), (2, 10), (3, 10)], fill=mid)
            d.polygon([(9, 5), (12, 5), (12, 10), (13, 10), (13, 12), (9, 12)], fill=mid)
            d.rectangle([2, 3, 6, 5], fill=rgb(0xD8C8B0))
            d.rectangle([9, 3, 13, 5], fill=rgb(0xD8C8B0))
            d.line([(2, 12), (6, 12)], fill=dark)
            d.line([(9, 12), (13, 12)], fill=dark)

    return {"raw": raw, "ingot": ingot, "sword": sword, "pickaxe": pickaxe, "axe": axe, "shovel": shovel, "hoe": hoe,
            "helmet": helmet, "chestplate": chestplate, "leggings": leggings, "boots": boots}


def draw_coal(colour):
    def draw(img, d, rng):
        d.polygon([(4, 4), (9, 3), (13, 6), (12, 11), (7, 13), (3, 10)], fill=rgb(0x2A2224))
        d.polygon([(5, 5), (9, 4), (10, 6), (6, 7)], fill=rgb(0x4A4044))
        for x, y in ((8, 9), (10, 8), (6, 10), (11, 10)):
            img.putpixel((x, y), rgb(colour))
        img.putpixel((9, 9), rgb(0xFFE08A))
    return draw


# ---------------------------------------------------------------- armour on the body (64x32 layers)

def _plate(img, rect, light, mid, dark, rng):
    x, y, w, h = rect
    fill_rect(img, x, y, w, h, mid, rng, 6)
    fill_rect(img, x, y, w, 1, light, rng, 4)
    fill_rect(img, x, y + h - 1, w, 1, dark, rng, 4)


def armour_layers(rng, colours, style):
    """layer_1: helmet (head), chestplate (body and arms) and boots (feet); layer_2: leggings (waist and legs)."""
    light, mid, dark = (rgb(c) for c in colours)
    one = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    head = box_faces(0, 0, 8, 8, 8)
    for name, rect in head.items():
        if name == "bottom":
            continue
        _plate(one, rect, light, mid, dark, rng)
    fx, fy, fw, fh = head["front"]
    if style == "greek":   # Corinthian helmet: a T-shaped opening and a red crest over the top
        for x in range(fx + 1, fx + 7):
            for y in range(fy + 3, fy + 5):
                one.putpixel((x, y), (0, 0, 0, 0))
        for x in range(fx + 3, fx + 5):
            for y in range(fy + 5, fy + 8):
                one.putpixel((x, y), (0, 0, 0, 0))
        tx, ty, tw, th = head["top"]
        fill_rect(one, tx + 3, ty, 2, th, rgb(0xC0262E), rng, 10)
        for name in ("front", "back"):
            x, y, w, h = head[name]
            fill_rect(one, x + 3, y, 2, 1, rgb(0xC0262E), rng, 10)
    else:                  # Viking helmet: an open face, brow and a nose guard, a ridge over the top
        for x in range(fx + 1, fx + 7):
            for y in range(fy + 3, fy + 8):
                one.putpixel((x, y), (0, 0, 0, 0))
        fill_rect(one, fx, fy + 2, fw, 1, dark, rng, 4)
        fill_rect(one, fx + 3, fy + 3, 2, 3, mid, rng, 4)
        tx, ty, tw, th = head["top"]
        fill_rect(one, tx + 3, ty, 2, th, light, rng, 4)
    body = box_faces(16, 16, 8, 12, 4)
    for name, rect in body.items():
        if name in ("top", "bottom"):
            continue
        x, y, w, h = rect
        if style == "greek":   # a muscled cuirass over a skirt of leather strips (pteruges) with gold tips
            _plate(one, (x, y, w, 9), light, mid, dark, rng)
            if name == "front":
                for px, py in ((2, 3), (5, 3), (3, 6), (4, 6)):
                    one.putpixel((x + px, y + py), light)
            for i in range(w):
                c = rgb(0x8A5A30) if i % 2 == 0 else rgb(0x6A4024)
                fill_rect(one, x + i, y + 9, 1, 2, c, rng, 4)
                one.putpixel((x + i, y + 11), rgb(GOLD) if i % 2 == 0 else (0, 0, 0, 0))
        else:                  # a long mail shirt with a leather belt
            _plate(one, (x, y, w, 12), light, mid, dark, rng)
            for j in range(1, 12, 2):
                for i in range(j % 4 // 2, w, 2):
                    one.putpixel((x + i, y + j), dark)
            fill_rect(one, x, y + 7, w, 1, rgb(LEATHER), rng, 4)
    arm = box_faces(40, 16, 4, 12, 4)
    for name, rect in arm.items():
        if name == "bottom":
            continue
        x, y, w, h = rect
        _plate(one, (x, y, w, min(h, 5)), light, mid, dark, rng)
        if style == "norse" and name != "top":       # a fur collar over the shoulders
            fill_rect(one, x, y, w, 1, rgb(0xD8C8B0), rng, 8)
        elif style == "norse":
            fill_rect(one, x, y, w, h, rgb(0xD8C8B0), rng, 8)
    leg = box_faces(0, 16, 4, 12, 4)
    for name, rect in leg.items():
        x, y, w, h = rect
        if name == "top":
            continue
        if name == "bottom":
            fill_rect(one, x, y, w, h, dark, rng, 4)
            continue
        if style == "greek":   # sandals: straps laced up the shin
            for j in range(4):
                if j % 2 == 0:
                    fill_rect(one, x, y + h - 4 + j, w, 1, rgb(0x8A5A30), rng, 4)
            fill_rect(one, x, y + h - 1, w, 1, mid, rng, 4)
        else:                  # boots with a fur top
            _plate(one, (x, y + h - 4, w, 4), light, mid, dark, rng)
            fill_rect(one, x, y + h - 4, w, 1, rgb(0xD8C8B0), rng, 8)
    two = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    for name, rect in body.items():
        if name in ("top", "bottom"):
            continue
        x, y, w, h = rect
        _plate(two, (x, y + 8, w, 4), light, mid, dark, rng)
    for name, rect in leg.items():
        if name in ("top", "bottom"):
            continue
        x, y, w, h = rect
        _plate(two, (x, y, w, 9), light, mid, dark, rng)
        if style == "greek":   # greaves with a knee boss
            two.putpixel((x + 1, y + 4), light)
        else:
            for j in range(2, 9, 3):
                fill_rect(two, x, y + j, w, 1, dark, rng, 4)
    return one, two


def girdle_layer(rng):
    """The girdle of Hippolyta on the leggings layer: a golden belt with a red jewel, leather strips below."""
    img = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    gold, deep, leather = rgb(0xFFD34E), rgb(0xC9963E), rgb(0x8A1E2A)
    body = box_faces(16, 16, 8, 12, 4)
    for name, (x, y, w, h) in body.items():
        if name in ("top", "bottom"):
            continue
        fill_rect(img, x, y + 9, w, 2, gold, rng, 6)
        fill_rect(img, x, y + 11, w, 1, deep, rng, 4)
    x, y, w, h = body["front"]
    img.putpixel((x + 3, y + 9), rgb(0xC0262E))
    img.putpixel((x + 4, y + 9), rgb(0xE85A5A))
    img.putpixel((x + 3, y + 10), rgb(0x8A1018))
    img.putpixel((x + 4, y + 10), rgb(0xC0262E))
    leg = box_faces(0, 16, 4, 12, 4)
    for name, (x, y, w, h) in leg.items():
        if name in ("top", "bottom"):
            continue
        for i in range(w):
            fill_rect(img, x + i, y, 1, 3 + (i % 2), leather if i % 2 == 0 else scale(leather, 0.75), rng, 6)
            img.putpixel((x + i, y + 3 + (i % 2)), gold)
    return img
