package com.mythsofworlds.mythology.greek.feature;

import com.mojang.serialization.Codec;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.portal.BrazierBlock;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.DecoratedPotBlock;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;

/**
 * Remains of the old temples scattered over Hellas: a row of broken columns with one fallen on the grass,
 * a small altar, the stump of a statue, a cluster of amphorae, a herm (a pillar with the head of Hermes) at the
 * roadside, or a little round shrine (tholos). Each piece sits on the ground where it lands.
 */
public class MarbleRuinFeature extends Feature<NoneFeatureConfiguration> {
    public MarbleRuinFeature(Codec<NoneFeatureConfiguration> codec) {
        super(codec);
    }

    @Override
    public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        WorldGenLevel level = context.level();
        RandomSource random = context.random();
        BlockPos origin = ground(level, context.origin());
        if (origin == null) {
            return false;
        }
        switch (random.nextInt(6)) {
            case 0 -> colonnade(level, random, origin);
            case 1 -> altar(level, random, origin);
            case 2 -> amphorae(level, random, origin);
            case 3 -> herm(level, random, origin);
            case 4 -> tholos(level, random, origin);
            default -> statue(level, random, origin);
        }
        return true;
    }

    /** First free block above dry, solid ground in this column, or null over water. */
    private static BlockPos ground(WorldGenLevel level, BlockPos pos) {
        int y = level.getHeight(Heightmap.Types.WORLD_SURFACE_WG, pos.getX(), pos.getZ());
        BlockPos top = new BlockPos(pos.getX(), y, pos.getZ());
        BlockState below = level.getBlockState(top.below());
        if (!below.getFluidState().isEmpty() || !below.isSolid()) {
            return null;
        }
        return top;
    }

    private static BlockState weathered(RandomSource random) {
        return switch (random.nextInt(6)) {
            case 0 -> Blocks.MOSSY_STONE_BRICKS.defaultBlockState();
            case 1 -> Blocks.CRACKED_STONE_BRICKS.defaultBlockState();
            default -> GreekContent.MARBLE_BRICKS.get().defaultBlockState();
        };
    }

    private void colonnade(WorldGenLevel level, RandomSource random, BlockPos origin) {
        Direction along = Direction.Plane.HORIZONTAL.getRandomDirection(random);
        BlockState pillar = GreekContent.MARBLE_PILLAR.get().defaultBlockState();
        int count = 3 + random.nextInt(3);
        for (int i = 0; i < count; i++) {
            BlockPos base = ground(level, origin.relative(along, i * 2));
            if (base == null) {
                continue;
            }
            setBlock(level, base.below(), weathered(random));
            int height = 1 + random.nextInt(5);
            for (int y = 0; y < height; y++) {
                setBlock(level, base.above(y), pillar);
            }
            if (height >= 4) {
                setBlock(level, base.above(height), GreekContent.MARBLE_BRICKS.get().defaultBlockState());
            }
        }
        // One column lies where it fell, beside the row.
        Direction side = along.getClockWise();
        BlockState lying = pillar.setValue(RotatedPillarBlock.AXIS, along.getAxis());
        BlockPos start = origin.relative(side, 2 + random.nextInt(2));
        for (int i = 0; i < 2 + random.nextInt(3); i++) {
            BlockPos pos = ground(level, start.relative(along, i));
            if (pos != null) {
                setBlock(level, pos, lying);
            }
        }
    }

    private void altar(WorldGenLevel level, RandomSource random, BlockPos origin) {
        for (int dx = -1; dx <= 1; dx++) {
            for (int dz = -1; dz <= 1; dz++) {
                BlockPos pos = ground(level, origin.offset(dx, 0, dz));
                if (pos != null && random.nextInt(5) != 0) {
                    setBlock(level, pos.below(), dx == 0 && dz == 0 ? GreekContent.OLYMPIAN_MARBLE.get().defaultBlockState()
                            : weathered(random));
                }
            }
        }
        setBlock(level, origin, Blocks.CHISELED_QUARTZ_BLOCK.defaultBlockState());
        setBlock(level, origin.above(), random.nextBoolean() ? Blocks.GOLD_BLOCK.defaultBlockState()
                : GreekContent.BRAZIER.get().defaultBlockState());
    }

    private void statue(WorldGenLevel level, RandomSource random, BlockPos origin) {
        setBlock(level, origin.below(), GreekContent.MARBLE_BRICKS.get().defaultBlockState());
        setBlock(level, origin, Blocks.QUARTZ_PILLAR.defaultBlockState());
        setBlock(level, origin.above(), Blocks.QUARTZ_BLOCK.defaultBlockState());
        if (random.nextBoolean()) {
            setBlock(level, origin.above(2), Blocks.CHISELED_QUARTZ_BLOCK.defaultBlockState());
        } else {
            // The head lies in the grass.
            BlockPos head = ground(level, origin.relative(Direction.Plane.HORIZONTAL.getRandomDirection(random), 2));
            if (head != null) {
                setBlock(level, head, Blocks.CHISELED_QUARTZ_BLOCK.defaultBlockState());
            }
        }
    }

    private void amphorae(WorldGenLevel level, RandomSource random, BlockPos origin) {
        for (int i = 0; i < 3 + random.nextInt(4); i++) {
            BlockPos pos = ground(level, origin.offset(random.nextInt(5) - 2, 0, random.nextInt(5) - 2));
            if (pos != null && level.getBlockState(pos).isAir()) {
                setBlock(level, pos, Blocks.DECORATED_POT.defaultBlockState()
                        .setValue(BlockStateProperties.HORIZONTAL_FACING, Direction.Plane.HORIZONTAL.getRandomDirection(random))
                        .setValue(DecoratedPotBlock.CRACKED, random.nextInt(3) == 0));
            }
        }
    }

    private void herm(WorldGenLevel level, RandomSource random, BlockPos origin) {
        setBlock(level, origin.below(), GreekContent.MARBLE_BRICKS.get().defaultBlockState());
        setBlock(level, origin, GreekContent.MARBLE_PILLAR.get().defaultBlockState());
        setBlock(level, origin.above(), GreekContent.MARBLE_PILLAR.get().defaultBlockState());
        setBlock(level, origin.above(2), Blocks.CHISELED_QUARTZ_BLOCK.defaultBlockState());
        BlockPos flowers = ground(level, origin.relative(Direction.Plane.HORIZONTAL.getRandomDirection(random)));
        if (flowers != null && level.getBlockState(flowers).isAir()) {
            setBlock(level, flowers, Blocks.DECORATED_POT.defaultBlockState());
        }
    }

    private void tholos(WorldGenLevel level, RandomSource random, BlockPos origin) {
        BlockState pillar = GreekContent.MARBLE_PILLAR.get().defaultBlockState();
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                if (dx * dx + dz * dz <= 5) {
                    setBlock(level, origin.offset(dx, -1, dz), weathered(random));
                }
            }
        }
        int[][] ring = {{2, 0}, {1, 2}, {-1, 2}, {-2, 0}, {-1, -2}, {1, -2}};
        for (int[] p : ring) {
            int height = random.nextInt(4) == 0 ? 1 + random.nextInt(2) : 3;
            for (int y = 0; y < height; y++) {
                setBlock(level, origin.offset(p[0], y, p[1]), pillar);
            }
            if (height == 3) {
                setBlock(level, origin.offset(p[0], 3, p[1]), Blocks.SMOOTH_QUARTZ_SLAB.defaultBlockState());
            }
        }
        setBlock(level, origin, GreekContent.BRAZIER.get().defaultBlockState().setValue(BrazierBlock.LIT, random.nextBoolean()));
    }
}
