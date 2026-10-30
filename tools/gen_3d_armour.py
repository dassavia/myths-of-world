"""Gives the armour of the myths a shape of its own: crests, pauldrons, horns, wings, fur and chainmail made of real
boxes that stand out of the body, instead of a skin painted flat on the vanilla armour model.

For each armour texture (textures/models/armor/<name>_layer_1.png) this writes armor_models/<name>.json, which lists
the extra boxes, the body part each one hangs on and where its pixels lie in the texture, and paints those pixels into
new rows below it (64x32 becomes 64x64 or taller; the vanilla layout at the top, the vanilla layout, is left untouched).
The client builds the models from the JSON (see ArmourModels.java). Leggings keep the vanilla inner model.

Coordinates are model pixels as in the vanilla HumanoidModel: y grows downwards, the head spans y -8..0 and the
armour around it is 1 pixel thicker. Box sizes are whole pixels (they set the texture layout); "inflate" grows a box
without changing its texture. Works on textures at any multiple of 64x32 (after hd_textures.py they are 128x64).
"""
import json
import os
import random

from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "mythsofworlds")


def box(bone, name, origin, size, paint, inflate=0.0, pivot=(0, 0, 0), rotation=(0, 0, 0)):
    return {"bone": bone, "name": name, "origin": list(origin), "size": list(size), "paint": paint,
            "inflate": inflate, "pivot": list(pivot), "rotation": list(rotation)}


def mirror(part):
    """The same box on the other side of the body (x flipped), for the left arm, leg or side of the head."""
    other = dict(part)
    swap = {"right_arm": "left_arm", "left_arm": "right_arm", "right_leg": "left_leg", "left_leg": "right_leg"}
    other["bone"] = swap.get(part["bone"], part["bone"])
    other["name"] = part["name"].replace("right", "left") if "right" in part["name"] else part["name"] + "_l"
    x, y, z = part["origin"]
    other["origin"] = [-x - part["size"][0], y, z]
    px, py, pz = part["pivot"]
    other["pivot"] = [-px, py, pz]
    rx, ry, rz = part["rotation"]
    other["rotation"] = [rx, -ry, -rz]
    return other


def pair(part):
    return [part, mirror(part)]


# Pauldrons sit over the shoulder: the arm's own origin is at the shoulder joint, the arm spans x -3..1 (right).
def pauldron(paint, size=(6, 3, 7), y=-3.6, inflate=0.0):
    w, h, d = size
    return pair(box("right_arm", "right_pauldron", (-3.6 - (w - 5) / 2, y, -d / 2), size, paint, inflate,
                    rotation=(0, 0, 0.18)))


