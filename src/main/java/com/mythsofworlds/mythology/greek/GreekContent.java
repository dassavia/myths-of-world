package com.mythsofworlds.mythology.greek;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.item.HydraEggItem;
import com.mythsofworlds.mythology.greek.item.MedusaHeadItem;
import com.mythsofworlds.journal.JournalItem;
import com.mythsofworlds.mythology.greek.block.CloudBlock;
import com.mythsofworlds.mythology.greek.block.FruitLeavesBlock;
import com.mythsofworlds.mythology.greek.item.GirdleItem;
import com.mythsofworlds.mythology.greek.item.WingsItem;
import com.mythsofworlds.mythology.greek.portal.BrazierBlock;
import com.mythsofworlds.mythology.greek.portal.PoolPortalBlock;
import com.mythsofworlds.mythology.greek.portal.PrometheanTorchItem;
import java.util.List;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.food.FoodProperties;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.FlowerBlock;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;

import static com.mythsofworlds.registry.ModRegistries.BLOCKS;
import static com.mythsofworlds.registry.ModRegistries.ITEMS;

/**
 * Greek mythology: marble, the Promethean Torch and the sacred pool portal to Hellas, plus the trophies dropped by its monsters.
 * Mobs live in {@link GreekEntities}; biomes, structures and loot are data files under data/mythsofworlds.
 */
public final class GreekContent {
    /** Defined in data/mythsofworlds/dimension/hellas.json. */
    public static final ResourceKey<Level> HELLAS =
            ResourceKey.create(Registries.DIMENSION, MythsOfWorlds.id("hellas"));
    /** Biomes of Hellas (data/mythsofworlds/worldgen/biome). */
    public static final List<String> BIOMES = List.of("olympus_peaks", "elysian_fields", "arcadian_grove",
            "asphodel_meadows", "stygian_marsh", "aegean_coast", "aegean_sea", "nemean_forest");
    /** Structures of Hellas (data/mythsofworlds/worldgen/structure, templates in data/mythsofworlds/structure/greek). */
    public static final List<String> STRUCTURES = List.of("greek_temple", "oracle_of_delphi", "labyrinth",
            "gates_of_hades", "hydra_lair", "medusa_lair", "cyclops_cave", "nemean_lion_den",
            "agora", "ship_of_theseus", "perseus_refuge", "amazon_camp", "themiscyra", "greek_farmstead");

    // ---- Blocks ----

