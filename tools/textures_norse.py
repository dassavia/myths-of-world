"""Placeholder textures for the Norse content (Jotunheim), drawn with the helpers of textures.py."""
import math

from PIL import Image

from textures import (amazon, band, beast, box_faces, face, fill_rect, greek_merchant, humanoid, item, jitter, leaves, rgb, save,
                      scale, shade_parts, side_faces, speckle, stone_bricks)

__all__ = ["BLOCKS", "ITEMS", "ENTITIES", "item", "save"]


# ====================================================================== blocks

RUNE_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (2, 0)],          # fehu
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 1), (2, 2), (2, 3)],  # uruz
    [(1, 0), (1, 1), (1, 2), (1, 3), (0, 1), (2, 1)],          # tiwaz-like
    [(0, 0), (1, 1), (2, 2), (2, 0), (0, 2), (1, 3)],          # gebo
]


def carved_runestone(rng):
    img = stone_bricks(rng, 0x6E7378, 0x4A4E52, rows=2)
    for n, (ox, oy) in enumerate(((2, 2), (10, 2), (2, 10), (10, 10))):
        for x, y in RUNE_SHAPES[(n + rng.randrange(4)) % 4]:
            img.putpixel((ox + x, oy + y), jitter(rgb(0xC0262E), rng, 10))
    return img


def ironwood_bark(rng):
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(0x3E3A38), rng, 6)
    for x in range(0, 16, 3):
        off = rng.randrange(16)
        for j in range(16):
            if (j + off) % 7 != 0:
                img.putpixel((x, j), jitter(rgb(0x2A2624), rng, 4))
    # Rusty sheen: the trees of the Iron Wood.
    for _ in range(14):
        img.putpixel((rng.randrange(16), rng.randrange(16)), jitter(rgb(0x7A4A2E), rng, 12))
    return img


def ironwood_log_top(rng):
    img = Image.new("RGBA", (16, 16))
    for x in range(16):
        for y in range(16):
            r = max(abs(x - 7.5), abs(y - 7.5))
            if r > 6.5:
                c = rgb(0x3E3A38)
            else:
                c = rgb(0x8A7E70) if int(r) % 2 == 0 else rgb(0x6E6458)
            img.putpixel((x, y), jitter(c, rng, 5))
    return img


def ironwood_planks(rng):
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(0x5A524C), rng, 6)
    for y in (0, 4, 8, 12):
        for x in range(16):
            img.putpixel((x, y), jitter(rgb(0x2E2A28), rng, 3))
        cut = (y * 3 + 5) % 16
        for j in range(y, y + 4):
            img.putpixel((cut, j), jitter(rgb(0x2E2A28), rng, 3))
    for _ in range(6):
        x, y = rng.randrange(16), rng.randrange(16)
        if img.getpixel((x, y))[0] > 60:
            img.putpixel((x, y), rgb(0x8A8A8E))  # iron nails
    return img


IRONWOOD_GREENS = (0x2E3E34, 0x3A4A3E, 0x24302A, 0x46584A)
IDUNN_GREENS = (0x5E9A3E, 0x6EAA4A, 0x4E8A34, 0x7EBA5A)

BLOCKS = {
    "carved_runestone": carved_runestone,
    "ironwood_log": ironwood_bark,
    "ironwood_log_top": ironwood_log_top,
    "ironwood_planks": ironwood_planks,
    "ironwood_leaves": lambda rng: leaves(rng, IRONWOOD_GREENS, holes=0.22),
    "idunn_leaves": lambda rng: leaves(rng, IDUNN_GREENS),
    "idunn_leaves_ripe": lambda rng: leaves(rng, IDUNN_GREENS, (0xE8C23A, 0xFFF0A0), 3, 3),
}


# ====================================================================== items

def draw_journal(img, d, rng, cover=0x4A5A6E, trim=0xC0C8D0):
    d.rectangle([3, 2, 12, 14], fill=rgb(cover))
    d.rectangle([3, 2, 4, 14], fill=scale(rgb(cover), 0.7))
    d.rectangle([12, 3, 13, 13], fill=rgb(0xF4ECD8))
    for x, y in RUNE_SHAPES[0]:
        img.putpixel((7 + x, 5 + y), rgb(trim))
    d.line([(6, 11), (10, 11)], fill=rgb(trim))


