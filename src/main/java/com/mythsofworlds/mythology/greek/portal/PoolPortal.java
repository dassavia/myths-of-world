package com.mythsofworlds.mythology.greek.portal;

import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekSounds;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashSet;
import java.util.Set;
import java.util.function.Predicate;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.FluidTags;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import org.jetbrains.annotations.Nullable;

/**
 * The Greek portal is a sacred pool rather than a frame:
 * <pre>
 *   B M M B      B = brazier (on top of the rim corner), M = Olympian marble rim, W = still water
 *   M W W M      Any rectangle of water from 1x1 up to 8x8 works. Light all four braziers
 *   M W W M      with the Promethean Torch and the water turns into the portal.
 *   B M M B
 * </pre>
 */
public final class PoolPortal {
    public static final int MAX_SIDE = 8;
    public static final int SEARCH_RADIUS = 16;

    private static final int[][] DIAGONALS = {{1, 1}, {1, -1}, {-1, 1}, {-1, -1}};

    private PoolPortal() {
    }

    private static boolean isRim(BlockState state) {
        return state.is(GreekContent.OLYMPIAN_MARBLE.get());
    }

    private static boolean isLitBrazier(BlockState state) {
        return state.is(GreekContent.BRAZIER.get()) && state.getValue(BrazierBlock.LIT);
    }

    private static boolean isStillWater(Level level, BlockPos pos) {
        var fluid = level.getFluidState(pos);
        return level.getBlockState(pos).is(Blocks.WATER) && fluid.isSource() && fluid.is(FluidTags.WATER);
    }

    /** Called after a brazier was lit: opens the pool it guards if all four corners burn. */
    public static boolean tryLight(Level level, BlockPos brazier) {
        for (int[] d : DIAGONALS) {
            BlockPos start = brazier.offset(d[0], -1, d[1]);
            Set<BlockPos> pool = flood(level, start, pos -> isStillWater(level, pos));
            if (pool == null || !isFramed(level, pool)) {
                continue;
            }
            BlockState portal = GreekContent.HELLAS_PORTAL.get().defaultBlockState();
            for (BlockPos pos : pool) {
                level.setBlock(pos, portal, Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE);
            }
            level.playSound(null, start, GreekSounds.PORTAL_IGNITE.get(), SoundSource.BLOCKS, 1.5F, 1.0F);
            return true;
        }
        return false;
    }

    /** Puts the water back in every pool portal this brazier was guarding. */
    public static void collapseAround(Level level, BlockPos brazier) {
        for (int[] d : DIAGONALS) {
            BlockPos start = brazier.offset(d[0], -1, d[1]);
            if (!level.getBlockState(start).is(GreekContent.HELLAS_PORTAL.get())) {
                continue;
            }
            Set<BlockPos> pool = flood(level, start, pos -> level.getBlockState(pos).is(GreekContent.HELLAS_PORTAL.get()));
            if (pool != null) {
                for (BlockPos pos : pool) {
                    level.setBlock(pos, Blocks.WATER.defaultBlockState(), Block.UPDATE_ALL);
                }
            }
        }
    }

    /** Flat flood fill in the horizontal plane; null if empty or larger than {@link #MAX_SIDE} squared. */
    @Nullable
    private static Set<BlockPos> flood(Level level, BlockPos start, Predicate<BlockPos> inside) {
        if (!inside.test(start)) {
            return null;
        }
        Set<BlockPos> found = new HashSet<>();
        Deque<BlockPos> queue = new ArrayDeque<>();
        found.add(start.immutable());
        queue.add(start.immutable());
        while (!queue.isEmpty()) {
            BlockPos pos = queue.poll();
            for (Direction dir : Direction.Plane.HORIZONTAL) {
                BlockPos next = pos.relative(dir);
                if (!found.contains(next) && inside.test(next)) {
                    found.add(next);
                    if (found.size() > MAX_SIDE * MAX_SIDE) {
                        return null;
                    }
                    queue.add(next);
                }
            }
        }
        return found;
    }

