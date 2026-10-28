package com.mythsofworlds.core.portal;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import org.jetbrains.annotations.Nullable;

/** Finds the matching portal on the other side, or builds a new one there. */
public final class PortalPlacement {
    /** How far around the arrival point we look for an existing portal before building a new one. */
    public static final int SEARCH_RADIUS = 16;

    private PortalPlacement() {
    }

    /** Returns the bottom corner block (smallest x/z) of a {@code portal} near {@code near} in {@code level}, building one if none exists. */
    public static BlockPos findOrCreate(ServerLevel level, BlockPos near, MythPortalBlock portal) {
        BlockPos existing = find(level, near, portal);
        return existing != null ? existing : build(level, near, portal);
    }

    @Nullable
    public static BlockPos find(ServerLevel level, BlockPos near, MythPortalBlock portal) {
        BlockPos.MutableBlockPos cursor = new BlockPos.MutableBlockPos();
        BlockPos best = null;
        double bestDist = Double.MAX_VALUE;
        int minY = level.getMinBuildHeight();
        int maxY = minY + level.dimensionType().logicalHeight() - 1;
        for (int dx = -SEARCH_RADIUS; dx <= SEARCH_RADIUS; dx++) {
            for (int dz = -SEARCH_RADIUS; dz <= SEARCH_RADIUS; dz++) {
                for (int y = minY; y <= maxY; y++) {
                    cursor.set(near.getX() + dx, y, near.getZ() + dz);
                    if (level.getBlockState(cursor).is(portal) && !level.getBlockState(cursor.below()).is(portal)) {
                        double dist = cursor.distSqr(near);
                        if (dist < bestDist) {
                            bestDist = dist;
                            best = cursor.immutable();
                        }
                    }
                }
            }
        }
        return best == null ? null : cornerOf(level, best, portal);
    }

    /** Walks from any bottom portal block to the bottom corner with the smallest x/z, so results are stable. */
    private static BlockPos cornerOf(ServerLevel level, BlockPos bottom, MythPortalBlock portal) {
        Direction back = level.getBlockState(bottom).getValue(MythPortalBlock.AXIS) == Direction.Axis.X
                ? Direction.WEST : Direction.NORTH;
        BlockPos pos = bottom;
        while (level.getBlockState(pos.relative(back)).is(portal)) {
            pos = pos.relative(back);
        }
        return pos;
    }

    /** Builds a 2x3 portal in its frame on the surface, with a small platform on both sides. */
    public static BlockPos build(ServerLevel level, BlockPos near, MythPortalBlock portal) {
        int x = near.getX();
        int z = near.getZ();
        int top = level.getMinBuildHeight() + level.dimensionType().logicalHeight();
        int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
        y = Math.max(level.getMinBuildHeight() + 2, Math.min(y, top - 6));
        BlockPos base = new BlockPos(x, y, z);

        BlockState frame = portal.settings().frame().get().defaultBlockState();
        BlockState surface = portal.defaultBlockState().setValue(MythPortalBlock.AXIS, Direction.Axis.X);
        int flags = Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE;

        // Platform and headroom in front of and behind the portal.
        for (int i = -1; i <= 2; i++) {
            for (int k = -1; k <= 1; k += 2) {
                level.setBlock(base.offset(i, -1, k), frame, flags);
                for (int j = 0; j <= 2; j++) {
                    level.setBlock(base.offset(i, j, k), Blocks.AIR.defaultBlockState(), flags);
                }
            }
        }
        // Frame first so the portal blocks never see a missing neighbour.
        for (int i = -1; i <= 2; i++) {
            for (int j = -1; j <= 3; j++) {
                if (i == -1 || i == 2 || j == -1 || j == 3) {
                    level.setBlock(base.offset(i, j, 0), frame, flags);
                }
            }
        }
        for (int i = 0; i <= 1; i++) {
            for (int j = 0; j <= 2; j++) {
                level.setBlock(base.offset(i, j, 0), surface, flags);
            }
        }
        return base;
    }
}
