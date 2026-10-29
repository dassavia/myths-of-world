package com.mythsofworlds.mythology.slavic.block;

import com.mythsofworlds.mythology.slavic.SlavicContent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.AABB;
import org.jetbrains.annotations.Nullable;

/**
 * The World Tree, the oak whose crown holds up the sky and whose roots reach down to Nav. Nothing is built: an acorn
 * of the World Tree planted on earth grows at once into a great oak, a 3x3 trunk {@link #HEIGHT} blocks tall with a
 * wide crown and roots, and a two-block hollow at the foot of the trunk is the way down.
 * <pre>
 *   top view      L L L      L = oak log, H = hollow (facing south here, towards the planter)
 *                 L L L
 *                 L H L
 *                   .        . = where you stand to step in, and where you arrive
 * </pre>
 */
public final class WorldTree {
    public static final int HEIGHT = 11;
    public static final int CROWN_RADIUS = 5;
    public static final int SEARCH_RADIUS = 16;

    /** Where a traveller arrives, and which way they face (away from the tree). */
    public record Arrival(BlockPos pos, Direction facing) {
    }

    private WorldTree() {
    }

    private static boolean replaceable(BlockState state) {
        return state.isAir() || state.canBeReplaced() || state.is(BlockTags.LEAVES) || state.is(BlockTags.FLOWERS)
                || state.is(BlockTags.SAPLINGS);
    }

    /** Whether a tree with its trunk centred on {@code centre} (ground level) fits: room for trunk and doorway. */
    public static boolean canGrow(Level level, BlockPos centre, Direction facing) {
        int top = level.getMinBuildHeight() + level.dimensionType().logicalHeight();
        if (centre.getY() - 1 < level.getMinBuildHeight() || centre.getY() + HEIGHT + CROWN_RADIUS >= top) {
            return false;
        }
        for (int dx = -1; dx <= 1; dx++) {
            for (int dz = -1; dz <= 1; dz++) {
                for (int y = 0; y < HEIGHT; y++) {
                    if (!replaceable(level.getBlockState(centre.offset(dx, y, dz)))) {
                        return false;
                    }
                }
            }
        }
        BlockPos door = centre.relative(facing, 2);
        if (!replaceable(level.getBlockState(door)) || !replaceable(level.getBlockState(door.above()))) {
            return false;
        }
        AABB trunk = new AABB(centre.getX() - 1, centre.getY(), centre.getZ() - 1, centre.getX() + 2, centre.getY() + HEIGHT,
                centre.getZ() + 2);
        return level.getEntitiesOfClass(LivingEntity.class, trunk).isEmpty();
    }

