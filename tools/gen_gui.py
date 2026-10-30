"""Textures of the Codex of Myths and of the HUD of the myths, drawn with Pillow at twice the GUI scale (each GUI
pixel is 2x2 texture pixels, so they stay sharp at the usual GUI scales).

textures/gui/codex.png          the open book, 292x186 GUI pixels
textures/gui/codex_widgets.png  arrows, lock, frames of the map steps and ornaments (layout in WIDGETS)
textures/gui/hud.png            frames of the bars, the level medallion and the world scroll (layout in HUD)
Java: codex/client/CodexScreen.java, core/client/MythHud.java.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "mythsofworlds", "textures", "gui")
S = 2  # texture pixels per GUI pixel

LEATHER = (92, 38, 24)
LEATHER_DARK = (52, 20, 14)
GOLD = (226, 179, 60)
GOLD_LIGHT = (255, 226, 132)
GOLD_DARK = (138, 96, 30)
PARCHMENT = (238, 222, 184)
PARCHMENT_EDGE = (206, 178, 128)
INK = (70, 44, 24)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def noise_fill(img, box, base, amount, rng, alpha=255):
    x0, y0, x1, y1 = box
    px = img.load()
    for y in range(y0, y1):
        for x in range(x0, x1):
            d = rng.randint(-amount, amount)
            px[x, y] = (max(0, min(255, base[0] + d)), max(0, min(255, base[1] + d)), max(0, min(255, base[2] + d)), alpha)


def scroll_curl(d, x, y, r, colour, dark):
    """A small spiral flourish, the motif of the frames."""
    pts = []
    for i in range(40):
        a = i / 40 * math.pi * 3.2
        rr = r * (1 - i / 48)
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    d.line(pts, fill=dark, width=3)
    d.line(pts, fill=colour, width=1)


def flourish_corner(d, x, y, fx, fy, size):
    """Gold filigree in a corner: a quarter-circle vine with curls; fx, fy flip it towards the corner."""
    for k, r in enumerate((size, size * 0.62)):
        pts = []
        for i in range(30):
            a = i / 29 * math.pi / 2
            pts.append((x + fx * (r - math.cos(a) * r), y + fy * (r - math.sin(a) * r)))
        d.line(pts, fill=GOLD_DARK, width=4 if k == 0 else 3)
        d.line(pts, fill=GOLD if k == 0 else GOLD_LIGHT, width=2 if k == 0 else 1)
    scroll_curl(d, x + fx * size * 0.95, y + fy * size * 0.25, size * 0.22, GOLD_LIGHT, GOLD_DARK)
    scroll_curl(d, x + fx * size * 0.25, y + fy * size * 0.95, size * 0.22, GOLD_LIGHT, GOLD_DARK)
    d.ellipse([x + fx * 4 - 4, y + fy * 4 - 4, x + fx * 4 + 4, y + fy * 4 + 4], fill=GOLD_LIGHT, outline=GOLD_DARK)


def meander(d, x0, x1, y, colour, dark, step=8):
    """A thin Greek key band, the ornament under the titles."""
    d.line([(x0, y), (x1, y)], fill=dark, width=1)
    d.line([(x0, y + step), (x1, y + step)], fill=dark, width=1)
    x = x0 + 2
    while x + step <= x1 - 2:
        d.line([(x, y + step - 2), (x, y + 2), (x + step - 3, y + 2), (x + step - 3, y + step - 4), (x + 3, y + step - 4),
                (x + 3, y + 5)], fill=colour, width=1)
        x += step


def book():
    w, h = 292 * S, 186 * S
    rng = random.Random("codex")
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Leather cover with rounded corners and tooled border.
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=14, fill=LEATHER_DARK + (255,))
    d.rounded_rectangle([3, 3, w - 4, h - 4], radius=12, fill=LEATHER + (255,))
    cover = Image.new("RGBA", (w, h))
    noise_fill(cover, (0, 0, w, h), LEATHER, 9, rng)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([3, 3, w - 4, h - 4], radius=12, fill=255)
    img.paste(cover, (0, 0), mask)
    d.rounded_rectangle([8, 8, w - 9, h - 9], radius=9, outline=GOLD_DARK, width=2)
    # Page block: stacked page edges, then the two pages.
    for i in range(4, 0, -1):
        c = lerp(PARCHMENT_EDGE, (150, 120, 80), i / 5)
        d.rectangle([18 - i, 14 + i, w - 19 + i, h - 13 + i], fill=c + (255,))
    pages = Image.new("RGBA", (w, h))
    pd = pages.load()
    cx = w // 2
    for y in range(14, h - 13):
        for x in range(18, w - 18):
            # Darker towards the outer edges and much darker in the gutter, like a curved page.
            t_out = min(x - 18, w - 19 - x) / 60
            t_gut = abs(x - cx) / 26
            shade = 1.0 - 0.10 * max(0.0, 1 - t_out) - 0.22 * max(0.0, 1 - t_gut)
            n = rng.randint(-5, 5)
            base = PARCHMENT
            pd[x, y] = (int(base[0] * shade) + n, int(base[1] * shade) + n, int(base[2] * shade) + n, 255)
    img.alpha_composite(pages.crop((0, 0, w, h)), (0, 0))
    # Stains and fibres of old parchment.
    for _ in range(14):
        x, y = rng.randint(30, w - 30), rng.randint(24, h - 24)
        r = rng.randint(6, 18)
        stain = Image.new("RGBA", (w, h))
        ImageDraw.Draw(stain).ellipse([x - r, y - r, x + r, y + r], fill=(160, 120, 70, 18))
        img.alpha_composite(stain.filter(ImageFilter.GaussianBlur(4)))
    d = ImageDraw.Draw(img)
    # Gutter line and the ribbon bookmark.
    d.line([(cx, 12), (cx, h - 12)], fill=(150, 116, 74), width=2)
    d.polygon([(cx - 4, 12), (cx + 4, 12), (cx + 4, h), (cx, h - 6), (cx - 4, h)], fill=(140, 28, 30))
    d.line([(cx - 3, 12), (cx - 3, h - 3)], fill=(180, 52, 50))
    # Gold filigree in the four corners of the cover.
    for fx, fy, x, y in ((1, 1, 5, 5), (-1, 1, w - 6, 5), (1, -1, 5, h - 6), (-1, -1, w - 6, h - 6)):
        flourish_corner(d, x, y, fx, fy, 30)
    # Thin double frame on each page.
    for x0, x1 in ((24, cx - 10), (cx + 10, w - 24)):
        d.rectangle([x0, 20, x1, h - 20], outline=(176, 138, 84), width=1)
        d.rectangle([x0 + 3, 23, x1 - 3, h - 23], outline=(196, 160, 104), width=1)
    img.save(os.path.join(ROOT, "codex.png"))


# name: (x, y, w, h) in GUI pixels inside codex_widgets.png (texture is twice as large).
WIDGETS = {
    "next": (0, 0, 18, 10), "next_hover": (0, 10, 18, 10),
    "prev": (18, 0, 18, 10), "prev_hover": (18, 10, 18, 10),
    "back": (36, 0, 14, 12), "back_hover": (36, 12, 14, 12),
    "lock": (50, 0, 9, 11),
    "step_done": (60, 0, 22, 22), "step_todo": (82, 0, 22, 22), "step_locked": (104, 0, 22, 22),
    "ornament": (0, 24, 110, 7),
    "row_hover": (0, 32, 114, 12),
}


def widgets():
    img = Image.new("RGBA", (128 * S, 64 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def box(name):
        x, y, w, h = WIDGETS[name]
        return x * S, y * S, w * S, h * S

    def arrow(name, colour, flip):
        x, y, w, h = box(name)
        pts = [(4, 8), (22, 8), (22, 2), (34, 10), (22, 18), (22, 12), (4, 12)]
        if flip:
            pts = [(w - px, py) for px, py in pts]
        d.polygon([(x + px + 1, y + py + 1) for px, py in pts], fill=(60, 34, 16, 160))
        d.polygon([(x + px, y + py) for px, py in pts], fill=colour, outline=GOLD_DARK)
    for name, flip in (("next", False), ("prev", True)):
        arrow(name, (176, 128, 60), flip)
        arrow(name + "_hover", GOLD_LIGHT, flip)
    for name, colour in (("back", (176, 128, 60)), ("back_hover", GOLD_LIGHT)):
        x, y, w, h = box(name)
        d.arc([x + 4, y + 4, x + w - 4, y + h + 6], 180, 360, fill=GOLD_DARK, width=5)
        d.arc([x + 4, y + 4, x + w - 4, y + h + 6], 180, 360, fill=colour, width=3)
        d.polygon([(x + 0, y + 14), (x + 10, y + 14), (x + 5, y + 22)], fill=colour, outline=GOLD_DARK)
    x, y, w, h = box("lock")
    d.arc([x + 3, y + 1, x + w - 3, y + 14], 180, 360, fill=(90, 90, 96), width=3)
    d.rounded_rectangle([x + 1, y + 9, x + w - 2, y + h - 1], radius=2, fill=(150, 120, 60), outline=(70, 50, 20))
    d.rectangle([x + w // 2 - 1, y + 13, x + w // 2, y + 17], fill=(40, 26, 12))
    for name, ring, inner in (("step_done", GOLD, (255, 236, 170)), ("step_todo", (150, 130, 100), (226, 212, 180)),
                              ("step_locked", (110, 100, 90), (170, 160, 150))):
        x, y, w, h = box(name)
        d.ellipse([x + 1, y + 1, x + w - 2, y + h - 2], fill=lerp(ring, (0, 0, 0), 0.45) + (255,))
        d.ellipse([x + 3, y + 3, x + w - 4, y + h - 4], fill=ring + (255,))
        d.ellipse([x + 6, y + 6, x + w - 7, y + h - 7], fill=inner + (255,))
        if name == "step_done":
            for a in range(0, 360, 45):
                r = math.radians(a)
                cx, cy = x + w / 2, y + h / 2
                d.line([(cx + math.cos(r) * 17, cy + math.sin(r) * 17), (cx + math.cos(r) * 21, cy + math.sin(r) * 21)],
                       fill=GOLD_LIGHT, width=2)
    x, y, w, h = box("ornament")
    cy = y + h // 2
    d.line([(x + 6, cy), (x + w - 6, cy)], fill=(150, 110, 60), width=2)
    for side in (1, -1):
        cx0 = x + w // 2
        scroll_curl(d, cx0 + side * 26, cy, 6, (196, 150, 70), (120, 84, 40))
        scroll_curl(d, cx0 + side * 70, cy, 5, (196, 150, 70), (120, 84, 40))
    d.polygon([(x + w // 2, cy - 6), (x + w // 2 + 6, cy), (x + w // 2, cy + 6), (x + w // 2 - 6, cy)], fill=GOLD,
              outline=GOLD_DARK)
    x, y, w, h = box("row_hover")
    hover = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for i in range(w):
        a = int(70 * math.sin(math.pi * i / (w - 1)))
        ImageDraw.Draw(hover).line([(i, 0), (i, h - 1)], fill=(200, 150, 60, a))
    img.alpha_composite(hover, (x, y))
    img.save(os.path.join(ROOT, "codex_widgets.png"))


# name: (x, y, w, h) in GUI pixels inside hud.png.
HUD = {
    "bar": (0, 0, 85, 13),          # frame of the health, armour, food and air bars (81x9 inside, at 2,2)
    "xp": (0, 13, 186, 9),          # frame of the experience bar (182x5 inside, at 2,2)
    "medallion": (0, 22, 24, 16),   # behind the level number
    "scroll": (24, 22, 104, 18),    # the world's name
    "heart": (86, 0, 9, 9), "shield": (95, 0, 9, 9), "drumstick": (104, 0, 9, 9), "bubble": (113, 0, 9, 9),
}


def hud():
    img = Image.new("RGBA", (128 * S, 48 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    def box(name):
        x, y, w, h = HUD[name]
        return x * S, y * S, w * S, h * S

    def frame(name):
        x, y, w, h = box(name)
        d.rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=5, fill=(28, 18, 12, 200), outline=GOLD_DARK, width=2)
        d.rounded_rectangle([x + 2, y + 2, x + w - 3, y + h - 3], radius=4, outline=GOLD, width=1)
        # Filigree caps at both ends.
        for fx, ex in ((1, x + 1), (-1, x + w - 2)):
            d.line([(ex, y + h // 2), (ex + fx * 3, y + 1), (ex + fx * 7, y + 1)], fill=GOLD_LIGHT, width=1)
            d.line([(ex, y + h // 2), (ex + fx * 3, y + h - 2), (ex + fx * 7, y + h - 2)], fill=GOLD_LIGHT, width=1)
        # Clear the inside: the bar is filled by code.
        ix, iy = x + 2 * S, y + 2 * S
        d.rectangle([ix, iy, x + w - 2 * S - 1, y + h - 2 * S - 1], fill=(20, 12, 8, 170))
    frame("bar")
    frame("xp")
    x, y, w, h = box("medallion")
    d.polygon([(x + w // 2, y), (x + w - 1, y + h // 2), (x + w // 2, y + h - 1), (x, y + h // 2)], fill=GOLD_DARK)
    d.polygon([(x + w // 2, y + 3), (x + w - 5, y + h // 2), (x + w // 2, y + h - 4), (x + 4, y + h // 2)], fill=(40, 26, 14))
    d.line([(x + w // 2, y + 3), (x + w - 5, y + h // 2), (x + w // 2, y + h - 4), (x + 4, y + h // 2), (x + w // 2, y + 3)],
           fill=GOLD_LIGHT, width=1)
    # The scroll: a parchment band with rolled ends.
    x, y, w, h = box("scroll")
    rng = random.Random("scroll")
    noise_fill(img, (x + 10, y + 6, x + w - 10, y + h - 6), PARCHMENT, 6, rng)
    d.rectangle([x + 10, y + 6, x + w - 11, y + h - 7], outline=PARCHMENT_EDGE)
    for ex in (x + 1, x + w - 15):
        d.rounded_rectangle([ex, y + 2, ex + 13, y + h - 3], radius=6, fill=(214, 186, 132), outline=(120, 90, 50))
        d.line([(ex + 6, y + 5), (ex + 6, y + h - 6)], fill=(170, 136, 86))
    d.line([(x + 14, y + 9), (x + w - 15, y + 9)], fill=GOLD_DARK)
    d.line([(x + 14, y + h - 10), (x + w - 15, y + h - 10)], fill=GOLD_DARK)

    def icon(name, draw):
        x, y, w, h = box(name)
        draw(x, y, w, h)
    icon("heart", lambda x, y, w, h: (d.polygon([(x + 9, y + 16), (x + 1, y + 7), (x + 1, y + 3), (x + 4, y + 1),
                                                  (x + 9, y + 4), (x + 14, y + 1), (x + 17, y + 3), (x + 17, y + 7)],
                                                 fill=(210, 30, 40), outline=(90, 10, 16)),
                                      d.line([(x + 4, y + 4), (x + 6, y + 3)], fill=(255, 170, 170), width=2)))
    icon("shield", lambda x, y, w, h: (d.polygon([(x + 2, y + 2), (x + 16, y + 2), (x + 16, y + 9), (x + 9, y + 17),
                                                   (x + 2, y + 9)], fill=(190, 196, 206), outline=(70, 74, 86)),
                                       d.line([(x + 9, y + 3), (x + 9, y + 15)], fill=GOLD, width=2)))
    icon("drumstick", lambda x, y, w, h: (d.ellipse([x + 5, y + 1, x + 17, y + 12], fill=(176, 96, 40), outline=(90, 44, 16)),
                                          d.line([(x + 7, y + 10), (x + 2, y + 16)], fill=(236, 226, 206), width=3)))
    icon("bubble", lambda x, y, w, h: (d.ellipse([x + 2, y + 2, x + 16, y + 16], fill=(120, 180, 240, 200), outline=(40, 80, 150)),
                                       d.ellipse([x + 5, y + 5, x + 8, y + 8], fill=(240, 250, 255))))
    img.save(os.path.join(ROOT, "hud.png"))


def main():
    os.makedirs(ROOT, exist_ok=True)
    book()
    widgets()
    hud()


if __name__ == "__main__":
    main()
