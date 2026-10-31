package com.mythsofworlds.core;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.entity.BalancedBoss;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;

/**
 * Applies the boss settings of the server config to every {@link BalancedBoss}: {@code bossHealth} as a saved modifier of the boss's maximum health
 * (updated when the setting changes, keeping the share of health the boss has left), {@code bossDamage} to every hit
 * whose source is a boss, its fireballs and arrows included.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class BossBalance {
    public static final ResourceLocation HEALTH = MythsOfWorlds.id("config_boss_health");

    private BossBalance() {
    }

    @SubscribeEvent
    public static void onJoin(EntityJoinLevelEvent event) {
        if (!event.getLevel().isClientSide && event.getEntity() instanceof BalancedBoss && event.getEntity() instanceof LivingEntity boss) {
            scaleHealth(boss, ServerConfig.get(ServerConfig.BOSS_HEALTH));
        }
    }

    /** Sets the boss's maximum health to {@code multiplier} times its own, keeping how wounded it is. */
    public static void scaleHealth(LivingEntity boss, double multiplier) {
        AttributeInstance health = boss.getAttribute(Attributes.MAX_HEALTH);
        if (health == null) {
            return;
        }
        double wanted = multiplier - 1.0;
        AttributeModifier current = health.getModifier(HEALTH);
        if (Math.abs((current == null ? 0.0 : current.amount()) - wanted) < 1.0E-6) {
            return;
        }
        float share = boss.getHealth() / boss.getMaxHealth();
        health.removeModifier(HEALTH);
        if (Math.abs(wanted) > 1.0E-6) {
            health.addPermanentModifier(new AttributeModifier(HEALTH, wanted, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL));
        }
        boss.setHealth(boss.getMaxHealth() * share);
    }

    @SubscribeEvent
    public static void onDamage(LivingIncomingDamageEvent event) {
        if (event.getSource().getEntity() instanceof BalancedBoss) {
            double multiplier = ServerConfig.get(ServerConfig.BOSS_DAMAGE);
            if (multiplier != 1.0) {
                event.setAmount((float) (event.getAmount() * multiplier));
            }
        }
    }
}
