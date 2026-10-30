"""The Codex of Myths: the one book of the mod (Java side: codex/Codex.java and codex/CodexBook.java;
tools/gen_book.py turns it into the Patchouli book).

Writes data/mythsofworlds/journal/codex.json (the chapters, what opens each one and the steps of each world in their
intended order), the volumes of the chapters that have no journal of their own ("path": the hero's path, gear tiers
and armour powers; "far": the far worlds) and the lang entries of the Codex, the milestones, the armour powers and
the HUD. Run it after the other generators (gen_greek_assets.py ... gen_slavic_assets.py).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import gen_greek_assets as g  # noqa: E402
from gen_greek_assets import NS, assets, data, write_json  # noqa: E402
from journal_gear import paginate  # noqa: E402


def step(milestone, icon):
    return {"milestone": milestone, "icon": icon if ":" in icon else f"{NS}:{icon}"}


# id, volume, icon, requires, steps (milestone, icon) in the intended order.
CHAPTERS = [
    ("path", "path", "codex", [], []),
    ("hellas", "greek", "promethean_torch", [], [
        ("enter.hellas", "promethean_torch"), ("kill.nemean_lion", "nemean_pelt"), ("kill.medusa", "medusa_head"),
        ("kill.cyclops", "cyclops_eye"), ("kill.minotaur", "minotaur_horn"), ("kill.hydra", "hydra_scale"),
        ("kill.hippolyta", "girdle_of_hippolyta"), ("kill.cerberus", "cerberus_fang")]),
    ("nav", "slavic", "world_tree_acorn", ["kill.minotaur"], [
        ("enter.nav", "world_tree_acorn"), ("kill.solovei", "skorokhody"), ("kill.zmey_gorynych", "zmey_scale"),
        ("kill.koschei", "shapka_nevidimka")]),
    ("jotunheim", "norse", "rune_igniter", ["kill.cerberus", "kill.zmey_gorynych"], [
        ("enter.jotunheim", "rune_igniter"), ("kill.draugr_chieftain", "barrow_crown"), ("kill.garm", "garm_fang"),
        ("kill.heimdall", "heimdall_eye"), ("kill.thrym", "mjolnir"), ("kill.fenrir", "fenrir_fang"),
        ("kill.surtr", "surtr_sword")]),
    ("far", "far", "minecraft:recovery_compass", ["kill.surtr"], []),
]

CHAPTER_NAMES = {
    "path": ("Путь героя", "The Hero's Path"),
    "hellas": ("Эллада", "Hellas"),
    "nav": ("Навь", "Nav"),
    "jotunheim": ("Йотунхейм", "Jotunheim"),
    "far": ("Дальние миры", "The Far Worlds"),
}

MILESTONES = {
    "enter.hellas": ("Вы ступили в Элладу", "You set foot in Hellas"),
    "enter.nav": ("Вы спустились в Навь", "You went down into Nav"),
    "enter.jotunheim": ("Вы прошли по Биврёсту в Йотунхейм", "You crossed Bifrost into Jotunheim"),
    "kill.nemean_lion": ("Немейский лев повержен", "The Nemean Lion is slain"),
    "kill.medusa": ("Медуза Горгона повержена", "Medusa is slain"),
    "kill.cyclops": ("Циклоп повержен", "The Cyclops is slain"),
    "kill.minotaur": ("Минотавр повержен", "The Minotaur is slain"),
    "kill.hydra": ("Лернейская гидра повержена", "The Lernaean Hydra is slain"),
    "kill.hippolyta": ("Ипполита признала вашу силу", "Hippolyta yields to you"),
    "kill.cerberus": ("Цербер повержен", "Cerberus is slain"),
    "kill.solovei": ("Соловей-разбойник повержен", "Solovei the Robber is slain"),
    "kill.zmey_gorynych": ("Змей Горыныч повержен", "Zmey Gorynych is slain"),
    "kill.koschei": ("Кощей Бессмертный повержен", "Koschei the Deathless is slain"),
    "kill.draugr_chieftain": ("Вождь драугров повержен", "The Draugr Chieftain is slain"),
    "kill.garm": ("Гарм повержен", "Garm is slain"),
    "kill.heimdall": ("Хеймдалль повержен", "Heimdall is defeated"),
    "kill.thrym": ("Трим повержен", "Thrym is slain"),
    "kill.fenrir": ("Фенрир повержен", "Fenrir is slain"),
    "kill.surtr": ("Сурт повержен: путь героя пройден", "Surtr is slain: the hero's path is walked"),
}

# Attribute name, then what it does (for the Codex page).
POWERS = {
    "reflection": ("Отражение", "Reflection"),
    "lifesteal": ("Живая сила", "Lifesteal"),
    "monster_slaying": ("Гроза чудовищ", "Monster Slaying"),
    "divine_ward": ("Божья защита", "Divine Ward"),
    "evasion": ("Уклонение", "Evasion"),
    "fury": ("Ярость", "Fury"),
}

PATH_INTRO = ("Кодекс мифов", "Codex of Myths",
              "Одна книга на все миры. Главы открываются по мере того, как вы проходите путь героя, а записи "
              "пишутся сами, когда вы встречаете существ и находите места. В творческом режиме открыто всё.",
              "One book for every world. Chapters open as you walk the hero's path, and entries write themselves "
              "when you meet creatures and find places. In creative mode everything is open.")

PATH = [
    ("welcome", "intro", None, *paginate(("Как читать Кодекс", "How to Read the Codex"), [
        ("Слева - главы, по одной на каждый мир. Закрытая глава показывает замок и то, что её откроет.",
         "On the left are the chapters, one for each world. A locked chapter shows a lock and what will open it."),
        ("Записи о существах, боссах и местах появляются, когда вы их видите или побеждаете. Пока нет, на их месте "
         "знак вопроса.",
         "Entries on creatures, bosses and places appear once you see or defeat them. Until then a question mark "
         "stands in their place."),
        ("Первая страница каждого мира - карта его боссов в порядке, в каком их лучше проходить. Золотые уже "
         "повержены.",
         "The first page of each world is a map of its bosses in the order best taken. The gold ones are slain."),
    ])),
    ("order", "intro", None, *paginate(("Порядок миров", "Order of the Worlds"), [
        ("I. Эллада открыта сразу: хватит железа. Полубоссы: Немейский лев, Медуза, Циклоп. Боссы: Минотавр (300), "
         "Гидра (400), Цербер (450).",
         "I. Hellas is open from the start: iron is enough. Half-bosses: the Nemean Lion, Medusa, the Cyclops. "
         "Bosses: the Minotaur (300), the Hydra (400), Cerberus (450)."),
        ("II. Навь открывает рог Минотавра: он нужен для жёлудя Мирового древа. Эти два мира можно проходить "
         "вместе. Боссы: Соловей (300), Змей Горыныч (500), Кощей (550).",
         "II. Nav is opened by the Minotaur's horn: the acorn of the World Tree needs it. The two worlds can be "
         "travelled side by side. Bosses: Solovei (300), Zmey Gorynych (500), Koschei (550)."),
        ("III. Йотунхейм самый суровый. Рунное огниво требует клык Цербера и чешую Змея Горыныча. Боссы: вождь "
         "драугров (350), Гарм (400), Хеймдалль (450), Трим (550), Фенрир (650), Сурт (800).",
         "III. Jotunheim is the harshest. The rune igniter needs a fang of Cerberus and a scale of Zmey Gorynych. "
         "Bosses: the Draugr Chieftain (350), Garm (400), Heimdall (450), Thrym (550), Fenrir (650), Surtr (800)."),
        ("IV. Победа над Суртом открывает главу о дальних мирах.",
         "IV. Victory over Surtr opens the chapter of the far worlds."),
        ("Босс засчитывается всем игрокам в 64 блоках от него: на сервере друзья идут по пути вместе.",
         "A boss counts for every player within 64 blocks of it: on a server, friends walk the path together."),
    ])),
    ("tiers", "intro", None, *paginate(("Ступени снаряжения", "Tiers of Gear"), [
        ("Железо: меч 6, броня 15.", "Iron: sword 6, armour 15."),
        ("I. Орихалк (Эллада): меч 6.5, броня 16, твёрдость 1, прочность 900. Отражение.",
         "I. Orichalcum (Hellas): sword 6.5, armour 16, toughness 1, durability 900. Reflection."),
        ("II. Булат (Навь, руда в глубинах): меч 7.5, броня 20, твёрдость 2, прочность 1700. Живая сила и "
         "божья защита. Кирка добывает тёмное железо.",
         "II. Bulat (Nav, ore deep below): sword 7.5, armour 20, toughness 2, durability 1700. Lifesteal and divine "
         "ward. Its pickaxe mines dark iron."),
        ("III. Тёмное железо (Йотунхейм, нужна алмазная или булатная кирка): меч 8.5, броня 20, твёрдость 3.5, "
         "прочность 2400. Гроза чудовищ и божья защита.",
         "III. Dark iron (Jotunheim, needs a diamond or bulat pickaxe): sword 8.5, armour 20, toughness 3.5, "
         "durability 2400. Monster slaying and divine ward."),
        ("Дары боссов сильнее металла своего мира: кладенец 8.5, меч Сурта 10.5, Мьёльнир 12.5.",
         "The gifts of the bosses beat the metal of their world: kladenets 8.5, Surtr's sword 10.5, Mjolnir 12.5."),
    ])),
    ("powers", "intro", None, *paginate(("Силы доспехов", "Powers of the Armour"), [
        ("У брони и оружия мифов есть силы, которых нет в обычной игре. Они видны в подсказке предмета и "
         "складываются по всем надетым вещам.",
         "The armour and weapons of the myths have powers the plain game lacks. They show in the item's tooltip "
         "and add up over everything you wear."),
        ("Отражение: эта доля удара в ближнем бою возвращается врагу.",
         "Reflection: that share of a melee blow strikes the attacker back."),
        ("Живая сила: эта доля нанесённого урона лечит вас.", "Lifesteal: that share of the damage you deal heals you."),
        ("Гроза чудовищ: больше урона существам и богам мифов.",
         "Monster slaying: more damage to the creatures and gods of the myths."),
        ("Божья защита: меньше урона от существ и богов мифов.",
         "Divine ward: less damage from the creatures and gods of the myths."),
        ("Уклонение: шанс, что удар или стрела пройдут мимо.", "Evasion: a chance that a blow or an arrow misses."),
        ("Ярость: больше урона, когда у вас половина здоровья или меньше.",
         "Fury: more damage while you are at half health or less."),
    ])),
    ("bearers", "intro", None, *paginate(("Кто что даёт", "Who Gives What"), [
        ("Орихалк: отражение 5% за вещь. Нагрудник титана: отражение 15%.",
         "Orichalcum: reflection 5% a piece. Titan's breastplate: reflection 15%."),
        ("Булат: живая сила 2.5% и божья защита 3% за вещь. Кладенец: живая сила 10%.",
         "Bulat: lifesteal 2.5% and divine ward 3% a piece. Kladenets: lifesteal 10%."),
        ("Тёмное железо: гроза чудовищ 5% и божья защита 5% за вещь. Шлем Хеймдалля 10%, Мьёльнир и меч Сурта 15%, "
         "харпа 10% грозы чудовищ.",
         "Dark iron: monster slaying 5% and divine ward 5% a piece. Heimdall's helmet 10%, Mjolnir and Surtr's sword "
         "15%, the harpe 10% monster slaying."),
        ("Немейский сет: ярость 5% за вещь. Пояс Ипполиты: ярость 15% и живая сила 5%.",
         "Nemean set: fury 5% a piece. Girdle of Hippolyta: fury 15% and lifesteal 5%."),
        ("Таларии: уклонение 10%. Сапоги-скороходы: 8%. Шапка-невидимка: уклонение 5% и божья защита 8%.",
         "Talaria: evasion 10%. Seven-league boots: 8%. Cap of invisibility: evasion 5% and divine ward 8%."),
    ])),
    ("sets", "intro", None, *paginate(("Союз пантеонов", "Union of the Pantheons"), [
        ("Четыре вещи одного мира: Эллада - скорость и прыжок, Йотунхейм - сила и стойкость, Навь - ночное "
         "зрение и подводное дыхание.",
         "Four pieces of one world: Hellas - speed and jump boost, Jotunheim - strength and resistance, Nav - night "
         "vision and water breathing."),
        ("Вещи двух или трёх миров вместе: 2 дают спешку, 3 ещё огнестойкость, 4 ещё регенерацию, а две и две - "
         "стойкость.",
         "Pieces of two or three worlds together: 2 give haste, 3 also fire resistance, 4 also regeneration, and two "
         "and two give resistance."),
        ("Весь Немейский сет: сила, и снаряды его не пробивают.",
         "The whole Nemean set: strength, and projectiles cannot pierce it."),
    ])),
    ("hud", "intro", None, *paginate(("Знаки мифов", "Signs of the Myths"), [
        ("Здоровье, броня, сытость, воздух и опыт показаны резными полосами со старинными цифрами, а в мирах "
         "мифов вверху виден свиток с названием мира.",
         "Health, armour, hunger, air and experience are shown as carved bars with old-style numbers, and in the "
         "worlds of the myths a scroll at the top names the world."),
        ("Клавиша H (меняется в управлении) или кнопка в меню паузы прямо в игре включают и выключают этот вид. "
         "Тонкие настройки - в списке модов, кнопка Config.",
         "The H key (change it in the controls) or a button in the pause menu turns this look on and off right in "
         "the game. Finer settings are in the mod list, the Config button."),
    ])),
]

FAR_INTRO = ("Дальние миры", "The Far Worlds",
             "За краем известных мифов лежат ещё три мира. Их страницы пока пусты: скальды ещё не вернулись оттуда.",
             "Beyond the known myths lie three more worlds. Their pages are still blank: the skalds have not yet "
             "come back from there.")

FAR = [
    ("hawaiki", "intro", None, ["Гаваики", "Тёплое море и острова предков Полинезии. Путь туда ещё не найден."],
     ["Hawaiki", "A warm sea and the islands of the Polynesian ancestors. No way there has been found yet."]),
    ("duat", "intro", None, ["Дуат", "Пустыня вечной ночи, где странствует ладья Ра. Путь туда ещё не найден."],
     ["Duat", "A desert of everlasting night where the barque of Ra sails. No way there has been found yet."]),
    ("svarga", "intro", None, ["Сварга", "Джунгли вечного полдня, небо богов Индии. Путь туда ещё не найден."],
     ["Svarga", "A jungle of eternal noon, the heaven of the gods of India. No way there has been found yet."]),
]

LANG = {
    "item.mythsofworlds.codex": ("Кодекс мифов", "Codex of Myths"),
    "item.mythsofworlds.codex.desc": ("Все миры, существа и путь героя в одной книге",
                                      "Every world, creature and the hero's path in one book"),
    "codex.mythsofworlds.milestone": ("Путь героя: %s", "Hero's path: %s"),
    "codex.mythsofworlds.locked": ("Глава закрыта", "Chapter locked"),
    "codex.mythsofworlds.requires": ("Откроется, когда: %s", "Opens when: %s"),
    "codex.mythsofworlds.unknown": ("???", "???"),
    "codex.mythsofworlds.unknown_hint": ("Встретьте это, чтобы узнать больше", "Meet it to learn more"),
    "codex.mythsofworlds.map": ("Путь мира", "Path of the World"),
    "codex.mythsofworlds.back": ("Назад", "Back"),
    "codex.mythsofworlds.contents": ("Оглавление", "Contents"),
    "codex.mythsofworlds.progress": ("Найдено записей: %s из %s", "Entries found: %s of %s"),
    "codex.mythsofworlds.creative": ("Творческий режим: всё открыто", "Creative mode: everything is open"),
    "key.categories.mythsofworlds": ("Мифы миров", "Myths of Worlds"),
    "key.mythsofworlds.toggle_hud": ("Знаки мифов (HUD)", "Signs of the myths (HUD)"),
    "hud.mythsofworlds.on": ("Знаки мифов включены", "Signs of the myths on"),
    "hud.mythsofworlds.off": ("Знаки мифов выключены", "Signs of the myths off"),
    "hud.mythsofworlds.button": ("HUD мифов: %s", "Myth HUD: %s"),
    "hud.mythsofworlds.button.on": ("вкл", "on"),
    "hud.mythsofworlds.button.off": ("выкл", "off"),
    "hud.mythsofworlds.world.hellas": ("Эллада", "Hellas"),
    "hud.mythsofworlds.world.nav": ("Навь", "Nav"),
    "hud.mythsofworlds.world.jotunheim": ("Йотунхейм", "Jotunheim"),
    "hud.mythsofworlds.world.hawaiki": ("Гаваики", "Hawaiki"),
    "hud.mythsofworlds.world.duat": ("Дуат", "Duat"),
    "hud.mythsofworlds.world.svarga": ("Сварга", "Svarga"),
    "boss.mythsofworlds.bar": ("%s · %s", "%s · %s"),
    "boss.mythsofworlds.bar.enraged": ("%s · %s · в ярости", "%s · %s · enraged"),
    "boss.mythsofworlds.enraged": ("%s приходит в ярость!", "%s flies into a rage!"),
    "mythsofworlds.configuration.title": ("Мифы миров: настройки", "Myths of Worlds settings"),
    "mythsofworlds.configuration.hudEnabled": ("Знаки мифов (HUD)", "Signs of the myths (HUD)"),
    "mythsofworlds.configuration.hudEnabled.tooltip": ("Резные полосы здоровья, брони, сытости и опыта вместо обычных",
                                                       "Carved bars of health, armour, hunger and experience in place of the plain ones"),
    "mythsofworlds.configuration.showWorldName": ("Свиток с названием мира", "Scroll with the world's name"),
    "mythsofworlds.configuration.showWorldName.tooltip": ("Показывать вверху экрана название мира мифов",
                                                          "Show the name of the world of the myths at the top of the screen"),
    "mythsofworlds.configuration.showNumbers": ("Цифры на полосах", "Numbers on the bars"),
    "mythsofworlds.configuration.showNumbers.tooltip": ("Писать здоровье, сытость и броню числами",
                                                        "Write health, hunger and armour as numbers"),
    "mythsofworlds.configuration.bossHealth": ("Здоровье боссов (множитель)", "Boss health (multiplier)"),
    "mythsofworlds.configuration.bossHealth.tooltip": ("Во сколько раз больше здоровья у боссов и полубоссов мифов",
                                                       "How many times more health the bosses and half-bosses of the myths have"),
    "mythsofworlds.configuration.bossDamage": ("Урон боссов (множитель)", "Boss damage (multiplier)"),
    "mythsofworlds.configuration.bossDamage.tooltip": ("Во сколько раз сильнее бьют боссы: удары, огонь и снаряды",
                                                       "How many times harder the bosses hit: blows, fire and missiles"),
    "mythsofworlds.configuration.bossShareRange": ("Общая победа над боссом, блоков", "Shared boss victory, blocks"),
    "mythsofworlds.configuration.bossShareRange.tooltip": ("Победа засчитывается всем игрокам ближе этого расстояния",
                                                           "Every player closer than this to a fallen boss shares the victory"),
    "mythsofworlds.configuration.heimdallRange": ("Зоркость шлема Хеймдалля, блоков", "Sight of Heimdall's helmet, blocks"),
    "mythsofworlds.configuration.heimdallRange.tooltip": ("Существа ближе этого расстояния светятся сквозь стены",
                                                          "Creatures closer than this glow through the walls"),
    "mythsofworlds.configuration.journalSightRange": ("Дальность записи в Кодекс, блоков", "Codex sight range, blocks"),
    "mythsofworlds.configuration.journalSightRange.tooltip": ("Существо попадает в Кодекс, когда вы видите его ближе этого",
                                                              "A creature enters the Codex once you see it this close"),
}


def codex_icon():
    """The Codex: a thick tome in red leather with gold corners, clasp and a sun disc on the cover (32x32)."""
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(5, 6), (24, 3), (28, 25), (9, 29)], fill=(236, 222, 186))          # page block
    for i in range(4):
        d.line([(9 + i, 28 - i), (27 - i // 2, 24 - i)], fill=(200, 180, 140))
    d.polygon([(3, 5), (22, 2), (26, 24), (7, 28)], fill=(120, 30, 26), outline=(52, 12, 10))  # cover
    d.line([(4, 6), (21, 3)], fill=(170, 60, 50))
    d.line([(3, 5), (7, 28)], fill=(70, 16, 14), width=2)                                       # spine
    for cx, cy in ((5, 7), (21, 4), (24, 23), (8, 26)):
        d.polygon([(cx - 2, cy), (cx, cy - 2), (cx + 2, cy), (cx, cy + 2)], fill=(230, 180, 60), outline=(140, 96, 30))
    d.ellipse([10, 9, 19, 18], fill=(226, 179, 60), outline=(138, 96, 30))                   # sun disc
    d.ellipse([13, 12, 16, 15], fill=(255, 230, 140))
    for a in range(0, 360, 45):
        import math
        r = math.radians(a)
        d.point((14.5 + math.cos(r) * 6.5, 13.5 + math.sin(r) * 6.5), fill=(255, 226, 132))
    d.rectangle([24, 12, 28, 16], fill=(226, 179, 60), outline=(138, 96, 30))                # clasp
    img.save(assets("textures", "item", "codex.png"))


def main():
    codex_icon()
    write_json(assets("models", "item", "codex.json"),
               {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/codex"}})
    chapters = []
    for cid, volume, icon, requires, steps in CHAPTERS:
        chapters.append({"id": cid, "volume": volume, "icon": icon if ":" in icon else f"{NS}:{icon}",
                         "requires": requires, "steps": [step(m, i) for m, i in steps]})
    write_json(data("journal", "codex.json"), {"chapters": chapters})
    entries = dict(LANG)
    entries.update(g.journal("path", PATH_INTRO, PATH))
    entries.update(g.journal("far", FAR_INTRO, FAR))
    for cid, names in CHAPTER_NAMES.items():
        entries[f"codex.{NS}.chapter.{cid}"] = names
    for milestone, names in MILESTONES.items():
        entries[f"codex.{NS}.milestone.{milestone}"] = names
    for name, names in POWERS.items():
        entries[f"attribute.name.{NS}.{name}"] = names
    for index, code in ((0, "ru_ru"), (1, "en_us")):
        path = assets("lang", f"{code}.json")
        with open(path, encoding="utf-8") as f:
            current = json.load(f)
        for key, values in entries.items():
            current[key] = values[index]
        write_json(path, current)


if __name__ == "__main__":
    main()
