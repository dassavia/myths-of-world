"""Structure templates of Nav, written as .nbt files. Same conventions as structures.py: x east, y up, z south,
origin at the corner, y = 0 is the ground the template stands on."""
import math
import random

from structures import AIR, Template, pick

NS = "mythsofworlds"
FENCE = "minecraft:oak_fence"
LANTERN = "minecraft:lantern[hanging=true]"
STANDING_LANTERN = "minecraft:lantern[hanging=false]"
SOUL_LANTERN = "minecraft:soul_lantern[hanging=false]"
CAMPFIRE = "minecraft:campfire[lit=true,signal_fire=false]"
SOUL_CAMPFIRE = "minecraft:soul_campfire[lit=true,signal_fire=false]"
EARTH = [("minecraft:grass_block[snowy=false]", 75), ("minecraft:coarse_dirt", 15), ("minecraft:dirt_path", 10)]
OAK_LEAVES = "minecraft:oak_leaves[distance=7,persistent=true,waterlogged=false]"
DARK_LEAVES = "minecraft:dark_oak_leaves[distance=7,persistent=true,waterlogged=false]"


def stairs(block, facing, half="bottom"):
    return f"minecraft:{block}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]"


def ground(t, rng, palette=EARTH):
    sx, sy, sz = t.size
    for x in range(sx):
        for z in range(sz):
            t.set(x, 0, z, pick(rng, palette))
    t.fill(0, 1, 0, sx - 1, sy - 1, sz - 1, AIR)


# ---------------------------------------------------------------- the izba and the village

def izba(t, x0, z0, rng, chest=None, merchant=None, length=7, width=6):
    """Log cabin along x with its door in the middle of the south wall: walls of logs laid crosswise at the corners,
    a steep gable roof, glass windows with carved shutters, a brick stove with a furnace, a bench and a red rug."""
    x1, z1 = x0 + length - 1, z0 + width - 1
    wall_top = 3
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            t.set(x, 0, z, "minecraft:cobblestone" if edge else "minecraft:spruce_planks")
            for y in range(1, wall_top + 1):
                if not edge:
                    t.set(x, y, z, AIR)
                elif z in (z0, z1) and x not in (x0, x1):
                    t.set(x, y, z, "minecraft:spruce_log[axis=x]")
                elif x in (x0, x1) and z not in (z0, z1):
                    t.set(x, y, z, "minecraft:spruce_log[axis=z]")
                else:
                    t.set(x, y, z, "minecraft:spruce_log[axis=y]")
    half = width // 2
    for k in range(half + 1):
        y = wall_top + 1 + k
        for x in range(x0 - 1, x1 + 2):
            if not t.inside(x, y, z0):
                continue
            if k < half:
                t.set(x, y, z0 + k, stairs("dark_oak", "south"))
                t.set(x, y, z1 - k, stairs("dark_oak", "north"))
            elif width % 2 == 0:
                t.set(x, y - 1, z0 + k, "minecraft:dark_oak_planks")
            else:
                t.set(x, y, z0 + k, "minecraft:dark_oak_slab[type=bottom]")
        for z in range(z0 + k + 1, z1 - k):
            t.set(x0, y, z, "minecraft:spruce_planks")
            t.set(x1, y, z, "minecraft:spruce_planks")
    # A carved ridge horse (konyok) on the gable.
    for x in (x0, x1):
        if t.inside(x, wall_top + half + 1, z0 + half):
            t.set(x, wall_top + half + 1, z0 + half - (0 if width % 2 else 1), "minecraft:oak_fence")
    mx = x0 + length // 2
    t.set(mx, 1, z1, "minecraft:spruce_door[facing=south,half=lower,hinge=left,open=false,powered=false]")
    t.set(mx, 2, z1, "minecraft:spruce_door[facing=south,half=upper,hinge=left,open=false,powered=false]")
    for wx in (x0 + 2, x1 - 2):
        if wx != mx:
            t.set(wx, 2, z1, "minecraft:glass_pane")
            for sx in (wx - 1, wx + 1):
                if sx not in (x0, x1, mx) and t.inside(sx, 2, z1 + 1):
                    t.set(sx, 2, z1 + 1, "minecraft:spruce_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]")
    t.set(x0, 2, z0 + half, "minecraft:glass_pane")
    t.set(x1, 2, z0 + half, "minecraft:glass_pane")
    # The stove in the corner: bricks with a furnace mouth, a chimney through the roof.
    t.fill(x0 + 1, 1, z0 + 1, x0 + 2, 2, z0 + 2, "minecraft:bricks")
    t.set(x0 + 2, 1, z0 + 2, "minecraft:furnace[facing=south,lit=true]")
    for y in range(3, wall_top + half + 2):
        if t.inside(x0 + 1, y, z0 + 1):
            t.set(x0 + 1, y, z0 + 1, "minecraft:bricks")
    t.set(x1 - 1, 1, z0 + 1, "minecraft:spruce_slab[type=bottom]")
    t.set(x1 - 2, 1, z0 + 1, "minecraft:spruce_slab[type=bottom]")
    for x in range(x0 + 2, x1 - 1):
        t.set(x, 1, z0 + half, "minecraft:red_carpet")
    t.set(x1 - 1, wall_top, z0 + half, LANTERN)
    t.set(x1 - 1, 1, z1 - 1, "minecraft:barrel[facing=up,open=false]")
    if chest:
        t.chest(x0 + 1, 1, z1 - 1, chest, facing="east")
    if merchant is not None:
        t.entity(mx + 0.5, 1.0, z0 + half + 0.5, f"{NS}:slavic_merchant", {"Kind": merchant})


