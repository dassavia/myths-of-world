"""Structure templates of Jotunheim, written as .nbt files. Same conventions as structures.py: x east, y up, z south,
origin at the corner, y = 0 is the ground the template stands on."""
import math
import random

import nbt
from structures import AIR, Template, pick

NS = "mythsofworlds"
RUNESTONE = f"{NS}:runestone"
CARVED = f"{NS}:carved_runestone"
IRONWOOD_LOG = f"{NS}:ironwood_log[axis=y]"
IRONWOOD_PLANKS = f"{NS}:ironwood_planks"
FENCE = "minecraft:spruce_fence"
LANTERN = "minecraft:lantern[hanging=true]"
STANDING_LANTERN = "minecraft:lantern[hanging=false]"
SOUL_LANTERN = "minecraft:soul_lantern[hanging=false]"
CAMPFIRE = "minecraft:campfire[lit=true,signal_fire=false]"
EARTH = [("minecraft:grass_block[snowy=false]", 70), ("minecraft:coarse_dirt", 20), ("minecraft:podzol", 10)]


def stairs(block, facing, half="bottom"):
    return f"minecraft:{block}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]"


def standing_stone(t, x, z, height, rng, top=CARVED):
    t.fill(x, 1, z, x, height, z, RUNESTONE)
    t.set(x, rng.randint(1, height), z, top)


# ---------------------------------------------------------------- longhouses and the Viking village

def longhouse(t, x0, z0, length, width, rng, chest=None, merchant=None, hearth=True):
    """Timber longhouse along x: stone footing, log posts, plank walls, a steep dark roof with a smoke hole over the
    hearth, a door in the middle of each long side, benches along the walls."""
    x1, z1 = x0 + length - 1, z0 + width - 1
    half = width // 2
    wall_top = 3
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            t.set(x, 0, z, "minecraft:cobblestone" if edge else pick(rng, [("minecraft:spruce_planks", 70), ("minecraft:dirt_path", 30)]))
            for y in range(1, wall_top + 1):
                if edge:
                    post = (x - x0) % 4 == 0 or z in (z0, z1) and x in (x0, x1)
                    t.set(x, y, z, "minecraft:spruce_log[axis=y]" if post else "minecraft:spruce_planks")
                else:
                    t.set(x, y, z, AIR)
            for y in range(wall_top + 1, wall_top + half + 2):
                t.set(x, y, z, AIR)
    # Roof: stairs rising from both long sides to a ridge of slabs.
    for k in range(half + 1):
        y = wall_top + 1 + k
        for x in range(x0, x1 + 1):
            if k < half:
                t.set(x, y, z0 + k, stairs("dark_oak", "south"))
                t.set(x, y, z1 - k, stairs("dark_oak", "north"))
            else:
                t.set(x, y, z0 + k, "minecraft:dark_oak_slab[type=bottom]")
        # Gable ends filled with planks under the slope.
        for z in range(z0 + k + 1, z1 - k):
            t.set(x0, y, z, "minecraft:spruce_planks")
            t.set(x1, y, z, "minecraft:spruce_planks")
    # Crossed dragon-head gable posts, standing on a full block at each end of the ridge (a fence on a bottom slab
    # would hover half a block above it).
    for x in (x0, x1):
        t.set(x, wall_top + 1 + half, z0 + half, "minecraft:dark_oak_planks")
        t.set(x, wall_top + half + 2, z0 + half, "minecraft:dark_oak_fence")
    # Doors in the middle of both long sides.
    mx = x0 + length // 2
    for z, facing in ((z0, "north"), (z1, "south")):
        t.set(mx, 1, z, f"minecraft:spruce_door[facing={facing},half=lower,hinge=left,open=false,powered=false]")
        t.set(mx, 2, z, f"minecraft:spruce_door[facing={facing},half=upper,hinge=left,open=false,powered=false]")
    # Long hearth down the middle, benches along the walls.
    if hearth:
        for x in range(x0 + 2, x1 - 1):
            if x != mx:
                t.set(x, 0, z0 + half, "minecraft:cobblestone")
        t.set(x0 + 3, 1, z0 + half, CAMPFIRE)
        t.set(x1 - 3, 1, z0 + half, CAMPFIRE)
    for x in range(x0 + 1, x1):
        if x != mx:
            t.set(x, 1, z0 + 1, "minecraft:spruce_slab[type=bottom]")
            t.set(x, 1, z1 - 1, "minecraft:spruce_slab[type=bottom]")
    # A tie beam down the length of the hall, lanterns hanging from it.
    for x in range(x0 + 1, x1):
        t.set(x, wall_top + 1, z0 + half, "minecraft:spruce_log[axis=x]")
    for x in range(x0 + 2, x1 - 1, 4):
        if x != mx:
            t.set(x, wall_top, z0 + half, LANTERN)
    # Shields on the walls inside.
    for x in range(x0 + 2, x1 - 1, 3):
        colour = rng.choice(("red", "yellow", "blue", "white"))
        t.set(x, 2, z0 + 1, f"minecraft:{colour}_wall_banner[facing=south]")
    if chest:
        t.chest(x0 + 1, 1, z0 + half - 1, chest, facing="east")
        t.set(x0 + 1, 1, z0 + half + 1, "minecraft:barrel[facing=up,open=false]")
    if merchant is not None:
        t.entity(x1 - 2 + 0.5, 1.0, z0 + half + 0.5, f"{NS}:norse_merchant", {"Kind": merchant})


