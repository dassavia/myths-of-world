package com.mythsofworlds.mythology.greek.feature;

import com.mojang.serialization.Codec;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.portal.BrazierBlock;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.util.RandomSource;
import net.minecraft.world.RandomizableContainer;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.ChestBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.minecraft.world.level.storage.loot.LootTable;

/**
 * A flat island of cloud made of a few overlapping squashed ellipsoids, floating high in the sky.
 * One in three carries a little shrine: a marble floor, four columns and a burning brazier, sometimes a chest.
 */
public class CloudIslandFeature extends Feature<NoneFeatureConfiguration> {
    private static final ResourceKey<LootTable> SHRINE_LOOT =
            ResourceKey.create(Registries.LOOT_TABLE, MythsOfWorlds.id("chests/cloud_shrine"));

    public CloudIslandFeature(Codec<NoneFeatureConfiguration> codec) {
        super(codec);
    }

    @Override
    public boolean place(FeaturePlaceContext<NoneFeatureConfiguration> context) {
        WorldGenLevel level = context.level();
        RandomSource random = context.random();
        BlockPos origin = context.origin();
        if (origin.getY() + 8 >= level.getMaxBuildHeight()) {
            return false;
        }
        BlockState cloud = GreekContent.CLOUD.get().defaultBlockState();
        int puffs = 2 + random.nextInt(4);
        int top = origin.getY();
        for (int i = 0; i < puffs; i++) {
            int rx = 3 + random.nextInt(5);
            int rz = 3 + random.nextInt(5);
            int ry = 1 + random.nextInt(2);
            BlockPos centre = i == 0 ? origin : origin.offset(random.nextInt(9) - 4, random.nextInt(3) - 1, random.nextInt(9) - 4);
            top = Math.max(top, centre.getY() + ry);
            for (int dx = -rx; dx <= rx; dx++) {
                for (int dz = -rz; dz <= rz; dz++) {
                    for (int dy = -ry; dy <= ry; dy++) {
                        double d = (dx * dx) / (double) (rx * rx) + (dz * dz) / (double) (rz * rz) + (dy * dy) / (double) (ry * ry);
                        if (d <= 1.0 - random.nextFloat() * 0.15) {
                            BlockPos pos = centre.offset(dx, dy, dz);
                            if (level.isEmptyBlock(pos)) {
                                setBlock(level, pos, cloud);
                            }
                        }
                    }
                }
            }
        }
        if (random.nextInt(3) == 0) {
            shrine(level, random, origin.atY(top + 1));
        }
        return true;
    }

    private void shrine(WorldGenLevel level, RandomSource random, BlockPos floor) {
        BlockState bricks = GreekContent.MARBLE_BRICKS.get().defaultBlockState();
        BlockState gold = GreekContent.OLYMPIAN_MARBLE.get().defaultBlockState();
        BlockState pillar = GreekContent.MARBLE_PILLAR.get().defaultBlockState();
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                setBlock(level, floor.offset(dx, -1, dz), Math.abs(dx) == 2 || Math.abs(dz) == 2 ? bricks : gold);
            }
        }
        for (int dx : new int[]{-2, 2}) {
            for (int dz : new int[]{-2, 2}) {
                for (int y = 0; y < 3; y++) {
                    setBlock(level, floor.offset(dx, y, dz), pillar);
                }
                setBlock(level, floor.offset(dx, 3, dz), bricks);
            }
        }
        setBlock(level, floor, GreekContent.BRAZIER.get().defaultBlockState().setValue(BrazierBlock.LIT, true));
        if (random.nextInt(3) == 0) {
            BlockPos chest = floor.north();
            setBlock(level, chest, Blocks.CHEST.defaultBlockState().setValue(ChestBlock.FACING, Direction.SOUTH));
            RandomizableContainer.setBlockEntityLootTable(level, random, chest, SHRINE_LOOT);
        }
    }
}