def well(t, cx, cz):
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            t.set(x, 0, z, "minecraft:cobblestone")
            if (x, z) != (cx, cz):
                t.set(x, 1, z, "minecraft:cobblestone_wall")
    t.set(cx, 0, cz, "minecraft:water")
    for x, z in ((cx - 1, cz), (cx + 1, cz)):
        t.fill(x, 2, z, x, 3, z, "minecraft:oak_fence")
    t.fill(cx - 1, 4, cz, cx + 1, 4, cz, "minecraft:spruce_slab[type=bottom]")
    t.set(cx, 3, cz, "minecraft:chain[axis=y,waterlogged=false]")


def slavic_village():
    sx, sy, sz = 40, 12, 36
    t = Template(sx, sy, sz)
    rng = random.Random(91)
    ground(t, rng)
    # A wide street down the middle.
    for x in range(sx):
        for z in range(16, 20):
            t.set(x, 0, z, pick(rng, [("minecraft:dirt_path", 80), ("minecraft:coarse_dirt", 20)]))
    izba(t, 2, 3, rng, chest="slavic_village", merchant=0)
    izba(t, 12, 2, rng, chest="slavic_izba", length=8, width=7)
    izba(t, 23, 3, rng, chest="slavic_izba", merchant=2)
    # Houses across the street.
    izba(t, 4, 24, rng, chest="slavic_izba")
    izba(t, 26, 23, rng, chest="slavic_izba", length=8, width=7)
    well(t, 18, 28)
    # Fenced gardens with cabbages (beetroots) and haystacks.
    for x in range(32, 39):
        for z in range(2, 12):
            if x in (32, 38) or z in (2, 11):
                t.set(x, 1, z, FENCE)
            else:
                t.set(x, 0, z, "minecraft:farmland[moisture=7]")
                crop = rng.choice(["beetroots", "potatoes", "wheat"])
                t.set(x, 1, z, f"minecraft:{crop}[age={3 if crop == 'beetroots' else rng.choice([5, 7])}]")
    t.set(35, 1, 11, "minecraft:oak_fence_gate[facing=south,in_wall=false,open=false,powered=false]")
    for x, z in ((14, 26), (22, 31), (36, 28)):
        t.fill(x, 1, z, x, 2, z, "minecraft:hay_block[axis=y]")
    for x in range(1, sx - 1, 6):
        t.fill(x, 1, 15, x, 2, 15, FENCE)
        t.set(x, 3, 15, STANDING_LANTERN)
    t.entity(18.5, 1.0, 21.5, "minecraft:chicken")
    t.entity(30.5, 1.0, 30.5, "minecraft:cow")
    t.entity(12.5, 1.0, 31.5, "minecraft:horse")
    return t


