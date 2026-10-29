"""
Generates the data and asset files of the Norse mythology: Jotunheim, its biomes, structures, loot, recipes,
models, translations and the skald's journal. Uses the helpers of gen_greek_assets.py.

    python3 tools/gen_norse_assets.py            # everything except textures
    python3 tools/gen_norse_assets.py --textures # also (re)draw the placeholder PNGs, overwriting them

Run it after gen_greek_assets.py (both merge their translations and tags into the same files).
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_greek_assets as g  # noqa: E402
import structures_norse  # noqa: E402
from gen_greek_assets import (NS, SAPLING_OK, _above, _biome, _block, _if, _noise, _seq, FLOOR, STEEP,  # noqa: E402
                              UNDER_FLOOR, assets, chest, data, entry, mob, simple, spawn, state, surface_placement,
                              write_json)

# ====================================================================== dimension

def jotunheim_surface():
    """Surface rules of Jotunheim, tried before the vanilla ones: snow and ice in the wastes and Niflheim, black
    basalt and magma in Muspelheim, grey gravel shores in the fjords, dark earth in the Iron Wood."""
    not_above = lambda y: {"type": "minecraft:not", "invert": _above(y)}  # noqa: E731
    return _if({"type": "minecraft:above_preliminary_surface"}, _seq(
        _if(_biome("frost_wastes"), _seq(
            _if(FLOOR, _seq(_if(_noise(0.45, 4.0), _block("minecraft:packed_ice")), _block("minecraft:snow_block"))),
            _if(UNDER_FLOOR, _block("minecraft:snow_block")))),
        _if(_biome("niflheim_mists"), _seq(
            _if(FLOOR, _seq(_if(_noise(0.3, 4.0), _block("minecraft:packed_ice")),
                            _if(_noise(-4.0, -0.45), _block("minecraft:blue_ice")), _block("minecraft:snow_block"))),
            _if(UNDER_FLOOR, _block("minecraft:packed_ice")))),
        _if(_biome("muspel_rift"), _seq(
            _if(FLOOR, _seq(_if(STEEP, _block("minecraft:basalt")), _if(_noise(0.25, 4.0), _block("minecraft:magma_block")),
                            _if(_noise(-4.0, -0.3), _block("minecraft:basalt")), _block("minecraft:blackstone"))),
            _if(UNDER_FLOOR, _block("minecraft:blackstone")))),
        _if(_biome("fjords"), _if(FLOOR, _seq(
            _if(STEEP, _block("minecraft:stone")),
            _if(not_above(66), _block("minecraft:gravel")),
            _if(_noise(0.4, 4.0), _block("minecraft:stone"))))),
        _if(_biome("norse_sea"), _if(UNDER_FLOOR, _seq(_if(_noise(0.0, 4.0), _block("minecraft:gravel")),
                                                       _block("minecraft:sand")))),
        _if(_biome("ironwood"), _if(FLOOR, _seq(
            _if(_noise(0.3, 4.0), _block("minecraft:coarse_dirt")),
            _if(_noise(-4.0, -0.4), _block("minecraft:rooted_dirt")),
            _block("minecraft:podzol")))),
        _if(_biome("giants_taiga"), _if(FLOOR, _seq(
            _if(STEEP, _block("minecraft:stone")),
            _if(_noise(0.35, 4.0), _block("minecraft:podzol")),
            _if(_noise(-4.0, -0.5), _block("minecraft:coarse_dirt"))))),
        _if(_biome("idunn_orchard"), _if(FLOOR, _if(_noise(0.5, 4.0), _block("minecraft:moss_block"))))))


def jotunheim_noise_settings():
    """The amplified terrain of the Overworld: mountains fit for giants."""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vanilla", "amplified_noise_settings.json"),
              encoding="utf-8") as f:
        settings = json.load(f)
    settings["surface_rule"]["sequence"].insert(1, jotunheim_surface())
    write_json(data("worldgen", "noise_settings", "jotunheim.json"), settings)


# ====================================================================== biomes

FEATURE_ORDER = [
    [],
    ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface"],
    ["minecraft:forest_rock", "minecraft:iceberg_packed", "minecraft:iceberg_blue"],
    ["minecraft:monster_room", "minecraft:monster_room_deep"],
    ["minecraft:ice_spike", "minecraft:ice_patch", f"{NS}:menhir", f"{NS}:basalt_spire"],
    [],
    g.COMMON_ORES + [f"{NS}:muspel_magma", f"{NS}:niflheim_frost"] + g.DISKS,
    [],
    ["minecraft:spring_water", "minecraft:spring_lava"],
    ["minecraft:glow_lichen", f"{NS}:ironwood_tree", f"{NS}:ironwood_bush", f"{NS}:idunn_tree", f"{NS}:fjord_spruce",
     f"{NS}:frozen_trunk", "minecraft:trees_old_growth_spruce_taiga", "minecraft:patch_large_fern",
     "minecraft:patch_grass_taiga", "minecraft:patch_berry_common", "minecraft:brown_mushroom_taiga",
     "minecraft:red_mushroom_taiga", "minecraft:flower_meadow", "minecraft:flower_default", "minecraft:patch_grass_plain",
     "minecraft:patch_dead_bush", "minecraft:kelp_cold", "minecraft:seagrass_cold"],
    ["minecraft:freeze_top_layer"],
]
COMMON = g.COMMON


def music(name):
    return (f"minecraft:music.{name}", 12000, 24000)


BIOMES = {
    "frost_wastes": {
        "ru": "Ледяные пустоши", "en": "Frost Wastes",
        "point": {"c": 0.4, "t": -0.8, "h": -0.3},
        "temperature": -0.8, "downfall": 0.5,
        "sky": 0x8FA8C7, "fog": 0xB8C8D8, "water": 0x3D5CD6, "water_fog": 0x050533, "grass": 0x80B497, "foliage": 0x60A17B,
        "particle": ("minecraft:snowflake", 0.015), "music": music("overworld.snowy_slopes"),
        "features": COMMON + ["minecraft:ice_spike", "minecraft:ice_patch", f"{NS}:menhir", "minecraft:forest_rock"],
        "spawners": {
            "monster": [spawn(f"{NS}:frost_giant", 25, 1, 1), spawn(f"{NS}:draugr", 40, 1, 3), spawn("minecraft:stray", 60, 1, 3),
                        spawn(f"{NS}:warg", 20, 2, 4), spawn(f"{NS}:troll", 10, 1, 1)],
            "creature": [spawn("minecraft:polar_bear", 2, 1, 2), spawn("minecraft:rabbit", 4, 2, 3)],
        },
    },
    "giants_taiga": {
        "ru": "Тайга великанов", "en": "Giants' Taiga",
        "point": {"c": 0.4, "t": -0.3, "h": 0.3},
        "temperature": -0.3, "downfall": 0.8,
        "sky": 0x7FA1C4, "fog": 0xA9BCCB, "water": 0x3D57D6, "water_fog": 0x050533, "grass": 0x86B783, "foliage": 0x68A464,
        "music": music("overworld.old_growth_taiga"),
        "features": COMMON + ["minecraft:forest_rock", f"{NS}:menhir", "minecraft:trees_old_growth_spruce_taiga",
                              "minecraft:patch_large_fern", "minecraft:patch_grass_taiga", "minecraft:patch_berry_common",
                              "minecraft:brown_mushroom_taiga", "minecraft:red_mushroom_taiga"],
        "spawners": {
            "monster": [spawn(f"{NS}:troll", 25, 1, 1), spawn(f"{NS}:warg", 30, 2, 4), spawn(f"{NS}:draugr", 40, 1, 3),
                        spawn("minecraft:skeleton", 40, 1, 3), spawn("minecraft:spider", 40, 1, 2), spawn("minecraft:creeper", 30, 1, 2)],
            "creature": [spawn(f"{NS}:raven", 8, 1, 3), spawn("minecraft:wolf", 6, 2, 4), spawn("minecraft:fox", 6, 1, 3),
                         spawn("minecraft:rabbit", 4, 2, 3)],
        },
    },
    "ironwood": {
        "ru": "Железный лес", "en": "Iron Wood",
        "point": {"c": 0.6, "t": -0.1, "h": 0.7, "w": 0.3},
        "temperature": 0.2, "downfall": 0.6,
        "sky": 0x5E6A75, "fog": 0x6B7279, "water": 0x3A4A5A, "water_fog": 0x101820, "grass": 0x5C6650, "foliage": 0x4A5048,
        "particle": ("minecraft:ash", 0.006), "music": music("overworld.forest"),
        "features": COMMON + ["minecraft:forest_rock", f"{NS}:ironwood_tree", f"{NS}:ironwood_bush",
                              "minecraft:patch_grass_taiga", "minecraft:brown_mushroom_taiga"],
        "spawners": {
            "monster": [spawn(f"{NS}:warg", 80, 3, 5), spawn(f"{NS}:troll", 20, 1, 1), spawn("minecraft:spider", 40, 1, 2),
                        spawn("minecraft:skeleton", 20, 1, 2)],
            "creature": [spawn(f"{NS}:raven", 6, 1, 3)],
        },
    },
    "fjords": {
        "ru": "Фьорды", "en": "Fjords",
        "point": {"c": -0.05, "t": -0.3, "e": 0.3},
        "temperature": 0.1, "downfall": 0.8,
        "sky": 0x7BA7D8, "fog": 0xC0D0E0, "water": 0x2E6B8A, "water_fog": 0x072A3A, "grass": 0x79A36A, "foliage": 0x5E8A52,
        "music": music("overworld.stony_peaks"),
        "features": COMMON + g.DISKS + [f"{NS}:menhir", f"{NS}:fjord_spruce", "minecraft:patch_grass_taiga"],
        "spawners": {
            "monster": [spawn(f"{NS}:draugr", 60, 1, 3), spawn("minecraft:skeleton", 40, 1, 3), spawn("minecraft:zombie", 40, 1, 3),
                        spawn("minecraft:creeper", 40, 1, 2)],
            "creature": [spawn(f"{NS}:raven", 6, 1, 3), spawn("minecraft:goat", 6, 1, 3), spawn("minecraft:sheep", 6, 2, 4)],
        },
    },
    "norse_sea": {
        "ru": "Северное море", "en": "Northern Sea",
        "point": {"c": -0.6, "t": -0.2},
        "temperature": 0.0, "downfall": 0.6,
        "sky": 0x7BA7D8, "fog": 0xC0D0E0, "water": 0x2E5B7A, "water_fog": 0x051E2E, "grass": 0x79A36A, "foliage": 0x5E8A52,
        "features": COMMON + g.DISKS + ["minecraft:iceberg_packed", "minecraft:iceberg_blue", "minecraft:kelp_cold",
                                        "minecraft:seagrass_cold"],
        "spawners": {
            "monster": [spawn("minecraft:drowned", 60, 1, 3)],
            "water_creature": [spawn("minecraft:squid", 6, 1, 4)],
            "water_ambient": [spawn("minecraft:cod", 15, 3, 6), spawn("minecraft:salmon", 15, 1, 5)],
        },
    },
    "muspel_rift": {
        "ru": "Разлом Муспельхейма", "en": "Rift of Muspelheim",
        "point": {"c": 0.7, "t": 0.7, "h": -0.7, "w": -0.5},
        "temperature": 2.0, "downfall": 0.0, "precipitation": False,
        "sky": 0xB04A2A, "fog": 0x6A2A1A, "water": 0xE0602A, "water_fog": 0x601A0A, "grass": 0x8A5A2A, "foliage": 0x6A3A1A,
        "particle": ("minecraft:ash", 0.02), "music": ("minecraft:music.nether.basalt_deltas", 12000, 24000),
        "additions": ("minecraft:ambient.basalt_deltas.additions", 0.0111),
        "features": COMMON + ["minecraft:lake_lava_surface", "minecraft:lake_lava_underground", f"{NS}:muspel_magma",
                              f"{NS}:basalt_spire", "minecraft:patch_dead_bush"],
        "spawners": {
            "monster": [spawn(f"{NS}:fire_giant", 40, 1, 2), spawn("minecraft:magma_cube", 60, 1, 3), spawn("minecraft:blaze", 15, 1, 2)],
        },
    },
    "niflheim_mists": {
        "ru": "Туманы Нифльхейма", "en": "Mists of Niflheim",
        "point": {"c": 0.5, "t": -0.9, "h": 0.6, "w": 0.6},
        "temperature": -1.0, "downfall": 0.9,
        "sky": 0x4A5A6A, "fog": 0x9AA8B4, "water": 0x2A3A4A, "water_fog": 0x0A1420, "grass": 0x6A7A7A, "foliage": 0x5A6A6A,
        "particle": ("minecraft:white_ash", 0.02), "music": music("overworld.deep_dark"),
        "additions": ("minecraft:ambient.soul_sand_valley.additions", 0.0111),
        "features": COMMON + ["minecraft:ice_patch", f"{NS}:menhir", f"{NS}:niflheim_frost", f"{NS}:frozen_trunk"],
        "spawners": {
            "monster": [spawn(f"{NS}:draugr", 100, 2, 4), spawn("minecraft:stray", 80, 1, 3), spawn(f"{NS}:troll", 10, 1, 1)],
        },
    },
    "idunn_orchard": {
        "ru": "Сады Идунн", "en": "Orchards of Idunn",
        "point": {"c": 0.3, "t": 0.4, "e": 0.5},
        "temperature": 0.6, "downfall": 0.6,
        "sky": 0x9AC8F0, "fog": 0xD8E8F0, "water": 0x4AA0E0, "water_fog": 0x0A3050, "grass": 0x8ED160, "foliage": 0x6EC04A,
        "particle": ("minecraft:spore_blossom_air", 0.002), "music": music("overworld.meadow"),
        "features": COMMON + [f"{NS}:idunn_tree", "minecraft:flower_meadow", "minecraft:flower_default", "minecraft:patch_grass_plain"],
        "spawners": {
            "monster": [spawn("minecraft:zombie", 20, 1, 2), spawn("minecraft:skeleton", 20, 1, 2)],
            "creature": [spawn(f"{NS}:raven", 8, 1, 3), spawn("minecraft:rabbit", 6, 2, 3), spawn("minecraft:sheep", 8, 2, 4),
                         spawn("minecraft:fox", 4, 1, 2)],
        },
    },
}


def features():
    # Ironwood: tall, gnarled, iron-grey trees of Jarnvidr.
    g.tree("ironwood_tree", f"{NS}:ironwood_log", f"{NS}:ironwood_leaves",
           {"type": "minecraft:fancy_trunk_placer", "base_height": 9, "height_rand_a": 5, "height_rand_b": 0},
           {"type": "minecraft:fancy_foliage_placer", "radius": 2, "offset": 4, "height": 4}, count=5,
           dirt="minecraft:rooted_dirt")
    g.tree("ironwood_bush", f"{NS}:ironwood_log", f"{NS}:ironwood_leaves",
           {"type": "minecraft:straight_trunk_placer", "base_height": 1, "height_rand_a": 0, "height_rand_b": 0},
           {"type": "minecraft:bush_foliage_placer", "radius": 2, "offset": 1, "height": 2}, count=2,
           dirt="minecraft:rooted_dirt")
    # The apple trees of Idunn: round crowns with golden apples.
    g.tree("idunn_tree", "minecraft:birch_log", f"{NS}:idunn_leaves",
           {"type": "minecraft:straight_trunk_placer", "base_height": 4, "height_rand_a": 2, "height_rand_b": 0},
           {"type": "minecraft:blob_foliage_placer", "radius": 2, "offset": 0, "height": 3}, count=2, fruit=True)
    # Lone spruces on the fjord shores.
    g.tree("fjord_spruce", "minecraft:spruce_log", "minecraft:spruce_leaves",
           {"type": "minecraft:straight_trunk_placer", "base_height": 6, "height_rand_a": 3, "height_rand_b": 0},
           {"type": "minecraft:spruce_foliage_placer", "radius": {"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 3},
            "offset": {"type": "minecraft:uniform", "min_inclusive": 0, "max_inclusive": 2},
            "trunk_height": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": 2}}, rarity=2)

    def column(name, layers, rarity, extra=None):
        write_json(data("worldgen", "configured_feature", f"{name}.json"), {"type": "minecraft:block_column", "config": {
            "layers": [{"height": {"type": "minecraft:uniform", "min_inclusive": lo, "max_inclusive": hi}, "provider": provider}
                       for lo, hi, provider in layers],
            "direction": "up", "allowed_placement": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
            "prioritize_tip": True}})
        write_json(data("worldgen", "placed_feature", f"{name}.json"),
                   {"feature": f"{NS}:{name}", "placement": surface_placement(rarity=rarity, extra=extra)})

    # Standing runestones raised over the graves of heroes.
    column("menhir", [(1, 2, simple(f"{NS}:runestone")), (1, 1, simple(f"{NS}:carved_runestone"))], 28)
    # Black basalt spires of Muspelheim and the frozen dead trunks of Niflheim.
    column("basalt_spire", [(2, 7, simple("minecraft:basalt", axis="y"))], 3)
    column("frozen_trunk", [(2, 5, simple("minecraft:stripped_spruce_log", axis="y"))], 3, extra=[SAPLING_OK])

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
                "vegetation_chance": chance, "xz_radius": {"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 6},
                "extra_edge_column_chance": 0.3,
            },
        })
        write_json(data("worldgen", "placed_feature", f"{name}.json"), {"feature": f"{NS}:{name}", "placement": [
            {"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
            {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"}, {"type": "minecraft:biome"}]})

    patch("muspel_magma", [("minecraft:magma_block", 3), ("minecraft:blackstone", 3), ("minecraft:basalt", 2)],
          simple("minecraft:air"), 3, 0.0)
    patch("niflheim_frost", [("minecraft:packed_ice", 3), ("minecraft:snow_block", 2), ("minecraft:blue_ice", 1)],
          simple("minecraft:snow"), 2, 0.4)


# ====================================================================== structures

STRUCTURES = {
    # Lairs of the bosses: one set, so that no two stand close together anywhere in Jotunheim.
    "utgard": (["frost_wastes"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "fenrir_island": (["ironwood"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "muspel_fortress": (["muspel_rift"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "helgrind": (["niflheim_mists"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "barrow": (["giants_taiga", "fjords", "frost_wastes", "idunn_orchard"], 0, 0, 0, "WORLD_SURFACE_WG", -1, "beard_thin"),
    # Villages, ships and shrines.
    "viking_village": (["fjords", "giants_taiga", "idunn_orchard"], 32, 12, 2450201, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "longship": (["norse_sea", "fjords"], 40, 14, 2450202, "WORLD_SURFACE_WG", -3, "none"),
    "naglfar": (["norse_sea"], 56, 20, 2450203, "WORLD_SURFACE_WG", -3, "none"),
    "dwarf_forge": (["giants_taiga", "frost_wastes", "ironwood"], 40, 14, 2450204, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "rune_circle": (["giants_taiga", "fjords", "frost_wastes", "idunn_orchard", "ironwood", "niflheim_mists"], 22, 8, 2450205,
                    "WORLD_SURFACE_WG", 0, "beard_thin"),
}
LAIRS = {"structures": {"utgard": 3, "fenrir_island": 3, "muspel_fortress": 3, "helgrind": 3, "barrow": 4},
         "spacing": 56, "separation": 36, "salt": 2450300}

STRUCTURE_NAMES = {
    "viking_village": ("Поселение викингов", "Viking Village"),
    "longship": ("Драккар", "Longship"),
    "naglfar": ("Нагльфар", "Naglfar"),
    "barrow": ("Курган", "Barrow"),
    "utgard": ("Утгард", "Utgard"),
    "fenrir_island": ("Остров Люнгви", "Isle of Lyngvi"),
    "muspel_fortress": ("Крепость Сурта", "Fortress of Surtr"),
    "helgrind": ("Врата Хель", "Gates of Hel"),
    "dwarf_forge": ("Кузня двергов", "Dwarven Forge"),
    "rune_circle": ("Рунный круг", "Rune Circle"),
}


def worldgen_structures():
    os.makedirs(data("structure", "norse"), exist_ok=True)
    for name, (biomes, spacing, separation, salt, heightmap, offset, adaptation) in STRUCTURES.items():
        structures_norse.STRUCTURES[name]().save(data("structure", "norse", f"{name}.nbt"))
        write_json(data("tags", "worldgen", "biome", "has_structure", f"{name}.json"),
                   {"replace": False, "values": [f"{NS}:{b}" for b in biomes]})
        write_json(data("worldgen", "template_pool", "norse", name, "start.json"), {
            "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {
                "element_type": "minecraft:single_pool_element",
                "location": f"{NS}:norse/{name}",
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
            "start_pool": f"{NS}:norse/{name}/start",
            "size": 1,
            "start_height": {"absolute": offset},
            "project_start_to_heightmap": heightmap,
            "max_distance_from_center": 80,
            "use_expansion_hack": False,
        })
        if name in LAIRS["structures"]:
            continue
        write_json(data("worldgen", "structure_set", f"{name}.json"), {
            "structures": [{"structure": f"{NS}:{name}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
        })
    write_json(data("worldgen", "structure_set", "norse_lairs.json"), {
        "structures": [{"structure": f"{NS}:{name}", "weight": w} for name, w in LAIRS["structures"].items()],
        "placement": {"type": "minecraft:random_spread", "spacing": LAIRS["spacing"], "separation": LAIRS["separation"],
                      "salt": LAIRS["salt"]},
    })


# ====================================================================== loot

def loot():
    for block in ("carved_runestone", "ironwood_log", "ironwood_planks"):
        write_json(data("loot_table", "blocks", f"{block}.json"), {
            "type": "minecraft:block",
            "pools": [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": f"{NS}:{block}"}],
                       "conditions": [{"condition": "minecraft:survives_explosion"}]}],
            "random_sequence": f"{NS}:blocks/{block}",
        })
    shears_or_silk = {"condition": "minecraft:any_of", "terms": [
        {"condition": "minecraft:match_tool", "predicate": {"items": "minecraft:shears"}},
        {"condition": "minecraft:match_tool", "predicate": {"predicates": {"minecraft:enchantments": [
            {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]}
    write_json(data("loot_table", "blocks", "ironwood_leaves.json"), {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{"type": "minecraft:alternatives", "children": [
            {"type": "minecraft:item", "name": f"{NS}:ironwood_leaves", "conditions": [shears_or_silk]},
            {"type": "minecraft:item", "name": "minecraft:stick", "conditions": [{"condition": "minecraft:random_chance", "chance": 0.06}]},
            {"type": "minecraft:item", "name": "minecraft:iron_nugget", "conditions": [{"condition": "minecraft:random_chance", "chance": 0.05}]}]}]}],
        "random_sequence": f"{NS}:blocks/ironwood_leaves",
    })
    write_json(data("loot_table", "blocks", "idunn_leaves.json"), {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "entries": [{"type": "minecraft:alternatives", "children": [
            {"type": "minecraft:item", "name": f"{NS}:idunn_leaves", "conditions": [shears_or_silk]},
            {"type": "minecraft:item", "name": f"{NS}:idunn_apple", "conditions": [
                {"condition": "minecraft:block_state_property", "block": f"{NS}:idunn_leaves", "properties": {"age": "3"}}]},
            {"type": "minecraft:item", "name": "minecraft:stick", "conditions": [{"condition": "minecraft:random_chance", "chance": 0.04}]}]}]}],
        "random_sequence": f"{NS}:blocks/idunn_leaves",
    })

    gold = [entry("minecraft:gold_ingot", 8, 1, 4), entry("minecraft:gold_nugget", 10, 3, 9), entry("minecraft:emerald", 6, 1, 4)]
    chest("viking_village", (3, 6), gold + [
        entry(f"{NS}:mead", 8, 1, 3), entry("minecraft:bread", 8, 2, 5), entry("minecraft:cooked_salmon", 6, 2, 5),
        entry("minecraft:iron_axe", 4, enchant=True), entry("minecraft:shield", 3), entry(f"{NS}:rune_igniter", 1),
    ])
    chest("viking_house", (3, 6), [
        entry("minecraft:wheat", 8, 2, 6), entry("minecraft:white_wool", 6, 1, 4), entry("minecraft:leather", 6, 1, 4),
        entry("minecraft:honey_bottle", 4, 1, 2), entry(f"{NS}:mead", 4, 1, 2), entry("minecraft:iron_ingot", 4, 1, 3),
        entry("minecraft:sweet_berries", 6, 2, 6),
    ])
    chest("longship", (3, 6), gold + [
        entry("minecraft:iron_axe", 4, enchant=True), entry("minecraft:cod", 8, 2, 6), entry(f"{NS}:mead", 6, 1, 3),
        entry("minecraft:map", 2), entry("minecraft:amethyst_shard", 4, 1, 3), entry("minecraft:saddle", 1),
    ])
    chest("naglfar", (4, 7), gold + [
        entry("minecraft:bone", 10, 2, 8), entry("minecraft:rotten_flesh", 8, 2, 6), entry("minecraft:iron_sword", 3, enchant=True),
        entry("minecraft:diamond", 3, 1, 2), entry("minecraft:echo_shard", 2), entry("minecraft:book", 3, enchant=True),
    ])
    chest("barrow", (4, 7), gold + [
        entry("minecraft:gold_ingot", 6, 2, 6), entry("minecraft:iron_sword", 4, enchant=True), entry("minecraft:chainmail_chestplate", 3),
        entry("minecraft:bone", 8, 1, 4), entry("minecraft:diamond", 2, 1, 2), entry("minecraft:book", 3, enchant=True),
        entry("minecraft:golden_apple", 2),
    ])
    chest("utgard", (4, 8), gold + [
        entry("minecraft:diamond", 4, 1, 3), entry("minecraft:blue_ice", 6, 2, 6), entry(f"{NS}:frost_heart", 4, 1, 2),
        entry("minecraft:diamond_axe", 2, enchant=True), entry("minecraft:golden_apple", 3), entry(f"{NS}:idunn_apple", 3, 1, 2),
    ])
    chest("fenrir_island", (3, 6), gold + [
        entry("minecraft:bone", 10, 2, 8), entry("minecraft:leather", 8, 2, 5), entry("minecraft:chain", 6, 2, 6),
        entry("minecraft:diamond", 3, 1, 2), entry("minecraft:book", 3, enchant=True),
    ])
    chest("muspel_fortress", (4, 8), gold + [
        entry("minecraft:blaze_rod", 6, 1, 4), entry("minecraft:magma_cream", 6, 1, 4), entry(f"{NS}:muspel_ember", 4, 1, 2),
        entry("minecraft:netherite_scrap", 2), entry("minecraft:diamond", 4, 1, 3), entry("minecraft:fire_charge", 6, 2, 6),
        entry("minecraft:golden_sword", 3, enchant=True),
    ])
    chest("helgrind", (3, 6), gold + [
        entry("minecraft:bone", 10, 2, 8), entry("minecraft:soul_torch", 6, 2, 6), entry("minecraft:echo_shard", 3),
        entry("minecraft:diamond", 3, 1, 2), entry("minecraft:book", 4, enchant=True),
    ])
    chest("dwarf_forge", (4, 7), gold + [
        entry("minecraft:iron_ingot", 10, 2, 8), entry("minecraft:gold_ingot", 6, 2, 6), entry("minecraft:diamond", 3, 1, 2),
        entry("minecraft:iron_pickaxe", 4, enchant=True), entry("minecraft:anvil", 1), entry("minecraft:raw_gold", 6, 1, 4),
        entry(f"{NS}:runestone", 6, 2, 8),
    ])
    chest("rune_circle", (2, 4), [
        entry(f"{NS}:raven_feather", 8, 1, 4), entry("minecraft:lapis_lazuli", 8, 2, 6), entry("minecraft:amethyst_shard", 6, 1, 3),
        entry(f"{NS}:carved_runestone", 4, 1, 2), entry(f"{NS}:idunn_apple", 2), entry("minecraft:book", 3, enchant=True),
        entry("minecraft:wheat_seeds", 6, 2, 6),
    ])

    mob("draugr", [("minecraft:rotten_flesh", 0, 2, None), ("minecraft:bone", 0, 2, None), ("minecraft:iron_nugget", 0, 2, None),
                   ("minecraft:gold_nugget", 1, 3, 0.15)])
    mob("warg", [("minecraft:leather", 0, 2, None), ("minecraft:bone", 0, 2, None)])
    mob("troll", [(f"{NS}:troll_tusk", 1, 1, 0.5), ("minecraft:leather", 1, 3, None), ("minecraft:cobblestone", 1, 4, None)])
    mob("frost_giant", [(f"{NS}:frost_heart", 1, 1, 0.35), ("minecraft:snowball", 2, 6, None), ("minecraft:packed_ice", 0, 2, None)])
    mob("fire_giant", [(f"{NS}:muspel_ember", 1, 1, 0.35), ("minecraft:blaze_powder", 0, 2, None), ("minecraft:magma_cream", 0, 2, None)])
    mob("raven", [(f"{NS}:raven_feather", 0, 2, None)])
    mob("norse_merchant", [])
    mob("draugr_chieftain", [(f"{NS}:barrow_crown", 1, 1, None), ("minecraft:gold_ingot", 3, 8, None), ("minecraft:emerald", 2, 6, None)])
    mob("garm", [(f"{NS}:garm_fang", 1, 1, None), ("minecraft:bone", 3, 8, None), ("minecraft:diamond", 1, 2, None)])
    mob("thrym", [(f"{NS}:mjolnir", 1, 1, None), (f"{NS}:frost_heart", 2, 4, None), ("minecraft:diamond", 2, 4, None),
                  ("minecraft:gold_ingot", 4, 10, None)])
    mob("fenrir", [(f"{NS}:fenrir_fang", 1, 2, None), ("minecraft:leather", 4, 8, None), ("minecraft:diamond", 2, 4, None)])
    mob("surtr", [(f"{NS}:surtr_sword", 1, 1, None), (f"{NS}:muspel_ember", 2, 4, None), ("minecraft:netherite_scrap", 1, 2, None),
                  ("minecraft:diamond", 2, 4, None)])


# ====================================================================== recipes and tags

def recipes():
    def shapeless(name, ingredients, result, count=1, category="misc"):
        write_json(data("recipe", f"{name}.json"), {
            "type": "minecraft:crafting_shapeless", "category": category,
            "ingredients": [{"item": i} if not i.startswith("#") else {"tag": i[1:]} for i in ingredients],
            "result": {"id": result, "count": count}})

    shapeless("ironwood_planks", [f"{NS}:ironwood_log"], f"{NS}:ironwood_planks", 4, "building")
    shapeless("carved_runestone", [f"{NS}:runestone", "minecraft:red_dye"], f"{NS}:carved_runestone", 1, "building")
    shapeless("mead", ["minecraft:honey_bottle", "minecraft:wheat", "minecraft:sweet_berries"], f"{NS}:mead", 1, "misc")
    shapeless("norse_journal", ["minecraft:book", "minecraft:feather", "minecraft:lapis_lazuli"], f"{NS}:norse_journal")
    # The six things the dwarves made Gleipnir of: the sound of a cat's footfall, a woman's beard, the roots of a
    # mountain, the sinews of a bear, the breath of a fish and the spittle of a bird.
    shapeless("gleipnir", ["minecraft:rabbit_foot", "minecraft:string", "minecraft:hanging_roots", "minecraft:leather",
                           "minecraft:pufferfish", f"{NS}:raven_feather"], f"{NS}:gleipnir", 1, "equipment")
    g.add_tag("block", "mineable/pickaxe", ["runestone", "carved_runestone"])
    g.add_tag("block", "mineable/axe", ["ironwood_log", "ironwood_planks"])
    g.add_tag("block", "mineable/hoe", ["ironwood_leaves", "idunn_leaves"])
    g.add_tag("block", "leaves", ["ironwood_leaves", "idunn_leaves"])
    g.add_tag("item", "leaves", ["ironwood_leaves", "idunn_leaves"])
    g.add_tag("block", "logs", ["ironwood_log"])
    g.add_tag("item", "logs", ["ironwood_log"])
    g.add_tag("block", "planks", ["ironwood_planks"])
    g.add_tag("item", "planks", ["ironwood_planks"])
    g.add_tag("block", "overworld_natural_logs", ["ironwood_log"])


# ====================================================================== models

ITEMS = ["norse_journal", "norse_journal_complete", "idunn_apple", "mead", "raven_feather", "frost_heart", "muspel_ember",
         "troll_tusk", "fenrir_fang", "garm_fang", "barrow_crown", "mjolnir", "gleipnir", "surtr_sword"]
HANDHELD = {"mjolnir", "surtr_sword"}
MOBS = ["draugr", "warg", "troll", "frost_giant", "fire_giant", "raven", "norse_merchant", "draugr_chieftain", "garm",
        "thrym", "fenrir", "surtr"]


def models():
    def cube(name, texture=None, render_type=None):
        write_json(assets("blockstates", f"{name}.json"), {"variants": {"": {"model": f"{NS}:block/{name}"}}})
        model = {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{texture or name}"}}
        if render_type:
            model["render_type"] = render_type
        write_json(assets("models", "block", f"{name}.json"), model)
        write_json(assets("models", "item", f"{name}.json"), {"parent": f"{NS}:block/{name}"})

    cube("carved_runestone")
    cube("ironwood_planks")
    cube("ironwood_leaves", render_type="minecraft:cutout_mipped")
    write_json(assets("blockstates", "ironwood_log.json"), {"variants": {
        "axis=y": {"model": f"{NS}:block/ironwood_log"},
        "axis=z": {"model": f"{NS}:block/ironwood_log_horizontal", "x": 90},
        "axis=x": {"model": f"{NS}:block/ironwood_log_horizontal", "x": 90, "y": 90},
    }})
    log_textures = {"end": f"{NS}:block/ironwood_log_top", "side": f"{NS}:block/ironwood_log"}
    write_json(assets("models", "block", "ironwood_log.json"), {"parent": "minecraft:block/cube_column", "textures": log_textures})
    write_json(assets("models", "block", "ironwood_log_horizontal.json"),
               {"parent": "minecraft:block/cube_column_horizontal", "textures": log_textures})
    write_json(assets("models", "item", "ironwood_log.json"), {"parent": f"{NS}:block/ironwood_log"})
    write_json(assets("blockstates", "idunn_leaves.json"), {"variants": {
        f"age={age}": {"model": f"{NS}:block/idunn_leaves" + ("_ripe" if age == 3 else "")} for age in range(4)}})
    for suffix in ("", "_ripe"):
        write_json(assets("models", "block", f"idunn_leaves{suffix}.json"), {
            "parent": "minecraft:block/cube_all", "render_type": "minecraft:cutout_mipped",
            "textures": {"all": f"{NS}:block/idunn_leaves{suffix}"}})
    write_json(assets("models", "item", "idunn_leaves.json"), {"parent": f"{NS}:block/idunn_leaves_ripe"})
    for item in ITEMS:
        parent = "minecraft:item/handheld" if item in HANDHELD else "minecraft:item/generated"
        write_json(assets("models", "item", f"{item}.json"), {"parent": parent, "textures": {"layer0": f"{NS}:item/{item}"}})
    for name in MOBS:
        write_json(assets("models", "item", f"{name}_spawn_egg.json"), {"parent": "minecraft:item/template_spawn_egg"})


# ====================================================================== translations

LANG = {
    "block.mythsofworlds.carved_runestone": ("Резной рунный камень", "Carved Runestone"),
    "block.mythsofworlds.ironwood_log": ("Бревно железного дерева", "Ironwood Log"),
    "block.mythsofworlds.ironwood_planks": ("Доски железного дерева", "Ironwood Planks"),
    "block.mythsofworlds.ironwood_leaves": ("Листва железного дерева", "Ironwood Leaves"),
    "block.mythsofworlds.idunn_leaves": ("Листва яблони Идунн", "Idunn's Apple Leaves"),
    "item.mythsofworlds.norse_journal": ("Сага скальда", "Skald's Saga"),
    "item.mythsofworlds.norse_journal_complete": ("Сага скальда (полная)", "Skald's Saga (complete)"),
    "item.mythsofworlds.idunn_apple": ("Яблоко Идунн", "Apple of Idunn"),
    "item.mythsofworlds.mead": ("Медовуха", "Mead"),
    "item.mythsofworlds.raven_feather": ("Перо ворона", "Raven Feather"),
    "item.mythsofworlds.frost_heart": ("Сердце инея", "Frost Heart"),
    "item.mythsofworlds.muspel_ember": ("Уголь Муспельхейма", "Ember of Muspelheim"),
    "item.mythsofworlds.troll_tusk": ("Клык тролля", "Troll Tusk"),
    "item.mythsofworlds.fenrir_fang": ("Клык Фенрира", "Fang of Fenrir"),
    "item.mythsofworlds.garm_fang": ("Клык Гарма", "Fang of Garm"),
    "item.mythsofworlds.barrow_crown": ("Корона курганного короля", "Barrow-King's Crown"),
    "item.mythsofworlds.mjolnir": ("Мьёльнир", "Mjolnir"),
    "item.mythsofworlds.mjolnir.desc": ("Молот Тора. ПКМ: молния бьёт туда, куда вы смотрите (до 40 блоков)",
                                        "Thor's hammer. Right-click: lightning strikes where you look (up to 40 blocks)"),
    "item.mythsofworlds.gleipnir": ("Глейпнир", "Gleipnir"),
    "item.mythsofworlds.gleipnir.desc": ("Путы двергов. ПКМ по Фенриру: волк связан на 8 секунд, не может двигаться и кусать",
                                         "The dwarves' fetter. Use it on Fenrir: the wolf is bound for 8 seconds, unable to move or bite"),
    "item.mythsofworlds.gleipnir.too_soon": ("Фенрир только что вырвался, путы не держат его", "Fenrir has only just torn loose, the fetter will not hold"),
    "item.mythsofworlds.surtr_sword": ("Пламенный меч Сурта", "Flaming Sword of Surtr"),
    "item.mythsofworlds.surtr_sword.desc": ("Каждый удар поджигает врага", "Every blow sets the foe on fire"),
    "entity.mythsofworlds.draugr": ("Драугр", "Draugr"),
    "entity.mythsofworlds.warg": ("Варг", "Warg"),
    "entity.mythsofworlds.troll": ("Тролль", "Troll"),
    "entity.mythsofworlds.frost_giant": ("Инеистый великан", "Frost Giant"),
    "entity.mythsofworlds.fire_giant": ("Огненный великан", "Fire Giant"),
    "entity.mythsofworlds.raven": ("Ворон", "Raven"),
    "entity.mythsofworlds.norse_merchant": ("Торговец викингов", "Viking Trader"),
    "entity.mythsofworlds.draugr_chieftain": ("Курганный король", "Barrow-King"),
    "entity.mythsofworlds.garm": ("Гарм", "Garm"),
    "entity.mythsofworlds.thrym": ("Трюм, король ётунов", "Thrym, King of the Jotnar"),
    "entity.mythsofworlds.fenrir": ("Фенрир", "Fenrir"),
    "entity.mythsofworlds.surtr": ("Сурт", "Surtr"),
}
MOB_NAMES_RU = {
    "draugr": "драугра", "warg": "варга", "troll": "тролля", "frost_giant": "инеистого великана",
    "fire_giant": "огненного великана", "raven": "ворона", "norse_merchant": "торговца викингов",
    "draugr_chieftain": "курганного короля", "garm": "Гарма", "thrym": "Трюма", "fenrir": "Фенрира", "surtr": "Сурта",
}


def lang():
    import journal_norse
    entries = dict(LANG)
    entries.update(g.journal("norse", journal_norse.INTRO, journal_norse.ENTRIES))
    for name in MOBS:
        en = LANG[f"entity.{NS}.{name}"][1].split(",")[0]
        entries[f"item.{NS}.{name}_spawn_egg"] = (f"Яйцо призыва {MOB_NAMES_RU[name]}", f"{en} Spawn Egg")
    for name, spec in BIOMES.items():
        entries[f"biome.{NS}.{name}"] = (spec["ru"], spec["en"])
    for index, code in ((0, "ru_ru"), (1, "en_us")):
        path = assets("lang", f"{code}.json")
        with open(path, encoding="utf-8") as f:
            current = json.load(f)
        for key, values in entries.items():
            current[key] = values[index]
        write_json(path, current)


# ====================================================================== textures

def textures():
    import textures_norse as tx
    for folder, table in (("block", tx.BLOCKS), ("entity", tx.ENTITIES)):
        os.makedirs(assets("textures", folder), exist_ok=True)
        for name, fn in table.items():
            tx.save(fn(random.Random(name)), assets("textures", folder, f"{name}.png"))
    os.makedirs(assets("textures", "item"), exist_ok=True)
    for name, fn in tx.ITEMS.items():
        tx.save(tx.item(fn, random.Random(name)), assets("textures", "item", f"{name}.png"))


def main():
    write_json(data("dimension_type", "jotunheim.json"), g.dimension_type())
    jotunheim_noise_settings()
    write_json(data("dimension", "jotunheim.json"),
               g.dimension("jotunheim", g.multi_noise([(f"{NS}:{name}", spec["point"]) for name, spec in BIOMES.items()]),
                           settings=f"{NS}:jotunheim"))
    for name, spec in BIOMES.items():
        write_json(data("worldgen", "biome", f"{name}.json"), g.biome_json(spec, FEATURE_ORDER))
    features()
    worldgen_structures()
    loot()
    recipes()
    models()
    lang()
    if "--textures" in sys.argv:
        textures()


if __name__ == "__main__":
    main()
