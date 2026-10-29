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
        # Petasos: the wide-brimmed travelling hat of Hermes' merchants. The rim is a 16x16x1 box that the model turns
        # flat, so its round brim goes on the big front and back faces and the thin edges stay empty.
        parts["rim"] = paint_box(img, 30, 47, 16, 16, 1, rgb(hat), rng, 10, shaded=False)
        for name in ("front", "back"):
            x, y, w, h = parts["rim"][name]
            for i in range(w):
                for j in range(h):
                    r = math.hypot(i - (w - 1) / 2, j - (h - 1) / 2)
                    if r > 7.6:
                        img.putpixel((x + i, y + j), (0, 0, 0, 0))
                    elif r > 6.6 or r < 4.2:
                        img.putpixel((x + i, y + j), scale(rgb(hat), 0.78))
        for name in ("top", "bottom", "right", "left"):
            x, y, w, h = parts["rim"][name]
            fill_rect(img, x, y, w, h, (0, 0, 0, 0), rng, 0)
        del parts["rim"]
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


# ================================================================ added in 0.4
# Each texture below gets its own random generator (seeded by its name), so adding one never changes the others.

def stone_bricks(rng, base, mortar, rows=4):
    img = Image.new("RGBA", (16, 16))
    fill_rect(img, 0, 0, 16, 16, rgb(base), rng, 7)
    h = 16 // rows
    for r in range(rows):
        y = r * h
        for x in range(16):
            img.putpixel((x, y), jitter(rgb(mortar), rng, 4))
        offset = 0 if r % 2 == 0 else 4
        for x in (offset, offset + 8):
            for j in range(y, y + h):
                img.putpixel((x % 16, j), jitter(rgb(mortar), rng, 4))
        # Light top edge and dark bottom edge on every brick.
        for x in range(16):
            if y + 1 < 16 and img.getpixel((x, y + 1))[:3] != rgb(mortar)[:3]:
                img.putpixel((x, y + 1), scale(img.getpixel((x, y + 1)), 1.1))
            if y + h - 1 < 16:
                img.putpixel((x, y + h - 1), scale(img.getpixel((x, y + h - 1)), 0.86))
    return img


def labyrinth_bricks(rng, moss=False, cracked=False):
    img = stone_bricks(rng, 0x5D6069, 0x2E3036)
    # A worn bronze-red meander inlaid in the middle row: the mark of Daedalus.
    for i, (x, y) in enumerate(((2, 9), (2, 10), (3, 10), (4, 10), (4, 9), (5, 9), (6, 9), (6, 10), (7, 10),
                                (10, 9), (10, 10), (11, 10), (12, 10), (12, 9), (13, 9))):
        img.putpixel((x, y), jitter(rgb(0x8A4A2E), rng, 10))
    if moss:
        for _ in range(5):
            cx, cy = rng.randrange(16), rng.randrange(16)
            for _ in range(7):
                x, y = (cx + rng.randint(-2, 2)) % 16, (cy + rng.randint(-1, 2)) % 16
                img.putpixel((x, y), jitter(rgb(rng.choice((0x4F6B32, 0x5E7D3A, 0x3E5A2A))), rng, 8))
    if cracked:
        for _ in range(2):
            x, y = rng.randrange(16), rng.randrange(16)
            for _ in range(9):
                img.putpixel((x % 16, y % 16), rgb(0x24262B))
                x += rng.choice((-1, 0, 1))
                y += rng.choice((0, 1))
    return img


def leaves(rng, colors, fruit=None, fruit_count=0, fruit_size=2, holes=0.16):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    for x in range(16):
        for y in range(16):
            if rng.random() > holes:
                img.putpixel((x, y), jitter(rgb(rng.choice(colors)), rng, 8))
    for _ in range(fruit_count):
        fx, fy = rng.randrange(1, 16 - fruit_size), rng.randrange(1, 16 - fruit_size)
        for dx in range(fruit_size):
            for dy in range(fruit_size):
                img.putpixel((fx + dx, fy + dy), rgb(fruit[0]))
        img.putpixel((fx, fy), rgb(fruit[1]))
        if fruit_size > 1:
            img.putpixel((fx + fruit_size - 1, fy + fruit_size - 1), scale(rgb(fruit[0]), 0.7))
    return img


