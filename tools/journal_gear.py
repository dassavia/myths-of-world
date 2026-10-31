"""Journal pages about the ores, tools, weapons and armour of each world: where the ores lie and the numbers of every
piece of gear. Generated from the specs below, which mirror the Java side (GreekContent, NorseContent, MetalSet:
tier damage + item bonus + 1 for the hand). gen_greek_assets.py and gen_norse_assets.py add these entries to their
journals.
"""
import gen_metals as m

# Durability of each armour piece is its base times the material's multiplier (ArmorItem.Type.getDurability).
ARMOUR_BASE = {"helmet": 11, "chestplate": 16, "leggings": 15, "boots": 13}
PIECE_RU = {"helmet": "Шлем", "chestplate": "Нагрудник", "leggings": "Поножи", "boots": "Сапоги"}
PIECE_EN = {"helmet": "Helmet", "chestplate": "Chestplate", "leggings": "Leggings", "boots": "Boots"}

# Tool tiers: durability, mining speed, damage, enchantability, armour per piece, armour multiplier, toughness,
# knockback resistance per piece. Keep in step with the MetalSet.Stats in GreekContent / NorseContent.
TIERS = {
    "orichalcum": {"uses": 900, "speed": 7.0, "damage": 2.5, "ench": 22, "armour": (2, 7, 5, 2), "mult": 22,
                   "tough": 1.0, "kb": 0.0, "mines": ("железная", "an iron")},
    "bulat": {"uses": 1700, "speed": 8.0, "damage": 3.5, "ench": 16, "armour": (3, 8, 6, 3), "mult": 34,
              "tough": 2.0, "kb": 0.0, "mines": ("алмазная", "a diamond")},
    "dark_iron": {"uses": 2400, "speed": 8.5, "damage": 4.5, "ench": 14, "armour": (3, 8, 6, 3), "mult": 40,
                  "tough": 3.5, "kb": 0.1, "mines": ("незеритовая", "a netherite")},
}
# Bonus damage and attack speed of each tool (MetalSet: createAttributes(tier, bonus, speed - 4)).
TOOLS = {"sword": (3, 1.6), "axe": (5, 1.0), "pickaxe": (1, 1.2), "shovel": (1.5, 1.0), "hoe": (None, 4.0)}
TOOL_NAMES = {"sword": ("Меч", "Sword"), "axe": ("Топор", "Axe"), "pickaxe": ("Кирка", "Pickaxe"),
              "shovel": ("Лопата", "Shovel"), "hoe": ("Мотыга", "Hoe")}


def num(value):
    return f"{value:g}"


def paginate(title, paragraphs):
    """Packs (ru, en) paragraphs into pages that fit in both languages; returns the ru and en page lists."""
    import gen_greek_assets as g
    ru, en = [title[0]], [title[1]]
    page_ru, page_en = [], []

    def budget(lang_title):
        return g.BOOK_LINES - (2 + g.text_lines(lang_title, bold=True) if len(ru) == 1 else 0)

    for p_ru, p_en in paragraphs:
        try_ru, try_en = "\n".join(page_ru + [p_ru]), "\n".join(page_en + [p_en])
        if page_ru and (g.text_lines(try_ru) > budget(title[0]) or g.text_lines(try_en) > budget(title[1])):
            ru.append("\n".join(page_ru))
            en.append("\n".join(page_en))
            page_ru, page_en = [], []
        page_ru.append(p_ru)
        page_en.append(p_en)
    ru.append("\n".join(page_ru))
    en.append("\n".join(page_en))
    return ru, en


# Pickaxe each ore needs (gen_metals.py tags).
NEEDS = {"orichalcum": ("железная", "an iron"), "bulat": ("железная", "an iron"), "dark_iron": ("алмазная", "a diamond")}


def ore_lines(metal, fuel, fuel_ru, fuel_en):
    spec, f = m.METALS[metal], m.FUELS[fuel]
    lo, hi = spec["y"]
    flo, fhi = f["y"]
    return [
        (f"Руда {spec['ru_gen']}: высота от {lo} до {hi}, около {spec['count']} жил на чанк по {spec['size']} блоков, "
         f"в камне и глубинном сланце. Нужна {NEEDS[metal][0]} кирка, удача увеличивает добычу.",
         f"{spec['en']} ore: y {lo} to {hi}, about {spec['count']} veins a chunk of up to {spec['size']} blocks, in "
         f"stone and deepslate. Needs {NEEDS[metal][1]} pickaxe; Fortune gives more."),
        (f"{fuel_ru}: высота от {flo} до {fhi}, около {f['count']} жил на чанк. Горит {f['burn'] // 20} секунд "
         f"(уголь 80) и плавит {f['burn'] // 200} предметов.",
         f"{fuel_en}: y {flo} to {fhi}, about {f['count']} veins a chunk. Burns {f['burn'] // 20} seconds (coal 80) "
         f"and smelts {f['burn'] // 200} items."),
    ]


