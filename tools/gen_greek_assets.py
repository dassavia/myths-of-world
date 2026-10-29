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


# ---------------------------------------------------------------- surface of Hellas

def _block(name):
    return {"type": "minecraft:block", "result_state": {"Name": name}}


def _if(condition, then):
    return {"type": "minecraft:condition", "if_true": condition, "then_run": then}


def _seq(*rules):
    return {"type": "minecraft:sequence", "sequence": list(rules)}


def _biome(*names):
    return {"type": "minecraft:biome", "biome_is": [f"{NS}:{n}" for n in names]}


def _noise(lo, hi, noise="minecraft:surface"):
    return {"type": "minecraft:noise_threshold", "noise": noise, "min_threshold": lo, "max_threshold": hi}


def _above(y):
    return {"type": "minecraft:y_above", "anchor": {"absolute": y}, "surface_depth_multiplier": 0, "add_stone_depth": False}


FLOOR = {"type": "minecraft:stone_depth", "offset": 0, "surface_type": "floor", "add_surface_depth": False,
         "secondary_depth_range": 0}
UNDER_FLOOR = {"type": "minecraft:stone_depth", "offset": 0, "surface_type": "floor", "add_surface_depth": True,
               "secondary_depth_range": 0}
STEEP = {"type": "minecraft:steep"}
DRY = {"type": "minecraft:water", "offset": -1, "surface_depth_multiplier": 0, "add_stone_depth": False}
NOT_DRY = {"type": "minecraft:not", "invert": DRY}
MARBLE_BLOCK = f"{NS}:marble"


def hellas_surface():
    """Surface rules of Hellas, tried before the Overworld's: white limestone on every steep slope, marble
    mountains, sand beaches below the white cliffs, grey ash in the fields of the dead, black mud by the Styx."""
    living = ("elysian_fields", "arcadian_grove", "nemean_forest", "aegean_coast")
    return _if({"type": "minecraft:above_preliminary_surface"}, _seq(
        _if(_biome("olympus_peaks"), _seq(
            _if(FLOOR, _seq(
                _if(STEEP, _block("minecraft:calcite")),
                _if(_above(150), _seq(_if(_noise(-0.15, 0.15), _block("minecraft:calcite")), _block(MARBLE_BLOCK))),
                _if(_noise(0.45, 4.0), _block("minecraft:calcite")))),
            _if(UNDER_FLOOR, _seq(
                _if(STEEP, _block(MARBLE_BLOCK)),
                _if(_above(140), _block(MARBLE_BLOCK)))))),
        _if(_biome("aegean_sea"), _if(UNDER_FLOOR, _seq(_if(_noise(0.4, 4.0), _block("minecraft:gravel")), _block("minecraft:sand")))),
        _if(_biome("stygian_marsh"), _if(UNDER_FLOOR, _seq(_if(_noise(0.35, 4.0), _block("minecraft:soul_soil")), _block("minecraft:mud")))),
        _if(_biome("asphodel_meadows"), _if(FLOOR, _seq(
            _if(_noise(0.15, 4.0), _block("minecraft:soul_soil")),
            _if(_noise(-4.0, -0.3), _block("minecraft:gravel"))))),
        _if(_biome(*living), _seq(
            _if(FLOOR, _seq(
                _if(STEEP, _block("minecraft:calcite")),
                _if(_biome("aegean_coast"), _seq(
                    _if({"type": "minecraft:not", "invert": _above(66)}, _block("minecraft:sand")),
                    _if(_noise(0.4, 4.0), _block("minecraft:calcite")))),
                _if(_biome("nemean_forest"), _seq(
                    _if(_noise(0.2, 4.0), _block("minecraft:coarse_dirt")),
                    _if(_noise(-4.0, -0.45), _block("minecraft:rooted_dirt")))),
                _if(_biome("arcadian_grove"), _if(_noise(0.5, 4.0), _block("minecraft:podzol"))))),
            _if(UNDER_FLOOR, _seq(
                _if(STEEP, _block("minecraft:calcite")),
                _if(_biome("aegean_coast"), _if({"type": "minecraft:not", "invert": _above(65)}, _block("minecraft:sandstone")))))))))


