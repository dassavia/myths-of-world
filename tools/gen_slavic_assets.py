"""
Generates the data and asset files of the Slavic mythology: Nav, the world under the roots of the World Tree, its
biomes, structures, loot, recipes, models, translations and the tales of Boyan. Uses the helpers of
gen_greek_assets.py.

    python3 tools/gen_slavic_assets.py            # everything except textures
    python3 tools/gen_slavic_assets.py --textures # also (re)draw the PNGs, overwriting them

Run it after gen_norse_assets.py (it reuses the basalt spires and magma patches of Muspelheim, and all scripts merge
their translations and tags into the same files).
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_greek_assets as g  # noqa: E402
import structures_slavic  # noqa: E402
from gen_greek_assets import (NS, SAPLING_OK, _above, _biome, _block, _if, _noise, _seq, FLOOR, STEEP,  # noqa: E402
                              UNDER_FLOOR, assets, chest, data, entry, mob, simple, spawn, state, surface_placement,
                              write_json)

# ====================================================================== dimension

def nav_surface():
    """Surface rules of Nav, tried before the vanilla ones: mud and moss in the bog, black stone and magma along the
    fiery river Smorodina, grey soul soil in the realm of Koschei, dry earth in the wild field, sand under the sea."""
    not_above = lambda y: {"type": "minecraft:not", "invert": _above(y)}  # noqa: E731
    return _if({"type": "minecraft:above_preliminary_surface"}, _seq(
        _if(_biome("kikimora_bog"), _seq(
            _if(FLOOR, _seq(_if(_noise(0.2, 4.0), _block("minecraft:mud")),
                            _if(_noise(-4.0, -0.4), _block("minecraft:moss_block")))),
            _if(UNDER_FLOOR, _block("minecraft:mud")))),
        _if(_biome("smorodina"), _seq(
            _if(FLOOR, _seq(_if(STEEP, _block("minecraft:basalt")), _if(_noise(0.3, 4.0), _block("minecraft:magma_block")),
                            _if(_noise(-4.0, -0.25), _block("minecraft:basalt")), _block("minecraft:blackstone"))),
            _if(UNDER_FLOOR, _block("minecraft:blackstone")))),
        _if(_biome("koschei_realm"), _seq(
            _if(FLOOR, _seq(_if(STEEP, _block("minecraft:deepslate")), _if(_noise(0.1, 4.0), _block("minecraft:soul_soil")),
                            _if(_noise(-4.0, -0.4), _block("minecraft:coarse_dirt")), _block("minecraft:podzol"))),
            _if(UNDER_FLOOR, _block("minecraft:soul_soil")))),
        _if(_biome("wild_field"), _if(FLOOR, _if(_noise(0.45, 4.0), _block("minecraft:coarse_dirt")))),
        _if(_biome("dense_forest"), _if(FLOOR, _seq(
            _if(_noise(0.3, 4.0), _block("minecraft:podzol")),
            _if(_noise(-4.0, -0.5), _block("minecraft:moss_block"))))),
        _if(_biome("okiyan_sea"), _if(UNDER_FLOOR, _seq(_if(_noise(0.2, 4.0), _block("minecraft:gravel")),
                                                        _block("minecraft:sand")))),
        _if(_biome("birch_grove", "wild_field"), _if(FLOOR, _if(not_above(63), _block("minecraft:sand"))))))


def nav_noise_settings():
    """The terrain of the Overworld: forests, fields and hills, as in the tales."""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vanilla", "overworld_noise_settings.json"),
              encoding="utf-8") as f:
        settings = json.load(f)
    settings["surface_rule"]["sequence"].insert(1, nav_surface())
    write_json(data("worldgen", "noise_settings", "nav.json"), settings)


# ====================================================================== biomes

FEATURE_ORDER = [
    [],
    ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface"],
    ["minecraft:forest_rock"],
    ["minecraft:monster_room", "minecraft:monster_room_deep"],
    [f"{NS}:basalt_spire", f"{NS}:nav_dead_trunk", f"{NS}:nav_bone_pile"],
    [],
    g.COMMON_ORES + [f"{NS}:muspel_magma", f"{NS}:nav_bog_mud"] + g.DISKS + [f"{NS}:ore_bulat"],
    [],
    ["minecraft:spring_water", "minecraft:spring_lava"],
    ["minecraft:glow_lichen", f"{NS}:nav_old_oak", "minecraft:dark_forest_vegetation", "minecraft:birch_tall",
     "minecraft:trees_birch", "minecraft:trees_swamp", "minecraft:trees_plains", "minecraft:forest_flowers",
     "minecraft:flower_default", "minecraft:flower_plains", "minecraft:flower_swamp", "minecraft:patch_sunflower",
     "minecraft:patch_pumpkin", "minecraft:patch_grass_forest", "minecraft:patch_grass_plain", "minecraft:patch_tall_grass_2",
     "minecraft:patch_large_fern", "minecraft:patch_berry_common", "minecraft:patch_dead_bush",
     "minecraft:brown_mushroom_normal", "minecraft:red_mushroom_normal", "minecraft:brown_mushroom_swamp",
     "minecraft:red_mushroom_swamp", "minecraft:patch_sugar_cane_swamp", "minecraft:patch_waterlily",
     "minecraft:seagrass_swamp", "minecraft:seagrass_normal", "minecraft:kelp_warm"],
    ["minecraft:freeze_top_layer"],
]
COMMON = g.COMMON + [f"{NS}:ore_bulat"]


def music(name):
    return (f"minecraft:music.{name}", 12000, 24000)


BIOMES = {
    "dense_forest": {
        "ru": "Дремучий лес", "en": "Dense Forest",
        "point": {"c": 0.3, "h": 0.5, "t": 0.0},
        "temperature": 0.6, "downfall": 0.8,
        "sky": 0x6A5A8A, "fog": 0x6E6A7A, "water": 0x3A5A6A, "water_fog": 0x0A1A20, "grass": 0x4E7A3A, "foliage": 0x3E6A2E,
        "particle": ("minecraft:spore_blossom_air", 0.004), "music": music("overworld.forest"),
        "features": COMMON + ["minecraft:forest_rock", f"{NS}:nav_old_oak", "minecraft:dark_forest_vegetation",
                              "minecraft:patch_grass_forest", "minecraft:patch_large_fern", "minecraft:patch_berry_common",
                              "minecraft:brown_mushroom_normal", "minecraft:red_mushroom_normal"],
        "spawners": {
            "monster": [spawn(f"{NS}:leshy", 15, 1, 1), spawn(f"{NS}:volkolak", 25, 1, 2), spawn(f"{NS}:upyr", 40, 1, 3),
                        spawn("minecraft:spider", 40, 1, 2), spawn("minecraft:skeleton", 30, 1, 2), spawn("minecraft:zombie", 30, 1, 2)],
            "creature": [spawn(f"{NS}:firebird", 2, 1, 1), spawn("minecraft:wolf", 6, 2, 4), spawn("minecraft:fox", 6, 1, 3),
                         spawn("minecraft:rabbit", 4, 2, 3)],
        },
    },
    "birch_grove": {
        "ru": "Берёзовая роща", "en": "Birch Grove",
        "point": {"c": 0.3, "h": -0.1, "t": 0.2},
        "temperature": 0.6, "downfall": 0.6,
        "sky": 0x8A7AAA, "fog": 0xB0A0C0, "water": 0x3F76E4, "water_fog": 0x050533, "grass": 0x88BB67, "foliage": 0x6BA941,
        "particle": ("minecraft:end_rod", 0.0004), "music": music("overworld.meadow"),  # pale lights between the birches
        "features": COMMON + ["minecraft:birch_tall", "minecraft:trees_birch", "minecraft:forest_flowers",
                              "minecraft:flower_default", "minecraft:patch_grass_forest"],
        "spawners": {
            "monster": [spawn(f"{NS}:upyr", 30, 1, 2), spawn("minecraft:zombie", 40, 1, 3), spawn("minecraft:skeleton", 30, 1, 2),
                        spawn("minecraft:creeper", 30, 1, 2), spawn(f"{NS}:rusalka", 8, 1, 1)],
            "creature": [spawn(f"{NS}:firebird", 5, 1, 2), spawn("minecraft:rabbit", 6, 2, 3), spawn("minecraft:sheep", 8, 2, 4),
                         spawn("minecraft:cow", 6, 2, 4)],
        },
    },
    "kikimora_bog": {
        "ru": "Кикиморино болото", "en": "Kikimora Bog",
        "point": {"c": 0.2, "e": 0.7, "h": 0.8},
        "temperature": 0.7, "downfall": 0.9,
        "sky": 0x5A6A5A, "fog": 0x7A8A6E, "water": 0x4A5A2A, "water_fog": 0x1A220A, "grass": 0x6A7A3A, "foliage": 0x5A6A2E,
        "particle": ("minecraft:mycelium", 0.02), "music": music("overworld.swamp"),
        "features": COMMON + [f"{NS}:nav_bog_mud", f"{NS}:nav_dead_trunk", "minecraft:trees_swamp", "minecraft:patch_waterlily",
                              "minecraft:flower_swamp", "minecraft:brown_mushroom_swamp", "minecraft:red_mushroom_swamp",
                              "minecraft:patch_sugar_cane_swamp", "minecraft:seagrass_swamp"],
        "spawners": {
            "monster": [spawn(f"{NS}:kikimora", 60, 1, 3), spawn(f"{NS}:rusalka", 30, 1, 2), spawn("minecraft:slime", 30, 1, 2),
                        spawn("minecraft:witch", 10, 1, 1), spawn("minecraft:zombie", 20, 1, 2)],
            "creature": [spawn("minecraft:frog", 10, 2, 5)],
        },
    },
    "wild_field": {
        "ru": "Дикое поле", "en": "Wild Field",
        "point": {"c": 0.4, "h": -0.6, "t": 0.4},
        "temperature": 0.8, "downfall": 0.4,
        "sky": 0x9A7AA0, "fog": 0xC8A8B0, "water": 0x3F76E4, "water_fog": 0x050533, "grass": 0x9ABE5A, "foliage": 0x7EA84A,
        "music": music("overworld.meadow"),
        "features": COMMON + ["minecraft:trees_plains", "minecraft:flower_plains", "minecraft:patch_sunflower",
                              "minecraft:patch_pumpkin", "minecraft:patch_grass_plain", "minecraft:patch_tall_grass_2"],
        "spawners": {
            "monster": [spawn(f"{NS}:volkolak", 40, 1, 3), spawn("minecraft:zombie", 40, 1, 3), spawn("minecraft:skeleton", 40, 1, 2),
                        spawn("minecraft:creeper", 30, 1, 2)],
            "creature": [spawn("minecraft:horse", 6, 2, 4), spawn("minecraft:cow", 8, 2, 4), spawn("minecraft:sheep", 8, 2, 4)],
        },
    },
    "smorodina": {
        "ru": "Огненная река Смородина", "en": "Fiery River Smorodina",
        "point": {"c": 0.6, "t": 0.8, "h": -0.8, "w": -0.6},
        "temperature": 2.0, "downfall": 0.0, "precipitation": False,
        "sky": 0xA04A3A, "fog": 0x5A2A20, "water": 0xE0602A, "water_fog": 0x601A0A, "grass": 0x8A5A2A, "foliage": 0x6A3A1A,
        "particle": ("minecraft:ash", 0.02), "music": ("minecraft:music.nether.basalt_deltas", 12000, 24000),
        "additions": ("minecraft:ambient.basalt_deltas.additions", 0.0111),
        "features": COMMON + ["minecraft:lake_lava_surface", "minecraft:lake_lava_underground", f"{NS}:muspel_magma",
                              f"{NS}:basalt_spire", "minecraft:patch_dead_bush"],
        "spawners": {
            "monster": [spawn("minecraft:magma_cube", 50, 1, 3), spawn("minecraft:blaze", 10, 1, 2), spawn("minecraft:skeleton", 20, 1, 2)],
        },
    },
    "koschei_realm": {
        "ru": "Кощеево царство", "en": "Realm of Koschei",
        "point": {"c": 0.6, "t": -0.7, "w": 0.6, "e": -0.4},
        "temperature": 0.2, "downfall": 0.3,
        "sky": 0x3A3048, "fog": 0x4A4058, "water": 0x2A2A4A, "water_fog": 0x0A0A1A, "grass": 0x6A6A5A, "foliage": 0x5A5A4A,
        "particle": ("minecraft:soul", 0.004), "music": music("overworld.deep_dark"),
        "additions": ("minecraft:ambient.soul_sand_valley.additions", 0.0111),
        "features": COMMON + [f"{NS}:nav_dead_trunk", f"{NS}:nav_bone_pile", "minecraft:patch_dead_bush"],
        "spawners": {
            "monster": [spawn(f"{NS}:upyr", 80, 2, 4), spawn("minecraft:skeleton", 60, 1, 3), spawn(f"{NS}:volkolak", 20, 1, 2),
                        spawn("minecraft:wither_skeleton", 5, 1, 1)],
        },
    },
    "okiyan_sea": {
        "ru": "Море-Окиян", "en": "Sea-Okiyan",
        "point": {"c": -0.6},
        "temperature": 0.5, "downfall": 0.5,
        "sky": 0x6A6AA0, "fog": 0x9A9AC0, "water": 0x2E5B9A, "water_fog": 0x051E3E, "grass": 0x79A36A, "foliage": 0x5E8A52,
        "features": COMMON + g.DISKS + ["minecraft:seagrass_normal", "minecraft:kelp_warm"],
        "spawners": {
            "monster": [spawn(f"{NS}:rusalka", 30, 1, 2), spawn("minecraft:drowned", 40, 1, 3)],
            "water_creature": [spawn("minecraft:squid", 6, 1, 4)],
            "water_ambient": [spawn("minecraft:cod", 15, 3, 6), spawn("minecraft:salmon", 15, 1, 5)],
        },
    },
}


def features():
    # Ancient oaks of the deep forest, huge and gnarled.
    g.tree("nav_old_oak", "minecraft:oak_log", "minecraft:oak_leaves",
           {"type": "minecraft:fancy_trunk_placer", "base_height": 10, "height_rand_a": 5, "height_rand_b": 0},
           {"type": "minecraft:fancy_foliage_placer", "radius": 3, "offset": 4, "height": 4}, count=2)

    def column(name, layers, rarity, extra=None):
        write_json(data("worldgen", "configured_feature", f"{name}.json"), {"type": "minecraft:block_column", "config": {
            "layers": [{"height": {"type": "minecraft:uniform", "min_inclusive": lo, "max_inclusive": hi}, "provider": provider}
                       for lo, hi, provider in layers],
            "direction": "up", "allowed_placement": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
            "prioritize_tip": True}})
        write_json(data("worldgen", "placed_feature", f"{name}.json"),
                   {"feature": f"{NS}:{name}", "placement": surface_placement(rarity=rarity, extra=extra)})

    # Dead black trunks in the bog and around the castle of Koschei; heaps of bones in his realm.
    column("nav_dead_trunk", [(2, 6, simple("minecraft:stripped_dark_oak_log", axis="y"))], 3)
    column("nav_bone_pile", [(1, 2, simple("minecraft:bone_block", axis="y"))], 6)

    write_json(data("worldgen", "configured_feature", "nav_bog_mud.json"), {
        "type": "minecraft:vegetation_patch",
        "config": {
            "replaceable": "#minecraft:moss_replaceable",
            "ground_state": {"type": "minecraft:weighted_state_provider", "entries": [
                {"weight": 3, "data": state("minecraft:mud")}, {"weight": 2, "data": state("minecraft:moss_block")}]},
            "vegetation_feature": {"feature": {"type": "minecraft:simple_block", "config": {"to_place": simple("minecraft:moss_carpet")}},
                                   "placement": []},
            "surface": "floor", "depth": 1, "extra_bottom_block_chance": 0.0, "vertical_range": 5,
            "vegetation_chance": 0.3, "xz_radius": {"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 5},
            "extra_edge_column_chance": 0.3,
        },
    })
    write_json(data("worldgen", "placed_feature", "nav_bog_mud.json"), {"feature": f"{NS}:nav_bog_mud", "placement": [
        {"type": "minecraft:count", "count": 2}, {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "WORLD_SURFACE_WG"}, {"type": "minecraft:biome"}]})


# ====================================================================== structures

STRUCTURES = {
    # Lairs of Solovei, Zmey Gorynych and Koschei: one set, so that they never stand close together.
    "solovei_nest": (["dense_forest", "birch_grove"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "kalinov_bridge": (["smorodina"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "koschei_castle": (["koschei_realm"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    # Villages, huts and shrines.
    "slavic_village": (["wild_field", "birch_grove", "dense_forest"], 30, 12, 2560201, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "baba_yaga_hut": (["dense_forest", "kikimora_bog", "birch_grove"], 28, 10, 2560202, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "kapishche": (["birch_grove", "wild_field", "dense_forest"], 26, 10, 2560203, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "koschei_oak": (["koschei_realm", "kikimora_bog", "dense_forest"], 26, 10, 2560204, "WORLD_SURFACE_WG", 0, "beard_thin"),
}
LAIRS = {"structures": {"solovei_nest": 3, "kalinov_bridge": 3, "koschei_castle": 3},
         "spacing": 48, "separation": 30, "salt": 2560300}


def worldgen_structures():
    os.makedirs(data("structure", "slavic"), exist_ok=True)
    for name, (biomes, spacing, separation, salt, heightmap, offset, adaptation) in STRUCTURES.items():
        structures_slavic.STRUCTURES[name]().save(data("structure", "slavic", f"{name}.nbt"))
        write_json(data("tags", "worldgen", "biome", "has_structure", f"{name}.json"),
                   {"replace": False, "values": [f"{NS}:{b}" for b in biomes]})
        write_json(data("worldgen", "template_pool", "slavic", name, "start.json"), {
            "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {
                "element_type": "minecraft:single_pool_element",
                "location": f"{NS}:slavic/{name}",
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
            "start_pool": f"{NS}:slavic/{name}/start",
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
    write_json(data("worldgen", "structure_set", "slavic_lairs.json"), {
        "structures": [{"structure": f"{NS}:{name}", "weight": w} for name, w in LAIRS["structures"].items()],
        "placement": {"type": "minecraft:random_spread", "spacing": LAIRS["spacing"], "separation": LAIRS["separation"],
                      "salt": LAIRS["salt"]},
    })


# ====================================================================== loot

def loot():
    gold = [entry("minecraft:gold_ingot", 8, 1, 4), entry("minecraft:gold_nugget", 10, 3, 9), entry("minecraft:emerald", 6, 1, 4)]
    chest("slavic_village", (3, 6), gold + [
        entry(f"{NS}:karavai", 8, 1, 3), entry("minecraft:bread", 8, 2, 5), entry("minecraft:honey_bottle", 6, 1, 3),
        entry("minecraft:iron_axe", 4, enchant=True), entry("minecraft:white_wool", 6, 1, 4), entry("minecraft:string", 6, 2, 6),
        entry(f"{NS}:world_tree_acorn", 1),
    ])
    chest("slavic_izba", (3, 6), [
        entry("minecraft:wheat", 8, 2, 6), entry("minecraft:beetroot", 6, 2, 6), entry("minecraft:potato", 6, 2, 6),
        entry("minecraft:honey_bottle", 4, 1, 2), entry(f"{NS}:karavai", 4, 1, 2), entry("minecraft:iron_ingot", 4, 1, 3),
        entry("minecraft:sweet_berries", 6, 2, 6), entry("minecraft:candle", 4, 1, 3),
    ])
    chest("baba_yaga_hut", (3, 6), [
        entry(f"{NS}:living_water", 3), entry(f"{NS}:dead_water", 3), entry("minecraft:bone", 10, 2, 8),
        entry("minecraft:spider_eye", 6, 1, 3), entry("minecraft:fermented_spider_eye", 4, 1, 2), entry("minecraft:glass_bottle", 6, 1, 4),
        entry("minecraft:mushroom_stew", 4), entry("minecraft:book", 3, enchant=True), entry(f"{NS}:world_tree_acorn", 2),
    ])
    chest("kapishche", (2, 5), [
        entry("minecraft:honey_bottle", 8, 1, 3), entry(f"{NS}:karavai", 8, 1, 2), entry("minecraft:gold_ingot", 6, 1, 3),
        entry("minecraft:honeycomb", 6, 1, 4), entry(f"{NS}:firebird_feather", 3),
        entry("minecraft:book", 3, enchant=True), entry(f"{NS}:world_tree_acorn", 2),
    ])
    # The chest on the old oak always holds the egg with Koschei's death.
    chest("koschei_oak", (2, 4), gold + [entry("minecraft:bone", 6, 2, 6), entry("minecraft:feather", 6, 1, 4)],
          bonus=[entry(f"{NS}:koschei_egg", 1)])
    chest("solovei_nest", (4, 7), gold + [
        entry("minecraft:gold_ingot", 6, 2, 6), entry("minecraft:iron_sword", 4, enchant=True), entry("minecraft:saddle", 3),
        entry("minecraft:leather_boots", 3, enchant=True), entry("minecraft:diamond", 3, 1, 2), entry("minecraft:feather", 8, 2, 6),
        entry(f"{NS}:karavai", 4, 1, 2),
    ])
    chest("kalinov_bridge", (4, 8), gold + [
        entry("minecraft:diamond", 4, 1, 3), entry("minecraft:blaze_rod", 6, 1, 4), entry(f"{NS}:zmey_scale", 4, 1, 2),
        entry("minecraft:netherite_scrap", 2), entry("minecraft:golden_apple", 3), entry("minecraft:fire_charge", 6, 2, 6),
        entry(f"{NS}:living_water", 2),
    ])
    chest("koschei_castle", (4, 8), gold + [
        entry("minecraft:diamond", 4, 1, 3), entry("minecraft:gold_block", 3), entry("minecraft:echo_shard", 3),
        entry("minecraft:book", 4, enchant=True), entry("minecraft:golden_apple", 3), entry(f"{NS}:dead_water", 3),
        entry(f"{NS}:living_water", 3), entry("minecraft:soul_lantern", 4, 1, 3),
    ])

    mob("leshy", [("minecraft:oak_log", 1, 4, None), ("minecraft:moss_block", 0, 2, None), ("minecraft:oak_sapling", 0, 2, None),
                  (f"{NS}:world_tree_acorn", 1, 1, 0.08)])
    mob("kikimora", [("minecraft:slime_ball", 0, 2, None), ("minecraft:string", 0, 2, None), ("minecraft:moss_carpet", 0, 2, None)])
    mob("upyr", [(f"{NS}:upyr_fang", 0, 2, None), ("minecraft:rotten_flesh", 0, 2, None), ("minecraft:bone", 0, 1, None)])
    mob("volkolak", [(f"{NS}:volkolak_pelt", 1, 1, 0.5), ("minecraft:leather", 0, 2, None), ("minecraft:bone", 0, 2, None)])
    mob("rusalka", [("minecraft:prismarine_crystals", 0, 2, None), ("minecraft:kelp", 0, 3, None), ("minecraft:nautilus_shell", 1, 1, 0.05)])
    mob("firebird", [(f"{NS}:firebird_feather", 1, 2, None)])
    mob("slavic_merchant", [])
    mob("solovei", [(f"{NS}:skorokhody", 1, 1, None), ("minecraft:gold_ingot", 3, 8, None), ("minecraft:emerald", 2, 6, None)])
    mob("zmey_gorynych", [(f"{NS}:kladenets", 1, 1, None), (f"{NS}:zmey_scale", 3, 6, None), ("minecraft:diamond", 2, 4, None),
                          ("minecraft:gold_ingot", 4, 10, None)])
    mob("koschei", [(f"{NS}:shapka_nevidimka", 1, 1, None), ("minecraft:gold_block", 1, 3, None), ("minecraft:diamond", 2, 4, None),
                    ("minecraft:netherite_scrap", 1, 2, None)])


# ====================================================================== recipes and tags

def recipes():
    def shapeless(name, ingredients, result, count=1, category="misc"):
        write_json(data("recipe", f"{name}.json"), {
            "type": "minecraft:crafting_shapeless", "category": category,
            "ingredients": [{"item": i} if not i.startswith("#") else {"tag": i[1:]} for i in ingredients],
            "result": {"id": result, "count": count}})

    # The acorn of the World Tree: a sapling, gold for the sun, glow berries for the light below, the Minotaur's horn as proof of a hero.
    shapeless("world_tree_acorn", ["minecraft:oak_sapling", "minecraft:gold_ingot", "minecraft:glow_berries",
                                   f"{NS}:minotaur_horn"], f"{NS}:world_tree_acorn")
    shapeless("slavic_journal", ["minecraft:book", "minecraft:feather", "minecraft:oak_sapling"], f"{NS}:slavic_journal")
    shapeless("karavai", ["minecraft:wheat", "minecraft:wheat", "minecraft:wheat", "minecraft:egg", "minecraft:honey_bottle"],
              f"{NS}:karavai", 2, "misc")
    g.add_tag("item", "foot_armor", ["skorokhody"])
    g.add_tag("item", "head_armor", ["shapka_nevidimka"])
    g.add_tag("item", "swords", ["kladenets"])
    # Breathing under water is a tag since 1.20.5 (LivingEntity.canBreatheUnderwater is final).
    g.add_tag("entity_type", "can_breathe_under_water", ["kikimora", "rusalka"])


# ====================================================================== models

ITEMS = ["world_tree_acorn", "slavic_journal", "slavic_journal_complete", "living_water", "dead_water", "karavai",
         "firebird_feather", "upyr_fang", "volkolak_pelt", "zmey_scale", "koschei_egg", "koschei_needle", "kladenets",
         "skorokhody", "shapka_nevidimka"]
HANDHELD = {"kladenets"}
MOBS = ["leshy", "kikimora", "upyr", "volkolak", "rusalka", "firebird", "slavic_merchant", "solovei", "zmey_gorynych", "koschei"]


def models():
    # The hollow: a cube of oak bark with the dark opening on its front (the model faces north).
    write_json(assets("blockstates", "world_tree_hollow.json"), {"variants": {
        f"facing={facing}": {"model": f"{NS}:block/world_tree_hollow", "y": y}
        for facing, y in (("north", 0), ("east", 90), ("south", 180), ("west", 270))}})
    write_json(assets("models", "block", "world_tree_hollow.json"), {
        "parent": "minecraft:block/orientable",
        "textures": {"front": f"{NS}:block/world_tree_hollow", "side": "minecraft:block/oak_log",
                     "top": "minecraft:block/oak_log_top", "particle": "minecraft:block/oak_log"}})
    for item in ITEMS:
        parent = "minecraft:item/handheld" if item in HANDHELD else "minecraft:item/generated"
        write_json(assets("models", "item", f"{item}.json"), {"parent": parent, "textures": {"layer0": f"{NS}:item/{item}"}})
    for name in MOBS:
        write_json(assets("models", "item", f"{name}_spawn_egg.json"), {"parent": "minecraft:item/template_spawn_egg"})


# ====================================================================== translations

LANG = {
    "block.mythsofworlds.world_tree_hollow": ("Дупло Мирового древа", "Hollow of the World Tree"),
    "item.mythsofworlds.world_tree_acorn": ("Жёлудь Мирового древа", "Acorn of the World Tree"),
    "item.mythsofworlds.world_tree_acorn.desc": (
        "Посадите на землю (ПКМ по верху травы или земли): вырастет великий дуб с дуплом, ведущим в Навь",
        "Plant it on earth (right-click the top of grass or dirt): a great oak grows with a hollow that leads to Nav"),
    "item.mythsofworlds.world_tree_acorn.no_room": ("Дубу здесь тесно: нужно место 3x3 и высота 11 блоков",
                                                    "No room for the oak: it needs a 3x3 space 11 blocks high"),
    "item.mythsofworlds.world_tree_acorn.grown": ("Мировое древо поднялось! Войдите в дупло, чтобы спуститься в Навь",
                                                  "The World Tree has risen! Step into the hollow to go down to Nav"),
    "item.mythsofworlds.slavic_journal": ("Сказы Бояна", "Tales of Boyan"),
    "item.mythsofworlds.slavic_journal_complete": ("Сказы Бояна (полные)", "Tales of Boyan (complete)"),
    "item.mythsofworlds.living_water": ("Живая вода", "Water of Life"),
    "item.mythsofworlds.dead_water": ("Мёртвая вода", "Dead Water"),
    "item.mythsofworlds.karavai": ("Каравай", "Karavai"),
    "item.mythsofworlds.firebird_feather": ("Перо Жар-птицы", "Firebird Feather"),
    "item.mythsofworlds.upyr_fang": ("Клык упыря", "Upyr Fang"),
    "item.mythsofworlds.volkolak_pelt": ("Шкура волколака", "Volkolak Pelt"),
    "item.mythsofworlds.zmey_scale": ("Чешуя Змея Горыныча", "Scale of Zmey Gorynych"),
    "item.mythsofworlds.koschei_egg": ("Яйцо Кощея", "Koschei's Egg"),
    "item.mythsofworlds.koschei_egg.desc": ("ПКМ: разбить. В яйце игла, а на конце её смерть Кощеева",
                                            "Right-click to break it. Inside is a needle, and at its tip the death of Koschei"),
    "item.mythsofworlds.koschei_egg.broken": ("Яйцо разбилось, и на ладонь упала игла. Носите её с собой, когда пойдёте на Кощея",
                                              "The egg breaks and a needle falls into your hand. Carry it when you go against Koschei"),
    "item.mythsofworlds.koschei_needle": ("Кощеева игла", "Koschei's Needle"),
    "item.mythsofworlds.kladenets": ("Меч-кладенец", "Sword Kladenets"),
    "item.mythsofworlds.kladenets.desc": ("Каждый удар рубит и врагов вокруг (урон 6 в 3 блоках)",
                                          "Every blow also cuts the foes around (6 damage within 3 blocks)"),
    "item.mythsofworlds.skorokhody": ("Сапоги-скороходы", "Seven-League Boots"),
    "item.mythsofworlds.skorokhody.desc": ("Скорость III и прыжок", "Speed III and Jump Boost"),
    "item.mythsofworlds.shapka_nevidimka": ("Шапка-невидимка", "Cap of Invisibility"),
    "item.mythsofworlds.shapka_nevidimka.desc": ("Пока вы крадётесь (Shift), вас не видно", "While you sneak, no one can see you"),
    "item.mythsofworlds.relic.slavic": ("Навь: дар из сказок", "Nav: a gift from the tales"),
    "entity.mythsofworlds.leshy": ("Леший", "Leshy"),
    "entity.mythsofworlds.kikimora": ("Кикимора", "Kikimora"),
    "entity.mythsofworlds.upyr": ("Упырь", "Upyr"),
    "entity.mythsofworlds.volkolak": ("Волколак", "Volkolak"),
    "entity.mythsofworlds.rusalka": ("Русалка", "Rusalka"),
    "entity.mythsofworlds.firebird": ("Жар-птица", "Firebird"),
    "entity.mythsofworlds.slavic_merchant": ("Торговец Нави", "Trader of Nav"),
    "entity.mythsofworlds.solovei": ("Соловей-разбойник", "Solovei the Robber"),
    "entity.mythsofworlds.zmey_gorynych": ("Змей Горыныч", "Zmey Gorynych"),
    "entity.mythsofworlds.koschei": ("Кощей Бессмертный", "Koschei the Deathless"),
    "entity.mythsofworlds.koschei.deathless": ("Кощей поднимается снова: смерть его не здесь, а в игле!",
                                               "Koschei rises again: his death is not here, it is in the needle!"),
    "entity.mythsofworlds.koschei.needle_broken": ("Вы ломаете иглу, и Кощей Бессмертный падает замертво!",
                                                   "You break the needle, and Koschei the Deathless falls dead!"),
}
MOB_NAMES_RU = {
    "leshy": "лешего", "kikimora": "кикиморы", "upyr": "упыря", "volkolak": "волколака", "rusalka": "русалки",
    "firebird": "Жар-птицы", "slavic_merchant": "торговца Нави", "solovei": "Соловья-разбойника",
    "zmey_gorynych": "Змея Горыныча", "koschei": "Кощея",
}


def lang():
    import journal_slavic
    entries = dict(LANG)
    entries.update(g.journal("slavic", journal_slavic.INTRO, journal_slavic.with_gear()))
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
    import textures_slavic as tx
    for folder, table in (("block", tx.BLOCKS), ("entity", tx.ENTITIES)):
        os.makedirs(assets("textures", folder), exist_ok=True)
        for name, fn in table.items():
            tx.save(fn(random.Random(name)), assets("textures", folder, f"{name}.png"))
    os.makedirs(assets("textures", "item"), exist_ok=True)
    for name, fn in tx.ITEMS.items():
        tx.save(tx.item(fn, random.Random(name)), assets("textures", "item", f"{name}.png"))
    os.makedirs(assets("textures", "models", "armor"), exist_ok=True)
    for name, fn in tx.LAYERS.items():
        tx.save(fn(random.Random(name + "_layer")), assets("textures", "models", "armor", f"{name}_layer_1.png"))


def main():
    write_json(data("dimension_type", "nav.json"), g.dimension_type(13000))
    nav_noise_settings()
    write_json(data("dimension", "nav.json"),
               g.dimension("nav", g.multi_noise([(f"{NS}:{name}", spec["point"]) for name, spec in BIOMES.items()]),
                           settings=f"{NS}:nav"))
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
