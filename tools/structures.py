"""Structure templates of Hellas, written as .nbt files. Coordinates: x east, y up, z south, origin at the corner."""
import math
import random

import nbt

DATA_VERSION = 3955  # Minecraft 1.21.1

AIR = "minecraft:air"
MARBLE = "mythsofworlds:marble"
BRICKS = "mythsofworlds:marble_bricks"
PILLAR = "mythsofworlds:marble_pillar[axis=y]"
GOLD = "mythsofworlds:olympian_marble"


def parse_state(state):
    if "[" not in state:
        return {"Name": state}
    name, rest = state[:-1].split("[", 1)
    props = dict(part.split("=") for part in rest.split(","))
    return {"Name": name, "Properties": props}


class Template:
    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.blocks = {}
        self.block_nbt = {}
        self.entities = []

    def inside(self, x, y, z):
        sx, sy, sz = self.size
        return 0 <= x < sx and 0 <= y < sy and 0 <= z < sz

    def set(self, x, y, z, state, tag=None):
        if not self.inside(x, y, z):
            raise ValueError(f"{(x, y, z)} outside {self.size}")
        self.blocks[(x, y, z)] = state
        if tag is not None:
            self.block_nbt[(x, y, z)] = tag
        else:
            self.block_nbt.pop((x, y, z), None)

    def get(self, x, y, z):
        return self.blocks.get((x, y, z))

    def fill(self, x1, y1, z1, x2, y2, z2, state):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                for z in range(min(z1, z2), max(z1, z2) + 1):
                    self.set(x, y, z, state)

    def chest(self, x, y, z, loot, facing="north"):
        self.set(x, y, z, f"minecraft:chest[facing={facing},type=single,waterlogged=false]",
                 {"id": "minecraft:chest", "LootTable": f"mythsofworlds:chests/{loot}"})

    def spawner(self, x, y, z, entity):
        self.set(x, y, z, "minecraft:spawner", {
            "id": "minecraft:mob_spawner",
            "SpawnData": {"entity": {"id": entity}},
            "Delay": nbt.Short(20),
            "MinSpawnDelay": nbt.Short(200),
            "MaxSpawnDelay": nbt.Short(600),
            "SpawnCount": nbt.Short(2),
            "MaxNearbyEntities": nbt.Short(4),
            "RequiredPlayerRange": nbt.Short(12),
            "SpawnRange": nbt.Short(3),
        })

    def entity(self, x, y, z, entity_id, extra=None):
        tag = {"id": entity_id, "PersistenceRequired": nbt.Byte(1)}
        tag.update(extra or {})
        self.entities.append((x, y, z, tag))

    def save(self, path):
        palette = []
        index = {}
        blocks = []
        for pos in sorted(self.blocks, key=lambda p: (p[1], p[2], p[0])):
            state = self.blocks[pos]
            if state not in index:
                index[state] = len(palette)
                palette.append(parse_state(state))
            entry = {"pos": nbt.IntList(pos), "state": index[state]}
            if pos in self.block_nbt:
                entry["nbt"] = self.block_nbt[pos]
            blocks.append(entry)
        entities = [{
            "pos": nbt.DoubleList([x, y, z]),
            "blockPos": nbt.IntList([math.floor(x), math.floor(y), math.floor(z)]),
            "nbt": tag,
        } for x, y, z, tag in self.entities]
        nbt.write(path, {
            "DataVersion": DATA_VERSION,
            "size": nbt.IntList(self.size),
            "palette": palette,
            "blocks": blocks,
            "entities": entities,
        })


def pick(rng, weighted):
    """weighted: list of (state, weight)."""
    total = sum(w for _, w in weighted)
    r = rng.uniform(0, total)
    for state, w in weighted:
        r -= w
        if r <= 0:
            return state
    return weighted[-1][0]


# ---------------------------------------------------------------- temple of the Olympians (Parthenon)

