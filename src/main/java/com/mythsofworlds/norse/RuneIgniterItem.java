package com.mythsofworlds.norse;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;

import java.util.List;

/** Igniter for the Bifrost portal: right-click the inside of a runestone frame, like flint and steel on obsidian. */
public class RuneIgniterItem extends Item {
    public RuneIgniterItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos target = context.getClickedPos().relative(context.getClickedFace());
        if (level.isClientSide) {
            // Let the server decide; swing the arm only if it could plausibly be a frame.
            return BifrostPortalShape.findInterior(level, target, Direction.Axis.X) != null
                    || BifrostPortalShape.findInterior(level, target, Direction.Axis.Z) != null
                    ? InteractionResult.SUCCESS : InteractionResult.PASS;
        }
        if (!BifrostPortalShape.tryLight(level, target)) {
            return InteractionResult.PASS;
        }
        level.playSound(null, target, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 1.0F, 0.8F);
        if (context.getPlayer() != null) {
            context.getItemInHand().hurtAndBreak(1, context.getPlayer(), LivingEntity.getSlotForHand(context.getHand()));
        }
        return InteractionResult.CONSUME;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
