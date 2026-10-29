"""Relics of the gods and their sets: the bident of Hades, the talaria of Hermes, the Titan's breastplate, the armour of
the Nemean lion, the eye and helmet of Heimdall, Brisingamen and the horn of Vingolf, and the scorched earth Mjolnir
leaves behind.

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

NEMEAN = ["nemean_helmet", "nemean_chestplate", "nemean_leggings", "nemean_boots"]
ITEMS = ["bident_of_hades", "talaria", "titan_breastplate", "heimdall_eye", "heimdall_helmet", "brisingamen",
         "horn_of_vingolf", "family_whistle"] + NEMEAN
HANDHELD = {"bident_of_hades"}

LANG = {
    "item.mythsofworlds.bident_of_hades": ("Двузубец Аида", "Bident of Hades"),
    "item.mythsofworlds.bident_of_hades.desc": (
        "Ударьте Цербера или нажмите ПКМ по нему: пёс Аида сразу падает. Срабатывает один раз",
        "Strike Cerberus or use it on him: the hound of Hades falls at once. Works only once"),
    "item.mythsofworlds.bident_of_hades.banished": ("Двузубец возвращается к Аиду, и Цербер уходит за ним в подземный мир!",
                                                    "The bident returns to Hades, and Cerberus follows it to the underworld!"),
    "item.mythsofworlds.talaria": ("Таларии Гермеса", "Talaria of Hermes"),
    "item.mythsofworlds.talaria.desc": ("Крылатые сандалии: скорость II, прыжок II, двойной прыжок (прыжок ещё раз в воздухе), нет урона от падения",
                                        "Winged sandals: Speed II, Jump Boost II, a double jump (jump again in mid-air), no fall damage"),
    "item.mythsofworlds.titan_breastplate": ("Нагрудник титана", "Titan's Breastplate"),
    "item.mythsofworlds.titan_breastplate.desc": ("Сила и стойкость, вас трудно сбить с ног",
                                                  "Strength and Resistance, and you are hard to knock back"),
    "item.mythsofworlds.heimdall_eye": ("Око Хеймдалля", "Eye of Heimdall"),
    "item.mythsofworlds.heimdall_helmet": ("Шлем Хеймдалля", "Helmet of Heimdall"),
    "item.mythsofworlds.heimdall_helmet.desc": ("Ночное зрение, все существа в 100 блоках светятся сквозь стены",
                                                "Night vision, every creature within 100 blocks glows through walls"),
    "item.mythsofworlds.nemean_helmet": ("Голова Немейского льва", "Nemean Lion's Head"),
    "item.mythsofworlds.nemean_helmet.desc": ("Пасть льва над лицом. Весь сет: сила, стрелы не ранят",
                                              "The lion's jaws over your face. Whole set: Strength, arrows cannot wound you"),
    "item.mythsofworlds.nemean_chestplate": ("Шкура Геракла", "Hide of Heracles"),
    "item.mythsofworlds.nemean_chestplate.desc": ("Шкура, которую не пробить стрелой. Весь сет: сила, стрелы не ранят",
                                                  "A hide no arrow can pierce. Whole set: Strength, arrows cannot wound you"),
    "item.mythsofworlds.nemean_leggings": ("Львиные поножи", "Nemean Leggings"),
    "item.mythsofworlds.nemean_leggings.desc": ("Весь сет: сила, стрелы не ранят", "Whole set: Strength, arrows cannot wound you"),
    "item.mythsofworlds.nemean_boots": ("Львиные лапы", "Nemean Paws"),
    "item.mythsofworlds.nemean_boots.desc": ("Весь сет: сила, стрелы не ранят", "Whole set: Strength, arrows cannot wound you"),
    "item.mythsofworlds.brisingamen": ("Брисингамен", "Brisingamen"),
    "item.mythsofworlds.horn_of_vingolf": ("Горн Вингольфа", "Horn of Vingolf"),
    "item.mythsofworlds.horn_of_vingolf.desc": ("ПКМ: валькирии вокруг возвращаются в свой чертог",
                                                "Right-click: the valkyries around go back to their hall"),
    "item.mythsofworlds.horn_of_vingolf.called": ("Горн трубит. Возвращаются в чертог: %s", "The horn sounds. Going home: %s"),
    "item.mythsofworlds.family_whistle": ("Семейный свисток", "Family Whistle"),
    "item.mythsofworlds.family_whistle.desc": ("ПКМ: жёны и дочери сразу приходят к вам из любого мира",
                                               "Right-click: your wives and daughters come to you at once from any world"),
    "item.mythsofworlds.family_whistle.called": ("Свисток зовёт вашу семью: %s", "The whistle calls your family: %s"),
    "item.mythsofworlds.family_whistle.nobody": ("Свисток звенит, но у вас нет ни жены, ни дочери",
                                                 "The whistle sounds, but you have no wife or daughter"),
    "item.mythsofworlds.family_whistle.arrived": ("%s пришла на ваш зов издалека", "%s came from afar at your call"),
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
    leather, pelt = "minecraft:leather", f"{NS}:nemean_pelt"
    shaped("nemean_helmet", ["CPC", "L L"], {"C": f"{NS}:nemean_claw", "P": pelt, "L": leather}, f"{NS}:nemean_helmet")
    shaped("nemean_chestplate", ["L L", "LPL", "LGL"], {"P": pelt, "L": leather, "G": "minecraft:gold_ingot"},
           f"{NS}:nemean_chestplate")
    shaped("nemean_leggings", ["LPL", "L L", "L L"], {"P": pelt, "L": leather}, f"{NS}:nemean_leggings")
    shaped("nemean_boots", ["L L", "LPL"], {"P": pelt, "L": leather}, f"{NS}:nemean_boots")
    write_json(data("recipe", "family_whistle.json"), {
        "type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": [{"item": "minecraft:gold_ingot"}, {"item": "minecraft:iron_nugget"}, {"item": "minecraft:ender_pearl"}],
        "result": {"id": f"{NS}:family_whistle", "count": 1},
    })
    write_json(data("recipe", "horn_of_vingolf.json"), {
        "type": "minecraft:crafting_shapeless", "category": "misc",
        "ingredients": [{"item": "minecraft:goat_horn"}, {"item": "minecraft:gold_ingot"}, {"item": f"{NS}:raven_feather"}],
        "result": {"id": f"{NS}:horn_of_vingolf", "count": 1},
    })
    shaped("heimdall_helmet", ["GEG", "GHG"],
           {"G": "minecraft:gold_ingot", "E": f"{NS}:heimdall_eye", "H": f"{NS}:dark_iron_helmet"}, f"{NS}:heimdall_helmet")


def tags():
    g.add_tag("item", "foot_armor", ["talaria", "nemean_boots"])
    g.add_tag("item", "chest_armor", ["titan_breastplate", "nemean_chestplate"])
    g.add_tag("item", "leg_armor", ["nemean_leggings"])
    g.add_tag("item", "head_armor", ["heimdall_helmet", "nemean_helmet"])
    write_json(data("tags", "worldgen", "structure", "valkyrie_homes.json"),
               {"replace": False, "values": [f"{NS}:valkyrie_hall"]})
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
    tr.save(tr.nemean_layer_1(random.Random("nemean_1")), assets("textures", "models", "armor", "nemean_layer_1.png"))
    tr.save(tr.nemean_layer_2(random.Random("nemean_2")), assets("textures", "models", "armor", "nemean_layer_2.png"))
    tr.save(tr.empty_slot_back(), assets("textures", "item", "empty_slot_back.png"))
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
