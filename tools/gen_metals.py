"""Metals and fuels of the myths: orichalcum and Hephaestus coal in Hellas, bulat in Nav, dark iron and Muspel embers
in Jotunheim.

Writes the ore features (the biomes list them in gen_greek_assets.py and gen_norse_assets.py), block states, models,
loot, recipes, fuel values, tags and lang entries; with --textures also the block, item and armour textures.
Run it after gen_greek_assets.py and gen_norse_assets.py. Java side: registry/MetalSet.java, GreekContent, NorseContent.
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import gen_greek_assets as g  # noqa: E402
from gen_greek_assets import NS, assets, data, write_json  # noqa: E402

# name: (ru, en, colours light/mid/dark, ore count per chunk, vein size, lowest and highest y)
METALS = {
    "orichalcum": {"ru": "Орихалк", "ru_gen": "орихалка", "en": "Orichalcum",
                   "light": 0xF6B06A, "mid": 0xD9783A, "dark": 0x8A3E1E, "count": 8, "size": 7, "y": (-48, 64),
                   "style": "greek"},
    "dark_iron": {"ru": "Тёмное железо", "ru_gen": "тёмного железа", "en": "Dark Iron",
                  "light": 0x9AA2B4, "mid": 0x5A6074, "dark": 0x2A2C38, "count": 9, "size": 6, "y": (-56, 56),
                  "style": "norse", "needs": "diamond"},
    "bulat": {"ru": "Булат", "ru_gen": "булата", "en": "Bulat",
              "light": 0xD6E2EE, "mid": 0x8A9CB4, "dark": 0x3A4458, "count": 8, "size": 7, "y": (-56, 48),
              "style": "slavic"},
}
# Fuels: the item, its ore, burn time in ticks (coal burns 1600), ore count, vein size, heights.
FUELS = {
    "hephaestus_coal": {"ore": "hephaestus_coal_ore", "burn": 3200, "count": 16, "size": 14, "y": (0, 192),
                        "colour": 0xE8642A, "xp": 0.2},
    "muspel_ember": {"ore": "muspel_ember_ore", "burn": 4800, "count": 14, "size": 10, "y": (-30, 160),
                     "colour": 0xFF8A1E, "xp": 0.3},
}
TOOLS = ["sword", "pickaxe", "axe", "shovel", "hoe"]
ARMOUR = ["helmet", "chestplate", "leggings", "boots"]

TOOL_RU = {"sword": ("Меч", "м"), "pickaxe": ("Кирка", "ж"), "axe": ("Топор", "м"), "shovel": ("Лопата", "ж"),
           "hoe": ("Мотыга", "ж"), "helmet": ("Шлем", "м"), "chestplate": ("Нагрудник", "м"),
           "leggings": ("Поножи", "мн"), "boots": ("Сапоги", "мн")}
ADJ_RU = {"orichalcum": {"м": "Орихалковый", "ж": "Орихалковая", "мн": "Орихалковые"},
          "dark_iron": {"м": "Тёмножелезный", "ж": "Тёмножелезная", "мн": "Тёмножелезные"},
          "bulat": {"м": "Булатный", "ж": "Булатная", "мн": "Булатные"}}
RAW_RU = {"orichalcum": "Необработанный орихалк", "dark_iron": "Необработанное тёмное железо",
          "bulat": "Сырой булат"}


def items(metal):
    return ([f"raw_{metal}", f"{metal}_ingot"] + [f"{metal}_{tool}" for tool in TOOLS]
            + [f"{metal}_{piece}" for piece in ARMOUR])


# ====================================================================== worldgen

def features():
    for metal, spec in METALS.items():
        g.ore(f"ore_{metal}", f"{NS}:{metal}_ore", spec["size"], spec["count"], *spec["y"])
    for fuel, spec in FUELS.items():
        g.ore(f"ore_{fuel}", f"{NS}:{spec['ore']}", spec["size"], spec["count"], *spec["y"])


# ====================================================================== loot, recipes, tags

def ore_loot(ore, drop, lo=1, hi=1):
    count = [] if lo == hi == 1 else [{"function": "minecraft:set_count",
                                        "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]
    write_json(data("loot_table", "blocks", f"{ore}.json"), {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "bonus_rolls": 0, "entries": [{"type": "minecraft:alternatives", "children": [
            {"type": "minecraft:item", "name": f"{NS}:{ore}", "conditions": [{
                "condition": "minecraft:match_tool", "predicate": {"predicates": {"minecraft:enchantments": [
                    {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}]},
            {"type": "minecraft:item", "name": drop, "functions": count + [
                {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune", "formula": "minecraft:ore_drops"},
                {"function": "minecraft:explosion_decay"}]},
        ]}]}],
    })


def self_loot(block):
    write_json(data("loot_table", "blocks", f"{block}.json"), {
        "type": "minecraft:block",
        "pools": [{"rolls": 1, "bonus_rolls": 0, "entries": [{"type": "minecraft:item", "name": f"{NS}:{block}"}],
                   "conditions": [{"condition": "minecraft:survives_explosion"}]}],
    })


def cook(name, source, result, xp, time=200):
    for kind, ticks in (("smelting", time), ("blasting", time // 2)):
        write_json(data("recipe", f"{name}_from_{kind}.json"), {
            "type": f"minecraft:{kind}", "category": "misc", "ingredient": {"item": source},
            "result": {"id": result}, "experience": xp, "cookingtime": ticks,
        })


def shaped(name, pattern, key, result, count=1, category="equipment"):
    write_json(data("recipe", f"{name}.json"), {
        "type": "minecraft:crafting_shaped", "category": category, "pattern": pattern,
        "key": {k: {"item": v} for k, v in key.items()}, "result": {"id": result, "count": count},
    })


TOOL_PATTERNS = {
    "sword": ["M", "M", "S"], "pickaxe": ["MMM", " S ", " S "], "axe": ["MM", "MS", " S"],
    "shovel": ["M", "S", "S"], "hoe": ["MM", " S", " S"],
    "helmet": ["MMM", "M M"], "chestplate": ["M M", "MMM", "MMM"], "leggings": ["MMM", "M M", "M M"],
    "boots": ["M M", "M M"],
}


def recipes():
    for metal in METALS:
        ingot = f"{NS}:{metal}_ingot"
        cook(f"{metal}_ingot_from_raw", f"{NS}:raw_{metal}", ingot, 1.0)
        cook(f"{metal}_ingot_from_ore", f"{NS}:{metal}_ore", ingot, 1.0)
        shaped(f"{metal}_block", ["MMM", "MMM", "MMM"], {"M": ingot}, f"{NS}:{metal}_block", category="building")
        write_json(data("recipe", f"{metal}_ingot_from_block.json"), {
            "type": "minecraft:crafting_shapeless", "category": "misc",
            "ingredients": [{"item": f"{NS}:{metal}_block"}], "result": {"id": ingot, "count": 9},
        })
        for piece, pattern in TOOL_PATTERNS.items():
            key = {"M": ingot}
            if "S" in "".join(pattern):
                key["S"] = "minecraft:stick"
            shaped(f"{metal}_{piece}", pattern, key, f"{NS}:{metal}_{piece}")
    for fuel, spec in FUELS.items():
        cook(f"{fuel}_from_ore", f"{NS}:{spec['ore']}", f"{NS}:{fuel}", spec["xp"])
    write_json(os.path.join(g.ROOT, "data", "neoforge", "data_maps", "item", "furnace_fuels.json"),
               {"values": {f"{NS}:{fuel}": {"burn_time": spec["burn"]} for fuel, spec in FUELS.items()}})


def tags():
    ores = [f"{m}_ore" for m in METALS] + [s["ore"] for s in FUELS.values()]
    blocks = [f"{m}_block" for m in METALS]
    g.add_tag("block", "mineable/pickaxe", ores + blocks)
    g.add_tag("block", "needs_iron_tool", [f"{m}_ore" for m, spec in METALS.items() if "needs" not in spec] + blocks)
    g.add_tag("block", "needs_diamond_tool", [f"{m}_ore" for m, spec in METALS.items() if spec.get("needs") == "diamond"])
    g.add_tag("block", "needs_stone_tool", [s["ore"] for s in FUELS.values()])
    for kind, values in (("swords", "sword"), ("pickaxes", "pickaxe"), ("axes", "axe"), ("shovels", "shovel"),
                         ("hoes", "hoe"), ("head_armor", "helmet"), ("chest_armor", "chestplate"),
                         ("leg_armor", "leggings"), ("foot_armor", "boots")):
        g.add_tag("item", kind, [f"{m}_{values}" for m in METALS])
    g.add_tag("item", "trimmable_armor", [f"{m}_{piece}" for m in METALS for piece in ARMOUR])
    g.add_tag("item", "beacon_payment_items", [f"{m}_ingot" for m in METALS])
    g.add_tag("block", "beacon_base_blocks", blocks)


# ====================================================================== models and lang

def models():
    for block in [f"{m}_ore" for m in METALS] + [f"{m}_block" for m in METALS] + [s["ore"] for s in FUELS.values()]:
        write_json(assets("blockstates", f"{block}.json"), {"variants": {"": {"model": f"{NS}:block/{block}"}}})
        write_json(assets("models", "block", f"{block}.json"),
                   {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/{block}"}})
        write_json(assets("models", "item", f"{block}.json"), {"parent": f"{NS}:block/{block}"})
    for metal in METALS:
        for name in items(metal):
            handheld = any(name.endswith("_" + tool) for tool in TOOLS)
            write_json(assets("models", "item", f"{name}.json"), {
                "parent": "minecraft:item/handheld" if handheld else "minecraft:item/generated",
                "textures": {"layer0": f"{NS}:item/{name}"}})
    write_json(assets("models", "item", "hephaestus_coal.json"),
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/hephaestus_coal"}})


def lang():
    entries = {
        f"block.{NS}.hephaestus_coal_ore": ("Руда угля Гефеста", "Hephaestus Coal Ore"),
        f"item.{NS}.hephaestus_coal": ("Уголь Гефеста", "Hephaestus Coal"),
        f"block.{NS}.muspel_ember_ore": ("Руда углей Муспельхейма", "Muspel Ember Ore"),
    }
    for metal, spec in METALS.items():
        entries[f"block.{NS}.{metal}_ore"] = (f"Руда {spec['ru_gen']}", f"{spec['en']} Ore")
        entries[f"block.{NS}.{metal}_block"] = (f"Блок {spec['ru_gen']}", f"Block of {spec['en']}")
        entries[f"item.{NS}.raw_{metal}"] = (RAW_RU[metal], f"Raw {spec['en']}")
        entries[f"item.{NS}.{metal}_ingot"] = (f"Слиток {spec['ru_gen']}", f"{spec['en']} Ingot")
        for piece in TOOLS + ARMOUR:
            noun, gender = TOOL_RU[piece]
            en = {"helmet": "Helmet", "chestplate": "Chestplate", "leggings": "Leggings", "boots": "Boots"}.get(
                piece, piece.capitalize())
            entries[f"item.{NS}.{metal}_{piece}"] = (f"{ADJ_RU[metal][gender]} {noun.lower()}", f"{spec['en']} {en}")
    for index, code in ((0, "ru_ru"), (1, "en_us")):
        path = assets("lang", f"{code}.json")
        with open(path, encoding="utf-8") as f:
            current = json.load(f)
        for key, values in entries.items():
            current[key] = values[index]
        write_json(path, current)


# ====================================================================== textures

def textures():
    import textures_metals as tm
    os.makedirs(assets("textures", "models", "armor"), exist_ok=True)
    for metal, spec in METALS.items():
        colours = (spec["light"], spec["mid"], spec["dark"])
        rng = random.Random(metal)
        tm.save(tm.ore(rng, colours, lumps=True), assets("textures", "block", f"{metal}_ore.png"))
        tm.save(tm.metal_block(rng, colours, spec["style"]), assets("textures", "block", f"{metal}_block.png"))
        for name, draw in tm.metal_items(colours, spec["style"]).items():
            tm.save(tm.icon(draw, random.Random(f"{metal}_{name}")), assets("textures", "item", f"{metal}_{name}.png")
                    if name != "raw" else assets("textures", "item", f"raw_{metal}.png"))
        layer1, layer2 = tm.armour_layers(random.Random(metal + "_armour"), colours, spec["style"])
        tm.save(layer1, assets("textures", "models", "armor", f"{metal}_layer_1.png"))
        tm.save(layer2, assets("textures", "models", "armor", f"{metal}_layer_2.png"))
    for fuel, spec in FUELS.items():
        tm.save(tm.ore(random.Random(spec["ore"]), (spec["colour"], tm.scale_hex(spec["colour"], 0.7),
                                                     0x1E1410), glow=fuel == "muspel_ember", lumps=True),
                assets("textures", "block", f"{spec['ore']}.png"))
    tm.save(tm.icon(tm.draw_coal(0xE8642A), random.Random("hephaestus_coal")),
            assets("textures", "item", "hephaestus_coal.png"))
    tm.save(tm.girdle_layer(random.Random("girdle")), assets("textures", "models", "armor", "girdle_of_hippolyta_layer_2.png"))


def main():
    features()
    for metal in METALS:
        ore_loot(f"{metal}_ore", f"{NS}:raw_{metal}")
        self_loot(f"{metal}_block")
    ore_loot("hephaestus_coal_ore", f"{NS}:hephaestus_coal")
    ore_loot("muspel_ember_ore", f"{NS}:muspel_ember", 1, 2)
    recipes()
    tags()
    models()
    lang()
    if "--textures" in sys.argv:
        textures()


if __name__ == "__main__":
    main()
