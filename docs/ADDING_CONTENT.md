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
├── mythology/norse/NorseContent.java   всё скандинавское: блоки, предметы, измерение
└── gametest/                   автотесты (./gradlew runGameTestServer)

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
по образцу `NorsePortalTests`.
