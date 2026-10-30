"""Textures of the HUD of the myths, drawn with Pillow at twice the GUI scale (each GUI
pixel is 2x2 texture pixels, so they stay sharp at the usual GUI scales).

textures/gui/hud.png            frames of the bars and the hotbar, the level medallion and the world scroll (layout in HUD)
textures/gui/inventory.png      the survival inventory, in vanilla's layout (INVENTORY_SLOTS)
Java: core/client/MythHud.java.
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


# name: (x, y, w, h) in GUI pixels inside hud.png.
HUD = {
    "bar": (0, 0, 85, 13),          # frame of the health, armour, food and air bars (81x9 inside, at 2,2)
    "xp": (0, 13, 186, 9),          # frame of the experience bar (182x5 inside, at 2,2)
    "medallion": (0, 22, 24, 16),   # behind the level number
    "scroll": (24, 22, 104, 18),    # the world's name
    "heart": (86, 0, 9, 9), "shield": (95, 0, 9, 9), "drumstick": (104, 0, 9, 9), "bubble": (113, 0, 9, 9),
    "hotbar": (0, 40, 182, 22),     # the nine slots (item i at 3 + 20 * i, 3)
    "selected": (182, 40, 24, 24),  # the frame of the selected slot, drawn one pixel up and left of its cell
    "offhand": (206, 40, 22, 22),   # the off-hand slot (item at 3, 3)
}


def hud():
    img = Image.new("RGBA", (256 * S, 64 * S), (0, 0, 0, 0))
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

    # The hotbar: a dark lacquered band in a gold rim, the slots sunk into it, gold studs between them.
    def slot_cell(cx, cy):
        d.rectangle([cx, cy, cx + 18 * S - 1, cy + 18 * S - 1], fill=(12, 8, 6, 150))
        d.line([(cx, cy), (cx + 18 * S - 1, cy)], fill=(0, 0, 0, 120), width=S)
        d.line([(cx, cy), (cx, cy + 18 * S - 1)], fill=(0, 0, 0, 120), width=S)
        d.line([(cx + 1, cy + 18 * S - 1), (cx + 18 * S - 1, cy + 18 * S - 1)], fill=(226, 179, 60, 70), width=1)
        d.line([(cx + 18 * S - 1, cy + 1), (cx + 18 * S - 1, cy + 18 * S - 1)], fill=(226, 179, 60, 70), width=1)

    def band(name, cells):
        x, y, w, h = box(name)
        d.rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=6, fill=(30, 20, 14, 205), outline=GOLD_DARK, width=2)
        d.rounded_rectangle([x + 2, y + 2, x + w - 3, y + h - 3], radius=5, outline=(226, 179, 60, 150), width=1)
        for i in range(cells):
            slot_cell(x + (2 + 20 * i) * S, y + 2 * S)
            if i:
                sx, sy = x + (20 * i + 1) * S, y + 11 * S
                d.polygon([(sx, sy - 3), (sx + 2, sy - 1), (sx + 2, sy), (sx, sy + 2), (sx - 1, sy), (sx - 1, sy - 1)],
                          fill=GOLD)
    band("hotbar", 9)
    band("offhand", 1)
    x, y, w, h = box("selected")
    d.rounded_rectangle([x, y, x + w - 1, y + h - 1], radius=6, outline=(70, 44, 14, 220), width=4)
    d.rounded_rectangle([x + 1, y + 1, x + w - 2, y + h - 2], radius=5, outline=GOLD_LIGHT, width=2)
    d.rounded_rectangle([x + 4, y + 4, x + w - 5, y + h - 5], radius=4, outline=(255, 226, 132, 90), width=2)
    for cx, cy in ((x + w // 2, y + 1), (x + w // 2, y + h - 2)):
        d.polygon([(cx - 4, cy), (cx, cy - 3), (cx + 4, cy), (cx, cy + 3)], fill=(255, 244, 196), outline=GOLD_DARK)
    img.save(os.path.join(ROOT, "hud.png"))


# The survival inventory, slot for slot where vanilla has it (InventoryScreen, 176x166 of a 256x256 texture).
INVENTORY_SLOTS = ([(8, 8 + 18 * i) for i in range(4)] + [(77, 62)]
                   + [(98 + 18 * c, 18 + 18 * r) for r in range(2) for c in range(2)]
                   + [(8 + 18 * c, 84 + 18 * r) for r in range(3) for c in range(9)]
                   + [(8 + 18 * c, 142) for c in range(9)])


def inventory():
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w, h = 176, 166
    rng = random.Random("inventory")
    # Parchment, a shade darker towards the bottom, with a faint grain.
    body = Image.new("RGBA", (w, h))
    px = body.load()
    for y in range(h):
        base = lerp((236, 225, 198), (220, 204, 168), y / h)
        for x in range(w):
            n = rng.randint(-3, 3)
            px[x, y] = (base[0] + n, base[1] + n, base[2] + n, 255)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=4, fill=255)
    img.paste(body, (0, 0), mask)
    # A dark outline, a gold band lit from the top left, and a thin line inside it.
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=4, outline=(54, 34, 20))
    d.rounded_rectangle([1, 1, w - 2, h - 2], radius=3, outline=(184, 140, 64))
    d.line([(3, 1), (w - 4, 1)], fill=(240, 206, 120))
    d.line([(1, 3), (1, h - 4)], fill=(240, 206, 120))
    d.line([(3, h - 2), (w - 4, h - 2)], fill=(122, 86, 36))
    d.line([(w - 2, 3), (w - 2, h - 4)], fill=(122, 86, 36))
    d.rounded_rectangle([3, 3, w - 4, h - 4], radius=2, outline=(206, 186, 146))
    # The portrait of the hero: a dark niche with an arched top and a gold frame.
    x0, y0, x1, y1 = 25, 7, 76, 79
    d.rounded_rectangle([x0, y0, x1, y1], radius=3, fill=(54, 34, 20))
    for y in range(y0 + 1, y1):
        c = lerp((46, 34, 30), (24, 16, 12), (y - y0) / (y1 - y0))
        d.line([(x0 + 1, y), (x1 - 1, y)], fill=c)
    d.rounded_rectangle([x0, y0, x1, y1], radius=3, outline=(184, 140, 64))
    d.arc([x0 + 4, y0 + 3, x1 - 4, y0 + 40], 180, 360, fill=(120, 88, 40))
    d.line([(x0 + 6, y1 - 4), (x1 - 6, y1 - 4)], fill=(120, 88, 40))
    # The slots: sunk into the parchment, shadow on top and left, light on the bottom and right.
    for sx, sy in INVENTORY_SLOTS:
        x, y = sx - 1, sy - 1
        d.rectangle([x, y, x + 17, y + 17], fill=(150, 128, 98))
        d.line([(x, y), (x + 16, y)], fill=(92, 70, 46))
        d.line([(x, y), (x, y + 16)], fill=(92, 70, 46))
        d.line([(x + 1, y + 17), (x + 17, y + 17)], fill=(250, 240, 216))
        d.line([(x + 17, y + 1), (x + 17, y + 17)], fill=(250, 240, 216))
    # The result slot, larger and framed in gold, and the arrow to it.
    x, y = 150, 24
    d.rectangle([x, y, x + 25, y + 25], fill=(184, 140, 64))
    d.rectangle([x + 1, y + 1, x + 24, y + 24], fill=(150, 128, 98))
    d.line([(x + 1, y + 1), (x + 23, y + 1)], fill=(92, 70, 46))
    d.line([(x + 1, y + 1), (x + 1, y + 23)], fill=(92, 70, 46))
    d.line([(x + 2, y + 24), (x + 24, y + 24)], fill=(250, 240, 216))
    d.line([(x + 24, y + 2), (x + 24, y + 24)], fill=(250, 240, 216))
    ax, ay = 136, 36
    d.polygon([(ax, ay - 2), (ax + 7, ay - 2), (ax + 7, ay - 6), (ax + 13, ay), (ax + 7, ay + 6), (ax + 7, ay + 2),
               (ax, ay + 2)], fill=(184, 140, 64), outline=(122, 86, 36))
    # A gold rule with a small Greek key between the backpack and the hotbar.
    d.line([(8, 139), (167, 139)], fill=(184, 140, 64))
    for x in range(14, 164, 18):
        d.point((x + 3, 140), fill=(122, 86, 36))
    img.save(os.path.join(ROOT, "inventory.png"))


def main():
    os.makedirs(ROOT, exist_ok=True)
    hud()
    inventory()


if __name__ == "__main__":
    main()