OLIVE_GREENS = (0x7E9468, 0x92A67C, 0x6A8058, 0xA9B998, 0x5E7450)
POMEGRANATE_GREENS = (0x3E6B34, 0x4E7E3E, 0x2E5628, 0x5A8A46)

NEW_BLOCKS = {
    "labyrinth_bricks": labyrinth_bricks,
    "mossy_labyrinth_bricks": lambda rng: labyrinth_bricks(rng, moss=True),
    "cracked_labyrinth_bricks": lambda rng: labyrinth_bricks(rng, cracked=True),
    "olive_leaves": lambda rng: leaves(rng, OLIVE_GREENS),
    "olive_leaves_ripe": lambda rng: leaves(rng, OLIVE_GREENS, (0x3B2A3A, 0x6E5470), 7, 1),
    "pomegranate_leaves": lambda rng: leaves(rng, POMEGRANATE_GREENS),
    "pomegranate_leaves_ripe": lambda rng: leaves(rng, POMEGRANATE_GREENS, (0xB8202A, 0xF06A6A), 3, 3),
}


def draw_olives(img, d, rng):
    d.line([(3, 3), (12, 9)], fill=rgb(0x6B4A2B))
    d.polygon([(6, 3), (9, 2), (11, 4), (8, 5)], fill=rgb(0x7E9468))
    for x, y in ((4, 8), (8, 10), (11, 12)):
        d.ellipse([x, y, x + 3, y + 3], fill=rgb(0x3B2A3A))
        img.putpixel((x + 1, y + 1), rgb(0x8A6E8E))


def draw_pomegranate(img, d, rng):
    d.ellipse([2, 4, 13, 14], fill=rgb(0xB8202A))
    d.ellipse([4, 6, 7, 9], fill=rgb(0xE85A5A))
    d.polygon([(6, 4), (7, 1), (8, 3), (9, 1), (10, 4)], fill=rgb(0x8A1A20))
    img.putpixel((5, 7), rgb(0xFFC0C0))


def draw_wings(img, d, rng):
    for side in (-1, 1):
        cx = 8 + side
        for i in range(6):
            x = cx + side * (1 + i)
            top = 3 + i // 2
            d.line([(x, top), (x, 13 - i)], fill=rgb(0xF4F1EA if i % 2 == 0 else 0xD9D2C2))
        d.line([(cx, 3), (cx + side * 6, 3)], fill=rgb(0xE2B33C))
    d.line([(8, 3), (8, 9)], fill=rgb(0xC98A2E))


def draw_karkinos_claw(img, d, rng):
    d.polygon([(3, 13), (6, 6), (11, 3), (13, 6), (9, 8), (12, 11), (7, 10), (5, 14)], fill=rgb(0xB3361E))
    d.line([(6, 7), (11, 4)], fill=rgb(0xE86A4A))
    d.line([(9, 8), (12, 11)], fill=rgb(0x7A1E10))


def draw_girdle(img, d, rng):
    d.ellipse([1, 5, 14, 12], outline=rgb(0xE2B33C), width=2)
    d.rectangle([6, 4, 9, 7], fill=rgb(0xC9962E))
    img.putpixel((7, 5), rgb(0xC0262E))
    img.putpixel((8, 5), rgb(0xE85A5A))
    for x in (3, 12):
        img.putpixel((x, 8), rgb(0x8A1E2A))


def draw_necklace(img, d, rng):
    d.arc([2, 0, 13, 12], 20, 160, fill=rgb(0xE2B33C), width=1)
    for x, y, c in ((3, 7, 0x3AB8C8), (5, 9, 0xE85A5A), (8, 11, 0x3AB8C8), (10, 9, 0xE85A5A), (12, 7, 0x3AB8C8)):
        img.putpixel((x, y), rgb(c))
    d.polygon([(7, 11), (9, 11), (9, 14), (8, 15), (7, 14)], fill=rgb(0xC9962E))
    img.putpixel((8, 12), rgb(0x5AE0A0))
    img.putpixel((8, 13), rgb(0x3AB888))


def draw_horn_of_themiscyra(img, d, rng):
    d.polygon([(2, 12), (4, 9), (8, 6), (12, 3), (14, 2), (13, 5), (9, 9), (5, 12), (3, 14)], fill=rgb(0xD8C8A0))
    d.line([(4, 11), (12, 4)], fill=rgb(0xB8A47A))
    for x, y in ((5, 10), (8, 7), (11, 4)):
        img.putpixel((x, y), rgb(0xE2B33C))
        img.putpixel((x + 1, y + 1), rgb(0xE2B33C))
    d.line([(3, 13), (6, 15)], fill=rgb(0x8A1E2A))


