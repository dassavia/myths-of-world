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

    # Blocks that fences, walls, panes and bars do not join onto (they have no full side to lean on).
    NOT_SOLID = ("air", "slab", "stairs", "carpet", "torch", "lantern", "flower", "short_grass", "tall_grass", "fern", "bed", "door",
                 "trapdoor", "sign", "banner", "button", "pressure_plate", "chain", "water", "lava", "campfire", "fire",
                 "skull", "head", "pot", "candle", "rail", "vine", "sapling", "bush", "roots", "snow[", "ladder",
                 "chest", "barrel", "anvil", "cauldron", "hay_block", "target", "bell", "path", "farmland")

    @staticmethod
    def _family(name):
        if name.endswith("_fence") or name.endswith("_fence_gate"):
            return "fence"
        if name.endswith("_wall") and not name.endswith("_banner"):
            return "wall"
        if name.endswith("_pane") or name == "minecraft:iron_bars":
            return "pane"
        return None

    def connect(self):
        """Joins fences, walls, panes and iron bars to their neighbours, as the game would when placing them by hand.
        Structure blocks are placed as saved, so unjoined states would leave lone posts."""
        sides = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}
        for pos, state in list(self.blocks.items()):
            name = state.split("[")[0]
            family = self._family(name)
            if family is None or name.endswith("_fence_gate"):
                continue
            props = parse_state(state).get("Properties", {})
            x, y, z = pos
            for side, (dx, dz) in sides.items():
                other = self.blocks.get((x + dx, y, z + dz))
                other_name = other.split("[")[0] if other else "minecraft:air"
                joins = self._family(other_name) == family or (
                    family == "pane" and self._family(other_name) == "wall") or (
                    family == "wall" and self._family(other_name) == "pane") or (
                    other is not None and self._family(other_name) is None
                    and not any(word in other_name for word in self.NOT_SOLID))
                if family == "wall":
                    props[side] = "low" if joins else "none"
                else:
                    props[side] = "true" if joins else "false"
            props.setdefault("waterlogged", "false")
            if family == "wall":
                ns = props["north"] != "none" and props["south"] != "none"
                ew = props["east"] != "none" and props["west"] != "none"
                one_line = (ns and props["east"] == props["west"] == "none") or (ew and props["north"] == props["south"] == "none")
                props["up"] = "false" if one_line and self.blocks.get((x, y + 1, z), AIR) == AIR else "true"
            self.blocks[pos] = name + "[" + ",".join(f"{k}={v}" for k, v in sorted(props.items())) + "]"

    def save(self, path):
        self.connect()
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

LAB = "mythsofworlds:labyrinth_bricks"
LAB_MOSSY = "mythsofworlds:mossy_labyrinth_bricks"
LAB_CRACKED = "mythsofworlds:cracked_labyrinth_bricks"


