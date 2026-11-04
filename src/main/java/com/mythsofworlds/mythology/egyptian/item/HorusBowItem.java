package com.mythsofworlds.mythology.egyptian.item;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.AbstractArrow;
import net.minecraft.world.entity.projectile.Arrow;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.item.BowItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * The bow of Horus, strung with the falcon feathers of the sky god: its arrows strike {@link #EXTRA_DAMAGE} harder,
 * and the eye of Horus marks whoever they hit, so that they glow through walls for {@link #GLOW_TICKS} ticks.
 */
public class HorusBowItem extends BowItem {
    public static final double EXTRA_DAMAGE = 2.5;
    public static final int GLOW_TICKS = 200;

    public HorusBowItem(Properties properties) {
        super(properties);
    }

    @Override
    protected Projectile createProjectile(Level level, LivingEntity shooter, ItemStack weapon, ItemStack ammo, boolean isCrit) {
        Projectile projectile = super.createProjectile(level, shooter, weapon, ammo, isCrit);
        if (projectile instanceof AbstractArrow arrow) {
            arrow.setBaseDamage(arrow.getBaseDamage() + EXTRA_DAMAGE);
        }
        if (projectile instanceof Arrow plain) {
            plain.addEffect(new MobEffectInstance(MobEffects.GLOWING, GLOW_TICKS, 0));
        }
        return projectile;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
