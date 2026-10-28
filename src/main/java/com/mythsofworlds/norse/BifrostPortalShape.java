package com.mythsofworlds.norse;

import com.mythsofworlds.registry.ModBlocks;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashSet;
import java.util.Set;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import org.jetbrains.annotations.Nullable;

/**
 * Finds a closed runestone frame around an air pocket and fills it with Bifrost portal blocks.
 * Any shape works as long as it is a flat, closed outline of runestone (like a nether portal, but not only rectangles).
 */
public final class BifrostPortalShape {
    /** Largest interior a frame may enclose: 21 x 21, the same limit as a nether portal. */
    public static final int MAX_INTERIOR = 21 * 21;
    /** Smallest interior: at least two blocks tall so a player fits. */
    public static final int MIN_INTERIOR = 2;

    private BifrostPortalShape() {
    }

    /** Tries both vertical orientations from {@code start}; returns true if a portal was created. */
    public static boolean tryLight(Level level, BlockPos start) {
        for (Direction.Axis axis : new Direction.Axis[]{Direction.Axis.X, Direction.Axis.Z}) {
            Set<BlockPos> interior = findInterior(level, start, axis);
            if (interior != null) {
                BlockState portal = ModBlocks.BIFROST_PORTAL.get().defaultBlockState()
                        .setValue(BifrostPortalBlock.AXIS, axis);
                for (BlockPos pos : interior) {
                    level.setBlock(pos, portal, Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE);
                }
                return true;
            }
        }
        return false;
    }

    /**
     * Flood-fills air in the vertical plane of {@code axis}. Returns null if the pocket leaks (touches a block
     * that is neither air nor runestone, or grows past {@link #MAX_INTERIOR}).
     */
    @Nullable
    public static Set<BlockPos> findInterior(Level level, BlockPos start, Direction.Axis axis) {
        if (!level.getBlockState(start).isAir()) {
            return null;
        }
        Direction[] dirs = axis == Direction.Axis.X
                ? new Direction[]{Direction.EAST, Direction.WEST, Direction.UP, Direction.DOWN}
                : new Direction[]{Direction.NORTH, Direction.SOUTH, Direction.UP, Direction.DOWN};

        Set<BlockPos> visited = new HashSet<>();
        Deque<BlockPos> queue = new ArrayDeque<>();
        visited.add(start.immutable());
        queue.add(start.immutable());
        while (!queue.isEmpty()) {
            BlockPos pos = queue.poll();
            for (Direction dir : dirs) {
                BlockPos next = pos.relative(dir);
                if (visited.contains(next)) {
                    continue;
                }
                BlockState state = level.getBlockState(next);
                if (state.is(ModBlocks.RUNESTONE.get())) {
                    continue;
                }
                if (!state.isAir() || level.isOutsideBuildHeight(next)) {
                    return null;
                }
                visited.add(next);
                if (visited.size() > MAX_INTERIOR) {
                    return null;
                }
                queue.add(next);
            }
        }
        return visited.size() >= MIN_INTERIOR ? visited : null;
    }
}