def labyrinth():
    """The labyrinth of Daedalus, deep under the ground. On the surface only its entrance stands, a red-columned
    Minoan propylon over a spiral stair; the maze below is built of bricks that nothing can break, so the only way to
    the Minotaur is through the passages. The entrance sits in the middle of the maze, the arena in a far corner."""
    cells = 15
    size = cells * 4 + 1
    maze_h = 7                # floor, five blocks of passage, ceiling
    ground = 21               # y of the entrance floor, which replaces the surface block
    height = ground + 10
    t = Template(size, height, size)
    rng = random.Random(1700)
    mid = cells // 2
    arena = range(cells - 4, cells - 1)  # 3x3 cells in the south-east corner, one cell in from the outer wall
    lo, hi = 4 * arena[0] + 1, 4 * (arena[-1] + 1) - 1
    c = (lo + hi) // 2
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

    # Depth-first maze grown from the entrance cell in the middle.
    start = (mid, mid)
    seen = {start}
    stack = [start]
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
        stack.append(nxt)
    # A few extra openings make loops, so the maze is less of a single corridor.
    for _ in range(18):
        cx, cz = rng.randrange(cells - 1), rng.randrange(cells)
        open_between((cx, cz), (cx + 1, cz))
    for x in range(lo, hi + 1):
        for z in range(lo, hi + 1):
            wall[x][z] = False

    wall_mix = [(LAB, 60), (LAB_MOSSY, 22), (LAB_CRACKED, 18)]
    for x in range(size):
        for z in range(size):
            t.set(x, 0, z, pick(rng, wall_mix))
            t.set(x, maze_h - 1, z, pick(rng, wall_mix))
            for y in range(1, maze_h - 1):
                if wall[x][z]:
                    t.set(x, y, z, pick(rng, wall_mix))
                else:
                    t.set(x, y, z, "minecraft:cobweb" if y >= 4 and rng.random() < 0.03 else AIR)
    # Dim lights here and there; most of the maze stays dark.
    for cx in range(cells):
        for cz in range(cells):
            if rng.random() < 0.15 and (cx, cz) != start:
                t.set(4 * cx + 2, maze_h - 2, 4 * cz + 2, "minecraft:lantern[hanging=true,waterlogged=false]")

    # Arena of the Minotaur: a golden floor ring, pillars, bones, treasure.
    for x in range(lo, hi + 1):
        for z in range(lo, hi + 1):
            ring = max(abs(x - c), abs(z - c))
            t.set(x, 0, z, GOLD if ring in (0, 3) else LAB)
            for y in range(1, maze_h - 1):
                t.set(x, y, z, AIR)
    for dx, dz in ((-4, -4), (4, -4), (-4, 4), (4, 4)):
        t.fill(c + dx, 1, c + dz, c + dx, maze_h - 2, c + dz, PILLAR)
    for _ in range(10):
        x, z = rng.randint(lo, hi), rng.randint(lo, hi)
        if max(abs(x - c), abs(z - c)) > 1 and t.get(x, 1, z) == AIR:
            t.set(x, 1, z, rng.choice(["minecraft:bone_block[axis=y]", "minecraft:skeleton_skull[rotation=%d]" % rng.randrange(16)]))
    t.chest(c - 2, 1, lo, "labyrinth", facing="south")
    t.chest(c + 2, 1, hi, "labyrinth", facing="north")
    for dx, dz in ((-2, -2), (2, 2)):
        t.set(c + dx, maze_h - 2, c + dz, "minecraft:lantern[hanging=true,waterlogged=false]")
    t.entity(c + 0.5, 1.0, c + 0.5, "mythsofworlds:minotaur")
    # Spartoi guard four far dead ends; four others hide treasure.
    degree = {}
    for cx in range(cells):
        for cz in range(cells):
            x, z = 4 * cx + 2, 4 * cz + 2
            degree[(cx, cz)] = sum(not wall[x + dx][z + dz] for dx, dz in ((2, 0), (-2, 0), (0, 2), (0, -2)))
    dead_ends = [cell for cell, d in degree.items()
                 if d == 1 and cell != start and not (cell[0] in arena and cell[1] in arena)]
    rng.shuffle(dead_ends)
    for cx, cz in dead_ends[:4]:
        t.spawner(4 * cx + 2, 1, 4 * cz + 2, "mythsofworlds:spartoi")
    for cx, cz in dead_ends[4:8]:
        t.chest(4 * cx + 2, 1, 4 * cz + 2, "labyrinth")

    # Spiral stair from the propylon down into the entrance cell, walled with the same unbreakable bricks.
    s0 = 4 * mid          # shaft walls on the cell's grid lines, 3x3 well inside
    axis = s0 + 2
    for y in range(maze_h - 1, ground):
        for x in range(s0, s0 + 5):
            for z in range(s0, s0 + 5):
                if x in (s0, s0 + 4) or z in (s0, s0 + 4):
                    t.set(x, y, z, pick(rng, wall_mix))
                else:
                    t.set(x, y, z, AIR)
    for y in range(1, ground + 1):
        t.set(axis, y, axis, PILLAR)
    ring = [(axis - 1, axis - 1), (axis, axis - 1), (axis + 1, axis - 1), (axis + 1, axis),
            (axis + 1, axis + 1), (axis, axis + 1), (axis - 1, axis + 1), (axis - 1, axis)]
    for step, y in enumerate(range(ground - 1, 0, -1)):
        x, z = ring[step % 8]
        t.set(x, y, z, LAB)
    for y, (x, z, facing) in ((ground - 3, (axis, axis - 1, "north")), (ground - 9, (axis + 1, axis, "east")),
                              (ground - 15, (axis, axis + 1, "south"))):
        if t.get(x, y, z) == AIR:
            t.set(x, y, z, f"minecraft:wall_torch[facing={facing}]")

    # The propylon on the surface: Minoan columns, red with black capitals, and the horns of consecration.
    p0, p1 = s0 - 2, s0 + 6
    for x in range(p0 - 1, p1 + 2):
        for z in range(p0 - 1, p1 + 2):
            for y in range(ground + 1, height):
                t.set(x, y, z, AIR)
            if p0 <= x <= p1 and p0 <= z <= p1:
                if s0 < x < s0 + 4 and s0 < z < s0 + 4:
                    t.set(x, ground, z, AIR)
                else:
                    t.set(x, ground, z, GOLD if x in (p0, p1) or z in (p0, p1) else BRICKS)
            else:
                t.set(x, ground, z, BRICKS)
    t.set(axis, ground, axis, GOLD)
    for x in (p0, p0 + 4, p1):
        for z in (p0, p0 + 4, p1):
            if (x, z) == (p0 + 4, p0 + 4):
                continue
            t.fill(x, ground + 1, z, x, ground + 4, z, "minecraft:red_terracotta")
            t.set(x, ground + 5, z, "minecraft:black_terracotta")
    t.fill(p0, ground + 6, p0, p1, ground + 6, p1, BRICKS)
    t.fill(p0 + 1, ground + 7, p0 + 1, p1 - 1, ground + 7, p1 - 1, MARBLE)
    for x in range(p0, p1 + 1):
        for z in (p0, p1):
            if x % 2 == 0:
                t.set(x, ground + 6, z, GOLD)
    for x in (axis - 2, axis + 2):
        t.set(x, ground + 8, axis, "minecraft:quartz_block")
        t.set(x, ground + 9, axis, "minecraft:quartz_block")
    t.fill(axis - 1, ground + 8, axis, axis + 1, ground + 8, axis, "minecraft:quartz_block")
    for x, z in ((p0 + 2, p0 + 2), (p1 - 2, p1 - 2)):
        t.set(x, ground + 1, z, "minecraft:decorated_pot[cracked=false,facing=north,waterlogged=false]")
    t.set(p0 + 2, ground + 1, p1 - 2, "minecraft:skeleton_skull[rotation=6]")
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
    # Karkinos, Hera's crab, waits on the bank to pinch the hero's heel.
    t.entity(c - 7.5, 3.0, c + 0.5, "mythsofworlds:karkinos")
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


