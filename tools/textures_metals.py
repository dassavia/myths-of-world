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


def _handle(d, top, wood=0x7A5230, dark=0x4A3220):
    """A wooden haft from the bottom left up to the head at top (x, y)."""
    x1, y1 = top
    d.line([(2, 13), (x1, y1)], fill=rgb(wood))
    d.line([(3, 13), (x1 + 1, y1)], fill=rgb(dark))


def metal_items(colours, style):
    light, mid, dark = (rgb(c) for c in colours)

    def raw(img, d, rng):
        d.polygon([(4, 5), (8, 3), (12, 5), (13, 9), (10, 13), (5, 12), (3, 9)], fill=mid)
        d.polygon([(5, 6), (8, 4), (10, 6), (7, 8)], fill=light)
        for x, y in ((9, 10), (6, 10), (11, 8)):
            img.putpixel((x, y), dark)

    def ingot(img, d, rng):
        d.polygon([(2, 10), (6, 6), (14, 6), (10, 10)], fill=light)
        d.polygon([(2, 10), (10, 10), (10, 12), (2, 12)], fill=mid)
        d.polygon([(10, 10), (14, 6), (14, 8), (10, 12)], fill=dark)

    def sword(img, d, rng):
        d.polygon([(6, 9), (13, 2), (14, 2), (14, 3), (7, 10)], fill=mid)
        d.line([(6, 9), (13, 2)], fill=light)
        d.line([(3, 8), (7, 12)], fill=dark if style == "norse" else light)
        d.line([(2, 13), (5, 10)], fill=rgb(0x5A3A20))
        img.putpixel((1, 14), dark)

    def pickaxe(img, d, rng):
        _handle(d, (10, 5))
        d.line([(4, 3), (7, 1), (11, 1), (14, 4), (14, 8)], fill=mid, width=1)
        d.line([(4, 2), (7, 0), (11, 0), (15, 4)], fill=light)
        d.line([(9, 2), (12, 5)], fill=dark)

    def axe(img, d, rng):
        _handle(d, (11, 4))
        d.polygon([(8, 3), (11, 0), (14, 2), (15, 6), (12, 7)], fill=mid)
        d.line([(11, 0), (15, 4)], fill=light)
        d.line([(9, 4), (11, 6)], fill=dark)

    def shovel(img, d, rng):
        _handle(d, (10, 5))
        d.polygon([(9, 4), (12, 1), (15, 2), (14, 6), (11, 7)], fill=mid)
        d.line([(12, 1), (15, 2)], fill=light)
        d.line([(11, 6), (14, 5)], fill=dark)

    def hoe(img, d, rng):
        _handle(d, (11, 4))
        d.polygon([(8, 2), (12, 2), (14, 4), (12, 4)], fill=mid)
        d.line([(8, 2), (12, 2)], fill=light)
        img.putpixel((13, 4), dark)

    def helmet(img, d, rng):
        d.rectangle([3, 3, 12, 9], fill=mid)
        d.rectangle([3, 3, 12, 4], fill=light)
        if style == "greek":   # a crest and a T-shaped opening
            d.rectangle([5, 0, 10, 2], fill=rgb(0xC0262E))
            d.rectangle([5, 6, 6, 11], fill=(0, 0, 0, 0))
            d.rectangle([9, 6, 10, 11], fill=(0, 0, 0, 0))
            d.rectangle([3, 10, 4, 12], fill=mid)
            d.rectangle([11, 10, 12, 12], fill=mid)
        else:                  # a rounded cap with a nose guard
            d.rectangle([4, 2, 11, 2], fill=light)
            d.rectangle([3, 8, 12, 10], fill=mid)
            d.rectangle([5, 7, 6, 8], fill=(0, 0, 0, 0))
            d.rectangle([9, 7, 10, 8], fill=(0, 0, 0, 0))
            d.rectangle([7, 7, 8, 11], fill=dark)

    def chestplate(img, d, rng):
        d.polygon([(2, 3), (6, 2), (9, 2), (13, 3), (13, 7), (11, 7), (11, 14), (4, 14), (4, 7), (2, 7)], fill=mid)
        d.line([(6, 2), (7, 4), (8, 4), (9, 2)], fill=dark)
        d.line([(5, 5), (5, 12)], fill=light)
        if style == "greek":
            d.line([(6, 8), (9, 8)], fill=dark)
            d.line([(6, 11), (9, 11)], fill=dark)
        else:
            for y in range(6, 14, 2):
                d.line([(5, y), (10, y)], fill=dark)

    def leggings(img, d, rng):
        d.polygon([(4, 2), (11, 2), (12, 14), (9, 14), (8, 6), (7, 6), (6, 14), (3, 14)], fill=mid)
        d.line([(4, 2), (11, 2)], fill=light)
        d.line([(4, 3), (11, 3)], fill=dark)
        d.line([(4, 5), (3, 13)], fill=light)

    def boots(img, d, rng):
        d.polygon([(3, 5), (6, 5), (6, 12), (2, 12), (2, 10), (3, 10)], fill=mid)
        d.polygon([(9, 5), (12, 5), (12, 10), (13, 10), (13, 12), (9, 12)], fill=mid)
        d.line([(3, 5), (6, 5)], fill=light)
        d.line([(9, 5), (12, 5)], fill=light)
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
        _plate(one, (x, y, w, 10), light, mid, dark, rng)
        if style == "greek" and name == "front":   # a muscled cuirass
            for px, py in ((2, 3), (5, 3), (3, 6), (4, 6)):
                one.putpixel((x + px, y + py), light)
        elif name in ("front", "back"):             # mail rings
            for j in range(2, 10, 2):
                for i in range(j % 4 // 2, w, 2):
                    one.putpixel((x + i, y + j), dark)
    arm = box_faces(40, 16, 4, 12, 4)
    for name, rect in arm.items():
        if name == "bottom":
            continue
        x, y, w, h = rect
        _plate(one, (x, y, w, min(h, 5)), light, mid, dark, rng)
    leg = box_faces(0, 16, 4, 12, 4)
    for name, rect in leg.items():
        x, y, w, h = rect
        if name == "top":
            continue
        if name == "bottom":
            fill_rect(one, x, y, w, h, dark, rng, 4)
            continue
        _plate(one, (x, y + h - 4, w, 4), light, mid, dark, rng)
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