# ---------------------------------------------------------------- the hut of Baba Yaga

def baba_yaga_hut():
    sx, sy, sz = 17, 13, 17
    t = Template(sx, sy, sz)
    rng = random.Random(92)
    ground(t, rng, [("minecraft:podzol", 50), ("minecraft:coarse_dirt", 30), ("minecraft:moss_block", 20)])
    # A ring of fence posts topped with skulls.
    cx, cz = 8, 8
    for x in range(sx):
        for z in range(sz):
            r = math.hypot(x - cx, z - cz)
            if 7.0 <= r < 7.8 and not (z > cz + 5 and abs(x - cx) <= 1):
                t.set(x, 1, z, FENCE)
                if (x + z) % 3 == 0:
                    t.set(x, 2, z, f"minecraft:skeleton_skull[rotation={rng.randrange(16)}]")
    # Two chicken legs: thick stripped trunks with toes of roots, raising the hut four blocks.
    for lx in (6, 10):
        t.fill(lx, 1, cz, lx, 4, cz, "minecraft:stripped_mangrove_log[axis=y]")
        for dx, dz in ((0, 1), (0, -1), (1, 1), (-1, 1)):
            t.set(lx + dx, 1, cz + dz, "minecraft:mangrove_roots[waterlogged=false]")
    # The hut itself on a floor at y = 5.
    x0, z0, x1, z1 = 5, 5, 11, 11
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            t.set(x, 5, z, "minecraft:dark_oak_planks")
            edge = x in (x0, x1) or z in (z0, z1)
            for y in range(6, 9):
                t.set(x, y, z, ("minecraft:dark_oak_log[axis=y]" if x in (x0, x1) and z in (z0, z1) else
                                "minecraft:spruce_log[axis=x]" if z in (z0, z1) else "minecraft:spruce_log[axis=z]") if edge else AIR)
    for k in range(4):
        y = 9 + k
        for x in range(x0 - 1, x1 + 2):
            if k < 3:
                t.set(x, y, z0 + k, stairs("spruce", "south"))
                t.set(x, y, z1 - k, stairs("spruce", "north"))
            else:
                t.set(x, y, z0 + k, "minecraft:moss_block")
        for z in range(z0 + k + 1, z1 - k):
            t.set(x0, y, z, "minecraft:spruce_planks")
            t.set(x1, y, z, "minecraft:spruce_planks")
    # Door at the back of the hut ("turn your back to the forest, your front to me") and a ladder up to it.
    t.set(cx, 6, z1, "minecraft:spruce_door[facing=south,half=lower,hinge=left,open=false,powered=false]")
    t.set(cx, 7, z1, "minecraft:spruce_door[facing=south,half=upper,hinge=left,open=false,powered=false]")
    t.set(cx, 5, z1 + 1, "minecraft:spruce_slab[type=top]")
    for y in range(1, 5):
        t.set(cx, y, z1 + 1, "minecraft:spruce_planks")
        t.set(cx, y, z1 + 2, "minecraft:ladder[facing=south,waterlogged=false]")
    t.set(x0, 7, cz, "minecraft:glass_pane")
    t.set(x1, 7, cz, "minecraft:glass_pane")
    # Inside: the stove, a cauldron of brew, herbs and the chest; Baba Yaga by the stove.
    t.fill(x0 + 1, 6, z0 + 1, x0 + 2, 7, z0 + 1, "minecraft:bricks")
    t.set(x0 + 1, 6, z0 + 2, "minecraft:smoker[facing=east,lit=true]")
    t.set(x1 - 1, 6, z0 + 1, "minecraft:water_cauldron[level=3]")
    t.set(x1 - 1, 6, z0 + 3, "minecraft:brewing_stand[has_bottle_0=true,has_bottle_1=false,has_bottle_2=true]")
    t.chest(x1 - 1, 6, z1 - 1, "baba_yaga_hut", facing="west")
    t.set(x0 + 1, 6, z1 - 1, "minecraft:flower_pot")
    t.set(x0 + 3, 8, z0 + 3, LANTERN)
    t.set(cx, 6, cz, "minecraft:black_carpet")
    t.entity(cx + 0.5, 6.0, cz - 0.5, f"{NS}:slavic_merchant", {"Kind": 1})
    t.entity(cx + 2.5, 1.0, cz + 4.5, "minecraft:cat", {"variant": "minecraft:all_black"})
    return t