SPECS = {
    # Hellas: a Corinthian helmet with a horsehair crest, round bronze pauldrons, greaves on the boots.
    "orichalcum": {
        "items": ["orichalcum_helmet", "orichalcum_chestplate", "orichalcum_boots"],
        "parts": [
            box("head", "crest_base", (-1, -10, -5), (2, 1, 10), "gold"),
            box("head", "crest", (-0.5, -14, -6), (1, 4, 13), "crest"),
            box("head", "crest_tail", (-0.5, -11, 7), (1, 6, 1), "crest"),
            *pauldron("metal"),
            *pair(box("right_leg", "right_greave", (-2.5, 6, -3.4), (5, 4, 1), "metal_light")),
        ],
    },
    # Nav: a pointed shishak with a chainmail aventail, layered shoulder plates.
    "bulat": {
        "items": ["bulat_helmet", "bulat_chestplate", "bulat_boots"],
        "parts": [
            box("head", "dome", (-3, -11, -3), (6, 2, 6), "metal"),
            box("head", "dome_top", (-2, -13, -2), (4, 2, 4), "metal_light"),
            box("head", "spire", (-1, -15, -1), (2, 2, 2), "gold"),
            box("head", "spire_tip", (-0.5, -17, -0.5), (1, 2, 1), "gold"),
            box("head", "aventail_back", (-5, -4, 4.4), (10, 7, 1), "chain", 0.1),
            *pair(box("head", "right_aventail", (-5.6, -4, -4), (1, 7, 8), "chain", 0.1)),
            box("head", "nasal", (-0.5, -8, -5.8), (1, 5, 1), "metal_light"),
            *pauldron("metal", (6, 2, 7)),
            *pair(box("right_arm", "right_lame", (-4.2, -1.4, -3.3), (5, 2, 6), "metal_dark", rotation=(0, 0, 0.18))),
        ],
    },
    # Jotunheim: horned dark iron with a nose guard, spiked pauldrons.
    "dark_iron": {
        "items": ["dark_iron_helmet", "dark_iron_chestplate", "dark_iron_boots"],
        "parts": [
            box("head", "nasal", (-0.5, -8, -5.8), (1, 5, 1), "metal_light"),
            box("head", "brow", (-5, -6, -5.6), (10, 1, 1), "metal_light"),
            *pair(box("head", "right_horn", (-8, -9, -1), (3, 2, 2), "bone")),
            *pair(box("head", "right_horn_rise", (-9, -12, -1), (2, 3, 2), "bone")),
            *pair(box("head", "right_horn_tip", (-9, -14, -0.5), (1, 2, 1), "bone_tip")),
            *pauldron("metal"),
            *pair(box("right_arm", "right_spike", (-3, -6, -0.5), (1, 2, 1), "metal_light", rotation=(0, 0, 0.18))),
            *pair(box("right_leg", "right_cuff", (-3, 8, -3), (6, 2, 6), "metal_dark", 0.2)),
        ],
    },
    # The hide of the Nemean lion: ears and the upper jaw over the brow, a mane around the shoulders.
    "nemean": {
        "items": ["nemean_helmet", "nemean_chestplate", "nemean_boots"],
        "parts": [
            box("head", "snout", (-3, -10, -7), (6, 2, 3), "fur"),
            box("head", "nose", (-1, -10.6, -7.4), (2, 1, 1), "fur_dark"),
            *pair(box("head", "right_ear", (-5, -11, 0), (2, 2, 1), "fur_dark")),
            box("head", "mane_back", (-5, -7, 4), (10, 9, 2), "mane"),
            box("body", "mane", (-6, -1.5, -3.6), (12, 3, 7), "mane", 0.2),
            *pair(box("right_leg", "right_paw", (-3, 10, -3.6), (6, 2, 2), "fur", 0.1)),
        ],
    },
    "titan_breastplate": {
        "items": ["titan_breastplate"],
        "parts": [
            *pauldron("gold", (7, 4, 8), -4.2),
            *pair(box("right_arm", "right_rim", (-4.4, -0.6, -4.1), (6, 1, 8), "metal_dark", rotation=(0, 0, 0.18))),
            box("body", "gorget", (-4, -2, -3.4), (8, 2, 7), "gold", 0.1),
        ],
    },
    # Heimdall's golden helmet with wings, the guardian of the bridge.
    "heimdall_helmet": {
        "items": ["heimdall_helmet"],
        "parts": [
            *pair(box("head", "right_wing", (-6, -12, -1), (1, 6, 6), "feather")),
            *pair(box("head", "right_wing_tip", (-6, -16, 2), (1, 4, 4), "feather")),
            box("head", "crown", (-5, -9.6, -5), (10, 1, 10), "gold", 0.05),
        ],
    },
    # The winged sandals of Hermes.
    "talaria": {
        "items": ["talaria"],
        "parts": [
            *pair(box("right_leg", "right_wing", (-4, 7, -1), (1, 4, 5), "feather")),
            *pair(box("right_leg", "right_wing_tip", (-4, 5, 1), (1, 3, 4), "feather")),
        ],
    },
    # Seven-league boots with turned-up toes.
    "skorokhody": {
        "items": ["skorokhody"],
        "parts": [
            *pair(box("right_leg", "right_toe", (-2.5, 11, -5), (5, 2, 2), "leather")),
            *pair(box("right_leg", "right_toe_tip", (-1, 9.5, -6), (2, 2, 1), "leather_dark")),
            *pair(box("right_leg", "right_cuff", (-3.2, 6, -3.2), (6, 2, 6), "fur", 0.2)),
        ],
    },
    # The cap of invisibility: a fur brim and a soft crown.
    "shapka_nevidimka": {
        "items": ["shapka_nevidimka"],
        "parts": [
            box("head", "brim", (-6, -8, -6), (12, 3, 12), "fur", 0.1),
            box("head", "crown", (-4, -12, -4), (8, 3, 8), "cloth"),
            box("head", "top", (-2, -13, -2), (4, 1, 4), "cloth_dark"),
        ],
    },
}


def net_size(size):
    w, h, d = size
    return 2 * (w + d), d + h


