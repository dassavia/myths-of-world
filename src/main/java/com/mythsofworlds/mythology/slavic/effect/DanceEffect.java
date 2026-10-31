package com.mythsofworlds.mythology.slavic.effect;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;

/**
 * The dance of the self-playing gusli: whoever hears them cannot help dancing. A dancing creature forgets whom it was
 * fighting, stops where it is, spins and hops in place until the music in its head dies away.
 */
public class DanceEffect extends MobEffect {
    public DanceEffect() {
        super(MobEffectCategory.HARMFUL, 0xE8B43C);
    }

    @Override
    public boolean shouldApplyEffectTickThisTick(int duration, int amplifier) {
        return true;
    }

    @Override
    public boolean applyEffectTick(LivingEntity entity, int amplifier) {
        if (entity instanceof Mob mob) {
            mob.setTarget(null);
            mob.getNavigation().stop();
            mob.setYRot(mob.getYRot() + 18.0F);
            mob.setYBodyRot(mob.getYRot());
            if (mob.onGround() && mob.tickCount % 10 == 0) {
                mob.getJumpControl().jump();
            }
        }
        return true;
    }
}
