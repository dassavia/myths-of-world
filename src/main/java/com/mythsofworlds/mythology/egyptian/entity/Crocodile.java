package com.mythsofworlds.mythology.egyptian.entity;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.RandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.pathfinder.PathType;

/**
 * The crocodile of the Nile, sacred animal of Sobek: a long armoured lizard that lies in wait in the shallows and on
 * the banks. It swims as fast as it walks, holds its breath as long as it likes, and its scaly back turns light
 * blows. Its bite slows; in the water it drags its prey down in the death roll. Drops its hide and, sometimes, a
 * tooth.
 */
public class Crocodile extends Monster {
    public Crocodile(EntityType<? extends Monster> type, Level level) {
        super(type, level);
        setPathfindingMalus(PathType.WATER, 0.0F);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 30.0)
                .add(Attributes.ATTACK_DAMAGE, 6.0)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.MOVEMENT_SPEED, 0.24)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.5)
                .add(Attributes.FOLLOW_RANGE, 20.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.35, false));
        goalSelector.addGoal(7, new RandomStrollGoal(this, 0.6));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 10.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (isInWater()) {
            setDeltaMovement(getDeltaMovement().multiply(1.15, 1.0, 1.15));
        }
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1), this);
            if (isInWater() && living.isInWater()) {
                deathRoll(living);
            }
        }
        return hit;
    }

    /** The death roll: the prey is dragged under and its strength fails. */
    public void deathRoll(LivingEntity prey) {
        prey.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 3), this);
        prey.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0), this);
        prey.setDeltaMovement(prey.getDeltaMovement().multiply(0.3, 1.0, 0.3).add(0.0, -0.3, 0.0));
        prey.hurtMarked = true;
        if (level() instanceof ServerLevel server) {
            server.sendParticles(ParticleTypes.SPLASH, prey.getX(), prey.getY(0.6), prey.getZ(), 30, 0.5, 0.3, 0.5, 0.2);
        }
        playSound(SoundEvents.PLAYER_SPLASH, 1.2F, 0.6F);
    }

    @Override
    public boolean isPushedByFluid() {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.TURTLE_AMBIENT_LAND;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.TURTLE_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.TURTLE_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return super.getVoicePitch() * 0.5F;
    }
}
