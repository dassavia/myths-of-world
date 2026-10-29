package com.mythsofworlds.mythology.greek.block;

import java.util.function.Supplier;
import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.phys.BlockHitResult;

/**
 * Leaves of a fruit tree (olive, pomegranate). Fruit ripens slowly (age 0 to 3); right-click ripe leaves to pick it,
 * like sweet berries. The leaves still decay when their tree is cut down.
 */
public class FruitLeavesBlock extends LeavesBlock {
    public static final IntegerProperty AGE = BlockStateProperties.AGE_3;
    public static final int RIPE = 3;

    private final Supplier<? extends ItemLike> fruit;

    public FruitLeavesBlock(Supplier<? extends ItemLike> fruit, Properties properties) {
        super(properties);
        this.fruit = fruit;
        registerDefaultState(defaultBlockState().setValue(AGE, 0));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        super.createBlockStateDefinition(builder);
        builder.add(AGE);
    }

    @Override
    protected boolean isRandomlyTicking(BlockState state) {
        return true;
    }

    @Override
    protected void randomTick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        super.randomTick(state, level, pos, random);
        BlockState now = level.getBlockState(pos);
        if (now.is(this) && now.getValue(AGE) < RIPE && random.nextInt(6) == 0) {
            level.setBlock(pos, now.setValue(AGE, now.getValue(AGE) + 1), Block.UPDATE_CLIENTS);
        }
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (state.getValue(AGE) < RIPE) {
            return InteractionResult.PASS;
        }
        if (!level.isClientSide) {
            popResource(level, pos, new ItemStack(fruit.get(), 1 + level.random.nextInt(2)));
            level.playSound(null, pos, SoundEvents.SWEET_BERRY_BUSH_PICK_BERRIES, SoundSource.BLOCKS, 1.0F,
                    0.8F + level.random.nextFloat() * 0.4F);
            level.setBlock(pos, state.setValue(AGE, 0), Block.UPDATE_CLIENTS);
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }
}
