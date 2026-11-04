"""Structure templates of the Duat, written as .nbt files. Same conventions as structures.py: x east, y up, z south,
origin at the corner, y = 0 is the ground the template stands on."""
import math
import random

from structures import AIR, Template, pick

NS = "mythsofworlds"
PYRAMID = f"{NS}:pyramid_stone"
GLYPHS = f"{NS}:hieroglyph_stone"
SAND = [("minecraft:sand", 70), ("minecraft:smooth_sandstone", 15), ("minecraft:sandstone", 15)]
RED_SAND = [("minecraft:red_sand", 60), ("minecraft:red_sandstone", 25), ("minecraft:terracotta", 15)]
MUD_BRICK = [("minecraft:mud_bricks", 80), ("minecraft:packed_mud", 20)]
LANTERN = "minecraft:lantern[hanging=true]"
STANDING_LANTERN = "minecraft:lantern[hanging=false]"
SOUL_LANTERN = "minecraft:soul_lantern[hanging=false]"
FIRE_BOWL = "minecraft:campfire[lit=true,signal_fire=false]"
SOUL_FIRE = "minecraft:soul_campfire[lit=true,signal_fire=false]"
PALM_LEAVES = f"{NS}:date_palm_leaves[age=3,distance=7,persistent=true,waterlogged=false]"
PALM_LEAVES_GREEN = f"{NS}:date_palm_leaves[age=0,distance=7,persistent=true,waterlogged=false]"


def stairs(block, facing, half="bottom"):
    return f"minecraft:{block}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]"


def ground(t, rng, palette=SAND):
    sx, sy, sz = t.size
    for x in range(sx):
        for z in range(sz):
            t.set(x, 0, z, pick(rng, palette))
    t.fill(0, 1, 0, sx - 1, sy - 1, sz - 1, AIR)


def column(t, x, z, y0, height, shaft="minecraft:cut_sandstone", capital="minecraft:chiseled_sandstone"):
    """A papyrus column: a smooth shaft with a carved capital and a wider abacus under the roof."""
    t.set(x, y0, z, "minecraft:smooth_sandstone")
    for y in range(y0 + 1, y0 + height - 1):
        t.set(x, y, z, shaft)
    t.set(x, y0 + height - 1, z, capital)


def palm(t, x, z, height, rng):
    """A date palm: a straight trunk of jungle wood and a crown of fronds drooping to four sides."""
    for y in range(1, height + 1):
        t.set(x, y, z, "minecraft:jungle_log[axis=y]")
    top = height + 1
    t.set(x, top, z, PALM_LEAVES)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        for i in (1, 2):
            if t.inside(x + dx * i, top, z + dz * i):
                t.set(x + dx * i, top, z + dz * i, PALM_LEAVES if rng.random() < 0.4 else PALM_LEAVES_GREEN)
        if t.inside(x + dx * 3, top - 1, z + dz * 3):
            t.set(x + dx * 3, top - 1, z + dz * 3, PALM_LEAVES_GREEN)
    for dx, dz in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
        if t.inside(x + dx, top, z + dz):
            t.set(x + dx, top, z + dz, PALM_LEAVES_GREEN)


# ---------------------------------------------------------------- the village on the Nile