def greek_temple():
    t = Template(13, 15, 21)
    t.fill(0, 1, 0, 12, 14, 20, AIR)
    # Three steps of the stylobate.
    t.fill(0, 0, 0, 12, 0, 20, BRICKS)
    t.fill(1, 1, 1, 11, 1, 19, BRICKS)
    t.fill(2, 2, 2, 10, 2, 18, MARBLE)
    # Peristyle of columns.
    for x in (2, 4, 6, 8, 10):
        for z in (2, 18):
            t.fill(x, 3, z, x, 8, z, PILLAR)
    for z in range(4, 17, 2):
        for x in (2, 10):
            t.fill(x, 3, z, x, 8, z, PILLAR)
    # Entablature, golden frieze and the gabled roof.
    t.fill(2, 9, 2, 10, 9, 18, BRICKS)
    t.fill(2, 10, 2, 10, 10, 18, BRICKS)
    for x in range(2, 11):
        for z in range(2, 19):
            if x in (2, 10) or z in (2, 18):
                t.set(x, 10, z, GOLD)
    for k in range(1, 5):
        t.fill(2 + k, 10 + k, 2, 10 - k, 10 + k, 18, BRICKS)
        for z in range(2, 19):
            t.set(1 + k, 10 + k, z, "minecraft:smooth_quartz_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]")
            t.set(11 - k, 10 + k, z, "minecraft:smooth_quartz_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]")
    # Cella with the statue of Zeus.
    for y in range(3, 9):
        for z in range(6, 16):
            t.set(4, y, z, BRICKS)
            t.set(8, y, z, BRICKS)
        for x in range(4, 9):
            t.set(x, y, 6, BRICKS)
            t.set(x, y, 15, BRICKS)
    t.fill(5, 3, 6, 7, 5, 6, AIR)
    t.fill(5, 3, 7, 7, 8, 14, AIR)
    t.set(6, 3, 13, "minecraft:gold_block")
    t.set(6, 4, 13, "minecraft:quartz_pillar[axis=y]")
    t.set(6, 5, 13, "minecraft:quartz_block")
    t.set(5, 5, 13, "minecraft:quartz_block")
    t.set(7, 5, 13, "minecraft:quartz_block")
    t.set(7, 6, 13, "minecraft:lightning_rod[facing=up,powered=false,waterlogged=false]")
    t.set(6, 6, 13, "minecraft:chiseled_quartz_block")
    t.set(6, 7, 13, "minecraft:gold_block")
    t.chest(5, 3, 14, "greek_temple")
    t.chest(7, 3, 14, "greek_temple")
    for x in (5, 7):
        t.set(x, 3, 8, "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]")
    # Altar with the eternal flame in front of the cella.
    t.set(6, 3, 4, "minecraft:chiseled_quartz_block")
    t.set(6, 4, 4, "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]")
    for x, z in ((3, 3), (9, 3), (3, 17), (9, 17), (3, 10), (9, 10)):
        t.set(x, 8, z, "minecraft:lantern[hanging=true,waterlogged=false]")
    return t


# ---------------------------------------------------------------- oracle of Delphi (tholos)

def oracle_of_delphi():
    t = Template(11, 9, 11)
    c = 5
    for x in range(11):
        for z in range(11):
            r = math.hypot(x - c, z - c)
            if r <= 5.4:
                t.set(x, 0, z, BRICKS)
                for y in range(1, 9):
                    t.set(x, y, z, AIR)
            if r <= 4.5:
                t.set(x, 1, z, MARBLE)
            if r <= 4.6:
                t.set(x, 6, z, BRICKS)
            if r <= 3.2:
                t.set(x, 7, z, BRICKS)
            if r <= 1.5:
                t.set(x, 8, z, GOLD)
    for dx, dz in ((4, 0), (-4, 0), (0, 4), (0, -4), (3, 3), (3, -3), (-3, 3), (-3, -3)):
        t.fill(c + dx, 2, c + dz, c + dx, 5, c + dz, PILLAR)
    # Pythia's tripod, the sacred spring and the oracle's chest.
    t.set(c, 2, c, "minecraft:brewing_stand[has_bottle_0=false,has_bottle_1=false,has_bottle_2=false]")
    t.set(c + 1, 2, c, "minecraft:water_cauldron[level=3]")
    t.set(c, 2, c + 2, "minecraft:campfire[facing=north,lit=true,signal_fire=true,waterlogged=false]")
    t.chest(c - 1, 2, c, "oracle_of_delphi", facing="east")
    t.set(c, 5, c, "minecraft:lantern[hanging=true,waterlogged=false]")
    return t


# ---------------------------------------------------------------- labyrinth of the Minotaur

