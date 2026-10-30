"""A small pixel-art renderer for the 32x32 icons and blocks of the mod (used by gen_art32_items.py and
gen_art32_blocks.py).

An icon is a stack of shapes (polygons, ellipses, strokes) given in the coordinates of the 32x32 grid. Each shape has
a material, a colour ramp from deep shadow to highlight. Rendering:

* every shape is rasterised from a 4x supersampled mask, so diagonals step cleanly one pixel at a time;
* a height field is built per shape (the distance to its edge, capped at its bevel, or a dome for round shapes) and
  lit from the top left, which gives each part its own volume;
* the light picks a tone from the ramp, with an optional pattern (wood grain, scales, fur, noise) on top;
* where a shape lies over another, its lower and right edges get a dark line so the parts read apart;
* finally a one-pixel outline is drawn around the silhouette, in the darkest tone of the material it touches,
  lighter on the lit side (selective outline), and the brightest pixels may get a glint.
"""
import colorsys
import math
import random

import numpy as np
from PIL import Image, ImageDraw

N = 32
SS = 4
LIGHT = np.array([-0.55, -0.7, 0.45])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def hexrgb(value):
    return ((value >> 16) & 255, (value >> 8) & 255, value & 255)


def ramp(base, steps=7, spread=0.5, hue_shift=0.045):
    """A colour ramp around {@code base}: shadows go cooler and more saturated, lights warmer and paler."""
    if isinstance(base, int):
        base = hexrgb(base)
    h, l, s = colorsys.rgb_to_hls(*(c / 255 for c in base))
    out = []
    for i in range(steps):
        t = i / (steps - 1) * 2 - 1  # -1 shadow .. 1 light
        target = 0.13 if t > 0 else 0.72  # lights lean to warm yellow, shadows to cool violet
        diff = ((target - h + 0.5) % 1.0) - 0.5
        hh = (h + diff * min(1.0, hue_shift * 4 * abs(t)) * (s > 0.08)) % 1.0
        ll = min(0.97, max(0.04, l + t * spread * (0.55 if t > 0 else 0.6) * (1.0 if l < 0.75 else 0.6)))
        ss = min(1.0, max(0.0, s * (1 + (-0.25 * t if t > 0 else -0.15 * t))))
        r, g, b = colorsys.hls_to_rgb(hh, ll, ss)
        out.append((int(r * 255), int(g * 255), int(b * 255)))
    return out


class Material:
    def __init__(self, base, spread=0.5, outline=None, glint=True, hue_shift=0.045, flat=False):
        self.tones = ramp(base, spread=spread, hue_shift=hue_shift)
        o = self.tones[0]
        self.outline = outline or (int(o[0] * 0.55), int(o[1] * 0.5), int(o[2] * 0.6))
        self.glint = glint
        self.flat = flat

    def tone(self, value):
        """Tone for a light value in [0, 1]."""
        i = int(round(max(0.0, min(1.0, value)) * (len(self.tones) - 1)))
        return self.tones[i]


def mat(base, **kw):
    return Material(base, **kw)


def _distance(mask):
    """City-block distance of each pixel inside {@code mask} to the outside (two-pass chamfer)."""
    h, w = mask.shape
    big = 99
    d = np.where(mask, big, 0).astype(np.int32)
    for y in range(h):
        for x in range(w):
            if d[y, x]:
                up = d[y - 1, x] if y else 0
                left = d[y, x - 1] if x else 0
                d[y, x] = min(d[y, x], up + 1, left + 1)
    for y in range(h - 1, -1, -1):
        for x in range(w - 1, -1, -1):
            if d[y, x]:
                down = d[y + 1, x] if y < h - 1 else 0
                right = d[y, x + 1] if x < w - 1 else 0
                d[y, x] = min(d[y, x], down + 1, right + 1)
    return d


class Shape:
    def __init__(self, mask, material, bevel=2.5, dome=None, pattern=None, base=0.55, contrast=1.0, edge=True,
                 height=None):
        self.mask = mask
        self.material = material
        self.bevel = bevel
        self.dome = dome
        self.pattern = pattern
        self.base = base
        self.contrast = contrast
        self.edge = edge
        self.height = height


