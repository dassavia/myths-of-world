"""
Builds the GeckoLib models of the bosses of Nav and Jotunheim: geometry, animations and textures.

    python3 tools/gen_geo_models.py

Each boss is described below in model pixels (16 to a block, feet at y = 0, the face looking to -z): bones with a
pivot, and boxes of a material. The script lays every face of every box out on the texture (per-face UV), paints it
at twice the resolution with its material (colour, grain, light from above, a dark rim), and writes

    assets/mythsofworlds/geo/entity/boss/<name>.geo.json
    assets/mythsofworlds/animations/entity/boss/<name>.animation.json
    assets/mythsofworlds/textures/entity/boss/<name>.png           (and <name>_glowmask.png if any material glows)

Animations are built from the same bones: idle and walk loop, attack and special are played once when the boss
strikes or uses its power (see MythBoss in Java). Bone names the Java side relies on: head (turns to look).
"""
import json
import math
import os
import random

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources", "assets", "mythsofworlds")
SCALE = 2          # texture pixels per model pixel, as the other skins of the mod
ATLAS_WIDTHS = (64, 128, 256)  # tried in turn, in model pixels: the smallest texture wins

# name: (base colour, grain, pattern, glows)
MATERIALS = {
    "bone": ((222, 212, 182), 10, "cracks", False),
    "bone_dark": ((168, 156, 128), 10, "cracks", False),
    "robe": ((46, 30, 58), 6, "folds", False),
    "robe_trim": ((120, 92, 40), 8, "plain", False),
    "gold": ((222, 176, 58), 10, "metal", False),
    "dark_iron": ((58, 60, 68), 8, "metal", False),
    "iron": ((150, 154, 160), 10, "metal", False),
    "soul": ((90, 240, 220), 0, "plain", True),
    "skin": ((214, 160, 124), 6, "plain", False),
    "skin_pale": ((168, 182, 190), 8, "plain", False),
    "draugr_skin": ((104, 126, 128), 10, "cracks", False),
    "beard_brown": ((86, 56, 34), 12, "strands", False),
    "beard_white": ((226, 230, 236), 8, "strands", False),
    "beard_fair": ((206, 168, 96), 10, "strands", False),
    "caftan": ((150, 34, 30), 8, "folds", False),
    "caftan_trim": ((214, 170, 70), 8, "plain", False),
    "trousers": ((44, 62, 108), 6, "folds", False),
    "leather": ((74, 50, 34), 8, "plain", False),
    "boots": ((36, 28, 24), 6, "plain", False),
    "feather": ((112, 88, 64), 14, "feathers", False),
    "wood": ((116, 82, 48), 10, "grain", False),
    "white_cloth": ((228, 226, 216), 6, "folds", False),
    "blue_cloth": ((44, 74, 150), 6, "folds", False),
    "horn": ((236, 224, 196), 8, "rings", False),
    "mail": ((112, 116, 120), 14, "mail", False),
    "rust": ((120, 76, 50), 14, "cracks", False),
    "fur_grey": ((112, 108, 104), 16, "strands", False),
    "fur_dark": ((52, 50, 54), 14, "strands", False),
    "fur_black": ((30, 26, 28), 10, "strands", False),
    "fur_white": ((214, 218, 224), 10, "strands", False),
    "blood": ((118, 22, 22), 12, "strands", False),
    "ice": ((168, 216, 240), 12, "cracks", False),
    "ice_skin": ((122, 168, 200), 10, "cracks", False),
    "ice_bright": ((210, 240, 255), 0, "plain", True),
    "char": ((40, 30, 30), 10, "lava", False),
    "lava": ((255, 140, 30), 0, "plain", True),
    "fire": ((255, 196, 60), 0, "flame", True),
    "scale_green": ((52, 104, 58), 12, "scales", False),
    "belly": ((196, 178, 104), 8, "bands", False),
    "membrane": ((70, 52, 44), 8, "veins", False),
    "eye_orange": ((255, 170, 40), 0, "plain", True),
    "eye_red": ((255, 40, 30), 0, "plain", True),
    "eye_yellow": ((255, 230, 80), 0, "plain", True),
    "eye_blue": ((120, 200, 255), 0, "plain", True),
    "mouth": ((96, 20, 24), 6, "plain", False),
    "teeth": ((240, 236, 220), 4, "plain", False),
    "chain": ((92, 94, 100), 10, "chain", False),
}

FACE_LIGHT = {"up": 1.12, "north": 1.0, "south": 0.86, "east": 0.94, "west": 0.94, "down": 0.72}


class Model:
    def __init__(self, name):
        self.name = name
        self.bones = []
        self.by_name = {}
        self.anims = {}

    def bone(self, name, parent=None, pivot=(0, 0, 0), rotation=None):
        bone = {"name": name, "pivot": [pivot[0], pivot[1], pivot[2]], "cubes": []}
        if parent:
            bone["parent"] = parent
        if rotation:
            bone["rotation"] = list(rotation)
        self.bones.append(bone)
        self.by_name[name] = bone
        return name

    def box(self, bone, origin, size, material, inflate=0.0, rotation=None, pivot=None, decal=None):
        """A box from origin (its corner with the least x, y, z) of the given size; decal paints the front face."""
        cube = {"origin": list(origin), "size": list(size), "material": material, "decal": decal}
        if inflate:
            cube["inflate"] = inflate
        if rotation:
            cube["rotation"] = list(rotation)
            cube["pivot"] = list(pivot if pivot else origin)
        self.by_name[bone]["cubes"].append(cube)

    def centred(self, bone, centre_x, y, centre_z, w, h, d, material, **kw):
        self.box(bone, (centre_x - w / 2, y, centre_z - d / 2), (w, h, d), material, **kw)


# ====================================================================== texture layout and painting

def face_sizes(size):
    w, h, d = size
    return {"north": (w, h), "south": (w, h), "east": (d, h), "west": (d, h), "up": (w, d), "down": (w, d)}


def pack(model, width):
    """Shelf-packs every face of every box into a texture this wide; returns its height (a power of two)."""
    x = y = shelf = 0
    for bone in model.bones:
        for cube in bone["cubes"]:
            cube["uv"] = {}
            for face, (fw, fh) in face_sizes(cube["size"]).items():
                pw, ph = max(1, math.ceil(fw)), max(1, math.ceil(fh))
                if x + pw > width:
                    x, y, shelf = 0, y + shelf, 0
                cube["uv"][face] = (x, y, pw, ph)
                x += pw
                shelf = max(shelf, ph)
    height = y + shelf
    size = 16
    while size < height:
        size *= 2
    return size