def draw_apple(img, d, rng):
    d.ellipse([3, 4, 12, 13], fill=rgb(0xE8C23A))
    d.ellipse([5, 6, 7, 8], fill=rgb(0xFFF0A0))
    d.line([(8, 1), (8, 4)], fill=rgb(0x5A3A1E))
    d.polygon([(9, 2), (12, 1), (11, 3)], fill=rgb(0x5E9A3E))


def draw_mead(img, d, rng):
    d.rectangle([5, 2, 10, 3], fill=rgb(0x8A6A3A))
    d.rectangle([6, 4, 9, 5], fill=rgb(0xD8E8F0))
    d.ellipse([3, 5, 12, 14], fill=rgb(0xC98A2E))
    d.ellipse([4, 6, 7, 9], fill=rgb(0xF2C45A))


def draw_feather(img, d, rng):
    d.line([(3, 13), (12, 2)], fill=rgb(0x5A5A6E))
    for i in range(7):
        x, y = 4 + i, 11 - i
        d.line([(x - 2, y - 1), (x, y)], fill=rgb(0x1A1A24))
        d.line([(x + 1, y + 2), (x, y)], fill=rgb(0x24243A))


def draw_frost_heart(img, d, rng):
    d.polygon([(8, 14), (2, 7), (3, 3), (6, 2), (8, 4), (10, 2), (13, 3), (14, 7)], fill=rgb(0x8EC8E8))
    d.polygon([(8, 12), (4, 7), (5, 4), (8, 6)], fill=rgb(0xD8F0FF))
    img.putpixel((5, 5), rgb(0xFFFFFF))


def draw_ember(img, d, rng):
    d.polygon([(8, 2), (13, 8), (8, 14), (3, 8)], fill=rgb(0x3A1A10))
    d.polygon([(8, 4), (11, 8), (8, 12), (5, 8)], fill=rgb(0xE5501F))
    d.polygon([(8, 6), (9, 8), (8, 10), (7, 8)], fill=rgb(0xFFD040))


def draw_tusk(img, d, rng):
    d.polygon([(3, 13), (5, 9), (8, 5), (12, 2), (10, 6), (7, 11), (5, 14)], fill=rgb(0xD8CFAE))
    d.line([(4, 13), (7, 9)], fill=rgb(0xA89E7E))


def draw_fang(img, d, rng, color=0xE8E2D0, root=0x6E5A4A):
    d.polygon([(5, 2), (11, 2), (9, 13), (8, 14)], fill=rgb(color))
    d.rectangle([5, 2, 11, 4], fill=rgb(root))
    d.line([(9, 5), (8, 12)], fill=scale(rgb(color), 0.8))


def draw_crown(img, d, rng):
    d.polygon([(2, 12), (2, 5), (5, 8), (8, 3), (11, 8), (14, 5), (14, 12)], fill=rgb(0xC9962E))
    d.rectangle([2, 11, 14, 13], fill=rgb(0x8A6A1E))
    for x, c in ((5, 0x2E7A8A), (8, 0xC0262E), (11, 0x2E7A8A)):
        img.putpixel((x, 12), rgb(c))
    for _ in range(5):
        img.putpixel((rng.randrange(3, 14), rng.randrange(6, 11)), rgb(0x4E6A3A))  # barrow moss


def draw_mjolnir(img, d, rng):
    d.line([(3, 13), (9, 7)], fill=rgb(0x6B4A2B), width=2)
    d.rectangle([2, 13, 3, 14], fill=rgb(0x3A2A1C))
    d.polygon([(7, 2), (14, 9), (11, 12), (4, 5)], fill=rgb(0x8A8E96))
    d.line([(7, 2), (14, 9)], fill=rgb(0xC8CCD4))
    for x, y in ((8, 6), (9, 7), (10, 8)):
        img.putpixel((x, y), rgb(0x5AB8E8))