def hellas_noise_settings():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vanilla", "overworld_noise_settings.json"),
              encoding="utf-8") as f:
        settings = json.load(f)
    settings["surface_rule"]["sequence"].insert(1, hellas_surface())
    write_json(data("worldgen", "noise_settings", "hellas.json"), settings)


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
    [f"{NS}:marble_ruin", f"{NS}:cloud_island"],
    [],
    ["minecraft:ore_dirt", "minecraft:ore_gravel", "minecraft:ore_granite_upper", "minecraft:ore_granite_lower",
     "minecraft:ore_diorite_upper", "minecraft:ore_diorite_lower", "minecraft:ore_andesite_upper",
     "minecraft:ore_andesite_lower", "minecraft:ore_tuff", "minecraft:ore_coal_upper", "minecraft:ore_coal_lower",
     "minecraft:ore_iron_upper", "minecraft:ore_iron_middle", "minecraft:ore_iron_small", "minecraft:ore_gold",
     "minecraft:ore_gold_lower", "minecraft:ore_redstone", "minecraft:ore_redstone_lower", "minecraft:ore_diamond",
     "minecraft:ore_diamond_medium", "minecraft:ore_diamond_large", "minecraft:ore_diamond_buried",
     "minecraft:ore_lapis", "minecraft:ore_lapis_buried", "minecraft:ore_copper", "minecraft:ore_emerald",
     f"{NS}:ore_marble", f"{NS}:olympus_marble", f"{NS}:olympus_calcite", f"{NS}:white_cliffs", "minecraft:disk_sand", "minecraft:disk_clay", "minecraft:disk_gravel"],
    [],
    ["minecraft:spring_water", "minecraft:spring_lava"],
    ["minecraft:glow_lichen", f"{NS}:asphodel_ash", f"{NS}:stygian_mud", f"{NS}:golden_apple_tree", f"{NS}:olive_tree", f"{NS}:olive_grove", f"{NS}:pomegranate_tree",
     f"{NS}:cypress_tree", f"{NS}:laurel_bush", f"{NS}:dead_trunk", f"{NS}:elysian_flowers", f"{NS}:maquis", "minecraft:trees_plains", "minecraft:trees_birch_and_oak", "minecraft:trees_savanna",
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


# The biomes are meant to look like the world of the myths, not like the Overworld: marble mountains under
# clouds for the gods, golden meadows of the blessed, groves of olive and cypress, the grey fields of the dead.
OLYMPUS_MUSIC = (f"{NS}:music.hellas.elysium", 6000, 18000)
UNDERWORLD_MUSIC = (f"{NS}:music.hellas.underworld", 6000, 18000)

BIOMES = {
    "olympus_peaks": {
        "ru": "Вершины Олимпа", "en": "Peaks of Olympus",
        "point": {"c": 0.5, "e": -0.8, "t": -0.2},
        "temperature": 0.3, "downfall": 0.4,
        "sky": 0xB4DCFF, "fog": 0xFFF6E2, "water": 0x55C8F0, "water_fog": 0x0A3A5A, "grass": 0xA8C98A, "foliage": 0x8FA27A,
        "particle": ("minecraft:end_rod", 0.0008), "music": OLYMPUS_MUSIC,
        "features": COMMON + [f"{NS}:marble_ruin", f"{NS}:cloud_island", f"{NS}:ore_marble", f"{NS}:olympus_marble",
                              f"{NS}:olympus_calcite", "minecraft:ore_emerald", f"{NS}:laurel_bush", f"{NS}:cypress_tree",
                              "minecraft:flower_meadow", "minecraft:patch_grass_plain"],
        "spawners": {
            "monster": [spawn(f"{NS}:harpy", 70, 1, 3), spawn("minecraft:skeleton", 20, 1, 2)],
            "creature": [spawn(f"{NS}:pegasus", 8, 1, 2), spawn("minecraft:goat", 8, 1, 3)],
        },
    },
    "elysian_fields": {
        "ru": "Елисейские поля", "en": "Elysian Fields",
        "point": {"c": 0.3, "e": 0.5, "t": 0.6, "h": -0.3},
        "temperature": 0.8, "downfall": 0.4,
        "sky": 0xFFE09A, "fog": 0xFFF1C9, "water": 0x7FE9FF, "water_fog": 0x0A4A5A, "grass": 0xE6CC5A, "foliage": 0xD9B84A,
        "particle": ("minecraft:end_rod", 0.003), "music": OLYMPUS_MUSIC,
        "features": COMMON + [f"{NS}:marble_ruin", f"{NS}:cloud_island", f"{NS}:golden_apple_tree", f"{NS}:olive_tree", f"{NS}:olive_grove", f"{NS}:pomegranate_tree",
                              f"{NS}:elysian_flowers", "minecraft:flower_meadow", "minecraft:patch_sunflower",
                              "minecraft:patch_grass_plain", "minecraft:patch_sugar_cane"],
        "spawners": {
            "monster": [spawn(f"{NS}:satyr", 20, 1, 2)],
            "creature": [spawn(f"{NS}:pegasus", 6, 1, 3), spawn(f"{NS}:golden_hind", 2, 1, 2), spawn("minecraft:sheep", 10, 2, 4),
                         spawn("minecraft:cow", 6, 2, 4), spawn("minecraft:horse", 4, 2, 4)],
        },
    },
    "arcadian_grove": {
        "ru": "Рощи Аркадии", "en": "Arcadian Grove",
        "point": {"c": 0.3, "e": 0.2, "t": 0.3, "h": 0.5},
        "temperature": 0.7, "downfall": 0.8,
        "sky": 0x8ECFFF, "fog": 0xCFE6FF, "water": 0x3FA0E4, "water_fog": 0x050533, "grass": 0x7FBF4A, "foliage": 0x8AA36A,
        "particle": ("minecraft:spore_blossom_air", 0.002),
        "features": COMMON + ["minecraft:amethyst_geode", "minecraft:forest_rock", f"{NS}:marble_ruin", f"{NS}:ore_marble",
                              f"{NS}:olive_tree", f"{NS}:olive_grove", f"{NS}:cypress_tree", f"{NS}:laurel_bush", f"{NS}:maquis",
                              "minecraft:flower_default", "minecraft:patch_grass_forest", "minecraft:patch_tall_grass_2",
                              "minecraft:patch_pumpkin"],
        "spawners": {
            "monster": [spawn(f"{NS}:satyr", 80, 2, 4), spawn("minecraft:spider", 30, 1, 2), spawn("minecraft:zombie", 20, 1, 3)],
            "creature": [spawn(f"{NS}:golden_hind", 3, 1, 2), spawn("minecraft:fox", 8, 2, 3), spawn("minecraft:sheep", 8, 2, 4),
                         spawn("minecraft:pig", 6, 2, 4), spawn("minecraft:wolf", 4, 2, 4), spawn("minecraft:rabbit", 4, 2, 3)],
        },
    },
    "asphodel_meadows": {
        "ru": "Асфоделевые луга", "en": "Asphodel Meadows",
        "point": {"c": 0.5, "e": 0.4, "t": -0.6, "h": -0.4, "w": 0.5},
        "temperature": 0.4, "downfall": 0.0, "precipitation": False,
        "sky": 0x5E636C, "fog": 0x6C7078, "water": 0x4A5A6A, "water_fog": 0x10181E, "grass": 0x8A9088, "foliage": 0x6E746C,
        "particle": ("minecraft:soul", 0.004), "music": UNDERWORLD_MUSIC,
        "additions": ("minecraft:ambient.soul_sand_valley.additions", 0.0111),
        "features": COMMON + ["minecraft:lake_lava_underground", f"{NS}:asphodel_ash", f"{NS}:pomegranate_tree", f"{NS}:dead_trunk",
                              f"{NS}:patch_asphodel", "minecraft:patch_dead_bush"],
        "spawners": {
            "monster": [spawn(f"{NS}:shade", 100, 1, 3), spawn(f"{NS}:spartoi", 60, 1, 3), spawn("minecraft:skeleton", 20, 1, 2)],
            "ambient": [spawn("minecraft:bat", 10, 8, 8)],
        },
    },
    "stygian_marsh": {
        "ru": "Стигийские топи", "en": "Stygian Marsh",
        "point": {"c": 0.15, "e": 0.8, "t": -0.3, "h": 0.7},
        "temperature": 0.6, "downfall": 0.9,
        "sky": 0x4E5A52, "fog": 0x3E4A42, "water": 0x1E2A24, "water_fog": 0x0A100C, "grass": 0x4C6040, "foliage": 0x3A4A30,
        "particle": ("minecraft:soul_fire_flame", 0.002), "music": UNDERWORLD_MUSIC,
        "additions": ("minecraft:ambient.basalt_deltas.additions", 0.0111),
        "features": COMMON + ["minecraft:disk_clay", f"{NS}:stygian_mud", f"{NS}:dead_trunk", "minecraft:trees_swamp",
                              "minecraft:brown_mushroom_swamp", "minecraft:patch_waterlily", "minecraft:seagrass_swamp"],
        "spawners": {
            "monster": [spawn(f"{NS}:shade", 80, 1, 2), spawn("minecraft:drowned", 30, 1, 2), spawn("minecraft:witch", 5, 1, 1)],
            "creature": [spawn("minecraft:frog", 10, 2, 5)],
        },
    },
    "aegean_coast": {
        "ru": "Эгейское побережье", "en": "Aegean Coast",
        "point": {"c": -0.1, "e": 0.3, "t": 0.5, "h": -0.2},
        "temperature": 0.9, "downfall": 0.3,
        "sky": 0x78C0FF, "fog": 0xD8EEFF, "water": 0x2FD8D0, "water_fog": 0x05313A, "grass": 0xA9C25A, "foliage": 0x8FA27A,
        "features": COMMON + DISKS + [f"{NS}:marble_ruin", f"{NS}:white_cliffs", f"{NS}:olive_tree", f"{NS}:olive_grove",
                                      f"{NS}:cypress_tree", f"{NS}:maquis", "minecraft:flower_default", "minecraft:patch_grass_plain", "minecraft:patch_dead_bush",
                                      "minecraft:patch_sugar_cane", "minecraft:seagrass_warm", "minecraft:sea_pickle"],
        "spawners": {
            "monster": [spawn(f"{NS}:harpy", 40, 1, 3), spawn("minecraft:drowned", 30, 1, 2), spawn("minecraft:zombie", 20, 1, 2)],
            "creature": [spawn("minecraft:turtle", 5, 2, 5), spawn("minecraft:goat", 4, 1, 2)],
            "water_creature": [spawn("minecraft:squid", 4, 1, 4)],
            "water_ambient": [spawn("minecraft:tropical_fish", 25, 8, 8)],
        },
    },
    # Home of the pride of lions, and of the Nemean Lion in its den: a dry open forest of olive, oak and cypress
    # on golden grass.
    "nemean_forest": {
        "ru": "Немейский лес", "en": "Nemean Forest",
        "point": {"c": 0.45, "e": 0.0, "t": 0.45, "h": 0.15},
        "temperature": 1.2, "downfall": 0.2, "precipitation": False,
        "sky": 0x8CC8FF, "fog": 0xE8DDB8, "water": 0x3FA0C4, "water_fog": 0x05313A, "grass": 0xC4B04A, "foliage": 0x9AA048,
        "particle": ("minecraft:white_ash", 0.0015),
        "features": COMMON + ["minecraft:forest_rock", f"{NS}:marble_ruin", f"{NS}:ore_marble", f"{NS}:olive_tree",
                              f"{NS}:olive_grove", f"{NS}:cypress_tree", f"{NS}:maquis", "minecraft:trees_savanna",
                              "minecraft:trees_birch_and_oak", "minecraft:flower_default", "minecraft:patch_grass_forest",
                              "minecraft:patch_tall_grass_2", "minecraft:patch_dead_bush"],
        "spawners": {
            "monster": [spawn(f"{NS}:satyr", 40, 1, 3), spawn("minecraft:spider", 20, 1, 2)],
            "creature": [spawn(f"{NS}:lion", 14, 2, 4), spawn("minecraft:sheep", 8, 2, 4), spawn("minecraft:goat", 6, 1, 3),
                         spawn("minecraft:rabbit", 6, 2, 3), spawn(f"{NS}:golden_hind", 1, 1, 1)],
        },
    },
    "aegean_sea": {
        "ru": "Эгейское море", "en": "Aegean Sea",
        "point": {"c": -0.6, "t": 0.5},
        "temperature": 0.8, "downfall": 0.5,
        "sky": 0x6AB4FF, "fog": 0xD0E8FF, "water": 0x2FD8D0, "water_fog": 0x05313A, "grass": 0xA9C25A, "foliage": 0x8FA27A,
        "features": COMMON + DISKS + ["minecraft:seagrass_warm", "minecraft:sea_pickle", "minecraft:warm_ocean_vegetation"],
        "spawners": {
            "monster": [spawn("minecraft:drowned", 100, 1, 3)],
            "water_creature": [spawn("minecraft:dolphin", 4, 1, 3), spawn("minecraft:squid", 4, 1, 4)],
            "water_ambient": [spawn("minecraft:tropical_fish", 25, 8, 8), spawn("minecraft:pufferfish", 5, 1, 3)],
        },
    },
}


def biome_json(spec, order=None):
    order = order or FEATURE_ORDER
    used = set(spec["features"])
    unknown = used - {f for step in order for f in step}
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
    if "music" in spec:
        sound, min_delay, max_delay = spec["music"]
        effects["music"] = {"sound": sound, "min_delay": min_delay, "max_delay": max_delay, "replace_current_music": False}
    if "additions" in spec:
        sound, chance = spec["additions"]
        effects["additions_sound"] = {"sound": sound, "tick_chance": chance}
    return {
        "has_precipitation": spec.get("precipitation", True),
        "temperature": spec["temperature"],
        "downfall": spec["downfall"],
        "effects": effects,
        "spawners": spec["spawners"],
        "spawn_costs": {},
        "carvers": {"air": ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"]},
        "features": [[f for f in step if f in used] for step in order],
    }


def ore(name, block, size, count, lo, hi, rarity=None):
    write_json(data("worldgen", "configured_feature", f"{name}.json"), {
        "type": "minecraft:ore",
        "config": {"size": size, "discard_chance_on_air_exposure": 0.0, "targets": [{
            "target": {"predicate_type": "minecraft:tag_match", "tag": "minecraft:stone_ore_replaceables"},
            "state": {"Name": block}}]},
    })
    placement = [{"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
                 {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": lo},
                                                               "max_inclusive": {"absolute": hi}}},
                 {"type": "minecraft:biome"}]
    if rarity:
        placement.insert(0, {"type": "minecraft:rarity_filter", "chance": rarity})
    write_json(data("worldgen", "placed_feature", f"{name}.json"), {"feature": f"{NS}:{name}", "placement": placement})


SAPLING_OK = {"type": "minecraft:block_predicate_filter",
              "predicate": {"type": "minecraft:would_survive", "state": {"Name": "minecraft:oak_sapling", "Properties": {"stage": "0"}}}}


def surface_placement(count=None, rarity=None, extra=None):
    placement = []
    if rarity:
        placement.append({"type": "minecraft:rarity_filter", "chance": rarity})
    if count:
        placement.append({"type": "minecraft:count", "count": count})
    placement += [{"type": "minecraft:in_square"}, {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 0},
                  {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR"}]
    placement += extra or []
    placement.append({"type": "minecraft:biome"})
    return placement


def state(name, **props):
    s = {"Name": name}
    if props:
        s["Properties"] = {k: str(v).lower() for k, v in props.items()}
    return s


def simple(name, **props):
    return {"type": "minecraft:simple_state_provider", "state": state(name, **props)}


def tree(name, log, leaves, trunk, foliage, count=None, rarity=None, dirt="minecraft:dirt", fruit=False, placement=None):
    if fruit:
        # Fruit trees grow with some of their fruit already ripe.
        foliage_provider = {"type": "minecraft:weighted_state_provider", "entries": [
            {"weight": 3, "data": state(leaves, age=0, distance=7, persistent=False, waterlogged=False)},
            {"weight": 1, "data": state(leaves, age=3, distance=7, persistent=False, waterlogged=False)}]}
    else:
        foliage_provider = simple(leaves, distance=7, persistent=False, waterlogged=False)
    write_json(data("worldgen", "configured_feature", f"{name}.json"), {
        "type": "minecraft:tree",
        "config": {
            "trunk_provider": simple(log, axis="y"),
            "foliage_provider": foliage_provider,
            "dirt_provider": simple(dirt),
            "trunk_placer": trunk,
            "foliage_placer": foliage,
            "minimum_size": {"type": "minecraft:two_layers_feature_size", "limit": 1, "lower_size": 0, "upper_size": 1},
            "decorators": [],
            "ignore_vines": True,
            "force_dirt": False,
        },
    })
    write_json(data("worldgen", "placed_feature", f"{name}.json"),
               {"feature": f"{NS}:{name}", "placement": placement or surface_placement(count, rarity, [SAPLING_OK])})


def hellas_features():
    # Olympus is a mountain of marble: huge veins of marble and calcite all the way to the peaks.
    ore("olympus_marble", f"{NS}:marble", 64, 28, 50, 320)
    ore("olympus_calcite", "minecraft:calcite", 48, 12, 60, 320)
    # The chalk-white cliffs of the Aegean.
    ore("white_cliffs", "minecraft:calcite", 40, 10, 55, 120)

    # Olive: short, gnarled, forking trunk with a wide silvery crown.
    olive_trunk = {"type": "minecraft:forking_trunk_placer", "base_height": 3, "height_rand_a": 2, "height_rand_b": 1}
    olive_crown = {"type": "minecraft:acacia_foliage_placer", "radius": 2, "offset": 0}
    tree("olive_tree", "minecraft:oak_log", f"{NS}:olive_leaves", olive_trunk, olive_crown, count=1, fruit=True)
    # Olive groves: patches where many olive trees stand together, as on the hills of Attica.
    tree("olive_grove", "minecraft:oak_log", f"{NS}:olive_leaves", olive_trunk, olive_crown, fruit=True,
         placement=[{"type": "minecraft:rarity_filter", "chance": 6}, {"type": "minecraft:count", "count": 8}] +
         surface_placement(extra=[SAPLING_OK]))
    # Pomegranate of Persephone: a small round tree with red fruit.
    tree("pomegranate_tree", "minecraft:dark_oak_log", f"{NS}:pomegranate_leaves",
         {"type": "minecraft:straight_trunk_placer", "base_height": 2, "height_rand_a": 1, "height_rand_b": 0},
         {"type": "minecraft:blob_foliage_placer", "radius": 2, "offset": 0, "height": 2}, rarity=3, fruit=True)
    # Maquis: the low, thick, sweet-smelling scrub of the Mediterranean hills.
    write_json(data("worldgen", "configured_feature", "maquis.json"), {"type": "minecraft:random_patch", "config": {
        "tries": 24, "xz_spread": 5, "y_spread": 2, "feature": {"feature": {"type": "minecraft:simple_block", "config": {
            "to_place": {"type": "minecraft:weighted_state_provider", "entries": [
                {"weight": 4, "data": state("minecraft:azalea_leaves", distance=1, persistent=True, waterlogged=False)},
                {"weight": 2, "data": state("minecraft:oak_leaves", distance=1, persistent=True, waterlogged=False)},
                {"weight": 2, "data": state("minecraft:sweet_berry_bush", age=3)},
                {"weight": 1, "data": state("minecraft:flowering_azalea_leaves", distance=1, persistent=True, waterlogged=False)},
                {"weight": 2, "data": state("minecraft:short_grass")}]}}},
            "placement": [{"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:all_of", "predicates": [
                {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
                {"type": "minecraft:matching_blocks", "offset": [0, -1, 0], "blocks": ["minecraft:grass_block", "minecraft:coarse_dirt",
                                                                                   "minecraft:dirt", "minecraft:podzol"]}]}}]}}})
    write_json(data("worldgen", "placed_feature", "maquis.json"), {"feature": f"{NS}:maquis", "placement": [
        {"type": "minecraft:count", "count": 2}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]})
    # Cypress: a tall dark-green spire.
    tree("cypress_tree", "minecraft:spruce_log", "minecraft:spruce_leaves",
         {"type": "minecraft:straight_trunk_placer", "base_height": 7, "height_rand_a": 4, "height_rand_b": 0},
         {"type": "minecraft:spruce_foliage_placer", "radius": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": 1},
          "offset": 0, "trunk_height": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": 2}}, rarity=2)
    # Laurel of Apollo: a low round bush.
    tree("laurel_bush", "minecraft:oak_log", "minecraft:azalea_leaves",
         {"type": "minecraft:straight_trunk_placer", "base_height": 1, "height_rand_a": 0, "height_rand_b": 0},
         {"type": "minecraft:bush_foliage_placer", "radius": 2, "offset": 1, "height": 2}, count=2)
    # The golden apple trees of the Hesperides: white trunks, glowing golden leaves.
    tree("golden_apple_tree", "minecraft:birch_log", f"{NS}:golden_leaves",
         {"type": "minecraft:straight_trunk_placer", "base_height": 5, "height_rand_a": 2, "height_rand_b": 0},
         {"type": "minecraft:blob_foliage_placer", "radius": 2, "offset": 0, "height": 3}, rarity=2)

    for name, rarity in (("cloud_island", 5), ("marble_ruin", 3)):
        write_json(data("worldgen", "configured_feature", f"{name}.json"), {"type": f"{NS}:{name}", "config": {}})
    write_json(data("worldgen", "placed_feature", "cloud_island.json"), {"feature": f"{NS}:cloud_island", "placement": [
        {"type": "minecraft:rarity_filter", "chance": 5}, {"type": "minecraft:in_square"},
        {"type": "minecraft:height_range", "height": {"type": "minecraft:uniform", "min_inclusive": {"absolute": 150},
                                                      "max_inclusive": {"absolute": 200}}},
        {"type": "minecraft:biome"}]})
    write_json(data("worldgen", "placed_feature", "marble_ruin.json"), {"feature": f"{NS}:marble_ruin", "placement": [
        {"type": "minecraft:rarity_filter", "chance": 3}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"}, {"type": "minecraft:biome"}]})

    # Fields of the dead: grey soul soil and coarse earth among the asphodels.
    def patch(name, ground, vegetation, count, chance):
        write_json(data("worldgen", "configured_feature", f"{name}.json"), {
            "type": "minecraft:vegetation_patch",
            "config": {
                "replaceable": "#minecraft:moss_replaceable",
                "ground_state": {"type": "minecraft:weighted_state_provider",
                                 "entries": [{"weight": w, "data": state(b)} for b, w in ground]},
                "vegetation_feature": {"feature": {"type": "minecraft:simple_block", "config": {"to_place": vegetation}},
                                       "placement": []},
                "surface": "floor", "depth": 1, "extra_bottom_block_chance": 0.0, "vertical_range": 5,
                "vegetation_chance": chance, "xz_radius": {"type": "minecraft:uniform", "min_inclusive": 3, "max_inclusive": 7},
                "extra_edge_column_chance": 0.3,
            },
        })
        write_json(data("worldgen", "placed_feature", f"{name}.json"), {"feature": f"{NS}:{name}", "placement": [
            {"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
            {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"}, {"type": "minecraft:biome"}]})

    patch("asphodel_ash", [("minecraft:soul_soil", 3), ("minecraft:coarse_dirt", 2), ("minecraft:gravel", 1)],
          simple(f"{NS}:asphodel"), 4, 0.25)
    patch("stygian_mud", [("minecraft:mud", 4), ("minecraft:soul_soil", 1)],
          {"type": "minecraft:weighted_state_provider", "entries": [
              {"weight": 3, "data": state("minecraft:dead_bush")}, {"weight": 1, "data": state("minecraft:brown_mushroom")}]}, 3, 0.1)

    # Bare black trunks of trees that died with the light.
    write_json(data("worldgen", "configured_feature", "dead_trunk.json"), {"type": "minecraft:block_column", "config": {
        "layers": [{"height": {"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 5},
                    "provider": simple("minecraft:stripped_dark_oak_log", axis="y")}],
        "direction": "up", "allowed_placement": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
        "prioritize_tip": False}})
    write_json(data("worldgen", "placed_feature", "dead_trunk.json"),
               {"feature": f"{NS}:dead_trunk", "placement": surface_placement(rarity=2, extra=[SAPLING_OK])})

    # Meadows of the blessed: white, blue and gold flowers everywhere.
    write_json(data("worldgen", "configured_feature", "elysian_flowers.json"), {"type": "minecraft:flower", "config": {
        "tries": 96, "xz_spread": 7, "y_spread": 3, "feature": {"feature": {"type": "minecraft:simple_block", "config": {
            "to_place": {"type": "minecraft:weighted_state_provider", "entries": [
                {"weight": w, "data": state(f)} for f, w in (
                    ("minecraft:oxeye_daisy", 3), ("minecraft:lily_of_the_valley", 3), ("minecraft:dandelion", 2),
                    ("minecraft:azure_bluet", 2), ("minecraft:cornflower", 1), (f"{NS}:asphodel", 1))]}}},
            "placement": [{"type": "minecraft:block_predicate_filter",
                           "predicate": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}}]}}})
    write_json(data("worldgen", "placed_feature", "elysian_flowers.json"), {"feature": f"{NS}:elysian_flowers", "placement": [
        {"type": "minecraft:count", "count": 4}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"}, {"type": "minecraft:biome"}]})


def worldgen_features():
    hellas_features()
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
# Spacing is in chunks. The lairs of the bosses and mini-bosses share one structure set (LAIRS below), so there is at
# most one lair per cell of that grid and two lairs are never closer than its separation, however far from spawn.
STRUCTURES = {
    "greek_temple": (["olympus_peaks", "elysian_fields"], 56, 20, 1450201, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "oracle_of_delphi": (["arcadian_grove", "olympus_peaks"], 48, 16, 1450202, "WORLD_SURFACE_WG", 0, "beard_thin"),
    # Underground: only the propylon on top of the 21-block-deep template shows above the ground.
    "labyrinth": (["elysian_fields", "aegean_coast", "arcadian_grove"], 0, 0, 0, "WORLD_SURFACE_WG", -21, "none"),
    "gates_of_hades": (["asphodel_meadows"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "hydra_lair": (["stygian_marsh"], 0, 0, 0, "WORLD_SURFACE_WG", -2, "beard_thin"),
    "medusa_lair": (["aegean_coast"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "cyclops_cave": (["olympus_peaks", "aegean_coast", "arcadian_grove"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "nemean_lion_den": (["nemean_forest"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "themiscyra": (["elysian_fields", "arcadian_grove", "aegean_coast"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    # The agora is the hub of Hellas, so it stays the most common big structure.
    "agora": (["elysian_fields", "arcadian_grove", "aegean_coast"], 32, 12, 1450209, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "ship_of_theseus": (["aegean_sea"], 44, 14, 1450210, "WORLD_SURFACE_WG", -3, "none"),
    "perseus_refuge": (["aegean_coast", "olympus_peaks"], 44, 14, 1450211, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "amazon_camp": (["elysian_fields", "arcadian_grove", "aegean_coast", "nemean_forest"], 36, 14, 1450212,
                    "WORLD_SURFACE_WG", 0, "beard_thin"),
    "greek_farmstead": (["elysian_fields", "arcadian_grove", "aegean_coast", "nemean_forest"], 14, 5, 1450213,
                        "WORLD_SURFACE_WG", 0, "beard_thin"),
}
LAIRS = {"structures": {"labyrinth": 3, "gates_of_hades": 3, "hydra_lair": 3, "medusa_lair": 3, "cyclops_cave": 3,
                        "nemean_lion_den": 3, "themiscyra": 2},
         "spacing": 56, "separation": 36, "salt": 1450300}

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
    "amazon_camp": ("Лагерь амазонок", "Amazon Camp"),
    "themiscyra": ("Фемискира", "Themiscyra"),
    "greek_farmstead": ("Усадьба", "Farmstead"),
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
        set_path = data("worldgen", "structure_set", f"{name}.json")
        if name in LAIRS["structures"]:
            if os.path.exists(set_path):  # each lair had its own set before 0.4
                os.remove(set_path)
            continue
        write_json(set_path, {
            "structures": [{"structure": f"{NS}:{name}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
        })
    write_json(data("worldgen", "structure_set", "greek_lairs.json"), {
        "structures": [{"structure": f"{NS}:{name}", "weight": w} for name, w in LAIRS["structures"].items()],
        "placement": {"type": "minecraft:random_spread", "spacing": LAIRS["spacing"], "separation": LAIRS["separation"],
                      "salt": LAIRS["salt"]},
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
        entry(f"{NS}:promethean_torch", 2), entry(f"{NS}:necklace_of_harmonia", 1),
    ])
    chest("oracle_of_delphi", (2, 5), [
        entry("minecraft:glass_bottle", 6, 1, 3), entry("minecraft:glowstone_dust", 6, 1, 4), entry("minecraft:amethyst_shard", 6, 1, 4),
        entry("minecraft:ender_eye", 2), entry("minecraft:book", 5, enchant=True), entry(f"{NS}:ambrosia", 3),
        entry("minecraft:experience_bottle", 4, 1, 3),
    ])
    chest("labyrinth", (4, 8), gold + [
        entry("minecraft:iron_ingot", 8, 2, 6), entry("minecraft:diamond", 3, 1, 2), entry("minecraft:string", 6, 4, 12),
        entry("minecraft:iron_sword", 3, enchant=True), entry("minecraft:golden_apple", 3), entry(f"{NS}:ambrosia", 2),
        entry(f"{NS}:necklace_of_harmonia", 1),
    ])
    chest("gates_of_hades", (4, 7), [
        entry("minecraft:soul_lantern", 4, 1, 3), entry("minecraft:obsidian", 6, 2, 6), entry("minecraft:diamond", 4, 1, 3),
        entry("minecraft:netherite_scrap", 1), entry("minecraft:gold_ingot", 6, 2, 6), entry("minecraft:book", 4, enchant=True),
        entry("minecraft:enchanted_golden_apple", 1), entry(f"{NS}:necklace_of_harmonia", 1),
    ])
    chest("hydra_lair", (3, 6), gold + [
        entry("minecraft:slime_ball", 6, 1, 4), entry("minecraft:emerald", 4, 1, 4), entry("minecraft:diamond", 3, 1, 2),
        entry("minecraft:book", 4, enchant=True), entry("minecraft:golden_apple", 3), entry(f"{NS}:necklace_of_harmonia", 1),
    ])
    chest("medusa_lair", (3, 6), gold + [
        entry("minecraft:shield", 4), entry("minecraft:prismarine_shard", 6, 2, 6), entry("minecraft:heart_of_the_sea", 1),
        entry("minecraft:book", 4, enchant=True), entry("minecraft:emerald", 4, 1, 3), entry(f"{NS}:necklace_of_harmonia", 1),
    ])
    chest("cyclops_cave", (3, 6), [
        entry("minecraft:white_wool", 8, 2, 6), entry("minecraft:mutton", 8, 2, 5), entry("minecraft:iron_ingot", 6, 2, 5),
        entry("minecraft:anvil", 1), entry("minecraft:iron_axe", 3, enchant=True), entry("minecraft:gold_ingot", 4, 1, 4),
    ])
    chest("nemean_lion_den", (2, 5), [
        entry("minecraft:bone", 10, 2, 6), entry("minecraft:leather", 8, 1, 4), entry("minecraft:gold_ingot", 5, 1, 4),
        entry("minecraft:book", 3, enchant=True), entry("minecraft:golden_apple", 2),
    ])

    shears_or_silk = {"condition": "minecraft:any_of", "terms": [
        {"condition": "minecraft:match_tool", "predicate": {"items": "minecraft:shears"}},
        {"condition": "minecraft:match_tool", "predicate": {"predicates": {"minecraft:enchantments": [
            {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]}
    write_json(data("loot_table", "blocks", "golden_leaves.json"), {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{"type": "minecraft:alternatives", "children": [
            {"type": "minecraft:item", "name": f"{NS}:golden_leaves", "conditions": [shears_or_silk]},
            {"type": "minecraft:item", "name": "minecraft:golden_apple",
             "conditions": [{"condition": "minecraft:random_chance", "chance": 0.04}]},
            {"type": "minecraft:item", "name": "minecraft:gold_nugget",
             "conditions": [{"condition": "minecraft:random_chance", "chance": 0.15}]}]}]}],
        "random_sequence": f"{NS}:blocks/golden_leaves",
    })
    write_json(data("loot_table", "blocks", "cloud.json"), {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{NS}:cloud"}]}],
        "random_sequence": f"{NS}:blocks/cloud",
    })
    chest("cloud_shrine", (3, 6), gold + [
        entry(f"{NS}:ambrosia", 6, 1, 3), entry("minecraft:golden_apple", 4), entry("minecraft:enchanted_golden_apple", 1),
        entry("minecraft:feather", 6, 2, 6), entry(f"{NS}:harpy_feather", 4, 1, 3), entry("minecraft:book", 4, enchant=True),
        entry(f"{NS}:cloud", 5, 4, 12),
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

    for leaves, fruit in (("olive_leaves", "olives"), ("pomegranate_leaves", "pomegranate")):
        write_json(data("loot_table", "blocks", f"{leaves}.json"), {
            "type": "minecraft:block",
            "pools": [
                {"rolls": 1, "entries": [{"type": "minecraft:alternatives", "children": [
                    {"type": "minecraft:item", "name": f"{NS}:{leaves}", "conditions": [shears_or_silk]},
                    {"type": "minecraft:item", "name": f"{NS}:{fruit}", "conditions": [
                        {"condition": "minecraft:block_state_property", "block": f"{NS}:{leaves}", "properties": {"age": "3"}}]},
                    {"type": "minecraft:item", "name": "minecraft:stick",
                     "conditions": [{"condition": "minecraft:random_chance", "chance": 0.04}]}]}]}],
            "random_sequence": f"{NS}:blocks/{leaves}",
        })
    chest("amazon_camp", (3, 6), [
        entry("minecraft:arrow", 8, 4, 16), entry("minecraft:leather", 8, 2, 6), entry("minecraft:iron_ingot", 6, 1, 4),
        entry("minecraft:bow", 3, enchant=True), entry("minecraft:iron_sword", 3, enchant=True), entry("minecraft:cooked_mutton", 6, 2, 5),
        entry("minecraft:saddle", 2), entry(f"{NS}:wedding_ring", 1),
    ])
    chest("themiscyra", (4, 7), gold + [
        entry("minecraft:emerald", 6, 2, 6), entry("minecraft:diamond", 3, 1, 3), entry("minecraft:golden_horse_armor", 2),
        entry("minecraft:book", 4, enchant=True), entry("minecraft:golden_apple", 3), entry(f"{NS}:ambrosia", 3),
        entry(f"{NS}:wedding_ring", 2),
    ])
    chest("greek_farmstead", (3, 6), [
        entry(f"{NS}:olives", 10, 2, 8), entry(f"{NS}:pomegranate", 4, 1, 3), entry("minecraft:bread", 8, 1, 4),
        entry("minecraft:honey_bottle", 6, 1, 3), entry("minecraft:honeycomb", 6, 1, 4), entry("minecraft:wheat", 8, 2, 8),
        entry("minecraft:white_wool", 5, 1, 4), entry("minecraft:emerald", 3, 1, 2),
    ])
    mob("lion", [("minecraft:leather", 0, 2, None), ("minecraft:beef", 1, 3, None)])
    mob("karkinos", [(f"{NS}:karkinos_claw", 1, 2, None), ("minecraft:cod", 2, 5, None), ("minecraft:prismarine_shard", 1, 4, None)])
    mob("amazon", [])
    mob("hippolyta", [("minecraft:gold_ingot", 4, 9, None), ("minecraft:diamond", 1, 2, None)])
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
    write_json(data("recipe", "wings_of_daedalus.json"), {
        "type": "minecraft:crafting_shaped", "category": "equipment",
        "pattern": ["HFH", "FFF", "F F"], "key": {"H": {"item": "minecraft:honeycomb"}, "F": {"item": f"{NS}:harpy_feather"}},
        "result": {"id": f"{NS}:wings_of_daedalus", "count": 1},
    })
    write_json(data("recipe", "wedding_ring.json"), {
        "type": "minecraft:crafting_shaped", "category": "misc",
        "pattern": [" D ", "G G", " G "], "key": {"D": {"item": "minecraft:diamond"}, "G": {"item": "minecraft:gold_ingot"}},
        "result": {"id": f"{NS}:wedding_ring", "count": 1},
    })
    write_json(data("recipe", "horn_of_themiscyra.json"), {
        "type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": [{"item": "minecraft:goat_horn"}, {"item": "minecraft:gold_ingot"}, {"item": "minecraft:leather"}],
        "result": {"id": f"{NS}:horn_of_themiscyra", "count": 1},
    })
    write_json(data("tags", "worldgen", "structure", "amazon_homes.json"),
               {"replace": False, "values": [f"{NS}:amazon_camp", f"{NS}:themiscyra"]})
    write_json(data("recipe", "greek_journal.json"), {
        "type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": [{"item": "minecraft:book"}, {"item": "minecraft:feather"}, {"item": "minecraft:gold_nugget"}],
        "result": {"id": f"{NS}:greek_journal", "count": 1},
    })
    add_tag("block", "mineable/pickaxe", ["marble", "marble_bricks", "marble_pillar", "olympian_marble", "brazier"])
    fruit_leaves = ["golden_leaves", "olive_leaves", "pomegranate_leaves"]
    add_tag("block", "leaves", fruit_leaves)
    add_tag("block", "mineable/hoe", fruit_leaves)
    add_tag("block", "mineable/shovel", ["cloud"])
    add_tag("item", "leaves", fruit_leaves)
    add_tag("block", "small_flowers", ["asphodel"])
    add_tag("item", "small_flowers", ["asphodel"])


def add_tag(kind, name, values, namespace="minecraft"):
    """Adds mod entries to a tag file, keeping what other scripts (gen_norse_assets.py) put there."""
    path = os.path.join(ROOT, "data", namespace, "tags", kind, f"{name}.json")
    tag = {"replace": False, "values": []}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            tag = json.load(f)
    for value in values:
        if f"{NS}:{value}" not in tag["values"]:
            tag["values"].append(f"{NS}:{value}")
    write_json(path, tag)


# ====================================================================== models

ITEMS = ["promethean_torch", "ambrosia", "harpy_feather", "minotaur_horn", "hydra_scale", "cerberus_fang",
         "nemean_pelt", "cyclops_eye", "medusa_head", "nemean_claw", "nemean_claw_dagger", "harpe", "hydra_egg",
         "olives", "pomegranate", "wings_of_daedalus", "karkinos_claw", "girdle_of_hippolyta", "wedding_ring",
         "necklace_of_harmonia", "horn_of_themiscyra",
         "greek_journal", "greek_journal_complete"]
HANDHELD = {"promethean_torch", "nemean_claw_dagger", "harpe"}
MOBS = ["satyr", "harpy", "spartoi", "shade", "pegasus", "golden_hind", "hydra_hatchling", "greek_merchant",
        "cyclops", "medusa", "nemean_lion", "minotaur", "hydra", "cerberus", "lion", "amazon", "karkinos", "hippolyta"]


def models():
    for leaves in ("olive_leaves", "pomegranate_leaves"):
        write_json(assets("blockstates", f"{leaves}.json"), {"variants": {
            f"age={age}": {"model": f"{NS}:block/{leaves}" + ("_ripe" if age == 3 else "")} for age in range(4)}})
        for suffix in ("", "_ripe"):
            write_json(assets("models", "block", f"{leaves}{suffix}.json"), {
                "parent": "minecraft:block/cube_all", "render_type": "minecraft:cutout_mipped",
                "textures": {"all": f"{NS}:block/{leaves}{suffix}"}})
        write_json(assets("models", "item", f"{leaves}.json"), {"parent": f"{NS}:block/{leaves}_ripe"})
    for block in ("marble", "marble_bricks", "olympian_marble", "labyrinth_bricks", "mossy_labyrinth_bricks",
                  "cracked_labyrinth_bricks"):
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

    write_json(assets("blockstates", "cloud.json"), {"variants": {"": {"model": f"{NS}:block/cloud"}}})
    write_json(assets("models", "block", "cloud.json"), {"parent": "minecraft:block/cube_all", "render_type": "minecraft:translucent",
                                                         "textures": {"all": f"{NS}:block/cloud"}})
    write_json(assets("models", "item", "cloud.json"), {"parent": f"{NS}:block/cloud"})
    # Golden leaves are not tinted by the biome, so they use cube_all rather than the leaves parent.
    write_json(assets("blockstates", "golden_leaves.json"), {"variants": {"": {"model": f"{NS}:block/golden_leaves"}}})
    write_json(assets("models", "block", "golden_leaves.json"), {"parent": "minecraft:block/cube_all",
                                                                 "render_type": "minecraft:cutout_mipped",
                                                                 "textures": {"all": f"{NS}:block/golden_leaves"}})
    write_json(assets("models", "item", "golden_leaves.json"), {"parent": f"{NS}:block/golden_leaves"})

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
    "block.mythsofworlds.cloud": ("Облако", "Cloud"),
    "block.mythsofworlds.golden_leaves": ("Листва золотой яблони", "Golden Apple Leaves"),
    "block.mythsofworlds.asphodel": ("Асфодель", "Asphodel"),
    "block.mythsofworlds.labyrinth_bricks": ("Кирпичи лабиринта", "Labyrinth Bricks"),
    "block.mythsofworlds.mossy_labyrinth_bricks": ("Замшелые кирпичи лабиринта", "Mossy Labyrinth Bricks"),
    "block.mythsofworlds.cracked_labyrinth_bricks": ("Потрескавшиеся кирпичи лабиринта", "Cracked Labyrinth Bricks"),
    "block.mythsofworlds.olive_leaves": ("Листва оливы", "Olive Leaves"),
    "block.mythsofworlds.pomegranate_leaves": ("Листва граната", "Pomegranate Leaves"),
    "item.mythsofworlds.olives": ("Оливки", "Olives"),
    "item.mythsofworlds.pomegranate": ("Гранат", "Pomegranate"),
    "item.mythsofworlds.wings_of_daedalus": ("Крылья Дедала", "Wings of Daedalus"),
    "item.mythsofworlds.wings_of_daedalus.desc": (
        "Надеваются вместо нагрудника: высокий прыжок и плавное падение. Не поднимайтесь к солнцу выше 200 блоков: воск тает",
        "Worn in the chest slot: a very high jump and a gentle glide down. Do not fly above y 200 in the sun: the wax melts"),
    "item.mythsofworlds.wings_of_daedalus.melting": ("Солнце растапливает воск ваших крыльев!", "The sun is melting the wax of your wings!"),
    "item.mythsofworlds.karkinos_claw": ("Клешня Каркина", "Claw of Karkinos"),
    "item.mythsofworlds.girdle_of_hippolyta": ("Пояс Ипполиты", "Girdle of Hippolyta"),
    "item.mythsofworlds.girdle_of_hippolyta.desc": ("Надевается вместо поножей: сила II, стойкость II, скорость и регенерация",
                                                    "Worn in the legs slot: Strength II, Resistance II, Speed and Regeneration"),
    "item.mythsofworlds.necklace_of_harmonia": ("Ожерелье Гармонии", "Necklace of Harmonia"),
    "item.mythsofworlds.horn_of_themiscyra": ("Горн Фемискиры", "Horn of Themiscyra"),
    "item.mythsofworlds.horn_of_themiscyra.desc": ("ПКМ: амазонки вокруг возвращаются в свой лагерь",
                                                   "Right-click: the amazons around go back to their camp"),
    "item.mythsofworlds.horn_of_themiscyra.called": ("Горн трубит. Возвращаются домой: %s", "The horn sounds. Going home: %s"),
    "item.mythsofworlds.wedding_ring": ("Обручальное кольцо", "Wedding Ring"),
    "item.mythsofworlds.greek_journal": ("Журнал героя Эллады", "Hero's Journal of Hellas"),
    "item.mythsofworlds.greek_journal_complete": ("Полный журнал героя Эллады", "Complete Hero's Journal of Hellas"),
    "item.mythsofworlds.journal.desc": ("Записи появляются, когда вы встречаете существ и находите места",
                                        "Entries appear as you meet creatures and find places"),
    "item.mythsofworlds.journal.complete": ("Все записи уже на месте", "Every entry is already written"),
    "entity.mythsofworlds.lion": ("Лев", "Lion"),
    "entity.mythsofworlds.amazon": ("Амазонка", "Amazon"),
    "entity.mythsofworlds.karkinos": ("Каркин", "Karkinos"),
    "entity.mythsofworlds.hippolyta": ("Ипполита", "Hippolyta"),
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
    "entity.mythsofworlds.medusa.petrify": ("Взгляд Медузы обращает вас в камень! Отвернитесь, поднимите щит или наденьте тыкву",
                                            "Medusa's gaze is turning you to stone! Look away, raise a shield or wear a pumpkin"),
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
    "hydra_hatchling": "гидрёныша", "greek_merchant": "торговца агоры", "lion": "льва", "amazon": "амазонки",
    "karkinos": "Каркина", "hippolyta": "Ипполиты",
}


def lang():
    import journal_greek
    entries = dict(LANG)
    entries.update(JOURNAL_UI)
    entries.update(journal("greek", journal_greek.INTRO, journal_greek.ENTRIES))
    for key, values in AMAZON_TEXT.items():
        entries[f"entity.{NS}.amazon.{key}"] = values
    for key, values in HIPPOLYTA_TEXT.items():
        entries[f"entity.{NS}.hippolyta.{key}"] = values
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


# ====================================================================== journal

NARROW = {"i": 2, "l": 3, "t": 4, "f": 5, "k": 5, "I": 4, " ": 4, ".": 2, ",": 2, ":": 2, ";": 2, "!": 2, "'": 2,
          "|": 2, "(": 4, ")": 4, "[": 4, "]": 4, "*": 4, "\"": 4, "`": 3}
BOOK_WIDTH, BOOK_LINES = 114, 14


def text_lines(text, bold=False):
    """How many lines a text takes in the book screen (word wrap with the widths of the default font)."""
    count = 0
    for paragraph in text.split("\n"):
        width = 0
        count += 1
        for word in paragraph.split(" "):
            w = sum(NARROW.get(ch, 6) + (1 if bold else 0) for ch in word)
            if width and width + 4 + w > BOOK_WIDTH:
                count += 1
                width = w
            else:
                width += (4 if width else 0) + w
    return count


def journal(volume, intro, entries):
    """Writes data/mythsofworlds/journal/<volume>.json and the journal text into LANG; checks every page fits."""
    lang_entries = {}
    title_ru, title_en, intro_ru, intro_en = intro
    lang_entries[f"journal.{NS}.{volume}.title"] = (title_ru, title_en)
    lang_entries[f"journal.{NS}.{volume}.intro"] = (intro_ru, intro_en)
    listed = []
    for entry_id, category, unlock, ru, en in entries:
        if len(ru) != len(en):
            raise ValueError(f"journal {entry_id}: {len(ru) - 1} Russian pages but {len(en) - 1} English")
        full_id = f"{volume}.{entry_id}"
        for lang_index, pages in ((0, ru), (1, en)):
            title, body = pages[0], pages[1:]
            for n, page in enumerate(body, 1):
                budget = BOOK_LINES - (2 + text_lines(title, bold=True) if n == 1 else 0)
                if text_lines(page) > budget:
                    raise ValueError(f"journal {full_id} page {n} ({'ru' if lang_index == 0 else 'en'}) is "
                                     f"{text_lines(page)} lines, only {budget} fit")
        lang_entries[f"journal.{NS}.{full_id}.title"] = (ru[0], en[0])
        for n in range(1, len(ru)):
            lang_entries[f"journal.{NS}.{full_id}.page{n}"] = (ru[n], en[n])
        item = {"id": full_id, "category": category, "pages": len(ru) - 1}
        if unlock:
            item[unlock[0]] = unlock[1]
        listed.append(item)
    write_json(data("journal", f"{volume}.json"), {"entries": listed})
    return lang_entries


JOURNAL_UI = {
    "journal.mythsofworlds.progress": ("Записей: %s из %s", "Entries: %s of %s"),
    "journal.mythsofworlds.new_entry": ("Новая запись в журнале: %s", "New journal entry: %s"),
    "journal.mythsofworlds.given": ("В вашей сумке появился %s. Записи в нём будут появляться сами.",
                                    "You find %s in your pack. Its entries will write themselves."),
    "journal.mythsofworlds.category.intro": ("Введение", "Introduction"),
    "journal.mythsofworlds.category.creature": ("Существа", "Creatures"),
    "journal.mythsofworlds.category.boss": ("Боссы", "Bosses"),
    "journal.mythsofworlds.category.place": ("Места", "Places"),
}

AMAZON_TEXT = {
    "daughter": ("%1$s тянет вас за руку: «Папа, научи меня держать меч!»", "%1$s tugs at your hand: \"Father, teach me to hold a sword!\""),
    "child": ("%1$s прячется за маму.", "%1$s hides behind her mother."),
    "angry": ("%1$s в ярости и не желает с вами говорить!", "%1$s is furious and will not talk to you!"),
    "stay": ("%1$s: «Я подожду здесь».", "%1$s: \"I will wait here.\""),
    "wander": ("%1$s: «Я погуляю тут неподалёку».", "%1$s: \"I will look around here.\""),
    "necklace": ("%1$s не может отвести глаз от ожерелья Гармонии. Она влюблена!",
                 "%1$s cannot take her eyes off the necklace of Harmonia. She is in love!"),
    "necklace_already": ("%1$s: «Моё сердце и так твоё. Оставь ожерелье себе».",
                         "%1$s: \"My heart is already yours. Keep the necklace.\""),
    "follow": ("%1$s: «Я иду с тобой».", "%1$s: \"I am coming with you.\""),
    "busy": ("%1$s ещё любуется прошлым подарком. Подождите немного.", "%1$s is still admiring your last gift. Wait a little."),
    "gift": ("%1$s принимает подарок. Симпатия: %2$s/%3$s", "%1$s accepts the gift. Affection: %2$s/%3$s"),
    "gift_favourite": ("%1$s в восторге: это её любимое! Симпатия: %2$s/%3$s", "%1$s is delighted: her favourite! Affection: %2$s/%3$s"),
    "in_love": ("%1$s смотрит на вас с нежностью. Подарите ей обручальное кольцо!",
                "%1$s looks at you tenderly. Give her a wedding ring!"),
    "wife": ("%1$s, ваша жена, улыбается. Подарите ей торт, и родится дочь. Shift+ПКМ: идти за вами, ждать или гулять.",
             "%1$s, your wife, smiles. Give her a cake and a daughter is born. Shift + right-click: follow, stay or wander."),
    "grown_daughter": ("%1$s, ваша дочь, готова сражаться рядом с вами.", "%1$s, your daughter, is ready to fight at your side."),
    "talk": ("%1$s: «Чем ты удивишь амазонку?» Больше всего она любит %2$s. Симпатия: %3$s/%4$s",
             "%1$s: \"What can you offer an amazon?\" She likes %2$s best. Affection: %3$s/%4$s"),
    "likes.0": ("цветы", "flowers"),
    "likes.1": ("золото и драгоценности", "gold and jewels"),
    "likes.2": ("оружие и трофеи чудовищ", "weapons and monster trophies"),
    "likes.3": ("вкусную еду", "good food"),
    "is_daughter": ("%1$s - ваша дочь!", "%1$s is your daughter!"),
    "already_yours": ("%1$s уже ваша жена.", "%1$s is already your wife."),
    "taken": ("%1$s замужем за другим героем.", "%1$s is married to another hero."),
    "you_are_married": ("Вы уже женаты. Амазонки не делят мужей.", "You are already married. Amazons do not share husbands."),
    "unworthy": ("%1$s не примет кольцо от вас.", "%1$s will not take a ring from you."),
    "not_yet": ("%1$s смеётся: «Сначала завоюй моё сердце». Симпатия: %2$s/%3$s",
                "%1$s laughs: \"Win my heart first.\" Affection: %2$s/%3$s"),
    "married": ("%1$s принимает кольцо! Теперь она ваша жена.", "%1$s takes the ring! She is your wife now."),
    "tired": ("%1$s: «Не сегодня. Приходи завтра».", "%1$s: \"Not today. Come back tomorrow.\""),
    "not_tonight": ("%1$s: «Не сегодня».", "%1$s: \"Not tonight.\""),
    "daughter_born": ("У вас родилась дочь, %2$s!", "A daughter is born to you: %2$s!"),
    "died": ("Ваша жена %1$s погибла...", "Your wife %1$s has died..."),
}
HIPPOLYTA_TEXT = dict(AMAZON_TEXT, **{
    "challenge": ("%1$s: «Ты вошёл в Фемискиру с оружием. Победи меня или уходи».",
                  "%1$s: \"You came armed into Themiscyra. Defeat me or leave.\""),
    "yield": ("%1$s опускает меч: «Ты сильнее меня. Возьми мой пояс, герой».",
              "%1$s lowers her sword: \"You are stronger than me. Take my girdle, hero.\""),
    "unworthy": ("%1$s: «Я слушаю только того, кто победил меня в бою».", "%1$s: \"I listen only to the one who beat me in battle.\""),
    "scorn": ("%1$s отвергает подарок: «Это недостойно царицы». Симпатия: %2$s/%3$s",
              "%1$s scorns the gift: \"This is not fit for a queen.\" Affection: %2$s/%3$s"),
    "gift_again": ("%1$s: «Такой дар у меня уже есть, но он мне по-прежнему приятен». Симпатия: %2$s/%3$s",
                   "%1$s: \"I already have such a gift, but it still pleases me.\" Affection: %2$s/%3$s"),
    "gift": ("%1$s благосклонно принимает дар. Симпатия: %2$s/%3$s", "%1$s graciously accepts the gift. Affection: %2$s/%3$s"),
    "talk": ("%1$s: «Принеси трофеи великих чудовищ, амброзию или сокровища, каких нет ни у кого». Симпатия: %2$s/%3$s",
             "%1$s: \"Bring me trophies of the great monsters, ambrosia or treasures no one else has.\" Affection: %2$s/%3$s"),
    "in_love": ("%1$s: «Ты достоин стать мужем царицы. Где твоё кольцо?»", "%1$s: \"You are worthy to wed a queen. Where is your ring?\""),
    "wife": ("%1$s, царица амазонок и ваша жена. Амброзия, и, может быть, родится царевна. Shift+ПКМ: идти, ждать или гулять.",
             "%1$s, queen of the Amazons and your wife. Ambrosia, and perhaps a princess is born. Shift + right-click: follow, stay or wander."),
    "you_are_married": ("Царица не делит мужа ни с кем!", "A queen shares her husband with no one!"),
    "married": ("%1$s надевает кольцо. Царица амазонок - ваша жена!", "%1$s puts on the ring. The queen of the Amazons is your wife!"),
    "tired": ("%1$s: «Царице нужен отдых. Приходи через три дня».", "%1$s: \"A queen needs her rest. Come back in three days.\""),
    "not_tonight": ("%1$s: «Не сегодня, мой царь».", "%1$s: \"Not tonight, my king.\""),
    "daughter_born": ("У вас родилась царевна, %2$s!", "A princess is born to you: %2$s!"),
})


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
    for name, fn in tx.NEW_BLOCKS.items():
        tx.save(fn(random.Random(name)), assets("textures", "block", f"{name}.png"))
    for name, fn in tx.NEW_ITEMS.items():
        tx.save(tx.item(fn, random.Random(name)), assets("textures", "item", f"{name}.png"))
    for name, fn in tx.NEW_ENTITIES.items():
        tx.save(fn(random.Random(name)), assets("textures", "entity", f"{name}.png"))


def main():
    write_json(data("dimension_type", "hellas.json"), dimension_type())
    hellas_noise_settings()
    write_json(data("dimension", "hellas.json"),
               dimension("hellas", multi_noise([(f"{NS}:{name}", spec["point"]) for name, spec in BIOMES.items()]),
                         settings=f"{NS}:hellas"))
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