def layout(model):
    """Lays the faces out on the smallest texture they fit; returns (width, height) in model pixels."""
    best = min(ATLAS_WIDTHS, key=lambda w: (w * pack(model, w), w))
    return best, pack(model, best)


def clamp(v):
    return max(0, min(255, int(v)))


def shade(colour, k):
    return tuple(clamp(c * k) for c in colour)


def paint_face(img, glow, rng, material, face, rect, decal):
    base, grain, pattern, glows = MATERIALS[material]
    x0, y0, w, h = (v * SCALE for v in rect)
    light = FACE_LIGHT[face] if not glows else 1.0
    for py in range(h):
        for px in range(w):
            k = light
            n = rng.randint(-grain, grain) if grain else 0
            # Light falls from above: side faces are a little brighter at the top.
            if face not in ("up", "down") and not glows:
                k *= 1.06 - 0.12 * py / max(1, h - 1)
            k *= pattern_factor(pattern, px, py, w, h, rng)
            colour = tuple(clamp(c * k + n) for c in base)
            if pattern == "flame":
                t = py / max(1, h - 1)
                colour = (255, clamp(230 - 150 * t + n), clamp(90 - 80 * t))
            # A darker rim gives every box its shape.
            if not glows and (px == 0 or py == 0 or px == w - 1 or py == h - 1):
                colour = shade(colour, 0.78)
            img.putpixel((x0 + px, y0 + py), colour + (255,))
            if glows:
                glow.putpixel((x0 + px, y0 + py), colour + (255,))
    if decal and face == "north":
        decal(img, glow, x0, y0, w, h)