def tool_lines(metal):
    t = TIERS[metal]
    lines = [(f"Прочность {t['uses']}, скорость добычи {num(t['speed'])} (алмаз 8), зачаровываемость {t['ench']}. "
              f"Добывает всё, что и {t['mines'][0]} кирка.",
              f"Durability {t['uses']}, mining speed {num(t['speed'])} (diamond 8), enchantability {t['ench']}. "
              f"Mines everything {t['mines'][1]} pickaxe does.")]
    for tool, (bonus, speed) in TOOLS.items():
        ru, en = TOOL_NAMES[tool]
        damage = 1 if bonus is None else 1 + t["damage"] + bonus
        lines.append((f"{ru}: урон {num(damage)}, скорость атаки {num(speed)}",
                      f"{en}: damage {num(damage)}, attack speed {num(speed)}"))
    return lines


def armour_lines(metal):
    t = TIERS[metal]
    lines = []
    for (piece, base), defence in zip(ARMOUR_BASE.items(), t["armour"]):
        lines.append((f"{PIECE_RU[piece]}: броня {defence}, прочность {base * t['mult']}",
                      f"{PIECE_EN[piece]}: armour {defence}, durability {base * t['mult']}"))
    total = sum(t["armour"])
    kb = f", отбрасывание -{round(t['kb'] * 100)}% за вещь" if t["kb"] else ""
    kb_en = f", knockback -{round(t['kb'] * 100)}% a piece" if t["kb"] else ""
    lines.append((f"Весь комплект: броня {total}, твёрдость {num(t['tough'])} за вещь{kb}. Зачаровываемость {t['ench']}.",
                  f"Whole set: armour {total}, toughness {num(t['tough'])} a piece{kb_en}. Enchantability {t['ench']}."))
    return lines


BACK_SLOT = ("Элитры и крылья Дедала можно надеть в слот за спиной (справа от игрока в инвентаре) вместе с "
             "нагрудником: они летают и работают так же.",
             "Elytra and the wings of Daedalus can go in the back slot (right of the player in the inventory) together "
             "with a chestplate: they fly and work just the same.")


def greek():
    ores = paginate(("Руды Эллады", "Ores of Hellas"), ore_lines("orichalcum", "hephaestus_coal", "Уголь Гефеста",
                                                              "Hephaestus coal"))
    tools = paginate(("Орихалковое оружие", "Orichalcum Tools"), tool_lines("orichalcum"))
    armour = paginate(("Орихалковая броня", "Orichalcum Armour"), armour_lines("orichalcum"))
    weapons = paginate(("Оружие героев", "Weapons of the Heroes"), [
        ("Кинжал из когтя Немейского льва: урон 6, скорость 2.2, прочность 1561. Ранит Немейского льва.",
         "Nemean claw dagger: damage 6, attack speed 2.2, durability 1561. It wounds the Nemean Lion."),
        ("Харпа Персея: урон 7, скорость 1.6, прочность 250. Вдвое больнее бьёт Медузу.",
         "Harpe of Perseus: damage 7, attack speed 1.6, durability 250. Double damage to Medusa."),
        ("Двузубец Аида: одним ударом или ПКМ сразу повергает Цербера, затем исчезает.",
         "Bident of Hades: one blow or right-click fells Cerberus at once, then it is gone."),
        ("Факел Прометея и голова Медузы: 32 использования.", "Promethean torch and Medusa's head: 32 uses."),
    ])
    relics = paginate(("Доспехи героев", "Armour of the Heroes"), [
        ("Сет Немейского льва (шкура, кожа, когти, золото): шлем 2, нагрудник 7, поножи 5, лапы 2, твёрдость 1.5, "
         "отбрасывание -10%.",
         "Nemean lion set (pelt, leather, claws, gold): helmet 2, chest 7, legs 5, paws 2, toughness 1.5, knockback "
         "-10%."),
        ("Прочность 363/528/495/429. Весь сет: сила, стрелы и снаряды не ранят.",
         "Durability 363/528/495/429. Whole set: Strength, arrows and projectiles cannot wound you."),
        ("Таларии Гермеса: броня 3, прочность 390; скорость II, прыжок II, прыжки в воздухе без перезарядки, нет урона от падения.",
         "Talaria of Hermes: armour 3, durability 390; Speed II, Jump Boost II, air jumps with no cooldown, no fall damage."),
        ("Нагрудник титана: броня 7, твёрдость 1.5, отбрасывание -20%, прочность 640, не горит; сила и стойкость.",
         "Titan's breastplate: armour 7, toughness 1.5, knockback -20%, durability 640, fireproof; Strength and "
         "Resistance."),
        ("Пояс Ипполиты: броня 3 вместо поножей; сила II, стойкость II, скорость, регенерация.",
         "Girdle of Hippolyta: armour 3 in place of leggings; Strength II, Resistance II, Speed, Regeneration."),
        ("Крылья Дедала: прочность 240, высокий прыжок и плавный спуск, тают выше 200 днём.",
         "Wings of Daedalus: durability 240, a high jump and a gentle glide, melt above y 200 by day."),
        BACK_SLOT,
    ])
    return [("ores", "intro", None, *ores), ("orichalcum_tools", "intro", None, *tools),
            ("orichalcum_armour", "intro", None, *armour), ("weapons", "intro", None, *weapons),
            ("hero_armour", "intro", None, *relics)]


