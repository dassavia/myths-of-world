"""Translations of the 0.16 additions that have no generator of their own: client settings, key bindings, action-bar
messages, the traveller's boat, the sounds of Isis and the MCA Reborn compatibility. Like the other scripts it adds
and updates its keys in lang/ru_ru.json and lang/en_us.json without touching the rest.

    python3 tools/gen_lang_extra.py
"""
import collections
import json
import os

LANG = os.path.join(os.path.dirname(__file__), "..", "src", "main", "resources", "assets", "mythsofworlds", "lang")

# key: (Russian, English). Keys are placed after the anchor named in AFTER, or at the end.
EXTRA = {
    "itemGroup.mythsofworlds": ("Мифы миров", "Myths of Worlds"),
    "mythsofworlds.configuration.codexFont": ("Чистый шрифт Кодекса", "Clean font in the Codex"),
    "mythsofworlds.configuration.codexFont.tooltip": ("Писать Кодекс мифов чётким шрифтом мода с полной кириллицей вместо шрифта Patchouli",
                                                      "Write the Codex of Myths in the mod's clear font with full Cyrillic instead of Patchouli's"),
    "mythsofworlds.configuration.worldBannerScale": ("Размер свитка с названием мира", "Size of the world's name banner"),
    "mythsofworlds.configuration.worldBannerScale.tooltip": ("От четверти до полного свитка; надпись остаётся читаемой при любом масштабе интерфейса",
                                                             "From a quarter to the full scroll; the name stays readable at every GUI scale"),
    "mythsofworlds.configuration.mcaSkins": ("Облики MCA для жриц, амазонок и валькирий", "MCA looks for priestesses, amazons and valkyries"),
    "mythsofworlds.configuration.mcaSkins.tooltip": ("Если установлен MCA Reborn, они надевают его женские облики, у каждой свой; Исида остаётся собой. Без MCA всегда свои текстуры",
                                                     "With MCA Reborn installed they wear its women's looks, each her own; Isis stays herself. Without MCA the mod's own textures are used"),
    "item.mythsofworlds.travelers_boat": ("Лодка странника", "Traveler's Boat"),
    "entity.mythsofworlds.travelers_boat": ("Лодка странника", "Traveler's Boat"),
    "key.mythsofworlds.heimdall_vision": ("Взор Хеймдалля", "Heimdall's vision"),
    "hud.mythsofworlds.heimdall_vision.on": ("Взор Хеймдалля: включён", "Heimdall's vision: on"),
    "hud.mythsofworlds.heimdall_vision.off": ("Взор Хеймдалля: выключен", "Heimdall's vision: off"),
    "hud.mythsofworlds.heimdall_vision.disabled": ("Взор Хеймдалля выключен на этом сервере", "Heimdall's vision is turned off on this server"),
    "mythsofworlds.configuration.heimdallVision": ("Взор Хеймдалля", "Heimdall's vision"),
    "mythsofworlds.configuration.heimdallVision.tooltip": ("Ночное зрение и подсветка существ в 100 блоках от шлема Хеймдалля. Также клавиша N",
                                                           "Night vision and the glow of creatures within 100 blocks from the helmet of Heimdall. Also the N key"),
    "mythsofworlds.configuration.heimdallVisionAllowed": ("Взор Хеймдалля на сервере", "Heimdall's vision on the server"),
    "mythsofworlds.configuration.heimdallVisionAllowed.tooltip": ("Если выключено, шлем Хеймдалля не даёт взора никому на этом сервере",
                                                                  "If off, the helmet of Heimdall gives its vision to no one on this server"),
    "mythsofworlds.configuration.mca": ("MCA Reborn", "MCA Reborn"),
    "mythsofworlds.configuration.mca.tooltip": ("Совместная работа с Minecraft Comes Alive Reborn (если установлен)",
                                                "Working together with Minecraft Comes Alive Reborn (when installed)"),
    "mythsofworlds.configuration.mcaCompat": ("Совместимость с MCA Reborn", "MCA Reborn compatibility"),
    "mythsofworlds.configuration.mcaCompat.tooltip": ("Стража MCA бьёт чудовищ мифов и не трогает богов, торговцев и мирных существ",
                                                      "MCA's guards fight the monsters of the myths and leave gods, traders and friendly creatures alone"),
    "mythsofworlds.configuration.mcaNoDoubleResidents": ("Без двойных жителей", "No double residents"),
    "mythsofworlds.configuration.mcaNoDoubleResidents.tooltip": ("В постройках мифов житель MCA не появляется рядом с торговцем или жрицей, который там уже живёт",
                                                                 "In the buildings of the myths, an MCA villager is not added next to a trader or priestess who already lives there"),
}

AFTER = {
    "mythsofworlds.configuration.worldBannerScale": "mythsofworlds.configuration.showWorldName.tooltip",
    "mythsofworlds.configuration.codexFont": "mythsofworlds.configuration.showNumbers.tooltip",
}


def main():
    for code, index in (("ru_ru", 0), ("en_us", 1)):
        path = os.path.join(LANG, code + ".json")
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        items = [(k, v) for k, v in json.loads(raw, object_pairs_hook=collections.OrderedDict).items() if k not in EXTRA]
        anchor = None
        for key, values in EXTRA.items():
            keys = [k for k, _ in items]
            target = AFTER.get(key, anchor)
            pos = keys.index(target) + 1 if target in keys else len(items)
            items.insert(pos, (key, values[index]))
            anchor = key
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(collections.OrderedDict(items), ensure_ascii=False, indent=2) + ("\n" if raw.endswith("\n") else ""))


if __name__ == "__main__":
    main()
