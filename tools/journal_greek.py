"""Text of the Hero's Journal of Hellas. Each entry: (id, category, unlock, [ru pages], [en pages]).

unlock is ("entity", id), ("structure", id) or None (always shown). Both languages must have the same number of pages;
gen_greek_assets.py checks that each page fits in the book.
"""

NS = "mythsofworlds"


def mob(name):
    return ("entity", f"{NS}:{name}")


def place(name):
    return ("structure", f"{NS}:{name}")


INTRO = ("Журнал героя Эллады", "Hero's Journal of Hellas",
         "Здесь записано всё, что вы узнали о мире мифов. Встречайте существ, побеждайте чудовищ и находите места, "
         "и страницы заполнятся сами.",
         "Everything you learn about the world of the myths is written here. Meet creatures, defeat monsters and find "
         "places, and the pages fill themselves.")

ENTRIES = [
    ("portal", "intro", None,
     ["Священный водоём",
      "Выкопайте водоём от 1x1 до 8x8 и залейте стоячей водой. Обложите край олимпийским мрамором "
      "(8 мрамора вокруг золотого слитка), на 4 угла края поставьте жертвенные чаши.",
      "Зажгите все чаши факелом Прометея (кремень, золото, олимпийский мрамор и факел). Вода станет золотой: "
      "встаньте в неё на 3 секунды. Погасшая или сломанная чаша закрывает портал."],
     ["The Sacred Pool",
      "Dig a pool from 1x1 to 8x8 and fill it with still water. Rim it with Olympian marble (8 marble around a gold "
      "ingot) and put braziers on the 4 corners of the rim.",
      "Light every brazier with the Promethean Torch (flint, gold, Olympian marble and a torch). The water turns "
      "gold: stand in it for 3 seconds. A brazier put out or broken closes the portal."]),

    ("orichalcum", "intro", None,
     ["Орихалк и уголь Гефеста",
      "Глубоко в камне Эллады лежит орихалк, красное золото Атлантиды. Добывайте железной киркой. "
      "Снаряжение из орихалка прочнее железного и легко зачаровывается.",
      "Выше в горах встречается уголь Гефеста из подземных кузниц бога. В печи он горит вдвое дольше "
      "обычного угля."],
     ["Orichalcum and Hephaestus Coal",
      "Deep in the stone of Hellas lies orichalcum, the red gold of Atlantis. It needs an iron pickaxe; smelt "
      "the raw metal into ingots. Orichalcum gear is stronger than iron and takes enchantments well.",
      "Higher in the mountains you find Hephaestus coal from the god's forges under the earth. In a furnace it "
      "burns twice as long as ordinary coal."]),

    ("relics", "intro", None,
     ['Таларии и нагрудник титана', 'Крылатые сандалии Гермеса: скорость, высокий прыжок и никакого урона от падения. Ищите в святилищах на облаках и в храмах или скуйте: перья гарпий, золото и золотые сапоги.', 'Нагрудник титана: сила, стойкость и твёрдая стойка. Лежит в пещерах циклопов и в лабиринте, или скуйте из орихалкового нагрудника, орихалка, глаза циклопа и чешуи гидры.'],
     ["Talaria and the Titan's Breastplate", 'The winged sandals of Hermes: speed, high jumps and no fall damage. Look in the cloud shrines and temples, or make them: harpy feathers, gold and golden boots.', "The Titan's breastplate: strength, resistance and a firm stance. Found in cyclops caves and the labyrinth, or made from an orichalcum chestplate, orichalcum, a cyclops eye and a hydra scale."]),
    ("god_sets", "intro", None,
     ['Сеты богов', 'Броня из разных мифологий складывается в сет. Эллада: орихалк, сет Немейского льва, пояс Ипполиты, таларии, нагрудник титана. Йотунхейм: тёмное железо, шлем Хеймдалля.', 'Союз пантеонов (обе мифологии): 2 вещи дают спешку, 3 - ещё огнестойкость, 4 - ещё регенерацию. Две и две - ещё и стойкость.', 'Только Эллада, 4 вещи: скорость и прыжок. Только Йотунхейм, 4 вещи: сила и стойкость.'],
     ['Sets of the Gods', "Armour of different mythologies adds up to a set. Hellas: orichalcum, the Nemean lion set, the girdle of Hippolyta, the talaria, the Titan's breastplate. Jotunheim: dark iron, the helmet of Heimdall.", 'Union of the pantheons (both mythologies): 2 pieces give Haste, 3 also Fire Resistance, 4 also Regeneration. Two and two also give Resistance.', 'Hellas only, 4 pieces: Speed and Jump Boost. Jotunheim only, 4 pieces: Strength and Resistance.']),

    # ---------------------------------------------------------------- creatures
    ("satyr", "creature", mob("satyr"),
     ["Сатир",
      "Козлоногий спутник Диониса в Аркадии и на полях. Днём играет на свирели и никого не трогает, ночью нападает. "
      "Его свирель ускоряет других сатиров, удар вызывает тошноту.",
      "Как победить: бейте того, кто играет, первым, и не дайте стае окружить себя. Роняет кожу и пшеницу."],
     ["Satyr",
      "Goat-legged follower of Dionysus, in Arcadia and the fields. By day he plays his pipes and leaves you be, at "
      "night he attacks. His pipes speed up other satyrs; his blow makes you sick.",
      "How to beat: strike the piper first and do not let the herd surround you. Drops leather and wheat."]),
    ("harpy", "creature", mob("harpy"),
     ["Гарпия",
      "Женщина-птица с медными перьями, в горах Олимпа и на побережье. Нападает сверху и крадёт еду прямо из сумки, "
      "а потом улетает.",
      "Как победить: стреляйте из лука, пока она кружит. Убейте воровку, чтобы вернуть еду. Роняет перья гарпии: "
      "из них и сот делают крылья Дедала."],
     ["Harpy",
      "Bird-woman with bronze feathers, in the mountains of Olympus and on the coast. She swoops from above, steals "
      "food right out of your pack and flies off.",
      "How to beat: shoot her with a bow while she circles. Kill the thief to get your food back. Drops harpy "
      "feathers: with honeycomb they make the wings of Daedalus."]),
    ("spartoi", "creature", mob("spartoi"),
     ["Спарт",
      "Воин в бронзе, выросший из зубов дракона, посеянных Кадмом. Бродит по ночам по полям мёртвых и сторожит тупики "
      "лабиринта.",
      "Особенность: один раз встаёт снова после смерти. Добейте его ещё раз. Роняет кости и железные самородки."],
     ["Spartoi",
      "Bronze warrior grown from the dragon's teeth Cadmus sowed. Walks the fields of the dead at night and guards "
      "the dead ends of the labyrinth.",
      "Special: once, he rises again after death. Strike him down a second time. Drops bones and iron nuggets."]),
    ("shade", "creature", mob("shade"),
     ["Тень умершего",
      "Полупрозрачная душа из Асфоделевых лугов и Стигийских топей. Переносится к убегающей жертве и лечится каждым "
      "ударом.",
      "Как победить: не убегайте, а сражайтесь, и бейте часто. Иногда роняет эхо-осколок."],
     ["Shade",
      "See-through soul of the Asphodel Meadows and the Stygian Marsh. Blinks to a fleeing victim and heals with "
      "every blow it lands.",
      "How to beat: do not run, fight, and strike often. Sometimes drops an echo shard."]),
    ("golden_hind", "creature", mob("golden_hind"),
     ["Керинейская лань",
      "Священная лань Артемиды с золотыми рогами и медными копытами, в Рощах Аркадии. Геракл ловил её целый год.",
      "Амазонки держат ручных ланей в загоне лагеря и во дворе Фемискиры.",
      "Самый быстрый скакун Эллады. Приручается как лошадь."],
     ["Ceryneian Hind",
      "Sacred hind of Artemis with golden antlers and bronze hooves, in the Arcadian Grove. Heracles chased it for a "
      "whole year.",
      "The amazons keep tame hinds in the pen of their camps and in the courtyard of Themiscyra.",
      "The fastest mount in Hellas. Tame it like a horse."]),
    ("hydra_hatchling", "creature", mob("hydra_hatchling"),
     ["Гидрёныш",
      "Вылупляется из яйца, которое всегда роняет Лернейская гидра: ПКМ яйцом по земле. Ручной с рождения.",
      "Ходит за хозяином, садится по ПКМ, кусает с ядом и сам яда не боится. Лечится рыбой."],
     ["Hydra Hatchling",
      "Hatches from the egg the Lernaean Hydra always drops: right-click the ground with it. Tame from birth.",
      "Follows its owner, sits on right-click, bites with poison and is immune to it. Heals on fish."]),
    ("greek_merchant", "creature", mob("greek_merchant"),
     ["Торговец агоры",
      "Живёт на агоре. Скупщик трофеев платит изумруды за рога, клыки, шкуры и чешую чудовищ. Кузнец Гефеста меняет "
      "трофеи на оружие и броню.",
      "Жрица продаёт амброзию, факел Прометея, олимпийский мрамор и зелья."],
     ["Agora Merchant",
      "Lives in the agora. The trophy dealer pays emeralds for the horns, fangs, pelts and scales of monsters. The "
      "smith of Hephaestus trades trophies for weapons and armour.",
      "The priestess sells ambrosia, the Promethean Torch, Olympian marble and potions."]),
    ("lion", "creature", mob("lion"),
     ["Лев",
      "Прайд львов живёт в Немейском лесу. Львы охотятся на овец, коз и кроликов и не трогают людей.",
      "Осторожно: если ранить одного, на вас бросится весь прайд. Размножаются на сырой говядине. Роняют кожу и мясо."],
     ["Lion",
      "A pride of lions lives in the Nemean Forest. They hunt sheep, goats and rabbits and leave people alone.",
      "Careful: hurt one and the whole pride comes for you. They breed on raw beef. Drop leather and meat."]),
    ("amazon", "creature", mob("amazon"),
     ["Амазонка",
      "Воительница Фемискиры (40 здоровья, урон 8, броня 10), живёт в лагерях и в городе. Бьёт чудовищ, а если её задеть, отвечает вместе с сёстрами.",
      "Ухаживание: дарите цветы, золото, оружие, трофеи или еду, раз в 20 секунд. ПКМ пустой рукой: она скажет, что "
      "любит больше всего. Любимый подарок даёт вдвое больше симпатии.",
      "При симпатии 100 подарите обручальное кольцо (алмаз над тремя слитками золота). Жена идёт за вами и сражается "
      "рядом. Shift+ПКМ: идти за вами, ждать или гулять рядом.",
      "Торт жене: родится дочь, раз в день. Она вырастет за 20 минут в амазонку, верную вашей семье. Удар по амазонке "
      "сильно снижает симпатию.",
      "Больше всего на свете амазонки любят ожерелье Гармонии: подарите его, и она сразу влюбится (симпатия 100). "
      "Его не скрафтить, оно лежит в сокровищницах храмов, лабиринта и логов чудовищ.",
      "Амазонки держатся своего лагеря. Если они разбрелись, протрубите в горн Фемискиры (козий рог, золото и кожа): "
      "все вокруг вернутся домой.",
      "Не хотите ждать, пока дочь подрастёт? Бросьте в неё взрывное зелье роста (пузырёк, костная мука, золотая "
      "морковь и порох): она сразу станет взрослой. Зелье растит и любых других малышей.",
      "Семейный свисток (золото, железный самородок и жемчуг Края): ПКМ, и все ваши жёны и дочери сразу приходят "
      "к вам, даже из другого мира."],
     ["Amazon",
      "Warrior woman of Themiscyra (40 health, damage 8, armour 10), in the camps and the city. She fights monsters, and if you hurt her she answers "
      "together with her sisters.",
      "Courtship: give flowers, gold, weapons, trophies or food, once every 20 seconds. Right-click with an empty hand: "
      "she says what she likes best, and that gift counts double.",
      "At affection 100, give her a wedding ring (a diamond over three gold ingots). Your wife follows you and fights "
      "at your side. Shift + right-click: follow, stay or wander nearby.",
      "Give your wife a cake and a daughter is born, once a day. In 20 minutes she grows into an amazon loyal to your "
      "family. Hitting an amazon costs a lot of affection.",
      "Above all, amazons love the necklace of Harmonia: give it and she falls in love at once (affection 100). It "
      "cannot be crafted; it lies in the treasuries of temples, the labyrinth and the monsters' lairs.",
      "Amazons keep to their camp. If they have wandered off, blow the horn of Themiscyra (a goat horn, gold and "
      "leather): everyone around goes back home.",
      "Cannot wait for your daughter to grow up? Throw a splash potion of growth at her (a glass bottle, bone meal, "
      "a golden carrot and gunpowder): she is grown at once. The potion grows up any other young creature too.",
      "The family whistle (gold, an iron nugget and an ender pearl): right-click and all your wives and daughters "
      "come to you at once, even from another world."]),

    # ---------------------------------------------------------------- bosses
    ("cyclops", "boss", mob("cyclops"),
     ["Циклоп",
      "Одноглазый великан ростом с дом. Пасёт овец в пещере и не трогает путников, пока его не ударят.",
      "Способности: топает и подбрасывает всех вокруг, бьёт очень сильно. Как победить: держитесь на расстоянии, "
      "стреляйте и отбегайте, когда он поднимает ногу. Роняет глаз циклопа."],
     ["Cyclops",
      "One-eyed giant as tall as a house. Herds sheep in his cave and leaves travellers alone until struck.",
      "Abilities: stomps and throws everyone around into the air, hits very hard. How to beat: keep your distance, "
      "shoot, and step back when he lifts his foot. Drops the cyclops eye."]),
    ("medusa", "boss", mob("medusa"),
     ["Медуза Горгона",
      "Женщина со змеями вместо волос, в руинах храма на побережье. Её укус отравляет.",
      "Способности: её взгляд замедляет, а через 3 секунды начинает обращать в камень. Защита: щит в руке, тыква на "
      "голове или просто не смотрите на неё.",
      "Как победить: харпа Персея ранит её вдвое сильнее. Роняет голову Медузы: ПКМ ею обращает в камень всех перед "
      "вами."],
     ["Medusa",
      "A woman with snakes for hair, in a ruined temple on the coast. Her bite poisons.",
      "Abilities: her gaze slows you, and after 3 seconds it starts to turn you to stone. Protection: a shield in hand, "
      "a carved pumpkin on your head, or simply do not look at her.",
      "How to beat: the harpe of Perseus hurts her twice as much. Drops the head of Medusa: right-click it to turn "
      "everything in front of you to stone."]),
    ("nemean_lion", "boss", mob("nemean_lion"),
     ["Немейский лев",
      "Огромный золотой лев в логове посреди Немейского леса. Прыгает на добычу.",
      "Способности: шкура неуязвима для мечей, стрел и кулаков. Ранят его только зелья (яд, урон, иссушение, в том "
      "числе на стрелах) и кинжал из его когтя.",
      "Как победить: первого льва одолейте зельями. Из когтя (коготь над палкой) сделайте кинжал. Роняет шкуру и "
      "когти."],
     ["Nemean Lion",
      "Huge golden lion in a den at the heart of the Nemean Forest. Pounces on its prey.",
      "Abilities: its hide turns swords, arrows and fists. Only potions (poison, harming, wither, also on arrows) and a "
      "dagger made from its own claw hurt it.",
      "How to beat: bring down the first lion with potions. Make a dagger from its claw (a claw over a stick). Drops "
      "its pelt and claws."]),
    ("karkinos", "creature", mob("karkinos"),
     ["Каркин",
      "Рак, посланный Герой на помощь гидре: маленький, но злой. Сидит на берегу её логова. В мифе он ущипнул Геракла за "
      "пятку, и тот одолел гидру лишь с Иолаем.",
      "Способности: щипок держит жертву на месте, панцирь вдвое ослабляет стрелы. Как победить: Геракл раздавил его "
      "ногой. Удар в прыжке наносит двойной урон. Роняет клешню."],
     ["Karkinos",
      "The crab Hera sent to help the Hydra: small but vicious. Sits on the bank of its lair. In the myth it pinched Heracles by "
      "the heel, so he beat the Hydra only with Iolaus.",
      "Abilities: its pinch holds you in place, its shell halves arrows. How to beat: Heracles crushed it under his "
      "foot. A jump attack does double damage. Drops a claw."]),
    ("minotaur", "boss", mob("minotaur"),
     ["Минотавр",
      "Человек с головой быка, 300 здоровья. Заперт в арене в дальнем углу подземного лабиринта.",
      "Способности: таранит рогами. Ниже половины здоровья впадает в ярость: бегает быстрее и таранит вдвое чаще.",
      "Как победить: уворачивайтесь от тарана в сторону и бейте в спину. Возьмите нить, то есть оставляйте метки, "
      "чтобы найти выход. Роняет рог, золото и алмазы."],
     ["Minotaur",
      "Man with the head of a bull, 300 health. Shut in the arena in a far corner of the underground labyrinth.",
      "Abilities: charges with his horns. Below half health he rages: runs faster and charges twice as often.",
      "How to beat: sidestep the charge and strike his back. Take a thread, that is, leave marks, to find the way out. "
      "Drops his horn, gold and diamonds."]),
    ("hydra", "boss", mob("hydra"),
     ["Лернейская гидра",
      "Пятиглавый змей Стигийских топей, 400 здоровья. Головы плюются ядом, раны затягиваются сами.",
      "Слабость: огонь. Он останавливает регенерацию на 10 секунд и жжёт втрое сильнее. Меч с заговором огня режет её "
      "в 2,5 раза глубже на I уровне и в 4 раза на II.",
      "Как победить: заговор огня, огненные стрелы, лава. Берегитесь Каркина рядом. Роняет чешую, изумруды, алмазы и "
      "яйцо гидры."],
     ["Lernaean Hydra",
      "Five-headed serpent of the Stygian Marsh, 400 health. Its heads spit poison and its wounds close by themselves.",
      "Weakness: fire. It stops the regeneration for 10 seconds and burns three times as hard. A fire aspect blade "
      "cuts 2.5 times as deep at level I and 4 times at II.",
      "How to beat: fire aspect, flame arrows, lava. Beware of Karkinos nearby. Drops scales, emeralds, diamonds and "
      "a hydra egg."]),
    ("cerberus", "boss", mob("cerberus"),
     ["Цербер",
      "Трёхглавый пёс у Врат Аида на Асфоделевых лугах, 450 здоровья. Не боится огня.",
      "Способности: укус поджигает, дышит огнём. На половине здоровья призывает три тени.",
      "Как победить: зелье огнестойкости и хорошая броня. Сначала разберитесь с тенями. Роняет клыки, огненные "
      "стержни и алмазы.",
      "В крепостях и бастионах Незера лежит двузубец Аида, хозяина пса. Ударьте им Цербера или нажмите ПКМ, "
      "и пёс сразу падает. Двузубец срабатывает один раз."],
     ["Cerberus",
      "Three-headed hound at the Gates of Hades in the Asphodel Meadows, 450 health. Fire does not harm it.",
      "Abilities: its bite sets you on fire, it breathes fire. At half health it calls up three shades.",
      "How to beat: a fire resistance potion and good armour. Deal with the shades first. Drops fangs, blaze rods "
      "and diamonds.",
      "In the fortresses and bastions of the Nether lies the bident of Hades, his master. Strike Cerberus with it "
      "or use it on him, and the hound falls at once. The bident works only once."]),
    ("hippolyta", "boss", mob("hippolyta"),
     ["Ипполита",
      "Царица амазонок на троне Фемискиры, 220 здоровья. Нападает на любого чужака, сёстры приходят ей на помощь.",
      "Как победить: доведите её до шестой части здоровья, и она сдастся: перестанет биться и отдаст пояс "
      "(сила II, стойкость II, скорость и регенерация, носится вместо поножей).",
      "Свадьба: она слушает только победителя и принимает лишь царские дары: трофеи чудовищ, амброзию, зачарованные "
      "золотые яблоки, незерит, сердце моря и ожерелье Гармонии (сразу 100).",
      "Новый дар даёт 20 симпатии, повторный 10, прочее она отвергает. Бой прощён, когда она сдаётся. Женатого не "
      "примет. Ребёнок: амброзия, раз в три дня."],
     ["Hippolyta",
      "Queen of the Amazons on the throne of Themiscyra, 220 health. She attacks any stranger; her sisters come to help.",
      "How to beat: bring her down to a sixth of her health and she yields: she stops fighting and hands over her "
      "girdle (Strength II, Resistance II, Speed and Regeneration, worn in the legs slot).",
      "Marriage: she listens only to her victor and accepts only gifts fit for a queen: monster trophies, ambrosia, "
      "enchanted golden apples, netherite, the heart of the sea and the necklace of Harmonia (100 at once).",
      "A new gift gives 20 affection, a repeat 10; anything else she scorns. The duel is forgiven once she yields. "
      "She turns away a married man. A child: ambrosia, once in three days."]),

    # ---------------------------------------------------------------- places
    ("greek_temple", "place", place("greek_temple"),
     ["Храм Олимпийцев",
      "Мраморный храм с колоннадой и золотым фризом на Олимпе и Елисейских полях, как Парфенон. Внутри сундуки с "
      "золотом, амброзией и иногда факелом Прометея."],
     ["Temple of the Olympians",
      "A marble temple with a colonnade and a golden frieze, on Olympus and the Elysian Fields, like the Parthenon. "
      "Inside are chests with gold, ambrosia and sometimes a Promethean Torch."]),
    ("oracle_of_delphi", "place", place("oracle_of_delphi"),
     ["Дельфийский оракул",
      "Круглое святилище Аполлона в Аркадии и горах. В сундуках пифии: склянки, светокамень, аметист, книги чар и "
      "бутыльки опыта."],
     ["Oracle of Delphi",
      "Round sanctuary of Apollo in Arcadia and the mountains. In the Pythia's chests: bottles, glowstone, amethyst, "
      "enchanted books and bottles of experience."]),
    ("labyrinth", "place", place("labyrinth"),
     ["Лабиринт Минотавра",
      "На поверхности видно только вход: портик с красными колоннами и чёрными капителями, а на крыше рога. Под ним "
      "винтовая лестница уходит на 20 блоков вниз.",
      "Внизу лабиринт 61x61 из кирпичей, которые ничем не сломать. Вход в центре, арена Минотавра в дальнем углу. "
      "В тупиках спарты и тайники с сокровищами."],
     ["Labyrinth of the Minotaur",
      "On the surface you see only the entrance: a porch with red columns, black capitals and horns on the roof. "
      "Under it a spiral stair goes 20 blocks down.",
      "Below is a 61x61 maze of bricks nothing can break. The entrance is in the middle, the Minotaur's arena in a far "
      "corner. Spartoi and hidden treasure wait in the dead ends."]),
    ("gates_of_hades", "place", place("gates_of_hades"),
     ["Врата Аида",
      "Чёрные колонны из базальта и запечатанная дверь из обсидиана среди Асфоделевых лугов. Горит синий огонь душ. "
      "Сторож - Цербер, в сундуке обсидиан, алмазы и незеритовый лом."],
     ["Gates of Hades",
      "Black basalt pillars and a sealed obsidian door in the Asphodel Meadows, lit by blue soul fire. Guarded by "
      "Cerberus; the chest holds obsidian, diamonds and netherite scrap."]),
    ("hydra_lair", "place", place("hydra_lair"),
     ["Логово гидры",
      "Круглое болото с чёрной водой и кувшинками в Стигийских топях, обнесённое разбитой стеной и упавшими колоннами. "
      "В середине сундук, в воде гидра, на берегу Каркин."],
     ["Lair of the Hydra",
      "A round pool of black water with lily pads in the Stygian Marsh, ringed by a broken wall and fallen columns. "
      "A chest in the middle, the Hydra in the water, Karkinos on the bank."]),
    ("medusa_lair", "place", place("medusa_lair"),
     ["Логово Медузы",
      "Разрушенный храм на побережье. Среди колонн стоят окаменевшие герои: каменные статуи тех, кто посмотрел ей в "
      "глаза. Возьмите щит или тыкву."],
     ["Lair of Medusa",
      "A ruined temple on the coast. Among the columns stand heroes turned to stone: statues of those who met her eyes. "
      "Bring a shield or a pumpkin."]),
    ("cyclops_cave", "place", place("cyclops_cave"),
     ["Пещера циклопа",
      "Каменный купол в горах и на побережье. Внутри загон с овцами Полифема, постель из сена, очаг и сундук с "
      "шерстью, мясом и железом."],
     ["Cyclops Cave",
      "A stone dome in the mountains and on the coast. Inside: Polyphemus' sheep pen, a bed of hay, a hearth and a "
      "chest of wool, meat and iron."]),
    ("nemean_lion_den", "place", place("nemean_lion_den"),
     ["Логово Немейского льва",
      "Пещера из гранита и мха в глубине Немейского леса, усыпанная костями. Вокруг бродит прайд обычных львов."],
     ["Den of the Nemean Lion",
      "A cave of granite and moss deep in the Nemean Forest, strewn with bones. A pride of ordinary lions roams around."]),
    ("agora", "place", place("agora"),
     ["Агора",
      "Рынок Эллады: фонтан с железным стражем, четыре лавки торговцев, белые дома с сундуками, храм Гермеса и оливы. "
      "Здесь продают трофеи чудовищ."],
     ["Agora",
      "The market of Hellas: a fountain with an iron guardian, four merchants' stalls, white houses with chests, a "
      "temple of Hermes and olive trees. Sell monster trophies here."]),
    ("ship_of_theseus", "place", place("ship_of_theseus"),
     ["Корабль Тесея",
      "Длинный корабль с чёрным парусом в Эгейском море: тот, что вёз Тесея с Крита. На палубе команда теней, в трюме "
      "сундук с картой, компасом и иногда трезубцем."],
     ["Ship of Theseus",
      "A long ship with a black sail in the Aegean Sea, the one that carried Theseus home from Crete. A crew of shades "
      "on deck; in the hold a chest with a map, a compass and sometimes a trident."]),
    ("perseus_refuge", "place", place("perseus_refuge"),
     ["Убежище Персея",
      "Маленький лагерь героя на побережье и в горах. Здесь всегда лежат харпа и зеркальный щит."],
     ["Refuge of Perseus",
      "The hero's small camp on the coast and in the mountains. The harpe and the mirror shield always lie here."]),
    ("amazon_camp", "place", place("amazon_camp"),
     ["Лагерь амазонок",
      "Частокол на равнине: шатры, костёр, мишени и загон с лошадьми. Здесь живут амазонки. В сундуке бывает "
      "обручальное кольцо."],
     ["Amazon Camp",
      "A palisade on the plain with tents, a fire, targets and a horse pen. Amazons live here. The chest sometimes "
      "holds a wedding ring."]),
    ("themiscyra", "place", place("themiscyra"),
     ["Фемискира",
      "Город амазонок за мраморными стенами с башнями. Во дворе статуя Ареса и оливы, на севере тронный зал с "
      "жаровнями, где сидит Ипполита. В сокровищнице золото и кольца."],
     ["Themiscyra",
      "City of the Amazons behind marble walls with towers. A statue of Ares and olive trees in the courtyard, and in "
      "the north the throne hall with braziers, where Hippolyta sits. Gold and rings in the treasury."]),
    ("greek_farmstead", "place", place("greek_farmstead"),
     ["Усадьба",
      "Белый дом с плоской крышей и синими ставнями, как на островах. Виноградный навес, олива, улей, амфоры, колодец "
      "и загон с козой. В сундуке оливки, мёд и хлеб."],
     ["Farmstead",
      "A white house with a flat roof and blue shutters, as on the islands. A vine pergola, an olive tree, a beehive, "
      "amphorae, a well and a goat pen. Olives, honey and bread in the chest."]),
]


def with_gear():
    """The entries with the ore and gear pages of journal_gear.py after the introduction pages."""
    import journal_gear
    intro = [entry for entry in ENTRIES if entry[1] == "intro"]
    rest = [entry for entry in ENTRIES if entry[1] != "intro"]
    return intro + journal_gear.greek() + rest