def smithy(t, x0, z0, rng):
    """Open dwarf smithy, 7x5: a roof on posts over the forge, anvil and quenching trough. Home of a dwarf smith."""
    for x in range(x0, x0 + 7):
        for z in range(z0, z0 + 5):
            t.set(x, 0, z, pick(rng, [("minecraft:cobblestone", 50), ("minecraft:stone_bricks", 30), ("minecraft:gravel", 20)]))
            for y in range(1, 4):
                t.set(x, y, z, AIR)
            t.set(x, 4, z, "minecraft:spruce_slab[type=bottom]")
    for x, z in ((x0, z0), (x0 + 6, z0), (x0, z0 + 4), (x0 + 6, z0 + 4)):
        t.fill(x, 1, z, x, 3, z, "minecraft:spruce_log[axis=y]")
    t.fill(x0 + 1, 1, z0, x0 + 3, 2, z0, "minecraft:stone_bricks")
    t.set(x0 + 2, 1, z0 + 1, "minecraft:blast_furnace[facing=south,lit=true]")
    t.set(x0 + 1, 1, z0 + 1, "minecraft:lava_cauldron")
    t.set(x0 + 3, 1, z0 + 1, "minecraft:smithing_table")
    t.set(x0 + 4, 1, z0 + 2, "minecraft:anvil[facing=east]")
    t.set(x0 + 5, 1, z0 + 1, "minecraft:water_cauldron[level=3]")
    t.set(x0 + 5, 1, z0 + 3, "minecraft:grindstone[face=floor,facing=north]")
    t.chest(x0 + 1, 1, z0 + 3, "dwarf_forge", facing="east")
    t.set(x0 + 3, 3, z0 + 2, LANTERN)
    t.entity(x0 + 3.5, 1.0, z0 + 3.5, f"{NS}:norse_merchant", {"Kind": 1})


def volva_hut(t, cx, cz, rng):
    """Small round hut of the seeress: turf walls, a cauldron, herbs and her runes."""
    for x in range(cx - 3, cx + 4):
        for z in range(cz - 3, cz + 4):
            r = math.hypot(x - cx, z - cz)
            if r > 3.3:
                continue
            t.set(x, 0, z, "minecraft:spruce_planks" if r < 2.6 else "minecraft:mossy_cobblestone")
            for y in range(1, 5):
                t.set(x, y, z, AIR)
            if r >= 2.6:
                t.fill(x, 1, z, x, 2, z, pick(rng, [("minecraft:mud_bricks", 40), ("minecraft:packed_mud", 30), ("minecraft:spruce_planks", 30)]))
            y = 3 if r >= 1.6 else 4
            t.set(x, y, z, pick(rng, [("minecraft:moss_block", 60), ("minecraft:grass_block[snowy=false]", 40)]))
    t.set(cx, 1, cz + 3, AIR)
    t.set(cx, 2, cz + 3, AIR)
    t.set(cx - 1, 1, cz - 1, "minecraft:water_cauldron[level=3]")
    t.set(cx + 1, 1, cz - 1, "minecraft:brewing_stand[has_bottle_0=false,has_bottle_1=false,has_bottle_2=false]")
    t.set(cx + 1, 1, cz + 1, "minecraft:flower_pot")
    t.set(cx - 1, 1, cz + 1, CARVED)
    t.set(cx, 3, cz, LANTERN)
    t.entity(cx + 0.5, 1.0, cz + 0.5, f"{NS}:norse_merchant", {"Kind": 2})


def viking_village():
    size = 49
    t = Template(size, 12, size)
    rng = random.Random(9)
    c = size // 2
    t.fill(0, 1, 0, size - 1, 11, size - 1, AIR)
    for x in range(size):
        for z in range(size):
            road = abs(x - c) <= 1 or abs(z - c) <= 1
            t.set(x, 0, z, "minecraft:dirt_path" if road and rng.random() < 0.85 else pick(rng, EARTH))
    # The jarl's mead hall in the middle, with the steward.
    longhouse(t, c - 9, c - 5, 19, 11, rng, chest="viking_village", merchant=0)
    t.set(c - 7, 1, c, "minecraft:spruce_stairs[facing=east]")
    t.set(c - 7, 1, c + 1, "minecraft:barrel[facing=up,open=false]")
    # Longhouses of the families.
    for x0, z0 in ((3, 3), (29, 3), (3, 38), (29, 38)):
        longhouse(t, x0, z0, 15, 7, rng, chest="viking_house")
    smithy(t, 4, 27, rng)
    volva_hut(t, 41, 24, rng)
    # Goat pen and a well.
    for x in range(36, 46):
        for z in range(13, 20):
            if x in (36, 45) or z in (13, 19):
                t.set(x, 1, z, FENCE)
    t.set(41, 1, 19, "minecraft:spruce_fence_gate[facing=south,in_wall=false,open=false,powered=false]")
    for x, z in ((38.5, 15.5), (42.5, 16.5), (40.5, 17.5)):
        t.entity(x, 1.0, z, "minecraft:goat")
    t.fill(37, 1, 14, 37, 1, 14, "minecraft:hay_block[axis=y]")
    wx, wz = c + 6, c + 9
    for x in range(wx - 1, wx + 2):
        for z in range(wz - 1, wz + 2):
            t.set(x, 0, z, "minecraft:water" if (x, z) == (wx, wz) else "minecraft:cobblestone")
            t.set(x, 1, z, AIR if (x, z) == (wx, wz) else "minecraft:cobblestone_wall")
    # Runestone at the crossroads, torches along the roads.
    standing_stone(t, c + 3, c - 8, 3, rng)
    for x, z in ((c - 2, 4), (c + 2, 44), (4, c + 2), (44, c - 2), (c - 2, 30), (c + 2, 18)):
        t.fill(x, 1, z, x, 2, z, FENCE)
        t.set(x, 3, z, STANDING_LANTERN)
    # Spruce trees and wood piles.
    for x, z in ((20, 2), (46, 30), (1, 34), (24, 46)):
        h = rng.randint(4, 6)
        t.fill(x, 1, z, x, h, z, "minecraft:spruce_log[axis=y]")
        for y in range(h - 2, h + 2):
            r = 2 if y < h else 1
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if (dx or dz or y > h) and abs(dx) + abs(dz) <= r + 1 and t.inside(x + dx, y, z + dz) and t.get(x + dx, y, z + dz) == AIR:
                        t.set(x + dx, y, z + dz, "minecraft:spruce_leaves[distance=1,persistent=true,waterlogged=false]")
        t.set(x, h + 2, z, "minecraft:spruce_leaves[distance=1,persistent=true,waterlogged=false]")
    for x, z in ((22, 34), (28, 12)):
        t.fill(x, 1, z, x + 2, 1, z, "minecraft:spruce_log[axis=x]")
        t.set(x + 1, 2, z, "minecraft:spruce_log[axis=x]")
    return t