class Sprite:
    def __init__(self, seed="sprite", size=N):
        self.size = size
        self.shapes = []
        self.rng = random.Random(seed)
        self.decals = []

    # ---------------------------------------------------------------- shapes

    def _mask(self, draw_fn):
        big = Image.new("L", (self.size * SS, self.size * SS), 0)
        draw_fn(ImageDraw.Draw(big), SS)
        small = big.resize((self.size, self.size), Image.BOX)
        return np.array(small) >= 128

    def poly(self, pts, material, **kw):
        mask = self._mask(lambda d, s: d.polygon([(x * s, y * s) for x, y in pts], fill=255))
        return self.add(mask, material, **kw)

    def ellipse(self, box, material, round_=True, **kw):
        x0, y0, x1, y1 = box
        mask = self._mask(lambda d, s: d.ellipse([x0 * s, y0 * s, x1 * s - 1, y1 * s - 1], fill=255))
        if round_ and "dome" not in kw:
            kw["dome"] = ((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2)
        return self.add(mask, material, **kw)

    def rect(self, box, material, **kw):
        x0, y0, x1, y1 = box
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], material, **kw)

    def stroke(self, pts, width, material, **kw):
        def draw(d, s):
            d.line([(x * s, y * s) for x, y in pts], fill=255, width=max(1, int(width * s)), joint="curve")
            r = width * s / 2
            for x, y in (pts[0], pts[-1]):
                d.ellipse([x * s - r, y * s - r, x * s + r, y * s + r], fill=255)
        return self.add(self._mask(draw), material, **kw)

    def add(self, mask, material, **kw):
        kw.setdefault("bevel", 2.5)
        shape = Shape(mask, material, **kw)
        self.shapes.append(shape)
        return shape

    def pixel(self, x, y, colour):
        """A hand-placed pixel drawn after everything else (an eye, a gem's sparkle)."""
        self.decals.append((x, y, colour))

    # ---------------------------------------------------------------- render

    def render(self, outline=True):
        n = self.size
        colour = np.zeros((n, n, 3), dtype=np.float64)
        alpha = np.zeros((n, n), dtype=bool)
        owner = -np.ones((n, n), dtype=np.int32)
        light_map = np.zeros((n, n))
        ys, xs = np.mgrid[0:n, 0:n]
        for index, shape in enumerate(self.shapes):
            m = shape.mask
            if not m.any():
                continue
            if shape.height is not None:
                height = shape.height(xs + 0.5, ys + 0.5)
            elif shape.dome:
                cx, cy, rx, ry = shape.dome
                u = ((xs + 0.5 - cx) / max(rx, 0.5)) ** 2 + ((ys + 0.5 - cy) / max(ry, 0.5)) ** 2
                height = np.sqrt(np.clip(1 - u, 0, 1)) * max(rx, ry) * 0.9
            else:
                d = _distance(m).astype(np.float64)
                height = np.minimum(d, shape.bevel)
            gy, gx = np.gradient(np.where(m, height, 0.0))
            normal = np.dstack([-gx, -gy, np.ones_like(gx) * 1.0])
            normal /= np.linalg.norm(normal, axis=2, keepdims=True)
            lit = normal @ LIGHT
            value = shape.base + (lit - LIGHT[2]) * 0.9 * shape.contrast
            # A soft top-left to bottom-right gradient over the whole part.
            box = np.argwhere(m)
            (y0, x0), (y1, x1) = box.min(0), box.max(0)
            span = max(1, (x1 - x0) + (y1 - y0))
            value += 0.18 * shape.contrast * (0.5 - ((xs - x0) + (ys - y0)) / span)
            if shape.pattern:
                value = value + shape.pattern(xs, ys, self.rng)
            for y, x in box:
                t = shape.material.tone(value[y, x])
                colour[y, x] = t
                light_map[y, x] = value[y, x]
                alpha[y, x] = True
                owner[y, x] = index
            # Dark seam where this part lies over another, on the side away from the light.
            if shape.edge:
                for y, x in box:
                    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                        ny, nx = y + dy, x + dx
                        if 0 <= nx < n and 0 <= ny < n and not m[ny, nx] and owner[ny, nx] >= 0 \
                                and owner[ny, nx] != index:
                            other = self.shapes[owner[ny, nx]]
                            if dx > 0 or dy > 0:
                                colour[ny, nx] = other.material.tones[0]
                            elif not other.material.flat:
                                colour[ny, nx] = other.material.tones[1]
        # Glints: the brightest pixel of each shiny part.
        for index, shape in enumerate(self.shapes):
            if not shape.material.glint:
                continue
            sel = owner == index
            if sel.sum() < 6:
                continue
            values = np.where(sel, light_map, -9)
            y, x = np.unravel_index(np.argmax(values), values.shape)
            top = shape.material.tones[-1]
            colour[y, x] = tuple(min(255, c + 40) for c in top)
        img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        px = img.load()
        for y in range(n):
            for x in range(n):
                if alpha[y, x]:
                    r, g, b = colour[y, x]
                    px[x, y] = (int(r), int(g), int(b), 255)
        if outline:
            out = []
            for y in range(n):
                for x in range(n):
                    if alpha[y, x]:
                        continue
                    best = None
                    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and alpha[ny, nx]:
                            best = self.shapes[owner[ny, nx]].material.outline
                            # The lit side (top, left) gets a softer outline.
                            if dx > 0 or dy > 0:
                                best = tuple(min(255, int(c * 1.35 + 12)) for c in best)
                            break
                    if best:
                        out.append((x, y, best))
            for x, y, c in out:
                px[x, y] = (*c, 255)
        for x, y, c in self.decals:
            px[x, y] = (*c[:3], c[3] if len(c) > 3 else 255)
        return img