# ---------------------------------------------------------------- the kapishche, a shrine of the old gods

def idol(t, x, z, facing, colour):
    t.fill(x, 1, z, x, 3, z, "minecraft:stripped_oak_log[axis=y]")
    t.set(x, 4, z, f"minecraft:carved_pumpkin[facing={facing}]")
    t.set(x, 5, z, f"minecraft:{colour}_carpet")


def kapishche():
    sx, sy, sz = 19, 8, 19
    t = Template(sx, sy, sz)
    rng = random.Random(93)
    ground(t, rng)
    c = 9
    for x in range(sx):
        for z in range(sz):
            r = math.hypot(x - c, z - c)
            if r < 6.5:
                t.set(x, 0, z, pick(rng, [("minecraft:dirt_path", 60), ("minecraft:coarse_dirt", 40)]))
            if 7.5 <= r < 8.4 and not (abs(x - c) <= 1 and z > c):
                t.set(x, 1, z, FENCE)
    # Perun in the north, Veles in the south, Mokosh and Dazhbog to the sides; all face the fire.
    idol(t, c, c - 5, "south", "red")
    idol(t, c, c + 5, "north", "brown")
    idol(t, c - 5, c, "east", "white")
    idol(t, c + 5, c, "west", "yellow")
    t.set(c, 0, c, "minecraft:cobblestone")
    t.set(c, 1, c, CAMPFIRE)
    for dx, dz in ((2, 2), (-2, 2), (2, -2), (-2, -2)):
        t.set(c + dx, 1, c + dz, "minecraft:spruce_slab[type=bottom]")
    t.chest(c + 1, 1, c - 4, "kapishche", facing="south")
    t.set(c - 1, 1, c - 4, "minecraft:candle[candles=3,lit=true,waterlogged=false]")
    t.entity(c + 0.5, 1.0, c + 3.5, f"{NS}:firebird")
    t.entity(c - 3.5, 1.0, c + 0.5, f"{NS}:firebird")
    return t


# ---------------------------------------------------------------- the old oak with the chest

