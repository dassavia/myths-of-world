package com.mythsofworlds.mythology.egyptian.block;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.FluidTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.LevelReader;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.BonemealableBlock;
import net.minecraft.world.level.block.state.BlockState;

/**
 * The black silt of the Nile (Kemet, "the black land"), left on the banks by the yearly flood: the most fertile soil
 * of the world. While there is water within {@link #WATER_RANGE} blocks, every random tick it makes
 * {@link #GROWTH_TRIES} plants above and beside it (up to two blocks around and two up: crops on farmland next to the
 * silt, saplings, papyrus (sugar cane) rooted in the silt itself) grow as if a random tick had fallen on them too.
 * It counts as dirt, so cane, saplings and flowers can be planted in it.
 */
public class NileSiltBlock extends Block {
    public static final int WATER_RANGE = 4;
    public static final int GROWTH_TRIES = 2;

    public NileSiltBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected boolean isRandomlyTicking(BlockState state) {
        return true;
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        if (!watered(level, pos)) {
            return;
        }
        for (int i = 0; i < GROWTH_TRIES; i++) {
            BlockPos plant = pos.offset(random.nextInt(5) - 2, 1 + random.nextInt(2), random.nextInt(5) - 2);
            if (feed(level, plant, random) && random.nextInt(4) == 0) {
                level.sendParticles(ParticleTypes.HAPPY_VILLAGER, plant.getX() + 0.5, plant.getY() + 0.5, plant.getZ() + 0.5,
                        2, 0.3, 0.3, 0.3, 0.0);
            }
        }
    }

    /** Gives the plant at {@code pos} one more random tick, if it is a growing plant; returns whether it was one. */
    public static boolean feed(ServerLevel level, BlockPos pos, RandomSource random) {
        BlockState plant = level.getBlockState(pos);
        boolean grows = plant.getBlock() instanceof BonemealableBlock || plant.is(Blocks.SUGAR_CANE);
        if (!grows || plant.isSolidRender(level, pos) || !plant.isRandomlyTicking()) {
            return false;
        }
        plant.randomTick(level, pos, random);
        return true;
    }

    /** Whether the flood reaches this silt: water within {@link #WATER_RANGE} blocks, at its level or one above. */
    public static boolean watered(LevelReader level, BlockPos pos) {
        for (BlockPos near : BlockPos.betweenClosed(pos.offset(-WATER_RANGE, 0, -WATER_RANGE), pos.offset(WATER_RANGE, 1, WATER_RANGE))) {
            if (level.getFluidState(near).is(FluidTags.WATER)) {
                return true;
            }
        }
        return false;
    }
}
