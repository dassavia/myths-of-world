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
