"""Textures of the relics (see gen_relics.py): the bident of Hades, the talaria, the Titan's breastplate, the eye and
helmet of Heimdall with their armour layers, and the earth scorched by Mjolnir."""
from PIL import Image

from textures import box_faces, fill_rect, item, jitter, mix, rgb, save, scale  # noqa: F401

GOLD, GOLD_LIGHT, GOLD_DARK = rgb(0xE2B33C), rgb(0xFFE08A), rgb(0x9A6E1E)
BRONZE, BRONZE_LIGHT, BRONZE_DARK = rgb(0xC9783A), rgb(0xF2A866), rgb(0x7A3E1A)
WING, WING_SHADE = rgb(0xF6F4EE), rgb(0xC8C4BA)
SOUL = rgb(0x5AE8E8)


# ---------------------------------------------------------------- items

def draw_bident(img, d, rng):
    """Black iron bident of Hades: a long shaft and two barbed prongs wreathed in soul fire."""
    shaft, iron, edge = rgb(0x2A2630), rgb(0x4A4652), rgb(0x8A8696)
    for i in range(10):
        img.putpixel((1 + i, 14 - i), shaft)
        img.putpixel((2 + i, 14 - i), scale(shaft, 1.5))
    for x, y in ((8, 3), (9, 4), (10, 5), (11, 6), (12, 7)):       # the crossbar of the fork
        img.putpixel((x, y), iron)
    for i in range(1, 4):                                          # two prongs, parallel to the shaft
        img.putpixel((8 + i, 3 - i), edge)
        img.putpixel((12 + i, 7 - i), edge)
    img.putpixel((11, 0), SOUL)
    img.putpixel((15, 4), SOUL)
    img.putpixel((10, 3), SOUL)
    img.putpixel((13, 4), SOUL)
    img.putpixel((3, 12), GOLD)
    img.putpixel((4, 11), GOLD_DARK)


def draw_talaria(img, d, rng):
    """Golden sandals of Hermes with little white wings at the heels."""
    for x0 in (1, 8):
        d.rectangle([x0 + 2, 6, x0 + 4, 12], fill=GOLD)
        for y in range(7, 12, 2):
            d.line([(x0 + 2, y), (x0 + 4, y)], fill=GOLD_DARK)
        d.line([(x0 + 1, 13), (x0 + 6, 13)], fill=BRONZE_DARK)
        d.polygon([(x0, 6), (x0 + 2, 8), (x0 + 2, 10), (x0 - 1 if x0 > 1 else 0, 9)], fill=WING)
        img.putpixel((x0 + 1, 8), WING_SHADE)
        img.putpixel((x0 + 3, 6), GOLD_LIGHT)


def draw_titan_breastplate(img, d, rng):
    """A huge bronze breastplate with a starry sky worked in gold over the chest, for those who held up the heavens."""
    d.polygon([(1, 2), (6, 2), (7, 4), (8, 4), (9, 2), (14, 2), (14, 7), (12, 7), (12, 14), (3, 14), (3, 7), (1, 7)], fill=BRONZE)
    d.line([(1, 2), (6, 2)], fill=BRONZE_LIGHT)
    d.line([(9, 2), (14, 2)], fill=BRONZE_LIGHT)
    d.rectangle([4, 5, 11, 10], fill=rgb(0x1E2A5A))
    for x, y in ((5, 6), (8, 5), (10, 7), (6, 9), (9, 9)):
        img.putpixel((x, y), GOLD_LIGHT)
    d.line([(4, 11), (11, 11)], fill=GOLD)
    d.line([(3, 13), (12, 13)], fill=BRONZE_DARK)


def draw_heimdall_eye(img, d, rng):
    """The all-seeing eye: a golden iris with rays."""
    d.ellipse([2, 4, 13, 11], fill=rgb(0xF4F2EA))
    d.ellipse([5, 4, 10, 11], fill=GOLD)
    d.ellipse([6, 5, 9, 10], fill=rgb(0xFFC83C))
    d.rectangle([7, 6, 8, 9], fill=rgb(0x1A1210))
    img.putpixel((6, 6), rgb(0xFFFFFF))
    for x, y in ((7, 1), (8, 1), (1, 7), (14, 8), (3, 2), (12, 2), (3, 13), (12, 13)):
        img.putpixel((x, y), GOLD_LIGHT)


def draw_heimdall_helmet(img, d, rng):
    """Gilded helmet of the watchman, the eye of Heimdall set over the brow, and a pair of ram's horns."""
    d.rectangle([3, 3, 12, 11], fill=GOLD)
    d.line([(3, 3), (12, 3)], fill=GOLD_LIGHT)
    d.rectangle([5, 8, 6, 9], fill=(0, 0, 0, 0))
    d.rectangle([9, 8, 10, 9], fill=(0, 0, 0, 0))
    d.rectangle([7, 8, 8, 11], fill=GOLD_DARK)
    d.rectangle([7, 4, 8, 6], fill=rgb(0xFFC83C))
    img.putpixel((7, 5), rgb(0x1A1210))
    for x, y in ((2, 4), (1, 5), (1, 6), (2, 7), (13, 4), (14, 5), (14, 6), (13, 7)):
        img.putpixel((x, y), rgb(0xD8C8A8))
    d.line([(3, 11), (12, 11)], fill=GOLD_DARK)


