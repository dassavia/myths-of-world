package com.mythsofworlds.mythology.egyptian.block;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import org.jetbrains.annotations.Nullable;

/**
 * The pyramid that leads to the Duat. It is built by hand of pyramid stone (or hieroglyph stone) in three steps, with
 * a golden capstone, the benben, on top, and a doorway left open in the middle of one side of the base:
 * <pre>
 *   step 0 (5x5)   S S S S S     step 1 (3x3)   S S S     step 2   G      S = pyramid stone, G = gold block
 *                  S S S S S                    S S S              (the benben)
 *                  S S S S S                    S S S
 *                  S S S S S
 *                  S S . S S     . = the doorway: air, and air above it
 * </pre>
 * Touch it with the ankh and the gate of shadow fills the doorway, two blocks high: its lower half stands in the
 * base, its upper half against the second step.
 */
public final class Pyramid {
    public static final int SEARCH_RADIUS = 16;
    /** Height of a pyramid with the air above its doorway. */
    public static final int HEIGHT = 3;

    /** The lower block of a gate and the way it faces (out of the pyramid). */
    public record Gate(BlockPos lower, Direction facing) {
    }

    /** Where a traveller arrives, and which way they face (away from the pyramid). */
    public record Arrival(BlockPos pos, Direction facing) {
    }

    private Pyramid() {
    }

    public static boolean isStone(BlockState state) {
        return state.is(EgyptianContent.PYRAMID_STONE.get()) || state.is(EgyptianContent.HIEROGLYPH_STONE.get());
    }

    private static boolean isGate(BlockState state) {
        return state.getBlock() instanceof PyramidGateBlock;
    }

    private static boolean open(BlockState state) {
        return state.isAir() || state.canBeReplaced() || isGate(state);
    }

    /** The pyramid around {@code clicked} (any of its blocks or its doorway), or null if there is none. */
    @Nullable
    public static Gate find(Level level, BlockPos clicked) {
        for (int dy = 0; dy <= 2; dy++) {
            for (int dx = -2; dx <= 2; dx++) {
                for (int dz = -2; dz <= 2; dz++) {
                    BlockPos cap = clicked.offset(dx, dy, dz);
                    if (level.getBlockState(cap).is(Blocks.GOLD_BLOCK)) {
                        Gate gate = check(level, cap);
                        if (gate != null) {
                            return gate;
                        }
                    }
                }
            }
        }
        return null;
    }

    /** Whether the golden capstone at {@code cap} crowns a whole pyramid; its gate if so. */
    @Nullable
    public static Gate check(Level level, BlockPos cap) {
        BlockPos step1 = cap.below();
        for (int dx = -1; dx <= 1; dx++) {
            for (int dz = -1; dz <= 1; dz++) {
                if (!isStone(level.getBlockState(step1.offset(dx, 0, dz)))) {
                    return null;
                }
            }
        }
        BlockPos base = cap.below(2);
        Direction door = null;
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                BlockPos pos = base.offset(dx, 0, dz);
                if (isStone(level.getBlockState(pos))) {
                    continue;
                }
                boolean sideMiddle = Math.abs(dx) == 2 && dz == 0 || Math.abs(dz) == 2 && dx == 0;
                if (door == null && sideMiddle && open(level.getBlockState(pos)) && open(level.getBlockState(pos.above()))) {
                    door = Direction.fromDelta(Integer.signum(dx), 0, Integer.signum(dz));
                } else {
                    return null;
                }
            }
        }
        return door == null ? null : new Gate(base.relative(door, 2), door);
    }

    /** Fills the doorway with the gate of shadow. */
    public static void open(Level level, Gate gate) {
        int flags = Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE;
        BlockState state = EgyptianContent.PYRAMID_GATE.get().defaultBlockState().setValue(PyramidGateBlock.FACING, gate.facing())
                .setValue(PyramidGateBlock.UPPER, false);
        level.setBlock(gate.lower(), state, flags);
        level.setBlock(gate.lower().above(), state.setValue(PyramidGateBlock.UPPER, true), flags);
    }

    /**
     * Builds a pyramid with its base centred on {@code centre} (ground level) and its doorway facing {@code facing},
     * on a platform of sandstone, and opens its gate. Returns the gate.
     */
    public static Gate build(Level level, BlockPos centre, Direction facing) {
        int flags = Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE;
        BlockState stone = EgyptianContent.PYRAMID_STONE.get().defaultBlockState();
        BlockState glyphs = EgyptianContent.HIEROGLYPH_STONE.get().defaultBlockState();
        for (int dx = -3; dx <= 3; dx++) {
            for (int dz = -3; dz <= 3; dz++) {
                level.setBlock(centre.offset(dx, -1, dz), Blocks.SMOOTH_SANDSTONE.defaultBlockState(), flags);
                for (int y = 0; y <= HEIGHT; y++) {
                    level.setBlock(centre.offset(dx, y, dz), Blocks.AIR.defaultBlockState(), flags);
                }
            }
        }
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                boolean corner = Math.abs(dx) == 2 && Math.abs(dz) == 2;
                level.setBlock(centre.offset(dx, 0, dz), corner ? glyphs : stone, flags);
                if (Math.abs(dx) <= 1 && Math.abs(dz) <= 1) {
                    level.setBlock(centre.offset(dx, 1, dz), stone, flags);
                }
            }
        }
        level.setBlock(centre.above(2), Blocks.GOLD_BLOCK.defaultBlockState(), flags);
        Gate gate = new Gate(centre.relative(facing, 2), facing);
        open(level, gate);
        return gate;
    }

    /** The lower block of the nearest gate within {@link #SEARCH_RADIUS} blocks, or null. */
    @Nullable
    public static BlockPos findGate(ServerLevel level, BlockPos near) {
        BlockPos.MutableBlockPos cursor = new BlockPos.MutableBlockPos();
        BlockPos best = null;
        double bestDist = Double.MAX_VALUE;
        int minY = level.getMinBuildHeight();
        int maxY = minY + level.dimensionType().logicalHeight() - 1;
        for (int dx = -SEARCH_RADIUS; dx <= SEARCH_RADIUS; dx++) {
            for (int dz = -SEARCH_RADIUS; dz <= SEARCH_RADIUS; dz++) {
                for (int y = minY; y <= maxY; y++) {
                    cursor.set(near.getX() + dx, y, near.getZ() + dz);
                    BlockState state = level.getBlockState(cursor);
                    if (isGate(state) && !state.getValue(PyramidGateBlock.UPPER)) {
                        double dist = cursor.distSqr(near);
                        if (dist < bestDist) {
                            bestDist = dist;
                            best = cursor.immutable();
                        }
                    }
                }
            }
        }
        return best;
    }

    /** The doorstep of a pyramid near {@code near}: an existing gate, or a pyramid built there on the surface. */
    public static Arrival findOrBuild(ServerLevel level, BlockPos near) {
        BlockPos gate = findGate(level, near);
        if (gate == null) {
            int x = near.getX();
            int z = near.getZ();
            int top = level.getMinBuildHeight() + level.dimensionType().logicalHeight();
            int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
            y = Math.max(level.getMinBuildHeight() + 2, Math.min(y, top - HEIGHT - 4));
            gate = build(level, new BlockPos(x, y, z), Direction.SOUTH).lower();
        }
        Direction facing = level.getBlockState(gate).getValue(PyramidGateBlock.FACING);
        return new Arrival(gate.relative(facing), facing);
    }
}