def koschei_oak():
    sx, sy, sz = 15, 22, 15
    t = Template(sx, sy, sz)
    rng = random.Random(94)
    ground(t, rng, [("minecraft:podzol", 50), ("minecraft:rooted_dirt", 30), ("minecraft:coarse_dirt", 20)])
    cx, cz = 7, 7
    height = 15
    for x in (cx, cx + 1):
        for z in (cz, cz + 1):
            t.fill(x, 1, z, x, height, z, "minecraft:dark_oak_log[axis=y]")
    for x, z in ((cx - 1, cz), (cx + 2, cz + 1), (cx, cz + 2), (cx + 1, cz - 1)):
        t.set(x, 1, z, "minecraft:dark_oak_log[axis=y]")
    # Boughs, the crown, and a platform of planks among the branches holding the chest on a chain.
    for i in range(1, 4):
        t.set(cx - i, height - 2, cz, "minecraft:dark_oak_log[axis=x]")
        t.set(cx + 1 + i, height - 1, cz + 1, "minecraft:dark_oak_log[axis=x]")
        t.set(cx, height - 1, cz - i, "minecraft:dark_oak_log[axis=z]")
        t.set(cx + 1, height - 2, cz + 1 + i, "minecraft:dark_oak_log[axis=z]")
    for x in range(sx):
        for z in range(sz):
            for y in range(height - 2, sy):
                r = math.sqrt((x - cx - 0.5) ** 2 + (z - cz - 0.5) ** 2 + ((y - height - 1) * 1.6) ** 2)
                if r < 6.2 - rng.random() * 0.8 and t.get(x, y, z) in (None, AIR):
                    t.set(x, y, z, DARK_LEAVES)
    for x in range(cx - 2, cx + 1):
        for z in range(cz - 2, cz + 1):
            if t.get(x, height - 1, z) != "minecraft:dark_oak_log[axis=y]":
                t.set(x, height - 1, z, "minecraft:dark_oak_planks")
            for y in (height, height + 1):
                if t.get(x, y, z) == DARK_LEAVES:
                    t.set(x, y, z, AIR)
    t.chest(cx - 1, height, cz - 1, "koschei_oak", facing="south")
    t.set(cx - 2, height, cz - 2, "minecraft:chain[axis=y,waterlogged=false]")
    # Ladders up the south side of the trunk.
    for y in range(1, height - 1):
        t.set(cx, y, cz + 2, "minecraft:ladder[facing=south,waterlogged=false]")
    t.set(cx, 1, cz + 2, "minecraft:ladder[facing=south,waterlogged=false]")
    t.fill(cx, height - 1, cz + 2, cx, height, cz + 2, "minecraft:ladder[facing=south,waterlogged=false]")
    t.entity(3.5, 1.0, 11.5, f"{NS}:volkolak")
    t.entity(11.5, 1.0, 3.5, f"{NS}:volkolak")
    return t


# ---------------------------------------------------------------- the nest of Solovei on nine oaks

def solovei_nest():
    sx, sy, sz = 15, 18, 15
    t = Template(sx, sy, sz)
    rng = random.Random(95)
    ground(t, rng, [("minecraft:podzol", 40), ("minecraft:grass_block[snowy=false]", 40), ("minecraft:coarse_dirt", 20)])
    deck = 9
    trunks = [(x, z) for x in (3, 7, 11) for z in (3, 7, 11)]
    for x, z in trunks:
        t.fill(x, 1, z, x, deck + 2, z, "minecraft:oak_log[axis=y]")
    # The nest: a deck of logs and hay with a rail of fences, a heap of branches around the edge.
    for x in range(2, 13):
        for z in range(2, 13):
            if (x, z) in trunks:
                continue
            t.set(x, deck, z, pick(rng, [("minecraft:oak_planks", 50), ("minecraft:hay_block[axis=y]", 30),
                                         ("minecraft:oak_log[axis=x]", 20)]))
            if x in (2, 12) or z in (2, 12):
                t.set(x, deck + 1, z, pick(rng, [(FENCE, 60), (OAK_LEAVES, 40)]))
    for x in range(1, 14):
        for z in range(1, 14):
            for y in range(deck + 3, deck + 7):
                r = math.sqrt((x - 7) ** 2 + (z - 7) ** 2 + ((y - deck - 4) * 2.0) ** 2)
                if 4.0 < r < 7.2 and rng.random() < 0.8:
                    t.set(x, y, z, OAK_LEAVES)
    # Ladder up the trunk at the south-west, an opening in the rail above it.
    for y in range(1, deck):
        t.set(3, y, 4, "minecraft:ladder[facing=south,waterlogged=false]")
    t.set(3, deck, 4, AIR)
    t.set(3, deck + 1, 4, AIR)
    t.chest(10, deck + 1, 10, "solovei_nest", facing="north")
    t.chest(4, deck + 1, 10, "solovei_nest", facing="north")
    t.set(7, deck + 1, 4, CAMPFIRE)
    t.entity(7.5, deck + 1.0, 9.5, f"{NS}:solovei")
    return t


