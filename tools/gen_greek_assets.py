"""
Generates the data and asset files of the Greek mythology (and the stub dimensions of the other mythologies).

    python3 tools/gen_greek_assets.py            # everything except textures
    python3 tools/gen_greek_assets.py --textures # also (re)draw the placeholder PNGs, overwriting them

Edit the tables below (biomes, mobs, structures, loot) and run it again; the JSON is rewritten each time.
Textures are only drawn with --textures, so real art you put in the texture folders is not overwritten by accident.
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import structures  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources")
DATA = os.path.join(ROOT, "data", "mythsofworlds")
ASSETS = os.path.join(ROOT, "assets", "mythsofworlds")
NS = "mythsofworlds"


def write_json(path, value):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write("\n")


def data(*parts):
    return os.path.join(DATA, *parts)


def assets(*parts):
    return os.path.join(ASSETS, *parts)


# ====================================================================== dimensions

def dimension_type(fixed_time=None):
    value = {
        "ultrawarm": False,
        "natural": True,
        "piglin_safe": False,
        "respawn_anchor_works": False,
        "bed_works": True,
        "has_raids": False,
        "has_skylight": True,
        "has_ceiling": False,
        "coordinate_scale": 1.0,
        "ambient_light": 0.0,
        "logical_height": 384,
        "min_y": -64,
        "height": 384,
        "infiniburn": "#minecraft:infiniburn_overworld",
        "effects": "minecraft:overworld",
        "monster_spawn_light_level": {"type": "minecraft:uniform", "min_inclusive": 0, "max_inclusive": 7},
        "monster_spawn_block_light_limit": 0,
    }
    if fixed_time is not None:
        value["fixed_time"] = fixed_time
    return value


def multi_noise(points):
    return {
        "type": "minecraft:multi_noise",
        "biomes": [{
            "biome": biome,
            "parameters": {
                "temperature": p.get("t", 0.0),
                "humidity": p.get("h", 0.0),
                "continentalness": p.get("c", 0.0),
                "erosion": p.get("e", 0.0),
                "weirdness": p.get("w", 0.0),
                "depth": 0.0,
                "offset": 0.0,
            },
        } for biome, p in points],
    }


def dimension(name, biome_source, settings="minecraft:overworld"):
    return {
        "type": f"{NS}:{name}",
        "generator": {"type": "minecraft:noise", "settings": settings, "biome_source": biome_source},
    }


# Stub worlds of the other mythologies: vanilla biomes only, no portal yet.
STUB_DIMENSIONS = {
    # Nav: dark forests under an eternal dusk.
    "nav": (13000, multi_noise([
        ("minecraft:dark_forest", {"h": 0.3}),
        ("minecraft:old_growth_spruce_taiga", {"h": -0.3}),
        ("minecraft:swamp", {"e": 0.8, "h": 0.6}),
    ])),
    # Hawaiki: warm sea, beaches and jungle islands.
    "hawaiki": (None, multi_noise([
        ("minecraft:warm_ocean", {"c": -0.6}),
        ("minecraft:beach", {"c": -0.15}),
        ("minecraft:jungle", {"c": 0.3, "h": 0.4}),
        ("minecraft:sparse_jungle", {"c": 0.3, "h": -0.2}),
    ])),
    # Duat: desert and badlands of the underworld.
    "duat": (18000, multi_noise([
        ("minecraft:desert", {"t": 0.5}),
        ("minecraft:badlands", {"t": 0.5, "e": -0.5}),
    ])),
    # Svarga: jungles and bamboo under the eternal noon of Indra.
    "svarga": (6000, multi_noise([
        ("minecraft:jungle", {"h": 0.4}),
        ("minecraft:bamboo_jungle", {"h": 0.8}),
        ("minecraft:savanna_plateau", {"h": -0.4, "e": -0.6}),
    ])),
}


# ====================================================================== biomes of Hellas

# Global order of the features of every generation step. Each biome uses a subset in this order, which is what
# Minecraft requires of biomes sharing a dimension ("feature order cycle" errors otherwise).
FEATURE_ORDER = [
    [],
    ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface"],
    ["minecraft:amethyst_geode", "minecraft:forest_rock"],
    ["minecraft:monster_room", "minecraft:monster_room_deep"],
    [],
    [],
    ["minecraft:ore_dirt", "minecraft:ore_gravel", "minecraft:ore_granite_upper", "minecraft:ore_granite_lower",
     "minecraft:ore_diorite_upper", "minecraft:ore_diorite_lower", "minecraft:ore_andesite_upper",
     "minecraft:ore_andesite_lower", "minecraft:ore_tuff", "minecraft:ore_coal_upper", "minecraft:ore_coal_lower",
     "minecraft:ore_iron_upper", "minecraft:ore_iron_middle", "minecraft:ore_iron_small", "minecraft:ore_gold",
     "minecraft:ore_gold_lower", "minecraft:ore_redstone", "minecraft:ore_redstone_lower", "minecraft:ore_diamond",
     "minecraft:ore_diamond_medium", "minecraft:ore_diamond_large", "minecraft:ore_diamond_buried",
     "minecraft:ore_lapis", "minecraft:ore_lapis_buried", "minecraft:ore_copper", "minecraft:ore_emerald",
     f"{NS}:ore_marble", "minecraft:disk_sand", "minecraft:disk_clay", "minecraft:disk_gravel"],
    [],
    ["minecraft:spring_water", "minecraft:spring_lava"],
    ["minecraft:glow_lichen", "minecraft:trees_plains", "minecraft:trees_birch_and_oak", "minecraft:trees_savanna",
     "minecraft:trees_swamp", "minecraft:trees_meadow", "minecraft:flower_meadow", "minecraft:flower_plains",
     "minecraft:flower_default", "minecraft:flower_swamp", f"{NS}:patch_asphodel", "minecraft:patch_sunflower",
     "minecraft:patch_grass_plain", "minecraft:patch_grass_forest", "minecraft:patch_tall_grass_2",
     "minecraft:patch_dead_bush", "minecraft:brown_mushroom_swamp", "minecraft:red_mushroom_swamp",
     "minecraft:patch_sugar_cane", "minecraft:patch_sugar_cane_swamp", "minecraft:patch_pumpkin",
     "minecraft:patch_waterlily", "minecraft:seagrass_swamp", "minecraft:seagrass_warm", "minecraft:sea_pickle",
     "minecraft:warm_ocean_vegetation"],
    ["minecraft:freeze_top_layer"],
]

COMMON_ORES = [
    "minecraft:ore_dirt", "minecraft:ore_gravel", "minecraft:ore_granite_upper", "minecraft:ore_granite_lower",
    "minecraft:ore_diorite_upper", "minecraft:ore_diorite_lower", "minecraft:ore_andesite_upper",
    "minecraft:ore_andesite_lower", "minecraft:ore_tuff", "minecraft:ore_coal_upper", "minecraft:ore_coal_lower",
    "minecraft:ore_iron_upper", "minecraft:ore_iron_middle", "minecraft:ore_iron_small", "minecraft:ore_gold",
    "minecraft:ore_gold_lower", "minecraft:ore_redstone", "minecraft:ore_redstone_lower", "minecraft:ore_diamond",
    "minecraft:ore_diamond_medium", "minecraft:ore_diamond_large", "minecraft:ore_diamond_buried",
    "minecraft:ore_lapis", "minecraft:ore_lapis_buried", "minecraft:ore_copper",
]
COMMON = ["minecraft:monster_room", "minecraft:monster_room_deep", "minecraft:spring_water", "minecraft:spring_lava",
          "minecraft:glow_lichen", "minecraft:freeze_top_layer"] + COMMON_ORES
DISKS = ["minecraft:disk_sand", "minecraft:disk_clay", "minecraft:disk_gravel"]


def spawn(entity, weight, min_count, max_count):
    return {"type": entity, "weight": weight, "minCount": min_count, "maxCount": max_count}


BIOMES = {
    "olympus_peaks": {
        "ru": "Вершины Олимпа", "en": "Peaks of Olympus",
        "point": {"c": 0.5, "e": -0.8, "t": -0.2},
        "temperature": -0.2, "downfall": 0.4,
        "sky": 0x9FD3FF, "fog": 0xE6F0FF, "water": 0x3D9BE9, "water_fog": 0x050533, "grass": 0x8AB689, "foliage": 0x6FA05A,
        "particle": ("minecraft:white_ash", 0.004),
        "features": COMMON + ["minecraft:amethyst_geode", "minecraft:forest_rock", "minecraft:ore_emerald",
                              f"{NS}:ore_marble", "minecraft:trees_meadow", "minecraft:flower_meadow",
                              "minecraft:patch_grass_plain"],
        "spawners": {
            "monster": [spawn(f"{NS}:harpy", 70, 1, 3), spawn("minecraft:skeleton", 30, 1, 2), spawn("minecraft:creeper", 20, 1, 1)],
            "creature": [spawn(f"{NS}:pegasus", 6, 1, 2), spawn("minecraft:goat", 8, 1, 3)],
        },
    },
    "elysian_fields": {
        "ru": "Елисейские поля", "en": "Elysian Fields",
        "point": {"c": 0.3, "e": 0.5, "t": 0.6, "h": -0.3},
        "temperature": 0.8, "downfall": 0.4,
        "sky": 0xFFD98A, "fog": 0xFFF1C9, "water": 0x4FD3E8, "water_fog": 0x0A3A4A, "grass": 0xD9C25A, "foliage": 0xC9B24A,
        "particle": ("minecraft:end_rod", 0.0006),
        "features": COMMON + ["minecraft:trees_plains", "minecraft:flower_meadow", "minecraft:flower_plains",
                              "minecraft:patch_sunflower", "minecraft:patch_grass_plain", "minecraft:patch_sugar_cane",
                              "minecraft:patch_pumpkin"],
        "spawners": {
            "monster": [spawn(f"{NS}:satyr", 20, 1, 2), spawn("minecraft:zombie", 20, 1, 2)],
            "creature": [spawn(f"{NS}:pegasus", 5, 1, 3), spawn("minecraft:sheep", 12, 2, 4), spawn("minecraft:cow", 8, 2, 4),
                         spawn("minecraft:horse", 4, 2, 4)],
        },
    },
    "arcadian_grove": {
        "ru": "Рощи Аркадии", "en": "Arcadian Grove",
        "point": {"c": 0.3, "e": 0.2, "t": 0.3, "h": 0.5},
        "temperature": 0.7, "downfall": 0.8,
        "sky": 0x88C8FF, "fog": 0xC0D8FF, "water": 0x3F76E4, "water_fog": 0x050533, "grass": 0x6CBF3F, "foliage": 0x59AE30,
        "features": COMMON + ["minecraft:amethyst_geode", "minecraft:forest_rock", f"{NS}:ore_marble",
                              "minecraft:trees_birch_and_oak", "minecraft:flower_default", "minecraft:patch_grass_forest",
                              "minecraft:patch_tall_grass_2", "minecraft:patch_pumpkin"],
        "spawners": {
            "monster": [spawn(f"{NS}:satyr", 80, 2, 4), spawn("minecraft:spider", 40, 1, 2), spawn("minecraft:creeper", 30, 1, 2),
                        spawn("minecraft:zombie", 30, 1, 3)],
            "creature": [spawn(f"{NS}:golden_hind", 3, 1, 2), spawn("minecraft:fox", 8, 2, 3), spawn("minecraft:sheep", 8, 2, 4),
                         spawn("minecraft:pig", 8, 2, 4),
                         spawn("minecraft:wolf", 4, 2, 4), spawn("minecraft:rabbit", 4, 2, 3)],
        },
    },
    "asphodel_meadows": {
        "ru": "Асфоделевые луга", "en": "Asphodel Meadows",
        "point": {"c": 0.5, "e": 0.4, "t": -0.6, "h": -0.4, "w": 0.5},
        "temperature": 0.4, "downfall": 0.0, "precipitation": False,
        "sky": 0x8A8F99, "fog": 0x9AA0A8, "water": 0x5A6B7A, "water_fog": 0x1A2228, "grass": 0x9DA39A, "foliage": 0x8C928A,
        "particle": ("minecraft:ash", 0.02),
        "features": COMMON + ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface", f"{NS}:patch_asphodel",
                              "minecraft:patch_dead_bush"],
        "spawners": {
            "monster": [spawn(f"{NS}:shade", 100, 1, 3), spawn(f"{NS}:spartoi", 60, 1, 3), spawn("minecraft:skeleton", 20, 1, 2),
                        spawn("minecraft:enderman", 5, 1, 1)],
            "ambient": [spawn("minecraft:bat", 10, 8, 8)],
        },
    },
    "stygian_marsh": {
        "ru": "Стигийские топи", "en": "Stygian Marsh",
        "point": {"c": 0.15, "e": 0.8, "t": -0.3, "h": 0.7},
        "temperature": 0.6, "downfall": 0.9,
        "sky": 0x6B7F6B, "fog": 0x5E6E5E, "water": 0x3B4A2F, "water_fog": 0x161E10, "grass": 0x4C6B3A, "foliage": 0x3E5A2E,
        "particle": ("minecraft:mycelium", 0.01),
        "features": COMMON + ["minecraft:disk_clay", "minecraft:trees_swamp", "minecraft:flower_swamp",
                              "minecraft:brown_mushroom_swamp", "minecraft:red_mushroom_swamp",
                              "minecraft:patch_sugar_cane_swamp", "minecraft:patch_waterlily", "minecraft:seagrass_swamp"],
        "spawners": {
            "monster": [spawn(f"{NS}:shade", 60, 1, 2), spawn("minecraft:zombie", 50, 2, 3), spawn("minecraft:witch", 5, 1, 1),
                        spawn("minecraft:slime", 1, 1, 1)],
            "creature": [spawn("minecraft:frog", 10, 2, 5)],
        },
    },
    "aegean_coast": {
        "ru": "Эгейское побережье", "en": "Aegean Coast",
        "point": {"c": -0.1, "e": 0.3, "t": 0.5, "h": -0.2},
        "temperature": 0.9, "downfall": 0.3,
        "sky": 0x78B8FF, "fog": 0xC8E4FF, "water": 0x2FD1C5, "water_fog": 0x05313A, "grass": 0xA9C25A, "foliage": 0x9AB04A,
        "features": COMMON + DISKS + ["minecraft:trees_savanna", "minecraft:flower_default", "minecraft:patch_grass_plain",
                                      "minecraft:patch_dead_bush", "minecraft:patch_sugar_cane", "minecraft:seagrass_warm",
                                      "minecraft:sea_pickle"],
        "spawners": {
            "monster": [spawn(f"{NS}:harpy", 40, 1, 3), spawn("minecraft:drowned", 30, 1, 2), spawn("minecraft:zombie", 30, 1, 2)],
            "creature": [spawn("minecraft:turtle", 5, 2, 5), spawn("minecraft:goat", 4, 1, 2)],
            "water_creature": [spawn("minecraft:squid", 4, 1, 4)],
            "water_ambient": [spawn("minecraft:tropical_fish", 25, 8, 8)],
        },
    },
    "aegean_sea": {
        "ru": "Эгейское море", "en": "Aegean Sea",
        "point": {"c": -0.6, "t": 0.5},
        "temperature": 0.8, "downfall": 0.5,
        "sky": 0x6AAAFF, "fog": 0xC0D8FF, "water": 0x2FD1C5, "water_fog": 0x05313A, "grass": 0xA9C25A, "foliage": 0x9AB04A,
        "features": COMMON + DISKS + ["minecraft:seagrass_warm", "minecraft:sea_pickle", "minecraft:warm_ocean_vegetation"],
        "spawners": {
            "monster": [spawn("minecraft:drowned", 100, 1, 3)],
            "water_creature": [spawn("minecraft:dolphin", 2, 1, 2), spawn("minecraft:squid", 4, 1, 4)],
            "water_ambient": [spawn("minecraft:tropical_fish", 25, 8, 8), spawn("minecraft:pufferfish", 5, 1, 3)],
        },
    },
}


def biome_json(spec):
    used = set(spec["features"])
    unknown = used - {f for step in FEATURE_ORDER for f in step}
    if unknown:
        raise ValueError(f"features missing from FEATURE_ORDER: {unknown}")
    effects = {
        "sky_color": spec["sky"],
        "fog_color": spec["fog"],
        "water_color": spec["water"],
        "water_fog_color": spec["water_fog"],
        "grass_color": spec["grass"],
        "foliage_color": spec["foliage"],
        "mood_sound": {"sound": "minecraft:ambient.cave", "tick_delay": 6000, "block_search_extent": 8, "offset": 2.0},
    }
    if "particle" in spec:
        particle, probability = spec["particle"]
        effects["particle"] = {"options": {"type": particle}, "probability": probability}
    return {
        "has_precipitation": spec.get("precipitation", True),
        "temperature": spec["temperature"],
        "downfall": spec["downfall"],
        "effects": effects,
        "spawners": spec["spawners"],
        "spawn_costs": {},
        "carvers": {"air": ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"]},
        "features": [[f for f in step if f in used] for step in FEATURE_ORDER],
    }


def worldgen_features():
    write_json(data("worldgen", "configured_feature", "ore_marble.json"), {
        "type": "minecraft:ore",
        "config": {
            "size": 48,
            "discard_chance_on_air_exposure": 0.0,
            "targets": [{
                "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"},
                "state": {"Name": f"{NS}:marble"},
            }],
        },
    })
    write_json(data("worldgen", "placed_feature", "ore_marble.json"), {
        "feature": f"{NS}:ore_marble",
        "placement": [
            {"type": "minecraft:count", "count": 8},
            {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform",
                                                          "min_inclusive": {"absolute": 0}, "max_inclusive": {"absolute": 256}}},
            {"type": "minecraft:biome"},
        ],
    })
    write_json(data("worldgen", "configured_feature", "patch_asphodel.json"), {
        "type": "minecraft:flower",
        "config": {
            "tries": 64,
            "xz_spread": 7,
            "y_spread": 3,
            "feature": {
                "feature": {
                    "type": "minecraft:simple_block",
                    "config": {"to_place": {"type": "minecraft:simple_state_provider", "state": {"Name": f"{NS}:asphodel"}}},
                },
                "placement": [{"type": "minecraft:block_predicate_filter",
                               "predicate": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}}],
            },
        },
    })
    write_json(data("worldgen", "placed_feature", "patch_asphodel.json"), {
        "feature": f"{NS}:patch_asphodel",
        "placement": [
            {"type": "minecraft:count", "count": 3},
            {"type": "minecraft:in_square"},
            {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"},
            {"type": "minecraft:biome"},
        ],
    })


# ====================================================================== structures

# name: (biomes, spacing, separation, salt, heightmap, depth offset, terrain adaptation)
# Spacing is in chunks; v0.3 doubled it so that lairs no longer crowd each other.
STRUCTURES = {
    "greek_temple": (["olympus_peaks", "elysian_fields"], 56, 20, 1450201, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "oracle_of_delphi": (["arcadian_grove", "olympus_peaks"], 48, 16, 1450202, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "labyrinth": (["elysian_fields", "aegean_coast", "arcadian_grove"], 64, 24, 1450203, "WORLD_SURFACE_WG", -1, "beard_box"),
    "gates_of_hades": (["asphodel_meadows"], 56, 20, 1450204, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "hydra_lair": (["stygian_marsh"], 52, 18, 1450205, "WORLD_SURFACE_WG", -2, "beard_thin"),
    "medusa_lair": (["aegean_coast"], 52, 18, 1450206, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "cyclops_cave": (["olympus_peaks", "aegean_coast", "arcadian_grove"], 56, 20, 1450207, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "nemean_lion_den": (["arcadian_grove"], 48, 16, 1450208, "WORLD_SURFACE_WG", 0, "beard_thin"),
    # The agora is the hub of Hellas, so it stays the most common structure.
    "agora": (["elysian_fields", "arcadian_grove", "aegean_coast"], 32, 12, 1450209, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "ship_of_theseus": (["aegean_sea"], 44, 14, 1450210, "WORLD_SURFACE_WG", -3, "none"),
    "perseus_refuge": (["aegean_coast", "olympus_peaks"], 44, 14, 1450211, "WORLD_SURFACE_WG", 0, "beard_thin"),
}

STRUCTURE_NAMES = {
    "greek_temple": ("Храм Олимпийцев", "Temple of the Olympians"),
    "oracle_of_delphi": ("Дельфийский оракул", "Oracle of Delphi"),
    "labyrinth": ("Лабиринт Минотавра", "Labyrinth of the Minotaur"),
    "gates_of_hades": ("Врата Аида", "Gates of Hades"),
    "hydra_lair": ("Логово Лернейской гидры", "Lair of the Hydra"),
    "medusa_lair": ("Логово Медузы", "Lair of Medusa"),
    "cyclops_cave": ("Пещера циклопа", "Cyclops Cave"),
    "nemean_lion_den": ("Логово Немейского льва", "Den of the Nemean Lion"),
    "agora": ("Агора", "Agora"),
    "ship_of_theseus": ("Корабль Тесея", "Ship of Theseus"),
    "perseus_refuge": ("Убежище Персея", "Refuge of Perseus"),
}


def worldgen_structures():
    os.makedirs(data("structure", "greek"), exist_ok=True)
    for name, (biomes, spacing, separation, salt, heightmap, offset, adaptation) in STRUCTURES.items():
        structures.STRUCTURES[name]().save(data("structure", "greek", f"{name}.nbt"))
        write_json(data("tags", "worldgen", "biome", "has_structure", f"{name}.json"),
                   {"replace": False, "values": [f"{NS}:{b}" for b in biomes]})
        write_json(data("worldgen", "template_pool", "greek", name, "start.json"), {
            "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {
                "element_type": "minecraft:single_pool_element",
                "location": f"{NS}:greek/{name}",
                "projection": "rigid",
                "processors": "minecraft:empty",
            }}],
        })
        write_json(data("worldgen", "structure", f"{name}.json"), {
            "type": "minecraft:jigsaw",
            "biomes": f"#{NS}:has_structure/{name}",
            "step": "surface_structures",
            "terrain_adaptation": adaptation,
            "spawn_overrides": {},
            "start_pool": f"{NS}:greek/{name}/start",
            "size": 1,
            "start_height": {"absolute": offset},
            "project_start_to_heightmap": heightmap,
            "max_distance_from_center": 80,
            "use_expansion_hack": False,
        })
        write_json(data("worldgen", "structure_set", f"{name}.json"), {
            "structures": [{"structure": f"{NS}:{name}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
        })


# ====================================================================== loot

def entry(item, weight=1, lo=1, hi=1, enchant=False):
    e = {"type": "minecraft:item", "name": item, "weight": weight}
    functions = []
    if (lo, hi) != (1, 1):
        functions.append({"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}})
    if enchant:
        functions.append({"function": "minecraft:enchant_randomly"})
    if functions:
        e["functions"] = functions
    return e


def chest(name, rolls, entries, bonus=None):
    pools = [{"rolls": {"type": "minecraft:uniform", "min": rolls[0], "max": rolls[1]}, "entries": entries}]
    if bonus:
        pools.append({"rolls": 1, "entries": bonus})
    write_json(data("loot_table", "chests", f"{name}.json"),
               {"type": "minecraft:chest", "pools": pools, "random_sequence": f"{NS}:chests/{name}"})


def mob(name, drops):
    """drops: list of (item, min, max, chance or None)."""
    pools = []
    for item, lo, hi, chance in drops:
        pool = {"rolls": 1, "entries": [entry(item, 1, lo, hi)]}
        if chance is not None:
            pool["conditions"] = [{"condition": "minecraft:random_chance", "chance": chance}]
        pools.append(pool)
    write_json(data("loot_table", "entities", f"{name}.json"),
               {"type": "minecraft:entity", "pools": pools, "random_sequence": f"{NS}:entities/{name}"})


def loot():
    for block in ("marble", "marble_bricks", "marble_pillar", "olympian_marble", "asphodel", "brazier"):
        write_json(data("loot_table", "blocks", f"{block}.json"), {
            "type": "minecraft:block",
            "pools": [{"rolls": 1, "bonus_rolls": 0, "entries": [{"type": "minecraft:item", "name": f"{NS}:{block}"}],
                       "conditions": [{"condition": "minecraft:survives_explosion"}]}],
            "random_sequence": f"{NS}:blocks/{block}",
        })
    gold = [entry("minecraft:gold_ingot", 10, 1, 5), entry("minecraft:gold_nugget", 10, 3, 9)]
    chest("greek_temple", (3, 6), gold + [
        entry(f"{NS}:ambrosia", 6, 1, 2), entry("minecraft:golden_apple", 5), entry("minecraft:enchanted_golden_apple", 1),
        entry(f"{NS}:olympian_marble", 6, 2, 6), entry("minecraft:book", 4, enchant=True), entry("minecraft:golden_sword", 3, enchant=True),
        entry(f"{NS}:promethean_torch", 2),
    ])
    chest("oracle_of_delphi", (2, 5), [
        entry("minecraft:glass_bottle", 6, 1, 3), entry("minecraft:glowstone_dust", 6, 1, 4), entry("minecraft:amethyst_shard", 6, 1, 4),
        entry("minecraft:ender_eye", 2), entry("minecraft:book", 5, enchant=True), entry(f"{NS}:ambrosia", 3),
        entry("minecraft:experience_bottle", 4, 1, 3),
    ])
    chest("labyrinth", (4, 8), gold + [
        entry("minecraft:iron_ingot", 8, 2, 6), entry("minecraft:diamond", 3, 1, 2), entry("minecraft:string", 6, 4, 12),
        entry("minecraft:iron_sword", 3, enchant=True), entry("minecraft:golden_apple", 3), entry(f"{NS}:ambrosia", 2),
    ])
    chest("gates_of_hades", (4, 7), [
        entry("minecraft:soul_lantern", 4, 1, 3), entry("minecraft:obsidian", 6, 2, 6), entry("minecraft:diamond", 4, 1, 3),
        entry("minecraft:netherite_scrap", 1), entry("minecraft:gold_ingot", 6, 2, 6), entry("minecraft:book", 4, enchant=True),
        entry("minecraft:enchanted_golden_apple", 1),
    ])
    chest("hydra_lair", (3, 6), gold + [
        entry("minecraft:slime_ball", 6, 1, 4), entry("minecraft:emerald", 4, 1, 4), entry("minecraft:diamond", 3, 1, 2),
        entry("minecraft:book", 4, enchant=True), entry("minecraft:golden_apple", 3),
    ])
    chest("medusa_lair", (3, 6), gold + [
        entry("minecraft:shield", 4), entry("minecraft:prismarine_shard", 6, 2, 6), entry("minecraft:heart_of_the_sea", 1),
        entry("minecraft:book", 4, enchant=True), entry("minecraft:emerald", 4, 1, 3),
    ])
    chest("cyclops_cave", (3, 6), [
        entry("minecraft:white_wool", 8, 2, 6), entry("minecraft:mutton", 8, 2, 5), entry("minecraft:iron_ingot", 6, 2, 5),
        entry("minecraft:anvil", 1), entry("minecraft:iron_axe", 3, enchant=True), entry("minecraft:gold_ingot", 4, 1, 4),
    ])
    chest("nemean_lion_den", (2, 5), [
        entry("minecraft:bone", 10, 2, 6), entry("minecraft:leather", 8, 1, 4), entry("minecraft:gold_ingot", 5, 1, 4),
        entry("minecraft:book", 3, enchant=True), entry("minecraft:golden_apple", 2),
    ])

    chest("agora_house", (3, 6), [
        entry("minecraft:bread", 10, 1, 4), entry("minecraft:wheat", 8, 2, 6), entry("minecraft:honey_bottle", 4),
        entry("minecraft:emerald", 6, 1, 4), entry("minecraft:sweet_berries", 6, 2, 6), entry("minecraft:clay_ball", 4, 2, 8),
        entry(f"{NS}:marble", 4, 2, 8),
    ])
    chest("agora_temple", (3, 5), gold + [
        entry("minecraft:emerald", 10, 2, 8), entry(f"{NS}:ambrosia", 3), entry(f"{NS}:promethean_torch", 3),
        entry("minecraft:feather", 4, 2, 5), entry("minecraft:golden_boots", 2, enchant=True),
    ])
    chest("ship_of_theseus", (3, 6), gold + [
        entry("minecraft:string", 6, 3, 10), entry("minecraft:map", 3), entry("minecraft:compass", 3),
        entry("minecraft:trident", 1), entry("minecraft:nautilus_shell", 3, 1, 2), entry("minecraft:book", 4, enchant=True),
        entry("minecraft:black_wool", 6, 2, 6), entry(f"{NS}:ambrosia", 2),
    ])
    chest("perseus_refuge", (2, 4), [
        entry("minecraft:bread", 6, 1, 3), entry(f"{NS}:ambrosia", 3), entry("minecraft:golden_apple", 2),
        entry("minecraft:arrow", 5, 4, 12), entry("minecraft:leather_boots", 3, enchant=True),
    ], bonus=[entry(f"{NS}:harpe", 1)])
    # The polished shield always waits beside the harpe.
    with open(data("loot_table", "chests", "perseus_refuge.json"), encoding="utf-8") as f:
        table = json.load(f)
    table["pools"].append({"rolls": 1, "entries": [entry("minecraft:shield", 1)]})
    write_json(data("loot_table", "chests", "perseus_refuge.json"), table)

    mob("satyr", [("minecraft:leather", 0, 2, None), ("minecraft:wheat", 0, 2, None)])
    mob("harpy", [(f"{NS}:harpy_feather", 0, 2, None), ("minecraft:feather", 0, 2, None)])
    mob("spartoi", [("minecraft:bone", 0, 2, None), ("minecraft:iron_nugget", 0, 3, None)])
    mob("shade", [("minecraft:echo_shard", 1, 1, 0.05)])
    mob("pegasus", [("minecraft:leather", 0, 2, None), (f"{NS}:harpy_feather", 1, 2, None)])
    mob("cyclops", [(f"{NS}:cyclops_eye", 1, 1, None), ("minecraft:mutton", 2, 6, None), ("minecraft:iron_ingot", 2, 6, None)])
    mob("medusa", [(f"{NS}:medusa_head", 1, 1, None), ("minecraft:gold_ingot", 2, 5, None)])
    mob("nemean_lion", [(f"{NS}:nemean_pelt", 1, 1, None), (f"{NS}:nemean_claw", 1, 2, None), ("minecraft:leather", 3, 6, None)])
    mob("golden_hind", [("minecraft:leather", 0, 2, None), ("minecraft:gold_nugget", 1, 4, None)])
    mob("minotaur", [(f"{NS}:minotaur_horn", 1, 2, None), ("minecraft:gold_ingot", 4, 10, None), ("minecraft:diamond", 1, 3, None)])
    mob("hydra", [(f"{NS}:hydra_scale", 3, 6, None), ("minecraft:emerald", 4, 10, None), ("minecraft:diamond", 1, 3, None),
                 (f"{NS}:hydra_egg", 1, 1, None)])
    mob("cerberus", [(f"{NS}:cerberus_fang", 1, 3, None), ("minecraft:blaze_rod", 2, 5, None), ("minecraft:diamond", 1, 3, None)])


# ====================================================================== recipes and tags

def recipes():
    write_json(data("recipe", "marble.json"), {
        "type": "minecraft:crafting_shaped", "category": "building",
        "pattern": ["DC", "CD"],
        "key": {"D": {"item": "minecraft:diorite"}, "C": {"item": "minecraft:calcite"}},
        "result": {"id": f"{NS}:marble", "count": 4},
    })
    write_json(data("recipe", "marble_bricks.json"), {
        "type": "minecraft:crafting_shaped", "category": "building",
        "pattern": ["MM", "MM"], "key": {"M": {"item": f"{NS}:marble"}},
        "result": {"id": f"{NS}:marble_bricks", "count": 4},
    })
    write_json(data("recipe", "marble_pillar.json"), {
        "type": "minecraft:crafting_shaped", "category": "building",
        "pattern": ["M", "M"], "key": {"M": {"item": f"{NS}:marble"}},
        "result": {"id": f"{NS}:marble_pillar", "count": 2},
    })
    write_json(data("recipe", "olympian_marble.json"), {
        "type": "minecraft:crafting_shaped", "category": "building",
        "pattern": ["MMM", "MGM", "MMM"], "key": {"M": {"item": f"{NS}:marble"}, "G": {"item": "minecraft:gold_ingot"}},
        "result": {"id": f"{NS}:olympian_marble", "count": 8},
    })
    write_json(data("recipe", "promethean_torch.json"), {
        "type": "minecraft:crafting_shapeless", "category": "equipment",
        "ingredients": [{"item": "minecraft:flint"}, {"item": "minecraft:gold_ingot"}, {"item": f"{NS}:olympian_marble"},
                        {"item": "minecraft:torch"}],
        "result": {"id": f"{NS}:promethean_torch", "count": 1},
    })
    write_json(data("recipe", "brazier.json"), {
        "type": "minecraft:crafting_shaped", "category": "building",
        "pattern": ["C C", "CCC", " M "],
        "key": {"C": {"item": "minecraft:copper_ingot"}, "M": {"item": f"{NS}:olympian_marble"}},
        "result": {"id": f"{NS}:brazier", "count": 1},
    })
    write_json(data("recipe", "nemean_claw_dagger.json"), {
        "type": "minecraft:crafting_shaped", "category": "equipment",
        "pattern": ["C", "S"], "key": {"C": {"item": f"{NS}:nemean_claw"}, "S": {"item": "minecraft:stick"}},
        "result": {"id": f"{NS}:nemean_claw_dagger", "count": 1},
    })
    pickaxe = os.path.join(ROOT, "data", "minecraft", "tags", "block", "mineable", "pickaxe.json")
    with open(pickaxe, encoding="utf-8") as f:
        tag = json.load(f)
    for block in ("marble", "marble_bricks", "marble_pillar", "olympian_marble", "brazier"):
        if f"{NS}:{block}" not in tag["values"]:
            tag["values"].append(f"{NS}:{block}")
    write_json(pickaxe, tag)
    write_json(os.path.join(ROOT, "data", "minecraft", "tags", "block", "small_flowers.json"),
               {"replace": False, "values": [f"{NS}:asphodel"]})
    write_json(os.path.join(ROOT, "data", "minecraft", "tags", "item", "small_flowers.json"),
               {"replace": False, "values": [f"{NS}:asphodel"]})


# ====================================================================== models

ITEMS = ["promethean_torch", "ambrosia", "harpy_feather", "minotaur_horn", "hydra_scale", "cerberus_fang",
         "nemean_pelt", "cyclops_eye", "medusa_head", "nemean_claw", "nemean_claw_dagger", "harpe", "hydra_egg"]
HANDHELD = {"promethean_torch", "nemean_claw_dagger", "harpe"}
MOBS = ["satyr", "harpy", "spartoi", "shade", "pegasus", "golden_hind", "hydra_hatchling", "greek_merchant",
        "cyclops", "medusa", "nemean_lion", "minotaur", "hydra", "cerberus"]


def models():
    for block in ("marble", "marble_bricks", "olympian_marble"):
        write_json(assets("blockstates", f"{block}.json"), {"variants": {"": {"model": f"{NS}:block/{block}"}}})
        write_json(assets("models", "block", f"{block}.json"),
                   {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{block}"}})
        write_json(assets("models", "item", f"{block}.json"), {"parent": f"{NS}:block/{block}"})
    write_json(assets("blockstates", "marble_pillar.json"), {"variants": {
        "axis=x": {"model": f"{NS}:block/marble_pillar_horizontal", "x": 90, "y": 90},
        "axis=y": {"model": f"{NS}:block/marble_pillar"},
        "axis=z": {"model": f"{NS}:block/marble_pillar_horizontal", "x": 90},
    }})
    pillar_textures = {"end": f"{NS}:block/marble_pillar_top", "side": f"{NS}:block/marble_pillar"}
    write_json(assets("models", "block", "marble_pillar.json"), {"parent": "minecraft:block/cube_column", "textures": pillar_textures})
    write_json(assets("models", "block", "marble_pillar_horizontal.json"),
               {"parent": "minecraft:block/cube_column_horizontal", "textures": pillar_textures})
    write_json(assets("models", "item", "marble_pillar.json"), {"parent": f"{NS}:block/marble_pillar"})

    write_json(assets("blockstates", "asphodel.json"), {"variants": {"": {"model": f"{NS}:block/asphodel"}}})
    write_json(assets("models", "block", "asphodel.json"), {
        "parent": "minecraft:block/cross", "render_type": "minecraft:cutout", "textures": {"cross": f"{NS}:block/asphodel"}})
    write_json(assets("models", "item", "asphodel.json"),
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:block/asphodel"}})

    # The lit pool: a flat golden surface a little below the rim, like water.
    write_json(assets("blockstates", "hellas_portal.json"), {"variants": {"": {"model": f"{NS}:block/hellas_portal"}}})
    write_json(assets("models", "block", "hellas_portal.json"), {
        "render_type": "minecraft:translucent",
        "textures": {"particle": f"{NS}:block/hellas_portal", "portal": f"{NS}:block/hellas_portal"},
        "elements": [{"from": [0, 0, 0], "to": [16, 12, 16], "shade": False,
                      "faces": {"up": {"uv": [0, 0, 16, 16], "texture": "#portal"},
                                "down": {"uv": [0, 0, 16, 16], "texture": "#portal", "cullface": "down"}}}],
    })
    for old in ("hellas_portal_ns", "hellas_portal_ew"):  # the vertical portal of v0.2
        if os.path.exists(assets("models", "block", f"{old}.json")):
            os.remove(assets("models", "block", f"{old}.json"))

    write_json(assets("blockstates", "brazier.json"), {"variants": {
        "lit=false": {"model": f"{NS}:block/brazier"},
        "lit=true": {"model": f"{NS}:block/brazier_lit"},
    }})
    bowl = [
        {"from": [5, 0, 5], "to": [11, 6, 11], "faces": {f: {"texture": "#foot"} for f in ("north", "south", "east", "west", "down")}},
        {"from": [2, 6, 2], "to": [14, 10, 14], "faces": dict(
            {f: {"texture": "#side"} for f in ("north", "south", "east", "west")},
            down={"texture": "#side"}, up={"texture": "#top"})},
    ]
    textures = {"particle": f"{NS}:block/brazier_side", "foot": f"{NS}:block/marble_pillar",
                "side": f"{NS}:block/brazier_side", "top": f"{NS}:block/brazier_top"}
    write_json(assets("models", "block", "brazier.json"), {"textures": textures, "elements": bowl})
    flames = [{"from": [3, 10, 8], "to": [13, 20, 8], "shade": False, "rotation": {"origin": [8, 8, 8], "axis": "y", "angle": 45},
               "faces": {"north": {"uv": [0, 0, 16, 16], "texture": "#fire"}, "south": {"uv": [0, 0, 16, 16], "texture": "#fire"}}},
              {"from": [8, 10, 3], "to": [8, 20, 13], "shade": False, "rotation": {"origin": [8, 8, 8], "axis": "y", "angle": 45},
               "faces": {"east": {"uv": [0, 0, 16, 16], "texture": "#fire"}, "west": {"uv": [0, 0, 16, 16], "texture": "#fire"}}}]
    write_json(assets("models", "block", "brazier_lit.json"), {
        "render_type": "minecraft:cutout",
        "textures": dict(textures, fire="minecraft:block/fire_0", top=f"{NS}:block/brazier_top_lit"),
        "elements": bowl + flames,
    })
    write_json(assets("models", "item", "brazier.json"), {"parent": f"{NS}:block/brazier"})

    for item in ITEMS:
        parent = "minecraft:item/handheld" if item in HANDHELD else "minecraft:item/generated"
        write_json(assets("models", "item", f"{item}.json"), {"parent": parent, "textures": {"layer0": f"{NS}:item/{item}"}})
    for name in MOBS:
        write_json(assets("models", "item", f"{name}_spawn_egg.json"), {"parent": "minecraft:item/template_spawn_egg"})


# ====================================================================== translations

LANG = {
    "block.mythsofworlds.marble": ("Мрамор", "Marble"),
    "block.mythsofworlds.marble_bricks": ("Мраморные кирпичи", "Marble Bricks"),
    "block.mythsofworlds.marble_pillar": ("Мраморная колонна", "Marble Pillar"),
    "block.mythsofworlds.olympian_marble": ("Олимпийский мрамор", "Olympian Marble"),
    "block.mythsofworlds.hellas_portal": ("Священный водоём Эллады", "Sacred Pool of Hellas"),
    "block.mythsofworlds.brazier": ("Жертвенная чаша", "Brazier"),
    "block.mythsofworlds.asphodel": ("Асфодель", "Asphodel"),
    "item.mythsofworlds.promethean_torch": ("Факел Прометея", "Promethean Torch"),
    "item.mythsofworlds.promethean_torch.desc": (
        "Обложите водоём олимпийским мрамором, поставьте жертвенные чаши на 4 угла и зажгите их факелом",
        "Ring a pool with Olympian marble, put braziers on its 4 corners and light them with the torch"),
    "item.mythsofworlds.ambrosia": ("Амброзия", "Ambrosia"),
    "item.mythsofworlds.harpy_feather": ("Перо гарпии", "Harpy Feather"),
    "item.mythsofworlds.minotaur_horn": ("Рог Минотавра", "Minotaur Horn"),
    "item.mythsofworlds.hydra_scale": ("Чешуя гидры", "Hydra Scale"),
    "item.mythsofworlds.cerberus_fang": ("Клык Цербера", "Cerberus Fang"),
    "item.mythsofworlds.nemean_pelt": ("Шкура Немейского льва", "Nemean Lion Pelt"),
    "item.mythsofworlds.cyclops_eye": ("Глаз циклопа", "Cyclops Eye"),
    "item.mythsofworlds.medusa_head": ("Голова Медузы", "Head of Medusa"),
    "item.mythsofworlds.nemean_claw": ("Коготь Немейского льва", "Nemean Lion Claw"),
    "item.mythsofworlds.nemean_claw_dagger": ("Кинжал из когтя Немейского льва", "Nemean Claw Dagger"),
    "item.mythsofworlds.harpe": ("Харпа Персея", "Harpe of Perseus"),
    "item.mythsofworlds.hydra_egg": ("Яйцо гидры", "Hydra Egg"),
    "item.mythsofworlds.hydra_egg.desc": (
        "ПКМ по земле: вылупится ручной гидрёныш", "Right-click the ground: a tame little hydra hatches"),
    "item.mythsofworlds.medusa_head.desc": (
        "ПКМ: обращает в камень всех существ перед вами на 5 секунд",
        "Right-click: turns the creatures in front of you to stone for 5 seconds"),
    "entity.mythsofworlds.satyr": ("Сатир", "Satyr"),
    "entity.mythsofworlds.harpy": ("Гарпия", "Harpy"),
    "entity.mythsofworlds.spartoi": ("Спарт", "Spartoi"),
    "entity.mythsofworlds.shade": ("Тень умершего", "Shade"),
    "entity.mythsofworlds.pegasus": ("Пегас", "Pegasus"),
    "entity.mythsofworlds.cyclops": ("Циклоп", "Cyclops"),
    "entity.mythsofworlds.medusa": ("Медуза Горгона", "Medusa"),
    "entity.mythsofworlds.medusa.petrify": ("Взгляд Медузы обращает вас в камень! Отвернитесь или поднимите щит",
                                            "Medusa's gaze is turning you to stone! Look away or raise a shield"),
    "entity.mythsofworlds.nemean_lion": ("Немейский лев", "Nemean Lion"),
    "entity.mythsofworlds.minotaur": ("Минотавр", "Minotaur"),
    "entity.mythsofworlds.hydra": ("Лернейская гидра", "Lernaean Hydra"),
    "entity.mythsofworlds.cerberus": ("Цербер", "Cerberus"),
    "entity.mythsofworlds.golden_hind": ("Керинейская лань", "Ceryneian Hind"),
    "entity.mythsofworlds.hydra_hatchling": ("Гидрёныш", "Hydra Hatchling"),
    "entity.mythsofworlds.greek_merchant": ("Торговец агоры", "Agora Merchant"),
}

MOB_NAMES_RU = {
    "satyr": "сатира", "harpy": "гарпии", "spartoi": "спарта", "shade": "тени умершего", "pegasus": "пегаса",
    "cyclops": "циклопа", "medusa": "Медузы Горгоны", "nemean_lion": "Немейского льва", "minotaur": "Минотавра",
    "hydra": "Лернейской гидры", "cerberus": "Цербера", "golden_hind": "Керинейской лани",
    "hydra_hatchling": "гидрёныша", "greek_merchant": "торговца агоры",
}


def lang():
    entries = dict(LANG)
    for name in MOBS:
        en = LANG[f"entity.{NS}.{name}"][1]
        entries[f"item.{NS}.{name}_spawn_egg"] = (f"Яйцо призыва {MOB_NAMES_RU[name]}", f"{en} Spawn Egg")
    for name, (ru, en) in ((n, (b["ru"], b["en"])) for n, b in BIOMES.items()):
        entries[f"biome.{NS}.{name}"] = (ru, en)
    for index, code in ((0, "ru_ru"), (1, "en_us")):
        path = assets("lang", f"{code}.json")
        with open(path, encoding="utf-8") as f:
            current = json.load(f)
        for key, values in entries.items():
            current[key] = values[index]
        write_json(path, current)


# ====================================================================== textures

def textures():
    import textures as tx
    rng = random.Random(2024)
    os.makedirs(assets("textures", "block"), exist_ok=True)
    os.makedirs(assets("textures", "item"), exist_ok=True)
    os.makedirs(assets("textures", "entity"), exist_ok=True)
    for name, fn in tx.BLOCKS.items():
        tx.save(fn(rng), assets("textures", "block", f"{name}.png"))
    with open(assets("textures", "block", "hellas_portal.png.mcmeta"), "w") as f:
        json.dump({"animation": {"frametime": 3, "interpolate": True}}, f, indent=2)
        f.write("\n")
    for name, fn in tx.ITEMS.items():
        tx.save(tx.item(fn, rng), assets("textures", "item", f"{name}.png"))
    for name, fn in tx.ENTITIES.items():
        tx.save(fn(rng), assets("textures", "entity", f"{name}.png"))


def main():
    write_json(data("dimension_type", "hellas.json"), dimension_type())
    write_json(data("dimension", "hellas.json"),
               dimension("hellas", multi_noise([(f"{NS}:{name}", spec["point"]) for name, spec in BIOMES.items()])))
    for name, (fixed_time, source) in STUB_DIMENSIONS.items():
        write_json(data("dimension_type", f"{name}.json"), dimension_type(fixed_time))
        write_json(data("dimension", f"{name}.json"), dimension(name, source))
    for name, spec in BIOMES.items():
        write_json(data("worldgen", "biome", f"{name}.json"), biome_json(spec))
    worldgen_features()
    worldgen_structures()
    loot()
    recipes()
    models()
    lang()
    if "--textures" in sys.argv:
        textures()


if __name__ == "__main__":
    main()
