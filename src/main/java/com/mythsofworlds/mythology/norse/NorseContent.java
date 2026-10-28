package com.mythsofworlds.mythology.norse;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.portal.MythPortalBlock;
import com.mythsofworlds.core.portal.PortalIgniterItem;
import com.mythsofworlds.core.portal.PortalSettings;
import java.util.List;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredItem;

import static com.mythsofworlds.registry.ModRegistries.BLOCKS;
import static com.mythsofworlds.registry.ModRegistries.ITEMS;

/**
 * Norse mythology: runestone, the Rune Igniter and the Bifrost portal to Jotunheim.
 * Use this class as a template for a new mythology (see docs/ADDING_CONTENT.md).
 */
public final class NorseContent {
    /** Defined in data/mythsofworlds/dimension/jotunheim.json. */
    public static final ResourceKey<Level> JOTUNHEIM =
            ResourceKey.create(Registries.DIMENSION, MythsOfWorlds.id("jotunheim"));

    // ---- Blocks ----

    /** Frame block for the Bifrost portal. Its carved runes glow faintly. */
    public static final DeferredBlock<Block> RUNESTONE = BLOCKS.registerSimpleBlock("runestone",
            BlockBehaviour.Properties.of()
                    .mapColor(MapColor.DEEPSLATE)
                    .strength(3.0F, 9.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.DEEPSLATE_BRICKS)
                    .lightLevel(state -> 3));

    public static final DeferredBlock<MythPortalBlock> BIFROST_PORTAL = BLOCKS.register("bifrost_portal",
            () -> new MythPortalBlock(
                    PortalSettings.toDimension(RUNESTONE, JOTUNHEIM, ParticleTypes.SNOWFLAKE),
                    BlockBehaviour.Properties.of()
                            .mapColor(MapColor.COLOR_LIGHT_BLUE)
                            .noCollission()
                            .strength(-1.0F)
                            .sound(SoundType.GLASS)
                            .lightLevel(state -> 11)
                            .noLootTable()
                            .pushReaction(PushReaction.BLOCK)));

    // ---- Items ----

    public static final DeferredItem<BlockItem> RUNESTONE_ITEM = ITEMS.registerSimpleBlockItem(RUNESTONE);

    public static final DeferredItem<PortalIgniterItem> RUNE_IGNITER = ITEMS.register("rune_igniter",
            () -> new PortalIgniterItem(new Item.Properties().durability(16).rarity(Rarity.RARE),
                    () -> SoundEvents.BEACON_ACTIVATE, List.of(BIFROST_PORTAL)));

    private NorseContent() {
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
