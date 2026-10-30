"""The block textures, drawn at 32x32: stone, marble and bricks, the ores and metal blocks, the woods and leaves of
the myths, the braziers, runestones, clouds and the hollow of the World Tree.

Each texture tiles: the noise wraps around the edges. Colours come from small ramps (art32.ramp), so the blocks keep
the flat tones of pixel art instead of photographic noise. Run after hd_textures.py, like gen_art32_items.py.
"""
import math
import os
import random
import sys
import zlib

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from art32 import ramp  # noqa: E402
from hd_textures import save_marked  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "mythsofworlds", "textures",
                    "block")
N = 32
BLOCKS = {}


def block(name):
    def wrap(fn):
        BLOCKS[name] = fn
        return fn
    return wrap


# ---------------------------------------------------------------- noise and tones

def value_noise(seed, cell, n=N):
    """Tileable value noise with cells of {@code cell} pixels, in [0, 1]."""
    rng = np.random.default_rng(zlib.crc32(str(seed).encode()))
    g = n // cell
    grid = rng.random((g, g))
    ys, xs = np.mgrid[0:n, 0:n] / cell
    x0, y0 = np.floor(xs).astype(int), np.floor(ys).astype(int)
    fx, fy = xs - x0, ys - y0
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = grid[y0 % g, x0 % g]
    b = grid[y0 % g, (x0 + 1) % g]
    c = grid[(y0 + 1) % g, x0 % g]
    d = grid[(y0 + 1) % g, (x0 + 1) % g]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def fbm(seed, cells=(16, 8, 4, 2), weights=(0.45, 0.3, 0.17, 0.08)):
    out = sum(w * value_noise(f"{seed}:{c}", c) for c, w in zip(cells, weights))
    return (out - out.min()) / max(1e-6, out.max() - out.min())


def paint(values, tones, alpha=None):
    """Picks a tone of the ramp for each value in [0, 1]."""
    idx = np.clip((values * len(tones)).astype(int), 0, len(tones) - 1)
    img = Image.new("RGBA", (N, N))
    px = img.load()
    for y in range(N):
        for x in range(N):
            a = 255 if alpha is None else int(alpha[y, x])
            px[x, y] = (*tones[idx[y, x]], a)
    return img


def tones(base, steps=6, spread=0.42):
    return ramp(base, steps=steps, spread=spread)


def put(img, x, y, colour):
    img.putpixel((x % N, y % N), (*colour[:3], colour[3] if len(colour) > 3 else 255))


def walk(rng, start, steps, drift=(0, 1), wobble=1):
    """A wandering line of pixels (veins, cracks)."""
    x, y = start
    pts = []
    for _ in range(steps):
        pts.append((x % N, y % N))
        x += drift[0] + rng.choice(range(-wobble, wobble + 1))
        y += drift[1]
    return pts


# ---------------------------------------------------------------- stone and marble

def stone_values(seed, contrast=1.0):
    v = fbm(seed, cells=(16, 8, 4, 2), weights=(0.3, 0.3, 0.25, 0.15))
    return np.clip(0.5 + (v - 0.5) * 1.05 * contrast, 0, 0.999)


def stone(seed="stone", base=0x7E7E80):
    return paint(stone_values(seed), tones(base, spread=0.36))


def marble(seed="marble", base=0xECE8E1, vein=0xB4AEA4, veins=3):
    rng = random.Random(seed)
    v = 0.55 + (fbm(seed, cells=(16, 8)) - 0.5) * 0.5
    img = paint(np.clip(v, 0, 0.999), tones(base, steps=4, spread=0.12))
    vt = tones(vein, steps=3, spread=0.2)
    for k in range(veins):
        for i, (x, y) in enumerate(walk(rng, (rng.randrange(N), 0), N, drift=(rng.choice((-1, 1)) * 0, 1))):
            put(img, x, y, vt[1 if i % 7 else 0])
            if rng.random() < 0.25:
                put(img, x + 1, y, vt[2])
    return img


@block("marble")
def _():
    return marble()


