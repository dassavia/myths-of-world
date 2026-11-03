"""Text of the Book of the Dead, the journal of the Duat. Same format as journal_greek.py:
(id, category, unlock, [ru title, pages...], [en title, pages...]).
"""

NS = "mythsofworlds"


def mob(name):
    return ("entity", f"{NS}:{name}")


def place(name):
    return ("structure", f"{NS}:{name}")


INTRO = ("Книга мёртвых", "The Book of the Dead",
         "Свиток писцов Тота о Дуате, царстве вечной ночи, через которое каждую ночь плывёт ладья Ра. Встречайте "
         "существ, побеждайте чудовищ и находите места, и в свитке появятся новые главы.",
         "A scroll of the scribes of Thoth about the Duat, the realm of everlasting night that the barque of Ra sails "
         "through every night. Meet creatures, defeat monsters and find places, and new chapters write themselves.")

ENTRIES = [
    ("portal", "intro", None,
     ["Пирамида",
      "Путь в Дуат лежит через пирамиду. Сделайте камень пирамид: 8 песчаника вокруг золотого слитка дают 8 блоков.",
      "Постройте основание 5x5, на нём ступень 3x3, а на вершину поставьте золотой блок. Посередине одной стороны "
      "основания оставьте проход: пустой блок и воздух над ним.",
      "Анх: два золотых слитка, лазурит и чешуя гидры. Коснитесь пирамиды анхом, и в проходе откроются врата тени. "
      "Постойте в них 3 секунды. Обратно - тем же путём."],
     ["The Pyramid",
      "The way to the Duat runs through a pyramid. Make pyramid stone: 8 sandstone around a gold ingot give 8 blocks.",
      "Build a 5x5 base, a 3x3 step on it, and set a gold block on the top. In the middle of one side of the base "
      "leave a doorway: an empty block with air above it.",
      "The ankh: two gold ingots, lapis and a scale of the Hydra. Touch the pyramid with the ankh and a gate of "
      "shadow opens in the doorway. Stand in it for 3 seconds. Come back the same way."]),
    ("lands", "intro", None,
     ["Земли Дуата",
      "Над Дуатом вечная ночь и звёзды. Пески Дуата с руинами колонн, оазисы под финиковыми пальмами и берега "
      "Небесного Нила с тростником и лотосами.",
      "Поля Иалу - золотые луга блаженных. В Долине царей среди красных скал стоят гробницы, а на юге горит "
      "Огненное озеро, где таится змей Апоп."],
     ["The Lands of the Duat",
      "An everlasting night with stars hangs over the Duat. The sands with ruined columns, oases under date palms "
      "and the banks of the Celestial Nile with reeds and lotus.",
      "The Fields of Aaru are the golden meadows of the blessed. Tombs stand among the red cliffs of the Valley of "
      "the Kings, and in the south burns the Lake of Fire, where the serpent Apep lies in wait."]),
    ("gifts", "intro", None,
     ["Дары Нила",
      "Финики созревают в листве пальм: ПКМ по спелой листве. Медовая лепёшка: две пшеницы, мёд и финики, она "
      "лечит. Систр Хатхор: золото, два самородка и палка.",
      "Око Гора нужно против Сета, узел Исиды завоёвывает сердце жрицы. Их находят в сундуках храмов и гробниц, "
      "око продаёт и жрец Анубиса."],
     ["Gifts of the Nile",
      "Dates ripen among the palm fronds: right-click the ripe leaves. A honey cake is two wheat, honey and dates, "
      "and it heals. The sistrum of Hathor: gold, two nuggets and a stick.",
      "The eye of Horus is needed against Set, the knot of Isis wins a priestess's heart. They are found in the "
      "chests of temples and tombs, and the priest of Anubis sells the eye."]),

    ("mummy", "creature", mob("mummy"),
     ["Мумия",
      "Мертвец в жёлтых пеленах. Солнце ему не страшно, но смола в бинтах горит: огонь ранит мумию вдвое. "
      "Хватка вызывает голод и замедляет."],
     ["Mummy",
      "A dead man in yellowed wrappings. The sun does not harm it, but the resin in the bandages burns: fire wounds "
      "a mummy twice as much. Its grip brings hunger and slows."]),
    ("scarab", "creature", mob("scarab"),
     ["Скарабей",
      "Чёрный жук песков с сине-зелёным отливом, размером с кошку. Ходят роями: тронешь одного - придут все. Укус "
      "ядовит. Иногда роняют панцирь."],
     ["Scarab",
      "A black beetle of the sands with a blue-green sheen, as big as a cat. They come in swarms: touch one and "
      "the rest come too. The bite is poisonous. Sometimes they drop a shell."]),
    ("jackal", "creature", mob("jackal"),
     ["Шакал Анубиса",
      "Чёрный пёс пустыни с золотыми глазами, страж путей мёртвых. Быстр и охотится стаей."],
     ["Jackal of Anubis",
      "A black desert dog with golden eyes, the guardian of the ways of the dead. Fast, and hunts in packs."]),
    ("scorpion", "creature", mob("scorpion"),
     ["Скорпион",
      "Огромный скорпион богини Серкет в панцире, который не берут слабые удары. Жало несёт сильный яд и "
      "слабость."],
     ["Scorpion",
      "A giant scorpion of the goddess Serket, in a shell that turns light blows. Its sting carries a strong "
      "poison and weakness."]),
    ("ushabti", "creature", mob("ushabti"),
     ["Ушебти",
      "Фигурка слуги из голубого фаянса, что кладут в гробницы. В Дуате ушебти оживают и стерегут их. Стрелы "
      "лишь царапают глазурь, а кирка раскалывает глину вдвое."],
     ["Ushabti",
      "A servant figure of blue faience put in the tombs. In the Duat the ushabti wake and guard them. Arrows only "
      "chip the glaze, while a pickaxe cracks the clay twice as hard."]),
    ("bastet_cat", "creature", mob("bastet_cat"),
     ["Кошка Бастет",
      "Чёрная храмовая кошка с золотыми глазами. Приручается сырой рыбой. Мумии и скарабеи её боятся, а ручная "
      "кошка рядом с хозяином дарит ему регенерацию.",
      "Ра в облике великого кота убил змея Апопа. Ручные кошки Бастет бросаются на Апопа, и змей получает полный "
      "урон только от героя, рядом с которым кошка."],
     ["Cat of Bastet",
      "A black temple cat with golden eyes. Tamed with raw fish. Mummies and scarabs fear it, and a tame cat near "
      "its master gives them Regeneration.",
      "Ra in the shape of a great cat slew the serpent Apep. Tame cats of Bastet throw themselves on Apep, and the "
      "serpent takes full harm only from a hero with a cat at their side."]),
    ("priestess", "creature", mob("priestess"),
     ["Жрица Исиды",
      "Служительницы Исиды живут в её храмах на Ниле. Ухаживание как за амазонками: подарки и кольцо. Любят лотосы "
      "и цветы, золото и лазурит, мёд и финики, трофеи Дуата.",
      "Узел Исиды сразу её влюбляет, систр Хатхор зовёт разбредшихся домой. Подарите жене медовую лепёшку, и "
      "родится дочь-жрица."],
     ["Priestess of Isis",
      "The servants of Isis live in her temples on the Nile. Courted like the amazons: gifts and a ring. They love "
      "lotus and flowers, gold and lapis, honey and dates, and trophies of the Duat.",
      "The knot of Isis wins her heart at once, the sistrum of Hathor calls strays home. Give your wife a honey "
      "cake and a daughter is born, a priestess too."]),
    ("egyptian_merchant", "creature", mob("egyptian_merchant"),
     ["Торговцы Дуата",
      "В деревнях на Ниле живут торговец рынка (скупает трофеи, продаёт финики и лазурит), жрец Анубиса (анх, око "
      "Гора, систр, зелья) и кузнец (небесное железо и оружие из трофеев)."],
     ["Traders of the Duat",
      "In the villages on the Nile live a trader of the market (buys trophies, sells dates and lapis), a priest of "
      "Anubis (the ankh, the eye of Horus, the sistrum, potions) and a smith (meteoric iron and trophy weapons)."]),

    ("pharaoh_mummy", "boss", mob("pharaoh_mummy"),
     ["Мумия фараона",
      "Полубосс, 220 здоровья, в гробнице Долины царей. Проклятие гробницы замедляет работу рук и мучает голодом "
      "всех рядом. Ниже половины здоровья поднимает мумий.",
      "Огонь ранит его вдвое: берите горящие стрелы и заговор огня. Роняет хопеш, а в его сундуке всегда лежит "
      "око Гора."],
     ["Mummy of the Pharaoh",
      "A half-boss, 220 health, in a tomb in the Valley of the Kings. The curse of the tomb slows the hands and "
      "starves everyone near. Below half health he raises mummies.",
      "Fire wounds him twice: bring burning arrows and Fire Aspect. He drops the khopesh, and his chest always "
      "holds an eye of Horus."]),
    ("sphinx", "boss", mob("sphinx"),
     ["Сфинкс",
      "Каменный лев с головой царя, 350 здоровья, у Великого Сфинкса в песках. Не нападает первым. Рёв отбрасывает "
      "и замедляет, а ниже половины здоровья ослепляет песком.",
      "Тело Сфинкса из камня: стрелы лишь царапают его, а кирка бьёт вдвое. Роняет немес и когти."],
     ["Sphinx",
      "A stone lion with a king's head, 350 health, by the Great Sphinx in the sands. It does not attack first. "
      "Its roar throws back and slows, and below half health blinds with sand.",
      "Its body is stone: arrows only scratch it, while a pickaxe strikes twice as hard. Drops the nemes and its "
      "claws."]),
    ("set", "boss", mob("set"),
     ["Сет",
      "Красный бог пустыни и бурь, 500 здоровья, в храме в Долине царей. Песчаная буря ранит, ослепляет и "
      "отбрасывает; Сет переносится за спину врага и зовёт шакалов.",
      "Сет вырвал око Гора, а Гор исцелил его и победил: без ока Гора Сет получает лишь четверть урона, а с ним "
      "буря не слепит. Роняет посох уас."],
     ["Set",
      "The red god of the desert and of storms, 500 health, in a temple in the Valley of the Kings. His sandstorm "
      "wounds, blinds and throws back; he steps behind his foe and calls jackals.",
      "Set tore out the eye of Horus, and Horus healed it and beat him: without the eye Set takes only a quarter of "
      "the harm, and with it his storm cannot blind. Drops the was-sceptre."]),
    ("apep", "boss", mob("apep"),
     ["Апоп",
      "Змей хаоса, 600 здоровья, на острове в Огненном озере у обломков ладьи Ра. Укус ядовит, издали плюёт ядом, "
      "хвостом отбрасывает. Ниже половины здоровья зовёт скарабеев. Огонь ему не страшен.",
      "Возьмите с собой ручную кошку Бастет: без неё Апоп получает лишь половину урона, с ней - в полтора раза "
      "больше, а укус кошки рвёт его вчетверо. Роняет пектораль Ра."],
     ["Apep",
      "The serpent of chaos, 600 health, on an island in the Lake of Fire by the wreck of the barque of Ra. Its "
      "bite is venom, it spits venom from afar and sweeps with its tail. Below half health it calls scarabs. "
      "Fire cannot hurt it.",
      "Bring a tame cat of Bastet: without one Apep takes only half the harm, with one half as much again, and the "
      "cat's bite tears it four times as hard. Drops the pectoral of Ra."]),

    ("egyptian_village", "place", place("egyptian_village"),
     ["Деревня на Ниле",
      "Дома из сырцового кирпича с плоскими крышами вдоль канала, поля пшеницы и тростника, пальмы и колодцы. "
      "Здесь живут торговцы и кошки Бастет."],
     ["Village on the Nile",
      "Houses of mud brick with flat roofs along a canal, fields of wheat and reeds, palms and wells. Traders and "
      "the cats of Bastet live here."]),
    ("temple_of_isis", "place", place("temple_of_isis"),
     ["Храм Исиды",
      "Пилоны у ворот, двор со священным прудом и лотосами, колонны и святилище с троном богини. Здесь живут жрицы "
      "Исиды и храмовые кошки."],
     ["Temple of Isis",
      "Pylons at the gate, a court with a sacred pool and lotus, columns, and a sanctuary with the throne of the "
      "goddess. The priestesses of Isis and the temple cats live here."]),
    ("obelisk", "place", place("obelisk"),
     ["Обелиск",
      "Каменная игла в иероглифах с золотой вершиной. У подножия жертвенник и сундук жрецов: в нём бывает око Гора."],
     ["Obelisk",
      "A needle of stone carved with hieroglyphs, with a golden tip. At its foot an offering table and the chest of "
      "the priests, where an eye of Horus may lie."]),
    ("pharaoh_tomb", "place", place("pharaoh_tomb"),
     ["Гробница фараона",
      "Мастаба с наклонными стенами в Долине царей. В тёмном зале среди колонн - саркофаг из золота и лазурита, "
      "его стерегут мумии и ушебти."],
     ["Tomb of the Pharaoh",
      "A mastaba with sloping walls in the Valley of the Kings. In the dark hall among the columns stands a "
      "sarcophagus of gold and lapis, guarded by mummies and ushabti."]),
    ("great_sphinx", "place", place("great_sphinx"),
     ["Великий Сфинкс",
      "Огромный каменный лев с головой в полосатом немесе лежит в песках. Между его лапами - клад, у обелисков "
      "ждёт живой Сфинкс."],
     ["The Great Sphinx",
      "A huge lion of stone with a head in the striped nemes lies in the sands. Between its paws is a hoard, and by "
      "the obelisks waits the living Sphinx."]),
    ("temple_of_set", "place", place("temple_of_set"),
     ["Храм Сета",
      "Красные стены под ночным небом, колонны с огнями и чёрный алтарь с пламенем. Здесь Сет и его шакалы."],
     ["Temple of Set",
      "Red walls under the night sky, columns with fires and a black altar with a flame. Here wait Set and his "
      "jackals."]),
    ("apep_lair", "place", place("apep_lair"),
     ["Логово Апопа",
      "Остров чёрного камня в кольце лавы. На нём обломки золотой ладьи Ра, которую змей утащил на дно, и "
      "ещё горящий солнечный диск."],
     ["Lair of Apep",
      "An island of black rock in a ring of lava. On it lies the wreck of the golden barque of Ra that the serpent "
      "dragged down, its sun disc still glowing."]),
]


def with_gear():
    """The entries with the gear pages of journal_gear.py after the introduction pages."""
    import journal_gear
    intro = [entry for entry in ENTRIES if entry[1] == "intro"]
    rest = [entry for entry in ENTRIES if entry[1] != "intro"]
    return intro + journal_gear.egyptian() + rest
