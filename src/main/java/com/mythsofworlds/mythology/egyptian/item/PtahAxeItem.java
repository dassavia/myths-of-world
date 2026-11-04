package com.mythsofworlds.mythology.egyptian.item;

import com.mythsofworlds.mythology.relic.RelicArmorItem;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * The battle-axe of Ptah, the craftsman god, with his chisel set in the blade: a heavy axe of meteoric iron that
 * fells trees and foes alike, and while it is in hand the skill of the maker of the world is yours (Haste II).
 */
public class PtahAxeItem extends AxeItem {
    public PtahAxeItem(Tier tier, Properties properties) {
        super(tier, properties);
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slotId, boolean isSelected) {
        super.inventoryTick(stack, level, entity, slotId, isSelected);
        if (!level.isClientSide && isSelected && entity instanceof Player player && player.tickCount % 20 == 0) {
            RelicArmorItem.keep(player, MobEffects.DIG_SPEED, 1);
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
