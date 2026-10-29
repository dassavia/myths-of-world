"""Placeholder textures for the Greek content, drawn with Pillow. Replace any PNG with a real one at any time."""
import math
import random

from PIL import Image, ImageDraw


def rgb(hex_color, alpha=255):
    return ((hex_color >> 16) & 255, (hex_color >> 8) & 255, hex_color & 255, alpha)


def jitter(color, rng, amount=12):
    r, g, b, a = color
    d = rng.randint(-amount, amount)
    return (max(0, min(255, r + d)), max(0, min(255, g + d)), max(0, min(255, b + d)), a)


def fill_rect(img, x, y, w, h, color, rng, noise=12):
    for i in range(x, x + w):
        for j in range(y, y + h):
            if 0 <= i < img.width and 0 <= j < img.height:
                img.putpixel((i, j), jitter(color, rng, noise) if noise else color)


def box_faces(u, v, w, h, d):
    """Texture rectangles of a model cube, as vanilla lays them out: name -> (x, y, width, height)."""
    return {
        "top": (u + d, v, w, d),
        "bottom": (u + d + w, v, w, d),
        "right": (u, v + d, d, h),
        "front": (u + d, v + d, w, h),
        "left": (u + d + w, v + d, d, h),
        "back": (u + 2 * d + w, v + d, w, h),
    }


# Light falling from above: top faces brightest, bottoms darkest, sides darken towards their lower edge.
FACE_LIGHT = {"top": 1.12, "front": 1.0, "right": 0.9, "left": 0.9, "back": 0.84, "bottom": 0.7}


def scale(color, factor):
    r, g, b, a = color
    return (max(0, min(255, int(r * factor))), max(0, min(255, int(g * factor))), max(0, min(255, int(b * factor))), a)


def mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))


def shade_rect(img, x, y, w, h, light, gradient=0.14, outline=0.82):
    """Darkens an already painted face: overall light level, a top-to-bottom gradient and a darker rim."""
    for j in range(h):
        for i in range(w):
            px, py = x + i, y + j
            if not (0 <= px < img.width and 0 <= py < img.height):
                continue
            c = img.getpixel((px, py))
            if c[3] == 0:
                continue
            f = light * (1.0 + gradient / 2 - gradient * (j / max(1, h - 1)))
            if w > 2 and h > 2 and (i in (0, w - 1) or j in (0, h - 1)):
                f *= outline
            img.putpixel((px, py), scale(c, f))


def paint_box(img, u, v, w, h, d, color, rng, noise=12, faces=None, shaded=True):
    """Paints a model cube's six faces. Returns the face rectangles so details can be drawn on top.
    Call shade_box() after the details if shaded=False, so that the details get the same lighting."""
    rects = box_faces(u, v, w, h, d)
    for name, (x, y, fw, fh) in rects.items():
        c = (faces or {}).get(name, color)
        fill_rect(img, x, y, fw, fh, c, rng, noise)
    if shaded:
        shade_box(img, rects)
    return rects


def shade_box(img, rects):
    for name, (x, y, fw, fh) in rects.items():
        shade_rect(img, x, y, fw, fh, FACE_LIGHT[name], gradient=0.0 if name in ("top", "bottom") else 0.14)


def speckle(img, rect, color, rng, count, noise=10):
    x, y, w, h = rect
    for _ in range(count):
        img.putpixel((x + rng.randrange(w), y + rng.randrange(h)), jitter(color, rng, noise))


def save(img, path):
    img.save(path)


# ---------------------------------------------------------------- blocks

def marble(rng, base=0xECE8E1, vein=0xB9B4AC):
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(base), rng, 5)
    for _ in range(2):
        x, y = rng.randrange(16), 0
        while y < 16:
            img.putpixel((x % 16, y), jitter(rgb(vein), rng, 8))
            x += rng.choice((-1, 0, 1))
            y += 1
    return img


def marble_bricks(rng):
    img = marble(rng)
    mortar = rgb(0xA8A39A)
    for y in (0, 8):
        for x in range(16):
            img.putpixel((x, y), mortar)
    for x, y0 in ((0, 1), (8, 9)):
        for y in range(y0, y0 + 7):
            img.putpixel((x, y), mortar)
    return img


def marble_pillar_side(rng):
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(0xEEEAE3), rng, 4)
    for x in (1, 4, 7, 10, 13):
        for y in range(16):
            img.putpixel((x, y), jitter(rgb(0xC4BFB6), rng, 4))
    return img


def marble_pillar_top(rng):
    img = Image.new("RGBA", (16, 16))
    for x in range(16):
        for y in range(16):
            r = math.hypot(x - 7.5, y - 7.5)
            c = 0xC4BFB6 if int(r) in (3, 6) else 0xEEEAE3
            img.putpixel((x, y), jitter(rgb(c), rng, 4))
    return img


def olympian_marble(rng):
    img = marble(rng)
    gold = rgb(0xE2B33C)
    for i in range(16):
        for t in (0, 15):
            img.putpixel((i, t), jitter(gold, rng, 10))
            img.putpixel((t, i), jitter(gold, rng, 10))
    for x in range(16):
        for y in range(16):
            if abs(x - 7.5) + abs(y - 7.5) in (3.0, 4.0):
                img.putpixel((x, y), jitter(gold, rng, 10))
    return img


def asphodel(rng):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    stem = rgb(0x6E8B4E)
    for y in range(6, 16):
        img.putpixel((8, y), stem)
    for y, x in ((12, 7), (13, 6), (11, 9), (12, 10)):
        img.putpixel((x, y), stem)
    for cx, cy in ((8, 3), (5, 6), (11, 6), (7, 8), (10, 9)):
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = cx + dx, cy + dy
            if 0 <= x < 16 and 0 <= y < 16:
                img.putpixel((x, y), rgb(0xF4F1EA) if (dx, dy) != (0, 0) else rgb(0xC98F4A))
    return img


def hellas_portal(rng):
    frames = 16
    img = Image.new("RGBA", (16, 16 * frames))
    for f in range(frames):
        for x in range(16):
            for y in range(16):
                swirl = math.sin((x * 0.6) + f * 0.4) + math.cos((y * 0.5) - f * 0.4) + math.sin((x + y) * 0.3 + f * 0.8)
                t = (swirl + 3) / 6
                r = int(230 + 25 * t)
                g = int(170 + 70 * t)
                b = int(40 + 120 * t * t)
                img.putpixel((x, y + 16 * f), (min(r, 255), min(g, 255), min(b, 255), 190))
    return img