# ---------------------------------------------------------------- patterns

def noise(amount=0.12, seed=0):
    def f(xs, ys, rng):
        r = random.Random(seed)
        return np.array([[r.uniform(-amount, amount) for _ in range(xs.shape[1])] for _ in range(xs.shape[0])])
    return f


def grain(direction=(1, -1), period=3.0, amount=0.14, seed=0):
    """Wood grain: stripes across {@code direction}, wavy, with knots of noise."""
    dx, dy = direction
    norm = math.hypot(dx, dy)

    def f(xs, ys, rng):
        r = random.Random(seed)
        offs = np.array([[r.uniform(-0.6, 0.6) for _ in range(xs.shape[1])] for _ in range(xs.shape[0])])
        across = (xs * -dy + ys * dx) / norm
        along = (xs * dx + ys * dy) / norm
        return amount * np.sin((across + 0.6 * np.sin(along / 3.0) + offs) * 2 * math.pi / period)
    return f


def scales(size=4, amount=0.18):
    def f(xs, ys, rng):
        row = (ys // size).astype(int)
        cx = (xs + (row % 2) * size / 2) % size - size / 2
        cy = ys % size
        return amount * (0.5 - (cx ** 2 + (cy - size * 0.2) ** 2) / (size * size * 0.35))
    return f


def fur(amount=0.16, seed=0, slant=0.6):
    def f(xs, ys, rng):
        r = random.Random(seed)
        strands = np.array([[r.uniform(-1, 1) for _ in range(xs.shape[1] + 8)] for _ in range(xs.shape[0] + 8)])
        out = np.zeros(xs.shape)
        for y in range(xs.shape[0]):
            for x in range(xs.shape[1]):
                out[y, x] = strands[y, x] * 0.5 + strands[y + 1, int(x + slant) + 1] * 0.3 + strands[y + 2, x + 2] * 0.2
        return amount * out
    return f


def bands(axis="y", period=4, amount=0.15, offset=0):
    def f(xs, ys, rng):
        v = ys if axis == "y" else xs
        return amount * np.where(((v + offset) // (period / 2)) % 2 == 0, 1.0, -1.0)
    return f


def combine(*patterns):
    def f(xs, ys, rng):
        return sum(p(xs, ys, rng) for p in patterns)
    return f


# ---------------------------------------------------------------- frames

class Diagonal:
    """Coordinates along the diagonal of a held item: t runs from the bottom-left corner towards the top right, s
    across it (positive to the upper left). Tools and weapons are drawn in this frame."""

    def __init__(self, start=(3.5, 28.5)):
        self.x0, self.y0 = start
        self.u = (1 / math.sqrt(2), -1 / math.sqrt(2))
        self.v = (-1 / math.sqrt(2), -1 / math.sqrt(2))

    def __call__(self, t, s=0.0):
        return (self.x0 + self.u[0] * t + self.v[0] * s, self.y0 + self.u[1] * t + self.v[1] * s)

    def pts(self, pairs):
        return [self(t, s) for t, s in pairs]


def save(img, path):
    img.save(path)
