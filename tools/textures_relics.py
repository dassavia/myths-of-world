"""Textures of the relics (see gen_relics.py): the bident of Hades, the talaria, the Titan's breastplate, the armour of
the Nemean lion, the eye and helmet of Heimdall with their armour layers, Brisingamen, the horn of Vingolf, and the earth
scorched by Mjolnir."""
from PIL import Image

from textures import box_faces, fill_rect, item, jitter, mix, rgb, save, scale  # noqa: F401

GOLD, GOLD_LIGHT, GOLD_DARK = rgb(0xE2B33C), rgb(0xFFE08A), rgb(0x9A6E1E)
BRONZE, BRONZE_LIGHT, BRONZE_DARK = rgb(0xC9783A), rgb(0xF2A866), rgb(0x7A3E1A)
WING, WING_SHADE = rgb(0xF6F4EE), rgb(0xC8C4BA)
SOUL = rgb(0x5AE8E8)
FUR, FUR_LIGHT, FUR_DARK, MANE = rgb(0xC8923E), rgb(0xE8B865), rgb(0x8A5A22), rgb(0x6E4018)
CLAW = rgb(0xF0E8D0)


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


def draw_brisingamen(img, d, rng):
    """Freyja's flaming necklace: a heavy gold torc, its links ending in dragon heads, set with amber that glows like
    fire."""
    d.arc([1, 0, 14, 13], 15, 165, fill=GOLD, width=2)
    d.arc([2, 1, 13, 12], 30, 150, fill=GOLD_LIGHT, width=1)
    for x, y in ((3, 9), (5, 11), (10, 11), (12, 9)):
        img.putpixel((x, y), rgb(0xE8642A))
        img.putpixel((x, y - 1), rgb(0xFFB040))
    d.polygon([(6, 11), (9, 11), (10, 13), (8, 15), (7, 15), (5, 13)], fill=GOLD_DARK)
    d.polygon([(7, 12), (8, 12), (9, 13), (8, 14), (7, 14), (6, 13)], fill=rgb(0xFF8A2A))
    img.putpixel((7, 12), rgb(0xFFE08A))
    img.putpixel((1, 7), GOLD_LIGHT)
    img.putpixel((14, 7), GOLD_LIGHT)


def draw_horn_of_vingolf(img, d, rng):
    """War horn of the valkyries: dark ox horn bound in silver, with a raven feather on its cord."""
    horn, horn_light, silver = rgb(0x4A3A2E), rgb(0x7A6450), rgb(0xD8DCE4)
    d.polygon([(2, 12), (4, 9), (8, 6), (12, 3), (14, 1), (14, 4), (10, 8), (5, 12), (3, 14)], fill=horn)
    d.line([(4, 11), (12, 3)], fill=horn_light)
    for x, y in ((4, 10), (8, 7), (12, 3)):
        img.putpixel((x, y), silver)
        img.putpixel((x + 1, y + 1), silver)
        img.putpixel((x, y + 1), scale(silver, 0.8))
    img.putpixel((14, 1), silver)
    d.line([(6, 11), (7, 14)], fill=rgb(0x8A6A4A))                   # cord
    d.line([(7, 14), (9, 15)], fill=rgb(0x1A1A22))                   # raven feather
    img.putpixel((8, 14), rgb(0x3A3A4A))


def draw_nemean_helmet(img, d, rng):
    """Head of the Nemean lion worn as a hood: a shaggy mane around the brow, and the upper jaw with its fangs."""
    d.ellipse([1, 1, 14, 14], fill=MANE)
    for _ in range(14):
        img.putpixel((rng.randrange(1, 15), rng.randrange(1, 15)), scale(MANE, 1.25))
    d.rectangle([4, 3, 11, 9], fill=FUR)
    d.line([(4, 3), (11, 3)], fill=FUR_LIGHT)
    img.putpixel((5, 5), rgb(0x1A1210))
    img.putpixel((10, 5), rgb(0x1A1210))
    d.rectangle([6, 6, 9, 8], fill=FUR_LIGHT)
    d.rectangle([7, 6, 8, 6], fill=rgb(0x3A2418))                   # nose
    for x in (5, 10):
        img.putpixel((x, 10), CLAW)
        img.putpixel((x, 11), CLAW)
    d.line([(5, 9), (10, 9)], fill=FUR_DARK)


