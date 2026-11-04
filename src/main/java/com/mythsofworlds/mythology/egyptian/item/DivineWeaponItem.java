package com.mythsofworlds.mythology.egyptian.item;

import java.util.List;
import java.util.function.BiConsumer;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;

/**
 * A melee weapon forged from the relic of a god of Egypt: the flail of Osiris, the glaive of Anubis, the dagger of
 * Bastet, the khopesh of Sobek and the spear of Sekhmet. Each blow does what the god's myth does to the foe
 * ({@code onHit}, given the target and the attacker); the item properties set its damage and speed.
 */
public class DivineWeaponItem extends SwordItem {
    private final BiConsumer<LivingEntity, LivingEntity> onHit;

    public DivineWeaponItem(Tier tier, Properties properties, BiConsumer<LivingEntity, LivingEntity> onHit) {
        super(tier, properties);
        this.onHit = onHit;
    }

    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        if (!attacker.level().isClientSide) {
            onHit.accept(target, attacker);
        }
        return super.hurtEnemy(stack, target, attacker);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