# ---------------------------------------------------------------- longships

def longship(dead=False):
    """Drakkar with a dragon prow, a row of shields along each side and a striped sail. With dead=True it is
    Naglfar, the ship of the dead made of dead men's nails, with a crew of draugr and a black sail."""
    width, height, length = 9, 16, 29
    t = Template(width, height, length)
    rng = random.Random(77 if dead else 7)
    c = width // 2
    if dead:
        hull = [("minecraft:dark_oak_planks", 50), ("minecraft:deepslate_tiles", 30), ("minecraft:bone_block[axis=y]", 20)]
        deck, rail, keel = "minecraft:dark_oak_planks", "minecraft:dark_oak_fence", "minecraft:polished_blackstone_bricks"
        shields = ("minecraft:black_wool", "minecraft:gray_wool")
        sail = ("minecraft:black_wool", "minecraft:gray_wool")
    else:
        hull = [("minecraft:spruce_planks", 75), ("minecraft:oak_planks", 25)]
        deck, rail, keel = "minecraft:spruce_planks", FENCE, "minecraft:spruce_log[axis=z]"
        shields = ("minecraft:red_wool", "minecraft:yellow_wool")
        sail = ("minecraft:red_wool", "minecraft:white_wool")

    def half_width(z, y):
        w = min(3, 1 + y // 2 + (1 if y >= 3 else 0))
        end = min(z, length - 1 - z)
        return min(w, max(0, end - 1 + y // 2))

    for z in range(length):
        for y in range(0, 5):
            w = half_width(z, y)
            for x in range(width):
                d = abs(x - c)
                if d > w:
                    continue
                if y == 0 and d == 0:
                    t.set(x, y, z, keel)
                elif y == 4:
                    t.set(x, y, z, deck if d < w else pick(rng, hull))
                elif d < w and y > 0 and half_width(z - 1, y) > d and half_width(z + 1, y) > d:
                    t.set(x, y, z, AIR)
                else:
                    t.set(x, y, z, pick(rng, hull))
    # Shields hung along the gunwales, rails, oars.
    for z in range(5, length - 5):
        w = half_width(z, 4)
        for x in (c - w, c + w):
            if t.get(x, 4, z) is not None:
                t.set(x, 5, z, shields[(z // 2) % 2] if z % 2 == 0 else rail)
    # Oars run out through the hull wherever it reaches the side of the template.
    for z in range(6, length - 6, 3):
        for x, inner in ((0, 1), (width - 1, width - 2)):
            if t.get(inner, 3, z) not in (None, AIR):
                t.set(x, 3, z, "minecraft:spruce_fence")
    # The curving prow and stern posts; the dragon head on the prow.
    for k in range(4):
        t.set(c, 5 + k, length - 2 + min(1, k // 2), "minecraft:dark_oak_log[axis=y]")
        t.set(c, 5 + k, 1 - min(1, k // 2), "minecraft:dark_oak_log[axis=y]")
    t.set(c, 9, length - 1, "minecraft:wither_skeleton_skull[rotation=0]" if dead else "minecraft:dragon_head[rotation=0]")
    t.set(c, 9, 0, "minecraft:dark_oak_fence")
    # Mast, yard and the sail.
    mz = length // 2
    t.fill(c, 5, mz, c, height - 1, mz, "minecraft:spruce_log[axis=y]")
    t.fill(0, height - 2, mz, width - 1, height - 2, mz, "minecraft:spruce_log[axis=x]")
    for y in range(7, height - 2):
        for x in range(1, width - 1):
            t.set(x, y, mz + 1, sail[(x - 1) // 2 % 2])
    # Cargo and treasure at the stern, a lantern on the mast.
    t.chest(c, 5, 4, "naglfar" if dead else "longship", facing="south")
    t.set(c - 1, 5, 4, "minecraft:barrel[facing=up,open=false]")
    t.set(c + 1, 5, 5, "minecraft:barrel[facing=up,open=false]")
    t.set(c, 8, mz - 1, SOUL_LANTERN if dead else STANDING_LANTERN)
    t.fill(c, 5, mz - 1, c, 7, mz - 1, "minecraft:spruce_fence")
    if dead:
        for x, z in ((c - 1, 8), (c + 1, 12), (c - 1, 18), (c + 1, 22), (c, 24)):
            t.entity(x + 0.5, 5.0, z + 0.5, f"{NS}:draugr")
        for z in (9, 20):
            t.set(c, 5, z, "minecraft:bone_block[axis=y]")
    return t


# ---------------------------------------------------------------- barrow of the Draugr chieftain

def barrow():
    size = 23
    t = Template(size, 10, size)
    rng = random.Random(21)
    c = size // 2
    for x in range(size):
        for z in range(size):
            r = math.hypot(x - c, z - c)
            t.set(x, 0, z, pick(rng, EARTH) if r > 7 else pick(rng, [("minecraft:stone_bricks", 50), ("minecraft:mossy_stone_bricks", 30), ("minecraft:cracked_stone_bricks", 20)]))
            # The grassy mound: a low dome.
            top = int(round(7.5 * math.sqrt(max(0.0, 1.0 - (r / 10.5) ** 2))))
            for y in range(1, 10):
                if y < top:
                    t.set(x, y, z, pick(rng, [("minecraft:dirt", 70), ("minecraft:coarse_dirt", 20), ("minecraft:rooted_dirt", 10)]))
                elif y == top and top > 0:
                    t.set(x, y, z, "minecraft:grass_block[snowy=false]")
                else:
                    t.set(x, y, z, AIR)
    # The stone chamber inside, and the passage from the south.
    for x in range(c - 4, c + 5):
        for z in range(c - 4, c + 5):
            edge = x in (c - 4, c + 4) or z in (c - 4, c + 4)
            for y in range(1, 5):
                t.set(x, y, z, pick(rng, [("minecraft:mossy_stone_bricks", 50), ("minecraft:stone_bricks", 35), ("minecraft:cracked_stone_bricks", 15)]) if edge else AIR)
            t.set(x, 5, z, "minecraft:stone_bricks")
    for z in range(c + 4, size):
        for x in (c - 1, c, c + 1):
            for y in (1, 2):
                t.set(x, y, z, AIR)
            t.set(x, 3, z, "minecraft:stone_bricks" if t.get(x, 3, z) != AIR else "minecraft:stone_brick_slab[type=bottom]")
        for x in (c - 2, c + 2):
            for y in (1, 2):
                if t.get(x, y, z) == AIR or z < size - 3:
                    t.set(x, y, z, "minecraft:mossy_stone_bricks")
    # Grave goods: the king's bier, chests, bones and cobwebs.
    t.fill(c - 1, 1, c - 3, c + 1, 1, c - 2, "minecraft:polished_andesite")
    t.set(c, 2, c - 3, "minecraft:skeleton_skull[rotation=8]")
    t.chest(c - 3, 1, c - 3, "barrow", facing="east")
    t.chest(c + 3, 1, c - 3, "barrow", facing="west")
    t.set(c - 3, 1, c + 2, "minecraft:bone_block[axis=y]")
    t.set(c + 3, 1, c + 3, "minecraft:cobweb")
    t.set(c - 3, 3, c - 1, "minecraft:cobweb")
    t.set(c + 3, 3, c + 1, "minecraft:cobweb")
    t.set(c, 4, c, SOUL_LANTERN.replace("false", "true"))
    t.entity(c + 0.5, 1.0, c + 0.5, f"{NS}:draugr_chieftain")
    t.entity(c - 2 + 0.5, 1.0, c + 2 + 0.5, f"{NS}:draugr")
    t.entity(c + 2 + 0.5, 1.0, c + 2 + 0.5, f"{NS}:draugr")
    # Standing stones around the mound.
    for i in range(6):
        a = i * math.pi / 3 + 0.3
        standing_stone(t, int(round(c + math.cos(a) * 10.4)), int(round(c + math.sin(a) * 10.4)), 2, rng)
    return t


# ---------------------------------------------------------------- Utgard, the ice hall of Thrym

def utgard():
    sx, sy, sz = 33, 22, 41
    t = Template(sx, sy, sz)
    rng = random.Random(33)
    ice = [("minecraft:packed_ice", 75), ("minecraft:blue_ice", 15), ("minecraft:snow_block", 10)]
    t.fill(0, 1, 0, sx - 1, sy - 1, sz - 1, AIR)
    for x in range(sx):
        for z in range(sz):
            t.set(x, 0, z, pick(rng, [("minecraft:packed_ice", 50), ("minecraft:snow_block", 35), ("minecraft:blue_ice", 15)]))
    wall_top = 13
    for y in range(1, wall_top + 1):
        for x in range(sx):
            for z in (0, sz - 1):
                t.set(x, y, z, "minecraft:blue_ice" if y % 5 == 0 else pick(rng, ice))
        for z in range(sz):
            for x in (0, sx - 1):
                t.set(x, y, z, "minecraft:blue_ice" if y % 5 == 0 else pick(rng, ice))
    # Stepped roof of ice.
    for k in range(0, 8):
        y = wall_top + 1 + k
        for x in range(2 * k, sx - 2 * k):
            for z in range(0, sz):
                if x in (2 * k, 2 * k + 1, sx - 1 - 2 * k, sx - 2 - 2 * k) or k == 7:
                    t.set(x, y, z, pick(rng, ice))
    # Gable ends of the roof.
    for k in range(0, 8):
        for x in range(2 * k, sx - 2 * k):
            for z in (0, sz - 1):
                t.set(x, wall_top + 1 + k, z, pick(rng, ice))
    # Great door in the south wall, tall enough for giants.
    t.fill(12, 1, sz - 1, 20, 10, sz - 1, AIR)
    for x in (11, 21):
        t.fill(x, 1, sz - 1, x, 11, sz - 1, "minecraft:blue_ice")
    t.fill(11, 11, sz - 1, 21, 11, sz - 1, "minecraft:blue_ice")
    # Rows of ice pillars with sea lanterns.
    for z in range(6, sz - 4, 6):
        for x in (7, sx - 8):
            t.fill(x, 1, z, x, wall_top, z, "minecraft:blue_ice")
            t.set(x, 7, z, "minecraft:sea_lantern")
    for z in range(4, sz - 2, 8):
        for x in (1, sx - 2):
            t.set(x, 8, z, "minecraft:sea_lantern")
    # Throne of Thrym on a dais at the north end, his treasure behind it.
    for x in range(10, 23):
        for z in range(1, 9):
            t.set(x, 1, z, "minecraft:packed_ice")
            if 12 <= x <= 20 and z <= 6:
                t.set(x, 2, z, "minecraft:snow_block")
    t.fill(15, 3, 2, 17, 3, 3, "minecraft:blue_ice")
    t.fill(15, 4, 2, 17, 7, 2, "minecraft:blue_ice")
    t.set(14, 4, 3, "minecraft:blue_ice")
    t.set(18, 4, 3, "minecraft:blue_ice")
    t.set(16, 8, 2, "minecraft:diamond_block")
    t.chest(13, 3, 1, "utgard", facing="south")
    t.chest(19, 3, 1, "utgard", facing="south")
    t.set(16, 3, 1, "minecraft:gold_block")
    # Long tables of the giants' feast.
    for x in (11, 21):
        for z in range(14, 32):
            t.set(x, 1, z, "minecraft:spruce_planks" if z % 6 else "minecraft:spruce_log[axis=y]")
        t.set(x, 2, 18, "minecraft:cake[bites=0]")
        t.set(x, 2, 26, "minecraft:barrel[facing=up,open=false]")
    for z in (12, 24, 34):
        t.set(16, 1, z, CAMPFIRE)
    t.entity(16.5, 1.0, 11.5, f"{NS}:thrym")
    t.entity(9.5, 1.0, 30.5, f"{NS}:frost_giant")
    t.entity(23.5, 1.0, 30.5, f"{NS}:frost_giant")
    return t


# ---------------------------------------------------------------- island of Lyngvi, where Fenrir is bound

def fenrir_island():
    size = 31
    t = Template(size, 12, size)
    rng = random.Random(41)
    c = size // 2
    t.fill(0, 1, 0, size - 1, 11, size - 1, AIR)
    for x in range(size):
        for z in range(size):
            r = math.hypot(x - c, z - c)
            if r <= 15.2:
                t.set(x, 0, z, pick(rng, [("minecraft:stone", 35), ("minecraft:gravel", 25), ("minecraft:mossy_cobblestone", 20),
                                          ("minecraft:coarse_dirt", 20)]))
            # A ring of jagged rocks around the clearing.
            if 12.5 <= r <= 15.0 and rng.random() < 0.55:
                h = rng.randint(1, 4)
                t.fill(x, 1, z, x, h, z, pick(rng, [("minecraft:stone", 50), ("minecraft:andesite", 25), ("minecraft:mossy_cobblestone", 25)]))
    for z in range(c + 11, size):
        for x in range(c - 2, c + 3):
            for y in range(1, 5):
                t.set(x, y, z, AIR)
    # Gjoll, the boulder the fetter is fastened to, and Thviti, the stone driven into the earth.
    for x in range(c - 2, c + 3):
        for z in range(c - 9, c - 5):
            for y in range(1, 6):
                if math.hypot((x - c) / 2.5, (y - 1) / 5.0, (z - c + 7) / 2.0) <= 1.0:
                    t.set(x, y, z, pick(rng, [("minecraft:stone", 60), ("minecraft:cobblestone", 40)]))
    t.fill(c, 1, c - 5, c, 3, c - 5, "minecraft:polished_deepslate")
    # Broken chains of Laeding and Dromi, the fetters Fenrir burst before Gleipnir held him.
    for x, z, h in ((c - 6, c - 3, 4), (c + 6, c - 3, 4), (c - 5, c + 5, 3), (c + 5, c + 5, 3)):
        t.fill(x, 1, z, x, h, z, CARVED if h == 4 else RUNESTONE)
        t.set(x, h + 1, z, "minecraft:chain[axis=y]")
    for x in range(c - 4, c + 5):
        if x != c:
            t.set(x, 1, c - 4, "minecraft:chain[axis=x]")
    for z in range(c - 4, c - 1):
        t.set(c, 1, z, "minecraft:chain[axis=z]")
    for x, z in ((c - 3, c + 2), (c + 4, c + 1), (c + 2, c + 7), (c - 6, c + 1)):
        t.set(x, 1, z, "minecraft:bone_block[axis=y]")
    t.set(c + 7, 1, c - 1, "minecraft:skeleton_skull[rotation=4]")
    t.chest(c + 2, 1, c - 6, "fenrir_island", facing="west")
    t.entity(c + 0.5, 1.0, c + 0.5, f"{NS}:fenrir")
    return t


# ---------------------------------------------------------------- fortress of Surtr in Muspelheim

def muspel_fortress():
    size, height = 35, 20
    t = Template(size, height, size)
    rng = random.Random(55)
    c = size // 2
    t.fill(0, 1, 0, size - 1, height - 1, size - 1, AIR)
    bricks = [("minecraft:polished_blackstone_bricks", 60), ("minecraft:cracked_polished_blackstone_bricks", 20),
              ("minecraft:blackstone", 15), ("minecraft:gilded_blackstone", 5)]
    for x in range(size):
        for z in range(size):
            t.set(x, 0, z, pick(rng, [("minecraft:basalt[axis=y]", 40), ("minecraft:blackstone", 40), ("minecraft:magma_block", 20)]))
    # Outer wall with corner towers.
    for x in range(size):
        for z in range(size):
            if x in (0, size - 1) or z in (0, size - 1):
                for y in range(1, 8):
                    t.set(x, y, z, pick(rng, bricks))
                if (x + z) % 2 == 0:
                    t.set(x, 8, z, "minecraft:polished_blackstone_brick_wall")
    for tx, tz in ((0, 0), (size - 4, 0), (0, size - 4), (size - 4, size - 4)):
        for x in range(tx, tx + 4):
            for z in range(tz, tz + 4):
                for y in range(1, 11):
                    t.set(x, y, z, pick(rng, bricks))
        t.set(tx + 1, 11, tz + 1, "minecraft:shroomlight")
        t.set(tx + 2, 11, tz + 2, "minecraft:shroomlight")
    t.fill(c - 2, 1, size - 1, c + 2, 6, size - 1, AIR)
    # Moat of lava around the keep, crossed by a bridge from the gate.
    for x in range(4, size - 4):
        for z in range(4, size - 4):
            r = max(abs(x - c), abs(z - c))
            if r in (10, 11, 12):
                t.set(x, 0, z, "minecraft:lava")
    for z in range(c + 9, size - 1):
        for x in range(c - 1, c + 2):
            t.set(x, 0, z, "minecraft:polished_blackstone_bricks")
        t.set(c - 2, 1, z, "minecraft:polished_blackstone_brick_wall")
        t.set(c + 2, 1, z, "minecraft:polished_blackstone_brick_wall")
    # The keep.
    k0, k1 = c - 8, c + 8
    for x in range(k0, k1 + 1):
        for z in range(k0, k1 + 1):
            t.set(x, 0, z, "minecraft:polished_blackstone" if (x + z) % 3 else "minecraft:magma_block")
            edge = x in (k0, k1) or z in (k0, k1)
            for y in range(1, 13):
                t.set(x, y, z, pick(rng, bricks) if edge else AIR)
            t.set(x, 13, z, pick(rng, bricks))
            if edge and (x + z) % 2 == 0:
                t.set(x, 14, z, "minecraft:polished_blackstone_brick_wall")
    t.fill(c - 2, 1, k1, c + 2, 8, k1, AIR)
    for x in (k0 + 3, k1 - 3):
        for z in range(k0 + 3, k1 - 2, 4):
            t.fill(x, 1, z, x, 12, z, "minecraft:polished_basalt[axis=y]")
            t.set(x, 6, z, "minecraft:shroomlight")
    # Surtr's throne of gilded stone, fire before it, his hoard.
    t.fill(c - 2, 1, k0 + 1, c + 2, 1, k0 + 3, "minecraft:gilded_blackstone")
    t.fill(c - 1, 2, k0 + 1, c + 1, 5, k0 + 1, "minecraft:gilded_blackstone")
    t.set(c, 6, k0 + 1, "minecraft:gold_block")
    for x in (c - 3, c + 3):
        t.set(x, 1, k0 + 5, "minecraft:netherrack")
        t.set(x, 2, k0 + 5, "minecraft:fire[age=0]")
    t.chest(c - 2, 2, k0 + 1, "muspel_fortress", facing="south")
    t.chest(c + 2, 2, k0 + 1, "muspel_fortress", facing="south")
    t.entity(c + 0.5, 1.0, c + 0.5, f"{NS}:surtr")
    t.entity(c - 5 + 0.5, 1.0, c + 15 + 0.5, f"{NS}:fire_giant")
    t.entity(c + 5 + 0.5, 1.0, c + 15 + 0.5, f"{NS}:fire_giant")
    return t


# ---------------------------------------------------------------- Helgrind, the gate of Hel

def helgrind():
    sx, sy, sz = 27, 18, 17
    t = Template(sx, sy, sz)
    rng = random.Random(66)
    c = sx // 2
    t.fill(0, 1, 0, sx - 1, sy - 1, sz - 1, AIR)
    dark = [("minecraft:deepslate_bricks", 50), ("minecraft:cracked_deepslate_bricks", 20), ("minecraft:polished_blackstone_bricks", 20),
            ("minecraft:deepslate_tiles", 10)]
    for x in range(sx):
        for z in range(sz):
            t.set(x, 0, z, pick(rng, [("minecraft:soul_soil", 35), ("minecraft:packed_ice", 25), ("minecraft:deepslate", 25), ("minecraft:snow_block", 15)]))
    # The wall of Hel with its great gate at z = 3.
    for x in range(sx):
        top = 12 + (2 if x in (c - 7, c + 7, c - 8, c + 8) else 0) + (1 if x % 4 == 0 else 0)
        for y in range(1, top + 1):
            for z in (2, 3, 4):
                t.set(x, y, z, pick(rng, dark))
    t.fill(c - 4, 1, 2, c + 4, 9, 4, AIR)
    t.fill(c - 4, 1, 3, c + 4, 9, 3, "minecraft:iron_bars")
    t.fill(c - 5, 10, 2, c + 5, 10, 4, "minecraft:polished_blackstone_bricks")
    t.set(c, 11, 3, "minecraft:wither_skeleton_skull[rotation=0]")
    for x in (c - 6, c + 6):
        t.fill(x, 1, 5, x, 2, 5, "minecraft:polished_deepslate_wall")
        t.set(x, 3, 5, SOUL_LANTERN)
    # Behind the gate: the darkness of Hel (a black floor and soul fire).
    for x in range(c - 4, c + 5):
        t.set(x, 0, 1, "minecraft:soul_soil")
        t.set(x, 1, 1, "minecraft:soul_fire" if x % 2 == 0 else AIR)
    # Gnipahellir, the cave mouth where Garm is chained, and bones of those who came unbidden.
    for x in range(c - 6, c + 7):
        for z in range(8, sz):
            if rng.random() < 0.08:
                t.set(x, 1, z, pick(rng, [("minecraft:bone_block[axis=y]", 60), ("minecraft:skeleton_skull[rotation=3]", 40)]))
    for x, z in ((c - 3, 6), (c + 3, 6)):
        t.fill(x, 1, z, x, 2, z, "minecraft:polished_deepslate_wall")
        t.set(x, 3, z, "minecraft:chain[axis=y]")
    for x in range(c - 2, c + 3):
        t.set(x, 1, 7, "minecraft:chain[axis=x]")
    for x, z in ((2, 10), (sx - 3, 12), (4, 15), (sx - 5, 8)):
        standing_stone(t, x, z, 3, rng)
    t.chest(1, 1, 6, "helgrind", facing="east")
    t.entity(c + 0.5, 1.0, 10.5, f"{NS}:garm")
    return t


# ---------------------------------------------------------------- forge of the dwarves

def dwarf_forge():
    sx, sy, sz = 17, 9, 15
    t = Template(sx, sy, sz)
    rng = random.Random(88)
    stone = [("minecraft:stone_bricks", 40), ("minecraft:deepslate_bricks", 30), ("minecraft:cobbled_deepslate", 20),
             ("minecraft:mossy_stone_bricks", 10)]
    for x in range(sx):
        for z in range(sz):
            t.set(x, 0, z, pick(rng, [("minecraft:polished_deepslate", 60), ("minecraft:deepslate_tiles", 40)]))
            edge = x in (0, sx - 1) or z in (0, sz - 1)
            for y in range(1, 7):
                t.set(x, y, z, pick(rng, stone) if edge else AIR)
            t.set(x, 7, z, pick(rng, stone))
            t.set(x, 8, z, pick(rng, [("minecraft:grass_block[snowy=false]", 60), ("minecraft:coarse_dirt", 25), ("minecraft:stone", 15)]))
    # Entrance with a carved runestone lintel.
    t.fill(7, 1, sz - 1, 9, 4, sz - 1, AIR)
    t.fill(6, 5, sz - 1, 10, 5, sz - 1, CARVED)
    # Forges along the back wall, anvils, the great bellows (pistons), chests of the hoard.
    for x in (3, 8, 13):
        t.fill(x - 1, 1, 1, x + 1, 1, 1, "minecraft:blast_furnace[facing=south,lit=true]")
        t.set(x, 2, 1, "minecraft:lava_cauldron")
        t.fill(x - 1, 3, 1, x + 1, 6, 1, "minecraft:bricks")
        t.set(x, 1, 3, "minecraft:anvil[facing=east]")
    t.set(1, 1, 6, "minecraft:piston[extended=false,facing=east]")
    t.set(sx - 2, 1, 6, "minecraft:piston[extended=false,facing=west]")
    t.chest(1, 1, 10, "dwarf_forge", facing="east")
    t.chest(sx - 2, 1, 10, "dwarf_forge", facing="west")
    t.set(1, 1, 11, "minecraft:gold_block")
    t.set(sx - 2, 1, 11, "minecraft:raw_iron_block")
    t.set(1, 1, 12, "minecraft:raw_gold_block")
    t.set(8, 1, 7, "minecraft:smithing_table")
    t.set(6, 1, 7, "minecraft:grindstone[face=floor,facing=north]")
    t.set(10, 1, 7, "minecraft:water_cauldron[level=3]")
    for x in (4, 12):
        t.set(x, 6, 7, LANTERN)
    t.set(8, 6, 11, LANTERN)
    for x, z in ((4.5, 5.5), (12.5, 9.5)):
        t.entity(x, 1.0, z, f"{NS}:norse_merchant", {"Kind": 1})
    return t


# ---------------------------------------------------------------- hall of the valkyries

def valkyrie_hall():
    """Vingolf, a hall of the valkyries: a long hall hung with shields, a stable of winged horses, a training ground
    with straw targets, and the shield-maidens themselves."""
    sx, sz = 31, 25
    t = Template(sx, 12, sz)
    rng = random.Random(77)
    t.fill(0, 1, 0, sx - 1, 11, sz - 1, AIR)
    for x in range(sx):
        for z in range(sz):
            t.set(x, 0, z, pick(rng, EARTH))
    longhouse(t, 4, 2, 21, 11, rng, chest="valkyrie_hall")
    # A gilded high seat at the end of the hall, under a golden shield.
    t.set(6, 1, 7, "minecraft:spruce_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]")
    t.set(5, 2, 7, "minecraft:yellow_wall_banner[facing=east]")
    t.set(5, 1, 6, "minecraft:gold_block")
    t.set(5, 1, 8, "minecraft:gold_block")
    for x, z in ((9.5, 5.5), (14.5, 9.5), (19.5, 5.5), (12.5, 7.5)):
        t.entity(x, 1.0, z, f"{NS}:valkyrie")
    # The stable: a roof on posts, hay and two pegasi, the winged steeds of the valkyries.
    for x in range(5, 15):
        for z in range(16, 22):
            t.set(x, 0, z, pick(rng, [("minecraft:coarse_dirt", 60), ("minecraft:podzol", 40)]))
            if x in (5, 14) or z in (16, 21):
                t.set(x, 1, z, FENCE)
            t.set(x, 4, z, "minecraft:spruce_slab[type=bottom]")
    for x, z in ((5, 16), (14, 16), (5, 21), (14, 21)):
        t.fill(x, 1, z, x, 3, z, "minecraft:spruce_log[axis=y]")
    t.set(9, 1, 16, "minecraft:spruce_fence_gate[facing=north,in_wall=false,open=false,powered=false]")
    t.set(6, 1, 20, "minecraft:hay_block[axis=y]")
    t.set(7, 1, 20, "minecraft:hay_block[axis=x]")
    t.set(13, 1, 17, "minecraft:water_cauldron[level=3]")
    for x, z in ((8.5, 18.5), (11.5, 19.5)):
        t.entity(x, 1.0, z, f"{NS}:pegasus", {"Tame": nbt.Byte(1)})
    # Training ground with straw targets and a weapon rack.
    for x, z in ((19, 17), (22, 19), (25, 17)):
        t.set(x, 1, z, "minecraft:hay_block[axis=y]")
        t.set(x, 2, z, "minecraft:target")
    t.fill(18, 1, 22, 26, 1, 22, FENCE)
    t.set(27, 1, 20, "minecraft:spruce_fence")
    t.set(27, 2, 20, STANDING_LANTERN)
    t.entity(22.5, 1.0, 20.5, f"{NS}:valkyrie")
    standing_stone(t, 28, 3, 3, rng)
    return t


# ---------------------------------------------------------------- Himinbjorg, Heimdall's hall at the end of the Bifrost

RAINBOW = ["red", "orange", "yellow", "lime", "light_blue", "purple"]


def himinbjorg():
    """Himinbjorg, where Heimdall keeps watch: a stone hall with a watchtower on a high terrace, and the rainbow bridge
    Bifrost running down from his gate. Heimdall stands at the head of the bridge; his treasure is by his seat."""
    sx, sy, sz = 21, 22, 34
    t = Template(sx, sy, sz)
    rng = random.Random(1010)
    t.fill(0, 0, 0, sx - 1, sy - 1, sz - 1, AIR)
    # The terrace.
    for x in range(sx):
        for z in range(20):
            for y in range(5):
                t.set(x, y, z, pick(rng, [("minecraft:deepslate_bricks", 70), ("minecraft:cracked_deepslate_bricks", 15),
                                          ("minecraft:deepslate_tiles", 15)]))
            t.set(x, 5, z, "minecraft:smooth_stone")
            if (x in (0, sx - 1) or z in (0, 19)) and not (7 <= x <= 12 and z == 19):
                t.set(x, 6, z, "minecraft:deepslate_brick_wall")
    for x, z in ((0, 0), (sx - 1, 0), (0, 19), (sx - 1, 19)):
        t.set(x, 6, z, "minecraft:gold_block")
        t.set(x, 7, z, STANDING_LANTERN)
    # The hall: stone walls, golden corner pillars, a flat roof with crenels.
    x0, x1, z0, z1, top = 4, 16, 2, 14, 11
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            for y in range(6, top + 1):
                if edge:
                    corner = x in (x0, x1) and z in (z0, z1)
                    t.set(x, y, z, "minecraft:gold_block" if corner else pick(rng, [("minecraft:stone_bricks", 80),
                                                                                   ("minecraft:mossy_stone_bricks", 20)]))
            t.set(x, top + 1, z, "minecraft:deepslate_tiles")
            if edge and (x + z) % 2 == 0:
                t.set(x, top + 2, z, "minecraft:deepslate_tile_wall")
    for z in range(z0 + 2, z1 - 1, 3):                      # windows
        for x in (x0, x1):
            t.set(x, 8, z, "minecraft:yellow_stained_glass_pane")
            t.set(x, 9, z, "minecraft:yellow_stained_glass_pane")
    t.fill(9, 6, z1, 11, 8, z1, AIR)                        # the gate
    # The watchtower rises over the back of the roof, a beacon of gold on top.
    for x in range(8, 13):
        for z in range(z0, z0 + 5):
            for y in range(top + 2, top + 9):
                if x in (8, 12) or z in (z0, z0 + 4):
                    t.set(x, y, z, "minecraft:stone_bricks" if y % 3 else "minecraft:gold_block")
    t.fill(9, top + 9, z0 + 1, 11, top + 9, z0 + 3, "minecraft:deepslate_tiles")
    t.set(10, top + 10, z0 + 2, "minecraft:glowstone")
    # Inside: the watchman's seat, his treasure, the great horn's bell, lanterns.
    t.set(10, 6, 4, "minecraft:quartz_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]")
    t.set(9, 6, 4, "minecraft:gold_block")
    t.set(11, 6, 4, "minecraft:gold_block")
    t.chest(7, 6, 3, "himinbjorg", facing="south")
    t.chest(13, 6, 3, "himinbjorg", facing="south")
    t.set(10, 6, 9, "minecraft:bell[attachment=floor,facing=south,powered=false]")
    for x, z in ((6, 6), (14, 6), (6, 12), (14, 12)):
        t.set(x, 6, z, STANDING_LANTERN)
    for z in range(6, 14):
        t.set(10, 5, z, "minecraft:polished_deepslate")
    # Bifrost: six bands of colour running down from the gate to the ground.
    for z in range(19, sz):
        y = max(0, 5 - (z - 19) * 5 // (sz - 20))
        for i, colour in enumerate(RAINBOW):
            t.set(7 + i, y, z, f"minecraft:{colour}_concrete")
            if y > 0:
                t.set(7 + i, y - 1, z, f"minecraft:{colour}_stained_glass")
    t.entity(10.5, 6.0, 17.5, f"{NS}:heimdall")
    return t


# ---------------------------------------------------------------- rune circle

def rune_circle():
    size = 13
    t = Template(size, 6, size)
    rng = random.Random(99)
    c = size // 2
    t.fill(0, 1, 0, size - 1, 5, size - 1, AIR)
    for x in range(size):
        for z in range(size):
            r = math.hypot(x - c, z - c)
            t.set(x, 0, z, "minecraft:gravel" if r < 2.5 else pick(rng, EARTH))
    for i in range(8):
        a = i * math.pi / 4
        standing_stone(t, int(round(c + math.cos(a) * 5)), int(round(c + math.sin(a) * 5)), 2 + i % 2, rng)
    t.set(c, 0, c, CARVED)
    t.chest(c, 1, c, "rune_circle", facing="south")
    t.set(c + 1, 1, c, CAMPFIRE)
    t.set(c - 1, 1, c, "minecraft:skeleton_skull[rotation=4]")
    for x, z in ((c - 1.5, c + 2.5), (c + 2.5, c - 1.5)):
        t.entity(x, 1.0, z, f"{NS}:raven")
    return t


STRUCTURES = {
    "viking_village": viking_village,
    "longship": lambda: longship(False),
    "naglfar": lambda: longship(True),
    "barrow": barrow,
    "utgard": utgard,
    "fenrir_island": fenrir_island,
    "muspel_fortress": muspel_fortress,
    "helgrind": helgrind,
    "dwarf_forge": dwarf_forge,
    "rune_circle": rune_circle,
    "valkyrie_hall": valkyrie_hall,
    "himinbjorg": himinbjorg,
}