def draw_ring(img, d, rng):
    d.ellipse([3, 5, 12, 14], outline=rgb(0xE2B33C), width=2)
    d.polygon([(7, 1), (9, 1), (10, 3), (8, 5), (6, 3)], fill=rgb(0xBFF4FF))
    img.putpixel((7, 2), rgb(0xFFFFFF))


def draw_journal(img, d, rng, cover=0x7A4A24, trim=0xE2B33C):
    d.rectangle([3, 2, 12, 14], fill=rgb(cover))
    d.rectangle([3, 2, 4, 14], fill=scale(rgb(cover), 0.7))
    d.rectangle([12, 3, 13, 13], fill=rgb(0xF4ECD8))
    for x, y in ((6, 4), (7, 4), (8, 4), (8, 5), (8, 6), (7, 6), (6, 6), (6, 7), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8)):
        img.putpixel((x, y), rgb(trim))
    d.line([(6, 11), (10, 11)], fill=rgb(trim))


NEW_ITEMS = {
    "olives": draw_olives,
    "pomegranate": draw_pomegranate,
    "wings_of_daedalus": draw_wings,
    "karkinos_claw": draw_karkinos_claw,
    "girdle_of_hippolyta": draw_girdle,
    "necklace_of_harmonia": draw_necklace,
    "horn_of_themiscyra": draw_horn_of_themiscyra,
    "wedding_ring": draw_ring,
    "greek_journal": draw_journal,
    "greek_journal_complete": lambda img, d, rng: draw_journal(img, d, rng, cover=0x4A2A6A),
}


def lion(rng):
    return beast(rng, 0xC4914A, 0xE0B880, 0x2A1C12, mane=0x6B4420, back=0xB07E3A, belly=0xE8D0A0)


