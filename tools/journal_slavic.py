"""Text of the Tales of Boyan, the journal of Nav. Same format as journal_greek.py:
(id, category, unlock, [ru title, pages...], [en title, pages...]).
"""

NS = "mythsofworlds"


def mob(name):
    return ("entity", f"{NS}:{name}")


def place(name):
    return ("structure", f"{NS}:{name}")


INTRO = ("Сказы Бояна", "Tales of Boyan",
         "Вещий Боян поёт о Нави, мире под корнями Мирового древа. Встречайте существ, побеждайте чудищ и "
         "находите места, и в книге сложатся новые сказы.",
         "Boyan the seer sings of Nav, the world under the roots of the World Tree. Meet creatures, defeat monsters "
         "and find places, and new tales write themselves in the book.")

ENTRIES = [
    ("portal", "intro", None,
     ["Мировое древо",
      "В Навь не строят врат: туда спускаются по корням Мирового древа. Сделайте жёлудь Мирового древа: "
      "саженец дуба, золотой слиток, светящиеся ягоды и рог Минотавра.",
      "Посадите жёлудь на траву или землю (ПКМ по верху блока). Вырастет великий дуб, а у его корней - дупло, "
      "обращённое к вам. Нужно место 3x3 и 11 блоков в высоту.",
      "Войдите в дупло и постойте 3 секунды: вы спуститесь в Навь и выйдете у такого же дуба. Обратно - тем же "
      "путём. Срубите ствол у дупла, и оно закроется."],
     ["The World Tree",
      "No gate is built to Nav: you go down along the roots of the World Tree. Make an acorn of the World Tree: "
      "an oak sapling, a gold ingot, glow berries and a horn of the Minotaur.",
      "Plant the acorn on grass or dirt (right-click the top of the block). A great oak grows, with a hollow at "
      "its roots facing you. It needs a 3x3 space 11 blocks high.",
      "Step into the hollow and stand for 3 seconds: you go down to Nav and come out by an oak just like it. "
      "Come back the same way. Cut the trunk by the hollow and it closes."]),
    ("lands", "intro", None,
     ["Земли Нави",
      "Над Навью вечные сумерки. Дремучий лес и берёзовые рощи, кикиморино болото, дикое поле и море-Окиян.",
      "На юге течёт огненная река Смородина, через неё перекинут Калинов мост. На севере лежит Кощеево царство: "
      "серая земля, мёртвые деревья и кости."],
     ["The Lands of Nav",
      "An endless dusk hangs over Nav. The dense forest and birch groves, the kikimora bog, the wild field and "
      "the Sea-Okiyan.",
      "In the south flows the fiery river Smorodina, with the Kalinov bridge across it. In the north lies the "
      "realm of Koschei: grey earth, dead trees and bones."]),
    ("waters", "intro", None,
     ["Живая и мёртвая вода",
      "Мёртвая вода сращивает раны: сопротивление II и поглощение III на минуту. Живая вода сразу лечит и "
      "даёт регенерацию II.",
      "Обе продаёт Баба-яга, иногда их находят в сундуках. Каравай - сытный хлеб: три пшеницы, яйцо и мёд."],
     ["Water of Life and Dead Water",
      "Dead water closes wounds: Resistance II and Absorption III for a minute. The water of life heals at once "
      "and gives Regeneration II.",
      "Baba Yaga sells both, and they turn up in chests. Karavai is a filling loaf: three wheat, an egg and honey."]),

    ("leshy", "creature", mob("leshy"),
     ["Леший",
      "Хозяин леса, высокий старик из коры и мха. Не трогайте его, и он не тронет вас.",
      "Разгневанный леший бьёт больно, а каждый удар ослепляет и уводит: вы оказываетесь в другом месте "
      "его леса. Иногда роняет жёлудь Мирового древа."],
     ["Leshy",
      "Master of the forest, a tall old man of bark and moss. Leave him alone, and he leaves you alone.",
      "An angry leshy hits hard, and every blow blinds you and leads you astray: you find yourself somewhere "
      "else in his woods. Sometimes he drops an acorn of the World Tree."]),
    ("kikimora", "creature", mob("kikimora"),
     ["Кикимора",
      "Маленькая кривая болотная нечисть с волосами из мха. Прыгает из тины, а её хватка тянет в грязь: "
      "сильное замедление и голод."],
     ["Kikimora",
      "A small crooked bog spirit with moss for hair. She leaps out of the mire, and her grip drags you into "
      "the mud: strong Slowness and Hunger."]),
    ("upyr", "creature", mob("upyr"),
     ["Упырь",
      "Мертвец, что пьёт кровь живых: каждый укус лечит его. Солнце жжёт упыря, но в сумерках Нави ему "
      "ничего не грозит. Из клыков упыря кузнец выкует меч."],
     ["Upyr",
      "A dead man who drinks the blood of the living: every bite heals him. The sun burns an upyr, but in the "
      "dusk of Nav he has nothing to fear. A smith forges a sword from upyr fangs."]),
    ("volkolak", "creature", mob("volkolak"),
     ["Волколак",
      "Колдун в шкуре огромного волка. Охотится стаей и в бою становится сильнее. Его шкуру ценят "
      "купцы и кузнецы."],
     ["Volkolak",
      "A sorcerer in the skin of a huge wolf. He hunts in packs and grows stronger in a fight. Merchants and "
      "smiths prize his pelt."]),
    ("rusalka", "creature", mob("rusalka"),
     ["Русалка",
      "Бледная дева с зелёными волосами в болотах и у моря. Её песня тянет вас к ней, а холодное "
      "прикосновение отнимает силу рук. Под водой она плавает быстро."],
     ["Rusalka",
      "A pale maiden with green hair in the bogs and by the sea. Her song draws you to her, and her cold touch "
      "takes the strength from your hands. Under water she swims fast."]),
    ("firebird", "creature", mob("firebird"),
     ["Жар-птица",
      "Птица с перьями как жар. Погладьте её пустой рукой, и она уронит перо - раз в две минуты. Перо "
      "в руке освещает сумерки: ночное зрение.",
      "Приручите её семенами, как ворона: она летает за вами и подсвечивает чудищ вокруг. Живёт в "
      "рощах и у капищ."],
     ["Firebird",
      "A bird with feathers like embers. Stroke her with an empty hand and she lets fall a feather, once every "
      "two minutes. A feather in your hand lights the dusk: Night Vision.",
      "Tame her with seeds, like a raven: she flies after you and lights up the monsters around. She lives in "
      "the groves and by the shrines."]),
    ("slavic_merchant", "creature", mob("slavic_merchant"),
     ["Торговцы Нави",
      "В деревнях живут купец и кузнец. Купец берёт трофеи и продаёт каравай, мёд и жёлуди. Кузнец "
      "куёт из трофеев алмазное оружие и броню.",
      "Баба-яга живёт в избушке на курьих ножках. Она продаёт живую и мёртвую воду, жёлуди Мирового "
      "древа и зелья."],
     ["Traders of Nav",
      "A merchant and a smith live in the villages. The merchant takes trophies and sells karavai, honey and "
      "acorns. The smith forges trophies into diamond weapons and armour.",
      "Baba Yaga lives in a hut on chicken legs. She sells the water of life and dead water, acorns of the "
      "World Tree and potions."]),

    ("solovei", "boss", mob("solovei"),
     ["Соловей-разбойник",
      "Сидит в гнезде на девяти дубах над дорогой. Его свист - буря: всех вокруг ранит, отбрасывает далеко "
      "и оглушает. Раненый, свистит чаще.",
      "Держитесь вплотную или стреляйте издалека, за 16 блоками свист не достанет. С него падают "
      "сапоги-скороходы."],
     ["Solovei the Robber",
      "He sits in his nest on nine oaks over the road. His whistle is a storm: everyone around is hurt, thrown "
      "far back and dazed. Wounded, he whistles more often.",
      "Stay close or shoot from afar, beyond 16 blocks the whistle cannot reach. He drops the seven-league "
      "boots."]),
    ("zmey_gorynych", "boss", mob("zmey_gorynych"),
     ["Змей Горыныч",
      "Трёхглавый змей стережёт Калинов мост над огненной Смородиной. Вблизи все три головы разом "
      "плюются огнём, издалека он мечет огненные шары.",
      "Огонь ему не страшен. Пока его не ранят, головы залечивают тело. Бейте без передышки и запаситесь "
      "зельем огнестойкости. С него падает меч-кладенец."],
     ["Zmey Gorynych",
      "The three-headed dragon guards the Kalinov bridge over the fiery Smorodina. Up close all three heads "
      "spit fire at once, from afar he hurls fireballs.",
      "Fire does not hurt him. While no one wounds him, his heads heal his body. Strike without a pause and "
      "bring potions of fire resistance. He drops the sword-kladenets."]),
    ("koschei", "boss", mob("koschei"),
     ["Кощей Бессмертный",
      "Костлявый царь-колдун в чёрном замке. Его удар иссушает, а раненый, он поднимает из земли упырей.",
      "Убить Кощея нельзя: он встаёт снова. Его смерть - на конце иглы, игла - в яйце, яйцо - в сундуке на "
      "старом дубе. Найдите Кощеев дуб.",
      "Разбейте яйцо (ПКМ) и носите иглу с собой. Тогда последний удар убьёт Кощея, а игла сломается. "
      "С него падает шапка-невидимка."],
     ["Koschei the Deathless",
      "The bony sorcerer-king in his black castle. His blow withers, and wounded, he raises upyri from the "
      "earth.",
      "Koschei cannot be killed: he gets up again. His death is at the tip of a needle, the needle in an egg, "
      "the egg in a chest on an old oak. Find Koschei's oak.",
      "Break the egg (right-click) and carry the needle. Then the last blow kills Koschei, and the needle "
      "breaks. He drops the cap of invisibility."]),

    ("slavic_village", "place", place("slavic_village"),
     ["Деревня",
      "Бревенчатые избы с печами и резными ставнями, колодец и огороды. Здесь живут купец и кузнец."],
     ["Village",
      "Log izbas with stoves and carved shutters, a well and vegetable gardens. A merchant and a smith live "
      "here."]),
    ("baba_yaga_hut", "place", place("baba_yaga_hut"),
     ["Избушка на курьих ножках",
      "Избушка стоит к лесу передом, к путнику задом, а вокруг частокол с черепами. Внутри Баба-яга, "
      "печь, котёл и сундук со снадобьями."],
     ["Hut on Chicken Legs",
      "The hut stands with its front to the forest and its back to the traveller, behind a fence of skulls. "
      "Inside are Baba Yaga, a stove, a cauldron and a chest of potions."]),
    ("kapishche", "place", place("kapishche"),
     ["Капище",
      "Круг деревянных идолов старых богов: Перун, Велес, Мокошь и Даждьбог смотрят на священный огонь. "
      "Здесь живут Жар-птицы."],
     ["Kapishche",
      "A ring of wooden idols of the old gods: Perun, Veles, Mokosh and Dazhbog look at the sacred fire. "
      "Firebirds live here."]),
    ("koschei_oak", "place", place("koschei_oak"),
     ["Кощеев дуб",
      "Старый чёрный дуб, который стерегут волколаки. Высоко в ветвях стоит сундук, а в нём яйцо с "
      "Кощеевой смертью."],
     ["Koschei's Oak",
      "An old black oak guarded by volkolaks. High in its branches stands a chest, and in it is the egg with "
      "Koschei's death."]),
    ("solovei_nest", "place", place("solovei_nest"),
     ["Гнездо Соловья",
      "Помост на девяти дубах, увитый ветвями. Лестница ведёт наверх, где сидит Соловей-разбойник "
      "с награбленным добром."],
     ["Solovei's Nest",
      "A deck on nine oaks, woven with branches. A ladder leads up to where Solovei the Robber sits on his "
      "loot."]),
    ("kalinov_bridge", "place", place("kalinov_bridge"),
     ["Калинов мост",
      "Каменный мост над огненной рекой Смородиной. На том берегу ждёт Змей Горыныч и его клад."],
     ["Kalinov Bridge",
      "A stone bridge over the fiery river Smorodina. On the far bank wait Zmey Gorynych and his hoard."]),
    ("koschei_castle", "place", place("koschei_castle"),
     ["Кощеев замок",
      "Чёрный замок с башнями и воротами в решётках. В тронном зале на костяном троне сидит Кощей, "
      "его стерегут упыри."],
     ["Koschei's Castle",
      "A black castle with towers and a barred gate. In the throne hall Koschei sits on a throne of bones, "
      "guarded by upyri."]),
]


def with_gear():
    """The entries with the gear pages of journal_gear.py after the introduction pages."""
    import journal_gear
    intro = [entry for entry in ENTRIES if entry[1] == "intro"]
    rest = [entry for entry in ENTRIES if entry[1] != "intro"]
    return intro + journal_gear.slavic() + rest
