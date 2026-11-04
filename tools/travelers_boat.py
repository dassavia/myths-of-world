"""The traveller's boat (EgyptianContent.TRAVELERS_BOAT): its entity texture on the vanilla boat model's layout
(textures/entity/boat/travelers_boat.png, 128x64 painted at twice the resolution) and its 32x32 item icon. A skiff of
bundled papyrus: golden reeds bound with dark cords, a band of lapis and gold along the gunwale, paddles with blue
blades. Run: python3 tools/travelers_boat.py
"""
import os
import random

from PIL import Image, ImageDraw
from PIL.PngImagePlugin import PngInfo

ROOT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "mythsofworlds", "textures")
K = 2
REED, REED_LIGHT, REED_DARK = (196, 170, 92), (226, 204, 128), (140, 116, 56)
CORD = (78, 52, 30)
LAPIS, GOLD, GOLD_LIGHT = (42, 90, 176), (226, 179, 60), (255, 227, 138)
WOOD, WOOD_DARK = (122, 84, 48), (88, 58, 32)


def faces(u, v, w, h, d):
    u, v, w, h, d = u * K, v * K, w * K, h * K, d * K
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}


def save(img, path):
    info = PngInfo()
    info.add_text("mythsofworlds:hd", "1")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, pnginfo=info)


def reeds(img, rect, rng, along_x=True, cords=12, light=1.0):
    """Bundled papyrus: reeds running along the boat, bound by dark cords every few texels."""
    x, y, w, h = rect
    px = img.load()
    for j in range(h):
        for i in range(w):
            k = j if along_x else i
            c = REED_LIGHT if k % 4 == 0 else REED_DARK if k % 4 == 3 else REED
            n = rng.randint(-6, 6)
            c = tuple(max(0, min(255, int(v * light) + n)) for v in c)
            if cords and (i if along_x else j) % cords in (0, 1):
                c = CORD
            px[x + i, y + j] = c + (255,)


def gunwale(img, rect):
    """A painted band along the top edge: lapis with a thin gold line."""
    x, y, w, h = rect
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w - 1, y + 2], fill=LAPIS + (255,))
    d.line([x, y + 3, x + w - 1, y + 3], fill=GOLD + (255,))


def entity(rng):
    img = Image.new("RGBA", (128 * K, 64 * K), (0, 0, 0, 0))
    bottom = faces(0, 0, 28, 16, 3)
    for name, rect in bottom.items():
        reeds(img, rect, rng, along_x=name not in ("right", "left"), light=0.9 if name == "bottom" else 1.0)
    for v, w in ((19, 18), (27, 16), (35, 28), (43, 28)):
        for name, rect in faces(0, v, w, 6, 2).items():
            reeds(img, rect, rng, along_x=name in ("front", "back", "top", "bottom"), cords=10)
            if name in ("front", "back"):
                gunwale(img, rect)
    for v in (0, 20):                                         # the paddles: a wooden shaft, a blue blade with gold edge
        shaft = faces(62, v, 2, 2, 18)
        for rect in shaft.values():
            x, y, w, h = rect
            ImageDraw.Draw(img).rectangle([x, y, x + w - 1, y + h - 1], fill=WOOD + (255,))
            for i in range(0, w, 6):
                ImageDraw.Draw(img).line([x + i, y, x + i, y + h - 1], fill=WOOD_DARK + (255,))
        blade = faces(62, v, 1, 6, 7)
        for rect in blade.values():
            x, y, w, h = rect
            ImageDraw.Draw(img).rectangle([x, y, x + w - 1, y + h - 1], fill=LAPIS + (255,), outline=GOLD + (255,))
    return img


def icon():
    """32x32: the skiff from the side, prow and stern curling up to golden lotus tips, a linen sail on a mast."""
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    outline = (48, 30, 16, 255)
    d.line([16, 6, 16, 22], fill=WOOD_DARK + (255,), width=1)          # the mast
    d.polygon([(17, 7), (25, 10), (24, 19), (17, 20)], fill=(242, 236, 220, 255), outline=(170, 160, 140, 255))  # the sail
    d.line([18, 12, 23, 13], fill=(210, 200, 180, 255))
    hull = [(3, 15), (6, 21), (10, 24), (22, 24), (26, 21), (29, 15), (27, 15), (24, 19), (8, 19), (5, 15)]
    d.polygon(hull, fill=REED + (255,), outline=outline)
    for x in (9, 13, 17, 21, 25):                                     # the cords binding the bundles
        d.line([x, 19, x - 1, 24], fill=CORD + (255,))
    d.line([8, 20, 24, 20], fill=LAPIS + (255,))
    d.line([9, 21, 23, 21], fill=GOLD + (255,))
    for x, y in ((3, 14), (29, 14)):                                  # the lotus tips
        d.ellipse([x - 1, y - 2, x + 1, y], fill=GOLD_LIGHT + (255,), outline=GOLD + (255,))
    d.line([10, 23, 22, 23], fill=REED_DARK + (255,))
    return img


def main():
    rng = random.Random("travelers_boat")
    save(entity(rng), os.path.join(ROOT, "entity", "boat", "travelers_boat.png"))
    save(icon(), os.path.join(ROOT, "item", "travelers_boat.png"))


if __name__ == "__main__":
    main()
