# Как дорабатывать мод

Код разбит так, чтобы новое содержимое добавлялось копированием готового примера.

```
src/main/java/com/mythsofworlds/
├── MythsOfWorlds.java          точка входа: по одной строке init() на мифологию
├── registry/ModRegistries.java общие реестры блоков, предметов и творческой вкладки
├── core/portal/                общий движок порталов (трогать не нужно)
│   ├── PortalSettings.java     чем один портал отличается от другого
│   ├── MythPortalBlock.java    блок портала: телепорт, разрушение без рамки
│   ├── PortalShape.java        поиск замкнутой рамки любой формы
│   ├── PortalPlacement.java    поиск или постройка портала на другой стороне
│   └── PortalIgniterItem.java  «зажигалка» для порталов
├── mythology/Mythology.java    список шести мифологий и их измерений
├── mythology/greek/            всё греческое (полный пример)
│   ├── GreekContent.java       блоки, предметы, Факел Прометея, списки биомов и структур
│   ├── GreekEntities.java      мобы: типы, характеристики, яйца призыва, правила спавна
│   ├── GreekTrades.java        сделки торговцев агоры (скупщик, кузнец, жрица)
│   ├── GreekSounds.java        звуки; что в них звучит — assets/mythsofworlds/sounds.json
│   ├── portal/                 священный водоём: чаша, блок портала, проверка водоёма, факел
│   ├── entity/                 поведение мобов; GreekBoss — общая основа боссов (шкала здоровья, без деспавна,
│   │                           hostile() для нейтральных, enraged() ниже половины здоровья)
│   ├── client/                 модели и рендеры мобов (только клиент)
│   └── item/                   голова Медузы, яйцо гидры
├── mythology/norse/NorseContent.java   всё скандинавское: блоки, предметы, измерение
├── mythology/slavic|oceanic|egyptian|indian/   заготовки: только ключ измерения
└── gametest/                   автотесты (./gradlew runGameTestServer) и WorldSmokeTest (./gradlew runSmokeTest)

tools/gen_greek_assets.py       генератор греческих JSON, шаблонов структур (.nbt, сами постройки в tools/structures.py)
                                и текстур (--textures, рисунки в tools/textures.py)
tools/gen_greek_sounds.py       sounds.json, субтитры и синтез своих звуков в .ogg (--ogg, нужны numpy и ffmpeg)

src/main/resources/
├── assets/mythsofworlds/       то, что видит игрок: текстуры, модели, переводы
│   ├── blockstates/  models/block/  models/item/  textures/block/  textures/item/
│   └── lang/ru_ru.json, lang/en_us.json
└── data/mythsofworlds/         логика мира: рецепты, лут, измерения, биомы
    ├── recipe/  loot_table/blocks/
    ├── dimension/  dimension_type/  worldgen/biome/
    └── structure/empty.nbt     пустая площадка для автотестов
```

Все имена (id) пишутся маленькими латинскими буквами через `_`, например `olympus_marble`.

## Новый простой блок

1. В классе мифологии (например `NorseContent`) добавьте блок и его предмет:
   ```java
   public static final DeferredBlock<Block> CARVED_RUNESTONE = BLOCKS.registerSimpleBlock("carved_runestone",
           BlockBehaviour.Properties.of().mapColor(MapColor.DEEPSLATE).strength(3.0F).requiresCorrectToolForDrops());
   public static final DeferredItem<BlockItem> CARVED_RUNESTONE_ITEM = ITEMS.registerSimpleBlockItem(CARVED_RUNESTONE);
   ```
2. Скопируйте и переименуйте файлы `runestone` в ресурсах:
   - `assets/mythsofworlds/blockstates/carved_runestone.json`
   - `assets/mythsofworlds/models/block/carved_runestone.json` (внутри поменяйте путь к текстуре)
   - `assets/mythsofworlds/models/item/carved_runestone.json`
   - `assets/mythsofworlds/textures/block/carved_runestone.png` (16×16)
   - `data/mythsofworlds/loot_table/blocks/carved_runestone.json` (иначе блок ничего не роняет)
3. Добавьте название в `lang/ru_ru.json` и `lang/en_us.json`: `"block.mythsofworlds.carved_runestone": "Резной рунный камень"`.
4. Чтобы блок копался киркой, допишите id в `data/minecraft/tags/block/mineable/pickaxe.json`.
5. Рецепт по желанию: скопируйте `data/mythsofworlds/recipe/runestone.json`.

Во вкладку творческого режима предмет попадёт сам.

## Новый предмет

```java
public static final DeferredItem<Item> RAVEN_FEATHER = ITEMS.registerSimpleItem("raven_feather");
```
Затем `models/item/raven_feather.json` (скопируйте `rune_igniter.json`), текстура `textures/item/raven_feather.png`
и строка `"item.mythsofworlds.raven_feather"` в переводах. Если предмет должен что-то делать, создайте свой класс,
унаследованный от `Item`, по образцу `PortalIgniterItem`.

## Новая мифология с порталом (например, греческая)

1. Скопируйте `mythology/norse/NorseContent.java` в `mythology/greek/GreekContent.java`.
2. Поменяйте ключ измерения, блок рамки, блок портала и зажигалку:
   ```java
   public static final ResourceKey<Level> OLYMPUS = ResourceKey.create(Registries.DIMENSION, MythsOfWorlds.id("olympus"));
   public static final DeferredBlock<Block> MARBLE = BLOCKS.registerSimpleBlock("olympus_marble", ...);
   public static final DeferredBlock<MythPortalBlock> OLYMPUS_PORTAL = BLOCKS.register("olympus_portal",
           () -> new MythPortalBlock(PortalSettings.toDimension(MARBLE, OLYMPUS, ParticleTypes.CLOUD), ...));
   ```
   Одна зажигалка может открывать несколько порталов: `List.of(BIFROST_PORTAL, OLYMPUS_PORTAL)`.
