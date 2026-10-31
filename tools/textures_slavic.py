"""Textures of the Slavic content (Nav), drawn with the helpers of textures.py and textures_norse.py."""
from PIL import Image

from textures import (amazon, band, beast, box_faces, face, fill_rect, humanoid, hydra, item, jitter, rgb, save, scale,
                      shade_parts, side_faces, speckle)
from textures_norse import beard, draw_fang, draw_journal, giant, norse_merchant

__all__ = ["BLOCKS", "ITEMS", "ENTITIES", "LAYERS", "item", "save"]

GOLD, GOLD_LIGHT, GOLD_DARK = rgb(0xE2B33C), rgb(0xFFE08A), rgb(0x9A6E1E)
SOUL = rgb(0x5AE8E8)


# ====================================================================== blocks

def world_tree_hollow(rng):
    """The opening in the bark: a ragged rim of oak bark around a deep dark hollow, soul light glimmering inside."""
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(0x6B5236), rng, 10)
    for x in range(0, 16, 3):
        for y in range(16):
            if (y + x) % 5:
                img.putpixel((x, y), jitter(rgb(0x4A3824), rng, 6))
    for x in range(16):
        for y in range(16):
            dx, dy = (x - 7.5) / 5.6, (y - 8.5) / 7.4
            r = dx * dx + dy * dy
            if r < 1.0 - rng.random() * 0.08:
                depth = 1.0 - r
                c = scale(rgb(0x2A1E14), 1.0 - depth * 0.85)
                img.putpixel((x, y), jitter(c, rng, 3))
            elif r < 1.25:
                img.putpixel((x, y), jitter(rgb(0x3A2A1A), rng, 6))
    for _ in range(5):
        x, y = rng.randrange(5, 11), rng.randrange(5, 14)
        img.putpixel((x, y), jitter(SOUL, rng, 20))
    return img


BLOCKS = {"world_tree_hollow": world_tree_hollow}


# ====================================================================== items

def draw_acorn(img, d, rng):
    d.ellipse([4, 6, 11, 14], fill=rgb(0xB07A3A))
    d.ellipse([5, 8, 7, 11], fill=rgb(0xD8A060))
    d.chord([3, 3, 12, 10], 180, 360, fill=rgb(0x6B4A2B))
    for x in range(4, 12, 2):
        img.putpixel((x, 5), rgb(0x8A6A3E))
    d.line([(8, 1), (8, 3)], fill=rgb(0x4A3220))
    d.polygon([(9, 2), (13, 0), (14, 3), (11, 4)], fill=rgb(0x7EC04A))
    img.putpixel((12, 2), GOLD_LIGHT)
    img.putpixel((6, 12), rgb(0xFFF0A0))


def draw_bottle(img, d, rng, water, light):
    d.rectangle([6, 1, 9, 2], fill=rgb(0x8A6A3A))
    d.rectangle([6, 3, 9, 5], fill=rgb(0xD8E8F0))
    d.ellipse([3, 5, 12, 14], fill=rgb(0xD8E8F0))
    d.ellipse([4, 7, 11, 13], fill=rgb(water))
    d.ellipse([5, 8, 7, 10], fill=rgb(light))
    for _ in range(3):
        img.putpixel((rng.randrange(5, 11), rng.randrange(8, 13)), rgb(0xFFFFFF))


def draw_karavai(img, d, rng):
    d.ellipse([1, 5, 14, 14], fill=rgb(0xB8762E))
    d.ellipse([2, 4, 13, 12], fill=rgb(0xD8984A))
    d.ellipse([4, 5, 9, 8], fill=rgb(0xF0C070))
    for x, y in ((5, 9), (8, 7), (10, 9), (7, 10)):     # a braided pattern on top
        img.putpixel((x, y), rgb(0x8A5420))
    img.putpixel((8, 8), rgb(0xFFFFFF))                  # the salt in the middle