def house(t, x0, z0, rng, chest=None, merchant=None, length=7, width=6):
    """A house of mud brick with a flat roof and a parapet, its door in the middle of the south wall: inside a reed
    mat, a clay oven, jars and a chest. Stairs at the back lead to the roof, where people sleep in the heat."""
    x1, z1 = x0 + length - 1, z0 + width - 1
    top = 4
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            t.set(x, 0, z, "minecraft:smooth_sandstone" if edge else "minecraft:packed_mud")
            for y in range(1, top):
                t.set(x, y, z, pick(rng, MUD_BRICK) if edge else AIR)
            t.set(x, top, z, "minecraft:smooth_sandstone")
            if edge:
                t.set(x, top + 1, z, "minecraft:mud_brick_wall" if (x + z) % 2 else "minecraft:mud_brick_slab[type=bottom,waterlogged=false]")
    mx = x0 + length // 2
    t.set(mx, 1, z1, AIR)
    t.set(mx, 2, z1, AIR)
    t.set(mx, 3, z1, "minecraft:smooth_sandstone_slab[type=top,waterlogged=false]")
    for wx in (x0 + 1, x1 - 1):
        t.set(wx, 2, z1, "minecraft:spruce_trapdoor[facing=south,half=top,open=true,powered=false,waterlogged=false]")
    t.set(x0, 2, z0 + width // 2, AIR)
    t.set(x1, 2, z0 + width // 2, AIR)
    for x in range(x0 + 1, x1):
        t.set(x, 1, z0 + width // 2, "minecraft:yellow_carpet")
    t.set(x0 + 1, 1, z0 + 1, "minecraft:smoker[facing=south,lit=true]")
    t.set(x1 - 1, 1, z0 + 1, "minecraft:decorated_pot[facing=south,cracked=false,waterlogged=false]")
    t.set(x1 - 1, 1, z1 - 1, "minecraft:barrel[facing=up,open=false]")
    t.set(mx, top - 1, z0 + 1, LANTERN)
    if chest:
        t.chest(x0 + 1, 1, z1 - 1, chest, facing="east")
    if merchant is not None:
        t.entity(mx + 0.5, 1.0, z0 + width // 2 + 0.5, f"{NS}:egyptian_merchant", {"Kind": merchant})


def egyptian_village():
    sx, sy, sz = 42, 14, 38
    t = Template(sx, sy, sz)
    rng = random.Random(201)
    ground(t, rng, [("minecraft:sand", 55), ("minecraft:grass_block[snowy=false]", 30), ("minecraft:packed_mud", 15)])
    # A canal from the Nile runs across the village, with fields of papyrus and wheat along it.
    for x in range(sx):
        for z in range(17, 21):
            t.set(x, 0, z, "minecraft:water" if z in (18, 19) else f"{NS}:nile_silt")
        if x % 3 == 0:
            t.set(x, 1, 17, "minecraft:sugar_cane[age=0]")
            t.set(x, 2, 17, "minecraft:sugar_cane[age=0]")
        if x % 5 == 2:
            t.set(x, 1, 18, "minecraft:lily_pad")
    # A bridge of planks across the canal.
    for z in range(16, 22):
        for x in (20, 21):
            t.set(x, 1, z, "minecraft:jungle_slab[type=bottom,waterlogged=false]")
    house(t, 2, 3, rng, chest="egyptian_village", merchant=0)
    house(t, 12, 2, rng, chest="egyptian_house", length=8, width=7)
    house(t, 23, 3, rng, chest="egyptian_house", merchant=1)
    house(t, 33, 4, rng, chest="egyptian_house", merchant=2, length=7, width=6)
    house(t, 4, 25, rng, chest="egyptian_house")
    house(t, 26, 24, rng, chest="egyptian_house", length=8, width=7)
    # Fields of wheat between the houses and the canal, edged with the black silt of the Nile that makes them grow.
    for x in range(14, 24):
        for z in range(22, 30):
            if x in (14, 23) or z in (22, 29):
                t.set(x, 0, z, f"{NS}:nile_silt")
                continue
            t.set(x, 0, z, "minecraft:farmland[moisture=7]")
            t.set(x, 1, z, f"minecraft:wheat[age={rng.choice([5, 6, 7])}]")
    # Palms, a well and lanterns on posts.
    for x, z in ((10, 13), (30, 13), (2, 33), (38, 31), (12, 34), (36, 13)):
        palm(t, x, z, rng.randint(5, 7), rng)
    for x, z in ((19, 12), (35, 33)):
        t.set(x, 0, z, "minecraft:water")
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            t.set(x + dx, 1, z + dz, "minecraft:sandstone_wall")
    for x in range(3, sx - 2, 7):
        t.fill(x, 1, 15, x, 2, 15, "minecraft:sandstone_wall")
        t.set(x, 3, 15, STANDING_LANTERN)
    t.entity(17.5, 1.0, 13.5, f"{NS}:bastet_cat")
    t.entity(31.5, 1.0, 31.5, f"{NS}:bastet_cat")
    t.entity(8.5, 1.0, 22.5, "minecraft:cow")
    t.entity(36.5, 1.0, 22.5, "minecraft:sheep")
    return t


# ---------------------------------------------------------------- the temple of Isis

def pylon(t, x0, x1, z0, z1, height, rng):
    """A pylon tower: walls that lean inwards as they rise, with a cornice on top."""
    for y in range(1, height + 1):
        inset = y // 4
        for x in range(x0 + inset, x1 - inset + 1):
            for z in range(z0, z1 + 1):
                face = z in (z0, z1) or x in (x0 + inset, x1 - inset)
                t.set(x, y, z, (GLYPHS if (y % 4 == 2 and rng.random() < 0.5) else PYRAMID) if face else "minecraft:sandstone")
    for x in range(x0 + height // 4, x1 - height // 4 + 1):
        for z in range(z0, z1 + 1):
            t.set(x, height + 1, z, "minecraft:cut_sandstone_slab[type=bottom,waterlogged=false]")


def temple_of_isis():
    sx, sy, sz = 27, 15, 33
    t = Template(sx, sy, sz)
    rng = random.Random(202)
    ground(t, rng, SAND)
    c = sx // 2
    # The pylon gate in the south, a gateway between its towers.
    pylon(t, 1, c - 2, 27, 30, 10, rng)
    pylon(t, c + 2, sx - 2, 27, 30, 10, rng)
    for x in range(c - 1, c + 2):
        for z in range(27, 31):
            t.set(x, 0, z, "minecraft:smooth_sandstone")
            t.set(x, 7, z, "minecraft:chiseled_sandstone")
            t.set(x, 8, z, PYRAMID)
    # Banners of blue and gold on the towers.
    for x in (4, sx - 5):
        for y in range(3, 9):
            t.set(x, y, 31, "minecraft:blue_wool" if y % 2 else "minecraft:yellow_wool")
    # The courtyard: a sacred pool with lotus, columns along the sides, fire bowls.
    for x in range(3, sx - 3):
        for z in range(9, 26):
            t.set(x, 0, z, "minecraft:smooth_sandstone" if (x + z) % 2 else "minecraft:cut_sandstone")
    for x in range(c - 3, c + 4):
        for z in range(14, 21):
            edge = x in (c - 3, c + 3) or z in (14, 20)
            t.set(x, 0, z, "minecraft:chiseled_sandstone" if edge else "minecraft:water")
            if not edge and (x + z) % 3 == 0:
                t.set(x, 1, z, "minecraft:lily_pad")
    for z in range(10, 26, 3):
        for x in (4, sx - 5):
            column(t, x, z, 0, 7)
    for x, z in ((c - 5, 12), (c + 5, 12), (c - 5, 23), (c + 5, 23)):
        t.set(x, 1, z, FIRE_BOWL)
    # The sanctuary in the north, roofed and dim, with the throne of the goddess.
    for x in range(3, sx - 3):
        for z in range(1, 9):
            edge = x in (3, sx - 4) or z == 1
            t.set(x, 0, z, "minecraft:polished_blackstone" if (x + z) % 2 else "minecraft:lapis_block")
            for y in range(1, 8):
                t.set(x, y, z, (GLYPHS if y == 4 else PYRAMID) if edge else AIR)
            t.set(x, 8, z, PYRAMID)
    for x in range(c - 1, c + 2):
        for y in range(1, 5):
            t.set(x, y, 8, AIR)
    for x in range(3, sx - 3):
        if x not in range(c - 1, c + 2):
            for y in range(1, 8):
                t.set(x, y, 8, PYRAMID)
    for x in (c - 3, c + 3):
        column(t, x, 5, 0, 8)
    t.fill(c - 1, 1, 2, c + 1, 1, 3, "minecraft:gold_block")
    t.set(c, 2, 2, "minecraft:lapis_block")
    t.set(c, 3, 2, "minecraft:gold_block")
    t.set(c, 4, 2, "minecraft:end_rod[facing=up]")
    t.chest(c - 2, 1, 2, "temple_of_isis", facing="south")
    t.chest(c + 2, 1, 2, "temple_of_isis", facing="south")
    for x in (5, sx - 6):
        t.set(x, 6, 4, LANTERN)
    # The priestesses of Isis and the temple cats.
    for x, z in ((c - 4.5, 16.5), (c + 5.5, 18.5), (c + 0.5, 5.5)):
        t.entity(x, 1.0, z, f"{NS}:priestess")
    t.entity(c - 1.5, 1.0, 6.5, f"{NS}:isis")                  # the goddess herself before her throne
    t.entity(c - 6.5, 1.0, 21.5, f"{NS}:bastet_cat")
    t.entity(c + 6.5, 1.0, 11.5, f"{NS}:bastet_cat")
    for x, z in ((1, 3), (sx - 2, 3), (1, 20), (sx - 2, 20)):
        palm(t, x, z, rng.randint(5, 7), rng)
    return t


# ---------------------------------------------------------------- the obelisk

def obelisk():
    sx, sy, sz = 13, 18, 13
    t = Template(sx, sy, sz)
    rng = random.Random(203)
    ground(t, rng, SAND)
    c = 6
    for x in range(1, sx - 1):
        for z in range(1, sz - 1):
            t.set(x, 0, z, "minecraft:smooth_sandstone" if max(abs(x - c), abs(z - c)) < 5 else "minecraft:cut_sandstone")
    t.fill(c - 2, 1, c - 2, c + 2, 1, c + 2, "minecraft:smooth_sandstone")
    # The shaft, carved with hieroglyphs, narrowing to a pyramidion of gold.
    for y in range(2, 13):
        for x in range(c - 1, c + 2):
            for z in range(c - 1, c + 2):
                t.set(x, y, z, GLYPHS if (x == c or z == c) and y % 2 == 0 else PYRAMID)
    t.set(c, 13, c, PYRAMID)
    t.set(c, 14, c, "minecraft:gold_block")
    # An offering table with fire bowls and the chest of the priests.
    t.set(c, 2, c + 2, "minecraft:smooth_sandstone_slab[type=bottom,waterlogged=false]")
    t.chest(c, 2, c - 2, "obelisk", facing="north")
    for x, z in ((c - 3, c - 3), (c + 3, c - 3), (c - 3, c + 3), (c + 3, c + 3)):
        t.set(x, 1, z, "minecraft:sandstone_wall")
        t.set(x, 2, z, FIRE_BOWL)
    t.entity(c + 4.5, 1.0, c + 0.5, f"{NS}:scarab")
    return t


# ---------------------------------------------------------------- the tomb of the pharaoh

def pharaoh_tomb():
    sx, sy, sz = 27, 12, 29
    t = Template(sx, sy, sz)
    rng = random.Random(204)
    ground(t, rng, RED_SAND)
    stone = [("minecraft:sandstone", 50), ("minecraft:cut_sandstone", 25), (GLYPHS, 15), ("minecraft:smooth_sandstone", 10)]
    # A mastaba: a long low tomb with sloping walls, its entrance in the south, a burial hall inside.
    x0, x1, z0, z1 = 2, sx - 3, 2, sz - 3
    for y in range(1, 9):
        inset = (y - 1) // 3
        for x in range(x0 + inset, x1 - inset + 1):
            for z in range(z0 + inset, z1 - inset + 1):
                wall = x in (x0 + inset, x1 - inset) or z in (z0 + inset, z1 - inset)
                inner = x0 + 3 <= x <= x1 - 3 and z0 + 3 <= z <= z1 - 3 and y <= 6
                t.set(x, y, z, pick(rng, stone) if wall or not inner else AIR)
    c = sx // 2
    for z in range(z1 - 3, z1 + 1):
        for x in (c - 1, c, c + 1):
            for y in range(1, 4):
                t.set(x, y, z, AIR)
    for x in range(x0 + 3, x1 - 2):
        for z in range(z0 + 3, z1 - 2):
            t.set(x, 0, z, "minecraft:polished_blackstone_bricks" if (x + z) % 2 else "minecraft:chiseled_red_sandstone")
    # Pillars, soul fires, the sarcophagus of gold and lapis on a dais.
    for x in (x0 + 5, x1 - 5):
        for z in range(z0 + 6, z1 - 3, 5):
            column(t, x, z, 0, 7, shaft="minecraft:cut_red_sandstone", capital="minecraft:chiseled_red_sandstone")
            t.set(x + (1 if x < c else -1), 1, z, SOUL_FIRE)
    t.fill(c - 2, 1, z0 + 4, c + 2, 1, z0 + 8, "minecraft:smooth_sandstone")
    t.fill(c - 1, 2, z0 + 5, c + 1, 2, z0 + 7, "minecraft:lapis_block")
    t.set(c, 2, z0 + 6, "minecraft:gold_block")
    t.chest(c - 2, 2, z0 + 5, "pharaoh_tomb", facing="south")
    t.chest(c + 2, 2, z0 + 5, "pharaoh_tomb", facing="south")
    t.set(c, 1, z1 - 4, SOUL_LANTERN)
    t.entity(c + 0.5, 1.0, z0 + 11.5, f"{NS}:pharaoh_mummy")
    t.entity(c - 3.5, 1.0, z0 + 14.5, f"{NS}:mummy")
    t.entity(c + 4.5, 1.0, z0 + 14.5, f"{NS}:mummy")
    t.entity(c - 3.5, 1.0, z0 + 8.5, f"{NS}:ushabti")
    t.entity(c + 4.5, 1.0, z0 + 8.5, f"{NS}:ushabti")
    return t


# ---------------------------------------------------------------- the Great Sphinx

def great_sphinx():
    sx, sy, sz = 31, 16, 37
    t = Template(sx, sy, sz)
    rng = random.Random(205)
    ground(t, rng, SAND)
    c = sx // 2
    stone = [("minecraft:sandstone", 60), ("minecraft:smooth_sandstone", 25), ("minecraft:cut_sandstone", 15)]
    # The statue: a lion of stone lying with its paws stretched out to the south, its head raised under the nemes.
    for z in range(4, 22):
        for x in range(c - 4, c + 5):
            height = 6 if z < 16 else 5
            if abs(x - c) == 4 and (z < 6 or z > 19):
                continue
            for y in range(1, height + 1):
                t.set(x, y, z, pick(rng, stone))
    for z in range(1, 5):                                       # the tail curled along the back
        t.set(c + 3, 1, z, "minecraft:sandstone")
    for side in (-3, 2):                                        # the forepaws
        for z in range(22, 31):
            for x in range(c + side, c + side + 2):
                t.set(x, 1, z, "minecraft:smooth_sandstone")
                if z < 28:
                    t.set(x, 2, z, "minecraft:sandstone")
    head_z0 = 17
    for x in range(c - 3, c + 4):                               # the head with the striped nemes
        for z in range(head_z0, head_z0 + 6):
            for y in range(6, 13):
                face = z == head_z0 + 5
                band = (y + abs(x - c)) % 2
                nemes = "minecraft:yellow_terracotta" if band else "minecraft:blue_terracotta"
                t.set(x, y, z, "minecraft:smooth_sandstone" if face and abs(x - c) <= 2 and y <= 11 else nemes)
    for x in (c - 1, c + 1):
        t.set(x, 10, head_z0 + 5, "minecraft:black_terracotta")      # the eyes
    t.set(c, 8, head_z0 + 6, "minecraft:smooth_sandstone")           # the nose
    t.set(c, 7, head_z0 + 6, "minecraft:sandstone")
    for y in range(6, 11):                                      # the lappets of the nemes down to the chest
        for x in (c - 4, c + 4):
            t.set(x, y, head_z0 + 4, "minecraft:blue_terracotta" if y % 2 else "minecraft:yellow_terracotta")
    t.set(c, 13, head_z0 + 3, "minecraft:gold_block")           # the uraeus
    # A small temple between the paws with the hoard, and two obelisks at the front.
    for x in range(c - 1, c + 2):
        for z in range(26, 30):
            t.set(x, 0, z, "minecraft:smooth_sandstone")
    t.chest(c, 1, 27, "great_sphinx", facing="south")
    t.chest(c, 1, 25, "great_sphinx", facing="south")
    for x in (2, sx - 3):
        for y in range(1, 9):
            t.set(x, y, 33, GLYPHS if y % 2 else PYRAMID)
        t.set(x, 9, 33, "minecraft:gold_block")
    for x, z in ((c - 7, 31), (c + 7, 31)):
        t.set(x, 1, z, "minecraft:sandstone_wall")
        t.set(x, 2, z, FIRE_BOWL)
    t.entity(c + 0.5, 1.0, 33.5, f"{NS}:sphinx")
    return t


# ---------------------------------------------------------------- the temple of Set

def temple_of_set():
    sx, sy, sz = 31, 16, 31
    t = Template(sx, sy, sz)
    rng = random.Random(206)
    ground(t, rng, RED_SAND)
    stone = [("minecraft:red_sandstone", 50), ("minecraft:cut_red_sandstone", 25), ("minecraft:smooth_red_sandstone", 15),
             ("minecraft:red_nether_bricks", 10)]
    c = sx // 2
    # Walls of red stone around a court open to the night sky, the hall of the god in the north.
    for x in range(1, sx - 1):
        for z in range(1, sz - 1):
            wall = x in (1, sx - 2) or z in (1, sz - 2)
            if wall:
                for y in range(1, 9):
                    t.set(x, y, z, pick(rng, stone))
                if (x + z) % 2 == 0:
                    t.set(x, 9, z, "minecraft:red_sandstone_wall")
            else:
                t.set(x, 0, z, "minecraft:smooth_red_sandstone" if (x + z) % 3 else "minecraft:red_nether_bricks")
    for x in range(c - 2, c + 3):
        for y in range(1, 6):
            t.set(x, y, sz - 2, AIR)
    for z in range(4, 27, 4):
        for x in (5, sx - 6):
            column(t, x, z, 0, 9, shaft="minecraft:cut_red_sandstone", capital="minecraft:chiseled_red_sandstone")
            t.set(x + (1 if x < c else -1), 1, z, FIRE_BOWL)
    # The altar of Set: a dais of black stone with fire and his red sand heaped about.
    t.fill(c - 3, 1, 3, c + 3, 1, 7, "minecraft:polished_blackstone_bricks")
    t.fill(c - 1, 2, 4, c + 1, 2, 5, "minecraft:gilded_blackstone")
    t.set(c, 3, 4, "minecraft:netherrack")
    t.set(c, 4, 4, "minecraft:fire[age=0,east=false,north=false,south=false,up=false,west=false]")
    t.chest(c - 3, 2, 4, "temple_of_set", facing="south")
    t.chest(c + 3, 2, 4, "temple_of_set", facing="south")
    for _ in range(18):
        x, z = rng.randrange(3, sx - 3), rng.randrange(10, sz - 3)
        if t.get(x, 1, z) in (None, AIR):
            t.set(x, 1, z, "minecraft:red_sand")
    t.entity(c + 0.5, 1.0, 11.5, f"{NS}:set")
    t.entity(c - 4.5, 1.0, 16.5, f"{NS}:jackal")
    t.entity(c + 5.5, 1.0, 16.5, f"{NS}:jackal")
    return t


# ---------------------------------------------------------------- the lair of Apep in the lake of fire

def apep_lair():
    sx, sy, sz = 37, 12, 37
    t = Template(sx, sy, sz)
    rng = random.Random(207)
    rock = [("minecraft:blackstone", 50), ("minecraft:basalt[axis=y]", 30), ("minecraft:magma_block", 20)]
    ground(t, rng, rock)
    c = sx // 2
    # A ring of lava around an island of black rock.
    for x in range(sx):
        for z in range(sz):
            r = math.hypot(x - c, z - c)
            if 11.5 <= r < 15.5:
                t.set(x, 0, z, "minecraft:lava[level=0]")
            elif r < 11.5:
                t.set(x, 0, z, pick(rng, [("minecraft:blackstone", 60), ("minecraft:polished_basalt[axis=y]", 25),
                                           ("minecraft:gilded_blackstone", 15)]))
    # A causeway of stone across the lava from the south.
    for z in range(c + 10, sz):
        for x in (c - 1, c, c + 1):
            t.set(x, 0, z, "minecraft:polished_blackstone_bricks")
    # The wreck of a barque of Ra that the serpent dragged down: a golden hull broken in two.
    for x in range(c - 6, c + 7):
        if abs(x - c) <= 1:
            continue
        width = 2 if abs(x - c) < 5 else 1
        for z in range(c - width, c + width + 1):
            t.set(x, 1, z, "minecraft:stripped_jungle_log[axis=x]")
            if abs(z - c) == width:
                t.set(x, 2, z, "minecraft:jungle_fence")
    for x in (c - 7, c + 7):
        t.set(x, 2, c, "minecraft:gold_block")
        t.set(x, 3, c, "minecraft:gold_block")
    t.set(c - 3, 2, c, "minecraft:jungle_log[axis=y]")
    t.set(c - 3, 3, c, "minecraft:jungle_log[axis=y]")
    t.set(c - 3, 4, c, "minecraft:yellow_wool")
    t.set(c - 3, 5, c, "minecraft:shroomlight")              # the sun disc of Ra, still glowing
    t.chest(c + 3, 2, c, "apep_lair", facing="south")
    t.chest(c + 5, 2, c, "apep_lair", facing="south")
    # Spires of basalt around the island.
    for angle in range(0, 360, 45):
        a = math.radians(angle)
        x, z = round(c + math.cos(a) * 9), round(c + math.sin(a) * 9)
        for y in range(1, rng.randint(3, 6)):
            t.set(x, y, z, "minecraft:basalt[axis=y]")
    t.entity(c + 0.5, 1.0, c + 6.5, f"{NS}:apep")
    t.entity(c - 5.5, 1.0, c - 5.5, f"{NS}:scarab")
    t.entity(c + 5.5, 1.0, c - 5.5, f"{NS}:scarab")
    return t


# ---------------------------------------------------------------- the shrines of the gods

def sanctuary_shrine(seed, palette, god, chest, ground_palette=SAND, sx=23, sz=29):
    """A shrine of one god: a pylon gate in the south, a court with columns and fire bowls where the god waits, and a
    roofed sanctuary in the north with the god's colossal statue behind an offering table and two chests.

    palette: wall (weighted list), floor (two blocks in a chequer), column shaft and capital, accent (bands of colour
    on the pylons), fire (the bowls). Returns the template and the centre column, so that each god can add its own
    statue and details."""
    sy = 16
    t = Template(sx, sy, sz)
    rng = random.Random(seed)
    ground(t, rng, ground_palette)
    c = sx // 2
    wall = palette["wall"]
    for x in range(2, sx - 2):
        for z in range(2, sz - 2):
            t.set(x, 0, z, palette["floor"][(x + z) % 2])
    # The pylon gate.
    for x0, x1 in ((2, c - 2), (c + 2, sx - 3)):
        for y in range(1, 10):
            inset = y // 4
            for x in range(x0 + inset, x1 - inset + 1):
                for z in range(sz - 6, sz - 2):
                    t.set(x, y, z, pick(rng, wall))
        for y in range(3, 9):
            t.set((x0 + x1) // 2, y, sz - 2, palette["accent"][y % 2])
    for x in range(c - 1, c + 2):
        t.set(x, 7, sz - 4, "minecraft:chiseled_sandstone")
        for z in range(sz - 6, sz - 2):
            t.set(x, 8, z, pick(rng, wall))
    # The court with its columns and fire bowls.
    for z in range(10, sz - 7, 3):
        for x in (4, sx - 5):
            column(t, x, z, 0, 7, shaft=palette["shaft"], capital=palette["capital"])
    for x, z in ((c - 4, 12), (c + 4, 12), (c - 4, sz - 9), (c + 4, sz - 9)):
        t.set(x, 1, z, palette["fire"])
    # The sanctuary.
    for x in range(2, sx - 2):
        for z in range(2, 10):
            edge = x in (2, sx - 3) or z == 2
            for y in range(1, 10):
                t.set(x, y, z, pick(rng, wall) if edge else AIR)
            t.set(x, 10, z, pick(rng, wall))
    for x in range(3, sx - 3):
        if abs(x - c) > 1:
            for y in range(1, 10):
                t.set(x, y, 9, pick(rng, wall))
    for x in range(c - 1, c + 2):
        t.set(x, 6, 9, palette["capital"])
        for y in range(7, 10):
            t.set(x, y, 9, pick(rng, wall))
    t.fill(c - 2, 1, 6, c + 2, 1, 6, "minecraft:smooth_sandstone_slab[type=bottom,waterlogged=false]")
    t.chest(c - 3, 1, 6, chest, facing="south")
    t.chest(c + 3, 1, 6, chest, facing="south")
    for x in (4, sx - 5):
        t.set(x, 8, 5, LANTERN)
    t.entity(c + 0.5, 1.0, 13.5, f"{NS}:{god}")
    return t, c, rng


def colossus(t, c, z, body, head_fn, top=8):
    """A seated colossus of the god against the back wall: a throne block, legs, body and the head drawn by head_fn."""
    t.fill(c - 1, 1, z, c + 1, 2, z, body)
    t.fill(c - 1, 1, z + 1, c + 1, top - 3, z + 1, body)
    t.set(c, top - 3, z + 1, "minecraft:gold_block")
    head_fn(t, c, top - 2, z + 1)


def temple_of_horus():
    """The temple of Horus at Edfu: golden-white stone, two falcons of granite before the gate, the falcon colossus
    with the double crown in the sanctuary."""
    palette = {"wall": [(PYRAMID, 60), ("minecraft:smooth_sandstone", 25), (GLYPHS, 15)],
               "floor": ("minecraft:smooth_sandstone", "minecraft:cut_sandstone"),
               "shaft": "minecraft:cut_sandstone", "capital": "minecraft:chiseled_sandstone",
               "accent": ("minecraft:blue_wool", "minecraft:yellow_wool"), "fire": FIRE_BOWL}
    t, c, rng = sanctuary_shrine(208, palette, "horus", "temple_of_horus")
    sz = t.size[2]

    def falcon_head(t, x, y, z):
        t.fill(x - 1, y, z, x + 1, y + 1, z, "minecraft:brown_terracotta")
        t.set(x, y, z - 1, "minecraft:yellow_terracotta")              # the hooked beak
        t.set(x, y + 2, z, "minecraft:white_terracotta")              # the white crown of the south
        t.set(x, y + 2, z + 1, "minecraft:red_terracotta")            # the red crown of the north behind it
    colossus(t, c, 3, "minecraft:polished_blackstone", falcon_head)
    for x in (c - 4, c + 4):                                          # the falcons of granite at the gate
        t.set(x, 1, sz - 7, "minecraft:polished_blackstone")
        t.set(x, 2, sz - 7, "minecraft:polished_blackstone")
        t.set(x, 3, sz - 7, "minecraft:brown_terracotta")
        t.set(x, 4, sz - 7, "minecraft:red_terracotta")
    return t


def temple_of_bastet():
    """The temple of Bastet at Bubastis: pale stone with black and turquoise, the black cat colossus with a golden
    earring, and the sacred cats of the goddess in the court."""
    palette = {"wall": [("minecraft:smooth_sandstone", 60), (PYRAMID, 30), (GLYPHS, 10)],
               "floor": ("minecraft:polished_blackstone", "minecraft:smooth_sandstone"),
               "shaft": "minecraft:cut_sandstone", "capital": "minecraft:chiseled_sandstone",
               "accent": ("minecraft:cyan_wool", "minecraft:black_wool"), "fire": FIRE_BOWL}
    t, c, rng = sanctuary_shrine(209, palette, "bastet", "temple_of_bastet")

    def cat_head(t, x, y, z):
        t.fill(x - 1, y, z, x + 1, y + 1, z, "minecraft:black_concrete")
        t.set(x - 1, y + 2, z, "minecraft:black_concrete")              # the pointed ears
        t.set(x + 1, y + 2, z, "minecraft:black_concrete")
        t.set(x - 1, y + 1, z - 1, "minecraft:yellow_stained_glass")    # the golden eyes
        t.set(x + 1, y + 1, z - 1, "minecraft:yellow_stained_glass")
        t.set(x + 2, y + 1, z, "minecraft:gold_block")                   # the earring
    colossus(t, c, 3, "minecraft:black_concrete", cat_head)
    for x, z in ((c - 3, 16), (c + 3, 18), (c - 2, 21), (c + 2, 12)):
        t.entity(x + 0.5, 1.0, z + 0.5, f"{NS}:bastet_cat")
    for x, z in ((6, 15), (t.size[0] - 7, 20)):
        t.set(x, 1, z, "minecraft:decorated_pot[facing=south,cracked=false,waterlogged=false]")
    return t


def shrine_of_sobek():
    """The shrine of Sobek on the bank of the Nile, as at Kom Ombo: mud brick and green stone, a sacred pool in the
    court where his crocodiles bask, the crocodile colossus in the sanctuary."""
    palette = {"wall": [("minecraft:mud_bricks", 55), ("minecraft:packed_mud", 20), ("minecraft:mossy_stone_bricks", 25)],
               "floor": ("minecraft:mud_bricks", "minecraft:smooth_sandstone"),
               "shaft": "minecraft:mossy_stone_bricks", "capital": "minecraft:chiseled_stone_bricks",
               "accent": ("minecraft:green_wool", "minecraft:lime_wool"), "fire": FIRE_BOWL}
    t, c, rng = sanctuary_shrine(210, palette, "sobek", "shrine_of_sobek",
                                 ground_palette=[(f"{NS}:nile_silt", 50), ("minecraft:mud", 30), ("minecraft:grass_block[snowy=false]", 20)])
    # The sacred pool in the middle of the court, with silt and papyrus around it.
    for x in range(c - 3, c + 4):
        for z in range(15, 21):
            edge = x in (c - 3, c + 3) or z in (15, 20)
            t.set(x, 0, z, f"{NS}:nile_silt" if edge else "minecraft:water")
            if edge and (x + z) % 3 == 0:
                t.set(x, 1, z, "minecraft:sugar_cane[age=0]")
                t.set(x, 2, z, "minecraft:sugar_cane[age=0]")
    t.set(c, 1, 17, "minecraft:lily_pad")

    def crocodile_head(t, x, y, z):
        t.fill(x - 1, y, z, x + 1, y, z, "minecraft:green_terracotta")
        t.fill(x - 1, y, z - 1, x + 1, y, z - 1, "minecraft:green_terracotta")   # the long snout
        t.set(x, y, z - 2, "minecraft:green_terracotta")
        t.set(x - 1, y + 1, z, "minecraft:yellow_terracotta")                      # the eyes on top
        t.set(x + 1, y + 1, z, "minecraft:yellow_terracotta")
        t.set(x, y + 1, z + 1, "minecraft:gold_block")                             # the plumes and sun disc
    colossus(t, c, 3, "minecraft:green_terracotta", crocodile_head)
    t.entity(c - 1.5, 1.0, 17.5, f"{NS}:crocodile")
    t.entity(c + 2.5, 1.0, 18.5, f"{NS}:crocodile")
    return t


def shrine_of_hathor():
    """The shrine of Hathor in the Fields of Aaru: rose and white stone, Hathor-headed capitals, the colossus with the
    cow horns and the sun disc between them, and her cows grazing around."""
    palette = {"wall": [("minecraft:smooth_quartz", 40), ("minecraft:pink_terracotta", 35), (GLYPHS, 25)],
               "floor": ("minecraft:smooth_quartz", "minecraft:pink_terracotta"),
               "shaft": "minecraft:quartz_pillar[axis=y]", "capital": "minecraft:chiseled_quartz_block",
               "accent": ("minecraft:red_wool", "minecraft:yellow_wool"), "fire": FIRE_BOWL}
    t, c, rng = sanctuary_shrine(211, palette, "hathor", "shrine_of_hathor",
                                 ground_palette=[("minecraft:grass_block[snowy=false]", 80), ("minecraft:moss_block", 20)])

    def cow_head(t, x, y, z):
        t.fill(x - 1, y, z, x + 1, y + 1, z, "minecraft:white_terracotta")
        t.set(x - 2, y + 2, z, "minecraft:gold_block")                     # the horns curving up
        t.set(x + 2, y + 2, z, "minecraft:gold_block")
        t.set(x - 2, y + 1, z, "minecraft:gold_block")
        t.set(x + 2, y + 1, z, "minecraft:gold_block")
        t.set(x, y + 2, z, "minecraft:shroomlight")                         # the sun disc between them
    colossus(t, c, 3, "minecraft:pink_terracotta", cow_head)
    for x, z in ((1, 15), (t.size[0] - 2, 19)):
        t.entity(x + 0.5, 1.0, z + 0.5, "minecraft:cow")
    for x in range(5, t.size[0] - 5, 2):
        t.set(x, 1, t.size[2] - 1, "minecraft:poppy")
    return t


def forge_of_ptah():
    """The forge-temple of Ptah at Memphis, lord of craftsmen: dark stone and lapis, anvils, a blast furnace and a
    basin of molten metal in the court, the mummiform colossus with the blue cap, and ushabti at work."""
    palette = {"wall": [("minecraft:polished_blackstone_bricks", 50), ("minecraft:blackstone", 25), ("minecraft:lapis_block", 5),
                        (PYRAMID, 20)],
               "floor": ("minecraft:polished_blackstone", "minecraft:polished_basalt[axis=y]"),
               "shaft": "minecraft:polished_basalt[axis=y]", "capital": "minecraft:chiseled_polished_blackstone",
               "accent": ("minecraft:blue_wool", "minecraft:light_blue_wool"), "fire": FIRE_BOWL}
    t, c, rng = sanctuary_shrine(212, palette, "ptah", "forge_of_ptah", ground_palette=RED_SAND)
    for x in range(c - 1, c + 2):                                      # the basin of molten metal
        for z in range(17, 20):
            t.set(x, 0, z, "minecraft:lava[level=0]")
    for x, z in ((c - 2, 16), (c + 2, 16), (c - 2, 20), (c + 2, 20)):
        t.set(x, 1, z, "minecraft:polished_blackstone_wall")
    t.set(c - 4, 1, 17, "minecraft:anvil[facing=east]")
    t.set(c + 4, 1, 19, "minecraft:anvil[facing=west]")
    t.set(c - 4, 1, 20, "minecraft:blast_furnace[facing=east,lit=true]")
    t.set(c + 4, 1, 16, "minecraft:smithing_table")

    def ptah_head(t, x, y, z):
        t.fill(x - 1, y, z, x + 1, y + 1, z, "minecraft:white_terracotta")
        t.fill(x - 1, y + 2, z, x + 1, y + 2, z, "minecraft:lapis_block")   # the close blue cap
        t.set(x, y, z - 1, "minecraft:gold_block")                          # the straight beard
    colossus(t, c, 3, "minecraft:green_terracotta", ptah_head)
    t.entity(c - 3.5, 1.0, 14.5, f"{NS}:ushabti")
    t.entity(c + 4.5, 1.0, 14.5, f"{NS}:ushabti")
    return t


def shrine_of_sekhmet():
    """The shrine of Sekhmet by the Lake of Fire: red stone, fire everywhere, the lioness colossus with the sun disc
    and the cobra, and the bones of those she punished."""
    palette = {"wall": [("minecraft:red_sandstone", 45), ("minecraft:cut_red_sandstone", 25), ("minecraft:red_nether_bricks", 30)],
               "floor": ("minecraft:red_nether_bricks", "minecraft:smooth_red_sandstone"),
               "shaft": "minecraft:cut_red_sandstone", "capital": "minecraft:chiseled_red_sandstone",
               "accent": ("minecraft:red_wool", "minecraft:orange_wool"), "fire": FIRE_BOWL}
    t, c, rng = sanctuary_shrine(213, palette, "sekhmet", "shrine_of_sekhmet",
                                 ground_palette=[("minecraft:blackstone", 50), ("minecraft:magma_block", 20), ("minecraft:red_sand", 30)])

    def lioness_head(t, x, y, z):
        t.fill(x - 1, y, z, x + 1, y + 1, z, "minecraft:orange_terracotta")
        t.set(x, y, z - 1, "minecraft:yellow_terracotta")                   # the muzzle
        t.set(x, y + 2, z, "minecraft:shroomlight")                         # the sun disc
        t.set(x, y + 2, z - 1, "minecraft:gold_block")                      # the cobra on the brow
    colossus(t, c, 3, "minecraft:red_terracotta", lioness_head)
    for x, z in ((c - 3, 14), (c + 3, 20), (c - 2, 22)):
        t.set(x, 1, z, "minecraft:bone_block[axis=y]")
    for x in (c - 1, c + 1):
        t.set(x, 0, 17, "minecraft:netherrack")
        t.set(x, 1, 17, "minecraft:fire[age=0,east=false,north=false,south=false,up=false,west=false]")
    return t


# ---------------------------------------------------------------- the Hall of Judgment

def hall_of_judgment():
    """The Hall of the Two Truths, where the hearts of the dead are weighed: a long hall of columns open to the stars,
    the great scales in the middle with Anubis beside them and Thoth with his tablet, and Osiris enthroned at the
    north end under a canopy, with the devourer Ammit's jaws carved at the foot of the scales."""
    sx, sy, sz = 27, 15, 35
    t = Template(sx, sy, sz)
    rng = random.Random(214)
    ground(t, rng, SAND)
    c = sx // 2
    wall = [(PYRAMID, 50), (GLYPHS, 30), ("minecraft:smooth_sandstone", 20)]
    for x in range(1, sx - 1):
        for z in range(1, sz - 1):
            edge = x in (1, sx - 2) or z in (1, sz - 2)
            t.set(x, 0, z, "minecraft:lapis_block" if abs(x - c) <= 1 else
                  ("minecraft:polished_blackstone" if (x + z) % 2 else "minecraft:smooth_quartz"))
            if edge:
                for y in range(1, 8):
                    t.set(x, y, z, pick(rng, wall))
                if (x + z) % 2 == 0:
                    t.set(x, 8, z, "minecraft:sandstone_wall")
    for x in range(c - 1, c + 2):                                   # the doorway in the south
        for y in range(1, 5):
            t.set(x, y, sz - 2, AIR)
    for z in range(5, sz - 4, 4):                                   # two rows of papyrus columns
        for x in (5, sx - 6):
            column(t, x, z, 0, 9, shaft="minecraft:quartz_pillar[axis=y]", capital="minecraft:chiseled_sandstone")
            t.set(x, 9, z, "minecraft:gold_block")
    # The scales: a pillar with a beam, chains and two golden pans.
    zs = 17
    t.fill(c, 1, zs, c, 5, zs, "minecraft:gold_block")
    t.fill(c - 3, 6, zs, c + 3, 6, zs, "minecraft:gold_block")
    for x in (c - 3, c + 3):
        t.set(x, 5, zs, "minecraft:chain[axis=y,waterlogged=false]")
        t.set(x, 4, zs, "minecraft:chain[axis=y,waterlogged=false]")
        t.set(x, 3, zs, "minecraft:light_weighted_pressure_plate[power=0]")
        t.set(x, 2, zs, "minecraft:gold_block")
    t.set(c - 3, 1, zs, "minecraft:smooth_sandstone")
    t.set(c + 3, 1, zs, "minecraft:smooth_sandstone")
    t.set(c, 1, zs + 1, "minecraft:green_terracotta")              # Ammit, waiting at the foot of the scales
    t.set(c, 1, zs + 2, "minecraft:orange_terracotta")
    # The throne of Osiris on a dais under a canopy.
    t.fill(c - 3, 1, 3, c + 3, 1, 7, "minecraft:smooth_sandstone")
    t.fill(c - 1, 2, 3, c + 1, 2, 4, "minecraft:green_terracotta")
    t.fill(c - 1, 3, 3, c + 1, 4, 3, "minecraft:green_terracotta")
    for x in (c - 3, c + 3):
        for z in (3, 7):
            t.fill(x, 2, z, x, 7, z, "minecraft:quartz_pillar[axis=y]")
    t.fill(c - 3, 8, 3, c + 3, 8, 7, "minecraft:gold_block")
    t.chest(c - 2, 2, 5, "hall_of_judgment", facing="south")
    t.chest(c + 2, 2, 5, "hall_of_judgment", facing="south")
    for x, z in ((c - 4, 12), (c + 4, 12), (c - 4, 24), (c + 4, 24)):
        t.set(x, 1, z, SOUL_FIRE)
    t.entity(c + 0.5, 2.0, 5.5, f"{NS}:osiris")
    t.entity(c - 4.5, 1.0, zs + 0.5, f"{NS}:anubis")
    t.entity(c + 5.5, 1.0, zs + 0.5, f"{NS}:thoth")
    return t


# ---------------------------------------------------------------- boats on the Nile

def hull(t, x0, x1, cz, half_width, deck_y, planks, trim, bow_rise=2):
    """A boat of the Nile seen from above: a long hull, widest in the middle and narrowing to a bow and a stern that
    curve up. The keel sits in the water (y = 0, the water surface), the deck is at deck_y. Water is left where the hull
    is not, as the template keeps the blocks it does not set."""
    length = x1 - x0
    for x in range(x0, x1 + 1):
        f = (x - x0) / length
        width = max(0, round(half_width * math.sin(math.pi * f) ** 0.6))
        end = min(x - x0, x1 - x)
        for z in range(cz - width, cz + width + 1):
            side = abs(z - cz) == width
            t.set(x, 0, z, planks)
            for y in range(1, deck_y):
                t.set(x, y, z, planks)
            if side:
                t.set(x, deck_y, z, trim)
        if end < bow_rise:                                         # the bow and the stern curve up like a papyrus umbel
            for y in range(deck_y, deck_y + bow_rise - end + 1):
                t.set(x, y, cz, trim)


def solar_barque():
    """The barque of millions of years, in which Ra sails the sky by day and the Duat by night: a long golden hull on
    the Celestial Nile, a shrine with a golden roof amidships, the sun disc blazing on its mast, steering oars at the
    stern. Ra stands on the deck."""
    sx, sy, sz = 31, 14, 11
    t = Template(sx, sy, sz)
    rng = random.Random(215)
    cz = sz // 2
    hull(t, 1, sx - 2, cz, 4, 2, "minecraft:stripped_jungle_log[axis=x]", "minecraft:gold_block", bow_rise=4)
    for x in range(sx):                                                # the deck of cedar
        for z in range(sz):
            if t.get(x, 2, z) in (None, AIR) and t.get(x, 1, z) not in (None, AIR):
                t.set(x, 2, z, "minecraft:jungle_planks")
    c = sx // 2
    for x in range(c - 3, c + 2):                                      # the shrine of the god amidships
        for z in range(cz - 2, cz + 3):
            edge = x in (c - 3, c + 1) or abs(z - cz) == 2
            for y in range(3, 6):
                t.set(x, y, z, (GLYPHS if y == 4 else PYRAMID) if edge else AIR)
            t.set(x, 6, z, "minecraft:gold_block")
    for y in range(3, 5):
        t.set(c + 1, y, cz, AIR)
    t.chest(c - 2, 3, cz, "solar_barque", facing="east")
    for y in range(3, 10):                                             # the mast with the sun disc
        t.set(c + 5, y, cz, "minecraft:stripped_jungle_log[axis=y]")
    for dy in range(-1, 2):
        for dz in range(-1, 2):
            t.set(c + 5, 10 + dy, cz + dz, "minecraft:shroomlight" if (dy, dz) != (0, 0) else "minecraft:gold_block")
    t.set(c + 5, 12, cz, "minecraft:end_rod[facing=up]")
    for z in (cz - 4, cz + 4):                                         # the steering oars at the stern
        t.set(4, 3, z, "minecraft:jungle_fence")
        t.set(4, 2, z, "minecraft:jungle_fence")
        t.set(4, 1, z, "minecraft:jungle_fence")
    for x in (6, sx - 7):
        t.set(x, 3, cz, STANDING_LANTERN)
    t.entity(c + 3.5, 3.0, cz + 0.5, f"{NS}:ra")
    return t


def nile_boat():
    """A trading boat of the Nile: a hull of papyrus bundles tied with rope, a deck of planks, a tall mast with a wide
    square sail of linen, jars and a chest of goods. A trader of the market sails on it."""
    sx, sy, sz = 17, 12, 7
    t = Template(sx, sy, sz)
    rng = random.Random(216)
    cz = sz // 2
    hull(t, 0, sx - 1, cz, 3, 2, "minecraft:hay_block[axis=x]", "minecraft:stripped_bamboo_block[axis=x]", bow_rise=3)
    for x in range(sx):
        for z in range(sz):
            if t.get(x, 2, z) in (None, AIR) and t.get(x, 1, z) not in (None, AIR):
                t.set(x, 2, z, "minecraft:bamboo_mosaic")
    m = sx // 2
    for y in range(3, 11):
        t.set(m, y, cz, "minecraft:stripped_jungle_log[axis=y]")
    for z in range(cz - 3, cz + 4):                                    # the yard and the square sail
        t.set(m, 10, z, "minecraft:stripped_jungle_log[axis=z]")
        for y in range(5, 10):
            if abs(z - cz) <= 3 and z != cz:
                t.set(m + 1, y, z, "minecraft:white_wool")
        t.set(m + 1, 5, cz, "minecraft:white_wool")
        t.set(m + 1, 9, cz, "minecraft:white_wool")
    t.set(m - 3, 3, cz - 1, "minecraft:decorated_pot[facing=south,cracked=false,waterlogged=false]")
    t.set(m - 3, 3, cz + 1, "minecraft:barrel[facing=up,open=false]")
    t.chest(m - 2, 3, cz, "nile_boat", facing="east")
    t.set(m + 3, 3, cz, STANDING_LANTERN)
    t.entity(m + 2.5, 3.0, cz + 1.5, f"{NS}:egyptian_merchant", {"Kind": 0})
    return t


def papyrus_skiff():
    """A small skiff of papyrus bundles for fishing among the reeds, with a pole, a net and the morning's catch."""
    sx, sy, sz = 11, 6, 5
    t = Template(sx, sy, sz)
    rng = random.Random(217)
    cz = sz // 2
    hull(t, 0, sx - 1, cz, 2, 1, "minecraft:hay_block[axis=x]", "minecraft:hay_block[axis=x]", bow_rise=2)
    for x in range(3, sx - 3):
        t.set(x, 1, cz, "minecraft:bamboo_mosaic_slab[type=bottom,waterlogged=false]")
    t.chest(4, 1, cz, "papyrus_skiff", facing="east")
    t.set(6, 2, cz, "minecraft:cobweb")                                # the fishing net hung to dry
    t.set(sx // 2 + 2, 2, cz, "minecraft:bamboo_fence")
    t.set(sx // 2 + 2, 3, cz, "minecraft:bamboo_fence")
    return t


STRUCTURES = {
    "egyptian_village": egyptian_village,
    "temple_of_isis": temple_of_isis,
    "obelisk": obelisk,
    "pharaoh_tomb": pharaoh_tomb,
    "great_sphinx": great_sphinx,
    "temple_of_set": temple_of_set,
    "apep_lair": apep_lair,
    "hall_of_judgment": hall_of_judgment,
    "solar_barque": solar_barque,
    "temple_of_horus": temple_of_horus,
    "temple_of_bastet": temple_of_bastet,
    "shrine_of_sobek": shrine_of_sobek,
    "shrine_of_hathor": shrine_of_hathor,
    "forge_of_ptah": forge_of_ptah,
    "shrine_of_sekhmet": shrine_of_sekhmet,
    "nile_boat": nile_boat,
    "papyrus_skiff": papyrus_skiff,
}
