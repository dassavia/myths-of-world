package com.mythsofworlds.mythology.greek.portal;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * Bronze bowl on a marble foot. Placed on the four corners of a sacred pool and lit with the Promethean Torch,
 * it opens the way to Hellas (see {@link PoolPortal}). Right-click with an empty hand to put the fire out.
 */
public class BrazierBlock extends Block {
    public static final BooleanProperty LIT = BlockStateProperties.LIT;

    private static final VoxelShape SHAPE = Shapes.or(
            Block.box(5.0, 0.0, 5.0, 11.0, 6.0, 11.0),
            Block.box(2.0, 6.0, 2.0, 14.0, 10.0, 14.0));

    public BrazierBlock(Properties properties) {
        super(properties);
        registerDefaultState(stateDefinition.any().setValue(LIT, false));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(LIT);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPE;
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!state.getValue(LIT)) {
            return InteractionResult.PASS;
        }
        if (!level.isClientSide) {
            level.setBlock(pos, state.setValue(LIT, false), Block.UPDATE_ALL);
            level.playSound(null, pos, SoundEvents.FIRE_EXTINGUISH, SoundSource.BLOCKS, 0.8F, 1.0F);
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    /** A pool portal closes as soon as one of its fires goes out or its brazier is removed. */
    @Override
    protected void onRemove(BlockState state, Level level, BlockPos pos, BlockState newState, boolean movedByPiston) {
        boolean stillLit = newState.is(this) && newState.getValue(LIT);
        if (state.getValue(LIT) && !stillLit) {
            PoolPortal.collapseAround(level, pos);
        }
        super.onRemove(state, level, pos, newState, movedByPiston);
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (!state.getValue(LIT)) {
            return;
        }
        double x = pos.getX() + 0.5;
        double y = pos.getY() + 0.7;
        double z = pos.getZ() + 0.5;
        level.addParticle(ParticleTypes.FLAME, x + (random.nextDouble() - 0.5) * 0.4, y, z + (random.nextDouble() - 0.5) * 0.4,
                0.0, 0.03, 0.0);
        if (random.nextInt(4) == 0) {
            level.addParticle(ParticleTypes.SMOKE, x, y + 0.3, z, 0.0, 0.05, 0.0);
        }
        if (random.nextInt(10) == 0) {
            level.playLocalSound(x, y, z, SoundEvents.FIRE_AMBIENT, SoundSource.BLOCKS, 0.6F, 1.0F, false);
        }
    }
}