@block("olympian_marble")
def _():
    img = marble("olympian", base=0xF2EEE6, veins=2)
    gold = tones(0xE2B33C, steps=5)
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - 15.5, y - 15.5)
            if 8.5 <= r < 11.5:
                k = 4 if (x + y) < 28 and r < 10 else 3 if r < 10.5 else 1
                put(img, x, y, gold[k])
            elif 11.5 <= r < 12.5:
                put(img, x, y, gold[0])
    for k in range(8):
        a = k * math.pi / 4
        put(img, int(15.5 + 10 * math.cos(a)), int(15.5 + 10 * math.sin(a)), (255, 244, 200))
    return img


def bricks(seed, base, mortar, rows=4, cols=2, img=None, bevel=True, jitter=0.12):
    """Running bond bricks with a light top-left edge and a shadow on the bottom right."""
    rng = random.Random(seed)
    t = tones(base, steps=6, spread=0.4)
    mt = tones(mortar, steps=3, spread=0.2)
    noise = fbm(seed)
    out = Image.new("RGBA", (N, N))
    px = out.load()
    h = N // rows
    w = N // cols
    shade = {}
    for y in range(N):
        row = y // h
        off = (w // 2) * (row % 2)
        for x in range(N):
            col = ((x + off) % N) // w
            key = (row, col)
            if key not in shade:
                shade[key] = rng.uniform(-jitter, jitter)
            yy, xx = y % h, (x + off) % w
            if yy == h - 1 or xx == w - 1:
                px[x, y] = (*mt[1 if (x + y) % 3 else 0], 255)
                continue
            v = 0.5 + shade[key] + (noise[y, x] - 0.5) * 0.5
            if bevel:
                if yy == 0 or xx == 0:
                    v += 0.22
                elif yy == h - 2 or xx == w - 2:
                    v -= 0.22
            px[x, y] = (*t[int(np.clip(v, 0, 0.999) * len(t))], 255)
    return out


@block("marble_bricks")
def _():
    img = marble("marble_bricks_base", veins=2)
    br = bricks("marble_bricks", 0xE6E1D8, 0xA8A39A, rows=4, cols=2, jitter=0.06)
    # Keep the marble's veins inside the bricks: blend the vein pixels in.
    for y in range(N):
        for x in range(N):
            m = img.getpixel((x, y))
            b = br.getpixel((x, y))
            if sum(m[:3]) < 600 and sum(b[:3]) > 560:
                br.putpixel((x, y), tuple((m[i] + b[i]) // 2 for i in range(3)) + (255,))
    return br


@block("marble_pillar")
def _():
    t = tones(0xECE8E1, steps=5, spread=0.2)
    img = Image.new("RGBA", (N, N))
    noise = fbm("pillar", cells=(16, 8))
    for y in range(N):
        for x in range(N):
            k = x % 8
            v = 0.62 + (noise[y, x] - 0.5) * 0.15
            v += {0: -0.35, 1: 0.18, 2: 0.12, 6: -0.1, 7: -0.2}.get(k, 0)
            img.putpixel((x, y), (*t[int(np.clip(v, 0, 0.999) * 5)], 255))
    return img


@block("marble_pillar_top")
def _():
    img = marble("pillar_top", veins=1)
    t = tones(0xD8D2C8, steps=4, spread=0.25)
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - 15.5, y - 15.5)
            for ring, k in ((14.5, 0), (10.5, 1), (6.5, 2)):
                if ring <= r < ring + 1:
                    img.putpixel((x, y), (*t[k], 255))
            if x in (0, N - 1) or y in (0, N - 1):
                img.putpixel((x, y), (*t[1], 255))
    return img


def labyrinth(seed, variant=None):
    img = bricks(seed, 0x5E5A56, 0x34302C, rows=4, cols=2)
    rng = random.Random(seed + "x")
    if variant == "cracked":
        dark = (38, 34, 30)
        for _ in range(4):
            for x, y in walk(rng, (rng.randrange(N), rng.randrange(N)), rng.randint(6, 12),
                             drift=(rng.choice((-1, 1)), 1)):
                put(img, x, y, dark)
    if variant == "mossy":
        moss = fbm(seed + "moss", cells=(8, 4, 2), weights=(0.5, 0.35, 0.15))
        grad = np.mgrid[0:N, 0:N][0] / N
        mt = tones(0x4E7A2E, steps=4, spread=0.35)
        for y in range(N):
            for x in range(N):
                m = moss[y, x] * 0.8 + grad[y, x] * 0.45
                if m > 0.68:
                    put(img, x, y, mt[min(3, int((m - 0.68) * 14))])
    # Faded meander carvings: the labyrinth's mark.
    if variant is None:
        mark = tones(0x8A4A2A, steps=3)
        for x0, y0 in ((4, 3), (20, 19)):
            for dx, dy in ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (2, 2), (1, 2), (1, 3), (1, 4), (2, 4),
                           (3, 4), (4, 4)):
                put(img, x0 + dx, y0 + dy, mark[1])
    return img


@block("labyrinth_bricks")
def _():
    return labyrinth("labyrinth")


@block("cracked_labyrinth_bricks")
def _():
    return labyrinth("labyrinth_cracked", "cracked")


@block("mossy_labyrinth_bricks")
def _():
    return labyrinth("labyrinth_mossy", "mossy")


# ---------------------------------------------------------------- ores and metal blocks

def ore(seed, base, ore_colour, clusters=4, stone_base=0x7E7E80, glow=False):
    rng = random.Random(seed)
    img = stone(seed, stone_base)
    ot = tones(ore_colour, steps=5, spread=0.48)
    outline = tuple(int(c * 0.45) for c in ot[0])
    taken = []
    while len(taken) < clusters:
        cx, cy = rng.randrange(3, N - 3), rng.randrange(3, N - 3)
        if all(math.hypot(cx - x, cy - y) > 9 for x, y in taken):
            taken.append((cx, cy))
    for cx, cy in taken:
        r = rng.uniform(1.6, 2.4)
        pts = {(x, y) for x in range(cx - 3, cx + 4) for y in range(cy - 3, cy + 4)
               if math.hypot(x - cx, (y - cy) * 1.15) <= r + rng.uniform(-0.4, 0.4)}
        ring = {(x + dx, y + dy) for x, y in pts for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))} - pts
        for x, y in ring:
            put(img, x, y, outline if not glow else tuple(min(255, int(c * 0.8)) for c in ot[0]))
        for x, y in pts:
            k = 2 + (1 if (x - cx) + (y - cy) < 0 else 0) - (1 if (x - cx) + (y - cy) > 1 else 0)
            put(img, x, y, ot[k])
        put(img, min(pts)[0], min(pts)[1], ot[4])
    return img