# ---------------------------------------------------------------- agora (village of merchants)

def stall(t, cx, cz, kind, facing, rng, stripes):
    """5x5 market stall centred on (cx, cz): striped awning, counter on the side facing the square, a merchant."""
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            t.set(x, 0, z, "minecraft:smooth_stone")
    for dx, dz in ((-2, -2), (2, -2), (-2, 2), (2, 2)):
        t.fill(cx + dx, 1, cz + dz, cx + dx, 3, cz + dz, "minecraft:stripped_oak_log[axis=y]")
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            stripe = (x - cx) if facing in ("north", "south") else (z - cz)
            t.set(x, 4, z, stripes[stripe % 2])
    # Counter on the side the stall faces.
    dx, dz = {"north": (0, -1), "south": (0, 1), "west": (-1, 0), "east": (1, 0)}[facing]
    goods = {0: "minecraft:barrel[facing=up,open=false]", 1: "minecraft:smithing_table",
             2: "minecraft:brewing_stand[has_bottle_0=false,has_bottle_1=false,has_bottle_2=false]"}
    for i in (-1, 0, 1):
        x = cx + dx * 2 + (i if dz else 0)
        z = cz + dz * 2 + (i if dx else 0)
        t.set(x, 1, z, goods[kind] if i == 0 else "minecraft:spruce_slab[type=top,waterlogged=false]")
    t.set(cx - dx, 1, cz - dz, "minecraft:decorated_pot[cracked=false,facing=north,waterlogged=false]")
    t.entity(cx + 0.5, 1.0, cz + 0.5, "mythsofworlds:greek_merchant", {"Kind": kind})