# ---------------------------------------------------------------- items

def item(draw_fn, rng):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw_fn(img, ImageDraw.Draw(img), rng)
    return outline(img)


def outline(img, color=(40, 28, 20, 255)):
    """Dark one-pixel outline around the sprite and light from the top left, like vanilla items."""
    out = img.copy()
    for x in range(16):
        for y in range(16):
            c = img.getpixel((x, y))
            if c[3] == 0:
                if any(0 <= x + dx < 16 and 0 <= y + dy < 16 and img.getpixel((x + dx, y + dy))[3] > 0
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    out.putpixel((x, y), color)
                continue
            lit_edge = x > 0 and y > 0 and img.getpixel((x - 1, y - 1))[3] == 0
            dark_edge = x < 15 and y < 15 and img.getpixel((x + 1, y + 1))[3] == 0
            if lit_edge:
                out.putpixel((x, y), mix(c, (255, 255, 255, c[3]), 0.3))
            elif dark_edge:
                out.putpixel((x, y), scale(c, 0.72))
    return out


def draw_torch(img, d, rng):
    d.line([(5, 14), (10, 5)], fill=rgb(0x7A5230), width=2)
    d.rectangle([9, 4, 11, 6], fill=rgb(0xE2B33C))
    for x, y, c in ((10, 3, 0xFFD34E), (11, 2, 0xFF9A2E), (9, 2, 0xFFB43C), (10, 1, 0xFFF1A8), (12, 3, 0xFF7A1C)):
        img.putpixel((x, y), rgb(c))


def draw_ambrosia(img, d, rng):
    d.ellipse([3, 5, 12, 13], fill=rgb(0xF2D27A), outline=rgb(0xB98A2E))
    d.ellipse([5, 3, 10, 7], fill=rgb(0xFFF3C4))
    for x, y in ((6, 8), (9, 9), (7, 11)):
        img.putpixel((x, y), rgb(0xFFFFFF))


def draw_feather(img, d, rng):
    d.line([(3, 13), (12, 2)], fill=rgb(0x3E2B1E), width=1)
    for i in range(8):
        x, y = 4 + i, 12 - i
        d.line([(x, y), (x - 2, y - 2)], fill=rgb(0x8B6A45))
        d.line([(x, y), (x + 2, y + 1)], fill=rgb(0xB08E5E))


def draw_horn(img, d, rng):
    d.line([(3, 13), (6, 9), (9, 6), (12, 2)], fill=rgb(0xE8DCC0), width=3)
    d.line([(3, 13), (5, 11)], fill=rgb(0x5B4636), width=3)
    img.putpixel((12, 2), rgb(0x8A7A60))


def draw_scale(img, d, rng):
    d.polygon([(8, 2), (13, 7), (8, 14), (3, 7)], fill=rgb(0x3C7D46), outline=rgb(0x1F4A28))
    d.line([(8, 3), (8, 13)], fill=rgb(0x8BC34A))


def draw_fang(img, d, rng):
    d.polygon([(5, 2), (11, 2), (8, 14)], fill=rgb(0xF0EAD8), outline=rgb(0x9C8E74))
    d.line([(6, 3), (10, 3)], fill=rgb(0xC0392B))


def draw_pelt(img, d, rng):
    d.rectangle([2, 4, 13, 12], fill=rgb(0xC9962E))
    for x, y in ((2, 3), (13, 3), (2, 13), (13, 13)):
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=rgb(0xC9962E))
    d.rectangle([5, 1, 10, 4], fill=rgb(0x8A5A1C))
    for _ in range(10):
        img.putpixel((rng.randrange(3, 13), rng.randrange(5, 12)), rgb(0xE0B04A))


def draw_eye(img, d, rng):
    d.ellipse([2, 2, 13, 13], fill=rgb(0xF4F1EA), outline=rgb(0xB0453A))
    d.ellipse([5, 5, 10, 10], fill=rgb(0x6B4423))
    d.ellipse([7, 7, 8, 8], fill=rgb(0x111111))


def draw_medusa_head(img, d, rng):
    d.ellipse([4, 5, 11, 13], fill=rgb(0x9DB884))
    for i in range(7):
        a = math.pi * (0.1 + i * 0.13)
        x0, y0 = 8 + 3 * math.cos(a), 7 - 3 * math.sin(a)
        x1, y1 = 8 + 7 * math.cos(a), 6 - 6 * math.sin(a)
        d.line([(x0, y0), (x1, y1)], fill=rgb(0x3F6B2E), width=1)
        img.putpixel((max(0, min(15, int(x1))), max(0, min(15, int(y1)))), rgb(0xB3D16A))
    img.putpixel((6, 9), rgb(0xE8D44D))
    img.putpixel((9, 9), rgb(0xE8D44D))
    d.line([(6, 11), (9, 11)], fill=rgb(0x4E3B2A))


def draw_claw(img, d, rng):
    d.line([(4, 13), (6, 9), (9, 5), (12, 3)], fill=rgb(0x3A2A1C), width=3)
    d.line([(5, 12), (7, 8), (10, 5), (13, 3)], fill=rgb(0xE8DCC0), width=1)
    d.line([(3, 14), (5, 12)], fill=rgb(0xC9962E), width=3)


def draw_dagger(img, d, rng):
    # Curved golden-white claw blade, bronze guard, leather grip.
    d.line([(7, 9), (9, 6), (11, 4), (13, 2)], fill=rgb(0xE8DCC0), width=2)
    d.line([(8, 8), (13, 2)], fill=rgb(0xFFF6DC), width=1)
    d.line([(5, 9), (8, 12)], fill=rgb(0xC98A2E), width=2)
    d.line([(3, 14), (6, 11)], fill=rgb(0x6B4A2B), width=2)
    img.putpixel((2, 15), rgb(0xC9962E))


def draw_harpe(img, d, rng):
    # The sickle-sword: straight blade with a hooked second edge.
    d.line([(4, 12), (11, 5)], fill=rgb(0xC9D1D9), width=2)
    d.line([(11, 5), (12, 2), (10, 1)], fill=rgb(0xC9D1D9), width=2)
    d.line([(9, 7), (11, 8)], fill=rgb(0xA8B2BC), width=1)
    d.line([(5, 11), (11, 5)], fill=rgb(0xF4F7FA), width=1)
    d.line([(2, 14), (4, 12)], fill=rgb(0x5B3A22), width=2)
    d.line([(3, 11), (5, 13)], fill=rgb(0xE2B33C), width=1)