@block("orichalcum_ore")
def _():
    return ore("orichalcum_ore", 0x7E7E80, 0xDC8A3E)


@block("bulat_ore")
def _():
    return ore("bulat_ore", 0x7E7E80, 0xB7C8DA)


@block("dark_iron_ore")
def _():
    return ore("dark_iron_ore", 0x4A4A50, 0x7A8494, stone_base=0x55555C)


@block("hephaestus_coal_ore")
def _():
    return ore("hephaestus_coal_ore", 0x7E7E80, 0xF06A1E, clusters=6, glow=True)


@block("muspel_ember_ore")
def _():
    return ore("muspel_ember_ore", 0x3A3436, 0xF2A23A, clusters=5, stone_base=0x3E3638, glow=True)


def metal_block(seed, base, accent):
    t = tones(base, steps=6, spread=0.45)
    at = tones(accent, steps=4, spread=0.4)
    noise = fbm(seed, cells=(8, 4), weights=(0.6, 0.4))
    img = Image.new("RGBA", (N, N))
    for y in range(N):
        for x in range(N):
            # Four plates, each bevelled: light on top and left, dark on the bottom and right.
            px, py = x % 16, y % 16
            v = 0.55 + (noise[y, x] - 0.5) * 0.18 - (px + py) / 64
            if px == 0 or py == 0:
                v = 0.92
            elif px == 15 or py == 15:
                v = 0.05
            elif px == 1 or py == 1:
                v += 0.18
            elif px == 14 or py == 14:
                v -= 0.18
            img.putpixel((x, y), (*t[int(np.clip(v, 0, 0.999) * 6)], 255))
    for ox in (0, 16):
        for oy in (0, 16):
            for rx, ry in ((3, 3), (12, 3), (3, 12), (12, 12)):
                put(img, ox + rx, oy + ry, t[5])
                put(img, ox + rx + 1, oy + ry + 1, t[1])
                put(img, ox + rx + 1, oy + ry, t[3])
                put(img, ox + rx, oy + ry + 1, t[3])
            for dx, dy in ((7, 6), (8, 6), (6, 7), (9, 7), (6, 8), (9, 8), (7, 9), (8, 9)):
                put(img, ox + dx, oy + dy, at[1])
            for dx, dy in ((7, 7), (8, 7), (7, 8), (8, 8)):
                put(img, ox + dx, oy + dy, at[3] if (dx, dy) == (7, 7) else at[2])
    return img