def labyrinth():
    cells = 8
    size = cells * 4 + 1
    height = 7
    t = Template(size, height, size)
    rng = random.Random(1700)
    # Maze walls: grid lines every 4 blocks, then carve passages with a depth-first search.
    wall = [[x % 4 == 0 or z % 4 == 0 for z in range(size)] for x in range(size)]

    def open_between(a, b):
        (ax, az), (bx, bz) = a, b
        if ax != bx:
            x = 4 * max(ax, bx)
            for z in range(4 * az + 1, 4 * az + 4):
                wall[x][z] = False
        else:
            z = 4 * max(az, bz)
            for x in range(4 * ax + 1, 4 * ax + 4):
                wall[x][z] = False

    start = (3, 0)
    seen = {start}
    stack = [start]
    parent = {start: None}
    while stack:
        cx, cz = stack[-1]
        options = [(cx + dx, cz + dz) for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))
                   if 0 <= cx + dx < cells and 0 <= cz + dz < cells and (cx + dx, cz + dz) not in seen]
        if not options:
            stack.pop()
            continue
        nxt = rng.choice(options)
        open_between((cx, cz), nxt)
        seen.add(nxt)
        parent[nxt] = (cx, cz)
        stack.append(nxt)
    # A few extra openings make loops, so the maze is less of a single corridor.
    for _ in range(6):
        cx, cz = rng.randrange(cells - 1), rng.randrange(cells)
        open_between((cx, cz), (cx + 1, cz))
    # Central arena: cells 3..4 in both directions, all inner walls removed.
    for x in range(13, 20):
        for z in range(13, 20):
            wall[x][z] = False
    # Entrances in the north and south outer walls.
    for x in range(13, 16):
        wall[x][0] = False
    for x in range(17, 20):
        wall[x][size - 1] = False

    wall_mix = [("minecraft:stone_bricks", 60), ("minecraft:mossy_stone_bricks", 20),
                ("minecraft:cracked_stone_bricks", 15), (BRICKS, 5)]
    for x in range(size):
        for z in range(size):
            t.set(x, 0, z, pick(rng, [("minecraft:stone_bricks", 70), ("minecraft:cracked_stone_bricks", 20),
                                       ("minecraft:gravel", 10)]))
            t.set(x, height - 1, z, pick(rng, wall_mix[:3]))
            for y in range(1, height - 1):
                if wall[x][z]:
                    t.set(x, y, z, pick(rng, wall_mix))
                else:
                    t.set(x, y, z, "minecraft:cobweb" if y >= 4 and rng.random() < 0.03 else AIR)
    # Dim lights here and there.
    for cx in range(cells):
        for cz in range(cells):
            if rng.random() < 0.25:
                t.set(4 * cx + 2, height - 2, 4 * cz + 2, "minecraft:lantern[hanging=true,waterlogged=false]")
    # Arena floor, treasure and the Minotaur.
    for x in range(13, 20):
        for z in range(13, 20):
            t.set(x, 0, z, GOLD if abs(x - 16) <= 1 and abs(z - 16) <= 1 else BRICKS)
            for y in range(1, height - 1):
                t.set(x, y, z, AIR)
    for x, z in ((13, 13), (19, 13), (13, 19), (19, 19)):
        t.set(x, 1, z, "minecraft:bone_block[axis=y]")
    t.chest(14, 1, 13, "labyrinth", facing="south")
    t.chest(18, 1, 19, "labyrinth", facing="north")
    t.set(16, 5, 16, "minecraft:lantern[hanging=true,waterlogged=false]")
    t.entity(16.5, 1.0, 16.5, "mythsofworlds:minotaur")
    # Spartoi spawners in two dead ends far from the entrance.
    degree = {}
    for cx in range(cells):
        for cz in range(cells):
            x, z = 4 * cx + 2, 4 * cz + 2
            degree[(cx, cz)] = sum(not wall[x + dx][z + dz] for dx, dz in ((2, 0), (-2, 0), (0, 2), (0, -2)))
    dead_ends = [c for c, d in degree.items() if d == 1 and not (3 <= c[0] <= 4 and 3 <= c[1] <= 4)]
    dead_ends.sort(key=lambda c: -abs(c[1] - 0) - abs(c[0] - 3))
    for cx, cz in dead_ends[:2]:
        t.spawner(4 * cx + 2, 1, 4 * cz + 2, "mythsofworlds:spartoi")
    return t


# ---------------------------------------------------------------- gates of Hades

