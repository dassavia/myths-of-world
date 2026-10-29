"""Draws the mod's logo (src/main/resources/mythsofworlds.png): Surtr's flaming sword over the fires of Muspelheim."""
import math
import os
import random

from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources")
SIZE = 256


def main():
    rng = random.Random("logo")
    img = Image.new("RGBA", (SIZE, SIZE))
    centre = SIZE / 2
    for y in range(SIZE):
        for x in range(SIZE):
            # Night over Muspelheim: dark ash above, a red glow of embers rising from below.
            glow = max(0.0, 1.0 - math.hypot(x - centre, y - SIZE * 1.05) / (SIZE * 0.85))
            r = int(24 + 170 * glow ** 1.5)
            g = int(18 + 60 * glow ** 2.5)
            b = int(26 + 10 * glow)
            n = rng.randrange(-6, 6)
            img.putpixel((x, y), (max(0, min(255, r + n)), max(0, min(255, g + n)), max(0, b + n), 255))
    for _ in range(140):                                  # flying sparks
        x, y = rng.randrange(SIZE), rng.randrange(SIZE // 3, SIZE)
        img.putpixel((x, y), (255, rng.randrange(140, 220), 60, 255))
    # Rounded corners, like a launcher icon.
    radius = 28
    for y in range(SIZE):
        for x in range(SIZE):
            cx = min(max(x, radius), SIZE - 1 - radius)
            cy = min(max(y, radius), SIZE - 1 - radius)
            if math.hypot(x - cx, y - cy) > radius:
                img.putpixel((x, y), (0, 0, 0, 0))
    sword = Image.open(os.path.join(ROOT, "assets", "mythsofworlds", "textures", "item", "surtr_sword.png")).convert("RGBA")
    scale = SIZE * 3 // 4 // sword.width
    big = sword.resize((sword.width * scale, sword.height * scale), Image.NEAREST)
    shadow = Image.new("RGBA", big.size, (0, 0, 0, 0))
    for y in range(big.height):
        for x in range(big.width):
            if big.getpixel((x, y))[3] > 0:
                shadow.putpixel((x, y), (255, 120, 20, 90))
    offset = ((SIZE - big.width) // 2, (SIZE - big.height) // 2)
    img.alpha_composite(shadow, (offset[0] + 6, offset[1] + 6))
    img.alpha_composite(big, offset)
    img.save(os.path.join(ROOT, "mythsofworlds.png"))


if __name__ == "__main__":
    main()
