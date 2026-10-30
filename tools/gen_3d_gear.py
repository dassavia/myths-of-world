"""Turns the held weapons and tools into solid 3D models, built from their own 32x32 icons.

Vanilla extrudes an item icon into a sheet one pixel thick. Here every icon becomes a stack of boxes that grows
thicker towards the middle of the shape: the edge of a blade stays thin and sharp, its spine, the guard, the head
of a hammer or an axe are thick, so the weapon has a real body in the hand, on the ground and in an item frame.
Seen straight on, as in the inventory, the front of the stack is exactly the icon.

Each layer of the stack is cut into as few rectangles as possible (greedy meshing), so a sword is a few dozen boxes.
Run after the asset generators and hd_textures.py: it overwrites the item models of the held gear.
"""
import json
import os

from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "mythsofworlds")

METALS = ["orichalcum", "bulat", "dark_iron"]
TOOLS = ["sword", "axe", "pickaxe", "shovel", "hoe"]
RELICS = ["harpe", "kladenets", "mjolnir", "surtr_sword", "bident_of_hades", "nemean_claw_dagger"]
GEAR = [f"{metal}_{tool}" for metal in METALS for tool in TOOLS] + RELICS

# Half the thickness, in model units (16 per item), of each layer: the silhouette, then the pixels at least
# one, two and three pixels away from its edge. Heavy heads (hammers) get one more step.
DEPTH = [0.3, 0.75, 1.1, 1.4]
HEAVY = {"mjolnir": [0.3, 0.8, 1.3, 1.8, 2.2]}

# The transforms of minecraft:item/handheld and item/generated, written out because a model with its own boxes
# cannot inherit from item/generated (that parent would replace the boxes with the flat sheet).
DISPLAY = {
    "thirdperson_righthand": {"rotation": [0, -90, 55], "translation": [0, 4.0, 0.5], "scale": [0.85, 0.85, 0.85]},
    "thirdperson_lefthand": {"rotation": [0, 90, -55], "translation": [0, 4.0, 0.5], "scale": [0.85, 0.85, 0.85]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]},
    "fixed": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [1, 1, 1]},
    "gui": {"rotation": [0, 0, 0], "translation": [0, 0, 0], "scale": [1, 1, 1]},
}


def edge_distance(alpha, w, h):
    """How many pixels each opaque pixel lies inside the shape (1 on the edge), counting four neighbours."""
    inf = w + h
    dist = [[inf if alpha[y][x] else 0 for x in range(w)] for y in range(h)]
    changed = True
    while changed:
        changed = False
        for y in range(h):
            for x in range(w):
                if not dist[y][x]:
                    continue
                best = 1
                if x > 0 and y > 0 and x < w - 1 and y < h - 1:
                    best = 1 + min(dist[y][x - 1], dist[y][x + 1], dist[y - 1][x], dist[y + 1][x])
                if best < dist[y][x]:
                    dist[y][x] = best
                    changed = True
    return dist


def rectangles(mask, w, h):
    """Greedy meshing: covers the set pixels with few rectangles (x0, y0, x1, y1), ends exclusive."""
    used = [[False] * w for _ in range(h)]
    rects = []
    for y in range(h):
        for x in range(w):
            if not mask[y][x] or used[y][x]:
                continue
            x1 = x
            while x1 < w and mask[y][x1] and not used[y][x1]:
                x1 += 1
            y1 = y + 1
            while y1 < h and all(mask[y1][i] and not used[y1][i] for i in range(x, x1)):
                y1 += 1
            for j in range(y, y1):
                for i in range(x, x1):
                    used[j][i] = True
            rects.append((x, y, x1, y1))
    return rects


def r(v):
    return round(v, 4)


def element(rect, half, px):
    """One box of the stack. Model y grows upwards, the texture's v downwards; u and v run 0..16."""
    x0, y0, x1, y1 = rect
    u0, u1 = x0 * px, x1 * px
    v0, v1 = y0 * px, y1 * px
    z0, z1 = 8 - half, 8 + half
    return {
        "from": [r(u0), r(16 - v1), r(z0)],
        "to": [r(u1), r(16 - v0), r(z1)],
        "faces": {
            "south": {"uv": [r(u0), r(v0), r(u1), r(v1)], "texture": "#icon"},
            "north": {"uv": [r(u1), r(v0), r(u0), r(v1)], "texture": "#icon"},
            # The sides are painted with the outermost row or column of pixels, stretched over the thickness.
            "west": {"uv": [r(u0), r(v0), r(u0 + px), r(v1)], "texture": "#icon"},
            "east": {"uv": [r(u1 - px), r(v0), r(u1), r(v1)], "texture": "#icon"},
            "up": {"uv": [r(u0), r(v0), r(u1), r(v0 + px)], "texture": "#icon"},
            "down": {"uv": [r(u0), r(v1 - px), r(u1), r(v1)], "texture": "#icon"},
        },
    }


def model(name):
    img = Image.open(os.path.join(ROOT, "textures", "item", name + ".png")).convert("RGBA")
    w, h = img.size
    px = 16 / w
    alpha = [[img.getpixel((x, y))[3] > 40 for x in range(w)] for y in range(h)]
    dist = edge_distance(alpha, w, h)
    depths = HEAVY.get(name, DEPTH)
    elements = []
    for layer, half in enumerate(depths):
        mask = [[dist[y][x] > layer for x in range(w)] for y in range(h)]
        for rect in rectangles(mask, w, h):
            elements.append(element(rect, half, px))
    return {
        "gui_light": "front",
        "textures": {"icon": f"mythsofworlds:item/{name}", "particle": f"mythsofworlds:item/{name}"},
        "elements": elements,
        "display": DISPLAY,
    }


def main():
    for name in GEAR:
        data = model(name)
        path = os.path.join(ROOT, "models", "item", name + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"))
            f.write("\n")
        print(f"{name}: {len(data['elements'])} boxes")


if __name__ == "__main__":
    main()
