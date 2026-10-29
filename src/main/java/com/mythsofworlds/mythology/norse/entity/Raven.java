package com.mythsofworlds.mythology.norse.entity;

import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.FollowMobGoal;
import net.minecraft.world.entity.ai.goal.FollowOwnerGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.PanicGoal;
import net.minecraft.world.entity.ai.goal.SitWhenOrderedToGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomFlyingGoal;
import net.minecraft.world.entity.animal.Parrot;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/**
 * Raven like Huginn and Muninn, Odin's thought and memory. Tame one with seeds like a parrot; it follows you
 * instead of riding on your shoulder, and its sharp eyes mark the monsters hiding around you with a glow.
 */
public class Raven extends Parrot {
    public static final double WATCH_RANGE = 20.0;

    public Raven(EntityType<? extends Parrot> type, Level level) {
        super(type, level);
    }

    /** The parrot's goals without landing on the owner's shoulder (the raven would vanish there). */
    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new PanicGoal(this, 1.25));
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(2, new SitWhenOrderedToGoal(this));
        goalSelector.addGoal(2, new FollowOwnerGoal(this, 1.0, 5.0F, 1.0F));
        goalSelector.addGoal(2, new WaterAvoidingRandomFlyingGoal(this, 1.0));
        goalSelector.addGoal(3, new FollowMobGoal(this, 1.0, 3.0F, 7.0F));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (!level().isClientSide && isTame() && tickCount % 100 == 0 && getOwner() instanceof Player owner
                && distanceToSqr(owner) < 32.0 * 32.0) {
            for (LivingEntity enemy : level().getEntitiesOfClass(LivingEntity.class, owner.getBoundingBox().inflate(WATCH_RANGE),
                    e -> e instanceof Enemy && e.isAlive())) {
                enemy.addEffect(new MobEffectInstance(MobEffects.GLOWING, 120, 0, false, false));
            }
        }
    }

    @Override
    public float getVoicePitch() {
        return 0.55F;
    }

    @Override
    public boolean canFreeze() {
        return false;
    }
}
