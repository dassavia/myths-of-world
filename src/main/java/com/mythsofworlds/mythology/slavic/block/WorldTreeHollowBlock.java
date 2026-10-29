package com.mythsofworlds.mythology.slavic.block;

import com.mythsofworlds.mythology.slavic.SlavicContent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
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
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.level.portal.DimensionTransition;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * The dark hollow at the roots of the World Tree, two blocks high, opening towards {@link #FACING}. Step inside and
 * wait three seconds to go down the roots to Nav, or up them back to the Overworld. Cut away the trunk around it and
 * the hollow closes.
 */
public class WorldTreeHollowBlock extends Block implements Portal {
    public static final DirectionProperty FACING = BlockStateProperties.HORIZONTAL_FACING;
    public static final int DELAY_TICKS = 60;

    public WorldTreeHollowBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(FACING, Direction.NORTH));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING);
    }

    /** The trunk must stand on both sides, behind and above; the front stays open. */
    public static boolean isWall(BlockState state) {
        return state.is(BlockTags.LOGS) || state.getBlock() instanceof WorldTreeHollowBlock;
    }

    @Override
    protected BlockState updateShape(BlockState state, Direction direction, BlockState neighborState,
                                     LevelAccessor level, BlockPos pos, BlockPos neighborPos) {
        if (direction != state.getValue(FACING) && direction != Direction.DOWN && !isWall(neighborState)) {
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
        ResourceKey<Level> targetKey = level.dimension() == SlavicContent.NAV ? Level.OVERWORLD : SlavicContent.NAV;
        ServerLevel target = level.getServer().getLevel(targetKey);
        if (target == null) {
            return null;
        }
        BlockPos near = target.getWorldBorder().clampToBounds(pos.getX(), pos.getY(), pos.getZ());
        WorldTree.Arrival arrival = WorldTree.findOrGrow(target, near);
        return new DimensionTransition(target, Vec3.atBottomCenterOf(arrival.pos()), Vec3.ZERO, arrival.facing().toYRot(),
                entity.getXRot(), DimensionTransition.PLAY_PORTAL_SOUND.then(arrived -> arrived.placePortalTicket(arrival.pos())));
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (random.nextInt(3) == 0) {
            level.addParticle(ParticleTypes.SOUL, pos.getX() + 0.2 + random.nextDouble() * 0.6, pos.getY() + random.nextDouble(),
                    pos.getZ() + 0.2 + random.nextDouble() * 0.6, 0.0, 0.03, 0.0);
        }
    }
}
