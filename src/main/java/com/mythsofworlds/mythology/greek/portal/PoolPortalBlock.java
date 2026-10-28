package com.mythsofworlds.mythology.greek.portal;

import com.mythsofworlds.mythology.greek.GreekContent;
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
import net.minecraft.world.level.portal.DimensionTransition;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;
import org.jetbrains.annotations.Nullable;

/**
 * Golden surface of a sacred pool, made when the four braziers around a pool of water are lit.
 * Step into it and wait three seconds to travel between the Overworld and Hellas.
 */
public class PoolPortalBlock extends Block implements Portal {
    private static final VoxelShape SHAPE = Block.box(0.0, 0.0, 0.0, 16.0, 12.0, 16.0);
    public static final int DELAY_TICKS = 60;

    public PoolPortalBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPE;
    }

    /** Turns back into water when the marble rim around it is broken. */
    @Override
    protected BlockState updateShape(BlockState state, Direction direction, BlockState neighborState,
                                     LevelAccessor level, BlockPos pos, BlockPos neighborPos) {
        if (direction.getAxis().isHorizontal() && !neighborState.is(this) && !neighborState.is(GreekContent.OLYMPIAN_MARBLE.get())) {
            return Blocks.WATER.defaultBlockState();
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
            return player.getAbilities().invulnerable ? 1 : DELAY_TICKS;
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
        ResourceKey<Level> targetKey = level.dimension() == GreekContent.HELLAS ? Level.OVERWORLD : GreekContent.HELLAS;
        ServerLevel target = level.getServer().getLevel(targetKey);
        if (target == null) {
            return null;
        }
        BlockPos near = target.getWorldBorder().clampToBounds(pos.getX(), pos.getY(), pos.getZ());
        BlockPos arrival = PoolPortal.findOrCreate(target, near);
        return new DimensionTransition(target, Vec3.atBottomCenterOf(arrival), Vec3.ZERO, entity.getYRot(), entity.getXRot(),
                DimensionTransition.PLAY_PORTAL_SOUND.then(arrived -> arrived.placePortalTicket(arrival)));
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (random.nextInt(4) == 0) {
            level.addParticle(ParticleTypes.END_ROD, pos.getX() + random.nextDouble(), pos.getY() + 0.8,
                    pos.getZ() + random.nextDouble(), 0.0, 0.04, 0.0);
        }
    }
}
