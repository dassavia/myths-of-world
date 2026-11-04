"""The women of the myths at full resolution: amazons and Hippolyta (Hellas), valkyries (Jotunheim), the priestesses
of Isis and Isis herself (the Duat).

Each skin is painted directly at 128x128 on the 64x64 layout of the wide player model (two texels per model pixel),
so faces, hair and jewellery get real detail; the textures are marked as already high-resolution and hd_textures.py
leaves them alone. Every look is described by the same colour specs as before (tools/textures.py, textures_norse.py,
textures_egyptian.py), the painter adds the rest:

* a face with lashed almond eyes, a coloured iris with a glint, fine brows, a hint of a nose, two-toned lips and a
  touch of blush; the Egyptians have kohl lines drawn out to the temples;
* hair in strands with a sheen, its volume on the hat layer and long hair falling down the back;
* the dress of each culture: the pleated chiton and peplos with a meander hem, the huntress's short tunic, the bronze
  muscle cuirass with leather strips and greaves; the mail shirt, fur mantle and winged helm of the valkyries; the
  linen sheath, broad collar of gold, lapis, turquoise and carnelian, the diadem with the uraeus and golden arm rings
  of the priestesses;
* Isis: a royal priestess on the plain humanoid layout, the throne sign on her head, the vulture-feathered wings of
  the goddess down her arms and the knot of Isis on her collar.

Light falls from above: tops are brightest, sides and backs darker, every face shades towards its lower edge.
"""
import math

from PIL import Image

K = 2              # texels per model pixel
SIZE = 64 * K
HD_MARK = "mythsofworlds:hd"

GOLD, GOLD_LIGHT, GOLD_DARK = 0xE2B33C, 0xFFE38A, 0x9A6E1E
LAPIS, TURQUOISE, CARNELIAN = 0x2A5AB0, 0x3AB8A8, 0xC0402A
LINEN = 0xF2EEE2
FACE_LIGHT = {"top": 1.08, "front": 1.0, "right": 0.92, "left": 0.92, "back": 0.86, "bottom": 0.74}

# The wide player model: (u, v, w, h, d) in model pixels.
PLAYER = {"head": (0, 0, 8, 8, 8), "hat": (32, 0, 8, 8, 8), "body": (16, 16, 8, 12, 4), "jacket": (16, 32, 8, 12, 4),
          "right_arm": (40, 16, 4, 12, 4), "right_sleeve": (40, 32, 4, 12, 4), "left_arm": (32, 48, 4, 12, 4),
          "left_sleeve": (48, 48, 4, 12, 4), "right_leg": (0, 16, 4, 12, 4), "right_pants": (0, 32, 4, 12, 4),
          "left_leg": (16, 48, 4, 12, 4), "left_pants": (0, 48, 4, 12, 4)}
# The plain humanoid model (Isis): one arm and one leg, mirrored, and the hat layer.
HUMANOID = {k: PLAYER[k] for k in ("head", "hat", "body", "right_arm", "right_leg")}


def rgb(c, a=255):
    if isinstance(c, tuple):
        return c if len(c) == 4 else (*c, a)
    return ((c >> 16) & 255, (c >> 8) & 255, c & 255, a)


def scale(c, f):
    c = rgb(c)
    return (min(255, int(c[0] * f)), min(255, int(c[1] * f)), min(255, int(c[2] * f)), c[3])


def mix(a, b, t):
    a, b = rgb(a), rgb(b)
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)


def faces(u, v, w, h, d):
    """Rectangles of a cube's faces in texels: name -> (x, y, width, height)."""
    u, v, w, h, d = u * K, v * K, w * K, h * K, d * K
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}


SIDES = ("front", "right", "left", "back")