@block("orichalcum_block")
def _():
    return metal_block("orichalcum_block", 0xDC8A3E, 0x3CC0A0)


@block("bulat_block")
def _():
    return metal_block("bulat_block", 0xB7C2CE, 0x9ADCF2)


@block("dark_iron_block")
def _():
    return metal_block("dark_iron_block", 0x5A6070, 0x4FC8F0)


# ---------------------------------------------------------------- wood and leaves

@block("ironwood_log")
def _():
    t = tones(0x4A3E36, steps=6, spread=0.4)
    noise = fbm("ironwood_bark", cells=(16, 8, 4), weights=(0.3, 0.4, 0.3))
    img = Image.new("RGBA", (N, N))
    for y in range(N):
        for x in range(N):
            ridge = math.sin((x + 1.5 * math.sin(y / 7)) * math.pi / 4)
            v = 0.5 + ridge * 0.25 + (noise[y, x] - 0.5) * 0.5
            img.putpixel((x, y), (*t[int(np.clip(v, 0, 0.999) * 6)], 255))
    rng = random.Random("ironwood_rust")
    rust = tones(0x9A5A2A, steps=3)
    for _ in range(6):
        x, y = rng.randrange(N), rng.randrange(N)
        for k in range(rng.randint(2, 4)):
            put(img, x, y + k, rust[k % 3])
    return img


@block("ironwood_log_top")
def _():
    t = tones(0x8A6A4A, steps=5, spread=0.35)
    bark = tones(0x4A3E36, steps=4, spread=0.35)
    img = Image.new("RGBA", (N, N))
    noise = fbm("ironwood_top", cells=(8, 4))
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - 15.5, y - 15.5) + (noise[y, x] - 0.5) * 1.5
            if x in (0, N - 1) or y in (0, N - 1) or r > 15.5:
                c = bark[1 + (x + y) % 2]
            else:
                c = t[2 + (1 if int(r) % 3 == 0 else 0) - (1 if int(r) % 3 == 2 else 0)]
            img.putpixel((x, y), (*c, 255))
    return img


@block("ironwood_planks")
def _():
    t = tones(0x7A5A40, steps=6, spread=0.38)
    noise = fbm("ironwood_planks", cells=(16, 4, 2), weights=(0.3, 0.4, 0.3))
    img = Image.new("RGBA", (N, N))
    rng = random.Random("planks")
    shades = [rng.uniform(-0.1, 0.1) for _ in range(4)]
    for y in range(N):
        board = y // 8
        for x in range(N):
            v = 0.5 + shades[board] + (noise[y, x] - 0.5) * 0.35 + 0.08 * math.sin(x * 0.7 + board * 2)
            if y % 8 == 7:
                v = 0.02
            elif y % 8 == 0:
                v += 0.18
            seam = (board % 2) * 16 + 7
            if x == seam:
                v = 0.05
            img.putpixel((x, y), (*t[int(np.clip(v, 0, 0.999) * 6)], 255))
    for board in range(4):
        for x in ((board % 2) * 16 + 2, (board % 2) * 16 + 12):
            put(img, x, board * 8 + 3, (70, 74, 82))
            put(img, x, board * 8 + 4, (40, 42, 48))
    return img