    private static BlockBehaviour.Properties marble() {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.QUARTZ)
                .strength(1.8F, 6.0F)
                .requiresCorrectToolForDrops()
                .sound(SoundType.CALCITE);
    }

    /** Generates in the mountains of Hellas; craft it from diorite and calcite in the Overworld. */
    public static final DeferredBlock<Block> MARBLE = BLOCKS.registerSimpleBlock("marble", marble());
    public static final DeferredBlock<Block> MARBLE_BRICKS = BLOCKS.registerSimpleBlock("marble_bricks", marble());
    public static final DeferredBlock<RotatedPillarBlock> MARBLE_PILLAR =
            BLOCKS.registerBlock("marble_pillar", RotatedPillarBlock::new, marble());

    /** Frame block for the Hellas portal: marble inlaid with gold. */
    public static final DeferredBlock<Block> OLYMPIAN_MARBLE = BLOCKS.registerSimpleBlock("olympian_marble",
            marble().mapColor(MapColor.GOLD).strength(3.0F, 9.0F).lightLevel(state -> 4));

    /** Bowl of sacred fire for the corners of the portal pool (see portal/PoolPortal). */
    public static final DeferredBlock<BrazierBlock> BRAZIER = BLOCKS.register("brazier",
            () -> new BrazierBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_ORANGE)
                    .strength(2.0F, 6.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.COPPER)
                    .noOcclusion()
                    .lightLevel(state -> state.getValue(BrazierBlock.LIT) ? 15 : 0)));

    /** Golden surface of a lit sacred pool. */
    public static final DeferredBlock<PoolPortalBlock> HELLAS_PORTAL = BLOCKS.register("hellas_portal",
            () -> new PoolPortalBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.GOLD)
                    .noCollission()
                    .strength(-1.0F)
                    .sound(SoundType.GLASS)
                    .lightLevel(state -> 12)
                    .noLootTable()
                    .pushReaction(PushReaction.BLOCK)));

    /** Pale flower of the Asphodel Meadows, where the shades of the dead wander. */
    public static final DeferredBlock<FlowerBlock> ASPHODEL = BLOCKS.register("asphodel",
            () -> new FlowerBlock(MobEffects.WEAKNESS, 7.0F, BlockBehaviour.Properties.of()
                    .mapColor(MapColor.TERRACOTTA_WHITE)
                    .noCollission()
                    .instabreak()
                    .sound(SoundType.GRASS)
                    .offsetType(BlockBehaviour.OffsetType.XZ)
                    .pushReaction(PushReaction.DESTROY)));

    /** Soft white cloud of the islands that float above Olympus and Elysium. Breaks any fall. */
    public static final DeferredBlock<CloudBlock> CLOUD = BLOCKS.register("cloud",
            () -> new CloudBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.SNOW)
                    .strength(0.3F)
                    .sound(SoundType.WOOL)
                    .noOcclusion()
                    .speedFactor(0.8F)
                    .isViewBlocking((state, level, pos) -> false)
                    .isSuffocating((state, level, pos) -> false)));

    /** Leaves of the golden apple trees of the Hesperides, in the Elysian Fields. Sometimes drop a golden apple. */
    public static final DeferredBlock<LeavesBlock> GOLDEN_LEAVES = BLOCKS.register("golden_leaves",
            () -> new LeavesBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.GOLD)
                    .strength(0.2F)
                    .randomTicks()
                    .sound(SoundType.AZALEA_LEAVES)
                    .noOcclusion()
                    .lightLevel(state -> 6)
                    .isValidSpawn((state, level, pos, type) -> false)
                    .isSuffocating((state, level, pos) -> false)
                    .isViewBlocking((state, level, pos) -> false)
                    .ignitedByLava()
                    .pushReaction(PushReaction.DESTROY)));

    /** Walls of the labyrinth of Daedalus: no tool or explosion can break them, so the maze must be walked. */
    private static BlockBehaviour.Properties labyrinth() {
        return BlockBehaviour.Properties.of()
                .mapColor(MapColor.STONE)
                .strength(-1.0F, 3600000.0F)
                .noLootTable()
                .sound(SoundType.DEEPSLATE_BRICKS)
                .pushReaction(PushReaction.BLOCK)
                .isValidSpawn((state, level, pos, type) -> false);
    }

    public static final DeferredBlock<Block> LABYRINTH_BRICKS = BLOCKS.registerSimpleBlock("labyrinth_bricks", labyrinth());
    public static final DeferredBlock<Block> MOSSY_LABYRINTH_BRICKS = BLOCKS.registerSimpleBlock("mossy_labyrinth_bricks", labyrinth());
    public static final DeferredBlock<Block> CRACKED_LABYRINTH_BRICKS = BLOCKS.registerSimpleBlock("cracked_labyrinth_bricks", labyrinth());

    private static BlockBehaviour.Properties fruitLeaves(MapColor color) {
        return BlockBehaviour.Properties.of()
                .mapColor(color)
                .strength(0.2F)
                .randomTicks()
                .sound(SoundType.GRASS)
                .noOcclusion()
                .isValidSpawn((state, level, pos, type) -> false)
                .isSuffocating((state, level, pos) -> false)
                .isViewBlocking((state, level, pos) -> false)
                .ignitedByLava()
                .pushReaction(PushReaction.DESTROY);
    }

    /** Silvery leaves of the olive trees of Athena; olives ripen on them. */
    public static final DeferredBlock<FruitLeavesBlock> OLIVE_LEAVES = BLOCKS.register("olive_leaves",
            () -> new FruitLeavesBlock(GreekContent.OLIVES, fruitLeaves(MapColor.COLOR_LIGHT_GREEN)));
    /** Dark leaves of the pomegranate trees of Persephone, in the Asphodel Meadows and Elysium. */
    public static final DeferredBlock<FruitLeavesBlock> POMEGRANATE_LEAVES = BLOCKS.register("pomegranate_leaves",
            () -> new FruitLeavesBlock(GreekContent.POMEGRANATE, fruitLeaves(MapColor.COLOR_GREEN)));

    // ---- Items ----

    public static final DeferredItem<BlockItem> MARBLE_ITEM = ITEMS.registerSimpleBlockItem(MARBLE);
    public static final DeferredItem<BlockItem> MARBLE_BRICKS_ITEM = ITEMS.registerSimpleBlockItem(MARBLE_BRICKS);
    public static final DeferredItem<BlockItem> MARBLE_PILLAR_ITEM = ITEMS.registerSimpleBlockItem(MARBLE_PILLAR);
    public static final DeferredItem<BlockItem> OLYMPIAN_MARBLE_ITEM = ITEMS.registerSimpleBlockItem(OLYMPIAN_MARBLE);
    public static final DeferredItem<BlockItem> ASPHODEL_ITEM = ITEMS.registerSimpleBlockItem(ASPHODEL);
    public static final DeferredItem<BlockItem> BRAZIER_ITEM = ITEMS.registerSimpleBlockItem(BRAZIER);
    public static final DeferredItem<BlockItem> CLOUD_ITEM = ITEMS.registerSimpleBlockItem(CLOUD);
    public static final DeferredItem<BlockItem> GOLDEN_LEAVES_ITEM = ITEMS.registerSimpleBlockItem(GOLDEN_LEAVES);
    public static final DeferredItem<BlockItem> OLIVE_LEAVES_ITEM = ITEMS.registerSimpleBlockItem(OLIVE_LEAVES);
    public static final DeferredItem<BlockItem> POMEGRANATE_LEAVES_ITEM = ITEMS.registerSimpleBlockItem(POMEGRANATE_LEAVES);
    public static final DeferredItem<BlockItem> LABYRINTH_BRICKS_ITEM = ITEMS.registerSimpleBlockItem(LABYRINTH_BRICKS);
    public static final DeferredItem<BlockItem> MOSSY_LABYRINTH_BRICKS_ITEM = ITEMS.registerSimpleBlockItem(MOSSY_LABYRINTH_BRICKS);
    public static final DeferredItem<BlockItem> CRACKED_LABYRINTH_BRICKS_ITEM = ITEMS.registerSimpleBlockItem(CRACKED_LABYRINTH_BRICKS);

    /** Picked from olive leaves. */
    public static final DeferredItem<Item> OLIVES = ITEMS.registerItem("olives", props -> new Item(props
            .food(new FoodProperties.Builder().nutrition(2).saturationModifier(0.6F).fast().build())));
    /** Fruit of the underworld: whoever eats it sees in the dark for a while. */
    public static final DeferredItem<Item> POMEGRANATE = ITEMS.registerItem("pomegranate", props -> new Item(props
            .food(new FoodProperties.Builder().nutrition(5).saturationModifier(0.7F)
                    .effect(new MobEffectInstance(MobEffects.NIGHT_VISION, 900, 0), 1.0F).build())));

    /** Hero's journal: records every creature and place of Hellas the player has found. */
    public static final DeferredItem<JournalItem> GREEK_JOURNAL = ITEMS.register("greek_journal",
            () -> new JournalItem("greek", false, new Item.Properties().stacksTo(1)));
    /** Creative-only copy of the journal with every entry already written. */
    public static final DeferredItem<JournalItem> GREEK_JOURNAL_COMPLETE = ITEMS.register("greek_journal_complete",
            () -> new JournalItem("greek", true, new Item.Properties().stacksTo(1).rarity(Rarity.EPIC)));

    /** The fire Prometheus stole from the gods: lights the braziers of the portal pool. */
    public static final DeferredItem<PrometheanTorchItem> PROMETHEAN_TORCH = ITEMS.register("promethean_torch",
            () -> new PrometheanTorchItem(new Item.Properties().durability(32).rarity(Rarity.EPIC)));

    /** Food of the gods, found in temples. */
    public static final DeferredItem<Item> AMBROSIA = ITEMS.registerItem("ambrosia", props -> new Item(props
            .rarity(Rarity.RARE)
            .food(new FoodProperties.Builder()
                    .nutrition(6)
                    .saturationModifier(1.2F)
                    .alwaysEdible()
                    .effect(new MobEffectInstance(MobEffects.REGENERATION, 200, 1), 1.0F)
                    .effect(new MobEffectInstance(MobEffects.ABSORPTION, 1200, 1), 1.0F)
                    .build())));

    // Trophies dropped by the monsters of Hellas.
    public static final DeferredItem<Item> HARPY_FEATHER = ITEMS.registerSimpleItem("harpy_feather");
    public static final DeferredItem<Item> MINOTAUR_HORN = ITEMS.registerSimpleItem("minotaur_horn",
            new Item.Properties().rarity(Rarity.RARE));
    public static final DeferredItem<Item> HYDRA_SCALE = ITEMS.registerSimpleItem("hydra_scale",
            new Item.Properties().rarity(Rarity.RARE));
    public static final DeferredItem<Item> CERBERUS_FANG = ITEMS.registerSimpleItem("cerberus_fang",
            new Item.Properties().rarity(Rarity.RARE));
    public static final DeferredItem<Item> NEMEAN_PELT = ITEMS.registerSimpleItem("nemean_pelt",
            new Item.Properties().rarity(Rarity.UNCOMMON));
    public static final DeferredItem<Item> CYCLOPS_EYE = ITEMS.registerSimpleItem("cyclops_eye",
            new Item.Properties().rarity(Rarity.UNCOMMON));
    /** Claw of the Nemean Lion: the only blade that can cut its hide. */
    public static final DeferredItem<Item> NEMEAN_CLAW = ITEMS.registerSimpleItem("nemean_claw",
            new Item.Properties().rarity(Rarity.RARE));
    /** Dagger made from the lion's claw. Hurts the Nemean Lion like any other creature. */
    public static final DeferredItem<SwordItem> NEMEAN_CLAW_DAGGER = ITEMS.register("nemean_claw_dagger",
            () -> new SwordItem(Tiers.DIAMOND, new Item.Properties().rarity(Rarity.RARE)
                    .attributes(SwordItem.createAttributes(Tiers.DIAMOND, 2, -1.8F))));
    /** Sickle-sword of Perseus, found in his refuge. Deals double damage to Medusa. */
    public static final DeferredItem<SwordItem> HARPE = ITEMS.register("harpe",
            () -> new SwordItem(Tiers.IRON, new Item.Properties().rarity(Rarity.RARE)
                    .attributes(SwordItem.createAttributes(Tiers.IRON, 4, -2.4F))));
    /** Dropped by the Hydra. Use it on the ground to hatch a tame little hydra. */
    public static final DeferredItem<HydraEggItem> HYDRA_EGG = ITEMS.register("hydra_egg",
            () -> new HydraEggItem(new Item.Properties().stacksTo(1).rarity(Rarity.EPIC)));
    /** Harpy feathers and wax: a very high jump and a gentle glide down. Too close to the sun, the wax melts. */
    public static final DeferredItem<WingsItem> WINGS_OF_DAEDALUS = ITEMS.register("wings_of_daedalus",
            () -> new WingsItem(new Item.Properties().durability(240).rarity(Rarity.RARE)));
    /** Shell of Karkinos, the giant crab Hera sent against Heracles. */
    public static final DeferredItem<Item> KARKINOS_CLAW = ITEMS.registerSimpleItem("karkinos_claw",
            new Item.Properties().rarity(Rarity.UNCOMMON));
    /** War girdle of Hippolyta, queen of the Amazons: strength and resistance when worn. */
    public static final DeferredItem<GirdleItem> GIRDLE_OF_HIPPOLYTA = ITEMS.register("girdle_of_hippolyta",
            () -> new GirdleItem(new Item.Properties().stacksTo(1).rarity(Rarity.EPIC)));
    /** Give it to an amazon who loves you to marry her. */
    public static final DeferredItem<Item> WEDDING_RING = ITEMS.registerSimpleItem("wedding_ring",
            new Item.Properties().stacksTo(1).rarity(Rarity.UNCOMMON));
    /** Medusa's head still petrifies: right-click to freeze the creatures in front of you. */
    public static final DeferredItem<MedusaHeadItem> MEDUSA_HEAD = ITEMS.register("medusa_head",
            () -> new MedusaHeadItem(new Item.Properties().durability(32).rarity(Rarity.EPIC)));

    private GreekContent() {
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