def crab(rng, shell=0xB3361E, under=0xE8B07A, eyes=0x111111):
    """Layout of client/CrabModel."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    parts = {}
    parts["body"] = paint_box(img, 0, 0, 16, 6, 12, rgb(shell), rng, 12,
                              faces={"bottom": rgb(under)}, shaded=False)
    x, y, w, h = parts["body"]["top"]
    for _ in range(26):
        img.putpixel((x + rng.randrange(w), y + rng.randrange(h)), jitter(rgb(0xD9583A), rng, 10))
    for i in range(w):
        img.putpixel((x + i, y + h - 1), scale(rgb(shell), 0.7))
    for rect in side_faces(parts["body"]):
        rx, ry, rw, rh = rect
        fill_rect(img, rx, ry + rh - 2, rw, 2, rgb(under), rng, 6)
    parts["stalk"] = paint_box(img, 0, 18, 1, 4, 1, rgb(shell), rng, 6, shaded=False)
    parts["eye"] = paint_box(img, 4, 18, 2, 2, 2, rgb(eyes), rng, 4, shaded=False)
    parts["arm"] = paint_box(img, 0, 24, 3, 3, 6, rgb(shell), rng, 10, shaded=False)
    parts["pincer"] = paint_box(img, 20, 24, 5, 4, 6, rgb(shell), rng, 10, shaded=False)
    parts["finger"] = paint_box(img, 20, 36, 2, 1, 5, scale(rgb(shell), 0.8), rng, 8, shaded=False)
    parts["leg"] = paint_box(img, 0, 36, 8, 2, 2, rgb(shell), rng, 10, shaded=False)
    for rect in side_faces(parts["leg"]):
        rx, ry, rw, rh = rect
        for i in range(0, rw, 3):
            img.putpixel((rx + i, ry), rgb(under))
    shade_parts(img, parts)
    return img


# Player skin layout (slim arms) for the amazons.
SKIN = {"head": (0, 0, 8, 8, 8), "hat": (32, 0, 8, 8, 8), "body": (16, 16, 8, 12, 4), "jacket": (16, 32, 8, 12, 4),
        "right_arm": (40, 16, 3, 12, 4), "right_sleeve": (40, 32, 3, 12, 4), "left_arm": (32, 48, 3, 12, 4),
        "left_sleeve": (48, 48, 3, 12, 4), "right_leg": (0, 16, 4, 12, 4), "right_pants": (0, 32, 4, 12, 4),
        "left_leg": (16, 48, 4, 12, 4), "left_pants": (0, 48, 4, 12, 4)}


def amazon(rng, skin, hair, tunic, armour, trim, eyes=0x4A3320, crown=None, girdle=None, style="long", plume=None,
           flower=None, band=None, lips=0xC8505E):
    """A young amazon on the slim player skin. style: long, wavy, braid, ponytail or bob."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    parts = {}
    s = rgb(skin)
    h_c = rgb(hair)
    dark_hair = scale(h_c, 0.72)
    light_hair = scale(h_c, 1.25)

    def hair_px(x, y):
        c = h_c if (x + y) % 3 else light_hair
        if style == "wavy" and (x * 2 + y) % 5 == 0:
            c = dark_hair
        img.putpixel((x, y), jitter(c, rng, 6))

    def hair_rect(x, y, w, h):
        for i in range(x, x + w):
            for j in range(y, y + h):
                hair_px(i, j)

    parts["head"] = paint_box(img, *SKIN["head"], s, rng, 3, shaded=False)
    hd = parts["head"]
    hair_rect(*hd["top"])
    hair_rect(*hd["back"])
    long_hair = style in ("long", "wavy")
    for name in ("right", "left"):
        x, y, w, h = hd[name]
        hair_rect(x, y, w, 3)
        back = 5 if long_hair else 4 if style != "bob" else 6
        hair_rect(x + (w - back if name == "right" else 0), y, back, h if style != "bob" else 6)
        if style == "bob":
            hair_rect(x + (w - 7 if name == "right" else 0), y + 3, 7, 3)
    x, y, w, h = hd["front"]
    # A side-swept fringe that leaves the forehead partly bare.
    hair_rect(x, y, w, 1)
    hair_rect(x, y + 1, 5, 1)
    hair_px(x, y + 2)
    hair_px(x + 7, y + 2)
    if long_hair or style == "bob":
        for j in range(2, 7 if long_hair else 6):
            hair_px(x, y + j)
            hair_px(x + 7, y + j)
    # Brows, big eyes with dark lashes and a catchlight, a soft blush and full lips.
    for bx in (1, 2, 5, 6):
        img.putpixel((x + bx, y + 2), scale(dark_hair, 0.85))
    iris = rgb(eyes)
    for ex, outer in ((1, 0), (5, 1)):
        lash = rgb(0x1E1414)
        img.putpixel((x + ex, y + 3), lash)
        img.putpixel((x + ex + 1, y + 3), lash)
        white, pupil = (x + ex, x + ex + 1) if outer == 0 else (x + ex + 1, x + ex)
        img.putpixel((white, y + 4), rgb(0xF6F2EC))
        img.putpixel((pupil, y + 4), iris)
    img.putpixel((x + 2, y + 3), mix(rgb(0x1E1414), iris, 0.5))
    img.putpixel((x + 5, y + 3), mix(rgb(0x1E1414), iris, 0.5))
    img.putpixel((x + 4, y + 5), scale(s, 0.9))
    img.putpixel((x + 1, y + 5), mix(s, rgb(0xF08080), 0.4))
    img.putpixel((x + 6, y + 5), mix(s, rgb(0xF08080), 0.4))
    img.putpixel((x + 3, y + 6), rgb(lips))
    img.putpixel((x + 4, y + 6), scale(rgb(lips), 1.15))
    # Hair layer: volume over the crown, long hair down the back.
    hat = box_faces(*SKIN["hat"])
    hair_rect(*hat["top"])
    hx, hy, hw, hh = hat["back"]
    hair_rect(hx, hy, hw, hh if long_hair else 6)
    for name in ("right", "left"):
        hx, hy, hw, hh = hat[name]
        hair_rect(hx, hy, hw, 2)
        hair_rect(hx + (hw - 3 if name == "right" else 0), hy, 3, hh if long_hair else 5)
    fx, fy, fw, fh = hat["front"]
    hair_rect(fx, fy, fw, 1)
    hair_rect(fx, fy + 1, 3, 1)
    if crown:
        for name in ("front", "right", "left", "back"):
            cx, cy, cw, ch = hat[name]
            fill_rect(img, cx, cy, cw, 1, rgb(crown), rng, 6)
            for i in range(0, cw, 2):
                img.putpixel((cx + i, cy), scale(rgb(crown), 1.15))
        img.putpixel((fx + 3, fy + 1), rgb(0xC0262E))
        img.putpixel((fx + 4, fy + 1), rgb(0xC0262E))
    if band:
        for name in ("front", "right", "left", "back"):
            cx, cy, cw, ch = hat[name]
            fill_rect(img, cx, cy + 1, cw, 1, rgb(band), rng, 4)
    if flower:
        rx, ry, rw, rh = hat["left"]
        for dx, dy in ((1, 1), (2, 2), (1, 3), (0, 2)):
            img.putpixel((rx + dx, ry + dy), rgb(flower))
        img.putpixel((rx + 1, ry + 2), rgb(0xFFE08A))
    if plume:
        tx, ty, tw, th = hat["top"]
        fill_rect(img, tx + 3, ty, 2, th, rgb(plume), rng, 12)
        for name in ("front", "right", "left", "back"):
            cx, cy, cw, ch = hat[name]
            fill_rect(img, cx, cy, cw, 1, rgb(armour), rng, 6)
    parts["body"] = paint_box(img, *SKIN["body"], rgb(tunic), rng, 6, shaded=False)
    bx, by, bw, bh = parts["body"]["front"]
    fill_rect(img, bx + 2, by, 4, 1, s, rng, 3)       # a modest neckline
    for arm in ("right_arm", "left_arm"):
        parts[arm] = paint_box(img, *SKIN[arm], s, rng, 3, shaded=False)
        for rect in side_faces(parts[arm]):
            ax, ay, aw, ah = rect
            fill_rect(img, ax, ay, aw, 2, rgb(tunic), rng, 6)
            fill_rect(img, ax, ay + 8, aw, 2, rgb(armour), rng, 6)   # bracers
    for leg in ("right_leg", "left_leg"):
        parts[leg] = paint_box(img, *SKIN[leg], s, rng, 3, shaded=False)
        for rect in side_faces(parts[leg]):
            lx, ly, lw, lh = rect
            fill_rect(img, lx, ly, lw, 3, rgb(tunic), rng, 6)
            fill_rect(img, lx, ly + lh - 2, lw, 2, rgb(0x6B4A2B), rng, 6)    # sandals
            for j in range(lh - 6, lh - 2, 2):
                fill_rect(img, lx, ly + j, lw, 1, rgb(0x6B4A2B), rng, 4)     # straps
    # Armour layer: a shaped cuirass, a belt and a skirt of leather strips over the hips.
    jacket = box_faces(*SKIN["jacket"])
    for name in ("front", "back", "right", "left"):
        jx, jy, jw, jh = jacket[name]
        fill_rect(img, jx, jy + 2, jw, 5, rgb(armour), rng, 8)
        fill_rect(img, jx, jy + 7, jw, 1, rgb(girdle or trim), rng, 4)
        for i in range(jw):
            c = rgb(trim) if i % 2 == 0 else scale(rgb(trim), 0.75)
            fill_rect(img, jx + i, jy + 8, 1, 3 + (i % 2), c, rng, 6)
    jx, jy, jw, jh = jacket["front"]
    for px_ in (1, 2, 5, 6):
        img.putpixel((jx + px_, jy + 3), scale(rgb(armour), 1.22))
    img.putpixel((jx + 3, jy + 5), scale(rgb(armour), 0.8))
    img.putpixel((jx + 4, jy + 5), scale(rgb(armour), 0.8))
    if girdle:
        img.putpixel((jx + 3, jy + 7), rgb(0xC0262E))
        img.putpixel((jx + 4, jy + 7), rgb(0xFFE08A))
    for pants in ("right_pants", "left_pants"):
        pf = box_faces(*SKIN[pants])
        for name in ("front", "back", "right", "left"):
            px, py, pw, ph = pf[name]
            for i in range(pw):
                fill_rect(img, px + i, py, 1, 3, rgb(trim) if i % 2 == 0 else scale(rgb(trim), 0.75), rng, 8)
    for sleeve in ("right_sleeve", "left_sleeve"):
        pf = box_faces(*SKIN[sleeve])
        for name in ("front", "back", "right", "left"):
            px, py, pw, ph = pf[name]
            fill_rect(img, px, py, pw, 2, rgb(armour), rng, 8)
    # Hair down the back of the body.
    jx, jy, jw, jh = jacket["back"]
    if long_hair:
        hair_rect(jx + 1, jy, jw - 2, 6)
        for i in range(1, jw - 1, 2):
            hair_px(jx + i, jy + 6)
    elif style == "braid":
        hair_rect(jx + 3, jy, 2, 9)
        img.putpixel((jx + 3, jy + 9), rgb(band or trim))
        img.putpixel((jx + 4, jy + 9), rgb(band or trim))
    elif style == "ponytail":
        hair_rect(jx + 2, jy, 4, 2)
        hair_rect(jx + 3, jy + 2, 2, 5)
    for name in ("jacket", "right_pants", "left_pants", "right_sleeve", "left_sleeve", "hat"):
        parts[name] = box_faces(*SKIN[name])
    shade_parts(img, parts)
    return img


