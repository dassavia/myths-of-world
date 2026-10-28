package com.mythsofworlds.registry;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.norse.BifrostPortalBlock;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(MythsOfWorlds.MODID);

    /** Frame block for the Bifrost portal. Its carved runes glow faintly. */
    public static final DeferredBlock<Block> RUNESTONE = BLOCKS.registerSimpleBlock("runestone",
            BlockBehaviour.Properties.of()
                    .mapColor(MapColor.DEEPSLATE)
                    .strength(3.0F, 9.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.DEEPSLATE_BRICKS)
                    .lightLevel(state -> 3));

    public static final DeferredBlock<BifrostPortalBlock> BIFROST_PORTAL = BLOCKS.register("bifrost_portal",
            () -> new BifrostPortalBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_LIGHT_BLUE)
                    .noCollission()
                    .strength(-1.0F)
                    .sound(SoundType.GLASS)
                    .lightLevel(state -> 11)
                    .noLootTable()
                    .pushReaction(PushReaction.BLOCK)));

    private ModBlocks() {
    }
}
