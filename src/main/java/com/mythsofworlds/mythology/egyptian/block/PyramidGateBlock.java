package com.mythsofworlds.mythology.egyptian.block;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.Portal;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.level.portal.DimensionTransition;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * The gate of shadow in the doorway of a pyramid, two blocks high, facing out of it ({@link #FACING}). Stand inside
 * for three seconds to pass into the Duat, or out of it back to the Overworld. Break the pyramid stone beside or
 * behind it and the gate fades.
 */
public class PyramidGateBlock extends Block implements Portal {
    public static final DirectionProperty FACING = BlockStateProperties.HORIZONTAL_FACING;
    public static final BooleanProperty UPPER = BooleanProperty.create("upper");
    public static final int DELAY_TICKS = 60;

    public PyramidGateBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH).setValue(UPPER, false));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING, UPPER);
    }

    /** Which neighbours hold the gate: the stone behind it, beside the lower half, and the other half. */
    private static boolean holds(BlockState state, Direction direction, BlockState neighbour) {
        Direction facing = state.getValue(FACING);
        boolean upper = state.getValue(UPPER);
        if (direction == facing.getOpposite() || !upper && direction.getAxis() == facing.getClockWise().getAxis()) {
            return Pyramid.isStone(neighbour) || neighbour.getBlock() instanceof PyramidGateBlock;
        }
        if (direction == (upper ? Direction.DOWN : Direction.UP)) {
            return neighbour.getBlock() instanceof PyramidGateBlock;
        }
        return true;
    }

    @Override
    protected BlockState updateShape(BlockState state, Direction direction, BlockState neighborState,
                                     LevelAccessor level, BlockPos pos, BlockPos neighborPos) {
        if (!holds(state, direction, neighborState)) {
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
        ResourceKey<Level> targetKey = level.dimension() == EgyptianContent.DUAT ? Level.OVERWORLD : EgyptianContent.DUAT;
        ServerLevel target = level.getServer().getLevel(targetKey);
        if (target == null) {
            return null;
        }
        BlockPos near = target.getWorldBorder().clampToBounds(pos.getX(), pos.getY(), pos.getZ());
        Pyramid.Arrival arrival = Pyramid.findOrBuild(target, near);
        return new DimensionTransition(target, Vec3.atBottomCenterOf(arrival.pos()), Vec3.ZERO, arrival.facing().toYRot(),
                entity.getXRot(), DimensionTransition.PLAY_PORTAL_SOUND.then(arrived -> arrived.placePortalTicket(arrival.pos())));
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (random.nextInt(2) == 0) {
            level.addParticle(random.nextBoolean() ? ParticleTypes.SMOKE : ParticleTypes.ENCHANT,
                    pos.getX() + 0.2 + random.nextDouble() * 0.6, pos.getY() + random.nextDouble(),
                    pos.getZ() + 0.2 + random.nextDouble() * 0.6, 0.0, 0.02, 0.0);
        }
    }
}