# ---------------------------------------------------------------- the Kalinov bridge over the river Smorodina

def kalinov_bridge():
    sx, sy, sz = 37, 12, 23
    t = Template(sx, sy, sz)
    rng = random.Random(96)
    banks = [("minecraft:blackstone", 50), ("minecraft:basalt[axis=y]", 30), ("minecraft:magma_block", 20)]
    ground(t, rng, banks)
    # The river of fire runs north to south across the middle; the bridge crosses it from west to east.
    for x in range(10, 27):
        for z in range(sz):
            t.set(x, 0, z, "minecraft:lava[level=0]")
    for x in (9, 27):
        for z in range(sz):
            t.set(x, 1, z, "minecraft:blackstone")
    bridge_z = range(8, 15)
    for x in range(4, 33):
        for z in bridge_z:
            arch = 2 if 12 <= x <= 24 else 1
            t.set(x, arch, z, pick(rng, [("minecraft:polished_blackstone_bricks", 60), ("minecraft:cracked_polished_blackstone_bricks", 25),
                                         ("minecraft:gilded_blackstone", 15)]) if z in (8, 14) else
                  pick(rng, [("minecraft:red_nether_bricks", 60), ("minecraft:nether_bricks", 40)]))
            if arch == 2 and x in (12, 24):
                t.set(x, 1, z, "minecraft:polished_blackstone_bricks")
        for z in (8, 14):
            arch = 2 if 12 <= x <= 24 else 1
            t.set(x, arch + 1, z, "minecraft:red_nether_brick_wall" if x % 4 else "minecraft:polished_blackstone_bricks")
            if x % 4 == 0:
                t.set(x, arch + 2, z, SOUL_LANTERN)
    # Piers under the arch.
    for x in (15, 21):
        for z in bridge_z:
            t.set(x, 0, z, "minecraft:polished_blackstone_bricks")
            t.set(x, 1, z, "minecraft:polished_blackstone_bricks")
    # The guarded far bank: the dragon's hoard.
    t.chest(33, 1, 10, "kalinov_bridge", facing="west")
    t.chest(33, 1, 12, "kalinov_bridge", facing="west")
    t.set(34, 1, 11, "minecraft:gold_block")
    t.entity(30.5, 1.0, 11.5, f"{NS}:zmey_gorynych")
    return t


# ---------------------------------------------------------------- the castle of Koschei