class Canvas:
    def __init__(self, rng, layout):
        self.img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        self.rng = rng
        self.layout = layout
        self.part = {name: faces(*box) for name, box in layout.items()}

    def put(self, x, y, c, noise=2):
        c = rgb(c)
        if noise:
            n = self.rng.randint(-noise, noise)
            c = (max(0, min(255, c[0] + n)), max(0, min(255, c[1] + n)), max(0, min(255, c[2] + n)), c[3])
        self.img.putpixel((x, y), c)

    def get(self, x, y):
        return self.img.getpixel((x, y))

    def rect(self, x, y, w, h, c, noise=2):
        for j in range(y, y + h):
            for i in range(x, x + w):
                self.put(i, j, c, noise)

    def fill(self, part, c, names=None, noise=2):
        for name, r in self.part[part].items():
            if names is None or name in names:
                self.rect(*r, c, noise)

    def has(self, part):
        return part in self.part

    def shade(self):
        """Light from above on every face of every part, and a soft gradient down each side face."""
        for rects in self.part.values():
            for name, (x, y, w, h) in rects.items():
                for j in range(h):
                    f = FACE_LIGHT[name] * ((1.03 - 0.08 * j / max(1, h - 1)) if name in SIDES else 1.0)
                    for i in range(w):
                        c = self.get(x + i, y + j)
                        if c[3]:
                            self.img.putpixel((x + i, y + j), scale(c, f))

    def done(self):
        self.shade()
        self.img.info[HD_MARK] = "1"
        return self.img


# ---------------------------------------------------------------- hair

def strand(cv, base, col, row, sheen_row=None, wave=False):
    """The colour of one texel of hair: strands of light and dark, a sheen across the crown, darker tips."""
    f = 0.9 + 0.16 * math.sin(col * 1.7 + (math.sin(row * 0.5) * 1.2 if wave else 0.0)) + 0.06 * math.sin(col * 0.6 + 1.3)
    if sheen_row is not None and abs(row - sheen_row) <= 1:
        f += 0.18 - 0.07 * abs(row - sheen_row)
    return scale(base, f)


def hair_rect(cv, rect, base, sheen=None, wave=False, tips=True):
    x, y, w, h = rect
    for j in range(h):
        for i in range(w):
            c = strand(cv, base, x + i, j, sheen, wave)
            if tips and j >= h - 2:
                c = scale(c, 0.86)
            cv.put(x + i, y + j, c, 1)