def gates_of_hades():
    t = Template(21, 16, 21)
    rng = random.Random(666)
    t.fill(0, 1, 0, 20, 15, 20, AIR)
    for x in range(21):
        for z in range(21):
            edge = x in (0, 20) or z in (0, 20)
            t.set(x, 0, z, "minecraft:soul_soil" if edge else pick(rng, [
                ("minecraft:polished_blackstone_bricks", 70), ("minecraft:cracked_polished_blackstone_bricks", 25),
                ("minecraft:gilded_blackstone", 5)]))
    # Path to the gate.
    t.fill(9, 0, 1, 11, 0, 12, "minecraft:polished_blackstone")
    # Two massive pillars and the lintel.
    for x0 in (3, 15):
        t.fill(x0, 1, 13, x0 + 2, 11, 15, "minecraft:polished_basalt[axis=y]")
        t.fill(x0, 1, 13, x0 + 2, 1, 15, "minecraft:chiseled_polished_blackstone")
        t.set(x0 + 1, 6, 12, "minecraft:soul_lantern[hanging=false,waterlogged=false]")
    t.fill(3, 12, 13, 17, 13, 15, "minecraft:polished_blackstone_bricks")
    t.fill(4, 14, 14, 16, 14, 14, "minecraft:chiseled_polished_blackstone")
    for x in (4, 8, 12, 16):
        t.set(x, 14, 14, "minecraft:gilded_blackstone")
    # The sealed door of the underworld.
    for x in range(6, 15):
        for y in range(1, 12):
            t.set(x, y, 15, "minecraft:crying_obsidian" if rng.random() < 0.2 else "minecraft:obsidian")
    # Braziers of soul fire.
    for x, z in ((2, 4), (18, 4), (2, 10), (18, 10)):
        t.set(x, 1, z, "minecraft:soul_soil")
        t.set(x, 2, z, "minecraft:soul_fire")
    for _ in range(10):
        x, z = rng.randrange(1, 20), rng.randrange(1, 12)
        if not 8 <= x <= 12 and t.get(x, 1, z) == AIR:
            t.set(x, 1, z, rng.choice(["minecraft:bone_block[axis=y]", "minecraft:skeleton_skull[rotation=%d]" % rng.randrange(16)]))
    t.chest(10, 1, 14, "gates_of_hades", facing="north")
    t.entity(10.5, 1.0, 9.5, "mythsofworlds:cerberus")
    return t


# ---------------------------------------------------------------- lair of the Hydra

def hydra_lair():
    t = Template(23, 8, 23)
    rng = random.Random(9)
    c = 11
    for x in range(23):
        for z in range(23):
            r = math.hypot(x - c, z - c)
            if r > 11.4:
                continue
            t.set(x, 0, z, "minecraft:mud")
            if r <= 6.5 and r > 3.2:
                t.set(x, 1, z, "minecraft:water[level=0]")
                t.set(x, 2, z, "minecraft:water[level=0]")
                if rng.random() < 0.12:
                    t.set(x, 3, z, "minecraft:lily_pad")
            else:
                t.set(x, 1, z, "minecraft:mud")
                t.set(x, 2, z, "minecraft:moss_block")
            for y in range(3, 8):
                if t.get(x, y, z) is None:
                    t.set(x, y, z, AIR)
            # Broken ring wall.
            if 9.0 <= r <= 10.4:
                h = rng.randrange(0, 5)
                for y in range(3, 3 + h):
                    t.set(x, y, z, pick(rng, [("minecraft:mossy_stone_bricks", 60), ("minecraft:mossy_cobblestone", 30),
                                              ("minecraft:cracked_stone_bricks", 10)]))
            elif r > 6.5 and rng.random() < 0.05:
                t.set(x, 3, z, "minecraft:moss_carpet")
    # Fallen columns around the pool.
    for i in range(6):
        a = i * math.pi / 3
        x, z = round(c + 8 * math.cos(a)), round(c + 8 * math.sin(a))
        for y in range(3, 3 + rng.randrange(2, 6)):
            t.set(x, y, z, "mythsofworlds:marble_pillar[axis=y]" if rng.random() < 0.6 else "minecraft:mossy_cobblestone")
    t.chest(c, 3, c, "hydra_lair", facing="south")
    t.set(c - 1, 3, c, "minecraft:bone_block[axis=y]")
    t.entity(c + 0.5, 3.0, c + 2.5, "mythsofworlds:hydra")
    return t


# ---------------------------------------------------------------- lair of Medusa (ruined temple)