    /** The pool is a full rectangle, ringed with Olympian marble, with a lit brazier above each rim corner. */
    private static boolean isFramed(Level level, Set<BlockPos> pool) {
        int minX = Integer.MAX_VALUE, maxX = Integer.MIN_VALUE, minZ = Integer.MAX_VALUE, maxZ = Integer.MIN_VALUE;
        int y = pool.iterator().next().getY();
        for (BlockPos pos : pool) {
            minX = Math.min(minX, pos.getX());
            maxX = Math.max(maxX, pos.getX());
            minZ = Math.min(minZ, pos.getZ());
            maxZ = Math.max(maxZ, pos.getZ());
        }
        if ((maxX - minX + 1) * (maxZ - minZ + 1) != pool.size() || maxX - minX >= MAX_SIDE || maxZ - minZ >= MAX_SIDE) {
            return false;
        }
        for (int x = minX - 1; x <= maxX + 1; x++) {
            for (int z = minZ - 1; z <= maxZ + 1; z++) {
                boolean border = x == minX - 1 || x == maxX + 1 || z == minZ - 1 || z == maxZ + 1;
                if (border && !isRim(level.getBlockState(new BlockPos(x, y, z)))) {
                    return false;
                }
            }
        }
        for (int x : new int[]{minX - 1, maxX + 1}) {
            for (int z : new int[]{minZ - 1, maxZ + 1}) {
                if (!isLitBrazier(level.getBlockState(new BlockPos(x, y + 1, z)))) {
                    return false;
                }
            }
        }
        return true;
    }

    /** Where to stand after arriving: on the rim beside an existing pool near {@code near}, or beside a new one. */
    public static BlockPos findOrCreate(ServerLevel level, BlockPos near) {
        BlockPos existing = find(level, near);
        return existing != null ? standingSpot(level, existing) : build(level, near);
    }

    @Nullable
    public static BlockPos find(ServerLevel level, BlockPos near) {
        BlockPos.MutableBlockPos cursor = new BlockPos.MutableBlockPos();
        BlockPos best = null;
        double bestDist = Double.MAX_VALUE;
        int minY = level.getMinBuildHeight();
        int maxY = minY + level.dimensionType().logicalHeight() - 1;
        for (int dx = -SEARCH_RADIUS; dx <= SEARCH_RADIUS; dx++) {
            for (int dz = -SEARCH_RADIUS; dz <= SEARCH_RADIUS; dz++) {
                for (int y = minY; y <= maxY; y++) {
                    cursor.set(near.getX() + dx, y, near.getZ() + dz);
                    if (level.getBlockState(cursor).is(GreekContent.HELLAS_PORTAL.get())) {
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

    /** Walks to the north-west corner of the pool and returns the spot on the rim west of it. */
    private static BlockPos standingSpot(ServerLevel level, BlockPos portal) {
        BlockPos pos = portal;
        while (level.getBlockState(pos.west()).is(GreekContent.HELLAS_PORTAL.get())) {
            pos = pos.west();
        }
        while (level.getBlockState(pos.north()).is(GreekContent.HELLAS_PORTAL.get())) {
            pos = pos.north();
        }
        return pos.west().above();
    }

    /** Builds a 2x2 pool with its rim, foundation and four burning braziers on the surface. */
    public static BlockPos build(ServerLevel level, BlockPos near) {
        int x = near.getX();
        int z = near.getZ();
        int top = level.getMinBuildHeight() + level.dimensionType().logicalHeight();
        int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
        y = Math.max(level.getMinBuildHeight() + 2, Math.min(y, top - 6));
        int flags = Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE;
        BlockState rim = GreekContent.OLYMPIAN_MARBLE.get().defaultBlockState();
        BlockState floor = GreekContent.MARBLE_BRICKS.get().defaultBlockState();
        BlockState brazier = GreekContent.BRAZIER.get().defaultBlockState().setValue(BrazierBlock.LIT, true);
        BlockState portal = GreekContent.HELLAS_PORTAL.get().defaultBlockState();
        for (int i = -2; i <= 3; i++) {
            for (int k = -2; k <= 3; k++) {
                level.setBlock(new BlockPos(x + i, y - 1, z + k), floor, flags);
                for (int j = 0; j <= 3; j++) {
                    level.setBlock(new BlockPos(x + i, y + j, z + k), Blocks.AIR.defaultBlockState(), flags);
                }
            }
        }
        for (int i = -1; i <= 2; i++) {
            for (int k = -1; k <= 2; k++) {
                boolean border = i == -1 || i == 2 || k == -1 || k == 2;
                level.setBlock(new BlockPos(x + i, y, z + k), border ? rim : portal, flags);
            }
        }
        for (int i : new int[]{-1, 2}) {
            for (int k : new int[]{-1, 2}) {
                level.setBlock(new BlockPos(x + i, y + 1, z + k), brazier, flags);
            }
        }
        return new BlockPos(x - 1, y + 1, z);
    }
}