def koschei_castle():
    sx, sy, sz = 31, 22, 31
    t = Template(sx, sy, sz)
    rng = random.Random(97)
    stone = [("minecraft:deepslate_bricks", 55), ("minecraft:cracked_deepslate_bricks", 20), ("minecraft:deepslate_tiles", 15),
             ("minecraft:blackstone", 10)]
    ground(t, rng, [("minecraft:soul_soil", 50), ("minecraft:coarse_dirt", 30), ("minecraft:podzol", 20)])
    wall_top = 9
    # Curtain wall with battlements and four round towers at the corners.
    for x in range(1, sx - 1):
        for z in range(1, sz - 1):
            edge = x in (1, sx - 2) or z in (1, sz - 2)
            if edge:
                t.fill(x, 0, z, x, wall_top, z, pick(rng, stone))
                if (x + z) % 2 == 0:
                    t.set(x, wall_top + 1, z, "minecraft:polished_blackstone_brick_wall")
            else:
                t.set(x, 0, z, pick(rng, [("minecraft:polished_blackstone_bricks", 60), ("minecraft:soul_soil", 20),
                                          ("minecraft:deepslate_tiles", 20)]))
    for cx, cz in ((3, 3), (sx - 4, 3), (3, sz - 4), (sx - 4, sz - 4)):
        for x in range(cx - 3, cx + 4):
            for z in range(cz - 3, cz + 4):
                r = math.hypot(x - cx, z - cz)
                if r <= 3.2 and t.inside(x, 0, z):
                    for y in range(0, wall_top + 5):
                        t.set(x, y, z, pick(rng, stone) if r > 2.2 else AIR if y > 0 else "minecraft:deepslate_tiles")
                    if 2.2 < r <= 3.2:
                        t.set(x, wall_top + 5, z, "minecraft:polished_blackstone_brick_wall" if (x + z) % 2 else AIR)
                    for y in range(wall_top + 5, wall_top + 9):
                        if r <= 3.2 - (y - wall_top - 5) * 0.9:
                            t.set(x, y + 1, z, "minecraft:blackstone")
        t.set(cx, 1, cz, SOUL_LANTERN)
    # Gate in the south wall with iron bars.
    mid = sx // 2
    t.fill(mid - 2, 1, sz - 2, mid + 2, 5, sz - 2, AIR)
    t.fill(mid - 2, 5, sz - 2, mid + 2, 5, sz - 2, "minecraft:iron_bars")
    # The keep: a hall with the throne of bones.
    k0, k1 = 8, sx - 9
    for x in range(k0, k1 + 1):
        for z in range(5, 20):
            edge = x in (k0, k1) or z in (5, 19)
            for y in range(1, 13):
                t.set(x, y, z, pick(rng, stone) if edge else AIR)
            t.set(x, 13, z, "minecraft:deepslate_tile_slab[type=bottom]")
    for x in range(mid - 1, mid + 2):
        t.fill(x, 1, 19, x, 4, 19, AIR)
    for z in (9, 13, 17):
        for x in (k0, k1):
            t.set(x, 6, z, "minecraft:iron_bars")
    for z in range(8, 19, 4):
        for x in (k0 + 2, k1 - 2):
            t.fill(x, 1, z, x, 12, z, "minecraft:polished_blackstone_bricks")
            t.set(x, 7, z + 1 if z + 1 < 19 else z - 1, SOUL_LANTERN)
    for x in range(k0 + 1, k1):
        for z in range(6, 19):
            t.set(x, 0, z, "minecraft:polished_blackstone_bricks" if (x + z) % 2 else "minecraft:polished_deepslate")
    for x in range(mid - 1, mid + 2):
        for z in range(6, 19):
            t.set(x, 1, z, "minecraft:purple_carpet")
    t.fill(mid - 2, 1, 6, mid + 2, 1, 8, "minecraft:bone_block[axis=y]")
    t.fill(mid - 1, 2, 6, mid + 1, 2, 6, "minecraft:bone_block[axis=y]")
    t.set(mid, 2, 7, "minecraft:gold_block")
    t.set(mid, 3, 6, "minecraft:wither_skeleton_skull[rotation=8]")
    t.chest(mid - 2, 2, 7, "koschei_castle", facing="south")
    t.chest(mid + 2, 2, 7, "koschei_castle", facing="south")
    t.entity(mid + 0.5, 1.0, 10.5, f"{NS}:koschei")
    t.entity(mid - 3.5, 1.0, 15.5, f"{NS}:upyr")
    t.entity(mid + 4.5, 1.0, 15.5, f"{NS}:upyr")
    # Bones and soul fires in the yard.
    for x, z in ((5, 22), (25, 22), (6, 26), (24, 26)):
        t.set(x, 1, z, SOUL_CAMPFIRE)
    for _ in range(12):
        x, z = rng.randrange(3, sx - 3), rng.randrange(21, sz - 3)
        if t.get(x, 1, z) in (None, AIR):
            t.set(x, 1, z, "minecraft:bone_block[axis=y]")
    return t


STRUCTURES = {
    "slavic_village": slavic_village,
    "baba_yaga_hut": baba_yaga_hut,
    "kapishche": kapishche,
    "koschei_oak": koschei_oak,
    "solovei_nest": solovei_nest,
    "kalinov_bridge": kalinov_bridge,
    "koschei_castle": koschei_castle,
}
