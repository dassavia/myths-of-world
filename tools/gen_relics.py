"""Relics of the gods and their sets: the bident of Hades, the talaria of Hermes, the Titan's breastplate, the eye and
helmet of Heimdall, and the scorched earth Mjolnir leaves behind.

Writes models, recipes, tags, loot and lang entries; with --textures also the item, armour layer and block textures.
Run it after gen_metals.py. Java side: mythology/relic (RelicArmorItem, ArmourSets, Relics), GreekContent, NorseContent.
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))
import gen_greek_assets as g  # noqa: E402
from gen_greek_assets import NS, assets, data, write_json  # noqa: E402
from gen_metals import self_loot, shaped  # noqa: E402

ITEMS = ["bident_of_hades", "talaria", "titan_breastplate", "heimdall_eye", "heimdall_helmet"]
HANDHELD = {"bident_of_hades"}

LANG = {
    "item.mythsofworlds.bident_of_hades": ("Двузубец Аида", "Bident of Hades"),
    "item.mythsofworlds.bident_of_hades.desc": (
        "Ударьте Цербера или нажмите ПКМ по нему: пёс Аида сразу падает. Срабатывает один раз",
        "Strike Cerberus or use it on him: the hound of Hades falls at once. Works only once"),
    "item.mythsofworlds.bident_of_hades.banished": ("Двузубец возвращается к Аиду, и Цербер уходит за ним в подземный мир!",
                                                    "The bident returns to Hades, and Cerberus follows it to the underworld!"),
    "item.mythsofworlds.talaria": ("Таларии Гермеса", "Talaria of Hermes"),
    "item.mythsofworlds.talaria.desc": ("Крылатые сандалии: скорость II, прыжок II, нет урона от падения",
                                        "Winged sandals: Speed II, Jump Boost II, no fall damage"),
    "item.mythsofworlds.titan_breastplate": ("Нагрудник титана", "Titan's Breastplate"),
    "item.mythsofworlds.titan_breastplate.desc": ("Сила и стойкость, вас трудно сбить с ног",
                                                  "Strength and Resistance, and you are hard to knock back"),
    "item.mythsofworlds.heimdall_eye": ("Око Хеймдалля", "Eye of Heimdall"),
    "item.mythsofworlds.heimdall_helmet": ("Шлем Хеймдалля", "Helmet of Heimdall"),
    "item.mythsofworlds.heimdall_helmet.desc": ("Ночное зрение, чудовища в 32 блоках светятся сквозь стены",
                                                "Night vision, monsters within 32 blocks glow through walls"),
    "item.mythsofworlds.relic.greek": ("Эллада: часть сета богов", "Hellas: part of a set of the gods"),
    "item.mythsofworlds.relic.norse": ("Йотунхейм: часть сета богов", "Jotunheim: part of a set of the gods"),
    "block.mythsofworlds.scorched_earth": ("Обугленная земля", "Scorched Earth"),
}


def models():
    for name in ITEMS:
        write_json(assets("models", "item", f"{name}.json"), {
            "parent": "minecraft:item/handheld" if name in HANDHELD else "minecraft:item/generated",
            "textures": {"layer0": f"{NS}:item/{name}"}})
    write_json(assets("blockstates", "scorched_earth.json"), {"variants": {"": {"model": f"{NS}:block/scorched_earth"}}})
    write_json(assets("models", "block", "scorched_earth.json"),
               {"parent": "minecraft:block/cube_all", "textures": {"all": f"{NS}:block/scorched_earth"}})
    write_json(assets("models", "item", "scorched_earth.json"), {"parent": f"{NS}:block/scorched_earth"})


def recipes():
    shaped("talaria", ["FGF", "FBF"], {"F": f"{NS}:harpy_feather", "G": "minecraft:gold_ingot", "B": "minecraft:golden_boots"},
           f"{NS}:talaria")
    shaped("titan_breastplate", ["OEO", "OCO", "OHO"],
           {"O": f"{NS}:orichalcum_ingot", "E": f"{NS}:cyclops_eye", "C": f"{NS}:orichalcum_chestplate", "H": f"{NS}:hydra_scale"},
           f"{NS}:titan_breastplate")
    shaped("heimdall_helmet", ["GEG", "GHG"],
           {"G": "minecraft:gold_ingot", "E": f"{NS}:heimdall_eye", "H": f"{NS}:dark_iron_helmet"}, f"{NS}:heimdall_helmet")


def tags():
    g.add_tag("item", "foot_armor", ["talaria"])
    g.add_tag("item", "chest_armor", ["titan_breastplate"])
    g.add_tag("item", "head_armor", ["heimdall_helmet"])
    g.add_tag("block", "mineable/shovel", ["scorched_earth"])
    self_loot("scorched_earth")


def lang():
    for index, code in ((0, "ru_ru"), (1, "en_us")):
        path = assets("lang", f"{code}.json")
        with open(path, encoding="utf-8") as f:
            current = json.load(f)
        for key, values in LANG.items():
            current[key] = values[index]
        write_json(path, current)


def textures():
    import textures_relics as tr
    for name, draw in tr.ITEMS.items():
        tr.save(tr.item(draw, random.Random(name)), assets("textures", "item", f"{name}.png"))
    for name, layer in tr.LAYERS.items():
        tr.save(layer(random.Random(name + "_layer")), assets("textures", "models", "armor", f"{name}_layer_1.png"))
    tr.save(tr.scorched_earth(random.Random("scorched_earth")), assets("textures", "block", "scorched_earth.png"))


def main():
    models()
    recipes()
    tags()
    lang()
    if "--textures" in sys.argv:
        textures()


if __name__ == "__main__":
    main()