    /**
     * Grows the tree with its trunk centred on {@code centre} and its hollow facing {@code facing}. Blocks in the way of
     * the trunk are replaced; the crown only fills air. Returns the lower block of the hollow.
     */
    public static BlockPos grow(Level level, BlockPos centre, Direction facing, RandomSource random) {
        int flags = Block.UPDATE_CLIENTS | Block.UPDATE_KNOWN_SHAPE;
        BlockState log = Blocks.OAK_LOG.defaultBlockState();
        BlockState leaves = Blocks.OAK_LEAVES.defaultBlockState().setValue(LeavesBlock.PERSISTENT, true);
        BlockState soil = Blocks.ROOTED_DIRT.defaultBlockState();
        // Earth under the trunk and the doorstep, and the doorway cleared.
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                BlockPos ground = centre.offset(dx, -1, dz);
                if (Math.abs(dx) <= 1 && Math.abs(dz) <= 1 || !level.getBlockState(ground).isSolid()) {
                    level.setBlock(ground, soil, flags);
                }
            }
        }
        BlockPos step = centre.relative(facing, 2);
        level.setBlock(step.below(), Blocks.GRASS_BLOCK.defaultBlockState(), flags);
        level.setBlock(step, Blocks.AIR.defaultBlockState(), flags);
        level.setBlock(step.above(), Blocks.AIR.defaultBlockState(), flags);
        // The trunk.
        for (int dx = -1; dx <= 1; dx++) {
            for (int dz = -1; dz <= 1; dz++) {
                int height = HEIGHT - (Math.abs(dx) + Math.abs(dz) == 2 ? 2 : 0);
                for (int y = 0; y < height; y++) {
                    level.setBlock(centre.offset(dx, y, dz), log, flags);
                }
            }
        }
        // Roots spreading over the ground from the four sides, and down into it.
        for (Direction side : Direction.Plane.HORIZONTAL) {
            if (side == facing) {
                for (Direction around : new Direction[]{facing.getClockWise(), facing.getCounterClockWise()}) {
                    BlockPos root = centre.relative(facing).relative(around, 2);
                    placeIfFree(level, root, log, flags);
                }
                continue;
            }
            BlockState sideways = log.setValue(RotatedPillarBlock.AXIS, side.getAxis());
            int length = 2 + random.nextInt(2);
            for (int i = 2; i < 2 + length; i++) {
                placeIfFree(level, centre.relative(side, i), sideways, flags);
            }
            level.setBlock(centre.relative(side, 2).below(), soil, flags);
        }
        // Boughs and the crown.
        int crownY = centre.getY() + HEIGHT - 1;
        for (Direction side : Direction.Plane.HORIZONTAL) {
            BlockState bough = log.setValue(RotatedPillarBlock.AXIS, side.getAxis());
            for (int i = 2; i <= 3; i++) {
                level.setBlock(centre.relative(side, i).atY(crownY - 2 + i - 2), bough, flags);
            }
        }
        BlockPos crown = centre.atY(crownY + 1);
        for (int dx = -CROWN_RADIUS; dx <= CROWN_RADIUS; dx++) {
            for (int dz = -CROWN_RADIUS; dz <= CROWN_RADIUS; dz++) {
                for (int dy = -3; dy <= 3; dy++) {
                    double r = Math.sqrt(dx * dx + dz * dz + dy * dy * 2.2);
                    if (r <= CROWN_RADIUS + 0.3 - random.nextDouble() * 0.6) {
                        placeIfFree(level, crown.offset(dx, dy, dz), leaves, flags);
                    }
                }
            }
        }
        for (int y = 0; y <= 2; y++) {
            level.setBlock(crown.above(y - 1), log, flags);
        }
        // The hollow, last, so it never sees a missing wall.
        BlockPos hollow = centre.relative(facing);
        BlockState inside = SlavicContent.WORLD_TREE_HOLLOW.get().defaultBlockState().setValue(WorldTreeHollowBlock.FACING, facing);
        level.setBlock(hollow, inside, flags);
        level.setBlock(hollow.above(), inside, flags);
        return hollow;
    }

    private static void placeIfFree(Level level, BlockPos pos, BlockState state, int flags) {
        if (replaceable(level.getBlockState(pos)) && !level.getBlockState(pos).is(BlockTags.LOGS)) {
            level.setBlock(pos, state, flags);
        }
    }

    /** The lower block of the nearest World Tree hollow within {@link #SEARCH_RADIUS} blocks, or null. */
    @Nullable
    public static BlockPos find(ServerLevel level, BlockPos near) {
        BlockPos.MutableBlockPos cursor = new BlockPos.MutableBlockPos();
        BlockPos best = null;
        double bestDist = Double.MAX_VALUE;
        int minY = level.getMinBuildHeight();
        int maxY = minY + level.dimensionType().logicalHeight() - 1;
        Block hollow = SlavicContent.WORLD_TREE_HOLLOW.get();
        for (int dx = -SEARCH_RADIUS; dx <= SEARCH_RADIUS; dx++) {
            for (int dz = -SEARCH_RADIUS; dz <= SEARCH_RADIUS; dz++) {
                for (int y = minY; y <= maxY; y++) {
                    cursor.set(near.getX() + dx, y, near.getZ() + dz);
                    if (level.getBlockState(cursor).is(hollow) && !level.getBlockState(cursor.below()).is(hollow)) {
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

    /** The doorstep of a World Tree near {@code near}: an existing one, or a tree grown there on the surface. */
    public static Arrival findOrGrow(ServerLevel level, BlockPos near) {
        BlockPos hollow = find(level, near);
        if (hollow == null) {
            int x = near.getX();
            int z = near.getZ();
            int top = level.getMinBuildHeight() + level.dimensionType().logicalHeight();
            int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
            y = Math.max(level.getMinBuildHeight() + 2, Math.min(y, top - HEIGHT - CROWN_RADIUS - 2));
            hollow = grow(level, new BlockPos(x, y, z), Direction.SOUTH, level.getRandom());
        }
        Direction facing = level.getBlockState(hollow).getValue(WorldTreeHollowBlock.FACING);
        return new Arrival(hollow.relative(facing), facing);
    }
}