def wings_of_daedalus_entity(rng):
    """Elytra layout: one wing box at (22, 0), 10 x 20 x 2."""
    img = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    rects = box_faces(22, 0, 10, 20, 2)
    for name, (x, y, w, h) in rects.items():
        for i in range(w):
            for j in range(h):
                feather = (i + (j // 4)) % 3
                c = (0xF4F1EA, 0xE4DCCB, 0xCFC5B0)[feather]
                if name in ("front", "back") and j > h - 3 - (i % 4):
                    continue
                img.putpixel((x + i, y + j), jitter(rgb(c), rng, 6))
        if name in ("front", "back"):
            for i in range(w):
                img.putpixel((x + i, y), rgb(0xD9A441))    # wax along the frame
                img.putpixel((x + i, y + 1), rgb(0xE8C060))
    shade_box(img, rects)
    return img


NEW_ENTITIES = {
    "lion": lion,
    "karkinos": crab,
    # Common looks 0-3 and 5-9; 4 is the royal look of Hippolyta's daughters.
    "amazon_0": lambda rng: amazon(rng, 0xE0AE86, 0x3A2418, 0xF2ECDC, 0xB8823A, 0x7A3A22, eyes=0x5A3A22, band=0xC0262E),
    "amazon_1": lambda rng: amazon(rng, 0xC9946A, 0x8A3A1C, 0x8A2E22, 0xB8B8B8, 0x4A3220, eyes=0x3E6A3A, style="braid"),
    "amazon_2": lambda rng: amazon(rng, 0xF0D0B0, 0xE0B04A, 0x3A6AB8, 0xD9A441, 0xE2B33C, eyes=0x3A7AC8, style="wavy"),
    "amazon_3": lambda rng: amazon(rng, 0x8A5A3A, 0x1A1210, 0x3E7B44, 0xA87A3A, 0x6B4A2B, eyes=0x3A2418, style="wavy",
                                   flower=0xF4F1EA, lips=0xA8404A),
    "amazon_4": lambda rng: amazon(rng, 0xEEC4A0, 0x3A1E12, 0x6A2A7A, 0xE2B33C, 0xF4ECD8, eyes=0x6A3A8A, crown=0xE2B33C),
    "amazon_5": lambda rng: amazon(rng, 0xF4D4BC, 0xC0501E, 0x2E8A8A, 0x8A5A30, 0x5A3A20, eyes=0x3E8A3E, style="ponytail"),
    "amazon_6": lambda rng: amazon(rng, 0xD8A880, 0x141010, 0xF4F1EA, 0xD9A441, 0xE2B33C, eyes=0x2A1A10, style="bob",
                                   band=0xE2B33C),
    "amazon_7": lambda rng: amazon(rng, 0xF6DCC8, 0xF0E6C8, 0x8AB8D8, 0xC8CCD4, 0x5A6A8A, eyes=0x4A8AD8, style="braid",
                                   band=0x5A8AC8),
    "amazon_8": lambda rng: amazon(rng, 0x6E4228, 0x1E1410, 0xC9862E, 0xB8823A, 0x6B3A1E, eyes=0x2A1A10, style="braid",
                                   plume=0xC0262E, lips=0x9A3A44),
    "amazon_9": lambda rng: amazon(rng, 0xE6B892, 0x6A3E22, 0xD87A8A, 0xC9963E, 0x8A4A3A, eyes=0x6A4A2A, style="wavy",
                                   flower=0xF06A9A),
    "hippolyta": lambda rng: amazon(rng, 0xE6B894, 0x1E120C, 0x8A1E2A, 0xE2B33C, 0x5A1018, eyes=0x6B3E1A,
                                    crown=0xFFD34E, girdle=0xFFD34E),
    "wings_of_daedalus": wings_of_daedalus_entity,
}
