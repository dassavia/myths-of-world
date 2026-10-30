"""Doubles the resolution of the mod's textures: 16x16 blocks and items become 32x32, entity skins and armour layers
twice their size (the models keep their UV layout, so a texture of twice the size simply has finer pixels).

The generators draw at the base resolution; run this after them (and after gen_hd_gear.py, whose icons are drawn at
32x32 already and are left alone). Each upscaled PNG is marked in its metadata, so running it twice does nothing.

How each kind is enlarged:
* items: Scale2x (smooths diagonal edges without blurring), the dark outline thinned to one fine pixel, and a soft
  bevel lit from the top left that makes the icon look carved;
* blocks: Scale2x, a light bump from the brightness of the texture and a fine grain;
* entities and armour: plain doubling, with a fine grain only inside flat areas, so faces and small details keep
  exactly their drawing.
"""
import glob
import os
import random
import sys

from PIL import Image, ImageFilter
from PIL.PngImagePlugin import PngInfo

ROOT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "mythsofworlds", "textures")
MARK = "mythsofworlds:hd"
# Textures that are already drawn at full resolution or must keep their size.
SKIP_DIRS = {"gui"}


def is_marked(img):
    return img.info.get(MARK) == "1"


def save_marked(img, path):
    info = PngInfo()
    info.add_text(MARK, "1")
    img.save(path, pnginfo=info)


def scale2x(img):
    """AdvMAME2x / Scale2x on RGBA pixels."""
    w, h = img.size
    src = img.load()
    out = Image.new("RGBA", (w * 2, h * 2))
    dst = out.load()

    def p(x, y):
        return src[min(w - 1, max(0, x)), min(h - 1, max(0, y))]
    for y in range(h):
        for x in range(w):
            e = src[x, y]
            b, d, f, hh = p(x, y - 1), p(x - 1, y), p(x + 1, y), p(x, y + 1)
            e0 = e1 = e2 = e3 = e
            if b != hh and d != f:
                e0 = d if d == b else e
                e1 = f if b == f else e
                e2 = d if d == hh else e
                e3 = f if hh == f else e
            dst[2 * x, 2 * y] = e0
            dst[2 * x + 1, 2 * y] = e1
            dst[2 * x, 2 * y + 1] = e2
            dst[2 * x + 1, 2 * y + 1] = e3
    return out


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def clamp(v):
    return max(0, min(255, int(v)))


def shade(c, f, add=0):
    return (clamp(c[0] * f + add), clamp(c[1] * f + add), clamp(c[2] * f + add), c[3])


def thin_outline(small, big):
    """At 16px an outline pixel is a dark rim around the icon; doubled it would be two pixels thick. Keep only the
    half that touches the outside and give the inner half the colour of the neighbouring interior."""
    w, h = small.size
    s = small.load()
    b = big.load()

    def opaque(x, y):
        return 0 <= x < w and 0 <= y < h and s[x, y][3] > 0
    for y in range(h):
        for x in range(w):
            c = s[x, y]
            if c[3] == 0:
                continue
            outside = [(dx, dy) for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)) if not opaque(x + dx, y + dy)]
            if not outside or lum(c) > 70:
                continue
            # Interior neighbour: the brightest opaque neighbour.
            inner = [s[x + dx, y + dy] for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)) if opaque(x + dx, y + dy)]
            inner = [n for n in inner if lum(n) > lum(c) + 25]
            if not inner:
                continue
            fill = max(inner, key=lum)
            mixed = tuple(int(c[i] * 0.35 + fill[i] * 0.65) for i in range(3)) + (255,)
            for sx in (0, 1):
                for sy in (0, 1):
                    # The sub-pixel faces the outside if it lies on the side of a transparent neighbour.
                    faces_out = any((dx == -1 and sx == 0) or (dx == 1 and sx == 1) or (dy == -1 and sy == 0)
                                    or (dy == 1 and sy == 1) for dx, dy in outside)
                    if not faces_out:
                        b[2 * x + sx, 2 * y + sy] = mixed


def bevel(img, strength=0.16):
    """Soft carved light: brighter towards the top-left rim of the shape, darker towards the bottom-right."""
    w, h = img.size
    alpha = img.getchannel("A")
    depth = alpha.filter(ImageFilter.GaussianBlur(1.6))
    d = depth.load()
    px = img.load()
    for y in range(h):
        for x in range(w):
            c = px[x, y]
            if c[3] == 0:
                continue
            gx = d[min(w - 1, x + 1), y] - d[max(0, x - 1), y]
            gy = d[x, min(h - 1, y + 1)] - d[x, max(0, y - 1)]
            light = (gx + gy) / 255.0  # positive where the shape rises towards the bottom right: lit from top left
            px[x, y] = shade(c, 1.0 + strength * max(-1.0, min(1.0, light)))


def bump(img, rng, strength=0.10, grain=4):
    w, h = img.size
    px = img.load()
    height = img.convert("L").filter(ImageFilter.GaussianBlur(0.8))
    hp = height.load()
    for y in range(h):
        for x in range(w):
            c = px[x, y]
            if c[3] == 0:
                continue
            gx = hp[(x + 1) % w, y] - hp[(x - 1) % w, y]
            gy = hp[x, (y + 1) % h] - hp[x, (y - 1) % h]
            light = -(gx + gy) / 255.0
            px[x, y] = shade(c, 1.0 + strength * max(-1.0, min(1.0, light * 2)), rng.randint(-grain, grain))


def grain_flat(small, big, rng, grain=3):
    """Fine grain only where a pixel and its four neighbours are the same colour."""
    w, h = small.size
    s = small.load()
    b = big.load()
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            c = s[x, y]
            if c[3] < 255 or any(s[x + dx, y + dy] != c for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))):
                continue
            for sx in (0, 1):
                for sy in (0, 1):
                    b[2 * x + sx, 2 * y + sy] = shade(c, 1.0, rng.randint(-grain, grain))


def upscale(path, kind):
    img = Image.open(path).convert("RGBA")
    if is_marked(Image.open(path)):
        return False
    rng = random.Random(os.path.basename(path))
    w, h = img.size
    if kind == "item":
        if w >= 32:
            return False
        big = scale2x(img)
        thin_outline(img, big)
        bevel(big)
    elif kind == "block":
        if w >= 32:
            return False
        # Animated strips (portals) are a column of frames: enlarge frame by frame.
        frames = [img.crop((0, i * w, w, (i + 1) * w)) for i in range(h // w)]
        big = Image.new("RGBA", (w * 2, h * 2))
        for i, frame in enumerate(frames):
            f = scale2x(frame)
            bump(f, rng)
            big.paste(f, (0, i * w * 2))
    else:
        big = img.resize((w * 2, h * 2), Image.NEAREST)
        grain_flat(img, big, rng)
    save_marked(big, path)
    return True


def main():
    done = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.png"), recursive=True)):
        rel = os.path.relpath(path, ROOT)
        folder = rel.split(os.sep)[0]
        if folder in SKIP_DIRS:
            continue
        kind = "item" if folder == "item" else "block" if folder == "block" else "entity"
        if upscale(path, kind):
            done += 1
            if "-v" in sys.argv:
                print("hd", rel)
    print(f"{done} textures enlarged")


if __name__ == "__main__":
    main()