def draw_gleipnir(img, d, rng):
    for i in range(12):
        x = 2 + i
        y = int(8 + 4 * math.sin(i / 1.8))
        img.putpixel((x, y), rgb(0xE8E0F4))
        img.putpixel((x, y + 1), rgb(0xB8A8D8))
    for _ in range(6):
        img.putpixel((rng.randrange(2, 14), rng.randrange(3, 13)), rgb(0xFFFFFF))


def draw_surtr_sword(img, d, rng):
    d.line([(4, 11), (13, 2)], fill=rgb(0xE5501F), width=2)
    d.line([(5, 10), (13, 2)], fill=rgb(0xFFD040))
    d.line([(2, 10), (6, 14)], fill=rgb(0x2A1A14), width=2)
    d.line([(2, 14), (4, 12)], fill=rgb(0x5A2A1C), width=2)


ITEMS = {
    "norse_journal": draw_journal,
    "norse_journal_complete": lambda img, d, rng: draw_journal(img, d, rng, cover=0x6E1E24, trim=0xE2B33C),
    "idunn_apple": draw_apple,
    "mead": draw_mead,
    "raven_feather": draw_feather,
    "frost_heart": draw_frost_heart,
    "muspel_ember": draw_ember,
    "troll_tusk": draw_tusk,
    "fenrir_fang": draw_fang,
    "garm_fang": lambda img, d, rng: draw_fang(img, d, rng, color=0xC8C0B0, root=0x8A1C1C),
    "barrow_crown": draw_crown,
    "mjolnir": draw_mjolnir,
    "gleipnir": draw_gleipnir,
    "surtr_sword": draw_surtr_sword,
}


# ====================================================================== entities

def beard(img, head, color, rng, rows=3, braids=True):
    x, y, w, h = head["front"]
    fill_rect(img, x + 1, y + h - rows, w - 2, rows, rgb(color), rng, 10)
    if braids:
        for bx in (x + 2, x + 5):
            img.putpixel((bx, y + h - 1), scale(rgb(color), 0.7))
    for name in ("right", "left"):
        rx, ry, rw, rh = head[name]
        fill_rect(img, rx + (0 if name == "left" else rw - 2), ry + rh - rows, 2, rows, rgb(color), rng, 10)


def helmet(img, head, color, rng, horns=None):
    """Helm on the hat layer: a band around the head and a cap; optional horns drawn on the sides."""
    hat = box_faces(32, 0, 8, 8, 8)
    fill_rect(img, *hat["top"], rgb(color), rng, 10)
    for name in ("front", "back", "right", "left"):
        x, y, w, h = hat[name]
        fill_rect(img, x, y, w, 3, rgb(color), rng, 10)
    x, y, w, h = hat["front"]
    fill_rect(img, x + 3, y + 3, 2, 3, scale(rgb(color), 0.8), rng, 4)  # nose guard
    if horns:
        for name in ("right", "left"):
            x, y, w, h = hat[name]
            fill_rect(img, x + 3, y, 2, 2, rgb(horns), rng, 6)


def chainmail(img, rects, rng, color=0x7A7E84):
    for rect in side_faces(rects):
        x, y, w, h = rect
        for j in range(h):
            for i in range(w):
                if (i + j) % 2 == 0:
                    img.putpixel((x + i, y + j), jitter(rgb(color), rng, 10))


def draugr(rng, chief=False):
    img, parts = humanoid(rng, 0x6E7A6A, 0x4A4438, 0x3A342C, hair=0x9A9A8A, sleeves=6)
    face(img, parts["head"], iris=0x8EE0FF, eye_row=3, mouth=0x2A2420)
    beard(img, parts["head"], 0x9A9A8A, rng)
    chainmail(img, parts["body"], rng, 0x6A5A4A if not chief else 0x7A7E84)
    band(img, parts["body"], 7, 1, rgb(0x2A1E14), rng)
    for rect in side_faces(parts["arm"]) + side_faces(parts["leg"]):
        speckle(img, rect, rgb(0x4A5A44), rng, 5)  # rot
    if chief:
        helmet(img, parts["head"], 0xC9962E, rng)
        band(img, parts["leg"], 0, 3, rgb(0x6E1E24), rng)
    shade_parts(img, parts)
    return img


