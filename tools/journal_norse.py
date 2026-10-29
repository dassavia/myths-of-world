"""Text of the Skald's Saga, the journal of Jotunheim. Same format as journal_greek.py:
(id, category, unlock, [ru title, pages...], [en title, pages...]).
"""

NS = "mythsofworlds"


def mob(name):
    return ("entity", f"{NS}:{name}")


def place(name):
    return ("structure", f"{NS}:{name}")


INTRO = ("Сага скальда", "Skald's Saga",
         "Песнь о землях великанов. Встречайте существ, побеждайте чудовищ и находите места Йотунхейма, "
         "и скальд сложит о них новые строки.",
         "A song of the lands of the giants. Meet creatures, defeat monsters and find the places of Jotunheim, "
         "and the skald adds new verses about them.")

ENTRIES = [
    ("portal", "intro", None,
     ["Врата Биврёста",
      "Сложите рамку из рунных камней, как для портала в Незер: внутри от 2 до 21x21 блоков пустоты. "
      "Рунный камень: 8 каменных кирпичей вокруг лазурита.",
      "Зажгите рамку рунным огнивом (кремень, железо, рунный камень и аметист). Внутри засияет радуга "
      "Биврёста: войдите в неё. Ломаете рамку - гаснет портал."],
     ["The Gate of Bifrost",
      "Build a frame of runestone like a Nether portal: from 2 up to 21x21 empty blocks inside. "
      "Runestone: 8 stone bricks around lapis lazuli.",
      "Light the frame with the Rune Igniter (flint, iron, runestone and amethyst). The rainbow of Bifrost "
      "shines inside: step into it. Break the frame and the portal goes out."]),
    ("lands", "intro", None,
     ["Земли Йотунхейма",
      "Ледяные пустоши и тайга великанов, лес Железного дерева, фьорды и холодное море. На юге тлеет разлом "
      "Муспельхейма, на севере стелются туманы Нифльхейма.",
      "Где-то цветёт сад Идунн: её молодильные яблоки зреют на листве, как плоды. Ночи здесь длинные, и днём "
      "солнце прогоняет троллей под землю."],
     ["The Lands of Jotunheim",
      "Frost wastes and the giants' taiga, the Ironwood forest, the fjords and a cold sea. In the south the rift "
      "of Muspelheim smoulders, in the north the mists of Niflheim creep.",
      "Somewhere Idunn's orchard blooms: her apples of youth ripen on the leaves like fruit. The nights are long, "
      "and by day the sun drives the trolls under the earth."]),

    ("dark_iron", "intro", None,
     ["Тёмное железо и угли",
      "Глубоко в камне Йотунхейма лежит руда тёмного железа двергов. Нужна железная кирка; переплавьте сырьё "
      "в слитки. Из них куют самое прочное оружие, инструменты и броню.",
      "В разломе Муспельхейма в камне тлеют угли Муспельхейма. В печи они горят втрое дольше угля, а "
      "валькирии ценят их как трофей."],
     ["Dark Iron and Embers",
      "Deep in the stone of Jotunheim lies the dwarves' dark iron ore. It needs an iron pickaxe; smelt the raw "
      "metal into ingots. They make the toughest weapons, tools and armour.",
      "In the rift of Muspelheim, embers smoulder in the stone. In a furnace they burn three times as long as "
      "coal, and valkyries prize them as trophies."]),

    ("god_sets", "intro", None,
     ['Сеты богов', 'Броня из разных мифологий складывается в сет. Эллада: орихалк, сет Немейского льва, пояс Ипполиты, таларии, нагрудник титана. Йотунхейм: тёмное железо, шлем Хеймдалля.', 'Союз пантеонов (обе мифологии): 2 вещи дают спешку, 3 - ещё огнестойкость, 4 - ещё регенерацию. Две и две - ещё и стойкость.', 'Только Эллада, 4 вещи: скорость и прыжок. Только Йотунхейм, 4 вещи: сила и стойкость.'],
     ['Sets of the Gods', "Armour of different mythologies adds up to a set. Hellas: orichalcum, the Nemean lion set, the girdle of Hippolyta, the talaria, the Titan's breastplate. Jotunheim: dark iron, the helmet of Heimdall.", 'Union of the pantheons (both mythologies): 2 pieces give Haste, 3 also Fire Resistance, 4 also Regeneration. Two and two also give Resistance.', 'Hellas only, 4 pieces: Speed and Jump Boost. Jotunheim only, 4 pieces: Strength and Resistance.']),

    # ---------------------------------------------------------------- creatures
    ("draugr", "creature", mob("draugr"),
     ["Драугр",
      "Мертвец из кургана в ржавой броне. Бродит по фьордам, пустошам и туманам Нифльхейма. Солнце его не "
      "жжёт, а удар морозит и замедляет.",
      "Убитый мечом, драугр встаёт ещё раз с половиной сил. Чтобы упокоить его навсегда, добейте его "
      "топором или огнём. Роняет гнилую плоть и кости."],
     ["Draugr",
      "A dead man from the barrows in rusted armour. He walks the fjords, the wastes and the mists of Niflheim. "
      "The sun does not burn him; his blow freezes and slows.",
      "Killed with a sword, a draugr rises once more at half strength. To lay him to rest for good, finish him "
      "with an axe or with fire. Drops rotten flesh and bones."]),
    ("warg", "creature", mob("warg"),
     ["Варг",
      "Огромный волк Железного леса, родня Фенрира. Охотится стаями: ударите одного - бросится вся стая. "
      "Прыгает на добычу издалека.",
      "Как победить: держитесь спиной к стене, бейте по одному и не убегайте по открытому снегу. "
      "Роняет кожу и кости."],
     ["Warg",
      "A huge wolf of the Ironwood, kin of Fenrir. They hunt in packs: hit one and the whole pack charges. "
      "It leaps at its prey from afar.",
      "How to beat: keep your back to a wall, fight them one at a time and do not run across open snow. "
      "Drops leather and bones."]),
    ("troll", "creature", mob("troll"),
     ["Тролль",
      "Каменная громада тайги и Железного леса. Бьёт сильно и сам залечивает раны, пока его не обожгут "
      "огнём. Днём прячется в тени.",
      "Главная слабость - солнце: тролль на солнечном свете обращается в камень и оставляет клык. "
      "Заманите его на открытое место на рассвете."],
     ["Troll",
      "A stone hulk of the taiga and the Ironwood. He hits hard and heals his wounds by himself, unless fire "
      "burns him. By day he hides in the shade.",
      "His great weakness is the sun: a troll in sunlight turns to stone and leaves a tusk behind. "
      "Lure him into the open at dawn."]),
    ("frost_giant", "creature", mob("frost_giant"),
     ["Инеистый великан",
      "Хримтурс ледяных пустошей ростом с два дома. Его удар замораживает: вы двигаетесь медленно и "
      "покрываетесь инеем.",
      "Как победить: огонь вдвое сильнее против него. Берите меч с заговором огня и горящие стрелы. "
      "Иногда роняет сердце мороза."],
     ["Frost Giant",
      "A rime-thurs of the frost wastes, tall as two houses. His blow freezes: you move slowly and frost "
      "covers you.",
      "How to beat: fire hurts him twice as much. Take a Fire Aspect sword and flaming arrows. "
      "Sometimes drops a frost heart."]),
    ("fire_giant", "creature", mob("fire_giant"),
     ["Огненный великан",
      "Сын Муспельхейма из огненного разлома. Бросает огненные шары и поджигает ударом. Огонь и лава ему "
      "не вредят.",
      "Как победить: снежки ранят его сильно, а вода жжёт. Ведро воды и запас снежков - лучшее оружие. "
      "Иногда роняет уголь Муспеля."],
     ["Fire Giant",
      "A son of Muspelheim from the fiery rift. He throws fireballs and his blow sets you alight. Fire and "
      "lava do not harm him.",
      "How to beat: snowballs hurt him badly and water burns him. A water bucket and a stack of snowballs are "
      "the best weapons. Sometimes drops a Muspel ember."]),
    ("raven", "creature", mob("raven"),
     ["Ворон",
      "Чёрная птица, как Хугин и Мунин, вороны Одина. Живёт в тайге, фьордах и саду Идунн, никого не "
      "трогает.",
      "Приручите ворона семенами, как попугая. Ручной ворон летает рядом и подсвечивает чудовищ вокруг "
      "хозяина, чтобы те не подкрались. Роняет перья."],
     ["Raven",
      "A black bird, like Huginn and Muninn, the ravens of Odin. It lives in the taiga, the fjords and Idunn's "
      "orchard and harms no one.",
      "Tame a raven with seeds, like a parrot. A tame raven flies nearby and makes the monsters around its "
      "owner glow, so none can sneak up. Drops feathers."]),
    ("norse_merchant", "creature", mob("norse_merchant"),
     ["Торговцы Севера",
      "Живут в поселениях викингов и кузнях. Управитель медового зала скупает трофеи и продаёт мёд. "
      "Двергкузнец меняет трофеи на алмазное снаряжение.",
      "Дверг продаёт и Глейпнир - путы для Фенрира. Вёльва продаёт яблоки Идунн, рунное огниво, "
      "зелья и резные рунные камни."],
     ["Merchants of the North",
      "They live in Viking villages and forges. The steward of the mead hall buys trophies and sells mead. "
      "The dwarven smith trades trophies for diamond gear.",
      "The dwarf also sells Gleipnir, the fetter for Fenrir. The volva sells Idunn's apples, the Rune Igniter, "
      "potions and carved runestones."]),

    ("valkyrie", "creature", mob("valkyrie"),
     ["Валькирия",
      "Дева щита Одина (46 здоровья, урон 9, броня 12). Живёт в чертогах валькирий на фьордах, в тайге и пустошах. Бьёт чудовищ, а за "
      "обиду отвечает вместе с сёстрами.",
      "Как амазонке, дарите ей подарки раз в 20 секунд: золото, оружие и щиты, трофеи чудовищ Севера или "
      "пир (мёд, мясо, яблоки Идунн). ПКМ пустой рукой: она скажет, что любит больше всего.",
      "При симпатии 100 наденьте ей обручальное кольцо. Жена-валькирия идёт за вами в бой. Поднесите ей "
      "мёд, и раз в день родится дочь, которая вырастет в валькирию.",
      "Брисингамен, ожерелье Фрейи, сразу влюбляет валькирию (симпатия 100). Его не скрафтить: ищите в кузницах "
      "двергов, в Утгарде и Химинбьёрге.",
      "Горн Вингольфа (козий рог, золото, перо ворона) зовёт валькирий домой, "
      "семейный свисток зовёт к вам жён и дочерей из любого мира."],
     ["Valkyrie",
      "A shield-maiden of Odin (46 health, damage 9, armour 12). She lives in the halls of the valkyries in the fjords, the taiga and the wastes. "
      "She fights monsters and answers an insult together with her sisters.",
      "As with an amazon, give her gifts once every 20 seconds: gold, weapons and shields, trophies of the "
      "North or a feast (mead, meat, Idunn's apples). Right-click with an empty hand: she says what she likes.",
      "At affection 100 give her a wedding ring. Your valkyrie wife follows you into battle. Give her mead and "
      "once a day a daughter is born, who grows up a valkyrie.",
      "Brisingamen, Freyja's necklace, wins a valkyrie's heart at once (affection 100). It cannot be crafted: look in "
      "the dwarf forges, Utgard and Himinbjorg.",
      "The horn of Vingolf (goat horn, gold, raven feather) calls the "
      "valkyries home; the family whistle calls your wives and daughters to you from any world."]),
    ("pegasus", "creature", mob("pegasus"),
     ["Пегас валькирий",
      "Белый крылатый конь, на котором валькирии уносят павших героев в Вальхаллу. Пасётся во фьордах и в "
      "тайге великанов, двое всегда стоят в конюшне чертога валькирий.",
      "Приручается как лошадь, конюшенные уже ручные. Высоко прыгает и плавно планирует. Наденьте седло."],
     ["Pegasus of the Valkyries",
      "White winged horse on which the valkyries carry fallen heroes to Valhalla. Grazes in the fjords and the "
      "giants' taiga; two always stand in the stable of a valkyrie hall.",
      "Tame it like a horse; the stable ones are tame already. It jumps very high and glides gently down. Put a "
      "saddle on it."]),

    # ---------------------------------------------------------------- bosses
    ("draugr_chieftain", "boss", mob("draugr_chieftain"),
     ["Вождь драугров",
      "Конунг, похороненный в кургане со своей дружиной. Носит золотой шлем и топор, стрелы почти не "
      "берут его броню.",
      "Поднимает из земли драугров и, как они, встаёт после первой смерти. Бейте топором или огнём. "
      "Роняет корону кургана."],
     ["Draugr Chieftain",
      "A king buried in a barrow with his warband. He wears a golden helm and wields an axe; arrows barely "
      "pierce his armour.",
      "He raises draugr from the ground and, like them, rises after his first death. Strike with an axe or "
      "fire. Drops the barrow crown."]),
    ("garm", "boss", mob("garm"),
     ["Гарм",
      "Пёс, что стережёт врата Хель в туманах Нифльхейма. Его вой окутывает тьмой и замедляет, укус "
      "ослабляет и морозит.",
      "Как победить: возьмите молоко против тьмы и сражайтесь у стен, где он не разгонится. "
      "Роняет клык Гарма.",
      "Пёс холодных туманов боится огня: пока Гарм горит, любой удар ранит его вдвое сильнее. Берите меч "
      "с заговором огня или горящие стрелы."],
     ["Garm",
      "The hound that guards the gates of Hel in the mists of Niflheim. His howl brings darkness and slows you, "
      "his bite weakens and freezes.",
      "How to beat: bring milk against the darkness and fight near walls where he cannot charge. "
      "Drops Garm's fang.",
      "The hound of the cold mists dreads fire: while Garm burns, every blow hurts him twice as much. Bring a "
      "Fire Aspect sword or flaming arrows."]),
    ("thrym", "boss", mob("thrym"),
     ["Трим, король великанов",
      "Владыка Утгарда, укравший молот Тора. Дышит морозом перед собой и топает так, что всё вокруг "
      "отлетает.",
      "Разгневанный, зовёт двух инеистых великанов. Огонь вдвое сильнее против него, не стойте прямо перед "
      "ним. Роняет Мьёльнир.",
      "Тор был погибелью великанов: Мьёльнир бьёт любого великана и тролля вдвое сильнее, а Трима, "
      "укравшего молот, - втрое. Отобранный молот пригодится в Муспельхейме.",
      "Молния Мьёльнира плавит песок в стекло, а траву и землю вокруг обугливает: остаётся чёрная "
      "обугленная земля."],
     ["Thrym, King of Giants",
      "The lord of Utgard, who stole Thor's hammer. He breathes frost ahead of him and stamps so hard that "
      "everything around flies off.",
      "Enraged, he calls two frost giants. Fire hurts him twice as much; do not stand right in front of him. "
      "Drops Mjolnir.",
      "Thor was the bane of giants: Mjolnir strikes every giant and troll twice as hard, and Thrym, who stole "
      "it, three times as hard. Take it back and carry it to Muspelheim.",
      "Mjolnir's lightning melts sand into glass and chars the grass and soil around it into black "
      "scorched earth."]),
    ("fenrir", "boss", mob("fenrir"),
     ["Фенрир",
      "Чудовищный волк, сын Локи, на острове Люнгви. Его укус иссушает, а свободный Фенрир быстро залечивает "
      "раны и зовёт варгов.",
      "Свяжите его Глейпниром (ПКМ по волку): на 8 секунд он не может кусать, едва движется и получает в "
      "полтора раза больше урона. Потом путы рвутся.",
      "Пока волк свободен, оружие людей почти не ранит его: любой удар наносит лишь четверть урона. "
      "Без Глейпнира его не одолеть - купите путы у дверга."],
     ["Fenrir",
      "The monstrous wolf, son of Loki, on the isle of Lyngvi. His bite withers, and a free Fenrir heals his "
      "wounds fast and calls wargs.",
      "Bind him with Gleipnir (use it on the wolf): for 8 seconds he cannot bite, barely moves and takes half "
      "again as much damage. Then the fetter snaps.",
      "While the wolf is free, the weapons of men barely wound him: every blow does only a quarter of its "
      "damage. Without Gleipnir he cannot be beaten - buy the fetter from the dwarf."]),
    ("heimdall", "boss", mob("heimdall"),
     ["Хеймдалль",
      "Страж богов у моста Биврёст в Химинбьёрге, 320 здоровья. Видит за сто миль и слышит, как растёт трава: "
      "стрелы ранят его втрое слабее.",
      "Трубит в Гьяллархорн: всех рядом отбрасывает, замедляет и оглушает. На половине здоровья трубит вдвое чаще. "
      "Бейтесь вблизи, отходите, когда он поднимает рог.",
      "Роняет око Хеймдалля. Око, золото и тёмножелезный шлем дают шлем Хеймдалля: ночное зрение, и все "
      "существа в 100 блоках светятся сквозь стены."],
     ["Heimdall",
      "Watchman of the gods at the Bifrost bridge in Himinbjorg, 320 health. He sees a hundred leagues and hears "
      "the grass grow: arrows hurt him only a third as much.",
      "He blows the Gjallarhorn: everyone near is thrown back, slowed and stunned. At half health he blows it twice "
      "as often. Fight up close and step back when he raises the horn.",
      "Drops the eye of Heimdall. The eye, gold and a dark iron helmet make the helmet of Heimdall: night vision, "
      "and every creature within 100 blocks glows through the walls."]),
    ("surtr", "boss", mob("surtr"),
     ["Сурт",
      "Огненный великан с пылающим мечом, владыка Муспельхейма. Мечет огненные шары, разжигает вокруг "
      "себя кольцо пламени.",
      "Разгневанный, обрушивает огненный дождь. Снежки, вода и молнии Мьёльнира ранят его сильнее. "
      "Возьмите зелья огнестойкости. Роняет меч Сурта.",
      "Жар Сурта притупляет клинки и стрелы: они ранят его вдвое слабее. Держите во второй руке сердце "
      "инея, добытое у инеистых великанов, - и оружие бьёт в полную силу."],
     ["Surtr",
      "The fire giant with the flaming sword, lord of Muspelheim. He hurls fireballs and kindles a ring of "
      "flame around himself.",
      "Enraged, he brings down a rain of fire. Snowballs, water and Mjolnir's lightning hurt him more. "
      "Bring fire resistance potions. Drops the Sword of Surtr.",
      "Surtr's heat blunts blades and arrows: they wound him only half as deep. Hold a frost heart, taken "
      "from the frost giants, in your other hand and your weapon strikes at full strength."]),

    # ---------------------------------------------------------------- places
    ("viking_village", "place", place("viking_village"),
     ["Поселение викингов",
      "Медовый зал, длинные дома, кузня и хижина вёльвы над фьордом. Здесь живут торговцы Севера, "
      "а в сундуках хранятся припасы и мёд."],
     ["Viking Village",
      "A mead hall, longhouses, a smithy and the volva's hut above a fjord. The merchants of the North live "
      "here, and the chests keep supplies and mead."]),
    ("longship", "place", place("longship"),
     ["Драккар",
      "Корабль с головой дракона на носу, у берегов фьордов и в море. В трюме сундук с добычей набега."],
     ["Longship",
      "A ship with a dragon's head on the prow, off the fjords and out at sea. A chest of raiding loot "
      "lies in the hold."]),
    ("naglfar", "place", place("naglfar"),
     ["Нагльфар",
      "Корабль мертвецов, сложенный из ногтей. Плавает в открытом море с командой драугров. "
      "Захватите его - богатый сундук стоит того."],
     ["Naglfar",
      "The ship of the dead, built from nails. It sails the open sea with a crew of draugr. "
      "Take it: its rich chest is worth it."]),
    ("barrow", "place", place("barrow"),
     ["Курган",
      "Травяной холм с каменным входом. Внутри спит вождь драугров с дружиной и лежит его клад: "
      "золото и зачарованное оружие."],
     ["Barrow",
      "A grassy mound with a stone entrance. The draugr chieftain sleeps inside with his warband, beside "
      "his hoard of gold and enchanted weapons."]),
    ("utgard", "place", place("utgard"),
     ["Утгард",
      "Ледяной чертог великанов среди пустошей. На троне сидит Трим, у дверей стоят инеистые великаны. "
      "Сундуки полны трофеев."],
     ["Utgard",
      "The ice hall of the giants out in the wastes. Thrym sits on the throne, frost giants stand by the "
      "doors. The chests are full of trophies."]),
    ("fenrir_island", "place", place("fenrir_island"),
     ["Остров Люнгви",
      "Скала в Железном лесу, где боги сковали Фенрира. Цепи порваны, и волк ждёт вас. "
      "Не приходите без Глейпнира."],
     ["Isle of Lyngvi",
      "The rock in the Ironwood where the gods bound Fenrir. The chains are broken and the wolf awaits. "
      "Do not come without Gleipnir."]),
    ("muspel_fortress", "place", place("muspel_fortress"),
     ["Крепость Сурта",
      "Чёрная крепость за рвом лавы в разломе Муспельхейма. Внутри Сурт и огненные великаны. "
      "Возьмите воду, снежки и огнестойкость."],
     ["Fortress of Surtr",
      "A black fortress behind a lava moat in the rift of Muspelheim. Surtr and the fire giants wait inside. "
      "Bring water, snowballs and fire resistance."]),
    ("helgrind", "place", place("helgrind"),
     ["Врата Хель",
      "Высокие ворота в туманах Нифльхейма, за которыми царство мёртвых. Их сторожит пёс Гарм."],
     ["Gates of Hel",
      "Tall gates in the mists of Niflheim, the way to the realm of the dead. The hound Garm guards them."]),
    ("dwarf_forge", "place", place("dwarf_forge"),
     ["Кузня двергов",
      "Мастерская в скале, где дверги куют оружие. Здесь продают Глейпнир и алмазное снаряжение."],
     ["Dwarven Forge",
      "A workshop in the rock where dwarves forge weapons. Gleipnir and diamond gear are sold here."]),
    ("himinbjorg", "place", place("himinbjorg"),
     ["Химинбьёрг",
      "Чертог Хеймдалля на высокой террасе, со сторожевой башней. От ворот вниз сбегает радужный мост Биврёст, "
      "у его начала стоит сам страж богов."],
     ["Himinbjorg",
      "Heimdall's hall on a high terrace, with a watchtower. The rainbow bridge Bifrost runs down from the gate, "
      "and the watchman of the gods stands at its head."]),
    ("valkyrie_hall", "place", place("valkyrie_hall"),
     ["Чертог валькирий",
      "Длинный зал, увешанный щитами, с конюшней крылатых коней и площадкой для учебного боя. Здесь живут "
      "валькирии, на которых можно жениться."],
     ["Hall of the Valkyries",
      "A long hall hung with shields, with a stable of winged horses and a training ground. The valkyries live "
      "here, and they can be wed."]),
    ("rune_circle", "place", place("rune_circle"),
     ["Рунный круг",
      "Кольцо стоячих камней с горящими рунами. Здесь живут вороны, а в центре лежит сундук с подношениями."],
     ["Rune Circle",
      "A ring of standing stones with glowing runes. Ravens live here, and a chest of offerings lies in "
      "the centre."]),
]


def with_gear():
    """The entries with the ore and gear pages of journal_gear.py after the introduction pages."""
    import journal_gear
    intro = [entry for entry in ENTRIES if entry[1] == "intro"]
    rest = [entry for entry in ENTRIES if entry[1] != "intro"]
    return intro + journal_gear.norse() + rest
