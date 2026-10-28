package com.mythsofworlds.core.portal;

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
 * Finds a closed frame around an air pocket and fills it with portal blocks.
 * Works for any {@link MythPortalBlock}: the frame block comes from its {@link PortalSettings}.
 * Any flat, closed outline is accepted (rectangles like a nether portal, but also other shapes).
 */
public final class PortalShape {
    /** Largest interior a frame may enclose: 21 x 21, the same limit as a nether portal. */
    public static final int MAX_INTERIOR = 21 * 21;
    /** Smallest interior: at least two blocks so a player fits. */
    public static final int MIN_INTERIOR = 2;

    private PortalShape() {
    }

    /** Tries both vertical orientations from {@code start}; returns true if a portal was created. */
    public static boolean tryLight(Level level, BlockPos start, MythPortalBlock portal) {
        Block frame = portal.settings().frame().get();
        for (Direction.Axis axis : new Direction.Axis[]{Direction.Axis.X, Direction.Axis.Z}) {
            Set<BlockPos> interior = findInterior(level, start, axis, frame);
            if (interior != null) {
                BlockState state = portal.defaultBlockState().setValue(MythPortalBlock.AXIS, axis);
                for (BlockPos pos : interior) {
                    level.setBlock(pos, state, Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE);
                }
                return true;
            }
        }
        return false;
    }

    /**
     * Flood-fills air in the vertical plane of {@code axis}. Returns null if the pocket leaks (touches a block
     * that is neither air nor {@code frame}, or grows past {@link #MAX_INTERIOR}).
     */
    @Nullable
    public static Set<BlockPos> findInterior(Level level, BlockPos start, Direction.Axis axis, Block frame) {
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
                if (state.is(frame)) {
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
