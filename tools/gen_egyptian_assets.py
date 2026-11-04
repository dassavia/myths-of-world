"""
Generates the data and asset files of the Egyptian mythology: the Duat, the desert of everlasting night under the
world, its biomes, structures, loot, recipes, models, translations and the Book of the Dead. Uses the helpers of
gen_greek_assets.py.

    python3 tools/gen_egyptian_assets.py            # everything except textures
    python3 tools/gen_egyptian_assets.py --textures # also (re)draw the PNGs, overwriting them

Run it after gen_slavic_assets.py (it reuses the basalt spires and magma patches of Muspelheim and the bone piles of
Nav, and all scripts merge their translations and tags into the same files) and after gen_metals.py (the ore of
meteoric iron).
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_greek_assets as g  # noqa: E402
import structures_egyptian  # noqa: E402
from gen_greek_assets import (NS, SAPLING_OK, _above, _biome, _block, _if, _noise, _seq, FLOOR, STEEP,  # noqa: E402
                              UNDER_FLOOR, assets, chest, data, entry, mob, simple, spawn, state, surface_placement,
                              write_json)

# ====================================================================== dimension

def duat_surface():
    """Surface rules of the Duat, tried before the vanilla ones: sand over sandstone in the deserts, red sand and
    terracotta in the Valley of the Kings, black stone and magma around the lake of fire, the black silt of the flood
    on the low banks of the Nile and by the water of the oases with mud and grass higher up, grass among the sand of
    the oases, sand under the river."""
    not_above = lambda y: {"type": "minecraft:not", "invert": _above(y)}  # noqa: E731
    return _if({"type": "minecraft:above_preliminary_surface"}, _seq(
        _if(_biome("duat_sands"), _seq(
            _if(FLOOR, _seq(_if(STEEP, _block("minecraft:sandstone")), _block("minecraft:sand"))),
            _if(UNDER_FLOOR, _block("minecraft:sandstone")))),
        _if(_biome("valley_of_kings"), _seq(
            _if(FLOOR, _seq(_if(STEEP, _block("minecraft:orange_terracotta")),
                            _if(_noise(0.35, 4.0), _block("minecraft:terracotta")), _block("minecraft:red_sand"))),
            _if(UNDER_FLOOR, _seq(_if(_noise(-0.1, 4.0), _block("minecraft:red_sandstone")),
                                  _block("minecraft:orange_terracotta"))))),
        _if(_biome("lake_of_fire"), _seq(
            _if(FLOOR, _seq(_if(STEEP, _block("minecraft:basalt")), _if(_noise(0.3, 4.0), _block("minecraft:magma_block")),
                            _if(_noise(-4.0, -0.25), _block("minecraft:basalt")), _block("minecraft:blackstone"))),
            _if(UNDER_FLOOR, _block("minecraft:blackstone")))),
        _if(_biome("oasis"), _seq(
            _if(FLOOR, _seq(_if(not_above(64), _block(f"{NS}:nile_silt")),
                            _if(_noise(-0.15, 4.0), _block("minecraft:grass_block")), _block("minecraft:sand"))),
            _if(UNDER_FLOOR, _block("minecraft:sand")))),
        # The black silt the flood leaves on the low banks of the Nile and on its bed, mud a little higher up.
        _if(_biome("nile_banks"), _seq(
            _if(FLOOR, _seq(_if(not_above(66), _block(f"{NS}:nile_silt")), _if(_noise(0.45, 4.0), _block("minecraft:mud")))))),
        _if(_biome("celestial_nile"), _if(UNDER_FLOOR, _seq(_if(_noise(0.3, 4.0), _block("minecraft:clay")),
                                                            _block("minecraft:sand"))))))


def duat_noise_settings():
    """The terrain of the Overworld, sand and stone in place of grass: dunes, valleys and the river."""
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vanilla", "overworld_noise_settings.json"),
              encoding="utf-8") as f:
        settings = json.load(f)
    settings["surface_rule"]["sequence"].insert(1, duat_surface())
    write_json(data("worldgen", "noise_settings", "duat.json"), settings)


def duat_dimension_type():
    """Everlasting night (the sun is on the other side of the world while Ra sails through the Duat), with a faint
    starlight so that the desert can be crossed."""
    value = g.dimension_type(18000)
    value["ambient_light"] = 0.08
    return value


# ====================================================================== biomes

FEATURE_ORDER = [
    [],
    ["minecraft:lake_lava_underground", "minecraft:lake_lava_surface"],
    ["minecraft:amethyst_geode"],
    ["minecraft:monster_room", "minecraft:monster_room_deep", "minecraft:fossil_upper", "minecraft:fossil_lower"],
    ["minecraft:desert_well", f"{NS}:basalt_spire", f"{NS}:nav_bone_pile", f"{NS}:duat_ruin_column"],
    [],
    g.COMMON_ORES + [f"{NS}:muspel_magma"] + g.DISKS + [f"{NS}:disk_nile_silt", f"{NS}:ore_meteoric_iron"],
    [],
    ["minecraft:spring_water", "minecraft:spring_lava"],
    ["minecraft:glow_lichen", f"{NS}:date_palm", f"{NS}:date_palm_grove", "minecraft:trees_savanna",
     "minecraft:flower_default", "minecraft:flower_plains", "minecraft:patch_sunflower", "minecraft:patch_grass_savanna",
     "minecraft:patch_tall_grass", "minecraft:patch_dead_bush_2", "minecraft:patch_dead_bush_badlands",
     "minecraft:patch_melon", "minecraft:patch_pumpkin", "minecraft:patch_sugar_cane_desert",
     "minecraft:patch_sugar_cane", "minecraft:patch_cactus_desert", "minecraft:patch_cactus_decorated",
     "minecraft:patch_waterlily", "minecraft:seagrass_river", "minecraft:seagrass_warm", "minecraft:warm_ocean_vegetation"],
    ["minecraft:freeze_top_layer"],
]
COMMON = g.COMMON + [f"{NS}:ore_meteoric_iron"]


def music(name):
    return (f"minecraft:music.{name}", 12000, 24000)


BIOMES = {
    "duat_sands": {
        "ru": "Пески Дуата", "en": "Sands of the Duat",
        "point": {"c": 0.3, "t": 0.6, "h": -0.6},
        "temperature": 2.0, "downfall": 0.0, "precipitation": False,
        "sky": 0x1A1A4A, "fog": 0x3A3058, "water": 0x3A6AB8, "water_fog": 0x0A1A3A, "grass": 0xBFB755, "foliage": 0xAEA42A,
        "particle": ("minecraft:white_ash", 0.006), "music": music("overworld.desert"),
        "features": COMMON + ["minecraft:fossil_upper", "minecraft:fossil_lower", "minecraft:desert_well",
                              f"{NS}:duat_ruin_column", f"{NS}:date_palm", "minecraft:patch_dead_bush_2",
                              "minecraft:patch_cactus_desert"],
        "spawners": {
            "monster": [spawn(f"{NS}:scarab", 50, 2, 4), spawn(f"{NS}:mummy", 40, 1, 3), spawn(f"{NS}:scorpion", 25, 1, 2),
                        spawn(f"{NS}:jackal", 20, 2, 3), spawn("minecraft:husk", 20, 1, 3), spawn("minecraft:skeleton", 10, 1, 2)],
            "creature": [spawn("minecraft:camel", 4, 1, 2), spawn("minecraft:rabbit", 4, 2, 3)],
        },
    },
    "nile_banks": {
        "ru": "Берега Нила", "en": "Banks of the Nile",
        "point": {"c": 0.1, "h": 0.5, "t": 0.4},
        "temperature": 1.4, "downfall": 0.6,
        "sky": 0x22285A, "fog": 0x3A4A6A, "water": 0x2E7AA8, "water_fog": 0x0A2A3A, "grass": 0x7AB84A, "foliage": 0x5EA83A,
        "music": music("overworld.jungle"),
        "features": COMMON + g.DISKS + [f"{NS}:disk_nile_silt", f"{NS}:date_palm_grove", "minecraft:patch_tall_grass",
                                        "minecraft:flower_default",
                                        "minecraft:patch_melon", "minecraft:patch_sugar_cane", "minecraft:patch_waterlily",
                                        "minecraft:seagrass_river"],
        "spawners": {
            "monster": [spawn(f"{NS}:scarab", 20, 2, 3), spawn(f"{NS}:mummy", 20, 1, 2), spawn(f"{NS}:crocodile", 25, 1, 2),
                        spawn(f"{NS}:jackal", 10, 2, 3), spawn("minecraft:zombie", 10, 1, 2)],
            "creature": [spawn(f"{NS}:bastet_cat", 4, 1, 1), spawn("minecraft:cow", 6, 2, 4), spawn("minecraft:sheep", 6, 2, 4),
                         spawn("minecraft:frog", 4, 2, 4)],
            "water_ambient": [spawn("minecraft:cod", 10, 3, 6), spawn("minecraft:salmon", 10, 1, 5)],
        },
    },
    "fields_of_aaru": {
        "ru": "Поля Иалу", "en": "Fields of Aaru",
        "point": {"c": 0.4, "h": 0.7, "t": 0.2, "w": 0.3},
        "temperature": 1.0, "downfall": 0.5,
        "sky": 0x3A3A7A, "fog": 0x8A80B0, "water": 0x4A8AE8, "water_fog": 0x0A2A4A, "grass": 0xC8C850, "foliage": 0x9AB83A,
        "particle": ("minecraft:end_rod", 0.0006), "music": music("overworld.meadow"),  # the souls of the blessed
        "features": COMMON + [f"{NS}:disk_nile_silt", "minecraft:trees_savanna", f"{NS}:date_palm", "minecraft:flower_plains",
                              "minecraft:patch_sunflower", "minecraft:patch_grass_savanna", "minecraft:patch_pumpkin",
                              "minecraft:patch_sugar_cane", "minecraft:patch_waterlily"],
        "spawners": {
            "monster": [spawn(f"{NS}:scarab", 10, 1, 2), spawn(f"{NS}:mummy", 10, 1, 1)],
            "creature": [spawn(f"{NS}:bastet_cat", 6, 1, 2), spawn("minecraft:cow", 8, 2, 4), spawn("minecraft:sheep", 8, 2, 4),
                         spawn("minecraft:chicken", 6, 2, 4), spawn("minecraft:rabbit", 4, 2, 3)],
        },
    },
    "valley_of_kings": {
        "ru": "Долина царей", "en": "Valley of the Kings",
        "point": {"c": 0.6, "t": 0.7, "e": -0.5, "h": -0.3},
        "temperature": 2.0, "downfall": 0.0, "precipitation": False,
        "sky": 0x2A1A3A, "fog": 0x5A3A3A, "water": 0x3A5A8A, "water_fog": 0x0A1A2A, "grass": 0x9E814D, "foliage": 0x9E814D,
        "particle": ("minecraft:soul", 0.002), "music": music("overworld.badlands"),
        "additions": ("minecraft:ambient.soul_sand_valley.additions", 0.0111),
        "features": COMMON + ["minecraft:fossil_upper", "minecraft:fossil_lower", f"{NS}:duat_ruin_column",
                              f"{NS}:nav_bone_pile", "minecraft:patch_dead_bush_badlands", "minecraft:patch_cactus_decorated"],
        "spawners": {
            "monster": [spawn(f"{NS}:mummy", 60, 1, 3), spawn(f"{NS}:ushabti", 30, 1, 2), spawn(f"{NS}:scorpion", 30, 1, 2),
                        spawn(f"{NS}:jackal", 20, 2, 3), spawn("minecraft:skeleton", 20, 1, 2)],
        },
    },
    "lake_of_fire": {
        "ru": "Огненное озеро", "en": "Lake of Fire",
        "point": {"c": 0.6, "t": 0.9, "w": -0.6, "h": -0.8},
        "temperature": 2.0, "downfall": 0.0, "precipitation": False,
        "sky": 0x5A1A1A, "fog": 0x4A1A10, "water": 0xE0602A, "water_fog": 0x601A0A, "grass": 0x8A5A2A, "foliage": 0x6A3A1A,
        "particle": ("minecraft:ash", 0.02), "music": ("minecraft:music.nether.basalt_deltas", 12000, 24000),
        "additions": ("minecraft:ambient.basalt_deltas.additions", 0.0111),
        "features": COMMON + ["minecraft:lake_lava_surface", "minecraft:lake_lava_underground", f"{NS}:muspel_magma",
                              f"{NS}:basalt_spire", "minecraft:patch_dead_bush_badlands"],
        "spawners": {
            "monster": [spawn("minecraft:magma_cube", 40, 1, 3), spawn(f"{NS}:scarab", 30, 2, 4), spawn("minecraft:blaze", 10, 1, 2)],
        },
    },
    "oasis": {
        "ru": "Оазис", "en": "Oasis",
        "point": {"c": 0.3, "h": 0.2, "t": 0.5, "w": 0.6},
        "temperature": 1.6, "downfall": 0.4,
        "sky": 0x22285A, "fog": 0x3A4A6A, "water": 0x3ABAC8, "water_fog": 0x0A3A4A, "grass": 0x8AC04A, "foliage": 0x6AB03A,
        "particle": ("minecraft:spore_blossom_air", 0.002), "music": music("overworld.desert"),
        "features": COMMON + [f"{NS}:disk_nile_silt", f"{NS}:date_palm_grove", "minecraft:patch_grass_savanna",
                              "minecraft:flower_default", "minecraft:patch_melon", "minecraft:patch_sugar_cane_desert",
                              "minecraft:patch_waterlily"],
        "spawners": {
            "monster": [spawn(f"{NS}:scarab", 15, 1, 3), spawn(f"{NS}:jackal", 15, 2, 3), spawn(f"{NS}:mummy", 10, 1, 2),
                        spawn(f"{NS}:crocodile", 10, 1, 1)],
            "creature": [spawn(f"{NS}:bastet_cat", 4, 1, 1), spawn("minecraft:camel", 4, 1, 2), spawn("minecraft:rabbit", 4, 2, 3)],
        },
    },
    "celestial_nile": {
        "ru": "Небесный Нил", "en": "Celestial Nile",
        "point": {"c": -0.6},
        "temperature": 1.2, "downfall": 0.5,
        "sky": 0x22285A, "fog": 0x4A5A8A, "water": 0x2A5AB0, "water_fog": 0x051E3E, "grass": 0x7AB84A, "foliage": 0x5EA83A,
        "features": COMMON + g.DISKS + [f"{NS}:disk_nile_silt", "minecraft:seagrass_warm", "minecraft:warm_ocean_vegetation"],
        "spawners": {
            "monster": [spawn("minecraft:drowned", 30, 1, 2), spawn(f"{NS}:crocodile", 20, 1, 3)],
            "water_creature": [spawn("minecraft:squid", 4, 1, 3)],
            "water_ambient": [spawn("minecraft:cod", 15, 3, 6), spawn("minecraft:tropical_fish", 15, 3, 6)],
        },
    },
}


def features():
    # The date palm of the Nile: a tall straight trunk and a flat crown of fronds with dates among them.
    palm_trunk = {"type": "minecraft:straight_trunk_placer", "base_height": 6, "height_rand_a": 3, "height_rand_b": 0}
    palm_crown = {"type": "minecraft:acacia_foliage_placer", "radius": 2, "offset": 0}
    g.tree("date_palm", "minecraft:jungle_log", f"{NS}:date_palm_leaves", palm_trunk, palm_crown, rarity=4, fruit=True)
    g.tree("date_palm_grove", "minecraft:jungle_log", f"{NS}:date_palm_leaves", palm_trunk, palm_crown, count=2, fruit=True)

    # Broken columns of the old temples standing alone in the sand.
    write_json(data("worldgen", "configured_feature", "duat_ruin_column.json"), {"type": "minecraft:block_column", "config": {
        "layers": [{"height": {"type": "minecraft:uniform", "min_inclusive": 1, "max_inclusive": 4},
                    "provider": simple("minecraft:cut_sandstone")},
                   {"height": 1, "provider": simple("minecraft:chiseled_sandstone")}],
        "direction": "up", "allowed_placement": {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"},
        "prioritize_tip": True}})
    write_json(data("worldgen", "placed_feature", "duat_ruin_column.json"),
               {"feature": f"{NS}:duat_ruin_column", "placement": surface_placement(rarity=10)})

    # Patches of the black silt of the Nile on the river bed and the shores, like the clay of the Overworld.
    write_json(data("worldgen", "configured_feature", "disk_nile_silt.json"), {"type": "minecraft:disk", "config": {
        "state_provider": {"fallback": simple(f"{NS}:nile_silt"), "rules": []},
        "target": {"type": "minecraft:matching_blocks",
                   "blocks": ["minecraft:dirt", "minecraft:sand", "minecraft:clay", "minecraft:mud", "minecraft:gravel",
                              "minecraft:grass_block"]},
        "radius": {"type": "minecraft:uniform", "min_inclusive": 2, "max_inclusive": 5},
        "half_height": 2}})
    write_json(data("worldgen", "placed_feature", "disk_nile_silt.json"), {"feature": f"{NS}:disk_nile_silt", "placement": [
        {"type": "minecraft:count", "count": 2},
        {"type": "minecraft:in_square"},
        {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR_WG"},
        {"type": "minecraft:block_predicate_filter", "predicate": {"type": "minecraft:matching_fluids", "fluids": "minecraft:water"}},
        {"type": "minecraft:biome"}]})


# ====================================================================== structures

STRUCTURES = {
    # Lairs of the Pharaoh, the Sphinx, Set and Apep: one set, so that they never stand close together.
    "pharaoh_tomb": (["valley_of_kings", "duat_sands"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "great_sphinx": (["duat_sands", "oasis"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "temple_of_set": (["valley_of_kings", "duat_sands"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "apep_lair": (["lake_of_fire"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    # Villages, temples and obelisks.
    "egyptian_village": (["nile_banks", "oasis", "fields_of_aaru"], 30, 12, 2570201, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "temple_of_isis": (["nile_banks", "fields_of_aaru", "oasis"], 28, 10, 2570202, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "obelisk": (["duat_sands", "valley_of_kings", "nile_banks", "oasis"], 24, 8, 2570203, "WORLD_SURFACE_WG", 0, "beard_thin"),
    # The shrines of the gods: one set, so that two gods never stand side by side.
    "hall_of_judgment": (["fields_of_aaru", "duat_sands"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "temple_of_horus": (["duat_sands", "nile_banks", "oasis"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "temple_of_bastet": (["nile_banks", "oasis", "fields_of_aaru"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "shrine_of_sobek": (["nile_banks", "oasis"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "shrine_of_hathor": (["fields_of_aaru", "oasis"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "forge_of_ptah": (["valley_of_kings", "duat_sands"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    "shrine_of_sekhmet": (["lake_of_fire", "valley_of_kings"], 0, 0, 0, "WORLD_SURFACE_WG", 0, "beard_thin"),
    # Boats on the Celestial Nile. The water surface is one block under the first free block: the hull sits in the
    # water, which stays wherever the template sets nothing.
    "solar_barque": (["celestial_nile"], 48, 20, 2570204, "WORLD_SURFACE_WG", -1, "none"),
    "nile_boat": (["celestial_nile"], 20, 8, 2570205, "WORLD_SURFACE_WG", -1, "none"),
    "papyrus_skiff": (["celestial_nile"], 12, 5, 2570206, "WORLD_SURFACE_WG", -1, "none"),
}
LAIRS = {"structures": {"pharaoh_tomb": 3, "great_sphinx": 3, "temple_of_set": 3, "apep_lair": 3},
         "spacing": 44, "separation": 28, "salt": 2570300}
SHRINES = {"structures": {"hall_of_judgment": 3, "temple_of_horus": 2, "temple_of_bastet": 2, "shrine_of_sobek": 2,
                          "shrine_of_hathor": 2, "forge_of_ptah": 2, "shrine_of_sekhmet": 2},
           "spacing": 34, "separation": 16, "salt": 2570400}


def worldgen_structures():
    os.makedirs(data("structure", "egyptian"), exist_ok=True)
    for name, (biomes, spacing, separation, salt, heightmap, offset, adaptation) in STRUCTURES.items():
        structures_egyptian.STRUCTURES[name]().save(data("structure", "egyptian", f"{name}.nbt"))
        write_json(data("tags", "worldgen", "biome", "has_structure", f"{name}.json"),
                   {"replace": False, "values": [f"{NS}:{b}" for b in biomes]})
        write_json(data("worldgen", "template_pool", "egyptian", name, "start.json"), {
            "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {
                "element_type": "minecraft:single_pool_element",
                "location": f"{NS}:egyptian/{name}",
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
            "start_pool": f"{NS}:egyptian/{name}/start",
            "size": 1,
            "start_height": {"absolute": offset},
            "project_start_to_heightmap": heightmap,
            "max_distance_from_center": 80,
            "use_expansion_hack": False,
        })
        if name in LAIRS["structures"] or name in SHRINES["structures"]:
            continue
        write_json(data("worldgen", "structure_set", f"{name}.json"), {
            "structures": [{"structure": f"{NS}:{name}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
        })
    for set_name, group in (("egyptian_lairs", LAIRS), ("egyptian_shrines", SHRINES)):
        write_json(data("worldgen", "structure_set", f"{set_name}.json"), {
            "structures": [{"structure": f"{NS}:{name}", "weight": w} for name, w in group["structures"].items()],
            "placement": {"type": "minecraft:random_spread", "spacing": group["spacing"], "separation": group["separation"],
                          "salt": group["salt"]},
        })
    # The temples of Isis are the homes the sistrum of Hathor calls the priestesses back to.
    write_json(data("tags", "worldgen", "structure", "priestess_homes.json"),
               {"replace": False, "values": [f"{NS}:temple_of_isis"]})


# ====================================================================== loot

# god: (its relic, other drops of its myth)
GOD_RELICS = {
    "ra": ("sun_disc", [("minecraft:glowstone_dust", 4, 10, None)]),
    "osiris": ("djed_of_osiris", [("minecraft:wheat_seeds", 4, 10, None), (f"{NS}:mummy_wrappings", 2, 5, None)]),
    "isis": ("wing_of_isis", [(f"{NS}:knot_of_isis", 1, 1, 0.5)]),
    "horus": ("falcon_feather", [(f"{NS}:eye_of_horus", 1, 1, 0.5), ("minecraft:feather", 2, 6, None)]),
    "anubis": ("feather_of_maat", [(f"{NS}:jackal_pelt", 2, 4, None)]),
    "thoth": ("tablet_of_thoth", [("minecraft:book", 2, 4, None), ("minecraft:experience_bottle", 4, 8, None)]),
    "bastet": ("claw_of_bastet", [("minecraft:string", 2, 6, None)]),
    "sobek": ("fang_of_sobek", [(f"{NS}:crocodile_hide", 2, 4, None), (f"{NS}:crocodile_tooth", 1, 3, None)]),
    "hathor": ("horn_of_hathor", [(f"{NS}:sistrum", 1, 1, 0.5), ("minecraft:leather", 2, 5, None)]),
    "ptah": ("chisel_of_ptah", [(f"{NS}:meteoric_iron_ingot", 1, 3, None)]),
    "sekhmet": ("ember_of_sekhmet", [("minecraft:blaze_rod", 2, 4, None)]),
}

def loot():
    gold = [entry("minecraft:gold_ingot", 8, 1, 4), entry("minecraft:gold_nugget", 10, 3, 9), entry("minecraft:emerald", 6, 1, 4),
            entry("minecraft:lapis_lazuli", 8, 2, 8)]
    chest("egyptian_village", (3, 6), gold + [
        entry(f"{NS}:dates", 8, 2, 6), entry(f"{NS}:honey_cake", 6, 1, 3), entry("minecraft:bread", 8, 2, 5),
        entry("minecraft:white_wool", 6, 1, 4), entry("minecraft:paper", 6, 2, 6),
        entry("minecraft:iron_sword", 3, enchant=True), entry(f"{NS}:ankh", 1),
    ])
    chest("egyptian_house", (3, 6), [
        entry("minecraft:wheat", 8, 2, 6), entry("minecraft:melon_slice", 6, 2, 6), entry(f"{NS}:dates", 8, 2, 6),
        entry("minecraft:honey_bottle", 4, 1, 2), entry("minecraft:clay_ball", 6, 2, 6), entry("minecraft:iron_ingot", 4, 1, 3),
        entry("minecraft:string", 6, 2, 6), entry("minecraft:candle", 4, 1, 3),
    ])
    chest("temple_of_isis", (3, 6), gold + [
        entry(f"{NS}:honey_cake", 6, 1, 3), entry(f"{NS}:dates", 6, 2, 6), entry("minecraft:lily_pad", 6, 1, 3),
        entry(f"{NS}:knot_of_isis", 2), entry(f"{NS}:eye_of_horus", 2), entry(f"{NS}:sistrum", 2),
        entry(f"{NS}:wedding_ring", 1), entry("minecraft:book", 3, enchant=True),
    ])
    chest("obelisk", (2, 5), gold + [
        entry(f"{NS}:eye_of_horus", 3), entry(f"{NS}:ankh", 1), entry(f"{NS}:dates", 6, 2, 5),
        entry("minecraft:book", 3, enchant=True), entry(f"{NS}:mummy_wrappings", 4, 1, 4),
    ])
    # The tomb of the pharaoh always holds the eye of Horus for the hero who goes on against Set.
    chest("pharaoh_tomb", (4, 7), gold + [
        entry("minecraft:gold_block", 3), entry("minecraft:diamond", 4, 1, 3), entry("minecraft:golden_apple", 3),
        entry(f"{NS}:knot_of_isis", 2), entry(f"{NS}:mummy_wrappings", 6, 2, 6), entry("minecraft:book", 4, enchant=True),
        entry("minecraft:golden_horse_armor", 2),
    ], bonus=[entry(f"{NS}:eye_of_horus", 1)])
    chest("great_sphinx", (4, 7), gold + [
        entry("minecraft:diamond", 4, 1, 3), entry("minecraft:gold_block", 2), entry("minecraft:golden_apple", 3),
        entry(f"{NS}:eye_of_horus", 3), entry("minecraft:book", 4, enchant=True), entry("minecraft:lapis_block", 3),
    ])
    chest("temple_of_set", (4, 8), gold + [
        entry("minecraft:diamond", 4, 1, 3), entry("minecraft:netherite_scrap", 2), entry("minecraft:golden_apple", 3),
        entry("minecraft:red_sand", 4, 4, 12), entry("minecraft:fire_charge", 4, 2, 6), entry(f"{NS}:jackal_pelt", 4, 1, 3),
    ])
    chest("apep_lair", (4, 8), gold + [
        entry("minecraft:diamond", 4, 1, 3), entry("minecraft:gold_block", 3), entry("minecraft:netherite_scrap", 2),
        entry("minecraft:golden_apple", 3), entry(f"{NS}:apep_scale", 4, 1, 2), entry("minecraft:enchanted_golden_apple", 1),
    ])

    # The shrines of the gods: offerings of gold and lapis, and things of each god's myth.
    chest("hall_of_judgment", (4, 7), gold + [
        entry("minecraft:diamond", 4, 1, 3), entry("minecraft:golden_apple", 3), entry(f"{NS}:mummy_wrappings", 6, 2, 6),
        entry(f"{NS}:ankh", 2), entry(f"{NS}:eye_of_horus", 2), entry("minecraft:book", 4, enchant=True),
        entry("minecraft:feather", 4, 1, 3), entry("minecraft:totem_of_undying", 1),
    ])
    chest("temple_of_horus", (3, 6), gold + [
        entry(f"{NS}:eye_of_horus", 4), entry("minecraft:arrow", 8, 8, 24), entry("minecraft:spectral_arrow", 5, 4, 12),
        entry("minecraft:bow", 4, enchant=True), entry("minecraft:diamond", 3, 1, 2), entry("minecraft:feather", 6, 2, 6),
    ])
    chest("temple_of_bastet", (3, 6), gold + [
        entry("minecraft:cod", 8, 2, 6), entry("minecraft:salmon", 6, 1, 4), entry(f"{NS}:honey_cake", 6, 1, 3),
        entry("minecraft:string", 6, 2, 6), entry(f"{NS}:sistrum", 3), entry(f"{NS}:knot_of_isis", 2),
        entry("minecraft:diamond", 3, 1, 2),
    ])
    chest("shrine_of_sobek", (3, 6), gold + [
        entry(f"{NS}:crocodile_hide", 8, 1, 4), entry(f"{NS}:crocodile_tooth", 6, 1, 3), entry(f"{NS}:gift_of_hapi", 6, 2, 6),
        entry(f"{NS}:nile_silt", 6, 4, 12), entry("minecraft:cod", 6, 2, 6), entry("minecraft:diamond", 3, 1, 2),
    ])
    chest("shrine_of_hathor", (3, 6), gold + [
        entry(f"{NS}:honey_cake", 8, 1, 4), entry("minecraft:milk_bucket", 4), entry(f"{NS}:sistrum", 4),
        entry("minecraft:music_disc_cat", 1), entry("minecraft:cake", 3), entry(f"{NS}:gift_of_hapi", 4, 1, 4),
        entry("minecraft:diamond", 3, 1, 2), entry(f"{NS}:wedding_ring", 1),
    ])
    chest("forge_of_ptah", (3, 6), gold + [
        entry(f"{NS}:meteoric_iron_ingot", 6, 1, 3), entry(f"{NS}:raw_meteoric_iron", 6, 1, 4), entry("minecraft:iron_ingot", 8, 2, 6),
        entry("minecraft:diamond", 4, 1, 3), entry("minecraft:netherite_scrap", 2), entry("minecraft:clay_ball", 6, 2, 8),
        entry("minecraft:smithing_table", 2),
    ])
    chest("shrine_of_sekhmet", (4, 7), gold + [
        entry("minecraft:diamond", 4, 1, 3), entry("minecraft:fire_charge", 6, 2, 6), entry("minecraft:blaze_powder", 6, 2, 6),
        entry("minecraft:netherite_scrap", 2), entry("minecraft:golden_apple", 3), entry("minecraft:bone", 6, 2, 6),
    ])
    # The boats of the Nile.
    chest("solar_barque", (4, 8), gold + [
        entry("minecraft:gold_block", 3), entry("minecraft:diamond", 4, 1, 3), entry("minecraft:golden_apple", 4),
        entry("minecraft:enchanted_golden_apple", 1), entry("minecraft:glowstone_dust", 6, 4, 12), entry(f"{NS}:ankh", 2),
    ])
    chest("nile_boat", (3, 6), gold + [
        entry(f"{NS}:dates", 8, 2, 6), entry("minecraft:wheat", 8, 2, 8), entry("minecraft:paper", 6, 2, 6),
        entry("minecraft:white_wool", 4, 1, 4), entry(f"{NS}:gift_of_hapi", 4, 1, 3), entry(f"{NS}:honey_cake", 4, 1, 2),
    ])
    chest("papyrus_skiff", (2, 4), [
        entry("minecraft:cod", 10, 2, 6), entry("minecraft:salmon", 8, 1, 4), entry("minecraft:tropical_fish", 4, 1, 2),
        entry("minecraft:fishing_rod", 4), entry("minecraft:string", 6, 1, 4), entry("minecraft:sugar_cane", 8, 2, 6),
        entry(f"{NS}:crocodile_tooth", 2),
    ])

    mob("mummy", [(f"{NS}:mummy_wrappings", 0, 2, None), ("minecraft:rotten_flesh", 0, 2, None), ("minecraft:bone", 0, 1, None)])
    mob("scarab", [(f"{NS}:scarab_shell", 1, 1, 0.35), ("minecraft:string", 0, 1, None)])
    mob("jackal", [(f"{NS}:jackal_pelt", 1, 1, 0.5), ("minecraft:bone", 0, 2, None)])
    mob("scorpion", [(f"{NS}:scorpion_stinger", 0, 1, None), ("minecraft:string", 0, 2, None), ("minecraft:spider_eye", 0, 1, None)])
    mob("ushabti", [("minecraft:clay_ball", 0, 3, None), ("minecraft:lapis_lazuli", 1, 2, 0.25), ("minecraft:brick", 0, 1, None)])
    mob("bastet_cat", [("minecraft:string", 0, 2, None)])
    mob("priestess", [])
    mob("egyptian_merchant", [])
    mob("pharaoh_mummy", [(f"{NS}:khopesh", 1, 1, None), ("minecraft:gold_ingot", 3, 8, None),
                          (f"{NS}:mummy_wrappings", 2, 5, None), ("minecraft:emerald", 2, 5, None)])
    mob("sphinx", [(f"{NS}:nemes", 1, 1, None), (f"{NS}:sphinx_claw", 2, 4, None), ("minecraft:gold_ingot", 4, 10, None),
                   ("minecraft:lapis_lazuli", 4, 12, None)])
    mob("set", [(f"{NS}:was_sceptre", 1, 1, None), ("minecraft:diamond", 2, 4, None), ("minecraft:gold_ingot", 4, 10, None),
                (f"{NS}:jackal_pelt", 2, 4, None)])
    mob("apep", [(f"{NS}:pectoral_of_ra", 1, 1, None), (f"{NS}:apep_scale", 3, 6, None), ("minecraft:diamond", 2, 4, None),
                 ("minecraft:gold_block", 1, 3, None)])
    mob("crocodile", [(f"{NS}:crocodile_hide", 1, 2, None), (f"{NS}:crocodile_tooth", 1, 1, 0.35)])
    # Each god drops the relic of its myth, from which its weapon is forged, and gold.
    for god, (relic, extra) in GOD_RELICS.items():
        mob(god, [(f"{NS}:{relic}", 1, 2, None), ("minecraft:gold_ingot", 3, 8, None), ("minecraft:diamond", 1, 3, None)] + extra)

    shears_or_silk = {"condition": "minecraft:any_of", "terms": [
        {"condition": "minecraft:match_tool", "predicate": {"items": "minecraft:shears"}},
        {"condition": "minecraft:match_tool", "predicate": {"predicates": {"minecraft:enchantments": [
            {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]}
    write_json(data("loot_table", "blocks", "date_palm_leaves.json"), {
        "type": "minecraft:block",
        "pools": [
            {"rolls": 1, "entries": [{"type": "minecraft:alternatives", "children": [
                {"type": "minecraft:item", "name": f"{NS}:date_palm_leaves", "conditions": [shears_or_silk]},
                {"type": "minecraft:item", "name": f"{NS}:dates", "conditions": [
                    {"condition": "minecraft:block_state_property", "block": f"{NS}:date_palm_leaves", "properties": {"age": "3"}}]},
                {"type": "minecraft:item", "name": "minecraft:stick",
                 "conditions": [{"condition": "minecraft:random_chance", "chance": 0.04}]}]}]}],
        "random_sequence": f"{NS}:blocks/date_palm_leaves",
    })
    for block in ("pyramid_stone", "hieroglyph_stone", "nile_silt"):
        write_json(data("loot_table", "blocks", f"{block}.json"), {
            "type": "minecraft:block",
            "pools": [{"rolls": 1, "bonus_rolls": 0, "entries": [{"type": "minecraft:item", "name": f"{NS}:{block}"}],
                       "conditions": [{"condition": "minecraft:survives_explosion"}]}],
            "random_sequence": f"{NS}:blocks/{block}",
        })


# ====================================================================== recipes and tags

M = f"{NS}:meteoric_iron_ingot"
# The weapons of the gods: the god's relic, meteoric iron or gold, and a staff or a string.
WEAPON_RECIPES = [
    ("staff_of_ra", [" D ", " G ", " S "], {"D": f"{NS}:sun_disc", "G": "minecraft:gold_block", "S": "minecraft:stick"}),
    ("flail_of_osiris", ["CDC", " S ", " S "], {"C": "minecraft:chain", "D": f"{NS}:djed_of_osiris", "S": "minecraft:stick"}),
    ("sceptre_of_isis", [" W ", " L ", " G "], {"W": f"{NS}:wing_of_isis", "L": "minecraft:lapis_block", "G": "minecraft:gold_ingot"}),
    ("bow_of_horus", [" GS", "F S", " GS"], {"G": "minecraft:gold_ingot", "F": f"{NS}:falcon_feather", "S": "minecraft:string"}),
    ("glaive_of_anubis", ["MF", "MS", " S"], {"M": M, "F": f"{NS}:feather_of_maat", "S": "minecraft:stick"}),
    ("staff_of_thoth", [" T ", " A ", " S "], {"T": f"{NS}:tablet_of_thoth", "A": "minecraft:amethyst_shard", "S": "minecraft:stick"}),
    ("dagger_of_bastet", ["C", "M", "S"], {"C": f"{NS}:claw_of_bastet", "M": M, "S": "minecraft:stick"}),
    ("khopesh_of_sobek", ["FM", "TM", "S "], {"F": f"{NS}:fang_of_sobek", "T": f"{NS}:crocodile_tooth", "M": M,
                                             "S": "minecraft:stick"}),
    ("sceptre_of_hathor", [" H ", " G ", " S "], {"H": f"{NS}:horn_of_hathor", "G": "minecraft:gold_ingot", "S": "minecraft:stick"}),
    ("axe_of_ptah", ["MC", "MS", " S"], {"M": M, "C": f"{NS}:chisel_of_ptah", "S": "minecraft:stick"}),
    ("spear_of_sekhmet", ["  E", " M ", "S  "], {"E": f"{NS}:ember_of_sekhmet", "M": M, "S": "minecraft:stick"}),
]

def recipes():
    def shapeless(name, ingredients, result, count=1, category="misc"):
        write_json(data("recipe", f"{name}.json"), {
            "type": "minecraft:crafting_shapeless", "category": category,
            "ingredients": [{"item": i} if not i.startswith("#") else {"tag": i[1:]} for i in ingredients],
            "result": {"id": result, "count": count}})

    # The ankh, the key of life: gold for the sun, lapis for the night sky of the Duat, and a scale of the Hydra as
    # proof of a hero.
    shapeless("ankh", ["minecraft:gold_ingot", "minecraft:gold_ingot", "minecraft:lapis_lazuli", f"{NS}:hydra_scale"],
              f"{NS}:ankh")
    write_json(data("recipe", "pyramid_stone.json"), {
        "type": "minecraft:crafting_shaped", "category": "building", "pattern": ["SSS", "SGS", "SSS"],
        "key": {"S": {"item": "minecraft:sandstone"}, "G": {"item": "minecraft:gold_ingot"}},
        "result": {"id": f"{NS}:pyramid_stone", "count": 8}})
    shapeless("hieroglyph_stone", [f"{NS}:pyramid_stone", f"{NS}:pyramid_stone", "minecraft:ink_sac"],
              f"{NS}:hieroglyph_stone", 2, "building")
    shapeless("honey_cake", ["minecraft:wheat", "minecraft:wheat", "minecraft:honey_bottle", f"{NS}:dates"],
              f"{NS}:honey_cake", 2)
    shapeless("sistrum", ["minecraft:gold_ingot", "minecraft:gold_nugget", "minecraft:gold_nugget", "minecraft:stick"],
              f"{NS}:sistrum", 1, "equipment")
    shapeless("nile_silt", ["minecraft:mud", "minecraft:mud", "minecraft:bone_meal"], f"{NS}:nile_silt", 2, "building")
    # The gift of Hapi: silt of the flood, bone meal and papyrus, the strongest fertiliser.
    shapeless("gift_of_hapi", [f"{NS}:nile_silt", "minecraft:bone_meal", "minecraft:bone_meal", "minecraft:sugar_cane"],
              f"{NS}:gift_of_hapi", 2)
    shapeless("leather_from_crocodile_hide", [f"{NS}:crocodile_hide"], "minecraft:leather", 2)
    for name, pattern, key in WEAPON_RECIPES:
        write_json(data("recipe", f"{name}.json"), {
            "type": "minecraft:crafting_shaped", "category": "equipment", "pattern": pattern,
            "key": {k: {"item": v} for k, v in key.items()}, "result": {"id": f"{NS}:{name}", "count": 1}})
    g.add_tag("item", "swords", ["flail_of_osiris", "glaive_of_anubis", "dagger_of_bastet", "khopesh_of_sobek", "spear_of_sekhmet"])
    g.add_tag("item", "axes", ["axe_of_ptah"])
    g.add_tag("item", "enchantable/bow", ["bow_of_horus"])
    g.add_tag("item", "enchantable/durability", ["bow_of_horus", "staff_of_ra", "staff_of_thoth", "sceptre_of_isis",
                                                 "sceptre_of_hathor"])
    g.add_tag("block", "mineable/shovel", ["nile_silt"])
    g.add_tag("block", "dirt", ["nile_silt"])
    g.add_tag("item", "dirt", ["nile_silt"])
    g.add_tag("entity_type", "can_breathe_under_water", ["crocodile", "sobek"])
    g.add_tag("item", "head_armor", ["nemes"])
    g.add_tag("item", "chest_armor", ["pectoral_of_ra"])
    g.add_tag("item", "swords", ["khopesh"])
    g.add_tag("block", "mineable/pickaxe", ["pyramid_stone", "hieroglyph_stone"])
    g.add_tag("block", "leaves", ["date_palm_leaves"])
    g.add_tag("block", "mineable/hoe", ["date_palm_leaves"])
    g.add_tag("item", "leaves", ["date_palm_leaves"])
    g.add_tag("entity_type", "undead", ["mummy", "pharaoh_mummy"])


# ====================================================================== models

GODS = ["ra", "osiris", "isis", "horus", "anubis", "thoth", "bastet", "sobek", "hathor", "ptah", "sekhmet"]
WEAPONS = ["staff_of_ra", "flail_of_osiris", "sceptre_of_isis", "glaive_of_anubis", "staff_of_thoth", "dagger_of_bastet",
           "khopesh_of_sobek", "sceptre_of_hathor", "axe_of_ptah", "spear_of_sekhmet"]
ITEMS = ["ankh", "dates", "honey_cake", "mummy_wrappings", "scarab_shell", "scorpion_stinger", "jackal_pelt", "sphinx_claw",
         "apep_scale", "eye_of_horus", "knot_of_isis", "sistrum", "khopesh", "was_sceptre", "nemes", "pectoral_of_ra",
         "gift_of_hapi", "crocodile_hide", "crocodile_tooth"] + [relic for relic, _ in GOD_RELICS.values()] + WEAPONS
HANDHELD = {"khopesh", "was_sceptre"} | set(WEAPONS)
BLOCKS = ["pyramid_stone", "hieroglyph_stone", "nile_silt"]
MOBS = ["mummy", "scarab", "jackal", "scorpion", "ushabti", "bastet_cat", "priestess", "egyptian_merchant", "pharaoh_mummy",
        "sphinx", "set", "apep", "crocodile"] + GODS


def models():
    for block in BLOCKS:
        write_json(assets("blockstates", f"{block}.json"), {"variants": {"": {"model": f"{NS}:block/{block}"}}})
        write_json(assets("models", "block", f"{block}.json"),
                   {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{block}"}})
        write_json(assets("models", "item", f"{block}.json"), {"parent": f"{NS}:block/{block}"})
    # The gate of shadow: a dark veil of drifting sand and stars, seen through.
    write_json(assets("blockstates", "pyramid_gate.json"), {"variants": {
        f"facing={facing},upper={upper}": {"model": f"{NS}:block/pyramid_gate", "y": y}
        for facing, y in (("north", 0), ("east", 90), ("south", 180), ("west", 270)) for upper in ("false", "true")}})
    write_json(assets("models", "block", "pyramid_gate.json"), {
        "parent": "minecraft:block/cube_all", "render_type": "minecraft:translucent",
        "textures": {"all": f"{NS}:block/pyramid_gate", "particle": f"{NS}:block/pyramid_gate"}})
    write_json(assets("blockstates", "date_palm_leaves.json"), {"variants": {
        f"age={age}": {"model": f"{NS}:block/date_palm_leaves" + ("_ripe" if age == 3 else "")} for age in range(4)}})
    for suffix in ("", "_ripe"):
        write_json(assets("models", "block", f"date_palm_leaves{suffix}.json"), {
            "parent": "minecraft:block/cube_all", "render_type": "minecraft:cutout_mipped",
            "textures": {"all": f"{NS}:block/date_palm_leaves{suffix}"}})
    write_json(assets("models", "item", "date_palm_leaves.json"), {"parent": f"{NS}:block/date_palm_leaves_ripe"})
    for item in ITEMS:
        parent = "minecraft:item/handheld" if item in HANDHELD else "minecraft:item/generated"
        write_json(assets("models", "item", f"{item}.json"), {"parent": parent, "textures": {"layer0": f"{NS}:item/{item}"}})
    for name in MOBS:
        write_json(assets("models", "item", f"{name}_spawn_egg.json"), {"parent": "minecraft:item/template_spawn_egg"})
    # The bow of Horus draws like the vanilla bow: three pulling stages picked by the "pull" property.
    write_json(assets("models", "item", "bow_of_horus.json"), {
        "parent": "minecraft:item/bow", "textures": {"layer0": f"{NS}:item/bow_of_horus"},
        "overrides": [{"predicate": {"pulling": 1}, "model": f"{NS}:item/bow_of_horus_pulling_0"},
                      {"predicate": {"pulling": 1, "pull": 0.65}, "model": f"{NS}:item/bow_of_horus_pulling_1"},
                      {"predicate": {"pulling": 1, "pull": 0.9}, "model": f"{NS}:item/bow_of_horus_pulling_2"}]})
    for stage in range(3):
        write_json(assets("models", "item", f"bow_of_horus_pulling_{stage}.json"), {
            "parent": f"{NS}:item/bow_of_horus", "textures": {"layer0": f"{NS}:item/bow_of_horus_pulling_{stage}"}})


# ====================================================================== translations

LANG = {
    "block.mythsofworlds.pyramid_stone": ("Камень пирамид", "Pyramid Stone"),
    "block.mythsofworlds.hieroglyph_stone": ("Камень с иероглифами", "Hieroglyph Stone"),
    "block.mythsofworlds.pyramid_gate": ("Врата тени", "Gate of Shadow"),
    "block.mythsofworlds.date_palm_leaves": ("Листья финиковой пальмы", "Date Palm Fronds"),
    "item.mythsofworlds.ankh": ("Анх", "Ankh"),
    "item.mythsofworlds.ankh.desc": (
        "Коснитесь пирамиды (5x5, 3x3, золотая вершина, проход в основании): в проходе откроются врата в Дуат",
        "Touch a pyramid (5x5, 3x3, a golden top, a doorway in the base): a gate to the Duat opens in the doorway"),
    "item.mythsofworlds.ankh.no_pyramid": (
        "Это не пирамида: основание 5x5 и ступень 3x3 из камня пирамид, золотой блок на вершине, проход посередине стороны",
        "This is no pyramid: a 5x5 base and a 3x3 step of pyramid stone, a gold block on top, a doorway in a side"),
    "item.mythsofworlds.ankh.opened": ("Врата тени открылись! Встаньте в проход, чтобы попасть в Дуат",
                                       "The gate of shadow opens! Stand in the doorway to pass into the Duat"),
    "item.mythsofworlds.dates": ("Финики", "Dates"),
    "item.mythsofworlds.honey_cake": ("Медовая лепёшка", "Honey Cake"),
    "item.mythsofworlds.mummy_wrappings": ("Пелены мумии", "Mummy Wrappings"),
    "item.mythsofworlds.scarab_shell": ("Панцирь скарабея", "Scarab Shell"),
    "item.mythsofworlds.scorpion_stinger": ("Жало скорпиона", "Scorpion Stinger"),
    "item.mythsofworlds.jackal_pelt": ("Шкура шакала", "Jackal Pelt"),
    "item.mythsofworlds.sphinx_claw": ("Коготь Сфинкса", "Sphinx Claw"),
    "item.mythsofworlds.apep_scale": ("Чешуя Апопа", "Scale of Apep"),
    "item.mythsofworlds.eye_of_horus": ("Око Гора", "Eye of Horus"),
    "item.mythsofworlds.eye_of_horus.desc": ("Носите с собой против Сета", "Carry it against Set"),
    "item.mythsofworlds.knot_of_isis": ("Узел Исиды", "Knot of Isis"),
    "item.mythsofworlds.sistrum": ("Систр Хатхор", "Sistrum of Hathor"),
    "item.mythsofworlds.sistrum.desc": ("Встряхните (ПКМ): жрицы Исиды поблизости вернутся в свои храмы",
                                        "Shake it (right-click): the priestesses of Isis nearby go back to their temples"),
    "item.mythsofworlds.sistrum.called": ("Жрицы возвращаются домой: %s", "Priestesses going home: %s"),
    "item.mythsofworlds.khopesh": ("Хопеш фараона", "Khopesh of the Pharaoh"),
    "item.mythsofworlds.khopesh.desc": ("Каждый удар иссушает врага на 3 секунды", "Every blow withers the foe for 3 seconds"),
    "item.mythsofworlds.was_sceptre": ("Посох уас", "Was-Sceptre"),
    "item.mythsofworlds.was_sceptre.desc": (
        "ПКМ: песчаная буря отбрасывает, ослепляет и замедляет врагов в 8 блоках (раз в 10 секунд)",
        "Right-click: a sandstorm throws back, blinds and slows the foes within 8 blocks (every 10 seconds)"),
    "item.mythsofworlds.nemes": ("Немес Сфинкса", "Nemes of the Sphinx"),
    "item.mythsofworlds.nemes.desc": ("Ночное зрение", "Night Vision"),
    "item.mythsofworlds.pectoral_of_ra": ("Пектораль Ра", "Pectoral of Ra"),
    "item.mythsofworlds.pectoral_of_ra.desc": ("Огнестойкость и сила", "Fire Resistance and Strength"),
    "item.mythsofworlds.relic.egyptian": ("Дуат: дар богов Египта", "Duat: a gift of the gods of Egypt"),
    "entity.mythsofworlds.mummy": ("Мумия", "Mummy"),
    "entity.mythsofworlds.scarab": ("Скарабей", "Scarab"),
    "entity.mythsofworlds.jackal": ("Шакал Анубиса", "Jackal of Anubis"),
    "entity.mythsofworlds.scorpion": ("Скорпион", "Scorpion"),
    "entity.mythsofworlds.ushabti": ("Ушебти", "Ushabti"),
    "entity.mythsofworlds.bastet_cat": ("Кошка Бастет", "Cat of Bastet"),
    "entity.mythsofworlds.priestess": ("Жрица Исиды", "Priestess of Isis"),
    "entity.mythsofworlds.egyptian_merchant": ("Торговец Дуата", "Trader of the Duat"),
    "entity.mythsofworlds.pharaoh_mummy": ("Мумия фараона", "Mummy of the Pharaoh"),
    "entity.mythsofworlds.sphinx": ("Сфинкс", "Sphinx"),
    "entity.mythsofworlds.set": ("Сет", "Set"),
    "entity.mythsofworlds.apep": ("Апоп", "Apep"),
    "block.mythsofworlds.nile_silt": ("Ил Нила", "Nile Silt"),
    "item.mythsofworlds.gift_of_hapi": ("Дар Хапи", "Gift of Hapi"),
    "item.mythsofworlds.gift_of_hapi.desc": (
        "Сильнейшее удобрение: ПКМ по растению трижды подкармливает все растения в квадрате 5x5",
        "The strongest fertiliser: right-click a plant to feed every plant in a 5x5 square three times"),
    "item.mythsofworlds.crocodile_hide": ("Крокодилова кожа", "Crocodile Hide"),
    "item.mythsofworlds.crocodile_tooth": ("Зуб крокодила", "Crocodile Tooth"),
    "item.mythsofworlds.sun_disc": ("Солнечный диск Ра", "Sun Disc of Ra"),
    "item.mythsofworlds.djed_of_osiris": ("Джед Осириса", "Djed of Osiris"),
    "item.mythsofworlds.wing_of_isis": ("Крыло Исиды", "Wing of Isis"),
    "item.mythsofworlds.falcon_feather": ("Соколиное перо Гора", "Falcon Feather of Horus"),
    "item.mythsofworlds.feather_of_maat": ("Перо Маат", "Feather of Ma'at"),
    "item.mythsofworlds.tablet_of_thoth": ("Скрижаль Тота", "Tablet of Thoth"),
    "item.mythsofworlds.claw_of_bastet": ("Коготь Бастет", "Claw of Bastet"),
    "item.mythsofworlds.fang_of_sobek": ("Клык Себека", "Fang of Sobek"),
    "item.mythsofworlds.horn_of_hathor": ("Рог Хатхор", "Horn of Hathor"),
    "item.mythsofworlds.chisel_of_ptah": ("Резец Птаха", "Chisel of Ptah"),
    "item.mythsofworlds.ember_of_sekhmet": ("Уголь Сехмет", "Ember of Sekhmet"),
    "item.mythsofworlds.staff_of_ra": ("Посох Ра", "Staff of Ra"),
    "item.mythsofworlds.staff_of_ra.desc": ("ПКМ: три огненных шара солнца (раз в 2 секунды)",
                                            "Right-click: three fireballs of the sun (every 2 seconds)"),
    "item.mythsofworlds.flail_of_osiris": ("Цеп Осириса", "Flail of Osiris"),
    "item.mythsofworlds.flail_of_osiris.desc": ("Удары лечат вас; нежить слабеет и замедляется",
                                                "Your blows heal you; the undead grow weak and slow"),
    "item.mythsofworlds.sceptre_of_isis": ("Скипетр Исиды", "Sceptre of Isis"),
    "item.mythsofworlds.sceptre_of_isis.desc": (
        "ПКМ: лечит вас, игроков, питомцев и семью в 8 блоках и даёт регенерацию (раз в 20 секунд)",
        "Right-click: heals you, the players, pets and family within 8 blocks and gives Regeneration (every 20 seconds)"),
    "item.mythsofworlds.bow_of_horus": ("Лук Гора", "Bow of Horus"),
    "item.mythsofworlds.bow_of_horus.desc": ("Стрелы бьют сильнее, а раненый светится 10 секунд",
                                             "Arrows strike harder, and whoever they hit glows for 10 seconds"),
    "item.mythsofworlds.glaive_of_anubis": ("Глефа Анубиса", "Glaive of Anubis"),
    "item.mythsofworlds.glaive_of_anubis.desc": ("Гроза чудовищ и богов; удар замедляет",
                                                 "The bane of monsters and gods; its blow slows"),
    "item.mythsofworlds.staff_of_thoth": ("Посох Тота", "Staff of Thoth"),
    "item.mythsofworlds.staff_of_thoth.desc": (
        "ПКМ: слово силы бьёт существо, на которое вы смотрите (до 24 блоков), магией и поднимает в воздух",
        "Right-click: a word of power strikes the creature you look at (up to 24 blocks) with magic and lifts it up"),
    "item.mythsofworlds.dagger_of_bastet": ("Кинжал Бастет", "Dagger of Bastet"),
    "item.mythsofworlds.dagger_of_bastet.desc": ("Быстрый, как кошка: каждый удар даёт вам скорость",
                                                 "Quick as a cat: every blow makes you swift"),
    "item.mythsofworlds.khopesh_of_sobek": ("Хопеш Себека", "Khopesh of Sobek"),
    "item.mythsofworlds.khopesh_of_sobek.desc": ("Удар замедляет, а врага в воде ещё и лишает сил",
                                                 "Its blow slows, and saps the strength of a foe in the water"),
    "item.mythsofworlds.sceptre_of_hathor": ("Скипетр Хатхор", "Sceptre of Hathor"),
    "item.mythsofworlds.sceptre_of_hathor.desc": (
        "ПКМ: песня усмиряет чудовищ в 10 блоках, они забывают о вас (раз в 15 секунд)",
        "Right-click: the song calms the monsters within 10 blocks and they forget you (every 15 seconds)"),
    "item.mythsofworlds.axe_of_ptah": ("Секира Птаха", "Axe of Ptah"),
    "item.mythsofworlds.axe_of_ptah.desc": ("В руке: спешка II", "In hand: Haste II"),
    "item.mythsofworlds.spear_of_sekhmet": ("Копьё Сехмет", "Spear of Sekhmet"),
    "item.mythsofworlds.spear_of_sekhmet.desc": ("Каждый удар поджигает врага на 5 секунд",
                                                 "Every blow sets the foe on fire for 5 seconds"),
    "entity.mythsofworlds.crocodile": ("Крокодил", "Crocodile"),
    "entity.mythsofworlds.ra": ("Ра", "Ra"),
    "entity.mythsofworlds.osiris": ("Осирис", "Osiris"),
    "entity.mythsofworlds.isis": ("Исида", "Isis"),
    "entity.mythsofworlds.horus": ("Гор", "Horus"),
    "entity.mythsofworlds.anubis": ("Анубис", "Anubis"),
    "entity.mythsofworlds.thoth": ("Тот", "Thoth"),
    "entity.mythsofworlds.bastet": ("Бастет", "Bastet"),
    "entity.mythsofworlds.sobek": ("Себек", "Sobek"),
    "entity.mythsofworlds.hathor": ("Хатхор", "Hathor"),
    "entity.mythsofworlds.ptah": ("Птах", "Ptah"),
    "entity.mythsofworlds.sekhmet": ("Сехмет", "Sekhmet"),
    "entity.mythsofworlds.pharaoh_mummy.curse": ("Проклятие гробницы: руки слабеют, мучает голод",
                                                 "The curse of the tomb: your hands grow weak, hunger gnaws"),
    "entity.mythsofworlds.set.eye_guards": ("Око Гора защищает ваши глаза от бури Сета",
                                            "The eye of Horus shields your eyes from the storm of Set"),
}
PRIESTESS_TEXT = dict(g.AMAZON_TEXT, **{
    "daughter": ("%1$s тянет вас за руку: «Отец, покажи мне звёзды Дуата!»",
                 "%1$s tugs at your hand: \"Father, show me the stars of the Duat!\""),
    "talk": ("%1$s: «Чем ты почтишь служительницу Исиды?» Больше всего она любит %2$s. Симпатия: %3$s/%4$s",
             "%1$s: \"How will you honour a servant of Isis?\" She likes %2$s best. Affection: %3$s/%4$s"),
    "likes.0": ("лотосы и цветы", "lotus and flowers"),
    "likes.1": ("золото и лазурит", "gold and lapis"),
    "likes.2": ("сладкое: мёд и финики", "sweet things: honey and dates"),
    "likes.3": ("трофеи чудовищ Дуата", "trophies of the monsters of the Duat"),
    "wife": ("%1$s, ваша жена, улыбается. Подарите ей медовую лепёшку, и родится дочь. Shift+ПКМ: идти за вами, ждать или гулять.",
             "%1$s, your wife, smiles. Give her a honey cake and a daughter is born. Shift + right-click: follow, stay or wander."),
    "rivals": ("%1$s вызывает вашу жену %2$s на священный поединок! Они сражаются за вас.",
               "%1$s challenges your wife %2$s to a sacred duel! They are fighting for you."),
    "rival_won": ("%1$s победила в поединке и стала вашей женой!", "%1$s won the duel and is your wife now!"),
    "married": ("%1$s принимает кольцо! Жрица Исиды теперь ваша жена.", "%1$s takes the ring! The priestess of Isis is your wife now."),
    "in_love": ("%1$s: «Исида благословила тебя. Где твоё кольцо?»", "%1$s: \"Isis has blessed you. Where is your ring?\""),
    "grown_daughter": ("%1$s, ваша дочь, готова идти с вами сквозь ночь Дуата.",
                       "%1$s, your daughter, is ready to walk the night of the Duat at your side."),
    "necklace": ("%1$s не может отвести глаз от узла Исиды. Она влюблена!",
                 "%1$s cannot take her eyes off the knot of Isis. She is in love!"),
    "necklace_already": ("%1$s: «Моё сердце и так твоё. Оставь узел Исиды себе».",
                         "%1$s: \"My heart is already yours. Keep the knot of Isis.\""),
    "died": ("Ваша жена %1$s ушла на Поля Иалу...", "Your wife %1$s has gone to the Fields of Aaru..."),
})
MOB_NAMES_RU = {
    "mummy": "мумии", "scarab": "скарабея", "jackal": "шакала Анубиса", "scorpion": "скорпиона", "ushabti": "ушебти",
    "bastet_cat": "кошки Бастет", "priestess": "жрицы Исиды", "egyptian_merchant": "торговца Дуата",
    "pharaoh_mummy": "мумии фараона", "sphinx": "Сфинкса", "set": "Сета", "apep": "Апопа", "crocodile": "крокодила",
    "ra": "Ра", "osiris": "Осириса", "isis": "Исиды", "horus": "Гора", "anubis": "Анубиса", "thoth": "Тота",
    "bastet": "Бастет", "sobek": "Себека", "hathor": "Хатхор", "ptah": "Птаха", "sekhmet": "Сехмет",
}


def lang():
    import journal_egyptian
    entries = dict(LANG)
    entries.update(g.journal("egyptian", journal_egyptian.INTRO, journal_egyptian.with_gear()))
    for key, values in PRIESTESS_TEXT.items():
        entries[f"entity.{NS}.priestess.{key}"] = values
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
    import textures_egyptian as tx
    for folder, table in (("block", tx.BLOCKS), ("entity", tx.ENTITIES)):
        os.makedirs(assets("textures", folder), exist_ok=True)
        for name, fn in table.items():
            tx.save(fn(random.Random(name)), assets("textures", folder, f"{name}.png"))
    with open(assets("textures", "block", "pyramid_gate.png.mcmeta"), "w") as f:
        json.dump({"animation": {"frametime": 4, "interpolate": True}}, f, indent=2)
        f.write("\n")
    os.makedirs(assets("textures", "item"), exist_ok=True)
    for name, fn in tx.ITEMS.items():
        tx.save(tx.item(fn, random.Random(name)), assets("textures", "item", f"{name}.png"))
    os.makedirs(assets("textures", "models", "armor"), exist_ok=True)
    for name, fn in tx.LAYERS.items():
        tx.save(fn(random.Random(name + "_layer")), assets("textures", "models", "armor", f"{name}_layer_1.png"))


def main():
    write_json(data("dimension_type", "duat.json"), duat_dimension_type())
    duat_noise_settings()
    write_json(data("dimension", "duat.json"),
               g.dimension("duat", g.multi_noise([(f"{NS}:{name}", spec["point"]) for name, spec in BIOMES.items()]),
                           settings=f"{NS}:duat"))
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
