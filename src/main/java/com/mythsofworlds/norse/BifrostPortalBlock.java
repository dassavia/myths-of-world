package com.mythsofworlds.norse;

import com.mythsofworlds.registry.ModBlocks;
import com.mythsofworlds.world.ModDimensions;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Portal;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.portal.DimensionTransition;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;
import org.jetbrains.annotations.Nullable;

/** Shimmering Bifrost surface. Standing in it carries you between the Overworld and Jotunheim. */
public class BifrostPortalBlock extends Block implements Portal {
    public static final EnumProperty<Direction.Axis> AXIS = BlockStateProperties.HORIZONTAL_AXIS;
    /** How far around the arrival point we look for an existing portal before building a new one. */
    public static final int SEARCH_RADIUS = 16;

    private static final VoxelShape X_SHAPE = Block.box(0.0, 0.0, 6.0, 16.0, 16.0, 10.0);
    private static final VoxelShape Z_SHAPE = Block.box(6.0, 0.0, 0.0, 10.0, 16.0, 16.0);

    public BifrostPortalBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(AXIS, Direction.Axis.X));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(AXIS);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return state.getValue(AXIS) == Direction.Axis.Z ? Z_SHAPE : X_SHAPE;
    }

    /** The portal collapses as soon as its frame (or a neighbouring portal block) in its plane is removed. */
    @Override
    protected BlockState updateShape(BlockState state, Direction direction, BlockState neighborState,
                                     LevelAccessor level, BlockPos pos, BlockPos neighborPos) {
        Direction.Axis axis = state.getValue(AXIS);
        boolean inPlane = direction.getAxis() == Direction.Axis.Y || direction.getAxis() == axis;
        if (inPlane && !neighborState.is(this) && !neighborState.is(ModBlocks.RUNESTONE.get())) {
            return Blocks.AIR.defaultBlockState();
        }
        return super.updateShape(state, direction, neighborState, level, pos, neighborPos);
    }

    @Override
    protected void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
        if (entity.canUsePortal(false)) {
            entity.setAsInsidePortal(this, pos);
        }
    }

    @Override
    public int getPortalTransitionTime(ServerLevel level, Entity entity) {
        if (entity instanceof Player player) {
            return player.getAbilities().invulnerable ? 1 : 60;
        }
        return 0;
    }

    @Override
    public Portal.Transition getLocalTransition() {
        return Portal.Transition.CONFUSION;
    }

    @Nullable
    @Override
    public DimensionTransition getPortalDestination(ServerLevel level, Entity entity, BlockPos pos) {
        ResourceKey<Level> targetKey = level.dimension() == ModDimensions.JOTUNHEIM ? Level.OVERWORLD : ModDimensions.JOTUNHEIM;
        ServerLevel target = level.getServer().getLevel(targetKey);
        if (target == null) {
            return null;
        }
        BlockPos arrival = findOrCreatePortal(target, target.getWorldBorder().clampToBounds(pos.getX(), pos.getY(), pos.getZ()));
        Vec3 spot = Vec3.atBottomCenterOf(arrival);
        return new DimensionTransition(target, spot, Vec3.ZERO, entity.getYRot(), entity.getXRot(),
                DimensionTransition.PLAY_PORTAL_SOUND.then(arrived -> arrived.placePortalTicket(arrival)));
    }

    /** Returns the bottom block of a Bifrost portal near {@code near} in {@code level}, building one if none exists. */
    public static BlockPos findOrCreatePortal(ServerLevel level, BlockPos near) {
        BlockPos existing = findPortal(level, near);
        return existing != null ? existing : buildPortal(level, near);
    }

    @Nullable
    public static BlockPos findPortal(ServerLevel level, BlockPos near) {
        Block portal = ModBlocks.BIFROST_PORTAL.get();
        BlockPos.MutableBlockPos cursor = new BlockPos.MutableBlockPos();
        BlockPos best = null;
        double bestDist = Double.MAX_VALUE;
        int minY = level.getMinBuildHeight();
        int maxY = level.getMinBuildHeight() + level.dimensionType().logicalHeight() - 1;
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
        return best;
    }

    /** Builds a 2x3 portal in a runestone frame on the surface, with a small platform on both sides. */
    public static BlockPos buildPortal(ServerLevel level, BlockPos near) {
        int x = near.getX();
        int z = near.getZ();
        int top = level.getMinBuildHeight() + level.dimensionType().logicalHeight();
        int y = level.getHeight(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, x, z);
        y = Math.max(level.getMinBuildHeight() + 2, Math.min(y, top - 6));
        BlockPos base = new BlockPos(x, y, z);

        BlockState frame = ModBlocks.RUNESTONE.get().defaultBlockState();
        BlockState portal = ModBlocks.BIFROST_PORTAL.get().defaultBlockState().setValue(AXIS, Direction.Axis.X);
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
                boolean edge = i == -1 || i == 2 || j == -1 || j == 3;
                if (edge) {
                    level.setBlock(base.offset(i, j, 0), frame, flags);
                }
            }
        }
        for (int i = 0; i <= 1; i++) {
            for (int j = 0; j <= 2; j++) {
                level.setBlock(base.offset(i, j, 0), portal, flags);
            }
        }
        return base;
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (random.nextInt(3) == 0) {
            double px = pos.getX() + random.nextDouble();
            double py = pos.getY() + random.nextDouble();
            double pz = pos.getZ() + random.nextDouble();
            level.addParticle(ParticleTypes.SNOWFLAKE, px, py, pz, 0.0, 0.02, 0.0);
        }
        if (random.nextInt(8) == 0) {
            level.addParticle(ParticleTypes.END_ROD, pos.getX() + random.nextDouble(), pos.getY() + random.nextDouble(),
                    pos.getZ() + random.nextDouble(), 0.0, 0.01, 0.0);
        }
    }
}