3. В `MythsOfWorlds.java` допишите `GreekContent.init();`.
4. Ресурсы портала: скопируйте `blockstates/bifrost_portal.json`, оба `models/block/bifrost_portal_*.json`
   и анимированную текстуру `textures/block/bifrost_portal.png` вместе с `.png.mcmeta`.
5. Измерение: скопируйте `data/mythsofworlds/dimension/jotunheim.json` и `dimension_type/jotunheim.json`
   под новым именем. В `dimension/olympus.json` поле `type` должно указывать на новый `dimension_type`.
6. Биомы: скопируйте файлы из `worldgen/biome/` и поменяйте цвета неба, тумана, воды, мобов и украшения.
   Если используете ванильные биомы (`minecraft:desert` и т.п.), свои файлы не нужны.

## Греческие данные генерируются скриптом

Биомы Эллады, структуры, лут, модели, переводы и измерения-заготовки описаны таблицами в
`tools/gen_greek_assets.py` (постройки — в `tools/structures.py`). Поменяйте таблицу и запустите:

```bash
python3 tools/gen_greek_assets.py             # JSON и .nbt
python3 tools/gen_greek_assets.py --textures  # плюс перерисовать временные текстуры (затрёт PNG)
```

Скрипт сам следит за порядком украшений в биомах. Готовые файлы можно править и руками, но следующий запуск
скрипта их перезапишет. Структуру удобно доработать в игре блоком структуры (`/give @s structure_block`),
сохранить и положить .nbt в `data/mythsofworlds/structure/greek/`.

## Новый моб

1. Класс в `mythology/greek/entity/` (обычный монстр — по образцу `Satyr`, босс — наследник `GreekBoss`, как `Minotaur`).
2. В `GreekEntities`: тип (`register(...)`), яйцо (`egg(...)`), строка в `registerAttributes`, при естественном спавне — в `registerSpawnPlacements`.
3. В `client/GreekClient`: рендер. Человекоподобным подходит `GreekHumanoidRenderer` со слоем `HUMANOID`, зверям — `BeastModel`.
4. Текстура `textures/entity/<имя>.png`, лут `loot_table/entities/<имя>.json`, перевод `entity.mythsofworlds.<имя>`,
   модель яйца `models/item/<имя>_spawn_egg.json`. Где спавнится — в `spawners` нужных биомов.

## Новая сделка у торговцев агоры

В `GreekTrades.java` добавьте строку в нужный список: `sell(предмет, сколько, изумрудов)` — торговец покупает,
`buy(изумрудов, () -> new ItemStack(...), сколько раз)` — продаёт, `swap(трофей, изумрудов, () -> результат)` — обмен.
Сделки создаются заново для каждого нового торговца; у уже живущих в мире торговцев остаются старые.

## Новый звук

1. В `GreekSounds.java`: `sound("entity.<моб>.<что>")`.
2. В `tools/gen_greek_sounds.py` добавьте строку в `SOUNDS`: ванильный звук через `event(...)` с нужной высотой
   или свой файл через `own(...)` (свой .ogg положите в `assets/mythsofworlds/sounds/` или синтезируйте в `SYNTHS`).
3. `python3 tools/gen_greek_sounds.py` (с `--ogg`, чтобы пересоздать файлы).

## Как развить заготовку мифологии

Например, славянскую: в `SlavicContent` добавьте блок рамки, `MythPortalBlock` и зажигалку по образцу `NorseContent`
(или портал своей формы, как священный водоём в `mythology/greek/portal`),
поставьте `true` у `SLAVIC` в `Mythology.java`, замените ванильные биомы в `dimension/nav.json` своими.

## Измерения: что можно менять без кода

- `dimension_type/*.json`: `fixed_time` (12500 = вечные сумерки, 6000 = вечный полдень, убрать = смена дня и ночи),
  `has_ceiling` (потолок как в Незере), `ultrawarm` (вода испаряется), `bed_works`.
- `dimension/*.json` → `generator.settings`: рельеф. `minecraft:amplified` (горы), `minecraft:overworld`,
  `minecraft:nether`, `minecraft:floating_islands`, `minecraft:caves`.
- `worldgen/biome/*.json`: цвета, частицы в воздухе, кто спавнится (`spawners`), что растёт (`features`).
  В `features` 11 списков по шагам генерации; порядок одних и тех же украшений в разных биомах одного измерения
  должен совпадать, иначе мир не загрузится.

## Проверка

```bash
./gradlew build              # собрать jar (build/libs)
./gradlew runClient          # запустить игру с модом
./gradlew runGameTestServer  # автотесты; падают с ошибкой, если что-то сломано
```

GitHub Actions выполняет сборку и тесты на каждый push, а после push в `main` выкладывает jar в Releases.
Чтобы выпустить новую версию, увеличьте `mod_version` в `gradle.properties`. Сборки других веток лежат в артефакте `mythsofworlds-jar`
на странице запуска (вкладка Actions).

Новый автотест: добавьте метод с `@GameTest(template = "empty")` в класс из пакета `gametest`
по образцу `NorsePortalTests` или `GreekTests`. Автотесты не создают модовые измерения, поэтому в CI ещё запускается
`./gradlew runSmokeTest`: настоящий сервер генерирует все измерения, находит каждый биом и структуру Эллады и выходит
с ошибкой, если что-то не так (перед первым запуском создайте `run/smoke/eula.txt` с текстом `eula=true`).
