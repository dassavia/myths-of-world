"""Textures of the Egyptian content (the Duat), drawn with the helpers of textures.py and textures_norse.py."""
import math

from PIL import Image

from textures import (amazon, band, beast, box_faces, crayfish, face, fill_rect, humanoid, hydra, item, jitter, mix,
                      paint_box, rgb, save, scale, shade_parts, side_faces, speckle)
from textures_norse import giant, norse_merchant

__all__ = ["BLOCKS", "ITEMS", "ENTITIES", "LAYERS", "item", "save"]

GOLD, GOLD_LIGHT, GOLD_DARK = rgb(0xE2B33C), rgb(0xFFE08A), rgb(0x9A6E1E)
LAPIS, LAPIS_LIGHT = rgb(0x2A5AB0), rgb(0x5A8AE0)
LINEN, LINEN_DARK = rgb(0xE8E0C8), rgb(0xB8AE90)
TURQUOISE = rgb(0x3AB8A8)
CARNELIAN = rgb(0xC0402A)


# ====================================================================== blocks

def pyramid_stone(rng):
    """Smooth casing stone of a pyramid: pale golden limestone laid in long courses with fine joints."""
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(0xE2CC92), rng, 7)
    for y in (0, 8):
        for x in range(16):
            img.putpixel((x, y), jitter(rgb(0xB89C62), rng, 5))
    for x, y0 in ((5, 1), (12, 9)):
        for y in range(y0, y0 + 7):
            img.putpixel((x, y), jitter(rgb(0xC4A86C), rng, 5))
    for _ in range(14):
        img.putpixel((rng.randrange(16), rng.randrange(16)), jitter(rgb(0xF2E0AE), rng, 6))
    return img


def hieroglyph_stone(rng):
    """Pyramid stone carved with a column of hieroglyphs: an eye, a bird, waves of water and a reed, inlaid in blue."""
    img = pyramid_stone(rng)
    ink = rgb(0x24407A)
    fill_rect(img, 2, 1, 12, 14, rgb(0xD8C084), rng, 4)
    for x in range(2, 14):
        img.putpixel((x, 1), rgb(0xA88C52))
        img.putpixel((x, 14), rgb(0xA88C52))
    # An eye of Horus.
    for x in range(4, 9):
        img.putpixel((x, 3), ink)
    img.putpixel((6, 4), ink)
    img.putpixel((4, 4), ink)
    img.putpixel((8, 4), ink)
    img.putpixel((5, 5), ink)
    # A bird (the vulture of Nekhbet).
    for x, y in ((10, 3), (11, 3), (11, 4), (10, 5), (11, 5), (12, 5), (10, 6), (12, 6)):
        img.putpixel((x, y), ink)
    # Waves of water.
    for x in range(4, 13):
        img.putpixel((x, 9 if x % 2 else 8), ink)
    # A reed and an ankh.
    for y in range(10, 14):
        img.putpixel((5, y), ink)
    img.putpixel((6, 10), ink)
    for x, y in ((10, 10), (9, 11), (11, 11), (10, 12), (9, 12), (11, 12), (10, 13)):
        img.putpixel((x, y), rgb(0xC08A2A))
    return img


def pyramid_gate(rng):
    """The gate of shadow, animated: a dark veil of night with drifting gold dust and stars, eight frames."""
    frames = 8
    img = Image.new("RGBA", (16, 16 * frames))
    stars = [(rng.randrange(16), rng.randrange(16), rng.random()) for _ in range(14)]
    for f in range(frames):
        for x in range(16):
            for y in range(16):
                wave = math.sin((x + y * 0.6) * 0.7 + f * math.tau / frames) * 0.5 + 0.5
                c = mix(rgb(0x0A0818, 200), rgb(0x2A1A4A, 210), wave * 0.6)
                img.putpixel((x, f * 16 + y), jitter(c, rng, 4))
        for sx_, sy_, phase in stars:
            y = (sy_ - f) % 16
            glow = 0.5 + 0.5 * math.sin(phase * math.tau + f * math.tau / frames)
            img.putpixel((sx_, f * 16 + y), mix(rgb(0x8A6A2A, 230), rgb(0xFFE08A, 255), glow))
    return img


