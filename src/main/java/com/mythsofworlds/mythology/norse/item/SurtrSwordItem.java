package com.mythsofworlds.mythology.norse.item;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.item.TooltipFlag;

/** The sword that will set the world on fire at Ragnarok: every hit sets the target ablaze. */
public class SurtrSwordItem extends SwordItem {
    public static final float BURN_SECONDS = 6.0F;

    public SurtrSwordItem(Properties properties) {
        super(com.mythsofworlds.mythology.norse.NorseContent.DARK_IRON.tier, properties);
    }

    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        target.igniteForSeconds(BURN_SECONDS);
        return super.hurtEnemy(stack, target, attacker);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
