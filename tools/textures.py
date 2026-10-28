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


def paint_box(img, u, v, w, h, d, color, rng, noise=12, faces=None):
    for name, (x, y, fw, fh) in box_faces(u, v, w, h, d).items():
        c = (faces or {}).get(name, color)
        fill_rect(img, x, y, fw, fh, c, rng, noise)
    return box_faces(u, v, w, h, d)


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
    return img


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


ITEMS = {
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

def face(img, faces, eyes, eye_color=0x222222, mouth=None, rng=None, eye_row=3, single_eye=False):
    x, y, w, h = faces["front"]
    if single_eye:
        cx = x + w // 2 - 1
        for dx in range(2):
            for dy in range(2):
                img.putpixel((cx + dx, y + eye_row + dy), rgb(0xF4F1EA))
        img.putpixel((cx + 1, y + eye_row + 1), rgb(eye_color))
    else:
        for ex in eyes:
            img.putpixel((x + ex, y + eye_row), rgb(0xF4F1EA))
            img.putpixel((x + ex + 1, y + eye_row), rgb(eye_color))
    if mouth:
        for mx in range(2, w - 2):
            img.putpixel((x + mx, y + h - 2), rgb(mouth))


def humanoid(rng, skin, body, legs, arms=None, hair=None, eyes=0x222222, single_eye=False, alpha=255, mouth=None):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    skin_c, body_c, legs_c = rgb(skin, alpha), rgb(body, alpha), rgb(legs, alpha)
    head = paint_box(img, 0, 0, 8, 8, 8, skin_c, rng, 8,
                     faces={"top": rgb(hair, alpha) if hair else skin_c, "back": rgb(hair, alpha) if hair else skin_c})
    if hair:
        # Hair over the sides and the top rows of the face.
        for name in ("right", "left"):
            x, y, w, h = head[name]
            fill_rect(img, x, y, w, 5, rgb(hair, alpha), rng, 10)
        x, y, w, h = head["front"]
        fill_rect(img, x, y, w, 2, rgb(hair, alpha), rng, 10)
    face(img, head, (1, 5), eyes, mouth, rng, eye_row=4 if hair else 3, single_eye=single_eye)
    paint_box(img, 16, 16, 8, 12, 4, body_c, rng, 10)
    paint_box(img, 40, 16, 4, 12, 4, rgb(arms, alpha) if arms else skin_c, rng, 8)
    paint_box(img, 0, 16, 4, 12, 4, legs_c, rng, 10)
    return img


def satyr(rng):
    img = humanoid(rng, 0xC8956B, 0xC8956B, 0x6B4A2B, hair=0x3E2B1E, mouth=0x8A4B3A)
    # Hooves on the lowest rows of the legs, a little horn on the hat layer.
    for name, (x, y, w, h) in box_faces(0, 16, 4, 12, 4).items():
        if name not in ("top", "bottom"):
            fill_rect(img, x, y + h - 2, w, 2, rgb(0x2A1C12), rng, 4)
    hat = box_faces(32, 0, 8, 8, 8)
    x, y, w, h = hat["top"]
    for dx, dy in ((1, 1), (6, 1), (1, 2), (6, 2)):
        img.putpixel((x + dx, y + dy), rgb(0xD8CBB0))
    return img


def harpy(rng):
    img = humanoid(rng, 0xE2C3A4, 0x5B4636, 0xD89A3A, arms=0x6E5640, hair=0x2B1E16, eyes=0xC0392B)
    for u in (0, 24):
        faces = box_faces(u, 32, 1, 12, 8)
        for name, (x, y, w, h) in faces.items():
            fill_rect(img, x, y, w, h, rgb(0x6E5640), rng, 14)
            if name in ("right", "left"):
                for j in range(0, h, 3):
                    for i in range(w):
                        img.putpixel((x + i, y + j), rgb(0x8B6A45))
                fill_rect(img, x, y + h - 3, w, 3, rgb(0xC9A66B), rng, 8)
    return img


def shade(rng):
    img = humanoid(rng, 0xBFD6E3, 0x8EA3B5, 0x6F8394, eyes=0x0A0F14, alpha=150)
    x, y, w, h = box_faces(0, 0, 8, 8, 8)["front"]
    for ex in (1, 2, 5, 6):
        for ey in (3, 4):
            img.putpixel((x + ex, y + ey), (10, 15, 20, 230))
    return img


def cyclops(rng):
    img = humanoid(rng, 0xB08A63, 0x6B4A2B, 0xB08A63, hair=0x4E3B2A, eyes=0x3B5E2B, single_eye=True, mouth=0x5A3A2A)
    # Loincloth: only the lower part of the body is leather, the chest is bare skin.
    for name, (x, y, w, h) in box_faces(16, 16, 8, 12, 4).items():
        if name not in ("top", "bottom"):
            fill_rect(img, x, y, w, 7, rgb(0xB08A63), rng, 8)
    return img


def medusa(rng):
    img = humanoid(rng, 0x9DB884, 0xD4B85A, 0xC2A64A, arms=0x9DB884, hair=0x3F6B2E, eyes=0xE8D44D)
    # Snakes on the hat layer.
    for name, (x, y, w, h) in box_faces(32, 0, 8, 8, 8).items():
        for i in range(w):
            for j in range(h):
                if (i + j) % 3 == 0 or (name == "top"):
                    img.putpixel((x + i, y + j), jitter(rgb(0x4F7A3A), rng, 18))
                elif (i * 7 + j) % 5 == 0:
                    img.putpixel((x + i, y + j), rgb(0xB3D16A))
    for name in ("front",):
        x, y, w, h = box_faces(32, 0, 8, 8, 8)[name]
        for i in range(w):
            for j in range(2, h):
                img.putpixel((x + i, y + j), (0, 0, 0, 0))
    return img


def minotaur(rng):
    img = humanoid(rng, 0x4A2E1E, 0x5C3A26, 0x3B2416, arms=0x5C3A26, eyes=0xC0392B)
    paint_box(img, 0, 32, 6, 2, 2, rgb(0xE8DCC0), rng, 6)
    paint_box(img, 0, 36, 6, 2, 2, rgb(0xE8DCC0), rng, 6)
    faces = paint_box(img, 16, 32, 5, 3, 2, rgb(0x7A5640), rng, 6)
    x, y, w, h = faces["front"]
    img.putpixel((x + 1, y + 1), rgb(0x1A100A))
    img.putpixel((x + 3, y + 1), rgb(0x1A100A))
    # A bronze belt.
    for name, (x, y, w, h) in box_faces(16, 16, 8, 12, 4).items():
        if name not in ("top", "bottom"):
            fill_rect(img, x, y + 8, w, 2, rgb(0xB07A2E), rng, 8)
    return img


def spartoi(rng):
    img = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    bone = rgb(0xD8D3C4)
    head = paint_box(img, 0, 0, 8, 8, 8, bone, rng, 8)
    x, y, w, h = head["front"]
    for ex in (1, 2, 5, 6):
        for ey in (3, 4):
            img.putpixel((x + ex, y + ey), rgb(0x1A1A1A))
    for mx in range(2, 6, 1):
        img.putpixel((x + mx, y + 6), rgb(0x3A3A3A) if mx % 2 else bone)
    for name, (x, y, w, h) in box_faces(16, 16, 8, 12, 4).items():
        for j in range(h):
            for i in range(w):
                rib = name in ("front", "back") and j < 8 and j % 2 == 1 and 1 <= i < w - 1
                if not rib:
                    img.putpixel((x + i, y + j), jitter(bone, rng, 8))
    paint_box(img, 40, 16, 2, 12, 2, bone, rng, 8)
    paint_box(img, 0, 16, 2, 12, 2, bone, rng, 8)
    return img


def pegasus(rng):
    img = Image.new("RGBA", (64, 64))
    fill_rect(img, 0, 0, 64, 64, rgb(0xF4F1EA), rng, 8)
    for _ in range(40):
        img.putpixel((rng.randrange(64), rng.randrange(64)), rgb(0xE6C35C))
    return img


def beast(rng, fur, snout, eyes, mane=None, heads=1, tw=64):
    img = Image.new("RGBA", (tw, 64), (0, 0, 0, 0))
    fur_c = rgb(fur)
    paint_box(img, 0, 0, 10, 10, 18, fur_c, rng, 12)
    paint_box(img, 0, 44, 4, 10, 4, fur_c, rng, 12)
    paint_box(img, 16, 44, 2, 2, 10, rgb(mane if mane else fur), rng, 12)
    head = paint_box(img, 32, 28, 7, 7, 6, fur_c, rng, 12)
    x, y, w, h = head["front"]
    for ex in (1, 5):
        img.putpixel((x + ex, y + 2), rgb(eyes))
    nose = paint_box(img, 40, 44, 4, 3, 3, rgb(snout), rng, 8)
    x, y, w, h = nose["front"]
    fill_rect(img, x + 1, y, 2, 1, rgb(0x1A100A), rng, 0)
    if mane:
        paint_box(img, 0, 28, 10, 10, 4, rgb(mane), rng, 16)
    return img


def hydra(rng):
    img = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    scales = rgb(0x2F5D3A)
    body = paint_box(img, 0, 0, 16, 12, 20, scales, rng, 16, faces={"bottom": rgb(0x8BA86A)})
    paint_box(img, 0, 32, 6, 8, 6, scales, rng, 16)
    paint_box(img, 0, 46, 4, 4, 14, scales, rng, 16)
    paint_box(img, 72, 0, 3, 14, 3, rgb(0x3C7D46), rng, 14)
    head = paint_box(img, 72, 20, 5, 5, 7, rgb(0x3C7D46), rng, 14)
    x, y, w, h = head["front"]
    img.putpixel((x + 1, y + 1), rgb(0xE8D44D))
    img.putpixel((x + 3, y + 1), rgb(0xE8D44D))
    fill_rect(img, x, y + 3, w, 1, rgb(0x7A1C1C), rng, 0)
    # Spines along the back.
    x, y, w, h = body["top"]
    for j in range(0, h, 3):
        fill_rect(img, x + w // 2 - 1, y + j, 2, 1, rgb(0x8BC34A), rng, 0)
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
    "nemean_lion": lambda rng: beast(rng, 0xC9962E, 0xE0B870, 0x2A1C12, mane=0x8A5A1C),
    "cerberus": lambda rng: beast(rng, 0x241E1E, 0x3A2E2E, 0xFF4A1C),
    "hydra": hydra,
}

BLOCKS = {
    "marble": marble,
    "marble_bricks": marble_bricks,
    "marble_pillar": marble_pillar_side,
    "marble_pillar_top": marble_pillar_top,
    "olympian_marble": olympian_marble,
    "asphodel": asphodel,
    "hellas_portal": hellas_portal,
}