def draw_hydra_egg(img, d, rng):
    d.ellipse([3, 2, 12, 14], fill=rgb(0x4F9A4A))
    for _ in range(14):
        x, y = rng.randrange(4, 12), rng.randrange(3, 14)
        if img.getpixel((x, y))[3]:
            img.putpixel((x, y), rgb(0x2F5D3A))
    for x, y in ((6, 5), (7, 4), (5, 7)):
        img.putpixel((x, y), rgb(0xD7E88A))
    d.line([(8, 8), (9, 10), (8, 12)], fill=rgb(0x1F3A22))


ITEMS = {
    "nemean_claw": draw_claw,
    "nemean_claw_dagger": draw_dagger,
    "harpe": draw_harpe,
    "hydra_egg": draw_hydra_egg,
    "promethean_torch": draw_torch,
    "ambrosia": draw_ambrosia,
    "harpy_feather": draw_feather,
    "minotaur_horn": draw_horn,
    "hydra_scale": draw_scale,
    "cerberus_fang": draw_fang,
    "nemean_pelt": draw_pelt,
    "cyclops_eye": draw_eye,
    "medusa_head": draw_medusa_head,
}


# ---------------------------------------------------------------- entities
#
# Every entity texture is painted flat first (paint_box with shaded=False), then the details go on top, and
# finally shade_parts() lights all faces the same way, so details and base get identical shading.

HUMANOID_PARTS = {"head": (0, 0, 8, 8, 8), "hat": (32, 0, 8, 8, 8), "body": (16, 16, 8, 12, 4),
                  "arm": (40, 16, 4, 12, 4), "leg": (0, 16, 4, 12, 4)}


def shade_parts(img, parts):
    for rects in parts.values():
        shade_box(img, rects)


def side_faces(rects):
    return [rects[n] for n in ("front", "right", "left", "back")]


def band(img, rects, row, rows, color, rng, noise=8):
    """Horizontal band around a box (belts, cuffs, hooves), `row` counted from the top of the side faces."""
    for x, y, w, h in side_faces(rects):
        fill_rect(img, x, y + row, w, rows, color, rng, noise)


def face(img, head, eyes=(1, 5), iris=0x222222, eye_row=3, single_eye=False, mouth=None, brow=None):
    x, y, w, h = head["front"]
    if single_eye:
        fill_rect(img, x + 2, y + eye_row - 1, 4, 3, rgb(0xF4F1EA), None, 0)
        fill_rect(img, x + 3, y + eye_row, 2, 2, rgb(iris), None, 0)
        img.putpixel((x + 4, y + eye_row), rgb(0x111111))
        if brow:
            fill_rect(img, x + 1, y + eye_row - 2, 6, 1, rgb(brow), None, 0)
    else:
        for ex in eyes:
            img.putpixel((x + ex, y + eye_row), rgb(0xF4F1EA))
            img.putpixel((x + ex + 1, y + eye_row), rgb(iris))
            if brow:
                img.putpixel((x + ex, y + eye_row - 1), rgb(brow))
                img.putpixel((x + ex + 1, y + eye_row - 1), rgb(brow))
    for nx in (3, 4):
        px, py = x + nx, y + eye_row + 1
        img.putpixel((px, py), scale(img.getpixel((px, py)), 0.82))
    if mouth:
        for mx in range(2, 6):
            img.putpixel((x + mx, y + min(h - 1, eye_row + 3)), rgb(mouth))