def draw_nemean_chestplate(img, d, rng):
    """The golden hide of the lion, the forepaws knotted over the chest."""
    d.polygon([(1, 2), (5, 2), (7, 4), (8, 4), (10, 2), (14, 2), (14, 7), (12, 7), (12, 14), (3, 14), (3, 7), (1, 7)], fill=FUR)
    for _ in range(18):
        img.putpixel((rng.randrange(3, 12), rng.randrange(5, 14)), jitter(FUR_DARK, rng, 10))
    d.line([(1, 2), (5, 2)], fill=MANE)
    d.line([(10, 2), (14, 2)], fill=MANE)
    d.polygon([(4, 4), (7, 6), (8, 6), (11, 4), (10, 8), (5, 8)], fill=FUR_LIGHT)   # the knotted paws
    for x in (5, 7, 8, 10):
        img.putpixel((x, 9), CLAW)
    d.line([(3, 13), (12, 13)], fill=FUR_DARK)


def draw_nemean_leggings(img, d, rng):
    """Leggings of lion hide with a gold belt."""
    d.rectangle([3, 2, 12, 4], fill=FUR)
    d.line([(3, 2), (12, 2)], fill=GOLD)
    d.rectangle([3, 5, 6, 14], fill=FUR)
    d.rectangle([9, 5, 12, 14], fill=FUR)
    for _ in range(12):
        x = rng.choice((rng.randrange(3, 7), rng.randrange(9, 13)))
        img.putpixel((x, rng.randrange(5, 14)), jitter(FUR_DARK, rng, 10))
    d.line([(3, 14), (6, 14)], fill=MANE)
    d.line([(9, 14), (12, 14)], fill=MANE)


def draw_nemean_boots(img, d, rng):
    """The hind paws of the lion, claws and all."""
    for x0 in (1, 9):
        d.rectangle([x0 + 1, 6, x0 + 4, 11], fill=FUR)
        d.rectangle([x0, 11, x0 + 5, 13], fill=FUR_LIGHT)
        d.line([(x0 + 1, 6), (x0 + 4, 6)], fill=MANE)
        for i in (0, 2, 4):
            img.putpixel((x0 + i + (1 if i == 4 else 0), 14), CLAW)


def draw_family_whistle(img, d, rng):
    """A little gold whistle on a red cord, a green ender pearl set in its side (it calls across worlds)."""
    d.line([(2, 2), (5, 5)], fill=rgb(0x8A1E2A))
    d.line([(2, 2), (2, 6)], fill=rgb(0x8A1E2A))
    d.rectangle([5, 6, 13, 10], fill=GOLD)
    d.line([(5, 6), (13, 6)], fill=GOLD_LIGHT)
    d.line([(5, 10), (13, 10)], fill=GOLD_DARK)
    d.rectangle([3, 7, 4, 9], fill=GOLD_DARK)                       # mouthpiece
    img.putpixel((8, 7), rgb(0x1A1210))                              # the hole
    img.putpixel((9, 7), rgb(0x1A1210))
    d.ellipse([10, 7, 12, 9], fill=rgb(0x2A8A6A))
    img.putpixel((10, 7), rgb(0x8AF0C8))


