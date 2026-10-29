package com.mythsofworlds.mythology.norse.item;

import com.mythsofworlds.mythology.norse.entity.Fenrir;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/**
 * The ribbon the dwarves made from the sound of a cat's footfall, the roots of a mountain and the breath of a fish.
 * Use it on Fenrir to bind him: for a while he cannot move or bite and takes more damage.
 */
public class GleipnirItem extends Item {
    public GleipnirItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult interactLivingEntity(ItemStack stack, Player player, LivingEntity target, InteractionHand hand) {
        if (!(target instanceof Fenrir fenrir)) {
            return InteractionResult.PASS;
        }
        if (!player.level().isClientSide) {
            if (!fenrir.bind()) {
                player.displayClientMessage(Component.translatable("item.mythsofworlds.gleipnir.too_soon"), true);
                return InteractionResult.FAIL;
            }
            stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
        }
        return InteractionResult.sidedSuccess(player.level().isClientSide);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