def humanoid(rng, skin, tunic, legs, arms=None, hair=None, alpha=255, sleeves=4, sandals=None):
    """64x64 humanoid: skin head, tunic body, sleeves over skin arms, legs with sandals. Returns (img, parts)."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    skin_c, tunic_c, legs_c = rgb(skin, alpha), rgb(tunic, alpha), rgb(legs, alpha)
    parts = {}
    hair_c = rgb(hair, alpha) if hair else skin_c
    parts["head"] = paint_box(img, 0, 0, 8, 8, 8, skin_c, rng, 6, faces={"top": hair_c, "back": hair_c}, shaded=False)
    if hair:
        for name in ("right", "left"):
            x, y, w, h = parts["head"][name]
            fill_rect(img, x, y, w, 4, hair_c, rng, 10)
            fill_rect(img, x + (w - 2 if name == "right" else 0), y + 4, 2, 2, hair_c, rng, 10)
        x, y, w, h = parts["head"]["back"]
        fill_rect(img, x, y, w, h, hair_c, rng, 10)
        x, y, w, h = parts["head"]["front"]
        fill_rect(img, x, y, w, 2, hair_c, rng, 10)
        img.putpixel((x, y + 2), hair_c)
        img.putpixel((x + 7, y + 2), hair_c)
    parts["body"] = paint_box(img, 16, 16, 8, 12, 4, tunic_c, rng, 8, shaded=False)
    # Folds of the cloth.
    x, y, w, h = parts["body"]["front"]
    for fx in (2, 5):
        for j in range(4, h):
            img.putpixel((x + fx, y + j), scale(img.getpixel((x + fx, y + j)), 0.86))
    arm_c = rgb(arms, alpha) if arms else skin_c
    parts["arm"] = paint_box(img, 40, 16, 4, 12, 4, arm_c, rng, 6, shaded=False)
    if not arms and sleeves:
        band(img, parts["arm"], 0, sleeves, tunic_c, rng)
        fill_rect(img, *parts["arm"]["top"], tunic_c, rng, 8)
    parts["leg"] = paint_box(img, 0, 16, 4, 12, 4, legs_c, rng, 8, shaded=False)
    if sandals:
        band(img, parts["leg"], 10, 2, rgb(sandals, alpha), rng, 4)
        fill_rect(img, *parts["leg"]["bottom"], rgb(sandals, alpha), rng, 4)
    return img, parts


def satyr(rng):
    img, parts = humanoid(rng, 0xC8956B, 0xC8956B, 0x6B4A2B, hair=0x3E2B1E)
    face(img, parts["head"], iris=0x6B3E1A, eye_row=4, mouth=0x8A4B3A, brow=0x2A1C12)
    # Goat legs: shaggy fur with darker tufts, black hooves.
    for rect in side_faces(parts["leg"]):
        speckle(img, rect, rgb(0x4A321E), rng, 14)
    band(img, parts["leg"], 10, 2, rgb(0x1E140E), rng, 4)
    fill_rect(img, *parts["leg"]["bottom"], rgb(0x1E140E), rng, 4)
    # Fur on the belly, a wine-red sash and a beard.
    x, y, w, h = parts["body"]["front"]
    fill_rect(img, x, y + 8, w, 4, rgb(0x6B4A2B), rng, 10)
    for i in range(w):
        img.putpixel((x + i, y + 7 - (i // 3)), rgb(0x7A1E2E))
    hx, hy, hw, hh = parts["head"]["front"]
    fill_rect(img, hx + 2, hy + 7, 4, 1, rgb(0x3E2B1E), rng, 6)
    # Curled ram horns on the hat layer, and pointy ears.
    hat = box_faces(32, 0, 8, 8, 8)
    for name in ("right", "left"):
        x, y, w, h = hat[name]
        for dx, dy in ((2, 0), (3, 0), (4, 1), (4, 2), (3, 3), (2, 2)):
            img.putpixel((x + dx, y + dy), jitter(rgb(0xD8CBB0), rng, 10))
    x, y, w, h = hat["top"]
    for dx, dy in ((1, 2), (1, 3), (6, 2), (6, 3)):
        img.putpixel((x + dx, y + dy), rgb(0xBFAE8E))
    shade_parts(img, parts)
    return img


def harpy(rng):
    img, parts = humanoid(rng, 0xE2C3A4, 0x5B4636, 0xD89A3A, arms=0x6E5640, hair=0x2B1E16)
    face(img, parts["head"], iris=0xC0392B, eye_row=4, mouth=0x5A2A1E, brow=0x1A100A)
    # Feathered body and arms, bird legs with talons.
    for rect in side_faces(parts["body"]) + side_faces(parts["arm"]):
        x, y, w, h = rect
        for j in range(1, h, 3):
            for i in range((j // 3) % 2, w, 2):
                img.putpixel((x + i, y + j), rgb(0x8B6A45))
    for rect in side_faces(parts["leg"]):
        x, y, w, h = rect
        fill_rect(img, x, y, w, 5, rgb(0x6E5640), rng, 12)
        for i in range(0, w, 2):
            img.putpixel((x + i, y + h - 1), rgb(0x1A1410))
    parts["wing_r"] = paint_box(img, 0, 32, 1, 12, 8, rgb(0x6E5640), rng, 14, shaded=False)
    parts["wing_l"] = paint_box(img, 24, 32, 1, 12, 8, rgb(0x6E5640), rng, 14, shaded=False)
    for wing in (parts["wing_r"], parts["wing_l"]):
        for name in ("right", "left"):
            x, y, w, h = wing[name]
            for j in range(0, h, 2):
                for i in range(w):
                    if (i + j) % 4 == 0:
                        img.putpixel((x + i, y + j), rgb(0x8B6A45))
            fill_rect(img, x, y + h - 3, w, 3, rgb(0xC9A66B), rng, 8)
            for i in range(0, w, 2):
                img.putpixel((x + i, y + h - 1), (0, 0, 0, 0))
    shade_parts(img, parts)
    return img


def shade(rng):
    img, parts = humanoid(rng, 0xBFD6E3, 0x8EA3B5, 0x6F8394, alpha=150, sleeves=12)
    x, y, w, h = parts["head"]["front"]
    for ex in (1, 2, 5, 6):
        for ey in (3, 4):
            img.putpixel((x + ex, y + ey), (10, 15, 20, 230))
    for mx in (3, 4):
        img.putpixel((x + mx, y + 6), (10, 15, 20, 200))
    # The shroud fades away towards the feet; ghostly light streaks.
    for rect in side_faces(parts["leg"]) + side_faces(parts["body"]):
        rx, ry, rw, rh = rect
        for j in range(rh):
            for i in range(rw):
                c = img.getpixel((rx + i, ry + j))
                fade = 1.0 - (j / rh) * (0.7 if rect in side_faces(parts["leg"]) else 0.2)
                if rng.random() < 0.08:
                    c = (220, 240, 255, c[3])
                img.putpixel((rx + i, ry + j), (c[0], c[1], c[2], int(c[3] * fade)))
    shade_parts(img, parts)
    return img


def cyclops(rng):
    img, parts = humanoid(rng, 0xB08A63, 0x6B4A2B, 0xB08A63, hair=0x4E3B2A, sleeves=0)
    face(img, parts["head"], iris=0x3B5E2B, eye_row=4, single_eye=True, mouth=0x5A3A2A, brow=0x3A2A1C)
    # Bare chest with a sheepskin over one shoulder and a loincloth.
    for rect in side_faces(parts["body"]):
        x, y, w, h = rect
        fill_rect(img, x, y, w, h, rgb(0xB08A63), rng, 8)
        fill_rect(img, x, y + 7, w, 5, rgb(0x6B4A2B), rng, 10)
        for j in range(7):
            k = j if rect == parts["body"]["front"] else -1
            if 0 <= k < w:
                img.putpixel((x + k, y + j), rgb(0xE8E2D4))
                if k + 1 < w:
                    img.putpixel((x + k + 1, y + j), rgb(0xD8D0C0))
    x, y, w, h = parts["body"]["front"]
    for px, py in ((2, 3), (5, 3), (3, 5), (4, 5)):
        img.putpixel((x + px, y + py), scale(img.getpixel((x + px, y + py)), 0.85))
    # A thick beard.
    hx, hy, hw, hh = parts["head"]["front"]
    fill_rect(img, hx + 1, hy + 6, 6, 2, rgb(0x4E3B2A), rng, 10)
    band(img, parts["leg"], 10, 2, rgb(0x5A3A22), rng, 4)
    shade_parts(img, parts)
    return img


def medusa(rng):
    img, parts = humanoid(rng, 0x9DB884, 0xD4B85A, 0xC2A64A, hair=0x3F6B2E, sandals=0x8A6A2A)
    face(img, parts["head"], iris=0xE8D44D, eye_row=4, mouth=0x5A2A3A, brow=0x2F5A22)
    # Scales on her skin, a golden chiton with a meander border.
    for rect in side_faces(parts["arm"]) + [parts["head"]["right"], parts["head"]["left"]]:
        x, y, w, h = rect
        for j in range(4 if rect in side_faces(parts["arm"]) else 5, h, 2):
            for i in range(j % 2, w, 2):
                img.putpixel((x + i, y + j), rgb(0x7C9A66))
    for rect in side_faces(parts["body"]) + side_faces(parts["leg"]):
        x, y, w, h = rect
        if rect in side_faces(parts["leg"]):
            for i in range(w):
                img.putpixel((x + i, y + 7), rgb(0x7A5A1A))
                img.putpixel((x + i, y + 8 + (i % 2)), rgb(0x7A5A1A))
    band(img, parts["body"], 6, 1, rgb(0x7A5A1A), rng, 4)
    # Snakes on the hat layer, with yellow eyes.
    for name, (x, y, w, h) in box_faces(32, 0, 8, 8, 8).items():
        for i in range(w):
            for j in range(h):
                if name == "front" and j >= 2:
                    continue
                if name == "bottom":
                    continue
                if (i + j * 2) % 3 != 2 or name == "top":
                    img.putpixel((x + i, y + j), scale(jitter(rgb(0x4F7A3A), rng, 18), 1.0 - 0.25 * ((i + j) % 2)))
        if name in ("right", "left", "back", "front"):
            for i in range(1, w, 3):
                img.putpixel((x + i, y + (0 if name == "front" else rng.randrange(h))), rgb(0xE8D44D))
    shade_parts(img, parts)
    return img


def minotaur(rng):
    img, parts = humanoid(rng, 0x4A2E1E, 0x5C3A26, 0x3B2416, arms=0x5C3A26, sandals=0x1A100A)
    face(img, parts["head"], iris=0xC0392B, eye_row=3, brow=0x1A100A)
    # Shaggy fur everywhere, a lighter muzzle and a bronze kilt with studs.
    for part in ("head", "body", "arm", "leg"):
        for rect in side_faces(parts[part]):
            speckle(img, rect, rgb(0x2E1C12), rng, rect[2] * rect[3] // 5)
    x, y, w, h = parts["head"]["front"]
    fill_rect(img, x + 2, y + 5, 4, 3, rgb(0x7A5640), rng, 6)
    for rect in side_faces(parts["body"]):
        rx, ry, rw, rh = rect
        fill_rect(img, rx, ry + 8, rw, 4, rgb(0xB07A2E), rng, 10)
        for i in range(0, rw, 2):
            img.putpixel((rx + i, ry + 8), rgb(0xE2B33C))
            img.putpixel((rx + i + 1 if i + 1 < rw else rx + i, ry + 11), rgb(0x6A4416))
    parts["horn_r"] = paint_box(img, 0, 32, 6, 2, 2, rgb(0xE8DCC0), rng, 6, shaded=False)
    parts["horn_l"] = paint_box(img, 0, 36, 6, 2, 2, rgb(0xE8DCC0), rng, 6, shaded=False)
    for horn in (parts["horn_r"], parts["horn_l"]):
        for rect in side_faces(horn):
            fill_rect(img, rect[0], rect[1], 2, rect[3], rgb(0x8A7A60), rng, 6)
    parts["snout"] = paint_box(img, 16, 32, 5, 3, 2, rgb(0x7A5640), rng, 6, shaded=False)
    x, y, w, h = parts["snout"]["front"]
    img.putpixel((x + 1, y + 1), rgb(0x1A100A))
    img.putpixel((x + 3, y + 1), rgb(0x1A100A))
    fill_rect(img, x + 1, y + 2, 3, 1, rgb(0xE2B33C), rng, 0)  # nose ring
    shade_parts(img, parts)
    return img


def spartoi(rng):
    img = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    bone = rgb(0xD8D3C4)
    parts = {"head": paint_box(img, 0, 0, 8, 8, 8, bone, rng, 8, shaded=False)}
    x, y, w, h = parts["head"]["front"]
    for ex in (1, 2, 5, 6):
        for ey in (3, 4):
            img.putpixel((x + ex, y + ey), rgb(0x1A1A1A))
    img.putpixel((x + 3, y + 5), rgb(0x3A3A3A))
    img.putpixel((x + 4, y + 5), rgb(0x3A3A3A))
    for mx in range(1, 7):
        img.putpixel((x + mx, y + 6), rgb(0x3A3A3A) if mx % 2 else bone)
    # Cracks: these warriors grew from dragon's teeth.
    for rect in side_faces(parts["head"]):
        cx, cy = rect[0] + rng.randrange(rect[2]), rect[1]
        for _ in range(4):
            img.putpixel((cx, cy), rgb(0x8E887A))
            cx = max(rect[0], min(rect[0] + rect[2] - 1, cx + rng.choice((-1, 0, 1))))
            cy += 1
    parts["body"] = box_faces(16, 16, 8, 12, 4)
    for name, (x, y, w, h) in parts["body"].items():
        for j in range(h):
            for i in range(w):
                rib = name in ("front", "back") and j < 8 and j % 2 == 1 and 1 <= i < w - 1 and i != w // 2
                if not rib:
                    img.putpixel((x + i, y + j), jitter(bone, rng, 8))
    parts["arm"] = paint_box(img, 40, 16, 2, 12, 2, bone, rng, 8, shaded=False)
    parts["leg"] = paint_box(img, 0, 16, 2, 12, 2, bone, rng, 8, shaded=False)
    shade_parts(img, parts)
    return img


# Vanilla horse UV layout (HorseModel.createBodyMesh), shared by the pegasus and the golden hind.
HORSE_PARTS = {"body": (0, 32, 10, 10, 22), "neck": (0, 35, 4, 12, 7), "head": (0, 13, 6, 5, 7), "mouth": (0, 25, 4, 5, 5),
               "mane": (56, 36, 2, 16, 2), "tail": (42, 36, 3, 14, 4), "leg": (48, 21, 4, 11, 4), "ear": (19, 16, 2, 3, 1)}


def horse(rng, coat, mane, hooves, eyes=0x1A1410, spots=None):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    parts = {}
    for name in ("neck", "body", "head", "mouth", "ear", "leg"):
        parts[name] = paint_box(img, *HORSE_PARTS[name], rgb(coat), rng, 6, shaded=False)
    for name in ("mane", "tail"):
        parts[name] = paint_box(img, *HORSE_PARTS[name], rgb(mane), rng, 14, shaded=False)
        for rect in side_faces(parts[name]):
            x, y, w, h = rect
            for i in range(w):
                for j in range(h):
                    if (i * 3 + j) % 4 == 0:
                        img.putpixel((x + i, y + j), scale(img.getpixel((x + i, y + j)), 0.8))
    band(img, parts["leg"], 8, 3, rgb(hooves), rng, 6)
    fill_rect(img, *parts["leg"]["bottom"], rgb(hooves), rng, 6)
    # Eyes on the sides of the head, a darker muzzle with nostrils.
    for name in ("right", "left"):
        x, y, w, h = parts["head"][name]
        img.putpixel((x + 2, y + 1), rgb(eyes))
        img.putpixel((x + 3, y + 1), rgb(0xF4F1EA))
    x, y, w, h = parts["mouth"]["front"]
    fill_rect(img, x, y + 2, w, 3, scale(rgb(coat), 0.75), rng, 4)
    img.putpixel((x + 1, y + 2), rgb(0x1A1410))
    img.putpixel((x + 2, y + 2), rgb(0x1A1410))
    # Pale belly.
    x, y, w, h = parts["body"]["bottom"]
    fill_rect(img, x, y, w, h, mix(rgb(coat), rgb(0xFFFFFF), 0.35), rng, 6)
    if spots:
        for name in ("top", "right", "left"):
            speckle(img, parts["body"][name], rgb(spots), rng, 14, 6)
    return img, parts


def pegasus(rng):
    img, parts = horse(rng, 0xF4F1EA, 0xE6C35C, 0xB8A27A, eyes=0x2E5FA8)
    parts["wing"] = paint_box(img, 0, 0, 14, 1, 10, rgb(0xFBFAF6), rng, 6, shaded=False)
    for name in ("top", "bottom"):
        x, y, w, h = parts["wing"][name]
        for j in range(h):
            for i in range(w):
                if i % 3 == 0 and j > 1:
                    img.putpixel((x + i, y + j), rgb(0xDCD6C8))
            img.putpixel((x + w - 1, y + j), rgb(0xE6C35C))
        fill_rect(img, x, y + h - 2, w, 2, rgb(0xE6C35C), rng, 10)
    shade_parts(img, parts)
    return img


def golden_hind(rng):
    img, parts = horse(rng, 0xC08A3E, 0x8A5A22, 0xB07A2E, spots=0xF2E6C8)
    x, y, w, h = parts["tail"]["front"]
    fill_rect(img, x, y + h - 4, w, 4, rgb(0xF4F1EA), rng, 6)
    # Golden antlers, bronze hooves.
    parts["antler"] = paint_box(img, 0, 0, 1, 7, 1, rgb(0xF2C440), rng, 10, shaded=False)
    band(img, parts["leg"], 8, 3, rgb(0xC98A2E), rng, 8)
    for rect in side_faces(parts["leg"]):
        img.putpixel((rect[0] + 1, rect[1] + 9), rgb(0xFFE08A))
    shade_parts(img, parts)
    return img


BEAST_PARTS = {"body": (0, 0, 10, 10, 18), "leg": (0, 44, 4, 10, 4), "tail": (16, 44, 2, 2, 10), "head": (32, 28, 7, 7, 6),
               "nose": (40, 44, 4, 3, 3), "mane": (0, 28, 10, 10, 4)}


def beast(rng, fur, snout, eyes, mane=None, back=None, belly=None, claws=0x2A1C12, glow=False):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    parts = {}
    for name in ("body", "leg", "tail", "head", "nose"):
        parts[name] = paint_box(img, *BEAST_PARTS[name], rgb(snout if name == "nose" else fur), rng, 10, shaded=False)
    if back:
        x, y, w, h = parts["body"]["top"]
        for j in range(h):
            for i in range(w):
                t = abs(i - (w - 1) / 2) / (w / 2)
                img.putpixel((x + i, y + j), mix(rgb(back), img.getpixel((x + i, y + j)), t))
    if belly:
        fill_rect(img, *parts["body"]["bottom"], rgb(belly), rng, 8)
        for name in ("right", "left"):
            x, y, w, h = parts["body"][name]
            fill_rect(img, x, y + h - 3, w, 3, rgb(belly), rng, 8)
    for rect in side_faces(parts["body"]):
        speckle(img, rect, scale(rgb(fur), 0.8), rng, 20)
    band(img, parts["leg"], 8, 2, scale(rgb(fur), 0.75), rng, 6)
    for rect in side_faces(parts["leg"]):
        for i in (0, 2):
            img.putpixel((rect[0] + i, rect[1] + rect[3] - 1), rgb(claws))
    x, y, w, h = parts["head"]["front"]
    for ex in (1, 5):
        img.putpixel((x + ex, y + 2), rgb(eyes))
        if glow:
            img.putpixel((x + ex, y + 3), scale(rgb(eyes), 0.6))
        img.putpixel((x + ex, y + 1), scale(rgb(fur), 0.6))
    x, y, w, h = parts["nose"]["front"]
    fill_rect(img, x + 1, y, 2, 1, rgb(0x1A100A), rng, 0)
    fill_rect(img, x, y + 2, w, 1, rgb(0x2A1410), rng, 0)
    for i in (0, w - 1):
        img.putpixel((x + i, y + 2), rgb(0xF0EAD8))  # fangs
    if mane:
        parts["mane"] = paint_box(img, *BEAST_PARTS["mane"], rgb(mane), rng, 16, shaded=False)
        for rect in parts["mane"].values():
            mx, my, mw, mh = rect
            for i in range(mw):
                for j in range(mh):
                    if (i + j * 3) % 5 == 0:
                        img.putpixel((mx + i, my + j), scale(rgb(mane), 0.7))
                    elif (i * 2 + j) % 7 == 0:
                        img.putpixel((mx + i, my + j), mix(rgb(mane), rgb(0xE0B04A), 0.5))
        x, y, w, h = parts["mane"]["front"]
        fill_rect(img, x + 2, y + 2, w - 4, h - 4, (0, 0, 0, 0), rng, 0)
    shade_parts(img, parts)
    return img


def nemean_lion(rng):
    return beast(rng, 0xC9962E, 0xE0B870, 0x2A1C12, mane=0x8A5A1C, back=0xA8741E, belly=0xE8CC8A)


def cerberus(rng):
    img = beast(rng, 0x241E1E, 0x3A2E2E, 0xFF4A1C, back=0x141010, belly=0x3A2E2E, claws=0x8A1C1C, glow=True)
    # Glowing cracks of hellfire along the flanks.
    for name in ("right", "left"):
        x, y, w, h = box_faces(*BEAST_PARTS["body"])[name]
        cx, cy = x + 2, y + rng.randrange(2, h - 2)
        while cx < x + w - 1:
            img.putpixel((cx, cy), rgb(0xE5501F))
            cx += 1
            cy = max(y + 1, min(y + h - 2, cy + rng.choice((-1, 0, 1))))
    return img


def hydra(rng, scales=0x2F5D3A, neck=0x3C7D46, belly=0x8BA86A, spines=0x8BC34A, eyes=0xE8D44D):
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    parts = {
        "body": paint_box(img, 0, 0, 16, 12, 20, rgb(scales), rng, 10, faces={"bottom": rgb(belly)}, shaded=False),
        "leg": paint_box(img, 0, 32, 6, 8, 6, rgb(scales), rng, 10, shaded=False),
        "tail": paint_box(img, 0, 46, 4, 4, 14, rgb(scales), rng, 10, shaded=False),
        "neck": paint_box(img, 72, 0, 3, 14, 3, rgb(neck), rng, 10, shaded=False),
        "head": paint_box(img, 72, 20, 5, 5, 7, rgb(neck), rng, 10, shaded=False),
    }
    # Overlapping scales: a lighter crescent on every other pixel row.
    for part in ("body", "leg", "tail", "neck"):
        for name, rect in parts[part].items():
            if name == "bottom":
                continue
            x, y, w, h = rect
            for j in range(0, h, 2):
                for i in range((j // 2) % 2, w, 2):
                    img.putpixel((x + i, y + j), scale(img.getpixel((x + i, y + j)), 1.18))
    for name in ("right", "left"):
        x, y, w, h = parts["body"][name]
        fill_rect(img, x, y + h - 3, w, 3, rgb(belly), rng, 8)
    x, y, w, h = parts["neck"]["front"]
    fill_rect(img, x + 1, y, 1, h, rgb(belly), rng, 6)
    x, y, w, h = parts["head"]["front"]
    img.putpixel((x + 1, y + 1), rgb(eyes))
    img.putpixel((x + 3, y + 1), rgb(eyes))
    fill_rect(img, x, y + 3, w, 1, rgb(0x7A1C1C), rng, 0)
    img.putpixel((x + 1, y + 4), rgb(0xF0EAD8))
    img.putpixel((x + 3, y + 4), rgb(0xF0EAD8))
    x, y, w, h = parts["head"]["top"]
    for j in range(0, h, 2):
        img.putpixel((x + w // 2, y + j), rgb(spines))
    # Spines along the back.
    x, y, w, h = parts["body"]["top"]
    for j in range(0, h, 3):
        fill_rect(img, x + w // 2 - 1, y + j, 2, 2, rgb(spines), rng, 0)
    shade_parts(img, parts)
    return img


def hydra_hatchling(rng):
    return hydra(rng, scales=0x4F9A4A, neck=0x63B05A, belly=0xD7E88A, spines=0xF2D45A, eyes=0xF4F1EA)


# Villager UV layout (VillagerModel), used by the agora merchants.
VILLAGER_PARTS = {"head": (0, 0, 8, 10, 8), "nose": (24, 0, 2, 4, 2), "body": (16, 20, 8, 12, 6), "robe": (0, 38, 8, 20, 6),
                  "arm": (44, 22, 4, 8, 4), "arms_cross": (40, 38, 8, 4, 4), "leg": (0, 22, 4, 12, 4)}


def greek_merchant(rng, robe, trim, skin=0xC8956B, hair=0x3E2B1E, beard=True, hat=None, laurel=False, apron=None):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    parts = {}
    parts["head"] = paint_box(img, *VILLAGER_PARTS["head"], rgb(skin), rng, 6,
                              faces={"top": rgb(hair), "back": rgb(hair)}, shaded=False)
    for name in ("right", "left"):
        x, y, w, h = parts["head"][name]
        fill_rect(img, x, y, w, 3, rgb(hair), rng, 8)
    x, y, w, h = parts["head"]["front"]
    fill_rect(img, x, y, w, 2, rgb(hair), rng, 8)
    for ex in (1, 5):
        img.putpixel((x + ex, y + 4), rgb(0xF4F1EA))
        img.putpixel((x + ex + 1, y + 4), rgb(0x3B2A1A))
        img.putpixel((x + ex, y + 3), scale(rgb(hair), 0.8))
        img.putpixel((x + ex + 1, y + 3), scale(rgb(hair), 0.8))
    if beard:
        fill_rect(img, x + 1, y + 7, 6, 3, rgb(hair), rng, 10)
        for name in ("right", "left"):
            rx, ry, rw, rh = parts["head"][name]
            fill_rect(img, rx + (0 if name == "left" else rw - 3), ry + 6, 3, 4, rgb(hair), rng, 10)
    parts["nose"] = paint_box(img, *VILLAGER_PARTS["nose"], scale(rgb(skin), 0.92), rng, 4, shaded=False)
    for name in ("body", "robe", "arms_cross"):
        parts[name] = paint_box(img, *VILLAGER_PARTS[name], rgb(robe), rng, 8, shaded=False)
    parts["arm"] = paint_box(img, *VILLAGER_PARTS["arm"], rgb(robe), rng, 8, shaded=False)
    # Hands at the ends of the crossed arms.
    x, y, w, h = parts["arms_cross"]["front"]
    fill_rect(img, x, y, 2, h, rgb(skin), rng, 4)
    fill_rect(img, x + w - 2, y, 2, h, rgb(skin), rng, 4)
    parts["leg"] = paint_box(img, *VILLAGER_PARTS["leg"], rgb(skin), rng, 6, shaded=False)
    band(img, parts["leg"], 10, 2, rgb(0x6B4A2B), rng, 4)
    # Meander (Greek key) border along the hem of the robe, a sash across the chest.
    for rect in side_faces(parts["robe"]):
        rx, ry, rw, rh = rect
        for i in range(rw):
            img.putpixel((rx + i, ry + rh - 3), rgb(trim))
            img.putpixel((rx + i, ry + rh - 1), rgb(trim))
            if i % 3 == 0:
                img.putpixel((rx + i, ry + rh - 2), rgb(trim))
        for j in range(3, rh - 4):
            for fx in (2, rw - 3):
                if 0 <= fx < rw:
                    img.putpixel((rx + fx, ry + j), scale(img.getpixel((rx + fx, ry + j)), 0.86))
    for rect in (parts["body"]["front"], parts["robe"]["front"]):
        rx, ry, rw, rh = rect
        for k in range(min(rw, 8)):
            img.putpixel((rx + k, ry + k), rgb(trim))
    if apron:
        for rect in (parts["body"]["front"], parts["robe"]["front"]):
            rx, ry, rw, rh = rect
            fill_rect(img, rx + 1, ry + 2, rw - 2, rh - 4, rgb(apron), rng, 10)
            speckle(img, (rx + 1, ry + 2, rw - 2, rh - 4), rgb(0x1A1410), rng, 6)
    if hat:
        # Petasos: the wide-brimmed travelling hat of Hermes' merchants, on the hat rim layer.
        parts["rim"] = paint_box(img, 30, 47, 16, 16, 1, rgb(hat), rng, 10, shaded=False)
        x, y, w, h = parts["rim"]["top"]
        for i in range(w):
            for j in range(h):
                r = math.hypot(i - (w - 1) / 2, j - (h - 1) / 2)
                if r > 7.6:
                    img.putpixel((x + i, y + j), (0, 0, 0, 0))
                elif r > 6.6:
                    img.putpixel((x + i, y + j), scale(rgb(hat), 0.75))
        x, y, w, h = parts["rim"]["bottom"]
        for i in range(w):
            for j in range(h):
                if math.hypot(i - (w - 1) / 2, j - (h - 1) / 2) > 7.6:
                    img.putpixel((x + i, y + j), (0, 0, 0, 0))
        for name in ("front", "back", "right", "left"):
            x, y, w, h = parts["rim"][name]
            fill_rect(img, x, y, w, h, (0, 0, 0, 0), rng, 0)
        hat_rects = box_faces(32, 0, 8, 10, 8)
        x, y, w, h = hat_rects["top"]
        fill_rect(img, x + 1, y + 1, w - 2, h - 2, rgb(hat), rng, 10)
        for name in ("front", "back", "right", "left"):
            x, y, w, h = hat_rects[name]
            fill_rect(img, x, y, w, 1, scale(rgb(hat), 0.85), rng, 6)
    if laurel:
        hat_rects = box_faces(32, 0, 8, 10, 8)
        for name in ("front", "back", "right", "left"):
            x, y, w, h = hat_rects[name]
            for i in range(w):
                img.putpixel((x + i, y + 1 + (i % 2)), jitter(rgb(0x4F8A3A), rng, 16))
    shade_parts(img, parts)
    return img


ENTITIES = {
    "satyr": satyr,
    "harpy": harpy,
    "shade": shade,
    "cyclops": cyclops,
    "medusa": medusa,
    "minotaur": minotaur,
    "spartoi": spartoi,
    "pegasus": pegasus,
    "golden_hind": golden_hind,
    "nemean_lion": nemean_lion,
    "cerberus": cerberus,
    "hydra": hydra,
    "hydra_hatchling": hydra_hatchling,
    # 0 trophy dealer, 1 smith of Hephaestus, 2 priestess (see GreekMerchant).
    "greek_merchant_0": lambda rng: greek_merchant(rng, 0x2E5FA8, 0xE2B33C, hat=0x8A6A3A),
    "greek_merchant_1": lambda rng: greek_merchant(rng, 0x8A2E22, 0x3A2A1C, skin=0xB07A50, hair=0x1A1410, apron=0x4A3220),
    "greek_merchant_2": lambda rng: greek_merchant(rng, 0xF4F1EA, 0xE2B33C, skin=0xE2C3A4, hair=0x6B3E1A, beard=False,
                                                   laurel=True),
}

def brazier_side(rng):
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(0xB0723A), rng, 10)
    for x in range(16):
        img.putpixel((x, 0), rgb(0xE2B33C))
        img.putpixel((x, 15), rgb(0x6A3E1C))
        # Meander band in the middle.
        if x % 4 in (0, 1):
            img.putpixel((x, 6), rgb(0x6A3E1C))
        if x % 4 in (1, 2, 3) and x % 8 < 4:
            img.putpixel((x, 9), rgb(0x6A3E1C))
    for x in range(16):
        for y in range(1, 15):
            if (x + y) % 9 == 0:
                img.putpixel((x, y), rgb(0x3F8A6A))  # patina
    return img


def brazier_top(rng, lit=False):
    img = Image.new("RGBA", (16, 16))
    for x in range(16):
        for y in range(16):
            edge = x in (0, 15) or y in (0, 15)
            rim = x in (1, 14) or y in (1, 14)
            if edge:
                c = rgb(0xE2B33C)
            elif rim:
                c = rgb(0x8A522A)
            elif lit:
                t = rng.random()
                c = rgb(0xFFB43C if t < 0.3 else 0xE5501F if t < 0.6 else 0x5A1C0E)
            else:
                c = jitter(rgb(0x3A3430), rng, 14)
            img.putpixel((x, y), c)
    return img


def cloud(rng):
    img = Image.new("RGBA", (16, 16))
    for x in range(16):
        for y in range(16):
            puff = math.sin(x * 0.7) * math.cos(y * 0.6) + math.sin((x + y) * 0.4)
            v = int(238 + 10 * puff + rng.randint(-4, 4))
            img.putpixel((x, y), (min(255, v), min(255, v), min(255, v + 4), 215 + int(15 * puff)))
    return img


def golden_leaves(rng):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for x in range(16):
        for y in range(16):
            if rng.random() < 0.82:
                c = rng.choice((0xF2C440, 0xE2B33C, 0xD49A2A, 0xFFE08A, 0xC98A2E))
                img.putpixel((x, y), jitter(rgb(c), rng, 10))
    # A few golden apples among the leaves.
    for _ in range(2):
        ax, ay = rng.randrange(1, 14), rng.randrange(1, 14)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            img.putpixel((ax + dx, ay + dy), rgb(0xFFD700 if (dx, dy) != (0, 0) else 0xFFF6C0))
        img.putpixel((ax + 1, ay - 1), rgb(0x6B4A2B))
    return img


BLOCKS = {
    "cloud": cloud,
    "golden_leaves": golden_leaves,
    "brazier_side": brazier_side,
    "brazier_top": brazier_top,
    "brazier_top_lit": lambda rng: brazier_top(rng, lit=True),
    "marble": marble,
    "marble_bricks": marble_bricks,
    "marble_pillar": marble_pillar_side,
    "marble_pillar_top": marble_pillar_top,
    "olympian_marble": olympian_marble,
    "asphodel": asphodel,
    "hellas_portal": hellas_portal,
}