def draw_firebird_feather(img, d, rng):
    d.line([(3, 13), (12, 2)], fill=rgb(0xFFD040))
    for i in range(8):
        x, y = 4 + i, 12 - i
        c = (0xC0262E, 0xE5501F, 0xFF8A1E, 0xFFD040)[min(3, i // 2)]
        d.line([(x - 2, y - 1), (x, y)], fill=rgb(c))
        d.line([(x + 1, y + 2), (x, y)], fill=rgb(c))
    d.ellipse([9, 2, 12, 5], fill=rgb(0xFFD040))
    img.putpixel((10, 3), rgb(0x2E6AC8))
    img.putpixel((11, 4), rgb(0xC0262E))


def draw_pelt(img, d, rng):
    d.polygon([(2, 3), (6, 2), (10, 2), (14, 3), (13, 8), (14, 13), (10, 12), (6, 12), (2, 13), (3, 8)], fill=rgb(0x5A4A3E))
    for _ in range(18):
        img.putpixel((rng.randrange(3, 13), rng.randrange(3, 12)), jitter(rgb(0x7A6A5A), rng, 10))
    d.line([(4, 7), (12, 7)], fill=rgb(0x3A2E26))
    img.putpixel((6, 4), rgb(0xE8C23A))


def draw_zmey_scale(img, d, rng):
    d.polygon([(8, 1), (14, 6), (12, 13), (8, 15), (4, 13), (2, 6)], fill=rgb(0x2E5A2A))
    d.polygon([(8, 3), (12, 7), (10, 12), (8, 13), (6, 12), (4, 7)], fill=rgb(0x3E7A36))
    d.line([(8, 3), (8, 13)], fill=rgb(0x1E3A1A))
    d.line([(2, 6), (8, 1), (14, 6)], fill=rgb(0xE5501F))
    img.putpixel((6, 6), rgb(0x8ABE6A))


def draw_koschei_egg(img, d, rng):
    d.ellipse([3, 2, 12, 14], fill=rgb(0xE8E4DA))
    d.ellipse([4, 3, 7, 7], fill=rgb(0xFFFFFF))
    for x in range(4, 12, 2):
        img.putpixel((x, 9), rgb(0x3A2A4A))
        img.putpixel((x + 1, 10), rgb(0x3A2A4A))
    for x, y in ((6, 12), (9, 5), (10, 12)):
        img.putpixel((x, y), rgb(0x6A3A8A))


def draw_needle(img, d, rng):
    d.line([(3, 13), (13, 3)], fill=rgb(0xC8CCD4))
    d.line([(4, 13), (13, 4)], fill=rgb(0x8A8E96))
    img.putpixel((3, 13), rgb(0x5A5E66))
    img.putpixel((4, 12), (0, 0, 0, 0))                   # the eye of the needle
    img.putpixel((13, 3), rgb(0x9AE8FF))
    img.putpixel((14, 2), SOUL)
    img.putpixel((12, 2), scale(SOUL, 0.7))


def draw_kladenets(img, d, rng):
    d.line([(5, 10), (14, 1)], fill=rgb(0xD8DCE4), width=2)
    d.line([(6, 10), (14, 2)], fill=rgb(0x9AA2B4))
    d.line([(7, 8), (13, 2)], fill=rgb(0xF4F8FF))
    d.line([(2, 8), (7, 13)], fill=GOLD, width=2)
    d.line([(1, 14), (4, 11)], fill=rgb(0x6B2A1A), width=2)
    img.putpixel((1, 15), GOLD_DARK)
    img.putpixel((4, 10), rgb(0xC0262E))


def draw_skorokhody(img, d, rng):
    for x0 in (1, 8):
        d.rectangle([x0 + 1, 2, x0 + 4, 11], fill=rgb(0x8A1E1E))
        d.rectangle([x0, 11, x0 + 6, 13], fill=rgb(0x6A1414))
        d.line([(x0 + 1, 2), (x0 + 4, 2)], fill=GOLD)
        d.line([(x0 + 1, 7), (x0 + 4, 7)], fill=GOLD_DARK)
        img.putpixel((x0 + 6, 12), GOLD_LIGHT)            # upturned toe
    for x, y in ((4, 4), (11, 5)):
        img.putpixel((x, y), rgb(0xFFF0C0))


def draw_shapka(img, d, rng):
    d.chord([2, 2, 13, 14], 180, 360, fill=rgb(0x8A1E2A))
    d.rectangle([1, 8, 14, 12], fill=rgb(0x6B4A2E))
    for _ in range(14):
        img.putpixel((rng.randrange(1, 15), rng.randrange(8, 13)), jitter(rgb(0x8A6A48), rng, 10))
    d.line([(4, 5), (11, 5)], fill=GOLD)
    for x, y in ((3, 1), (12, 2), (8, 0)):
        img.putpixel((x, y), rgb(0xE8F0FF))                 # it shimmers


ITEMS = {
    "world_tree_acorn": draw_acorn,
    "slavic_journal": lambda img, d, rng: draw_journal(img, d, rng, cover=0x8A1E24, trim=0xE2B33C),
    "slavic_journal_complete": lambda img, d, rng: draw_journal(img, d, rng, cover=0x24386A, trim=0xFFE08A),
    "living_water": lambda img, d, rng: draw_bottle(img, d, rng, 0x3A8AE8, 0xA8E0FF),
    "dead_water": lambda img, d, rng: draw_bottle(img, d, rng, 0x4A3A5A, 0x8A7A9A),
    "karavai": draw_karavai,
    "firebird_feather": draw_firebird_feather,
    "upyr_fang": lambda img, d, rng: draw_fang(img, d, rng, color=0xE8E0D0, root=0x8A1414),
    "volkolak_pelt": draw_pelt,
    "zmey_scale": draw_zmey_scale,
    "koschei_egg": draw_koschei_egg,
    "koschei_needle": draw_needle,
    "kladenets": draw_kladenets,
    "skorokhody": draw_skorokhody,
    "shapka_nevidimka": draw_shapka,
}


# ====================================================================== entities

def leshy(rng):
    """Master of the forest: skin of bark, a beard and hair of moss, eyes glowing green like foxfire."""
    img, parts = humanoid(rng, 0x5A4632, 0x4E6A34, 0x4A3A2A, hair=0x5E8A3A, sleeves=0)
    face(img, parts["head"], iris=0x9AE85A, eye_row=3, brow=0x3A4A24)
    beard(img, parts["head"], 0x5E8A3A, rng, rows=4, braids=False)
    for part in ("head", "arm", "leg", "body"):
        for rect in side_faces(parts[part]):
            speckle(img, rect, rgb(0x3A2A1A), rng, 10)        # cracks in the bark
            speckle(img, rect, rgb(0x6E9A44), rng, 5)         # moss
    band(img, parts["body"], 7, 1, rgb(0x6B4A2B), rng)        # a belt of bast
    hat = box_faces(32, 0, 8, 8, 8)
    for name in ("front", "right", "left", "back"):
        x, y, w, h = hat[name]
        for i in range(0, w, 2):
            img.putpixel((x + i, y), rgb(0x4A3A24))             # twigs in the hair
            img.putpixel((x + i, y + 1), rgb(0x5E8A3A))
    shade_parts(img, parts)
    return img


def kikimora(rng):
    """A crooked little bog hag: grey-green skin, ragged clothes, long mossy hair, yellow eyes."""
    img, parts = humanoid(rng, 0x7A8A6A, 0x4E5A3A, 0x3A4A2E, hair=0x4E6A2E, sleeves=6)
    face(img, parts["head"], iris=0xE8D44D, eye_row=3, brow=0x2E3A1E)
    x, y, w, h = parts["head"]["front"]
    fill_rect(img, x + 3, y + 4, 2, 2, scale(rgb(0x7A8A6A), 0.8), rng, 4)    # a long nose
    for name in ("right", "left", "back"):
        rx, ry, rw, rh = parts["head"][name]
        fill_rect(img, rx, ry, rw, rh, rgb(0x4E6A2E), rng, 12)
    for rect in side_faces(parts["body"]) + side_faces(parts["leg"]):
        speckle(img, rect, rgb(0x2A2A1A), rng, 8)             # mud
        x, y, w, h = rect
        if h > 8:
            for i in range(0, w, 2):
                img.putpixel((x + i, y + h - 1), (0, 0, 0, 0))     # a ragged hem
    shade_parts(img, parts)
    return img


def upyr(rng):
    """A blood-drinking dead man: deathly pale, red eyes, fangs, a dark red caftan stained darker."""
    img, parts = humanoid(rng, 0xD8D4CC, 0x4A1A1E, 0x2A2228, hair=0x1A1418, sleeves=8)
    face(img, parts["head"], iris=0xC0262E, eye_row=3, brow=0x1A1418)
    x, y, w, h = parts["head"]["front"]
    img.putpixel((x + 2, y + 6), rgb(0x5A0E10))
    img.putpixel((x + 5, y + 6), rgb(0x5A0E10))
    img.putpixel((x + 3, y + 6), rgb(0xF4F1EA))
    img.putpixel((x + 4, y + 6), rgb(0xF4F1EA))                 # fangs
    img.putpixel((x + 3, y + 7), rgb(0x8A1414))
    band(img, parts["body"], 0, 2, rgb(0x2A0E10), rng)
    band(img, parts["body"], 7, 1, rgb(0xC9962E), rng)
    for rect in side_faces(parts["body"]):
        speckle(img, rect, rgb(0x2A0A0C), rng, 6)
    shade_parts(img, parts)
    return img


def rusalka(rng):
    """The water maiden: pale bluish skin, long green hair down to the waist, a wet white shift."""
    img = amazon(rng, skin=0xE4ECEC, hair=0x3E8A6A, dress=0xE8ECE4, trim=0x8AC8B0, eyes=0x5AB8A8, outfit="peplos",
                 style="long", flower=0xE8E0F0, lips=0x9AB0C0)
    # Strands of river weed in the hair and a little transparency at the hem, like water.
    for _ in range(20):
        x, y = rng.randrange(32, 64), rng.randrange(0, 16)
        if img.getpixel((x, y))[3] > 0:
            img.putpixel((x, y), jitter(rgb(0x2A6A4A), rng, 10))
    pixels = img.load()
    for x in range(64):
        for y in range(64):
            r, g, b, a = pixels[x, y]
            if a:
                pixels[x, y] = (r, g, b, 215)
    return img


def firebird(rng):
    """Parrot texture layout (32x32): feathers of flame, orange and gold with red tips, a golden beak."""
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    fill_rect(img, 0, 0, 32, 32, rgb(0xE5701F), rng, 10)
    for _ in range(60):
        img.putpixel((rng.randrange(32), rng.randrange(32)), jitter(rgb(rng.choice((0xFFD040, 0xFF9A2E, 0xC0262E))), rng, 10))
    fill_rect(img, 0, 16, 32, 6, rgb(0xFFB030), rng, 12)      # bright wings and tail
    fill_rect(img, 10, 6, 6, 4, rgb(0xFFD040), rng, 4)         # beak1
    fill_rect(img, 15, 6, 6, 4, rgb(0xE8B830), rng, 4)         # beak2
    fill_rect(img, 14, 17, 6, 6, rgb(0x8A3A1E), rng, 4)        # feet
    for x, y in ((4, 5), (2, 5), (6, 5)):
        img.putpixel((x, y), rgb(0x1A1410))                     # eyes
    return img


ENTITIES = {
    "leshy": leshy,
    "kikimora": kikimora,
    "upyr": upyr,
    "rusalka": rusalka,
    "firebird": firebird,
    "volkolak": lambda rng: beast(rng, 0x5A4A3E, 0x7A6A5A, 0xE8C23A, back=0x3A2E26, belly=0xA89A86, claws=0xD8D0C0),
    # 0 the merchant in a red caftan, 1 Baba Yaga in a headscarf, 2 the smith in a leather apron (see SlavicMerchant).
    "slavic_merchant_0": lambda rng: norse_merchant(rng, 0xA8282E, 0xE2B33C, skin=0xE2B490, hair=0x6B4A2B),
    "slavic_merchant_1": lambda rng: norse_merchant(rng, 0x4A3A2A, 0x8A2A2A, skin=0xC8A88A, hair=0xD8D0C0, beard=False,
                                                    hood=0x8A1E2A),
    "slavic_merchant_2": lambda rng: norse_merchant(rng, 0x5A3A24, 0x3A2A1C, skin=0xC8956B, hair=0x2A1A14, apron=0x2A1E14),
}


# ====================================================================== armour layers (64x32 layer_1)

def _layer():
    return Image.new("RGBA", (64, 32), (0, 0, 0, 0))


def skorokhody_layer(rng):
    """Red leather boots up to mid-shin with gold bands."""
    img = _layer()
    leg = box_faces(0, 16, 4, 12, 4)
    for name, (x, y, w, h) in leg.items():
        if name == "top":
            continue
        if name == "bottom":
            fill_rect(img, x, y, w, h, rgb(0x4A0E0E), rng, 4)
            continue
        fill_rect(img, x, y + h - 6, w, 6, rgb(0x8A1E1E), rng, 8)
        fill_rect(img, x, y + h - 6, w, 1, GOLD, rng, 4)
        fill_rect(img, x, y + h - 1, w, 1, rgb(0x4A0E0E), rng, 4)
    return img


def shapka_layer(rng):
    """A fur-trimmed cap with a red crown."""
    img = _layer()
    head = box_faces(0, 0, 8, 8, 8)
    fill_rect(img, *head["top"], rgb(0x8A1E2A), rng, 8)
    for name in ("front", "back", "right", "left"):
        x, y, w, h = head[name]
        fill_rect(img, x, y, w, 1, rgb(0x8A1E2A), rng, 8)
        fill_rect(img, x, y + 1, w, 2, rgb(0x6B4A2E), rng, 16)
    x, y, w, h = head["front"]
    img.putpixel((x + 3, y), GOLD)
    img.putpixel((x + 4, y), GOLD_LIGHT)
    return img


LAYERS = {"skorokhody": skorokhody_layer, "shapka_nevidimka": shapka_layer}