def date_palm_leaves(rng, ripe=False):
    """Fronds of the date palm: long narrow leaflets, with clusters of orange-brown dates when ripe."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for i in range(7):
        y0 = rng.randrange(16)
        x0 = rng.randrange(16)
        for k in range(9):
            x, y = (x0 + k) % 16, (y0 + k // 2) % 16
            img.putpixel((x, y), jitter(rgb(0x5A8A2E), rng, 14))
            img.putpixel((x, (y + 1) % 16), jitter(rgb(0x3E6A22), rng, 10))
    if ripe:
        for _ in range(4):
            cx, cy = rng.randrange(2, 14), rng.randrange(2, 14)
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 1)):
                img.putpixel((cx + dx, cy + dy), jitter(rgb(0xB0602A), rng, 16))
            img.putpixel((cx, cy), rgb(0xE0903A))
    return img


def nile_silt(rng):
    """The black silt of the Nile: dark wet earth, almost black, with streaks of grey clay, glints of water and tiny
    roots, the soil that gave Egypt its name of Kemet, the black land."""
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(0x2A2420), rng, 6)
    for _ in range(3):                                          # streaks of grey clay laid down by the flood
        y = rng.randrange(16)
        for x in range(16):
            if rng.random() < 0.7:
                img.putpixel((x, (y + x // 6) % 16), jitter(rgb(0x4A4440), rng, 5))
    for _ in range(18):
        img.putpixel((rng.randrange(16), rng.randrange(16)), jitter(rgb(0x1A1614), rng, 4))
    for _ in range(6):                                          # glints of water on the wet surface
        img.putpixel((rng.randrange(16), rng.randrange(16)), jitter(rgb(0x5A6A78), rng, 6))
    for _ in range(3):                                          # fine roots of papyrus
        x, y = rng.randrange(16), rng.randrange(16)
        for i in range(3):
            img.putpixel(((x + i) % 16, (y + (i % 2)) % 16), jitter(rgb(0x6A5A3A), rng, 6))
    return img


BLOCKS = {
    "nile_silt": nile_silt,
    "pyramid_stone": pyramid_stone,
    "hieroglyph_stone": hieroglyph_stone,
    "pyramid_gate": pyramid_gate,
    "date_palm_leaves": date_palm_leaves,
    "date_palm_leaves_ripe": lambda rng: date_palm_leaves(rng, ripe=True),
}


# ====================================================================== items

def draw_ankh(img, d, rng):
    d.ellipse([5, 1, 10, 7], outline=GOLD, width=2)
    d.rectangle([7, 7, 8, 14], fill=GOLD)
    d.rectangle([3, 7, 12, 8], fill=GOLD)
    img.putpixel((6, 2), GOLD_LIGHT)
    img.putpixel((7, 9), GOLD_LIGHT)
    img.putpixel((8, 14), GOLD_DARK)
    img.putpixel((7, 8), LAPIS)


def draw_dates(img, d, rng):
    d.line([(8, 1), (8, 5)], fill=rgb(0x8A6A3A))
    for x, y in ((5, 6), (9, 6), (7, 9), (4, 10), (10, 10), (7, 12)):
        d.ellipse([x, y, x + 3, y + 3], fill=rgb(0x9A4A1E))
        img.putpixel((x + 1, y + 1), rgb(0xD8803A))


def draw_honey_cake(img, d, rng):
    d.ellipse([1, 5, 14, 13], fill=rgb(0xB8762E))
    d.ellipse([2, 4, 13, 11], fill=rgb(0xD8A04A))
    d.ellipse([4, 5, 11, 9], fill=rgb(0xF0C860))
    for x, y in ((5, 6), (9, 7), (7, 8)):
        img.putpixel((x, y), rgb(0x8A3A1A))                       # dates pressed into the top
    img.putpixel((6, 5), rgb(0xFFF0A0))


def draw_wrappings(img, d, rng):
    d.polygon([(2, 3), (13, 1), (14, 4), (4, 7), (13, 8), (14, 11), (3, 14), (2, 11), (11, 9), (2, 7)], fill=LINEN)
    d.line([(3, 4), (12, 2)], fill=LINEN_DARK)
    d.line([(4, 12), (13, 10)], fill=LINEN_DARK)
    for _ in range(6):
        img.putpixel((rng.randrange(3, 13), rng.randrange(2, 13)), rgb(0x8A7A5A))


def draw_scarab_shell(img, d, rng):
    d.ellipse([3, 3, 12, 14], fill=rgb(0x1A2A3A))
    d.ellipse([5, 1, 10, 5], fill=rgb(0x14202A))
    d.line([(7, 4), (7, 14)], fill=rgb(0x0A1018))
    for x, y in ((5, 7), (9, 7), (5, 10), (10, 11)):
        img.putpixel((x, y), rgb(0x3AA88A))
    img.putpixel((6, 5), rgb(0x6AE0C0))
    img.putpixel((9, 9), TURQUOISE)


def draw_stinger(img, d, rng):
    d.line([(2, 14), (8, 8)], fill=rgb(0x8A5A2A), width=2)
    d.line([(8, 8), (11, 4)], fill=rgb(0x6A3A1A), width=2)
    d.polygon([(10, 5), (14, 1), (12, 6)], fill=rgb(0x2A1A10))
    img.putpixel((14, 1), rgb(0x9AE85A))
    img.putpixel((13, 2), rgb(0x6AC03A))


def draw_jackal_pelt(img, d, rng):
    d.polygon([(2, 3), (6, 2), (10, 2), (14, 3), (13, 8), (14, 13), (10, 12), (6, 12), (2, 13), (3, 8)], fill=rgb(0x2A2220))
    for _ in range(16):
        img.putpixel((rng.randrange(3, 13), rng.randrange(3, 12)), jitter(rgb(0x4A3A32), rng, 10))
    d.line([(4, 7), (12, 7)], fill=rgb(0x14100E))
    img.putpixel((6, 4), GOLD)


def draw_sphinx_claw(img, d, rng):
    d.polygon([(3, 13), (6, 7), (10, 3), (13, 1), (11, 5), (8, 10), (6, 14)], fill=rgb(0xD8C08A))
    d.line([(4, 13), (11, 3)], fill=rgb(0xF4E4B4))
    d.rectangle([2, 12, 6, 15], fill=rgb(0xB89A5A))
    img.putpixel((13, 1), rgb(0x6A5A3A))


def draw_apep_scale(img, d, rng):
    d.polygon([(8, 1), (14, 6), (12, 13), (8, 15), (4, 13), (2, 6)], fill=rgb(0x2A1A3A))
    d.polygon([(8, 3), (12, 7), (10, 12), (8, 13), (6, 12), (4, 7)], fill=rgb(0x4A2A5A))
    d.line([(8, 3), (8, 13)], fill=rgb(0x14081E))
    d.line([(2, 6), (8, 1), (14, 6)], fill=rgb(0xC0262E))
    img.putpixel((6, 6), rgb(0x8A6AAA))


def draw_eye_of_horus(img, d, rng):
    d.ellipse([2, 4, 13, 10], fill=rgb(0xF4F0E4), outline=LAPIS)
    d.ellipse([6, 5, 9, 9], fill=rgb(0x14141E))
    d.line([(1, 3), (13, 3)], fill=LAPIS)
    d.line([(8, 10), (8, 14)], fill=LAPIS)
    d.line([(11, 10), (13, 13), (11, 14)], fill=LAPIS)
    img.putpixel((7, 6), rgb(0xFFFFFF))
    img.putpixel((14, 3), GOLD)
    img.putpixel((0, 3), GOLD)


def draw_knot_of_isis(img, d, rng):
    red = CARNELIAN
    d.ellipse([5, 1, 10, 6], outline=red, width=2)
    d.polygon([(7, 6), (8, 6), (12, 14), (3, 14)], fill=red)
    d.line([(3, 8), (12, 8)], fill=red, width=2)
    img.putpixel((7, 10), rgb(0xE8704A))
    img.putpixel((6, 2), rgb(0xE8704A))
    img.putpixel((7, 14), GOLD)


def draw_sistrum(img, d, rng):
    d.line([(4, 15), (7, 9)], fill=rgb(0x6B4A2B), width=2)
    d.ellipse([5, 1, 13, 10], outline=GOLD, width=2)
    for y in (4, 6, 8):
        d.line([(7, y), (11, y)], fill=GOLD_LIGHT)
    img.putpixel((6, 4), GOLD_DARK)
    img.putpixel((12, 6), GOLD_DARK)
    img.putpixel((9, 1), GOLD_LIGHT)


def draw_khopesh(img, d, rng):
    blade = rgb(0xA8B4C8)
    d.arc([3, 1, 15, 12], 200, 350, fill=blade, width=3)
    d.line([(5, 8), (8, 6)], fill=blade, width=2)
    d.line([(2, 14), (5, 10)], fill=rgb(0x2A1A10), width=2)
    img.putpixel((5, 9), GOLD)
    img.putpixel((6, 9), GOLD)
    img.putpixel((1, 15), GOLD_DARK)
    img.putpixel((13, 3), rgb(0xE8F0FF))


def draw_was_sceptre(img, d, rng):
    d.line([(3, 14), (11, 4)], fill=rgb(0x2A2440), width=2)
    d.line([(1, 13), (3, 15)], fill=rgb(0x2A2440), width=2)                  # the forked foot
    d.polygon([(10, 3), (14, 1), (14, 3), (12, 5)], fill=rgb(0x3A3460))      # the head of the Set animal
    img.putpixel((13, 2), GOLD)
    for i in range(3):
        img.putpixel((5 + i * 2, 12 - i * 2), GOLD)


def draw_nemes(img, d, rng):
    d.polygon([(3, 3), (12, 3), (14, 9), (13, 15), (10, 15), (10, 9), (5, 9), (5, 15), (2, 15), (1, 9)], fill=GOLD)
    for y in range(4, 15, 2):
        d.line([(1, y), (14, y)], fill=LAPIS)
    d.rectangle([5, 6, 10, 9], fill=(0, 0, 0, 0))
    d.line([(3, 3), (12, 3)], fill=GOLD_LIGHT)
    img.putpixel((7, 2), CARNELIAN)                                           # the uraeus
    img.putpixel((8, 2), GOLD_LIGHT)


def draw_pectoral(img, d, rng):
    d.chord([1, 0, 14, 13], 0, 180, fill=GOLD)
    d.chord([3, 2, 12, 11], 0, 180, fill=LAPIS)
    d.chord([5, 4, 10, 9], 0, 180, fill=TURQUOISE)
    d.ellipse([5, 8, 10, 13], fill=rgb(0xE0502A), outline=GOLD)               # the sun disc of Ra
    img.putpixel((7, 9), rgb(0xFFB060))
    d.line([(1, 6), (3, 2)], fill=GOLD_DARK)
    d.line([(14, 6), (12, 2)], fill=GOLD_DARK)


ITEMS = {
    "ankh": draw_ankh,
    "dates": draw_dates,
    "honey_cake": draw_honey_cake,
    "mummy_wrappings": draw_wrappings,
    "scarab_shell": draw_scarab_shell,
    "scorpion_stinger": draw_stinger,
    "jackal_pelt": draw_jackal_pelt,
    "sphinx_claw": draw_sphinx_claw,
    "apep_scale": draw_apep_scale,
    "eye_of_horus": draw_eye_of_horus,
    "knot_of_isis": draw_knot_of_isis,
    "sistrum": draw_sistrum,
    "khopesh": draw_khopesh,
    "was_sceptre": draw_was_sceptre,
    "nemes": draw_nemes,
    "pectoral_of_ra": draw_pectoral,
}


# ====================================================================== entities

def wrapped(img, parts, rng, base=LINEN):
    """Linen bandages wound round and round: a darker strip every other row, loose ends and stains."""
    for part in ("head", "body", "arm", "leg"):
        for rect in side_faces(parts[part]):
            x, y, w, h = rect
            for j in range(h):
                for i in range(w):
                    if (j + (i // 3)) % 3 == 0:
                        img.putpixel((x + i, y + j), jitter(scale(base, 0.78), rng, 5))
            speckle(img, rect, rgb(0x6A5A3A), rng, 3)


def mummy(rng):
    """A dead man in yellowed linen wrappings, two dark hollows for eyes with a dull green glint."""
    img, parts = humanoid(rng, 0xD8CCA8, 0xD8CCA8, 0xC8BC98, hair=0xC8BC98, sleeves=0)
    wrapped(img, parts, rng, rgb(0xD8CCA8))
    face(img, parts["head"], iris=0x6AE85A, eye_row=3, brow=0x4A3E2A)
    shade_parts(img, parts)
    return img


def pharaoh_mummy(rng):
    """The pharaoh: wrappings of fine white linen, a golden death mask with the striped nemes and a broad collar."""
    img, parts = humanoid(rng, 0xEDE4CC, 0xEDE4CC, 0xDCD2B8, hair=0xE2B33C, sleeves=0)
    wrapped(img, parts, rng, rgb(0xEDE4CC))
    head = parts["head"]
    for name in ("top", "back", "right", "left"):                 # the nemes, gold and lapis stripes
        x, y, w, h = head[name]
        for j in range(h):
            fill_rect(img, x, y + j, w, 1, GOLD if j % 2 == 0 else LAPIS, rng, 6)
    x, y, w, h = head["front"]
    fill_rect(img, x, y, w, h, GOLD, rng, 8)                     # the golden mask
    fill_rect(img, x, y, w, 2, LAPIS, rng, 4)
    for ex in (2, 5):
        img.putpixel((x + ex, y + 4), rgb(0x14141E))
        img.putpixel((x + ex - (1 if ex == 2 else -1), y + 4), rgb(0xF4F0E4))
    img.putpixel((x + 3, y + 7), LAPIS)                          # the plaited beard
    img.putpixel((x + 4, y + 7), LAPIS)
    band(img, parts["body"], 0, 3, GOLD, rng)                    # the broad collar
    band(img, parts["body"], 1, 1, LAPIS, rng)
    band(img, parts["body"], 2, 1, TURQUOISE, rng)
    band(img, parts["arm"], 9, 1, GOLD, rng)
    shade_parts(img, parts)
    return img


def ushabti(rng):
    """A servant figure of blue faience: glazed turquoise body, black painted wig and eyes, hoe and basket in black."""
    img, parts = humanoid(rng, 0x3AA8B8, 0x2A8AB0, 0x2A8AB0, hair=0x14141E, sleeves=0)
    face(img, parts["head"], iris=0x14141E, eye_row=3, brow=0x14141E)
    for rect in side_faces(parts["body"]):
        x, y, w, h = rect
        for j in range(2, h, 3):
            fill_rect(img, x + 1, y + j, w - 2, 1, rgb(0x14141E), rng, 4)    # columns of painted spells
    for part in ("arm", "leg", "body"):
        for rect in side_faces(parts[part]):
            speckle(img, rect, rgb(0x8AE0E8), rng, 4)                     # the shine of the glaze
    shade_parts(img, parts)
    return img


def set_god(rng):
    """Set: red skin, the long dark snout and tall square ears of the Set animal drawn on a dark head, a red kilt,
    golden armbands and eyes of red fire."""
    img = giant(rng, 0x9A3A2A, 0xE8E0C8, 0x8A2A1E, 0x1E1414, 0xFF4A1C, 0xE2B33C)
    head = box_faces(0, 0, 8, 8, 8)
    for name in ("top", "back", "right", "left"):
        fill_rect(img, *head[name], rgb(0x2A1A1A), rng, 6)
    x, y, w, h = head["front"]
    fill_rect(img, x + 2, y + 4, 4, 4, rgb(0x2A1A1A), rng, 4)            # the snout
    hat = box_faces(32, 0, 8, 8, 8)
    for name in ("front", "back"):
        hx, hy, hw, hh = hat[name]
        fill_rect(img, hx, hy, 2, 3, rgb(0x2A1A1A), rng, 4)               # the square-topped ears
        fill_rect(img, hx + hw - 2, hy, 2, 3, rgb(0x2A1A1A), rng, 4)
    return img


def scarab(rng):
    """Spider texture layout (64x32): a black-blue beetle with a green and gold sheen, red eyes."""
    img = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    fill_rect(img, 0, 0, 64, 32, rgb(0x14202A), rng, 6)
    for _ in range(90):
        img.putpixel((rng.randrange(64), rng.randrange(32)), jitter(rgb(rng.choice((0x2A6A5A, 0x3AA88A, 0x1A3A5A))), rng, 8))
    body = box_faces(0, 12, 10, 8, 12)
    x, y, w, h = body["top"]
    for i in range(w):                                          # the parting of the wing cases
        img.putpixel((x + i, y + h // 2), rgb(0x0A1018))
    fill_rect(img, x + 2, y + 1, 2, 2, GOLD, rng, 6)
    head = box_faces(32, 4, 8, 8, 8)
    hx, hy, hw, hh = head["front"]
    img.putpixel((hx + 2, hy + 3), rgb(0xC0262E))
    img.putpixel((hx + 5, hy + 3), rgb(0xC0262E))
    fill_rect(img, hx + 1, hy + 6, hw - 2, 1, rgb(0x2A1A10), rng, 4)    # mandibles
    return img


def bastet_cat(rng):
    """Cat texture layout (64x32): a sleek black temple cat with golden eyes and a gold ring in one ear."""
    img = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    fill_rect(img, 0, 0, 64, 32, rgb(0x16161C), rng, 5)
    for _ in range(50):
        img.putpixel((rng.randrange(64), rng.randrange(32)), rgb(0x2A2A3A))
    head = box_faces(0, 0, 5, 4, 5)
    x, y, w, h = head["front"]
    for ex in (0, 3):
        img.putpixel((x + ex, y + 1), rgb(0xFFD040))
        img.putpixel((x + ex + 1, y + 1), rgb(0x0A0A0A))
    nose = box_faces(0, 24, 3, 2, 2)
    nx, ny, nw, nh = nose["front"]
    img.putpixel((nx + 1, ny), rgb(0x3A2A2A))
    ear = box_faces(6, 10, 1, 1, 2)
    ex_, ey_, _, _ = ear["front"]
    img.putpixel((ex_, ey_), GOLD)
    body = box_faces(20, 0, 4, 16, 6)
    bx, by, bw, bh = body["front"]
    fill_rect(img, bx, by, bw, 1, GOLD, rng, 4)                 # a collar of gold beads
    img.putpixel((bx + 1, by + 1), LAPIS)
    return img


def priestess(spec):
    return lambda rng: amazon(rng, **spec)


PRIESTESSES = [
    dict(skin=0xC8956B, hair=0x14100E, dress=0xF4F0E4, trim=0xE2B33C, eyes=0x3A2A1A, outfit="chiton", style="long",
         band=0xE2B33C, belt=0x2A5AB0),
    dict(skin=0xB07A52, hair=0x1A1414, dress=0xF4F0E4, trim=0x2A5AB0, eyes=0x2A1E14, outfit="peplos", style="braid",
         crown=0xE2B33C, belt=0xE2B33C),
    dict(skin=0xD8A47A, hair=0x2A1A14, dress=0xE8E0C8, trim=0x3AB8A8, eyes=0x4A3A1A, outfit="chiton", style="twin",
         band=0x3AB8A8, belt=0xC0402A),
    dict(skin=0x9A6A44, hair=0x0E0A0A, dress=0xF4F0E4, trim=0xC0402A, eyes=0x2A1A10, outfit="peplos", style="long",
         band=0xE2B33C, belt=0xE2B33C, flower=0x5A8AE0),
    dict(skin=0xC08A60, hair=0x1A1414, dress=0x2A5AB0, trim=0xE2B33C, eyes=0x3A2A14, outfit="chiton", style="ponytail",
         crown=0xE2B33C, belt=0xE2B33C),
    dict(skin=0xD0A07A, hair=0x14100E, dress=0xF4F0E4, trim=0xE2B33C, eyes=0x5A3A1A, outfit="peplos", style="wavy",
         band=0x2A5AB0, belt=0x2A5AB0),
    dict(skin=0xA87650, hair=0x1E1614, dress=0xE8E0C8, trim=0x2A5AB0, eyes=0x2A1E14, outfit="chiton", style="braid",
         band=0xE2B33C, belt=0x3AB8A8, flower=0xE8E0F0),
    dict(skin=0xC89870, hair=0x0E0A0A, dress=0xF4F0E4, trim=0xC0402A, eyes=0x3A2A1A, outfit="peplos", style="twin",
         crown=0xE2B33C, belt=0xC0402A),
]

# ---------------------------------------------------------------- the crocodile

def crocodile(rng):
    """Layout of client/CrocodileModel (64x64): an olive-green crocodile, dark and knobbly on the back with rows of
    raised scutes, banded with black on the tail, the flanks paler and the belly of smooth cream scales in square
    rows; yellow eyes with a slit pupil on raised sockets, a long snout with the teeth showing along the jaw line."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    back, flank, belly = rgb(0x4A5A2A), rgb(0x6A7A3A), rgb(0xD8CC98)
    dark, scute = rgb(0x2A321A), rgb(0x3A4420)
    parts = {}

    def scales_on(rect, base, cell=2, shade=0.82):
        """Square scales: every cell gets a darker rim on its lower and right side."""
        x, y, w, h = rect
        for j in range(h):
            for i in range(w):
                c = img.getpixel((x + i, y + j))
                if i % cell == cell - 1 or j % cell == cell - 1:
                    img.putpixel((x + i, y + j), scale(c, shade))

    def flanks(rects, rows_belly):
        for name in ("right", "left", "front", "back"):
            x, y, w, h = rects[name]
            for j in range(h):
                t = j / max(1, h - 1)
                for i in range(w):
                    c = mix(back, flank, min(1.0, t * 1.6))
                    if j >= h - rows_belly:
                        c = belly
                    img.putpixel((x + i, y + j), jitter(c, rng, 8))
            scales_on((x, y, w, h), None, cell=2)
            for _ in range(w * h // 10):                         # dark mottling
                img.putpixel((x + rng.randrange(w), y + rng.randrange(max(1, h - rows_belly))), jitter(dark, rng, 6))

    def top_scutes(rect, rows=2):
        """Rows of raised bony scutes along the back: light tips with dark gaps between them."""
        x, y, w, h = rect
        fill_rect(img, x, y, w, h, back, rng, 8)
        for j in range(h):
            for i in range(w):
                if j % 2 == 0 and (i % 3) != 1:
                    img.putpixel((x + i, y + j), jitter(scale(scute, 1.25), rng, 6))
                elif j % 2 == 1:
                    img.putpixel((x + i, y + j), jitter(dark, rng, 5))

    # The body and the ridge of scutes on the back.
    parts["body"] = paint_box(img, 0, 0, 8, 4, 16, back, rng, 8, faces={"bottom": belly}, shaded=False)
    top_scutes(parts["body"]["top"])
    flanks(parts["body"], 1)
    fill_rect(img, *parts["body"]["bottom"], belly, rng, 6)
    scales_on(parts["body"]["bottom"], None, cell=2, shade=0.9)
    parts["ridge"] = paint_box(img, 0, 20, 4, 1, 14, scute, rng, 6, shaded=False)
    x, y, w, h = parts["ridge"]["top"]
    for j in range(h):
        for i in range(w):
            img.putpixel((x + i, y + j), jitter(scale(scute, 1.35) if (j % 2 == 0 and i in (0, w - 1)) else dark, rng, 6))
    # The tail: three segments, banded black, the crest of paired scutes on top.
    for name, d in (("tail", (36, 20, 6, 4, 8)), ("tail2", (42, 45, 4, 3, 7)), ("tail3", (0, 55, 2, 2, 7))):
        parts[name] = paint_box(img, *d, back, rng, 8, faces={"bottom": belly}, shaded=False)
        top_scutes(parts[name]["top"])
        flanks(parts[name], 1 if d[3] > 2 else 0)
        for side in ("top", "right", "left"):
            rx, ry, rw, rh = parts[name][side]
            for k in range(2, (rh if side == "top" else rw), 3):
                if side == "top":
                    fill_rect(img, rx, ry + k, rw, 1, dark, rng, 4)
                else:
                    fill_rect(img, rx + k, ry, 1, rh, dark, rng, 4)
    # The head: a flat skull with the eye sockets, a long snout, the lower jaw with its pale throat.
    parts["skull"] = paint_box(img, 0, 35, 6, 4, 5, back, rng, 8, faces={"bottom": belly}, shaded=False)
    top_scutes(parts["skull"]["top"])
    flanks(parts["skull"], 1)
    parts["snout"] = paint_box(img, 22, 35, 4, 2, 8, back, rng, 8, faces={"bottom": belly}, shaded=False)
    sx_, sy_, sw, sh = parts["snout"]["top"]
    for _ in range(14):                                          # the bumpy hide of the snout
        img.putpixel((sx_ + rng.randrange(sw), sy_ + rng.randrange(sh)), jitter(scale(back, 1.2), rng, 8))
    img.putpixel((sx_ + 1, sy_), rgb(0x141410))                  # the nostrils at the tip
    img.putpixel((sx_ + 2, sy_), rgb(0x141410))
    for side in ("right", "left"):                               # the teeth along the jaw line
        rx, ry, rw, rh = parts["snout"][side]
        fill_rect(img, rx, ry, rw, rh - 1, flank, rng, 8)
        for i in range(rw):
            img.putpixel((rx + i, ry + rh - 1), rgb(0xF2ECD8) if i % 2 == 0 else rgb(0x2A1A14))
    fx, fy, fw, fh = parts["snout"]["front"]
    fill_rect(img, fx, fy, fw, fh, flank, rng, 6)
    img.putpixel((fx, fy + fh - 1), rgb(0xF2ECD8))
    img.putpixel((fx + fw - 1, fy + fh - 1), rgb(0xF2ECD8))
    parts["jaw"] = paint_box(img, 0, 45, 5, 1, 9, flank, rng, 8, faces={"bottom": belly, "top": rgb(0xB85A5A)}, shaded=False)
    jx, jy, jw, jh = parts["jaw"]["top"]                         # the pink mouth inside, lined with teeth
    for j in range(jh):
        img.putpixel((jx, jy + j), rgb(0xF2ECD8) if j % 2 else rgb(0xB85A5A))
        img.putpixel((jx + jw - 1, jy + j), rgb(0xF2ECD8) if j % 2 else rgb(0xB85A5A))
    scales_on(parts["jaw"]["bottom"], None, cell=2, shade=0.9)
    parts["eye"] = paint_box(img, 48, 8, 1, 1, 2, back, rng, 6, shaded=False)
    for name in ("front", "right", "left", "top"):
        ex, ey, ew, eh = parts["eye"][name]
        img.putpixel((ex, ey), rgb(0xE8C83A))                    # the yellow eye
    ex, ey, ew, eh = parts["eye"]["right"]
    img.putpixel((ex + ew - 1, ey), rgb(0x141410))              # the slit pupil
    ex, ey, ew, eh = parts["eye"]["left"]
    img.putpixel((ex, ey), rgb(0x141410))
    # The legs: scaly, with dark claws on the webbed feet.
    parts["leg"] = paint_box(img, 48, 0, 3, 4, 3, flank, rng, 8, faces={"bottom": dark}, shaded=False)
    for rect in side_faces(parts["leg"]):
        scales_on(rect, None, cell=2)
        rx, ry, rw, rh = rect
        fill_rect(img, rx, ry + rh - 1, rw, 1, dark, rng, 4)
        img.putpixel((rx, ry + rh - 1), rgb(0xD8D0B8))
        img.putpixel((rx + rw - 1, ry + rh - 1), rgb(0xD8D0B8))
    shade_parts(img, parts)
    return img


# ---------------------------------------------------------------- the gods of Egypt

def god_body(rng, skin, kilt=0xF4F0E4, collar=(GOLD, LAPIS, TURQUOISE), dress=None, arms=None, sandals=0xC8A060):
    """The body of a god as the temple walls show it: bare chest with a broad collar of gold and stone, a pleated
    white kilt with a golden belt, armbands and bracelets of gold, sandals. With dress, a long sheath dress from the
    chest to the ankles instead of the kilt. Returns (img, parts); the head is painted by the god's own function."""
    img, parts = humanoid(rng, skin, skin, skin, arms=arms, sleeves=0, sandals=sandals)
    body, leg = parts["body"], parts["leg"]
    if dress is not None:
        for x, y, w, h in side_faces(body):
            fill_rect(img, x, y + 3, w, h - 3, rgb(dress), rng, 6)
        for x, y, w, h in side_faces(leg):
            fill_rect(img, x, y, w, h - 2, rgb(dress), rng, 6)
            for i in range(0, w, 2):
                img.putpixel((x + i, y + h - 3), scale(rgb(dress), 0.75))
        fill_rect(img, *leg["top"], rgb(dress), rng, 6)
    else:
        for x, y, w, h in side_faces(body):
            fill_rect(img, x, y + 8, w, h - 8, rgb(kilt), rng, 4)
        for x, y, w, h in side_faces(leg):
            fill_rect(img, x, y, w, 5, rgb(kilt), rng, 4)
            for i in range(0, w, 2):                             # the pleats
                for j in range(5):
                    img.putpixel((x + i, y + j), scale(rgb(kilt), 0.86))
        band(img, body, 8, 1, GOLD, rng)                         # the golden belt
        x, y, w, h = body["front"]
        fill_rect(img, x + 3, y + 9, 2, 3, GOLD, rng, 6)         # the apron of the kilt
    for row, colour in enumerate(collar):                        # the broad collar
        band(img, body, row, 1, colour, rng)
    x, y, w, h = body["front"]
    for i in range(1, w - 1):
        img.putpixel((x + i, y + len(collar)), GOLD if i % 2 else CARNELIAN)
    fill_rect(img, *body["top"], collar[0], rng, 6)
    band(img, parts["arm"], 3, 1, GOLD, rng)                     # armbands and bracelets
    band(img, parts["arm"], 10, 1, GOLD, rng)
    return img, parts


def head_fill(img, colour, rng, noise=8, faces=("front", "right", "left", "back", "top", "bottom")):
    head = box_faces(0, 0, 8, 8, 8)
    for name in faces:
        fill_rect(img, *head[name], rgb(colour) if isinstance(colour, int) else colour, rng, noise)
    return head


def hat_px(img, face_name, pixels, colour):
    """Pixels on one face of the overlay that floats around the head (crowns, ears, horns)."""
    x, y, w, h = box_faces(32, 0, 8, 8, 8)[face_name]
    c = rgb(colour) if isinstance(colour, int) else colour
    for i, j in pixels:
        img.putpixel((x + i, y + j), c)


def wig(img, rng, colour=0x14100E, band_colour=None):
    """The heavy black wig of the gods and goddesses, falling behind the ears to the shoulders."""
    head = box_faces(0, 0, 8, 8, 8)
    for name in ("top", "back"):
        fill_rect(img, *head[name], rgb(colour), rng, 8)
    for name in ("right", "left"):
        x, y, w, h = head[name]
        fill_rect(img, x, y, w, h, rgb(colour), rng, 8)
        ear = (x + w - 3, y + 3) if name == "right" else (x + 1, y + 3)
        fill_rect(img, ear[0], ear[1], 2, 2, img.getpixel((8 + 3, 8 + 5)), rng, 0)
    x, y, w, h = head["front"]
    fill_rect(img, x, y, w, 2, rgb(colour), rng, 8)
    for j in range(2, h):
        img.putpixel((x, y + j), rgb(colour))
        img.putpixel((x + w - 1, y + j), rgb(colour))
    if band_colour:
        for name in ("front", "right", "left", "back"):
            bx, by, bw, bh = head[name]
            fill_rect(img, bx, by + 1, bw, 1, rgb(band_colour), rng, 4)
    return head


def bird_head(img, rng, feathers, cheek, beak, eye=0x141414, ring=0xE2B33C, curved=False):
    """The head of a falcon or an ibis: feathers all over, a pale cheek, a dark stripe under the eye, the beak in the
    middle of the face, hooked down for the falcon, long and curved down to the chest for the ibis."""
    head = head_fill(img, feathers, rng, 10)
    for name in ("front", "right", "left", "back", "top"):
        x, y, w, h = head[name]
        for j in range(0, h, 2):
            for i in range((j // 2) % 2, w, 2):
                img.putpixel((x + i, y + j), scale(img.getpixel((x + i, y + j)), 0.85))
    x, y, w, h = head["front"]
    fill_rect(img, x + 1, y + 4, 2, 3, rgb(cheek), rng, 4)
    fill_rect(img, x + 5, y + 4, 2, 3, rgb(cheek), rng, 4)
    for ex in (1, 5):
        img.putpixel((x + ex, y + 3), rgb(ring))
        img.putpixel((x + ex + 1, y + 3), rgb(eye))
        img.putpixel((x + ex + (1 if ex == 1 else 0), y + 4), scale(rgb(feathers), 0.5))   # the malar stripe
        img.putpixel((x + ex + (1 if ex == 1 else 0), y + 5), scale(rgb(feathers), 0.5))
    if curved:
        fill_rect(img, x + 3, y + 3, 2, 5, rgb(beak), rng, 4)
        bx, by, bw, bh = head["bottom"]
        fill_rect(img, bx + 3, by + 3, 2, 5, rgb(beak), rng, 4)
    else:
        fill_rect(img, x + 3, y + 3, 2, 3, rgb(beak), rng, 4)
        img.putpixel((x + 3, y + 6), scale(rgb(beak), 0.4))
        img.putpixel((x + 4, y + 6), scale(rgb(beak), 0.4))
    for name in ("right", "left"):                               # the eye seen from the side
        sx_, sy_, sw, sh = head[name]
        ex = sx_ + (sw - 3 if name == "right" else 2)
        img.putpixel((ex, sy_ + 3), rgb(ring))
        img.putpixel((ex + (1 if name == "right" else -1), sy_ + 3), rgb(eye))
    return head


def beast_head(img, rng, fur, muzzle, eyes, nose=0x1A1414, teeth=False, scales_=False):
    """The head of a jackal, a cat, a lioness or a crocodile: fur (or scales) all over, a muzzle of another colour
    in the lower middle of the face, the eyes above it, the nose at the bottom."""
    head = head_fill(img, fur, rng, 10)
    if scales_:
        for name in ("front", "right", "left", "back", "top"):
            x, y, w, h = head[name]
            for j in range(h):
                for i in range(w):
                    if i % 2 == 1 or j % 2 == 1:
                        img.putpixel((x + i, y + j), scale(img.getpixel((x + i, y + j)), 0.84))
    x, y, w, h = head["front"]
    fill_rect(img, x + 2, y + 4, 4, 4, rgb(muzzle), rng, 6)
    for ex in (1, 5):
        img.putpixel((x + ex, y + 3), rgb(eyes))
        img.putpixel((x + ex + 1, y + 3), rgb(0x0A0A0A) if not scales_ else rgb(eyes))
        img.putpixel((x + ex, y + 2), scale(rgb(fur), 0.6))
        img.putpixel((x + ex + 1, y + 2), scale(rgb(fur), 0.6))
    fill_rect(img, x + 3, y + 5, 2, 1, rgb(nose), rng, 0)
    if teeth:
        for i in range(2, 6):
            img.putpixel((x + i, y + 7), rgb(0xF2ECD8) if i % 2 == 0 else rgb(0x2A1A14))
        for name in ("right", "left"):
            sx_, sy_, sw, sh = head[name]
            for i in range(sw):
                img.putpixel((sx_ + i, sy_ + 6), rgb(0xF2ECD8) if i % 2 == 0 else rgb(0x2A1A14))
    else:
        fill_rect(img, x + 2, y + 7, 4, 1, scale(rgb(muzzle), 0.6), rng, 0)
    return head


def sun_disc(img, colour=0xE0402A, cobra=GOLD):
    """The red sun disc above the head, with the cobra (uraeus) rearing on the brow."""
    hat_px(img, "front", [(i, j) for j in range(0, 3) for i in range(2, 6)], colour)
    hat_px(img, "back", [(i, j) for j in range(0, 3) for i in range(2, 6)], colour)
    hat_px(img, "front", [(3, 3), (4, 3), (3, 4)], cobra)
    hat_px(img, "top", [(i, j) for j in range(3, 5) for i in range(2, 6)], colour)


def ra(rng):
    """Ra, king of the gods: the head of a falcon in gold-brown feathers under the red sun disc and the cobra, ruddy
    skin, a white kilt and a collar of gold, lapis and carnelian."""
    img, parts = god_body(rng, 0xB8643A, collar=(GOLD, LAPIS, CARNELIAN))
    bird_head(img, rng, 0x9A6A2A, 0xF0E0B0, 0xE2B33C)
    sun_disc(img)
    shade_parts(img, parts)
    return img


def horus(rng):
    """Horus the avenger: a falcon in brown and white feathers, the double crown of Egypt, white for the south and red
    for the north, his kilt banded with blue."""
    img, parts = god_body(rng, 0xA86A3A, collar=(GOLD, LAPIS, GOLD))
    bird_head(img, rng, 0x6A4A2A, 0xF4F0E4, 0xE8C060, ring=0x3A8AE0)
    for name in ("front", "back", "right", "left"):               # the white crown in the red crown
        hat_px(img, name, [(i, j) for j in range(0, 3) for i in range(2, 6)], 0xF4F0E4)
        hat_px(img, name, [(i, 3) for i in range(0, 8)], 0xC0262E)
    hat_px(img, "front", [(0, j) for j in range(0, 3)], 0xC0262E)    # the curl of the red crown
    band(img, parts["leg"], 3, 1, LAPIS, rng)
    shade_parts(img, parts)
    return img


def thoth(rng):
    """Thoth the scribe: the white head of an ibis with a black neck and a long curved black beak, the crescent and
    the full moon above, a kilt of white linen and a collar of turquoise."""
    img, parts = god_body(rng, 0xB07A52, collar=(TURQUOISE, GOLD, TURQUOISE))
    bird_head(img, rng, 0xF0ECE4, 0xF0ECE4, 0x1A1A1A, ring=0x1A1A1A, curved=True)
    head = box_faces(0, 0, 8, 8, 8)
    for name in ("back",):
        fill_rect(img, *head[name], rgb(0x1A1A1A), rng, 6)
    hat_px(img, "front", [(i, j) for j in range(0, 3) for i in range(2, 6)], 0xE8ECF4)   # the moon disc
    hat_px(img, "front", [(1, 2), (6, 2), (1, 3), (6, 3), (2, 3), (5, 3)], 0xC8CCD8)    # the crescent under it
    hat_px(img, "back", [(i, j) for j in range(0, 3) for i in range(2, 6)], 0xE8ECF4)
    shade_parts(img, parts)
    return img


def anubis(rng):
    """Anubis, guardian of the dead: the black head of a jackal with a long muzzle, eyes ringed with gold and tall
    pointed ears, dark skin, a kilt striped with gold and a collar of gold."""
    img, parts = god_body(rng, 0x5A3A2A, kilt=0xE8D8A0, collar=(GOLD, rgb(0x1A1A1A), GOLD))
    beast_head(img, rng, 0x161414, 0x1E1C1C, 0xE2B33C, nose=0x0A0A0A)
    for name in ("front", "back"):                                    # the tall ears
        hat_px(img, name, [(0, 0), (1, 0), (0, 1), (1, 1), (6, 0), (7, 0), (6, 1), (7, 1)], 0x161414)
    hat_px(img, "front", [(1, 1), (6, 1)], GOLD)
    for x, y, w, h in side_faces(parts["leg"]):
        for i in range(w):
            img.putpixel((x + i, y + 1), GOLD)
            img.putpixel((x + i, y + 3), GOLD)
    shade_parts(img, parts)
    return img


def bastet(rng):
    """Bastet, lady of the home: the black head of a cat with golden-green eyes and pointed ears, a gold ring in one
    ear, a dress of turquoise linen with a golden collar."""
    img, parts = god_body(rng, 0xB07A52, dress=0x2AA898, collar=(GOLD, LAPIS, GOLD))
    beast_head(img, rng, 0x1A1A20, 0x22222A, 0xB8E04A, nose=0xC87A8A)
    for name in ("front", "back"):
        hat_px(img, name, [(0, 0), (1, 1), (0, 1), (7, 0), (6, 1), (7, 1)], 0x1A1A20)
    hat_px(img, "front", [(7, 2)], GOLD)                               # the earring
    shade_parts(img, parts)
    return img


def sekhmet(rng):
    """Sekhmet, the lioness of slaughter: a tawny lioness head with amber eyes and a dark muzzle, the red sun disc and
    the cobra above, a red dress and a collar of gold and carnelian."""
    img, parts = god_body(rng, 0xB07A52, dress=0xA8202A, collar=(GOLD, CARNELIAN, GOLD))
    beast_head(img, rng, 0xC8903A, 0xE0B870, 0xF0A020, nose=0x5A2A1A, teeth=True)
    head = box_faces(0, 0, 8, 8, 8)
    for name in ("right", "left", "back"):                             # the ruff of fur round the face
        x, y, w, h = head[name]
        for j in range(h):
            for i in range(w):
                if (i + j) % 3 == 0:
                    img.putpixel((x + i, y + j), rgb(0xA8702A))
    for name in ("front", "back"):
        hat_px(img, name, [(0, 3), (1, 3), (6, 3), (7, 3)], 0xC8903A)  # the round ears
    sun_disc(img)
    shade_parts(img, parts)
    return img


def sobek(rng):
    """Sobek, lord of the Nile: the green scaly head of a crocodile with yellow eyes and the teeth showing, the sun
    disc with two tall plumes above, olive skin, a kilt striped with green and gold."""
    img, parts = god_body(rng, 0x8A6A3A, kilt=0xF4F0E4, collar=(GOLD, rgb(0x3A8A4A), GOLD))
    beast_head(img, rng, 0x4A6A2A, 0x5A7A3A, 0xE8C83A, nose=0x1A2A10, teeth=True, scales_=True)
    sun_disc(img)
    for name in ("front", "back"):                                    # the plumes
        hat_px(img, name, [(1, 0), (1, 1), (1, 2), (6, 0), (6, 1), (6, 2)], 0x3AA0D0)
    band(img, parts["leg"], 2, 1, rgb(0x3A8A4A), rng)
    shade_parts(img, parts)
    return img


def isis(rng):
    """Isis, great of magic: a woman with a black wig and a golden band, the throne sign on her head, a white sheath
    dress, and the feathered wings of the goddess drawn down her arms in red, blue and green."""
    img, parts = god_body(rng, 0xC8956B, dress=0xF4F0E4, collar=(GOLD, LAPIS, TURQUOISE))
    head = wig(img, rng, band_colour=0xE2B33C)
    face(img, head, iris=0x2A1E14, eye_row=4, brow=0x14100E)
    x, y, w, h = head["front"]
    for ex in (1, 6):
        img.putpixel((x + ex, y + 4), rgb(0x14100E))                    # the kohl lines
    for name in ("front", "back", "right", "left"):                   # the throne sign
        hat_px(img, name, [(2, 0), (2, 1), (2, 2), (3, 2), (4, 2), (5, 2), (5, 1)], 0x2A5AB0)
    for x, y, w, h in side_faces(parts["arm"]):                       # the wings of the goddess on her arms
        for j in range(2, h - 1):
            colour = (CARNELIAN, LAPIS, TURQUOISE, GOLD)[(j // 2) % 4]
            for i in range(w):
                if (i + j) % 4 != 0:
                    img.putpixel((x + i, y + j), jitter(colour, rng, 6))
    shade_parts(img, parts)
    return img


def hathor(rng):
    """Hathor, lady of joy: a woman with a black wig, the cow horns and the red sun disc between them, a red sheath
    dress and the menat necklace of the goddess."""
    img, parts = god_body(rng, 0xC8956B, dress=0xC0302A, collar=(GOLD, TURQUOISE, GOLD))
    head = wig(img, rng, band_colour=0x3AB8A8)
    face(img, head, iris=0x2A1E14, eye_row=4, brow=0x14100E)
    for name in ("front", "back"):
        hat_px(img, name, [(0, 0), (0, 1), (0, 2), (1, 3), (7, 0), (7, 1), (7, 2), (6, 3)], 0xF0E4C0)   # the horns
        hat_px(img, name, [(i, j) for j in range(0, 3) for i in range(2, 6)], 0xE0402A)                  # the disc
    hat_px(img, "front", [(3, 3), (4, 3)], GOLD)
    shade_parts(img, parts)
    return img


def osiris(rng):
    """Osiris, king of the dead: green skin, the colour of new life, the tall white atef crown with two plumes, the
    plaited beard of the gods, and the white wrappings of a mummy from the chest down."""
    img, parts = god_body(rng, 0x3A8A4A, dress=0xF4F0E4, collar=(GOLD, LAPIS, GOLD))
    for x, y, w, h in side_faces(parts["body"]) + side_faces(parts["leg"]):     # the fine linen wound round and round
        for j in range(h):
            for i in range(w):
                c = img.getpixel((x + i, y + j))
                if (j + i // 3) % 3 == 0 and c[0] > 200:
                    img.putpixel((x + i, y + j), scale(c, 0.86))
    head = head_fill(img, 0x3A8A4A, rng, 6)
    face(img, head, iris=0x14100E, eye_row=4, brow=0x14100E)
    x, y, w, h = head["front"]
    fill_rect(img, x + 3, y + 6, 2, 2, rgb(0x2A1A10), rng, 0)          # the plaited beard
    for name in ("front", "back", "right", "left", "top"):            # the white atef crown
        hx, hy, hw, hh = box_faces(32, 0, 8, 8, 8)[name]
        fill_rect(img, hx + 2, hy, hw - 4, hh // 2 if name != "top" else hh, rgb(0xF4F0E4), rng, 4)
    hat_px(img, "front", [(1, 0), (1, 1), (1, 2), (6, 0), (6, 1), (6, 2)], 0xE8D8A0)   # the plumes
    hat_px(img, "front", [(3, 3), (4, 3)], GOLD)
    shade_parts(img, parts)
    return img


def ptah(rng):
    """Ptah the craftsman: green skin, a close blue skullcap, a straight beard, the tight feathered robe wrapping him
    like a mummy, and the collar with the menat of gold."""
    img, parts = god_body(rng, 0x4A9A6A, kilt=0xE8E0C8, collar=(GOLD, LAPIS, GOLD), dress=0x6A8AB8)
    for x, y, w, h in side_faces(parts["body"]) + side_faces(parts["leg"]):
        for j in range(0, h, 2):                                     # the feathered pattern of the robe
            for i in range((j // 2) % 2, w, 2):
                img.putpixel((x + i, y + j), scale(img.getpixel((x + i, y + j)), 0.82))
    head = head_fill(img, 0x4A9A6A, rng, 6)
    for name in ("top", "back", "right", "left"):                    # the skullcap
        hx, hy, hw, hh = head[name]
        fill_rect(img, hx, hy, hw, hh if name == "top" else 3, LAPIS, rng, 6)
    x, y, w, h = head["front"]
    fill_rect(img, x, y, w, 2, LAPIS, rng, 6)
    face(img, head, iris=0x14100E, eye_row=3, brow=0x14100E)
    fill_rect(img, x + 3, y + 6, 2, 2, rgb(0x2A2A3A), rng, 0)          # the straight beard
    shade_parts(img, parts)
    return img


ENTITIES = {
    "crocodile": crocodile,
    "ra": ra,
    "osiris": osiris,
    "isis": isis,
    "horus": horus,
    "anubis": anubis,
    "thoth": thoth,
    "bastet": bastet,
    "sobek": sobek,
    "hathor": hathor,
    "ptah": ptah,
    "sekhmet": sekhmet,
    **{f"priestess_{i}": priestess(spec) for i, spec in enumerate(PRIESTESSES)},
    "mummy": mummy,
    "pharaoh_mummy": pharaoh_mummy,
    "ushabti": ushabti,
    "set": set_god,
    "scarab": scarab,
    "bastet_cat": bastet_cat,
    "jackal": lambda rng: beast(rng, 0x1E1A1A, 0x2E2828, 0xE2B33C, back=0x141010, belly=0x3A302A, claws=0xC8B890),
    "scorpion": lambda rng: crayfish(rng, shell=0xC89A5A, dark=0x5A3A1A, under=0xE8C890, claw=0xA87A3A, eyes=0x141414),
    # The Sphinx: a lion of sandstone with the striped nemes for a mane.
    "sphinx": lambda rng: beast(rng, 0xD8B878, 0xE8CC90, 0x2A5AB0, mane=0x2A5AB0, back=0xC8A060, belly=0xE8D4A0,
                                claws=0xA88A50),
    "apep": lambda rng: hydra(rng, scales=0x2A1A3A, neck=0x4A2A5A, belly=0xC8A060, spines=0xC0262E, eyes=0xFF4A1C),
    # 0 the trader of the market in white linen, 1 the priest of Anubis with a leopard skin, 2 the smith in a leather apron.
    "egyptian_merchant_0": lambda rng: norse_merchant(rng, 0xF0EAD8, 0x2A5AB0, skin=0xC8956B, hair=0x14100E),
    "egyptian_merchant_1": lambda rng: norse_merchant(rng, 0xE8E0C8, 0xD8A040, skin=0xB07A52, hair=0x14100E, beard=False,
                                                      hood=0x1E1A1A),
    "egyptian_merchant_2": lambda rng: norse_merchant(rng, 0x8A6A44, 0x3A2A1C, skin=0xA87650, hair=0x1A1414, apron=0x5A3A24),
}


# ====================================================================== armour layers (64x32 layer_1)

def _layer():
    return Image.new("RGBA", (64, 32), (0, 0, 0, 0))


def nemes_layer(rng):
    """The nemes: a headcloth striped gold and blue over the head and down behind the ears, the uraeus on the brow."""
    img = _layer()
    head = box_faces(0, 0, 8, 8, 8)
    for name in ("top", "back", "right", "left"):
        x, y, w, h = head[name]
        for j in range(h):
            fill_rect(img, x, y + j, w, 1, GOLD if j % 2 == 0 else LAPIS, rng, 5)
    x, y, w, h = head["front"]
    for j in range(2):
        fill_rect(img, x, y + j, w, 1, GOLD if j % 2 == 0 else LAPIS, rng, 5)
    for j in range(2, h):
        img.putpixel((x, y + j), GOLD if j % 2 == 0 else LAPIS)
        img.putpixel((x + w - 1, y + j), GOLD if j % 2 == 0 else LAPIS)
    img.putpixel((x + 3, y), CARNELIAN)
    img.putpixel((x + 4, y), GOLD_LIGHT)
    return img


def pectoral_layer(rng):
    """The pectoral of Ra: a broad collar of gold, lapis and turquoise over the chest and shoulders, the sun disc in
    the middle."""
    img = _layer()
    body = box_faces(16, 16, 8, 12, 4)
    for name in ("front", "back", "right", "left"):
        x, y, w, h = body[name]
        fill_rect(img, x, y, w, 1, GOLD, rng, 4)
        fill_rect(img, x, y + 1, w, 1, LAPIS, rng, 4)
        fill_rect(img, x, y + 2, w, 1, TURQUOISE, rng, 4)
        fill_rect(img, x, y + 3, w, 1, GOLD, rng, 4)
    x, y, w, h = body["front"]
    fill_rect(img, x + 2, y + 4, 4, 2, rgb(0xE0502A), rng, 6)
    img.putpixel((x + 3, y + 4), rgb(0xFFB060))
    fill_rect(img, x + 1, y + 6, w - 2, 1, GOLD, rng, 4)
    for arm in (box_faces(40, 16, 4, 12, 4),):
        for name in ("front", "back", "right", "left", "top"):
            ax, ay, aw, ah = arm[name]
            fill_rect(img, ax, ay, aw, 2 if name != "top" else ah, GOLD, rng, 4)
    return img


LAYERS = {"nemes": nemes_layer, "pectoral_of_ra": pectoral_layer}