def leaves(seed, base, fruit=None, fruit_count=6, holes=0.16):
    t = tones(base, steps=5, spread=0.45)
    clusters = fbm(seed, cells=(8, 4, 2), weights=(0.45, 0.35, 0.2))
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    for y in range(N):
        for x in range(N):
            v = clusters[y, x]
            if v < holes + 0.14:
                continue
            # Lighter on the top left of each clump of leaves.
            k = int(np.clip(v * 4.4 + ((x + y) % 7 == 0) * 0.4, 0, 4))
            img.putpixel((x, y), (*t[k], 255))
    if fruit:
        rng = random.Random(seed + "fruit")
        ft = tones(fruit, steps=4, spread=0.42)
        spots = []
        while len(spots) < fruit_count:
            x, y = rng.randrange(1, N - 2), rng.randrange(1, N - 2)
            if all(abs(x - a) + abs(y - b) > 6 for a, b in spots):
                spots.append((x, y))
        for x, y in spots:
            for dx, dy, k in ((0, 0, 3), (1, 0, 2), (0, 1, 2), (1, 1, 1), (-1, 0, 1), (0, -1, 2), (2, 1, 0),
                              (1, 2, 0)):
                put(img, x + dx, y + dy, ft[k])
            put(img, x, y - 1, (90, 60, 30))
    return img


@block("olive_leaves")
def _():
    return leaves("olive", 0x7A9A5A)


@block("olive_leaves_ripe")
def _():
    return leaves("olive", 0x7A9A5A, fruit=0x3E2E4E)


@block("pomegranate_leaves")
def _():
    return leaves("pomegranate", 0x3E7A2E)


@block("pomegranate_leaves_ripe")
def _():
    return leaves("pomegranate", 0x3E7A2E, fruit=0xC0262E, fruit_count=5)


@block("idunn_leaves")
def _():
    return leaves("idunn", 0x5A9A3A)


@block("idunn_leaves_ripe")
def _():
    return leaves("idunn", 0x5A9A3A, fruit=0xF2C232, fruit_count=5)


@block("golden_leaves")
def _():
    img = leaves("golden", 0xE2B33C, holes=0.2)
    rng = random.Random("golden_glint")
    for _ in range(10):
        x, y = rng.randrange(N), rng.randrange(N)
        if img.getpixel((x, y))[3]:
            put(img, x, y, (255, 246, 200))
    return img


@block("ironwood_leaves")
def _():
    return leaves("ironwood", 0x2E4A3A, holes=0.22)


@block("asphodel")
def _():
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    stem = tones(0x5A8A3A, steps=3)
    petal = tones(0xF2EEE4, steps=4, spread=0.25)
    rng = random.Random("asphodel")
    for x0, top in ((10, 8), (16, 4), (22, 9)):
        for y in range(top + 3, N):
            put(img, x0 + (1 if y > 24 and x0 != 16 else 0) * (1 if x0 > 16 else -1) * ((y - 24) // 3), y, stem[1])
        for k in range(5):
            fx, fy = x0 + rng.choice((-2, 2)), top + k * 3
            for dx, dy, c in ((0, 0, 2), (1, 0, 3), (-1, 0, 1), (0, 1, 1), (0, -1, 3)):
                put(img, fx + dx, fy + dy, petal[c])
            put(img, fx, fy, (230, 200, 120))
    for x0, y0 in ((7, 26), (24, 25), (13, 28)):
        for k in range(4):
            put(img, x0 + k, y0 - k // 2, stem[2])
    return img


# ---------------------------------------------------------------- myths

@block("brazier_side")
def _():
    t = tones(0xB07A3A, steps=6, spread=0.45)
    img = Image.new("RGBA", (N, N))
    noise = fbm("brazier", cells=(8, 4))
    for y in range(N):
        for x in range(N):
            v = 0.55 + (noise[y, x] - 0.5) * 0.25 - y / 80
            if y < 3:
                v = 0.85 - y * 0.15
            elif y > N - 3:
                v = 0.15
            elif (y - 3) % 9 == 0:
                v = 0.2
            img.putpixel((x, y), (*t[int(np.clip(v, 0, 0.999) * 6)], 255))
    gold = tones(0xE8B43C, steps=4)
    for x in range(N):
        put(img, x, 14, gold[3])
        put(img, x, 18, gold[1])
        if x % 4 == 1:
            put(img, x, 16, gold[2])
            put(img, x + 1, 16, gold[3])
    return img


def brazier_top(lit):
    t = tones(0xB07A3A, steps=5, spread=0.45)
    coal = tones(0x2A2426, steps=4, spread=0.3)
    fire = tones(0xF07A1E, steps=4, spread=0.45)
    noise = fbm("brazier_top_" + str(lit), cells=(4, 2), weights=(0.6, 0.4))
    img = Image.new("RGBA", (N, N))
    for y in range(N):
        for x in range(N):
            edge = min(x, y, N - 1 - x, N - 1 - y)
            if edge < 3:
                c = t[4 - edge if edge < 2 else 1]
            elif lit and noise[y, x] > 0.55:
                c = fire[min(3, int((noise[y, x] - 0.55) * 9))]
            else:
                c = coal[int(noise[y, x] * 3.99)]
            img.putpixel((x, y), (*c, 255))
    return img


@block("brazier_top")
def _():
    return brazier_top(False)


@block("brazier_top_lit")
def _():
    return brazier_top(True)


RUNES = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 1), (2, 0), (1, 3), (2, 2)],  # fehu-like
    [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (0, 1), (2, 1), (0, 2), (2, 2)],  # algiz-like
    [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (2, 1), (2, 3), (3, 0), (3, 4)],
    [(0, 0), (1, 1), (2, 2), (2, 3), (1, 4), (0, 5), (2, 0), (2, 1), (2, 4), (2, 5)],
]