def troll(rng):
    img, parts = humanoid(rng, 0x6E7A5E, 0x5A4A34, 0x5A6A4E, hair=0x3A4A2E, sleeves=0)
    face(img, parts["head"], iris=0xE8C23A, eye_row=3, mouth=0x2A2A1E, brow=0x3A4A2E)
    x, y, w, h = parts["head"]["front"]
    fill_rect(img, x + 3, y + 3, 2, 3, scale(rgb(0x6E7A5E), 0.85), rng, 4)  # big nose
    img.putpixel((x + 1, y + 6), rgb(0xD8CFAE))
    img.putpixel((x + 6, y + 6), rgb(0xD8CFAE))  # tusks
    for part in ("head", "arm", "leg"):
        for rect in side_faces(parts[part]):
            speckle(img, rect, rgb(0x4E5A44), rng, 8)
            speckle(img, rect, rgb(0x8A8E80), rng, 4)  # stone in the skin
    band(img, parts["body"], 7, 5, rgb(0x5A4A34), rng)
    shade_parts(img, parts)
    return img


def giant(rng, skin, tunic, legs, hair, iris, trim, crown=None, glow=None):
    img, parts = humanoid(rng, skin, tunic, legs, hair=hair, sleeves=4)
    face(img, parts["head"], iris=iris, eye_row=3, brow=hair)
    beard(img, parts["head"], hair, rng, rows=4)
    band(img, parts["body"], 7, 1, rgb(trim), rng)
    band(img, parts["arm"], 10, 2, rgb(trim), rng)
    band(img, parts["leg"], 10, 2, scale(rgb(legs), 0.7), rng)
    if glow:
        for part in ("arm", "leg", "body"):
            for rect in side_faces(parts[part]):
                x, y, w, h = rect
                cx, cy = x + rng.randrange(w), y
                while cy < y + h:
                    img.putpixel((cx, cy), rgb(glow))
                    cx = max(x, min(x + w - 1, cx + rng.choice((-1, 0, 1))))
                    cy += 1
    if crown:
        hat = box_faces(32, 0, 8, 8, 8)
        for name in ("front", "back", "right", "left"):
            x, y, w, h = hat[name]
            for i in range(w):
                img.putpixel((x + i, y + 1), rgb(crown))
                if i % 2 == 0:
                    img.putpixel((x + i, y), rgb(crown))
    shade_parts(img, parts)
    return img


def raven(rng):
    """Parrot texture layout (32x32): all black feathers, a grey beak and feet."""
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    fill_rect(img, 0, 0, 32, 32, rgb(0x16161E), rng, 6)
    for _ in range(40):
        img.putpixel((rng.randrange(32), rng.randrange(32)), rgb(0x2A2A44))  # blue sheen
    fill_rect(img, 10, 6, 6, 4, rgb(0x3A3A3E), rng, 4)    # beak1
    fill_rect(img, 15, 6, 6, 4, rgb(0x3A3A3E), rng, 4)    # beak2
    fill_rect(img, 14, 17, 6, 6, rgb(0x2E2E30), rng, 4)   # feet
    for x, y in ((4, 5), (2, 5), (6, 5)):
        img.putpixel((x, y), rgb(0x9A9A9A))  # eyes
    return img


def norse_merchant(rng, robe, trim, skin=0xE2B490, hair=0xC9962E, beard=True, apron=None, hood=None):
    img = greek_merchant(rng, robe, trim, skin=skin, hair=hair, beard=beard, apron=apron)
    if hood:
        hat = box_faces(32, 0, 8, 10, 8)
        fill_rect(img, *hat["top"], rgb(hood), rng, 8)
        for name in ("back", "right", "left"):
            fill_rect(img, *hat[name], rgb(hood), rng, 8)
        x, y, w, h = hat["front"]
        fill_rect(img, x, y, w, 2, rgb(hood), rng, 8)
    return img