def house(t, x0, z0, door, rng):
    """7x7 whitewashed house with a terracotta roof, a door on side `door` and a chest inside."""
    walls = [("minecraft:white_terracotta", 50), (BRICKS, 40), ("minecraft:calcite", 10)]
    for x in range(x0, x0 + 7):
        for z in range(z0, z0 + 7):
            t.set(x, 0, z, "minecraft:spruce_planks" if 0 < x - x0 < 6 and 0 < z - z0 < 6 else BRICKS)
            edge = x in (x0, x0 + 6) or z in (z0, z0 + 6)
            for y in range(1, 5):
                t.set(x, y, z, pick(rng, walls) if edge else AIR)
            t.set(x, 5, z, "minecraft:terracotta" if edge else "minecraft:orange_terracotta")
    for x, z in ((x0, z0), (x0 + 6, z0), (x0, z0 + 6), (x0 + 6, z0 + 6)):
        t.fill(x, 1, z, x, 4, z, PILLAR)
    mx, mz = x0 + 3, z0 + 3
    dx, dz = {"north": (0, -3), "south": (0, 3), "west": (-3, 0), "east": (3, 0)}[door]
    t.set(mx + dx, 1, mz + dz, AIR)
    t.set(mx + dx, 2, mz + dz, AIR)
    # Windows on the other sides.
    for wx, wz in ((0, -3), (0, 3), (-3, 0), (3, 0)):
        if (wx, wz) != (dx, dz):
            t.set(mx + wx, 2, mz + wz, "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]")
    t.chest(mx - dx // 3 * 2, 1, mz - dz // 3 * 2, "agora_house", facing=door)
    t.set(x0 + 1, 1, z0 + 1, "minecraft:crafting_table")
    t.set(x0 + 5, 1, z0 + 5, "minecraft:decorated_pot[cracked=false,facing=north,waterlogged=false]")
    t.set(x0 + 5, 1, z0 + 1, "minecraft:hay_block[axis=y]")
    t.set(mx, 4, mz, "minecraft:lantern[hanging=true,waterlogged=false]")


def olive_tree(t, x, z, rng):
    h = rng.randint(3, 4)
    t.fill(x, 1, z, x, h, z, "minecraft:oak_log[axis=y]")
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            for y in (h, h + 1):
                if abs(dx) + abs(dz) <= (3 if y == h else 2) and (dx, dz, y) != (0, 0, h) and rng.random() < 0.85:
                    if t.inside(x + dx, y, z + dz):
                        age = 3 if rng.random() < 0.3 else 0
                        t.set(x + dx, y, z + dz, f"mythsofworlds:olive_leaves[age={age},distance=1,persistent=true,waterlogged=false]")


def agora():
    size = 45
    t = Template(size, 12, size)
    rng = random.Random(3)
    c = size // 2
    t.fill(0, 1, 0, size - 1, 11, size - 1, AIR)
    # Paved square with marble roads leading out in four directions.
    for x in range(size):
        for z in range(size):
            road = abs(x - c) <= 1 or abs(z - c) <= 1
            r = math.hypot(x - c, z - c)
            if road or r <= 12:
                t.set(x, 0, z, pick(rng, [(BRICKS, 55), (MARBLE, 30), ("minecraft:smooth_stone", 15)]))
            else:
                t.set(x, 0, z, pick(rng, [("minecraft:grass_block[snowy=false]", 80), ("minecraft:coarse_dirt", 20)]))
    # Fountain in the middle, with the iron guardian (a gift of Hephaestus).
    for x in range(c - 3, c + 4):
        for z in range(c - 3, c + 4):
            r = math.hypot(x - c, z - c)
            if r <= 3.5:
                t.set(x, 0, z, BRICKS)
                t.set(x, 1, z, GOLD if r > 2.5 else "minecraft:water[level=0]")
    t.fill(c, 1, c, c, 3, c, PILLAR)
    t.set(c, 4, c, "minecraft:gold_block")
    t.set(c, 5, c, "minecraft:lantern[hanging=false,waterlogged=false]")
    t.entity(c + 5.5, 1.0, c + 5.5, "minecraft:iron_golem", {"PlayerCreated": nbt.Byte(0)})
    # Four stalls facing the fountain: two trophy dealers, the smith of Hephaestus and the priestess.
    stripes = [("minecraft:red_wool", "minecraft:white_wool"), ("minecraft:blue_wool", "minecraft:white_wool"),
               ("minecraft:yellow_wool", "minecraft:white_wool"), ("minecraft:cyan_wool", "minecraft:white_wool")]
    for (sx, sz, facing), kind, stripe in zip(((c, c - 9, "south"), (c + 9, c, "west"), (c, c + 9, "north"), (c - 9, c, "east")),
                                              (0, 1, 0, 2), stripes):
        stall(t, sx, sz, kind, facing, rng, stripe)
    # Houses in the corners of the square, doors towards the roads.
    for x0, z0, door in ((4, 4, "east"), (34, 4, "south"), (4, 34, "north"), (34, 34, "west")):
        house(t, x0, z0, door, rng)
    # Temple of Hermes, patron of merchants, on the north road.
    for x in range(c - 4, c + 5):
        for z in range(0, 7):
            t.set(x, 0, z, BRICKS)
            t.set(x, 1, z, MARBLE)
    for x in (c - 4, c - 2, c + 2, c + 4):
        for z in (0, 6):
            t.fill(x, 2, z, x, 5, z, PILLAR)
    for z in (2, 4):
        for x in (c - 4, c + 4):
            t.fill(x, 2, z, x, 5, z, PILLAR)
    t.fill(c - 4, 6, 0, c + 4, 6, 6, BRICKS)
    for x in range(c - 4, c + 5):
        t.set(x, 6, 0, GOLD)
        t.set(x, 6, 6, GOLD)
    t.fill(c - 3, 7, 1, c + 3, 7, 5, "minecraft:smooth_quartz_slab[type=bottom,waterlogged=false]")
    t.set(c, 2, 2, "minecraft:chiseled_quartz_block")
    t.set(c, 3, 2, "minecraft:gold_block")
    t.set(c, 4, 2, "minecraft:lightning_rod[facing=up,powered=false,waterlogged=false]")
    t.chest(c - 1, 2, 2, "agora_temple", facing="south")
    t.set(c + 1, 2, 2, "mythsofworlds:brazier[lit=true]")
    # Olive trees, lamps and amphorae around the square.
    for x, z in ((14, 14), (30, 14), (14, 30), (30, 30), (2, 16), (42, 28), (16, 42), (28, 42)):
        olive_tree(t, x, z, rng)
    for x, z in ((c - 2, 10), (c + 2, 34), (10, c + 2), (34, c - 2)):
        t.fill(x, 1, z, x, 2, z, "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]")
        t.set(x, 3, z, "minecraft:lantern[hanging=false,waterlogged=false]")
    for _ in range(10):
        x, z = rng.randrange(8, 37), rng.randrange(8, 37)
        if t.get(x, 1, z) == AIR and t.get(x, 0, z) not in (None, "minecraft:water[level=0]") and 5 < math.hypot(x - c, z - c):
            t.set(x, 1, z, "minecraft:decorated_pot[cracked=false,facing=north,waterlogged=false]")
    return t


# ---------------------------------------------------------------- ship of Theseus

def ship_of_theseus():
    width, height, length = 11, 18, 27
    t = Template(width, height, length)
    rng = random.Random(1234)
    c = width // 2
    hull = [("minecraft:dark_oak_planks", 70), ("minecraft:spruce_planks", 30)]

    def half_width(z, y):
        # Narrow keel, widest at the deck; bow (high z) and stern taper.
        w = min(4, 1 + y)
        if z < 3:
            w = min(w, 1 + z + y // 2)
        if z > length - 6:
            w = min(w, max(0, (length - 1 - z)) + y // 3)
        return w

    for z in range(length):
        for y in range(0, 6):
            w = half_width(z, y)
            for x in range(width):
                d = abs(x - c)
                if d > w:
                    continue
                inner = d < w and y > 0 and 0 < z < length - 1 and half_width(z - 1, y) >= d + 1 and half_width(z + 1, y) >= d + 1
                if y == 5:
                    t.set(x, y, z, "minecraft:spruce_planks" if d < w else pick(rng, hull))
                elif inner:
                    t.set(x, y, z, AIR)
                else:
                    t.set(x, y, z, pick(rng, hull))
    # Rails and the curved bow post.
    for z in range(length):
        w = half_width(z, 5)
        for x in (c - w, c + w):
            if t.get(x, 5, z) is not None:
                t.set(x, 6, z, "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]")
    for y, z in ((6, length - 2), (7, length - 1), (8, length - 1)):
        t.set(c, y, z, "minecraft:dark_oak_log[axis=y]")
    t.set(c, 9, length - 1, "minecraft:gold_block")
    # Oars along both sides.
    for z in range(7, 20, 3):
        for x, side in ((0, "east"), (width - 1, "west")):
            t.set(x, 4, z, "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]")
    # Mast and the black sail Theseus forgot to change.
    mz = 14
    t.fill(c, 6, mz, c, height - 1, mz, "minecraft:spruce_log[axis=y]")
    t.fill(1, height - 2, mz, width - 2, height - 2, mz, "minecraft:spruce_log[axis=x]")
    t.fill(1, 9, mz + 1, width - 2, height - 3, mz + 1, "minecraft:black_wool")
    # Stern cabin with the captain's chest; a hatch leads to the hold.
    t.fill(2, 6, 1, width - 3, 8, 5, "minecraft:dark_oak_planks")
    t.fill(3, 6, 2, width - 4, 7, 4, AIR)
    t.fill(c, 6, 5, c, 7, 5, AIR)
    t.fill(2, 9, 1, width - 3, 9, 5, "minecraft:dark_oak_slab[type=bottom,waterlogged=false]")
    t.chest(c, 6, 2, "ship_of_theseus", facing="south")
    t.set(3, 6, 2, "minecraft:lantern[hanging=false,waterlogged=false]")
    t.set(c, 5, 9, "minecraft:spruce_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]")
    t.chest(c, 1, 9, "ship_of_theseus", facing="south")
    t.set(c + 1, 1, 10, "minecraft:barrel[facing=up,open=false]")
    t.set(c - 1, 1, 10, "minecraft:barrel[facing=up,open=false]")
    # The ghost crew.
    for x, z in ((c - 2, 10), (c + 2, 17), (c, 21)):
        t.entity(x + 0.5, 6.0, z + 0.5, "mythsofworlds:shade")
    return t


# ---------------------------------------------------------------- refuge of Perseus

def perseus_refuge():
    t = Template(11, 8, 11)
    rng = random.Random(5)
    dome(t, 5, 5, 4.0, 5.4, rng,
         [("minecraft:stone", 40), ("minecraft:mossy_cobblestone", 25), (MARBLE, 20), ("minecraft:andesite", 15)],
         [(BRICKS, 60), (MARBLE, 40)])
    t.fill(4, 1, 0, 6, 2, 2, AIR)
    t.set(5, 3, 1, "minecraft:vine[east=false,north=true,south=false,up=false,west=false]")
    # The hero's bedroll, his polished shield on the wall and the chest with the harpe.
    t.set(3, 1, 6, "minecraft:white_carpet")
    t.set(3, 1, 7, "minecraft:white_carpet")
    t.set(5, 1, 8, "minecraft:chiseled_quartz_block")
    t.set(5, 2, 8, "minecraft:light_weighted_pressure_plate[power=0]")
    t.chest(7, 1, 7, "perseus_refuge", facing="west")
    t.set(7, 1, 4, "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]")
    t.set(5, 4, 5, "minecraft:lantern[hanging=true,waterlogged=false]")
    # Pegasus, born from Medusa's blood, waits by the hero.
    t.entity(5.5, 1.0, 3.5, "mythsofworlds:pegasus")
    return t


# ---------------------------------------------------------------- amazons

FENCE = "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]"


def tent(t, cx, cz, colour, rng, facing="south"):
    """Small wool tent, 5 wide and 5 deep, open on the `facing` side, with a bed roll."""
    for dz in range(-2, 3):
        for dx in range(-2, 3):
            h = 3 - abs(dx)
            for y in range(1, h + 1):
                inner = abs(dx) < 2 and y < h
                t.set(cx + dx, y, cz + dz, AIR if inner else (colour if (dx + dz) % 2 else "minecraft:white_wool"))
    # Open the front.
    fz = cz + (2 if facing == "south" else -2)
    for dx in (-1, 0, 1):
        for y in (1, 2):
            t.set(cx + dx, y, fz, AIR)
    t.set(cx, 1, cz - (1 if facing == "south" else -1), "minecraft:white_carpet")
    t.set(cx - 1, 1, cz, "minecraft:hay_block[axis=x]")


def amazon_camp():
    """War camp of the amazons on the plain: a palisade, tents, a fire, targets and a horse pen."""
    size = 27
    t = Template(size, 8, size)
    rng = random.Random(1906)
    c = size // 2
    t.fill(0, 1, 0, size - 1, 7, size - 1, AIR)
    for x in range(size):
        for z in range(size):
            r = math.hypot(x - c, z - c)
            if r <= 12.5:
                t.set(x, 0, z, pick(rng, [("minecraft:grass_block[snowy=false]", 60), ("minecraft:coarse_dirt", 25),
                                          ("minecraft:dirt_path", 15)]))
            if 11.5 < r <= 12.5:
                top = 3 + rng.randrange(2)
                for y in range(1, top + 1):
                    t.set(x, y, z, "minecraft:stripped_spruce_log[axis=y]")
    # Gate to the south.
    for x in range(c - 1, c + 2):
        for y in range(1, 6):
            t.set(x, y, size - 2, AIR)
            t.set(x, y, size - 1, AIR)
    for x, z in ((c - 2, size - 2), (c + 2, size - 2)):
        t.set(x, 5, z, "minecraft:lantern[hanging=false,waterlogged=false]")
    # Fire in the middle, ringed with stones.
    t.set(c, 0, c, "minecraft:cobblestone")
    t.set(c, 1, c, "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]")
    for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1), (0, -2), (0, 2), (-2, 0), (2, 0)):
        t.set(c + dx, 1, c + dz, "minecraft:cobblestone_slab[type=bottom,waterlogged=false]")
    # Tents well inside the palisade (each is 5 x 5 around its centre).
    for (cx, cz), colour in zip(((7, 8), (c, 6), (19, 8), (6, 13)), ("minecraft:red_wool", "minecraft:brown_wool",
                                                                       "minecraft:red_wool", "minecraft:orange_wool")):
        tent(t, cx, cz, colour, rng)
    # Archery targets and straw dummies on the east side.
    for z in (11, 14, 17):
        t.set(21, 1, z, "minecraft:hay_block[axis=y]")
        t.set(21, 2, z, "minecraft:target[power=0]")
    t.set(17, 1, 18, FENCE)
    t.set(17, 2, 18, "minecraft:hay_block[axis=y]")
    t.set(17, 3, 18, "minecraft:carved_pumpkin[facing=west]")
    # Horse pen to the south-west.
    for x in range(3, 10):
        for z in range(17, 23):
            if x in (3, 9) or z in (17, 22):
                if math.hypot(x - c, z - c) < 11.5:
                    t.set(x, 1, z, FENCE)
    t.set(6, 1, 17, "minecraft:spruce_fence_gate[facing=north,in_wall=false,open=false,powered=false]")
    t.entity(5.5, 1.0, 19.5, "minecraft:horse", {"Variant": 1})
    t.entity(7.5, 1.0, 20.5, "minecraft:horse", {"Variant": 3})
    t.set(8, 1, 21, "minecraft:hay_block[axis=y]")
    t.chest(c + 3, 1, 4, "amazon_camp", facing="south")
    t.set(c - 3, 1, 4, "minecraft:barrel[facing=up,open=false]")
    for x, z in ((c - 2, c + 2), (c + 2, c - 2), (c + 3, c + 3), (c - 3, c - 1), (c + 5, c + 1)):
        t.entity(x + 0.5, 1.0, z + 0.5, "mythsofworlds:amazon")
    return t


def themiscyra():
    """Themiscyra, city of the amazons: marble walls with towers, a courtyard with a statue of Ares,
    and the throne hall of Hippolyta in the north."""
    size = 41
    t = Template(size, 16, size)
    rng = random.Random(1907)
    c = size // 2
    t.fill(0, 1, 0, size - 1, 15, size - 1, AIR)
    for x in range(size):
        for z in range(size):
            t.set(x, 0, z, pick(rng, [(BRICKS, 55), (MARBLE, 25), ("minecraft:polished_andesite", 20)]))
    wall = [(BRICKS, 70), (MARBLE, 20), ("minecraft:cracked_stone_bricks", 10)]
    for x in range(size):
        for z in range(size):
            if x in (0, size - 1) or z in (0, size - 1):
                for y in range(1, 7):
                    t.set(x, y, z, pick(rng, wall))
                if (x + z) % 2 == 0:
                    t.set(x, 7, z, BRICKS)
    # Corner towers.
    for tx, tz in ((0, 0), (size - 5, 0), (0, size - 5), (size - 5, size - 5)):
        for x in range(tx, tx + 5):
            for z in range(tz, tz + 5):
                edge = x in (tx, tx + 4) or z in (tz, tz + 4)
                for y in range(1, 10):
                    t.set(x, y, z, pick(rng, wall) if edge else AIR)
                t.set(x, 10, z, BRICKS if edge else MARBLE)
                if edge and (x + z) % 2 == 0:
                    t.set(x, 11, z, BRICKS)
        t.set(tx + 2, 11, tz + 2, "mythsofworlds:brazier[lit=true]")
    # The gate in the south wall, with banners of red.
    for x in range(c - 2, c + 3):
        for y in range(1, 6):
            t.set(x, y, size - 1, AIR)
    for x in (c - 3, c + 3):
        t.fill(x, 1, size - 2, x, 7, size - 2, PILLAR)
        t.set(x, 5, size - 3, "minecraft:red_wall_banner[facing=south]")
    # Courtyard: statue of Ares, olive trees, training ground.
    t.fill(c - 1, 1, c + 6, c + 1, 1, c + 8, GOLD)
    t.fill(c, 2, c + 7, c, 3, c + 7, "minecraft:polished_andesite")
    t.set(c, 4, c + 7, "minecraft:chiseled_stone_bricks")
    t.set(c - 1, 3, c + 7, "minecraft:andesite_wall[east=low,north=none,south=none,up=true,waterlogged=false,west=none]")
    t.set(c + 1, 4, c + 7, "minecraft:lightning_rod[facing=up,powered=false,waterlogged=false]")
    for x, z in ((14, 23), (26, 23), (8, 33), (32, 33)):
        olive_tree(t, x, z, rng)
    for x in (10, 13, 16):
        t.set(x, 1, 30, "minecraft:hay_block[axis=y]")
        t.set(x, 2, 30, "minecraft:target[power=0]")
    # Throne hall: a colonnade and a raised dais in the north of the city.
    h0, h1 = 5, 16
    for x in range(6, size - 6):
        for z in range(h0, h1):
            t.set(x, 0, z, BRICKS)
            edge = x in (6, size - 7) or z == h0
            for y in range(1, 9):
                t.set(x, y, z, pick(rng, wall) if edge else AIR)
            t.set(x, 9, z, BRICKS)
            if z == h1 - 1 and (x - 6) % 3 == 0:
                t.fill(x, 1, z, x, 8, z, PILLAR)
    for x in range(c - 1, c + 2):
        for z in range(h0 + 2, h1):
            t.set(x, 1, z, "minecraft:red_carpet")
    t.fill(c - 3, 1, h0 + 1, c + 3, 1, h0 + 3, GOLD)
    t.fill(c - 1, 2, h0 + 1, c + 1, 2, h0 + 2, "minecraft:gold_block")
    t.set(c, 3, h0 + 1, "minecraft:quartz_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]")
    t.set(c - 1, 3, h0 + 1, "minecraft:quartz_slab[type=bottom,waterlogged=false]")
    t.set(c + 1, 3, h0 + 1, "minecraft:quartz_slab[type=bottom,waterlogged=false]")
    for x in (c - 4, c + 4):
        t.set(x, 2, h0 + 2, "mythsofworlds:brazier[lit=true]")
        t.set(x, 1, h0 + 2, MARBLE)
    for x in (8, size - 9):
        for z in (h0 + 3, h0 + 7):
            t.set(x, 6, z, "minecraft:lantern[hanging=false,waterlogged=false]")
    t.chest(8, 1, h0 + 1, "themiscyra", facing="south")
    t.chest(size - 9, 1, h0 + 1, "themiscyra", facing="south")
    t.entity(c + 0.5, 2.0, h0 + 3.5, "mythsofworlds:hippolyta")
    # Her guard and the women of the city.
    for x, z in ((c - 3, h0 + 6), (c + 3, h0 + 6), (c - 5, c + 4), (c + 5, c + 4), (12, 26), (28, 28), (c, 32)):
        t.entity(x + 0.5, 1.0, z + 0.5, "mythsofworlds:amazon")
    # Houses along the walls.
    for x0, z0, door in ((2, 18, "east"), (32, 18, "west")):
        house(t, x0, z0, door, rng)
    return t


# ---------------------------------------------------------------- farmstead

def greek_farmstead():
    """A whitewashed farmhouse of the islands with blue shutters and a flat roof, a vine pergola,
    an olive tree, a beehive, amphorae, a well and a small goat pen."""
    t = Template(17, 8, 15)
    rng = random.Random(1908)
    t.fill(0, 1, 0, 16, 7, 14, AIR)
    for x in range(17):
        for z in range(15):
            t.set(x, 0, z, pick(rng, [("minecraft:grass_block[snowy=false]", 60), ("minecraft:coarse_dirt", 25),
                                      ("minecraft:rooted_dirt", 15)]))
    white = [("minecraft:white_concrete", 45), ("minecraft:calcite", 35), ("minecraft:white_terracotta", 20)]
    x0, z0, w, d = 1, 1, 7, 6
    for x in range(x0, x0 + w):
        for z in range(z0, z0 + d):
            t.set(x, 0, z, "minecraft:smooth_stone")
            edge = x in (x0, x0 + w - 1) or z in (z0, z0 + d - 1)
            for y in range(1, 4):
                t.set(x, y, z, pick(rng, white) if edge else AIR)
            t.set(x, 4, z, "minecraft:smooth_quartz")
            if edge:
                t.set(x, 5, z, "minecraft:smooth_quartz_slab[type=bottom,waterlogged=false]")
    # Blue door and shutters.
    t.set(x0 + 3, 1, z0 + d - 1, "minecraft:warped_door[facing=south,half=lower,hinge=left,open=false,powered=false]")
    t.set(x0 + 3, 2, z0 + d - 1, "minecraft:warped_door[facing=south,half=upper,hinge=left,open=false,powered=false]")
    for x, z, facing in ((x0 + 1, z0 + d - 1, "south"), (x0 + 5, z0 + d - 1, "south"), (x0, z0 + 2, "west"),
                         (x0 + w - 1, z0 + 3, "east")):
        t.set(x, 2, z, "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]")
        ox, oz = {"south": (0, 1), "west": (-1, 0), "east": (1, 0)}[facing]
        t.set(x + ox, 2, z + oz, f"minecraft:warped_trapdoor[facing={facing},half=top,open=true,powered=false,waterlogged=false]")
    t.set(x0 + 1, 1, z0 + 1, "minecraft:crafting_table")
    t.set(x0 + 2, 1, z0 + 1, "minecraft:furnace[facing=south,lit=false]")
    t.chest(x0 + 5, 1, z0 + 1, "greek_farmstead", facing="south")
    t.set(x0 + 5, 1, z0 + 3, "minecraft:red_bed[facing=north,occupied=false,part=head]")
    t.set(x0 + 5, 1, z0 + 4, "minecraft:red_bed[facing=north,occupied=false,part=foot]")
    t.set(x0 + 3, 3, z0 + 2, "minecraft:lantern[hanging=true,waterlogged=false]")
    # Vine pergola over a terrace in front of the house.
    for x in range(x0, x0 + w):
        for z in range(z0 + d, z0 + d + 3):
            t.set(x, 0, z, "minecraft:terracotta")
    for x in (x0, x0 + w - 1):
        t.fill(x, 1, z0 + d + 2, x, 3, z0 + d + 2, "minecraft:stripped_oak_log[axis=y]")
    for x in range(x0, x0 + w):
        for z in range(z0 + d, z0 + d + 3):
            if rng.random() < 0.8:
                t.set(x, 4, z, "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]")
    for x in (x0 + 1, x0 + 5):
        t.set(x, 1, z0 + d + 1, "minecraft:decorated_pot[cracked=false,facing=north,waterlogged=false]")
    t.set(x0 + 3, 1, z0 + d + 1, "minecraft:spruce_slab[type=top,waterlogged=false]")
    # Olive tree, beehive, well.
    olive_tree(t, 12, 3, rng)
    t.set(14, 1, 6, FENCE)
    t.set(14, 2, 6, "minecraft:beehive[facing=west,honey_level=3]")
    for dx in range(3):
        for dz in range(3):
            x, z = 11 + dx, 9 + dz
            t.set(x, 0, z, "minecraft:cobblestone")
            t.set(x, 1, z, "minecraft:water[level=0]" if (dx, dz) == (1, 1) else "minecraft:cobblestone_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]")
    t.set(12, 0, 10, "minecraft:water[level=0]")  # two blocks deep
    # Goat pen.
    for x in range(1, 7):
        for z in range(10, 14):
            if x in (1, 6) or z in (10, 13):
                t.set(x, 1, z, FENCE)
    t.entity(3.5, 1.0, 11.5, "minecraft:goat")
    t.set(4, 1, 12, "minecraft:hay_block[axis=y]")
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
    "agora": agora,
    "ship_of_theseus": ship_of_theseus,
    "perseus_refuge": perseus_refuge,
    "amazon_camp": amazon_camp,
    "themiscyra": themiscyra,
    "greek_farmstead": greek_farmstead,
}