def runestone(seed, glow):
    img = stone(seed, 0x5A5E6A)
    carve = tones(0x56D2F2, steps=4) if glow else tones(0x24262E, steps=3, spread=0.2)
    for (x0, y0), rune in zip(((4, 4), (20, 3), (6, 19), (21, 20)), RUNES):
        for dx, dy in rune:
            for sx, sy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                put(img, x0 + dx * 2 + sx, y0 + dy * 2 + sy, carve[2 if glow and (sx + sy) == 0 else 1])
    return img


@block("runestone")
def _():
    return runestone("runestone", False)


@block("carved_runestone")
def _():
    return runestone("carved_runestone", True)


@block("cloud")
def _():
    v = fbm("cloud", cells=(16, 8, 4), weights=(0.5, 0.35, 0.15))
    t = tones(0xF2F4FA, steps=4, spread=0.12)
    alpha = 190 + v * 60
    return paint(np.clip(0.3 + v * 0.7, 0, 0.999), t, alpha=alpha)


@block("scorched_earth")
def _():
    img = paint(stone_values("scorched", 0.8), tones(0x3A2E2A, spread=0.3))
    rng = random.Random("scorched")
    ember = tones(0xF06A1E, steps=4)
    for _ in range(5):
        pts = walk(rng, (rng.randrange(N), rng.randrange(N)), rng.randint(5, 10), drift=(rng.choice((-1, 1)), 1))
        for i, (x, y) in enumerate(pts):
            put(img, x, y, (20, 14, 12))
            if i % 3 == 1:
                put(img, x, y, ember[2])
    return img


@block("world_tree_hollow")
def _():
    t = tones(0x6A4A30, steps=6, spread=0.42)
    noise = fbm("world_tree_bark", cells=(16, 8, 4), weights=(0.3, 0.4, 0.3))
    img = Image.new("RGBA", (N, N))
    dark = tones(0x140C10, steps=3, spread=0.2)
    rng = random.Random("hollow")
    for y in range(N):
        for x in range(N):
            r = ((x - 15.5) / 9) ** 2 + ((y - 17) / 12) ** 2
            if r < 1:
                c = dark[0 if r < 0.6 else 1]
            else:
                ridge = math.sin((x + 2 * math.sin(y / 4)) * math.pi / 3.5)
                v = 0.5 + ridge * 0.22 + (noise[y, x] - 0.5) * 0.45 - (0.25 if r < 1.35 else 0)
                c = t[int(np.clip(v, 0, 0.999) * 6)]
            img.putpixel((x, y), (*c, 255))
    for _ in range(9):
        a, rr = rng.uniform(0, 2 * math.pi), rng.uniform(0, 0.8)
        put(img, int(15.5 + 9 * rr * math.cos(a)), int(17 + 12 * rr * math.sin(a)), (120, 220, 255))
    return img


def main(names):
    for name in names or sorted(BLOCKS):
        save_marked(BLOCKS[name](), os.path.join(ROOT, name + ".png"))
    print(f"blocks: {len(names or BLOCKS)} drawn at 32x32")


if __name__ == "__main__":
    main(sys.argv[1:])
