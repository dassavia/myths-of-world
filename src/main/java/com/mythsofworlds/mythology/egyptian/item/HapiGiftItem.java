package com.mythsofworlds.mythology.egyptian.item;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.BonemealableBlock;
import net.minecraft.world.level.block.state.BlockState;

/**
 * The gift of Hapi, god of the flood of the Nile: black silt mixed with bone meal, the strongest of fertilisers.
 * Used on a block, it feeds every plant (crops, saplings, cane, not grass blocks) within {@link #RADIUS} blocks around it (and one block up and down)
 * {@link #ROUNDS} times over, as the flood once made the fields of Egypt the richest in the world.
 */
public class HapiGiftItem extends Item {
    public static final int RADIUS = 2;
    public static final int ROUNDS = 3;
    /** The level event of bone meal: green sparkles and the sound of growth. */
    private static final int PLANT_GROWTH_EVENT = 1505;

    public HapiGiftItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos centre = context.getClickedPos();
        if (!(level instanceof ServerLevel server)) {
            return InteractionResult.SUCCESS;
        }
        int fed = flood(server, centre);
        if (fed == 0) {
            return InteractionResult.PASS;
        }
        Player player = context.getPlayer();
        if (player == null || !player.getAbilities().instabuild) {
            context.getItemInHand().shrink(1);
        }
        server.playSound(null, centre, SoundEvents.BONE_MEAL_USE, SoundSource.BLOCKS, 1.0F, 0.8F);
        return InteractionResult.CONSUME;
    }

    /** Feeds the plants around {@code centre}; returns how many plants could be fed. */
    public static int flood(ServerLevel level, BlockPos centre) {
        int fed = 0;
        for (BlockPos pos : BlockPos.betweenClosed(centre.offset(-RADIUS, -1, -RADIUS), centre.offset(RADIUS, 1, RADIUS))) {
            BlockPos at = pos.immutable();
            boolean grew = false;
            for (int round = 0; round < ROUNDS; round++) {
                BlockState state = level.getBlockState(at);
                // Plants only: grass and moss blocks would cover the field with weeds.
                if (!state.isSolidRender(level, at) && state.getBlock() instanceof BonemealableBlock plant
                        && plant.isValidBonemealTarget(level, at, state)) {
                    if (plant.isBonemealSuccess(level, level.getRandom(), at, state)) {
                        plant.performBonemeal(level, level.getRandom(), at, state);
                    }
                    grew = true;
                }
            }
            if (grew) {
                level.levelEvent(PLANT_GROWTH_EVENT, at, 15);
                fed++;
            }
        }
        return fed;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