def pattern_factor(pattern, x, y, w, h, rng):
    if pattern == "metal":
        return 1.18 if y <= 1 else (0.9 if y >= h - 2 else 1.0)
    if pattern == "folds":
        return 0.9 if x % 6 in (0, 1) else 1.0
    if pattern == "strands":
        return 0.88 if (x * 7 + y // 3) % 5 == 0 else 1.0
    if pattern == "feathers":
        return 0.8 if (y + (x // 4) * 2) % 6 == 0 else 1.0
    if pattern == "scales":
        return 0.78 if (y % 4 == 0) or ((x + (y // 4) * 2) % 4 == 0 and y % 4 == 1) else 1.0
    if pattern == "bands":
        return 0.82 if y % 5 == 0 else 1.0
    if pattern == "mail":
        return 0.7 if (x + y) % 3 == 0 else 1.05
    if pattern == "chain":
        return 0.6 if y % 4 == 0 or x % 4 == 0 else 1.1
    if pattern == "rings":
        return 0.85 if y % 4 == 0 else 1.0
    if pattern == "grain":
        return 0.86 if (x + y // 6) % 4 == 0 else 1.0
    if pattern == "veins":
        return 0.75 if (x * 3 + y) % 11 == 0 or (x - y) % 13 == 0 else 1.0
    if pattern == "cracks":
        return 0.82 if rng.random() < 0.05 else 1.0
    if pattern == "lava":
        return 1.0
    return 1.0


def lava_veins(img, glow, x0, y0, w, h, seed):
    """Glowing cracks over charred skin (Surtr)."""
    rng = random.Random(seed)
    for _ in range(max(1, w * h // 60)):
        x, y = rng.randrange(w), rng.randrange(h)
        for _ in range(rng.randint(3, 8)):
            if 0 <= x < w and 0 <= y < h:
                c = (255, rng.randint(110, 170), 30, 255)
                img.putpixel((x0 + x, y0 + y), c)
                glow.putpixel((x0 + x, y0 + y), c)
            x += rng.choice((-1, 0, 1))
            y += 1


def eyes(colour, glows=True, low=0.42, gap=0.2, size=0.14):
    """Two eyes on a face, colour (r, g, b); glowing eyes are copied to the glow mask."""
    def draw(img, glow, x0, y0, w, h):
        ew = max(2, round(w * size))
        eh = max(2, round(h * size * 0.8))
        cy = y0 + round(h * low)
        for cx in (x0 + round(w * (0.5 - gap)) - ew // 2, x0 + round(w * (0.5 + gap)) - ew // 2):
            for y in range(cy, cy + eh):
                for x in range(cx, cx + ew):
                    img.putpixel((x, y), colour + (255,))
                    if glows:
                        glow.putpixel((x, y), colour + (255,))
    return draw


def face(eye, mouth=None, beard=None, glows=False):
    """A humanoid face: eyes, a mouth line and optionally a beard over the lower part."""
    draw_eyes = eyes(eye, glows=glows, low=0.4, gap=0.18, size=0.13)

    def draw(img, glow, x0, y0, w, h):
        if beard:
            for y in range(round(h * 0.62), h):
                for x in range(round(w * 0.12), round(w * 0.88)):
                    n = (x * 5 + y * 3) % 7
                    img.putpixel((x0 + x, y0 + y), shade(beard, 0.9 if n == 0 else 1.0) + (255,))
        if mouth:
            y = y0 + round(h * (0.72 if not beard else 0.66))
            for x in range(x0 + round(w * 0.36), x0 + round(w * 0.64)):
                img.putpixel((x, y), mouth + (255,))
        # Brows give the face a frown.
        by = y0 + round(h * 0.33)
        for x in range(x0 + round(w * 0.2), x0 + round(w * 0.8)):
            if abs(x - (x0 + w / 2)) > w * 0.06:
                img.putpixel((x, by), shade(MATERIALS["leather"][0], 0.6) + (255,))
        draw_eyes(img, glow, x0, y0, w, h)
    return draw


def skull(eye):
    """A skull's face: dark sockets with a glowing spark in each, a nose hole and teeth."""
    def draw(img, glow, x0, y0, w, h):
        dark = (34, 26, 30, 255)
        sw, sh = max(3, round(w * 0.22)), max(3, round(h * 0.2))
        sy = y0 + round(h * 0.34)
        for sx in (x0 + round(w * 0.3) - sw // 2, x0 + round(w * 0.7) - sw // 2):
            for y in range(sy, sy + sh):
                for x in range(sx, sx + sw):
                    img.putpixel((x, y), dark)
            for y in range(sy + sh // 3, sy + sh // 3 + 2):
                for x in range(sx + sw // 3, sx + sw // 3 + 2):
                    img.putpixel((x, y), eye + (255,))
                    glow.putpixel((x, y), eye + (255,))
        nx, ny = x0 + w // 2 - 1, y0 + round(h * 0.6)
        for y in range(ny, ny + 2):
            for x in range(nx, nx + 2):
                img.putpixel((x, y), dark)
        ty = y0 + round(h * 0.78)
        for x in range(x0 + round(w * 0.25), x0 + round(w * 0.75)):
            img.putpixel((x, ty), dark if x % 2 else (240, 232, 210, 255))
    return draw


def paint(model, width, height, seed):
    img = Image.new("RGBA", (width * SCALE, height * SCALE), (0, 0, 0, 0))
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    rng = random.Random(seed)
    for bone in model.bones:
        for i, cube in enumerate(bone["cubes"]):
            for face_name, rect in cube["uv"].items():
                paint_face(img, glow, rng, cube["material"], face_name, rect, cube["decal"])
                if MATERIALS[cube["material"]][2] == "lava":
                    x0, y0, w, h = (v * SCALE for v in rect)
                    lava_veins(img, glow, x0, y0, w, h, f"{seed}{bone['name']}{i}{face_name}")
    return img, glow


# ====================================================================== geometry and animation files

def geo_json(model, width, height):
    bones = []
    for bone in model.bones:
        out = {"name": bone["name"], "pivot": bone["pivot"]}
        if "parent" in bone:
            out["parent"] = bone["parent"]
        if "rotation" in bone:
            out["rotation"] = bone["rotation"]
        cubes = []
        for cube in bone["cubes"]:
            c = {"origin": cube["origin"], "size": cube["size"],
                 "uv": {f: {"uv": [u, v], "uv_size": [w, h]} for f, (u, v, w, h) in cube["uv"].items()}}
            if "inflate" in cube:
                c["inflate"] = cube["inflate"]
            if "rotation" in cube:
                c["rotation"] = cube["rotation"]
                c["pivot"] = cube["pivot"]
            cubes.append(c)
        if cubes:
            out["cubes"] = cubes
        bones.append(out)
    xs = [abs(c["origin"][0]) + c["size"][0] for b in model.bones for c in b["cubes"]]
    ys = [c["origin"][1] + c["size"][1] for b in model.bones for c in b["cubes"]]
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {
                "identifier": f"geometry.mythsofworlds.{model.name}",
                "texture_width": width,
                "texture_height": height,
                "visible_bounds_width": math.ceil(max(xs) * 2 / 16) + 2,
                "visible_bounds_height": math.ceil(max(ys) / 16) + 2,
                "visible_bounds_offset": [0, max(ys) / 32, 0],
            },
            "bones": bones,
        }],
    }


def r(v):
    return round(v, 3)


def track(length, fn, steps_per_second=12):
    """Keyframes of fn(t) -> (x, y, z) sampled over the animation."""
    steps = max(2, round(length * steps_per_second))
    return {f"{r(length * i / steps)}": [r(v) for v in fn(length * i / steps)] for i in range(steps + 1)}


def wave(t, period, amplitude, phase=0.0):
    return amplitude * math.sin(2 * math.pi * (t / period + phase))


def pulse(t, start, peak, end, amount):
    """0 before start, rising to amount at peak, back to 0 at end (smooth)."""
    if t <= start or t >= end:
        return 0.0
    if t <= peak:
        k = (t - start) / (peak - start)
    else:
        k = 1.0 - (t - peak) / (end - peak)
    return amount * (0.5 - 0.5 * math.cos(math.pi * k))


class Anim:
    def __init__(self, length, loop):
        self.length = length
        self.loop = loop
        self.bones = {}

    def rot(self, bone, fn):
        self.bones.setdefault(bone, {})["rotation"] = track(self.length, fn)
        return self

    def pos(self, bone, fn):
        self.bones.setdefault(bone, {})["position"] = track(self.length, fn)
        return self

    def json(self):
        out = {"animation_length": self.length, "bones": self.bones}
        if self.loop:
            out["loop"] = True
        return out


def anim_json(model):
    return {"format_version": "1.8.0", "animations": {name: a.json() for name, a in model.anims.items()}}


# ====================================================================== shared bodies

def humanoid(m, hip, leg, torso, arm, head, materials, arm_down=True):
    """Bones and boxes of a two-legged body.

    hip: height of the hips; leg (w, d); torso (w, h, d); arm (w, len); head (w, h, d) on top of the torso.
    materials: dict with legs, boots, torso, arms, hands, head.
    """
    lw, ld = leg
    tw, th, td = torso
    aw, al = arm
    hw, hh, hd = head
    shoulder = hip + th
    m.bone("root")
    m.bone("leg_left", "root", (lw / 2 + 0.5, hip, 0))
    m.bone("leg_right", "root", (-lw / 2 - 0.5, hip, 0))
    for side, sx in (("leg_left", 1), ("leg_right", -1)):
        cx = sx * (lw / 2 + 0.5)
        m.centred(side, cx, hip * 0.22, 0, lw, hip * 0.78, ld, materials["legs"])
        m.centred(side, cx, 0, -0.5, lw + 0.6, hip * 0.25, ld + 1.2, materials["boots"])
    m.bone("torso", "root", (0, hip, 0))
    m.centred("torso", 0, hip, 0, tw, th, td, materials["torso"])
    m.bone("head", "torso", (0, shoulder, 0))
    m.centred("head", 0, shoulder, 0, hw, hh, hd, materials["head"], decal=materials.get("face"))
    m.bone("arm_left", "torso", (tw / 2 + aw / 2, shoulder - 1.5, 0))
    m.bone("arm_right", "torso", (-tw / 2 - aw / 2, shoulder - 1.5, 0))
    for side, sx in (("arm_left", 1), ("arm_right", -1)):
        cx = sx * (tw / 2 + aw / 2)
        m.centred(side, cx, shoulder + 1 - al * 0.8, 0, aw, al * 0.8, aw, materials["arms"])
        m.centred(side, cx, shoulder + 1 - al, 0, aw + 0.2, al * 0.2, aw + 0.2, materials["hands"])
    return shoulder


def humanoid_anims(m, stride=28.0, arm_swing=22.0, heavy=1.0, attack="arm_right"):
    """Idle, walk and an overhead blow for a two-legged body; heavy slows the giants down."""
    walk_t = 1.0 * heavy
    m.anims["walk"] = (Anim(walk_t, True)
                       .rot("leg_left", lambda t: (wave(t, walk_t, stride), 0, 0))
                       .rot("leg_right", lambda t: (wave(t, walk_t, -stride), 0, 0))
                       .rot("arm_left", lambda t: (wave(t, walk_t, -arm_swing), 0, 0))
                       .rot("arm_right", lambda t: (wave(t, walk_t, arm_swing), 0, 0))
                       .pos("torso", lambda t: (0, abs(wave(t, walk_t, 0.8 * heavy)), 0))
                       .rot("torso", lambda t: (0, wave(t, walk_t, 4), 0)))
    idle_t = 3.0
    m.anims["idle"] = (Anim(idle_t, True)
                       .pos("torso", lambda t: (0, wave(t, idle_t, 0.35), 0))
                       .rot("arm_left", lambda t: (wave(t, idle_t, 3), 0, -3 + wave(t, idle_t, 2)))
                       .rot("arm_right", lambda t: (wave(t, idle_t, -3), 0, 3 - wave(t, idle_t, 2)))
                       .rot("head", lambda t: (wave(t, idle_t, 2, 0.25), wave(t, idle_t * 2, 6), 0)))
    att_t = 0.7 * heavy
    m.anims["attack"] = (Anim(att_t, False)
                         .rot(attack, lambda t: (-pulse(t, 0, 0.35 * att_t, 0.6 * att_t, 150) + pulse(t, 0.45 * att_t, 0.7 * att_t, att_t, 40), 0, 0))
                         .rot("torso", lambda t: (pulse(t, 0.3 * att_t, 0.6 * att_t, att_t, 12), pulse(t, 0, 0.35 * att_t, att_t, -18), 0)))


def quadruped(m, body, leg, neck_y, head, materials, tail_len=10):
    """A four-legged beast: body (w, h, d, height of its underside), legs (w, len), head (w, h, d)."""
    bw, bh, bd, belly = body
    lw, ll = leg
    hw, hh, hd = head
    m.bone("root")
    m.bone("body", "root", (0, belly + bh / 2, 0))
    m.centred("body", 0, belly, 0, bw, bh, bd, materials["body"])
    m.centred("body", 0, belly + bh * 0.25, -bd / 2 - 3 + 0.01, bw + 2, bh * 0.85, 6, materials["mane"])
    for name, x, z in (("leg_front_left", 1, -1), ("leg_front_right", -1, -1), ("leg_back_left", 1, 1), ("leg_back_right", -1, 1)):
        px, pz = x * (bw / 2 - lw / 2), z * (bd / 2 - lw)
        m.bone(name, "root", (px, belly + 2, pz))
        m.centred(name, px, 0, pz, lw, ll + 2, lw, materials["legs"])
        m.centred(name, px, 0, pz - 0.6, lw + 0.6, 1.6, lw + 1.6, materials["paws"])
    m.bone("tail", "body", (0, belly + bh - 2, bd / 2))
    m.box("tail", (-1.5, belly + bh - 4, bd / 2), (3, 3, tail_len), materials["tail"], rotation=(-30, 0, 0), pivot=(0, belly + bh - 2, bd / 2))
    m.bone("neck", "body", (0, neck_y, -bd / 2))
    m.centred("neck", 0, neck_y - 3, -bd / 2 - 3, hw * 0.75, hh * 0.85, 6, materials["mane"])
    m.bone("head", "neck", (0, neck_y + 1, -bd / 2 - 5))
    hz = -bd / 2 - 5 - hd / 2
    m.centred("head", 0, neck_y - 1, hz, hw, hh, hd, materials["head"], decal=materials["face"])
    m.centred("head", 0, neck_y - 1, hz - hd / 2 - 3, hw * 0.55, hh * 0.35, 6, materials["head"])
    m.centred("head", 0, neck_y - 1 + hh * 0.35 - 0.6, hz - hd / 2 - 3, hw * 0.45, 1.0, 5.6, "teeth")
    for sx in (1, -1):
        m.box("head", (sx * hw * 0.32 - 1.5, neck_y - 1 + hh, hz + hd * 0.2), (3, 4, 2), materials["head"],
              rotation=(-15, 0, sx * 10), pivot=(sx * hw * 0.32, neck_y - 1 + hh, hz))
    m.bone("jaw", "head", (0, neck_y - 1, hz - hd / 2))
    m.centred("jaw", 0, neck_y - 1 - hh * 0.3, hz - hd / 2 - 2.5, hw * 0.5, hh * 0.3, 5, "mouth")


def quadruped_anims(m, stride=30.0, heavy=1.0):
    walk_t = 0.9 * heavy
    m.anims["walk"] = (Anim(walk_t, True)
                       .rot("leg_front_left", lambda t: (wave(t, walk_t, stride), 0, 0))
                       .rot("leg_back_right", lambda t: (wave(t, walk_t, stride), 0, 0))
                       .rot("leg_front_right", lambda t: (wave(t, walk_t, -stride), 0, 0))
                       .rot("leg_back_left", lambda t: (wave(t, walk_t, -stride), 0, 0))
                       .pos("body", lambda t: (0, abs(wave(t, walk_t, 0.8)), 0))
                       .rot("tail", lambda t: (wave(t, walk_t, 8), wave(t, walk_t, 14), 0))
                       .rot("neck", lambda t: (wave(t, walk_t, 4, 0.25), 0, 0)))
    idle_t = 2.6
    m.anims["idle"] = (Anim(idle_t, True)
                       .pos("body", lambda t: (0, wave(t, idle_t, 0.3), 0))
                       .rot("tail", lambda t: (0, wave(t, idle_t, 18), 0))
                       .rot("neck", lambda t: (wave(t, idle_t, 3), wave(t, idle_t * 2, 8), 0))
                       .rot("jaw", lambda t: (pulse(t % idle_t, 1.6, 1.9, 2.3, 12), 0, 0)))
    att_t = 0.6
    m.anims["attack"] = (Anim(att_t, False)
                         .rot("neck", lambda t: (-pulse(t, 0, 0.2, 0.35, 15) + pulse(t, 0.2, 0.35, att_t, 25), 0, 0))
                         .rot("jaw", lambda t: (pulse(t, 0.05, 0.25, 0.45, 40), 0, 0))
                         .pos("body", lambda t: (0, 0, -pulse(t, 0.15, 0.32, att_t, 3))))
    howl_t = 1.6
    m.anims["special"] = (Anim(howl_t, False)
                          .rot("neck", lambda t: (-pulse(t, 0, 0.4, howl_t, 55), 0, 0))
                          .rot("head", lambda t: (-pulse(t, 0, 0.4, howl_t, 15), 0, 0))
                          .rot("jaw", lambda t: (pulse(t, 0.2, 0.5, howl_t, 35), 0, 0))
                          .rot("leg_front_left", lambda t: (-pulse(t, 0, 0.4, howl_t, 10), 0, 0))
                          .rot("leg_front_right", lambda t: (-pulse(t, 0, 0.4, howl_t, 10), 0, 0)))


# ====================================================================== the bosses

def koschei():
    m = Model("koschei")
    sh = humanoid(m, hip=17, leg=(2.5, 2.5), torso=(8, 14, 4), arm=(2.5, 17), head=(7, 8, 7),
                  materials={"legs": "bone", "boots": "robe", "torso": "robe", "arms": "bone", "hands": "bone_dark",
                             "head": "bone", "face": skull((90, 240, 220))})
    m.centred("torso", 0, 25, -2.1, 5, 6, 0.4, "bone")           # ribs showing through the torn robe
    m.centred("torso", 0, 17, 0, 9, 2, 5, "robe_trim")           # belt
    m.bone("cloak", "torso", (0, sh, 2.2))
    m.box("cloak", (-5.5, 3, 2), (11, sh - 3, 1), "robe")
    m.box("cloak", (-5.5, sh - 2, 1.5), (11, 2, 2), "robe_trim")
    for i, x in enumerate((-3, -1.25, 0.5, 2.25)):               # crown of spikes
        m.box("head", (x - 0.25, sh + 8, -3.5 + (i % 2) * 0.5), (1, 3 + (i % 2), 1), "gold")
    m.centred("head", 0, sh + 7.5, 0, 7.6, 1.2, 7.6, "gold")
    m.bone("sword", "arm_right", (-5.25, sh - 16, 0))
    m.box("sword", (-5.75, sh - 17, -3), (1, 1.5, 6), "gold")                  # guard
    m.box("sword", (-5.75, sh - 18.5, -1), (1, 1.5, 2), "robe")
    m.box("sword", (-5.6, sh - 17, -12), (0.7, 1.2, 9), "dark_iron")           # blade held forward
    humanoid_anims(m, stride=22, arm_swing=16)
    sp = 1.8
    m.anims["special"] = (Anim(sp, False)                                       # raises the dead
                          .rot("arm_left", lambda t: (-pulse(t, 0, 0.6, sp, 150), 0, -pulse(t, 0, 0.6, sp, 20)))
                          .rot("arm_right", lambda t: (-pulse(t, 0, 0.6, sp, 150), 0, pulse(t, 0, 0.6, sp, 20)))
                          .rot("head", lambda t: (-pulse(t, 0.2, 0.7, sp, 25), 0, 0))
                          .rot("cloak", lambda t: (pulse(t, 0.2, 0.8, sp, 25), 0, 0)))
    m.anims["idle"].rot("cloak", lambda t: (6 + wave(t, 3.0, 4), 0, 0))
    m.anims["walk"].rot("cloak", lambda t: (12 + wave(t, 1.0, 6), 0, 0))
    return m


def solovei():
    m = Model("solovei")
    sh = humanoid(m, hip=14, leg=(4, 4), torso=(11, 13, 6), arm=(3.5, 13), head=(8, 8, 8),
                  materials={"legs": "trousers", "boots": "boots", "torso": "caftan", "arms": "caftan", "hands": "skin",
                             "head": "skin", "face": face((40, 30, 20), (90, 40, 30), beard=MATERIALS["beard_brown"][0])})
    m.centred("torso", 0, 14, 0, 11.6, 2, 6.6, "leather")          # belt
    m.centred("torso", 0, 14 + 4, -3.05, 1.6, 9, 0.4, "caftan_trim")
    m.centred("head", 0, sh - 2, -4.2, 7, 4, 1.4, "beard_brown")   # beard
    m.centred("head", 0, sh + 7, 0, 9, 2.5, 9, "fur_dark")         # fur hat
    m.centred("head", 0, sh + 9.5, 0, 7, 2, 7, "caftan")
    m.bone("mantle", "torso", (0, sh, 0))                          # feathered mantle, half a bird
    m.centred("mantle", 0, sh - 4, 0, 14, 4, 8, "feather")
    for i, x in enumerate((-6, -3, 0, 3, 6)):
        m.box("mantle", (x - 1.5, sh - 9 - (i % 2) * 2, 3.5), (3, 6 + (i % 2) * 2, 1), "feather")
    m.bone("axe", "arm_right", (-7.25, sh - 12, 0))
    m.box("axe", (-7.75, sh - 13, -8), (1, 1, 14), "wood")
    m.box("axe", (-8.0, sh - 15.5, -9), (1.5, 6, 4), "iron")
    humanoid_anims(m, stride=26, arm_swing=24)
    sp = 1.6
    m.anims["special"] = (Anim(sp, False)                           # the whistle: fingers to the mouth, lean, blow
                          .rot("arm_left", lambda t: (-pulse(t, 0, 0.3, 1.2, 120), 0, -pulse(t, 0, 0.3, 1.2, 35)))
                          .rot("arm_right", lambda t: (-pulse(t, 0, 0.3, 1.2, 120), 0, pulse(t, 0, 0.3, 1.2, 35)))
                          .rot("torso", lambda t: (-pulse(t, 0.1, 0.5, 0.7, 14) + pulse(t, 0.6, 0.8, sp, 16), 0, 0))
                          .rot("head", lambda t: (-pulse(t, 0.1, 0.5, 0.7, 18) + pulse(t, 0.6, 0.8, sp, 10), 0, 0))
                          .rot("mantle", lambda t: (pulse(t, 0.6, 0.8, sp, 30), 0, 0)))
    return m


def zmey():
    m = Model("zmey_gorynych")
    m.bone("root")
    m.bone("body", "root", (0, 22, 0))
    m.centred("body", 0, 14, 0, 22, 17, 30, "scale_green")
    m.centred("body", 0, 13.6, -1, 16, 2, 26, "belly")
    for i in range(5):                                            # spines along the back
        m.centred("body", 0, 31, -12 + i * 6, 2, 3, 3, "horn")
    for name, x, z in (("leg_front_left", 1, -1), ("leg_front_right", -1, -1), ("leg_back_left", 1, 1), ("leg_back_right", -1, 1)):
        px, pz = x * 10, z * 10
        m.bone(name, "root", (px, 18, pz))
        m.centred(name, px, 0, pz, 7, 19, 7, "scale_green")
        m.centred(name, px, 0, pz - 1, 8, 2, 9, "horn")
    m.bone("tail", "body", (0, 22, 15))
    m.centred("tail", 0, 18, 22, 10, 8, 14, "scale_green")
    m.bone("tail_tip", "tail", (0, 21, 29))
    m.centred("tail_tip", 0, 19, 36, 6, 5, 14, "scale_green")
    m.centred("tail_tip", 0, 20, 44, 4, 6, 3, "horn")
    for side, sx in (("wing_left", 1), ("wing_right", -1)):
        m.bone(side, "body", (sx * 10, 30, -4))
        m.box(side, (sx * 10 + (0 if sx > 0 else -26), 30, -6), (26, 1, 18), "membrane")
        m.box(side, (sx * 10 + (0 if sx > 0 else -26), 30.5, -7), (26, 1.5, 2), "scale_green")
    for name, angle in (("neck_left", 28), ("neck_middle", 0), ("neck_right", -28)):
        ox = math.sin(math.radians(angle)) * 6
        m.bone(name, "body", (ox, 28, -14), rotation=(0, angle, 0))
        m.centred(name, ox, 25, -18, 6, 7, 8, "scale_green")
        m.centred(name, ox, 30, -22, 5.5, 6, 6, "scale_green")
        head = name.replace("neck", "head")
        m.bone(head, name, (ox, 35, -24))
        m.centred(head, ox, 33, -26, 7, 6, 8, "scale_green", decal=eyes((255, 170, 40), low=0.25, gap=0.26))
        m.centred(head, ox, 33, -32, 5, 3.5, 6, "scale_green")
        for sx in (1, -1):
            m.box(head, (ox + sx * 2.5 - 0.5, 39, -25), (1, 3, 1), "horn", rotation=(-30, 0, 0), pivot=(ox, 39, -25))
        jaw = name.replace("neck", "jaw")
        m.bone(jaw, head, (ox, 33, -26))
        m.centred(jaw, ox, 31.5, -31, 4.6, 1.5, 6, "mouth")
        m.centred(jaw, ox, 32.8, -31, 4.2, 0.6, 5.6, "teeth")
    walk_t = 1.2
    w = Anim(walk_t, True)
    for leg, sign in (("leg_front_left", 1), ("leg_back_right", 1), ("leg_front_right", -1), ("leg_back_left", -1)):
        w.rot(leg, lambda t, s=sign: (wave(t, walk_t, 22 * s), 0, 0))
    w.rot("tail", lambda t: (0, wave(t, walk_t, 12), 0)).rot("tail_tip", lambda t: (0, wave(t, walk_t, 18, 0.2), 0))
    w.pos("body", lambda t: (0, abs(wave(t, walk_t, 0.9)), 0))
    for i, n in enumerate(("neck_left", "neck_middle", "neck_right")):
        w.rot(n, lambda t, i=i: (wave(t, walk_t, 5, i / 3), 0, 0))
    for side, sx in (("wing_left", 1), ("wing_right", -1)):
        w.rot(side, lambda t, sx=sx: (0, 0, sx * (10 + wave(t, walk_t, 6))))
    m.anims["walk"] = w
    idle_t = 3.0
    i_ = Anim(idle_t, True)
    for i, n in enumerate(("neck_left", "neck_middle", "neck_right")):
        i_.rot(n, lambda t, i=i: (wave(t, idle_t, 6, i / 3), wave(t, idle_t * 2, 10, i / 5), 0))
        i_.rot(n.replace("neck", "jaw"), lambda t, i=i: (pulse((t + i) % idle_t, 1.0, 1.3, 1.8, 18), 0, 0))
    for side, sx in (("wing_left", 1), ("wing_right", -1)):
        i_.rot(side, lambda t, sx=sx: (0, 0, sx * (15 + wave(t, idle_t, 10))))
    i_.rot("tail", lambda t: (0, wave(t, idle_t, 10), 0)).pos("body", lambda t: (0, wave(t, idle_t, 0.4), 0))
    m.anims["idle"] = i_
    att_t = 0.7
    a = Anim(att_t, False)
    for i, n in enumerate(("neck_left", "neck_middle", "neck_right")):
        a.rot(n, lambda t, i=i: (-pulse(t, 0, 0.2, 0.35, 20) + pulse(t, 0.2 + i * 0.05, 0.4 + i * 0.05, att_t, 35), 0, 0))
        a.rot(n.replace("neck", "jaw"), lambda t, i=i: (pulse(t, 0.1, 0.35 + i * 0.05, att_t, 45), 0, 0))
    m.anims["attack"] = a
    sp = 1.5
    s = Anim(sp, False)                                            # three streams of fire
    for n in ("neck_left", "neck_middle", "neck_right"):
        s.rot(n, lambda t: (-pulse(t, 0, 0.45, 0.6, 30) + pulse(t, 0.5, 0.7, sp, 25), 0, 0))
        s.rot(n.replace("neck", "jaw"), lambda t: (pulse(t, 0.45, 0.65, sp, 50), 0, 0))
    for side, sx in (("wing_left", 1), ("wing_right", -1)):
        s.rot(side, lambda t, sx=sx: (0, 0, sx * pulse(t, 0, 0.5, sp, 45)))
    m.anims["special"] = s
    return m


def heimdall():
    m = Model("heimdall")
    sh = humanoid(m, hip=16, leg=(3.5, 3.5), torso=(10, 14, 5), arm=(3.5, 15), head=(7.5, 8, 7.5),
                  materials={"legs": "white_cloth", "boots": "gold", "torso": "gold", "arms": "white_cloth", "hands": "gold",
                             "head": "skin", "face": face((120, 200, 255), (110, 60, 50), beard=MATERIALS["beard_fair"][0], glows=True)})
    m.centred("torso", 0, 16, 0, 10.6, 2, 5.6, "blue_cloth")
    m.centred("torso", 0, 25, -2.6, 6, 4, 0.4, "white_cloth")      # a sun on the breastplate
    m.centred("head", 0, sh - 2, -4, 6.5, 3, 1.4, "beard_fair")
    m.centred("head", 0, sh + 6, 0, 8.2, 3, 8.2, "gold")           # winged helmet
    m.centred("head", 0, sh + 9, 0, 3, 1.5, 6, "gold")
    for sx in (1, -1):
        m.box("head", (sx * 4.1 - (0 if sx > 0 else 1), sh + 6, -1), (1, 6, 5), "white_cloth",
              rotation=(0, 0, -sx * 25), pivot=(sx * 4.1, sh + 6, 0))
    m.bone("cloak", "torso", (0, sh, 2.6))
    m.box("cloak", (-6, 2, 2.5), (12, sh - 2, 1), "blue_cloth")
    for side, sx in (("arm_left", 1), ("arm_right", -1)):          # pauldrons
        m.centred(side, sx * 6.75, sh - 3, 0, 4.6, 3.5, 4.6, "gold")
    m.bone("sword", "arm_right", (-6.75, sh - 14, 0))
    m.box("sword", (-7.25, sh - 15, -3), (1, 1.5, 6), "gold")
    m.box("sword", (-7.1, sh - 15, -15), (0.7, 1.4, 12), "iron")
    m.bone("gjallarhorn", "arm_left", (6.75, sh - 14, 0))
    m.box("gjallarhorn", (5.75, sh - 16, -2), (2, 2, 5), "horn", rotation=(20, 0, 0), pivot=(6.75, sh - 14, 0))
    m.box("gjallarhorn", (5.25, sh - 16.5, -6), (3, 3, 4), "gold", rotation=(20, 0, 0), pivot=(6.75, sh - 14, 0))
    humanoid_anims(m, stride=26, arm_swing=20)
    sp = 2.0
    m.anims["special"] = (Anim(sp, False)                           # blows the Gjallarhorn
                          .rot("arm_left", lambda t: (-pulse(t, 0, 0.4, sp, 140), 0, -pulse(t, 0, 0.4, sp, 40)))
                          .rot("head", lambda t: (-pulse(t, 0.2, 0.5, sp, 20), 0, 0))
                          .rot("torso", lambda t: (-pulse(t, 0.3, 0.6, sp, 8), 0, 0))
                          .rot("cloak", lambda t: (pulse(t, 0.3, 0.8, sp, 30), 0, 0)))
    m.anims["idle"].rot("cloak", lambda t: (5 + wave(t, 3.0, 3), 0, 0))
    m.anims["walk"].rot("cloak", lambda t: (14 + wave(t, 1.0, 6), 0, 0))
    return m


def draugr_chieftain():
    m = Model("draugr_chieftain")
    sh = humanoid(m, hip=15, leg=(3.5, 3.5), torso=(10, 13, 5.5), arm=(3.2, 14), head=(7.5, 8, 7.5),
                  materials={"legs": "rust", "boots": "boots", "torso": "mail", "arms": "draugr_skin", "hands": "draugr_skin",
                             "head": "draugr_skin", "face": face((120, 200, 255), (30, 30, 40), beard=MATERIALS["fur_grey"][0], glows=True)})
    m.centred("torso", 0, 15, 0, 10.6, 2, 6.1, "leather")
    m.centred("torso", 0, 21, 0, 10.4, 5, 5.9, "rust")
    m.centred("head", 0, sh - 2.5, -4, 6.5, 4, 1.4, "fur_grey")
    m.centred("head", 0, sh + 5.5, 0, 8.2, 3, 8.2, "dark_iron")      # helmet
    m.centred("head", 0, sh + 1.5, -4.2, 1, 5, 0.8, "dark_iron")     # nose guard
    for i, x in enumerate((-3, -1, 1, 3)):                            # the barrow crown
        m.box("head", (x - 0.5, sh + 8.5, -3.6), (1, 2 + (i % 2), 1), "gold")
    m.bone("cloak", "torso", (0, sh, 2.8))
    m.box("cloak", (-5.5, 3, 2.75), (11, sh - 3, 1), "fur_dark")
    m.bone("axe", "arm_right", (-6.6, sh - 13, 0))
    m.box("axe", (-7.1, sh - 14, -9), (1, 1, 15), "wood")
    m.box("axe", (-7.35, sh - 17, -10), (1.5, 7, 4), "dark_iron")
    m.bone("shield", "arm_left", (6.6, sh - 8, 0))
    m.box("shield", (8.2, sh - 15, -5), (1, 10, 10), "wood")
    m.centred("shield", 8.9, sh - 11, 0, 1, 2, 2, "iron")
    humanoid_anims(m, stride=24, arm_swing=18)
    sp = 1.6
    m.anims["special"] = (Anim(sp, False)                            # calls his dead from the barrow
                          .rot("arm_right", lambda t: (-pulse(t, 0, 0.5, sp, 170), 0, 0))
                          .rot("head", lambda t: (-pulse(t, 0.1, 0.5, sp, 25), 0, 0))
                          .rot("torso", lambda t: (-pulse(t, 0.1, 0.5, sp, 8), 0, 0)))
    m.anims["idle"].rot("cloak", lambda t: (5 + wave(t, 3.0, 3), 0, 0))
    m.anims["walk"].rot("cloak", lambda t: (12 + wave(t, 1.0, 5), 0, 0))
    return m


def thrym():
    m = Model("thrym")
    sh = humanoid(m, hip=28, leg=(8, 8), torso=(22, 28, 12), arm=(7, 32), head=(13, 14, 13),
                  materials={"legs": "fur_white", "boots": "leather", "torso": "ice_skin", "arms": "ice_skin", "hands": "ice_skin",
                             "head": "ice_skin", "face": face((210, 240, 255), (40, 60, 90), beard=MATERIALS["beard_white"][0], glows=True)})
    m.centred("torso", 0, 28, 0, 23, 4, 13, "leather")
    m.centred("torso", 0, 28, 0, 23, 12, 13, "fur_white", inflate=0.2)
    m.centred("head", 0, sh - 6, -6.8, 12, 9, 2, "beard_white")
    m.centred("head", 0, sh + 14, 0, 14, 2.5, 14, "ice")             # crown of ice
    for i, x in enumerate((-5, -2, 1, 4)):
        m.box("head", (x, sh + 16, -6), (2, 3 + 2 * (i % 2), 2), "ice_bright")
    m.bone("cloak", "torso", (0, sh, 6))
    m.box("cloak", (-12, 6, 6), (24, sh - 6, 2), "fur_white")
    for side, sx in (("arm_left", 1), ("arm_right", -1)):
        m.centred(side, sx * 14.5, sh - 6, 0, 9, 6, 9, "fur_white")
    m.bone("hammer", "arm_right", (-14.5, sh - 30, 0))
    m.box("hammer", (-15.5, sh - 31, -14), (2, 2, 22), "wood")
    m.box("hammer", (-18.5, sh - 34, -20), (8, 8, 9), "ice")
    humanoid_anims(m, stride=22, arm_swing=14, heavy=1.6)
    sp = 1.8
    m.anims["special"] = (Anim(sp, False)                            # stamps the frozen ground
                          .rot("leg_right", lambda t: (-pulse(t, 0, 0.6, 0.85, 45), 0, 0))
                          .rot("arm_left", lambda t: (-pulse(t, 0, 0.6, sp, 60), 0, -pulse(t, 0, 0.6, sp, 30)))
                          .rot("arm_right", lambda t: (-pulse(t, 0, 0.6, sp, 60), 0, pulse(t, 0, 0.6, sp, 30)))
                          .pos("root", lambda t: (0, pulse(t, 0.2, 0.6, 0.85, 2) - pulse(t, 0.8, 0.9, 1.2, 1.5), 0))
                          .rot("head", lambda t: (-pulse(t, 0.8, 1.0, sp, 20), 0, 0)))
    m.anims["idle"].rot("cloak", lambda t: (4 + wave(t, 3.0, 2), 0, 0))
    m.anims["walk"].rot("cloak", lambda t: (8 + wave(t, 1.6, 4), 0, 0))
    return m


def surtr():
    m = Model("surtr")
    sh = humanoid(m, hip=28, leg=(8, 8), torso=(22, 28, 12), arm=(7, 32), head=(13, 14, 13),
                  materials={"legs": "char", "boots": "char", "torso": "char", "arms": "char", "hands": "char",
                             "head": "char", "face": face((255, 200, 60), (255, 120, 30), glows=True)})
    m.centred("torso", 0, 28, 0, 23, 3, 13, "dark_iron")
    m.centred("torso", 0, 46, -6.2, 12, 6, 0.4, "lava")
    for i, x in enumerate((-6, -3, 0, 3, 6)):                        # crown of flames
        m.box("head", (x - 1, sh + 14, -1 - (i % 2) * 3), (2, 4 + 3 * ((i + 1) % 2), 2), "fire")
    for side, sx in (("arm_left", 1), ("arm_right", -1)):
        m.centred(side, sx * 14.5, sh - 6, 0, 9, 6, 9, "dark_iron")
    m.bone("sword", "arm_right", (-14.5, sh - 30, 0))
    m.box("sword", (-15.5, sh - 31, -4), (2, 2, 8), "dark_iron")      # guard
    m.box("sword", (-15.5, sh - 33, -1), (2, 3, 2), "char")
    m.box("sword", (-15.25, sh - 31, -34), (1.5, 2.5, 30), "fire")    # the flaming blade
    humanoid_anims(m, stride=22, arm_swing=14, heavy=1.6)
    sp = 1.8
    m.anims["special"] = (Anim(sp, False)                            # raises the sword: a ring of fire
                          .rot("arm_right", lambda t: (-pulse(t, 0, 0.7, sp, 175), 0, 0))
                          .rot("arm_left", lambda t: (-pulse(t, 0.1, 0.7, sp, 60), 0, -pulse(t, 0.1, 0.7, sp, 40)))
                          .rot("head", lambda t: (-pulse(t, 0.2, 0.7, sp, 25), 0, 0))
                          .rot("torso", lambda t: (-pulse(t, 0.2, 0.7, sp, 10), 0, 0)))
    return m


def fenrir():
    m = Model("fenrir")
    quadruped(m, body=(18, 18, 34, 18), leg=(6, 16), neck_y=36, head=(13, 12, 13),
              materials={"body": "fur_dark", "legs": "fur_dark", "paws": "fur_black", "tail": "fur_dark",
                         "mane": "fur_grey", "head": "fur_dark", "face": eyes((255, 230, 80), low=0.3, gap=0.25)},
              tail_len=16)
    m.centred("neck", 0, 31, -19.5, 13, 2, 7, "chain")                # a broken link of Gleipnir
    quadruped_anims(m, stride=30, heavy=1.2)
    return m


def garm():
    m = Model("garm")
    quadruped(m, body=(13, 13, 24, 13), leg=(4.5, 11), neck_y=26, head=(10, 9, 10),
              materials={"body": "fur_black", "legs": "fur_black", "paws": "fur_dark", "tail": "fur_black",
                         "mane": "blood", "head": "fur_black", "face": eyes((255, 40, 30), low=0.3, gap=0.25)},
              tail_len=12)
    m.centred("neck", 0, 22, -14.5, 10, 2, 6, "chain")
    quadruped_anims(m, stride=34, heavy=0.9)
    return m


BOSSES = [koschei, solovei, zmey, heimdall, draugr_chieftain, thrym, surtr, fenrir, garm]


def write_json(path, value):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(value, f, indent=1, ensure_ascii=False)
        f.write("\n")


def save_png(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, optimize=False, compress_level=9)


def main():
    for build in BOSSES:
        model = build()
        width, height = layout(model)
        img, glow = paint(model, width, height, model.name)
        write_json(os.path.join(ROOT, "geo", "entity", "boss", model.name + ".geo.json"), geo_json(model, width, height))
        write_json(os.path.join(ROOT, "animations", "entity", "boss", model.name + ".animation.json"), anim_json(model))
        save_png(img, os.path.join(ROOT, "textures", "entity", "boss", model.name + ".png"))
        # Only a model with glowing parts gets a glow mask (MythGeoRenderer is told so in Java: GLOWING there).
        mask = os.path.join(ROOT, "textures", "entity", "boss", model.name + "_glowmask.png")
        if glow.getbbox():
            save_png(glow, mask)
        elif os.path.exists(mask):
            os.remove(mask)
        cubes = sum(len(b["cubes"]) for b in model.bones)
        print(f"{model.name}: {len(model.bones)} bones, {cubes} boxes, texture {width * SCALE}x{height * SCALE}")


if __name__ == "__main__":
    main()