def norse():
    ores = paginate(("Руды Йотунхейма", "Ores of Jotunheim"), ore_lines("dark_iron", "muspel_ember",
                                                                      "Угли Муспельхейма", "Muspel embers"))
    tools = paginate(("Тёмножелезное оружие", "Dark Iron Tools"), tool_lines("dark_iron"))
    armour = paginate(("Тёмножелезная броня", "Dark Iron Armour"), armour_lines("dark_iron"))
    relics = paginate(("Оружие и доспехи богов", "Weapons and Armour of the Gods"), [
        ("Мьёльнир: урон 12.5, скорость 1, прочность 400. ПКМ: молния туда, куда вы смотрите; песок плавится в "
         "стекло, земля обугливается.",
         "Mjolnir: damage 12.5, attack speed 1, durability 400. Right-click: lightning where you look; sand melts "
         "into glass, earth is scorched."),
        ("Меч Сурта: урон 10.5, скорость 1.6, прочность 2400, не горит. Поджигает всё, по чему бьёт.",
         "Surtr's sword: damage 10.5, attack speed 1.6, durability 2400, fireproof. Sets whatever it strikes on fire."),
        ("Глейпнир: 4 использования, связывает Фенрира.", "Gleipnir: 4 uses, binds Fenrir."),
        ("Шлем Хеймдалля: броня 4, твёрдость 2.5, отбрасывание -10%, прочность 418. Ночное зрение, все существа "
         "в 100 блоках светятся сквозь стены.",
         "Helmet of Heimdall: armour 4, toughness 2.5, knockback -10%, durability 418. Night vision, every creature "
         "within 100 blocks glows through walls."),
        BACK_SLOT,
    ])
    return [("ores", "intro", None, *ores), ("dark_iron_tools", "intro", None, *tools),
            ("dark_iron_armour", "intro", None, *armour), ("gods_gear", "intro", None, *relics)]


def slavic():
    ores = paginate(("Руды Нави", "Ores of Nav"), [ore_lines("bulat", "hephaestus_coal", "", "")[0]])
    tools = paginate(("Булатное оружие", "Bulat Tools"), tool_lines("bulat"))
    armour = paginate(("Булатная броня", "Bulat Armour"), armour_lines("bulat"))
    relics = paginate(("Дары из сказок", "Gifts from the Tales"), [
        ("Меч-кладенец: урон 8.5, скорость 1.6, прочность 1700, не горит. Каждый удар рубит и врагов вокруг: "
         "урон 6 в 3 блоках.",
         "Sword kladenets: damage 8.5, attack speed 1.6, durability 1700, fireproof. Every blow also cuts the foes "
         "around: 6 damage within 3 blocks."),
        ("Сапоги-скороходы: броня 3, твёрдость 2, прочность 390. Скорость III и прыжок.",
         "Seven-league boots: armour 3, toughness 2, durability 390. Speed III and Jump Boost."),
        ("Шапка-невидимка: броня 3, твёрдость 2, прочность 330. Пока вы крадётесь, вас не видно.",
         "Cap of invisibility: armour 3, toughness 2, durability 330. While you sneak, no one can see you."),
        BACK_SLOT,
    ])
    return [("ores", "intro", None, *ores), ("bulat_tools", "intro", None, *tools),
            ("bulat_armour", "intro", None, *armour), ("gods_gear", "intro", None, *relics)]