def medusa_lair():
    t = Template(15, 10, 15)
    rng = random.Random(42)
    t.fill(0, 1, 0, 14, 9, 14, AIR)
    for x in range(15):
        for z in range(15):
            t.set(x, 0, z, pick(rng, [(BRICKS, 60), (MARBLE, 25), ("minecraft:mossy_cobblestone", 15)]))
    for i in range(1, 14, 2):
        for x, z in ((i, 1), (i, 13), (1, i), (13, i)):
            for y in range(1, 1 + rng.randrange(3, 8)):
                t.set(x, y, z, PILLAR)
    for x in range(1, 14):
        for z in range(1, 14):
            if rng.random() < 0.45:
                t.set(x, 8, z, rng.choice([BRICKS, MARBLE]))
            elif 2 <= x <= 12 and 2 <= z <= 12 and rng.random() < 0.05:
                t.set(x, 1, z, "minecraft:cobweb")
    # Heroes turned to stone.
    for x, z in ((4, 4), (10, 4), (3, 9), (11, 10), (7, 11)):
        t.set(x, 1, z, "minecraft:andesite_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]")
        t.set(x, 2, z, "minecraft:polished_andesite")
        t.set(x, 3, z, "minecraft:stone")
    t.set(7, 1, 7, "minecraft:chiseled_stone_bricks")
    t.set(7, 2, 7, "minecraft:soul_lantern[hanging=false,waterlogged=false]")
    t.chest(7, 1, 9, "medusa_lair", facing="north")
    t.entity(7.5, 1.0, 5.5, "mythsofworlds:medusa")
    return t


# ---------------------------------------------------------------- dome caves

def dome(t, cx, cz, inner, outer, rng, shell, floor):
    sx, sy, sz = t.size
    for x in range(sx):
        for z in range(sz):
            for y in range(sy):
                r = math.sqrt((x - cx) ** 2 + y ** 2 + (z - cz) ** 2)
                if y == 0 and math.hypot(x - cx, z - cz) <= outer:
                    t.set(x, 0, z, pick(rng, floor))
                elif y > 0 and r <= inner:
                    t.set(x, y, z, AIR)
                elif y > 0 and r <= outer:
                    t.set(x, y, z, pick(rng, shell))


def cyclops_cave():
    t = Template(19, 10, 19)
    rng = random.Random(1)
    dome(t, 9, 9, 7.0, 9.0, rng,
         [("minecraft:stone", 50), ("minecraft:cobblestone", 25), ("minecraft:andesite", 15), ("minecraft:mossy_cobblestone", 10)],
         [("minecraft:coarse_dirt", 60), ("minecraft:gravel", 25), ("minecraft:dirt", 15)])
    t.fill(8, 1, 13, 10, 3, 18, AIR)
    # Polyphemus' sheep pen.
    for x in range(2, 7):
        for z in range(3, 8):
            if x in (2, 6) or z in (3, 7):
                t.set(x, 1, z, "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]")
    t.set(4, 1, 7, "minecraft:oak_fence_gate[facing=south,in_wall=false,open=false,powered=false]")
    for x, z in ((3.5, 4.5), (5.5, 4.5), (4.5, 6.0)):
        t.entity(x, 1.0, z, "minecraft:sheep")
    # The giant's bed of hay, his hearth and his hoard.
    t.fill(12, 1, 3, 14, 1, 5, "minecraft:hay_block[axis=y]")
    t.set(9, 1, 9, "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]")
    t.chest(14, 1, 8, "cyclops_cave", facing="west")
    t.set(13, 1, 10, "minecraft:bone_block[axis=y]")
    t.entity(9.5, 1.0, 5.5, "mythsofworlds:cyclops")
    return t


def nemean_lion_den():
    t = Template(13, 7, 13)
    rng = random.Random(7)
    dome(t, 6, 6, 4.6, 6.0, rng,
         [("minecraft:stone", 40), ("minecraft:mossy_cobblestone", 30), ("minecraft:granite", 30)],
         [("minecraft:coarse_dirt", 50), ("minecraft:podzol", 30), ("minecraft:gravel", 20)])
    t.fill(5, 1, 0, 7, 2, 3, AIR)
    for x, z in ((3, 7), (8, 4), (9, 8)):
        t.set(x, 1, z, "minecraft:bone_block[axis=y]")
    t.set(4, 1, 4, "minecraft:skeleton_skull[rotation=3]")
    t.chest(7, 1, 9, "nemean_lion_den", facing="north")
    t.entity(6.5, 1.0, 6.5, "mythsofworlds:nemean_lion")
    return t


STRUCTURES = {
    "greek_temple": greek_temple,
    "oracle_of_delphi": oracle_of_delphi,
    "labyrinth": labyrinth,
    "gates_of_hades": gates_of_hades,
    "hydra_lair": hydra_lair,
    "medusa_lair": medusa_lair,
    "cyclops_cave": cyclops_cave,
    "nemean_lion_den": nemean_lion_den,
}