ITEMS = {
    "family_whistle": draw_family_whistle,
    "brisingamen": draw_brisingamen,
    "horn_of_vingolf": draw_horn_of_vingolf,
    "nemean_helmet": draw_nemean_helmet,
    "nemean_chestplate": draw_nemean_chestplate,
    "nemean_leggings": draw_nemean_leggings,
    "nemean_boots": draw_nemean_boots,
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


def _fur(img, x, y, w, h, rng):
    fill_rect(img, x, y, w, h, FUR, rng, 14)
    for _ in range(w * h // 6):
        img.putpixel((x + rng.randrange(w), y + rng.randrange(h)), jitter(FUR_DARK, rng, 10))


def nemean_layer_1(rng):
    """Heracles in the lion's skin: the head as a hood with the jaws over the brow and the mane around it, the hide on
    the back and shoulders with the forepaws knotted on the chest, and the hind paws as boots."""
    img = _layer()
    head = box_faces(0, 0, 8, 8, 8)
    for name, (x, y, w, h) in head.items():
        if name == "bottom":
            continue
        fill_rect(img, x, y, w, h, MANE, rng, 16)
        if name in ("top", "back"):
            _fur(img, x + 1, y + 1, w - 2, h - 2, rng)
    fx, fy, fw, fh = head["front"]
    for i in range(1, 7):                                            # the open jaws: your face looks out of them
        for j in range(3, 8):
            img.putpixel((fx + i, fy + j), (0, 0, 0, 0))
    fill_rect(img, fx + 1, fy, 6, 3, FUR, rng, 10)                     # muzzle over the brow
    img.putpixel((fx + 3, fy + 1), rgb(0x3A2418))
    img.putpixel((fx + 4, fy + 1), rgb(0x3A2418))
    img.putpixel((fx + 1, fy + 1), rgb(0x1A1210))
    img.putpixel((fx + 6, fy + 1), rgb(0x1A1210))
    for i in (1, 2, 5, 6):                                           # fangs
        img.putpixel((fx + i, fy + 3), CLAW)
    body = box_faces(16, 16, 8, 12, 4)
    for name, (x, y, w, h) in body.items():
        if name == "bottom":
            continue
        _fur(img, x, y, w, h, rng)
        if name == "front":
            for i in range(w):                                       # the open front of the hide
                for j in range(3, h):
                    if 2 <= i <= 5:
                        img.putpixel((x + i, y + j), (0, 0, 0, 0))
            fill_rect(img, x + 1, y, 6, 2, FUR_LIGHT, rng, 8)        # forepaws knotted at the throat
            for i in (1, 3, 4, 6):
                img.putpixel((x + i, y + 2), CLAW)
        if name == "top":
            fill_rect(img, x, y, w, h, MANE, rng, 12)
    arm = box_faces(40, 16, 4, 12, 4)
    for name, (x, y, w, h) in arm.items():
        if name == "bottom":
            continue
        _fur(img, x, y, w, min(h, 5), rng)
        if h > 5:
            fill_rect(img, x, y + 4, w, 1, MANE, rng, 8)
    leg = box_faces(0, 16, 4, 12, 4)
    for name, (x, y, w, h) in leg.items():
        if name == "top":
            continue
        if name == "bottom":
            fill_rect(img, x, y, w, h, FUR_DARK, rng, 6)
            continue
        _fur(img, x, y + h - 5, w, 5, rng)
        fill_rect(img, x, y + h - 5, w, 1, MANE, rng, 8)
        if name == "front":
            for i in (0, 2, 3):
                img.putpixel((x + i, y + h - 1), CLAW)
    return img


def nemean_layer_2(rng):
    """Leggings of lion hide: a gold belt round the waist and fur down to the knees."""
    img = _layer()
    body = box_faces(16, 16, 8, 12, 4)
    for name, (x, y, w, h) in body.items():
        if name in ("top", "bottom"):
            continue
        _fur(img, x, y + h - 5, w, 5, rng)
        fill_rect(img, x, y + h - 5, w, 1, GOLD, rng, 6)
    leg = box_faces(0, 16, 4, 12, 4)
    for name, (x, y, w, h) in leg.items():
        if name in ("top", "bottom"):
            continue
        _fur(img, x, y, w, 9, rng)
        fill_rect(img, x, y + 8, w, 1, MANE, rng, 8)
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