def pack(parts):
    """Shelf-packs the texture nets of the boxes below the vanilla layout (from row 32) of a 64-wide texture, tallest
    first. Returns the height the texture needs: 64, or more in steps of 32 for armour with many boxes."""
    x, y, row = 0, 32, 0
    for part in sorted(parts, key=lambda p: (-net_size(p["size"])[1], -net_size(p["size"])[0])):
        nw, nh = net_size(part["size"])
        if x + nw > 64:
            x, y, row = 0, y + row, 0
        part["uv"] = [x, y]
        x += nw
        row = max(row, nh)
    bottom = y + row
    return max(64, -(-bottom // 32) * 32)


def mean(colours):
    n = max(1, len(colours))
    return tuple(sum(c[i] for c in colours) // n for i in range(3))


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def palette(img, scale):
    """The material's own colours, taken from the helmet front and the chest of the vanilla layout."""
    picks = []
    for (x0, y0, x1, y1) in ((8, 8, 16, 16), (20, 20, 28, 32)):
        for y in range(y0 * scale, y1 * scale):
            for x in range(x0 * scale, x1 * scale):
                p = img.getpixel((x, y))
                if p[3] > 200:
                    picks.append(p[:3])
    picks.sort(key=sum)
    base = mean(picks[len(picks) // 4: 3 * len(picks) // 4]) if picks else (150, 150, 160)
    return {
        "metal": base, "metal_light": shade(base, 1.25), "metal_dark": shade(base, 0.7),
        "gold": (222, 176, 58), "crest": (178, 34, 34), "chain": shade(base, 0.85),
        "bone": (226, 214, 188), "bone_tip": (180, 166, 140),
        "fur": (176, 128, 64), "fur_dark": (110, 74, 36), "mane": (140, 92, 40),
        "feather": (242, 240, 232), "leather": (120, 72, 40), "leather_dark": (84, 48, 26),
        "cloth": (60, 40, 92), "cloth_dark": (40, 26, 64),
    }


def paint_face(img, scale, rect, paint, colour, rng):
    """Fills one face of a box net, in texture pixels of the 64-wide layout, with a texture fitting its paint."""
    x0, y0, x1, y1 = rect
    if x1 <= x0 or y1 <= y0:
        return
    for y in range(y0 * scale, y1 * scale):
        for x in range(x0 * scale, x1 * scale):
            lx, ly = x - x0 * scale, y - y0 * scale
            w, h = (x1 - x0) * scale, (y1 - y0) * scale
            f = 1.0 + rng.uniform(-0.06, 0.06)
            if paint == "crest":
                f *= 0.8 if (lx // max(1, scale // 2)) % 2 else 1.08
            elif paint == "chain":
                f *= 1.25 if (lx + ly) % 2 == 0 else 0.7
            elif paint in ("fur", "mane", "fur_dark"):
                f *= 0.8 + 0.4 * ((lx * 7 + ly * 3 + rng.randint(0, 2)) % 5) / 4
            elif paint == "feather":
                f *= 1.0 - 0.18 * ((ly // max(1, scale)) % 2) - 0.12 * ly / max(1, h)
            elif paint.startswith(("metal", "gold")):
                f *= 1.12 - 0.3 * ly / max(1, h)
            # A darker rim around every face draws the box's edges in the game.
            if lx < 1 or ly < 1 or lx >= w - 1 or ly >= h - 1:
                f *= 0.72
            img.putpixel((x, y), shade(colour, f) + (255,))


def paint_box(img, scale, part, colours, rng):
    w, h, d = part["size"]
    u, v = part["uv"]
    colour = colours[part["paint"]]
    faces = [
        (u + d, v, u + d + w, v + d), (u + d + w, v, u + d + 2 * w, v + d),
        (u, v + d, u + d, v + d + h), (u + d, v + d, u + d + w, v + d + h),
        (u + d + w, v + d, u + 2 * d + w, v + d + h), (u + 2 * d + w, v + d, u + 2 * (d + w), v + d + h),
    ]
    for face in faces:
        paint_face(img, scale, face, part["paint"], colour, rng)


def main():
    out_dir = os.path.join(ROOT, "armor_models")
    os.makedirs(out_dir, exist_ok=True)
    for name, spec in SPECS.items():
        parts = spec["parts"]
        height = pack(parts)
        path = os.path.join(ROOT, "textures", "models", "armor", f"{name}_layer_1.png")
        img = Image.open(path)
        info = dict(img.info)
        img = img.convert("RGBA")
        scale = img.width // 64
        full = Image.new("RGBA", (64 * scale, height * scale), (0, 0, 0, 0))
        full.paste(img.crop((0, 0, 64 * scale, 32 * scale)), (0, 0))
        colours = palette(full, scale)
        rng = random.Random(name)
        for part in parts:
            paint_box(full, scale, part, colours, rng)
        from PIL.PngImagePlugin import PngInfo
        meta = PngInfo()
        for key, value in info.items():
            if isinstance(value, str):
                meta.add_text(key, value)
        full.save(path, pnginfo=meta)
        model = {"items": spec["items"], "texture_height": height,
                 "parts": [{k: p[k] for k in ("bone", "name", "uv", "origin", "size", "inflate", "pivot", "rotation")}
                           for p in parts]}
        with open(os.path.join(out_dir, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(model, f, indent=1)
            f.write("\n")
        print(f"{name}: {len(parts)} boxes")
    with open(os.path.join(out_dir, "index.json"), "w", encoding="utf-8") as f:
        json.dump(sorted(SPECS), f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main()