ITEMS = {
    "bident_of_hades": draw_bident,
    "talaria": draw_talaria,
    "titan_breastplate": draw_titan_breastplate,
    "heimdall_eye": draw_heimdall_eye,
    "heimdall_helmet": draw_heimdall_helmet,
}


# ---------------------------------------------------------------- armour on the body (64x32 layer_1)

def _layer():
    return Image.new("RGBA", (64, 32), (0, 0, 0, 0))


def talaria_layer(rng):
    """Gold sandal straps up the shins and white wings on both sides of the ankles."""
    img = _layer()
    leg = box_faces(0, 16, 4, 12, 4)
    for name, (x, y, w, h) in leg.items():
        if name == "top":
            continue
        if name == "bottom":
            fill_rect(img, x, y, w, h, GOLD_DARK, rng, 4)
            continue
        for j in (h - 5, h - 3):
            fill_rect(img, x, y + j, w, 1, GOLD, rng, 6)
        fill_rect(img, x, y + h - 1, w, 1, GOLD_DARK, rng, 4)
        if name in ("right", "left"):
            for i in range(w):
                for j in range(h - 4 - i // 2, h - 1):
                    img.putpixel((x + i, y + j), WING if (i + j) % 2 else WING_SHADE)
    return img


def titan_layer(rng):
    """A bronze breastplate with a starry sky on the chest and broad pauldrons."""
    img = _layer()
    body = box_faces(16, 16, 8, 12, 4)
    for name, (x, y, w, h) in body.items():
        if name in ("top", "bottom"):
            continue
        fill_rect(img, x, y, w, 11, BRONZE, rng, 8)
        fill_rect(img, x, y, w, 1, BRONZE_LIGHT, rng, 4)
        fill_rect(img, x, y + 10, w, 1, GOLD, rng, 4)
        if name == "front":
            fill_rect(img, x + 1, y + 2, w - 2, 6, rgb(0x1E2A5A), rng, 6)
            for px, py in ((2, 3), (5, 2), (6, 5), (3, 6), (1, 4)):
                img.putpixel((x + px, y + py), GOLD_LIGHT)
    arm = box_faces(40, 16, 4, 12, 4)
    for name, (x, y, w, h) in arm.items():
        if name == "bottom":
            continue
        fill_rect(img, x, y, w, min(h, 4), BRONZE, rng, 8)
        fill_rect(img, x, y, w, 1, BRONZE_LIGHT, rng, 4)
        if h > 4:
            fill_rect(img, x, y + 3, w, 1, GOLD, rng, 4)
    return img


def heimdall_layer(rng):
    """A gilded helmet with an open face, the golden eye over the brow and curling horns on the sides."""
    img = _layer()
    head = box_faces(0, 0, 8, 8, 8)
    for name, (x, y, w, h) in head.items():
        if name == "bottom":
            continue
        fill_rect(img, x, y, w, h, GOLD, rng, 8)
        fill_rect(img, x, y, w, 1, GOLD_LIGHT, rng, 4)
    fx, fy, fw, fh = head["front"]
    for i in range(1, 7):
        for j in range(4, 8):
            img.putpixel((fx + i, fy + j), (0, 0, 0, 0))
    fill_rect(img, fx + 3, fy + 4, 2, 2, GOLD_DARK, rng, 4)        # nose guard
    img.putpixel((fx + 3, fy + 2), rgb(0xFFC83C))
    img.putpixel((fx + 4, fy + 2), rgb(0x1A1210))
    for name in ("right", "left"):
        x, y, w, h = head[name]
        for i, j in ((2, 2), (3, 2), (4, 3), (4, 4), (3, 5), (2, 5)):
            img.putpixel((x + i, y + j), rgb(0xD8C8A8))
    return img


LAYERS = {"talaria": talaria_layer, "titan_breastplate": titan_layer, "heimdall_helmet": heimdall_layer}


# ---------------------------------------------------------------- blocks

def scorched_earth(rng):
    """Soil burnt black by lightning, cracked, with a few embers still glowing."""
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(0x2A2422), rng, 8)
    for _ in range(30):
        img.putpixel((rng.randrange(16), rng.randrange(16)), jitter(rgb(0x3E3632), rng, 6))
    for _ in range(3):                                   # cracks
        x, y = rng.randrange(16), rng.randrange(16)
        for _ in range(5):
            img.putpixel((x % 16, y % 16), rgb(0x141010))
            x += rng.choice((-1, 0, 1))
            y += 1
    for _ in range(5):
        img.putpixel((rng.randrange(16), rng.randrange(16)), jitter(rgb(0xE8642A), rng, 10))
    img.putpixel((rng.randrange(16), rng.randrange(16)), rgb(0xFFC83C))
    return img