def paint_hair(cv, spec):
    """Hair on the head and its volume on the hat layer; long hair also down the back of the body."""
    hair, style, egypt = spec["hair"], spec["style"], spec["culture"] == "egypt"
    wave = style == "wavy"
    head, hat = cv.part["head"], cv.part["hat"]
    for name in ("top", "back", "right", "left"):
        hair_rect(cv, head[name], hair, sheen=None if name == "top" else 3, wave=wave, tips=False)
    x, y, w, h = head["top"]                                    # the parting
    if not egypt:
        cv.rect(x + w // 2, y, 1, h, scale(hair, 0.72), 1)
    fx, fy, fw, fh = head["front"]
    if egypt:                                                   # the black wig: a straight fringe, a blunt bob
        hair_rect(cv, (fx, fy, fw, 5), hair, sheen=1, tips=False)
        for j in range(5, fh):
            for i in (0, 1, fw - 2, fw - 1):
                cv.put(fx + i, fy + j, strand(cv, hair, fx + i, j, None))
    else:                                                       # a soft fringe swept to the side, locks framing the face
        for i in range(fw):
            depth = 4 + (1 if (i + 1) % 5 == 0 else 0) - (1 if i in (6, 7) else 0)
            for j in range(depth):
                cv.put(fx + i, fy + j, strand(cv, hair, fx + i, j, 1, wave))
        for j in range(4, fh - (0 if style in ("long", "wavy") else 3)):
            for i in (0, fw - 1):
                cv.put(fx + i, fy + j, strand(cv, hair, fx + i, j, None, wave))
    # The hat layer: hair standing a little off the head on top, the sides and the back.
    hx, hy, hw, hh = hat["top"]
    hair_rect(cv, hat["top"], hair, sheen=None, wave=wave, tips=False)
    for name in ("back", "right", "left"):
        x, y, w, h = hat[name]
        bottom = h if (style in ("long", "wavy") or egypt) else h - 4
        hair_rect(cv, (x, y, w, bottom), hair, sheen=3, wave=wave)
    x, y, w, h = hat["front"]
    for i in range(w):                                          # only the edge of the fringe, the face stays clear
        cv.put(x + i, y, strand(cv, hair, x + i, 0, None, wave))
    if egypt:
        for j in range(1, h):
            for i in (0, w - 1):
                cv.put(x + i, y + j, strand(cv, hair, x + i, j, None))
    # Long hair down the back (jacket layer of the player model).
    if cv.has("jacket"):
        x, y, w, h = cv.part["jacket"]["back"]
        if style in ("long", "wavy") or egypt:
            length = 10 if egypt else 16
            for j in range(length):
                inset = 0 if j < length - 3 else (j - length + 4)
                for i in range(inset, w - inset):
                    cv.put(x + i, y + j, strand(cv, hair, x + i, j, None, wave))
        elif style == "braid":
            for j in range(18):
                c = scale(hair, 1.12 if (j // 2) % 2 == 0 else 0.84)
                cv.rect(x + w // 2 - 2 + (1 if (j // 2) % 2 else 0), y + j, 3, 1, c, 1)
            cv.rect(x + w // 2 - 1, y + 18, 2, 1, spec.get("band") or spec["trim"], 1)
        elif style == "ponytail":
            for j in range(14):
                width = 4 if j < 10 else 2
                cv.rect(x + w // 2 - width // 2, y + j, width, 1, strand(cv, hair, x + w // 2, j, None), 1)
        elif style == "twin":
            fx, fy, fw, fh = cv.part["jacket"]["front"]          # two braids over the shoulders, in front
            for bx in (fx + 1, fx + fw - 3):
                for j in range(12):
                    cv.rect(bx, fy + j, 2, 1, scale(hair, 1.12 if (j // 2) % 2 == 0 else 0.84), 1)
                cv.rect(bx, fy + 12, 2, 1, spec.get("band") or spec["trim"], 1)


# ---------------------------------------------------------------- the face

def paint_face(cv, spec):
    fx, fy, fw, fh = cv.part["head"]["front"]
    skin, eyes = spec["skin"], spec["eyes"]
    egypt = spec["culture"] == "egypt"
    kohl = rgb(0x120C0A)
    brow = mix(mix(spec["hair"], 0x1A1210, 0.35), skin, 0.3)
    white, iris = rgb(0xF6F2EE), rgb(eyes)
    for left, right in ((3, 6), (9, 12)):                       # brows, eyes with lashes, iris and a glint
        for i in range(left + (1 if left < 8 else 0), right + (0 if left < 8 else -1) + 1):
            outer_end = i == (left + 1 if left < 8 else right - 1)
            cv.put(fx + i, fy + 5 + (1 if outer_end and not egypt else 0), brow, 1)
        for i in range(left, right + 1):
            cv.put(fx + i, fy + 7, kohl, 0)
        outer = left - 1 if left < 8 else right + 1
        cv.put(fx + outer, fy + 7 - (1 if egypt else 0), kohl, 0)   # the lashes (a kohl wing for the Egyptians)
        if egypt:
            cv.put(fx + (outer - 1 if left < 8 else outer + 1), fy + 6, kohl, 0)
        inner_white, outer_white = (right, left) if left < 8 else (left, right)
        cv.put(fx + outer_white, fy + 8, white, 0)
        cv.put(fx + inner_white, fy + 8, mix(white, skin, 0.4), 0)
        for i in range(left + 1, right):
            cv.put(fx + i, fy + 8, scale(iris, 0.7), 0)
            cv.put(fx + i, fy + 9, iris, 0)
        cv.put(fx + left + 1, fy + 8, mix(iris, white, 0.75), 0)   # the glint
        for i in range(left, right + 1):
            cv.put(fx + i, fy + 10, mix(skin, iris, 0.08) if i in (left, right) else scale(skin, 0.95), 1)
    cv.put(fx + 8, fy + 11, scale(skin, 0.86), 1)               # the nose
    cv.put(fx + 7, fy + 10, scale(skin, 1.04), 1)
    lips = rgb(spec["lips"])
    for i in range(6, 10):
        cv.put(fx + i, fy + 13, scale(lips, 0.86), 1)
        cv.put(fx + i, fy + 14, lips if i in (7, 8) else scale(lips, 0.94), 1)
    cv.put(fx + 5, fy + 13, scale(skin, 0.9), 1)
    cv.put(fx + 10, fy + 13, scale(skin, 0.9), 1)
    for cx in (3, 12):                                          # blush
        cv.put(fx + cx, fy + 11, mix(skin, 0xE86A7A, 0.22), 1)
        cv.put(fx + cx + (1 if cx < 8 else -1), fy + 11, mix(skin, 0xE86A7A, 0.14), 1)
    for i in range(2, 14):
        cv.put(fx + i, fy + 15, scale(skin, 0.93), 1)


# ---------------------------------------------------------------- jewellery and borders

def meander(cv, x, y, w, c):
    """A Greek key border, two texels high."""
    dark = scale(c, 0.7)
    for i in range(w):
        k = i % 4
        cv.put(x + i, y, c if k != 3 else dark, 0)
        cv.put(x + i, y + 1, c if k in (0, 3) else dark, 0)


def beads(cv, x, y, w, colours):
    for i in range(w):
        c = colours[i % len(colours)]
        cv.put(x + i, y, c, 0)


def band_around(cv, part, row, c, rows=1, names=SIDES, accent=None):
    for name in names:
        x, y, w, h = cv.part[part][name]
        cv.rect(x, y + row, w, rows, c, 1)
        if accent is not None and name == "front":
            cv.put(x + w // 2 - 1, y + row, accent, 0)


def broad_collar(cv, part, rich=False):
    """The usekh: rows of gold, lapis, turquoise and carnelian beads across the chest and shoulders."""
    rows = [GOLD, LAPIS, GOLD, TURQUOISE, GOLD, CARNELIAN, GOLD_LIGHT] if rich else [GOLD, LAPIS, TURQUOISE, GOLD, CARNELIAN]
    x, y, w, h = cv.part[part]["front"]
    for j, c in enumerate(rows):
        inset = max(0, j - 2)
        for i in range(inset, w - inset):
            cv.put(x + i, y + j, scale(c, 1.15) if (i + j) % 3 == 0 else c, 0)
    for name in ("back", "right", "left"):
        bx, by, bw, bh = cv.part[part][name]
        for j, c in enumerate(rows[:3]):
            cv.rect(bx, by + j, bw, 1, c, 0)
    tx, ty, tw, th = cv.part[part]["top"]
    cv.rect(tx, ty, tw, th, GOLD, 1)
    return x, y + len(rows), w


def arm_rings(cv, arm, metal, upper=True, wrist=True, stone=None):
    if upper:
        band_around(cv, arm, 6, metal, 2, accent=stone)
    if wrist:
        band_around(cv, arm, 19, metal, 2, accent=stone)


# ---------------------------------------------------------------- outfits

def pleats(cv, rect, c, every=3):
    x, y, w, h = rect
    for j in range(h):
        for i in range(w):
            k = (x + i) % every
            cv.put(x + i, y + j, scale(c, 1.06 if k == 0 else 0.9 if k == every - 1 else 1.0), 1)


def draw_dress(cv, spec, length_on_legs):
    """A long dress: the body, then the legs down to {@code length_on_legs} texels, pleated, with a border at the hem."""
    d, trim = spec["dress"], spec["trim"]
    for name in SIDES:
        pleats(cv, cv.part["body"][name], d)
    for leg in legs(cv):
        for name in SIDES:
            x, y, w, h = cv.part[leg][name]
            pleats(cv, (x, y, w, length_on_legs), d)
            if spec["culture"] == "greek":
                meander(cv, x, y + length_on_legs - 3, w, rgb(trim))
            else:
                cv.rect(x, y + length_on_legs - 2, w, 1, trim, 0)
    x, y, w, h = cv.part["body"]["front"]
    if spec["culture"] == "greek":
        meander(cv, x, y, w, rgb(trim))                         # the neckline


def draw_belt(cv, spec, row=14):
    c = spec.get("girdle") or spec.get("belt") or spec["trim"]
    band_around(cv, "body", row, c, 2)
    x, y, w, h = cv.part["body"]["front"]
    cv.put(x + w // 2 - 1, y + row, scale(c, 1.3), 0)           # the buckle or knot
    cv.put(x + w // 2, y + row, scale(c, 1.3), 0)
    if spec.get("girdle"):                                      # Hippolyta's girdle: a red stone in gold
        cv.rect(x + w // 2 - 1, y + row, 2, 2, 0xC0262E, 0)


def sandals(cv, spec, lace_rows=4):
    strap = spec.get("bronze") if spec["culture"] == "greek" else GOLD if spec["culture"] == "egypt" else 0x5A3A20
    for leg in legs(cv):
        for name in SIDES:
            x, y, w, h = cv.part[leg][name]
            cv.rect(x, y + h - 1, w, 1, scale(strap, 0.8), 0)
            for j in range(1, lace_rows):
                for i in range(w):
                    if (i + j) % 3 == 0:
                        cv.put(x + i, y + h - 1 - j, strap, 0)
        bx, by, bw, bh = cv.part[leg]["bottom"]
        cv.rect(bx, by, bw, bh, 0x6A4A2A, 1)


def legs(cv):
    return [p for p in ("right_leg", "left_leg") if cv.has(p)]


def arms(cv):
    return [p for p in ("right_arm", "left_arm") if cv.has(p)]


def sleeves(cv):
    return [p for p in ("right_sleeve", "left_sleeve") if cv.has(p)]


def cuirass(cv, spec):
    """A bronze muscle cuirass over a short chiton, leather strips (pteruges) below it, greaves on the shins."""
    bronze = rgb(spec.get("bronze", 0xC9963E))
    for name in SIDES:
        cv.rect(*cv.part["body"][name], bronze, 2)
    x, y, w, h = cv.part["body"]["front"]
    dark, light = scale(bronze, 0.72), scale(bronze, 1.22)
    for i in range(w):                                          # the chest and the ribs of the armour
        cv.put(x + i, y + 8, dark, 0)
    for j in range(2, 8):
        cv.put(x + w // 2, y + j, dark, 0)
    for j in (11, 14, 17):
        cv.rect(x + 3, y + j, w - 6, 1, dark, 0)
    for i in (3, w - 4):
        cv.put(x + i, y + 4, light, 0)
    cv.rect(x, y, w, 1, light, 0)
    for leg in legs(cv):
        for name in SIDES:
            lx, ly, lw, lh = cv.part[leg][name]
            for i in range(lw):                                 # the pteruges: strips of leather with bronze tips
                c = 0x7A4A24 if i % 2 == 0 else 0x5A341A
                cv.rect(lx + i, ly, 1, 6, c, 1)
                cv.put(lx + i, ly + 6, bronze, 0)
            cv.rect(lx, ly + 7, lw, 3, spec["dress"], 1)
            cv.rect(lx, ly + 14, lw, 8, bronze, 2)               # the greaves
            cv.rect(lx, ly + 14, lw, 1, light, 0)


def huntress(cv, spec):
    """A short tunic to mid-thigh, a leather belt and the strap of the quiver across the chest, bracers and boots."""
    for name in SIDES:
        pleats(cv, cv.part["body"][name], spec["dress"], 4)
    for leg in legs(cv):
        for name in SIDES:
            x, y, w, h = cv.part[leg][name]
            pleats(cv, (x, y, w, 7), spec["dress"], 4)
            cv.rect(x, y + 6, w, 1, spec["trim"], 0)
            cv.rect(x, y + 15, w, 9, 0x6A4424, 1)                # tall boots
            cv.rect(x, y + 15, w, 1, 0x8A5A30, 0)
    x, y, w, h = cv.part["body"]["front"]
    for j in range(h - 6):                                      # the quiver strap
        cv.rect(x + int(j * (w - 2) / (h - 6)), y + j, 2, 1, 0x5A3418, 0)
    for arm in arms(cv):
        band_around(cv, arm, 15, 0x6A4424, 6)


def valkyrie(cv, spec):
    """A mail shirt over a long dress, a fur mantle over the shoulders, bracers and a broad belt."""
    steel = rgb(0xA8ACB4)
    for name in SIDES:
        x, y, w, h = cv.part["body"][name]
        for j in range(h):
            for i in range(w):
                cv.put(x + i, y + j, scale(steel, 1.15 if (i + (j % 2)) % 2 == 0 else 0.78), 1)
    for leg in legs(cv):
        for name in SIDES:
            x, y, w, h = cv.part[leg][name]
            pleats(cv, (x, y, w, 20), spec["dress"], 3)
            cv.rect(x, y + 18, w, 2, spec["trim"], 0)
            for j in range(3):                                  # the mail hangs over the dress
                for i in range(w):
                    cv.put(x + i, y + j, scale(steel, 1.12 if (i + j) % 2 == 0 else 0.78), 1)
    fur, fur_dark = rgb(0xE8E0D0), rgb(0xA89A84)
    for part in ["body"] + arms(cv):
        for name in SIDES:
            x, y, w, h = cv.part[part][name]
            for i in range(w):
                depth = 4 + (1 if (i * 7) % 3 == 0 else 0)
                for j in range(depth):
                    cv.put(x + i, y + j, fur if (i + j) % 3 else fur_dark, 3)
        cv.rect(*cv.part[part]["top"], fur, 3)
    for arm in arms(cv):
        for name in SIDES:
            x, y, w, h = cv.part[arm][name]
            for j in range(5, 13):
                for i in range(w):
                    cv.put(x + i, y + j, scale(steel, 1.1 if (i + j) % 2 == 0 else 0.8), 1)
        band_around(cv, arm, 16, 0x6A4424, 6)
        band_around(cv, arm, 17, spec["trim"], 1)


def winged_helm(cv, spec):
    """The valkyrie's helmet: a steel cap with a nose guard, and white wings on its sides (the hat layer)."""
    metal = rgb(spec.get("helm") or 0xC8CCD4)
    full = spec.get("helm") is not None
    hat = cv.part["hat"]
    for name in ("top",) if full else ():
        cv.rect(*hat[name], metal, 2)
    for name in ("back", "right", "left", "front"):
        x, y, w, h = hat[name]
        rows = 6 if full else 2
        cv.rect(x, y, w, rows, metal, 2)
        cv.rect(x, y + rows, w, 1, scale(metal, 0.7), 0)
        if name == "front" and full:
            cv.rect(x + w // 2 - 1, y + rows, 2, 4, scale(metal, 0.85), 0)
            cv.rect(x, y + rows, w, 1, spec["trim"], 0)
    feather, shadow, quill = rgb(0xF6F4F0), rgb(0xC8C8D2), rgb(0x9A9AA8)
    for name in ("right", "left"):                              # the wings: three rows of feathers swept up and back
        x, y, w, h = hat[name]
        rows = (6, 4, 3) if full else (3, 2)
        top = 1
        for k, length in enumerate(rows):
            span = w - 2 - k * 3 if full else (w // 2) - k * 2
            for j in range(length):
                for i in range(max(1, span - j)):
                    px = x + (i if name == "left" else w - 1 - i)
                    c = quill if j == length - 1 else shadow if i % 3 == 2 else feather
                    cv.put(px, y + top + j, c, 1)
            top += length

def egyptian_sheath(cv, spec):
    """A sheath of fine linen from under the collar to the ankles, a sash with long ends, the broad collar."""
    linen = rgb(spec.get("dress") or LINEN)
    for name in SIDES:
        pleats(cv, cv.part["body"][name], linen, 2)
    for leg in legs(cv):
        for name in SIDES:
            x, y, w, h = cv.part[leg][name]
            pleats(cv, (x, y, w, h - 3), linen, 2)
            cv.rect(x, y + h - 5, w, 1, spec["trim"], 0)
    sash = spec.get("belt") or spec["trim"]
    band_around(cv, "body", 15, sash, 2)
    x, y, w, h = cv.part["body"]["front"]
    cv.rect(x + w // 2 - 1, y + 17, 2, 7, sash, 1)              # the ends of the sash
    for leg in legs(cv):
        lx, ly, lw, lh = cv.part[leg]["front"]
        cv.rect(lx + (lw - 1 if leg == "right_leg" else 0), ly, 1, 6, sash, 1)
    broad_collar(cv, "body")
    if cv.has("jacket"):
        broad_collar(cv, "jacket")
        jx, jy, jw, jh = cv.part["jacket"]["front"]
        cv.rect(jx, jy + 7, jw, jh - 7, (0, 0, 0, 0), 0)


def diadem(cv, spec, uraeus=True):
    """A golden band round the wig with the rearing cobra (or a lotus) at the brow."""
    gold = rgb(spec.get("crown") or spec.get("band") or GOLD)
    band_around(cv, "hat", 4, gold, 1, names=("front", "back", "right", "left"))
    x, y, w, h = cv.part["hat"]["front"]
    cv.rect(x + 1, y + 4, w - 2, 1, gold, 0)
    for i in range(2, w - 2, 3):
        cv.put(x + i, y + 4, LAPIS, 0)
    if uraeus:
        cv.rect(x + w // 2 - 1, y + 1, 2, 3, gold, 0)
        cv.put(x + w // 2 - 1, y + 1, CARNELIAN, 0)
    if spec.get("flower"):
        rx, ry, rw, rh = cv.part["hat"]["right"]
        for dx, dy in ((1, 3), (2, 2), (3, 3), (2, 4), (2, 3)):
            cv.put(rx + dx, ry + dy, spec["flower"] if (dx, dy) != (2, 3) else GOLD_LIGHT, 0)


def greek_headwear(cv, spec):
    x, y, w, h = cv.part["hat"]["front"]
    if spec.get("crown"):                                       # a golden crown of leaves
        for name in ("front", "back", "right", "left"):
            cx, cy, cw, ch = cv.part["hat"][name]
            for i in range(cw):
                cv.put(cx + i, cy + 1, spec["crown"], 0)
                if i % 3 == 1:
                    cv.put(cx + i, cy, scale(spec["crown"], 1.15), 0)
        cv.put(x + w // 2, y + 2, 0xC0262E, 0)
    elif spec.get("band"):
        band_around(cv, "hat", 2, spec["band"], 1, names=("front", "back", "right", "left"))
    if spec.get("flower"):
        rx, ry, rw, rh = cv.part["hat"]["right"]
        for dx, dy in ((1, 2), (2, 1), (3, 2), (2, 3)):
            cv.put(rx + dx, ry + dy, spec["flower"], 0)
        cv.put(rx + 2, ry + 2, GOLD_LIGHT, 0)


# ---------------------------------------------------------------- the painter

def heroine(rng, skin, hair, dress, trim, eyes=0x4A3320, outfit="chiton", style="long", belt=None, crown=None,
            girdle=None, flower=None, band=None, lips=0xD87A84, bronze=0xC9963E, helm=None, culture=None):
    """One woman of the myths; the arguments are those of textures.amazon (culture: greek, norse or egypt)."""
    if culture is None:
        culture = "norse" if outfit == "valkyrie" else "greek"
    spec = dict(skin=rgb(skin), hair=rgb(hair), dress=rgb(dress), trim=rgb(trim), eyes=eyes, outfit=outfit, style=style,
                belt=belt, crown=crown, girdle=girdle, flower=flower, band=band, lips=lips, bronze=bronze, helm=helm,
                culture=culture)
    cv = Canvas(rng, PLAYER)
    for part in ("head", "body") + tuple(arms(cv)) + tuple(legs(cv)):
        cv.fill(part, spec["skin"], noise=1)
    paint_hair(cv, spec)
    paint_face(cv, spec)
    metal = GOLD if culture == "egypt" else rgb(bronze) if culture == "greek" else 0xC8CCD4
    if culture == "egypt":
        egyptian_sheath(cv, spec)
        diadem(cv, spec)
        for arm in arms(cv):
            arm_rings(cv, arm, GOLD, stone=TURQUOISE)
        sandals(cv, spec, 2)
    elif culture == "norse":
        valkyrie(cv, spec)
        belt_spec = dict(spec, girdle=None)
        draw_belt(cv, belt_spec, 14)
        winged_helm(cv, spec)
        sandals(cv, spec, 1)
    else:
        if outfit == "cuirass":
            cuirass(cv, spec)
        elif outfit == "huntress":
            huntress(cv, spec)
        else:
            draw_dress(cv, spec, 18 if outfit == "chiton" else 20)
            if outfit == "peplos":                              # the fold of the peplos over the chest
                x, y, w, h = cv.part["body"]["front"]
                cv.rect(x, y + 9, w, 1, scale(spec["dress"], 0.78), 0)
                meander(cv, x, y + 10, w, rgb(trim))
        if outfit != "huntress":
            draw_belt(cv, spec, 13 if outfit != "cuirass" else 20)
        for arm in arms(cv):
            arm_rings(cv, arm, metal, wrist=outfit != "huntress")
        if outfit != "huntress":
            sandals(cv, spec, 5)
        greek_headwear(cv, spec)
    return cv.done()


def isis(rng):
    """Isis: a royal priestess on the plain humanoid layout, the throne sign on her head, a white sheath with a red sash,
    the rich collar with the knot of Isis and the wings of the goddess, feathered in carnelian, lapis and turquoise,
    down her arms."""
    spec = dict(skin=rgb(0xC8956B), hair=rgb(0x0E0A0A), dress=rgb(0xF6F2E8), trim=rgb(GOLD), eyes=0x2A1E14, outfit="sheath",
                style="long", belt=0xB02A24, crown=GOLD, girdle=None, flower=None, band=None, lips=0xA8505A, bronze=GOLD,
                helm=None, culture="egypt")
    cv = Canvas(rng, HUMANOID)
    for part in ("head", "body", "right_arm", "right_leg"):
        cv.fill(part, spec["skin"], noise=1)
    paint_hair(cv, spec)
    paint_face(cv, spec)
    egyptian_sheath(cv, spec)
    x, y, w, h = cv.part["body"]["front"]
    broad_collar(cv, "body", rich=True)
    cv.rect(x + w // 2 - 1, y + 8, 2, 3, 0xB02A24, 0)           # the knot of Isis (tyet) below the collar
    cv.put(x + w // 2 - 1, y + 8, GOLD_LIGHT, 0)
    diadem(cv, spec, uraeus=True)
    hat = cv.part["hat"]
    for name in ("front", "back"):                              # the throne sign above her brow
        hx, hy, hw, hh = hat[name]
        cx = hx + hw // 2 - 3
        cv.rect(cx, hy, 2, 4, LAPIS, 0)
        cv.rect(cx, hy + 3, 6, 1, LAPIS, 0)
        cv.rect(cx + 4, hy + 1, 2, 2, LAPIS, 0)
        cv.put(cx, hy, GOLD_LIGHT, 0)
    # The wings of the goddess down her arm: rows of feathers, each with a dark rib and a light tip.
    colours = (LAPIS, TURQUOISE, CARNELIAN)
    for name in ("front", "back", "right", "left"):
        ax, ay, aw, ah = cv.part["right_arm"][name]
        cv.rect(ax, ay + 2, aw, 2, GOLD, 0)                     # the golden edge of the wing at the shoulder
        for j in range(4, ah - 4):
            row, inside = (j - 4) // 4, (j - 4) % 4
            c = rgb(colours[row % 3])
            for i in range(aw):
                scallop = (i + row * 2) % 4                     # rounded feather tips, overlapping like scales
                if inside == 3 and scallop in (0, 3):
                    cv.put(ax + i, ay + j, scale(c, 0.62), 0)
                elif inside == 3:
                    cv.put(ax + i, ay + j, scale(c, 1.2), 0)
                else:
                    cv.put(ax + i, ay + j, scale(c, 0.84) if scallop == 0 else c, 1)
    arm_rings(cv, "right_arm", GOLD, upper=False, stone=CARNELIAN)
    sandals(cv, spec, 2)
    return cv.done()