# Valkyries: the amazon skin (textures.amazon) in a mail shirt over a long dress, most with a winged helmet.
VALKYRIES = [
    dict(skin=0xF6DCCC, hair=0xF0D890, dress=0x3A5A9A, trim=0xC8CCD4, eyes=0x4A8AE8, style="braid", helm=0xC8CCD4,
         belt=0x6B4A2B),
    dict(skin=0xF8E0D0, hair=0xB8401E, dress=0x2E6A4A, trim=0xE2B33C, eyes=0x3E9A4E, style="long", helm=0xB8BCC8,
         belt=0xE2B33C),
    dict(skin=0xF2D2BC, hair=0x5A3A22, dress=0x8A1E2A, trim=0xF4F1EA, eyes=0x6A4A2A, style="twin", belt=0x3A2A1A,
         band=0xC8CCD4),
    dict(skin=0xFBE6DA, hair=0xF4ECD8, dress=0xE8E4DA, trim=0x5A8AC8, eyes=0x6AA8F0, style="wavy", helm=0xE2B33C,
         belt=0x5A8AC8),
    dict(skin=0xE8C0A0, hair=0x2A1A14, dress=0x4A3A6A, trim=0xC8CCD4, eyes=0x5A3A6A, style="ponytail", helm=0x9AA2B4,
         belt=0x2A2A2A),
    dict(skin=0xF6D8C4, hair=0xD8A050, dress=0x7A5030, trim=0xE8E0D0, eyes=0x4A7A3A, style="braid", belt=0x4A3220,
         flower=0x6AA8F0),
    dict(skin=0xF4D4C0, hair=0x8A6A4A, dress=0x2A4A6A, trim=0xE2B33C, eyes=0x3A6AB8, style="long", helm=0xC8CCD4,
         belt=0xE2B33C),
    dict(skin=0xFAE2D4, hair=0xE8C070, dress=0xA8282E, trim=0xC8CCD4, eyes=0x3A7AD8, style="wavy", helm=0xE2B33C,
         belt=0x6B4A2B),
]


ENTITIES = {
    **{f"valkyrie_{i}": (lambda spec: lambda rng: amazon(rng, outfit="valkyrie", **spec))(spec)
       for i, spec in enumerate(VALKYRIES)},
    "draugr": draugr,
    "draugr_chieftain": lambda rng: draugr(rng, chief=True),
    "troll": troll,
    "frost_giant": lambda rng: giant(rng, 0xB8D4E8, 0x5A7A9A, 0x3A5A7A, 0xF0F4FF, 0x2E7AC8, 0xD8F0FF),
    "fire_giant": lambda rng: giant(rng, 0x6A3A2A, 0x2A1A14, 0x3A2A1E, 0xE5501F, 0xFFD040, 0x8A3A1E, glow=0xE5501F),
    "thrym": lambda rng: giant(rng, 0xA8C8E0, 0x2E4A6E, 0x24384E, 0xE8F0FF, 0x5AB8E8, 0xC0C8D0, crown=0x8EC8E8),
    "surtr": lambda rng: giant(rng, 0x2A1A14, 0x1A100C, 0x2A1A14, 0xFF7A1C, 0xFFF0A0, 0xE5501F, crown=0xFFD040,
                               glow=0xFF7A1C),
    "warg": lambda rng: beast(rng, 0x4A4A4E, 0x6A6A6E, 0xE8C23A, back=0x2E2E32, belly=0x8A8A8E),
    "fenrir": lambda rng: beast(rng, 0x2E2A2A, 0x4A4444, 0xFF4A1C, back=0x1A1616, belly=0x5A5050, claws=0xD8D0C0,
                                glow=True),
    "garm": lambda rng: beast(rng, 0x3A3030, 0x5A4A4A, 0xC0262E, mane=0x8A1C1C, back=0x241C1C, belly=0x4A3A3A,
                              claws=0x8A1C1C, glow=True),
    "raven": raven,
    # 0 steward of the mead hall, 1 dwarven smith, 2 volva (see NorseMerchant).
    "norse_merchant_0": lambda rng: norse_merchant(rng, 0x2E5A3A, 0xC9962E),
    "norse_merchant_1": lambda rng: norse_merchant(rng, 0x5A3A24, 0x3A2A1C, skin=0xC8956B, hair=0x8A3A1E,
                                                   apron=0x2A1E14),
    "norse_merchant_2": lambda rng: norse_merchant(rng, 0x3A2E5A, 0xD8D0C0, hair=0xE8E0D0, beard=False, hood=0x241E3A),
}
