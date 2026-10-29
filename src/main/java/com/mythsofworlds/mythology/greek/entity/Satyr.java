package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekSounds;
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
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/**
 * Goat-legged wild man of the groves of Arcadia, follower of Pan and Dionysus. By day it only plays its pan flute;
 * at night, drunk on Dionysus' wine, it attacks travellers. In a fight its flute rallies nearby satyrs (Speed),
 * and its headbutt leaves you dizzy (Nausea).
 */
public class Satyr extends Monster {
    private int fluteCooldown = 100;

    public Satyr(EntityType<? extends Monster> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 24.0)
                .add(Attributes.ATTACK_DAMAGE, 4.0)
                .add(Attributes.MOVEMENT_SPEED, 0.33)
                .add(Attributes.FOLLOW_RANGE, 24.0)
                .add(Attributes.JUMP_STRENGTH, 0.6);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.1, false));
        goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 1.0));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers());
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, 10, true, false, p -> !level().isDay()));
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (--fluteCooldown > 0) {
            return;
        }
        LivingEntity target = getTarget();
        fluteCooldown = target != null ? 160 : 400 + random.nextInt(400);
        playSound(GreekSounds.PAN_FLUTE.get(), 1.5F, 0.9F + random.nextFloat() * 0.2F);
        if (target != null) {
            for (Satyr satyr : level().getEntitiesOfClass(Satyr.class, getBoundingBox().inflate(12.0))) {
                satyr.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 120, 1));
                if (satyr.getTarget() == null) {
                    satyr.setTarget(target);
                }
            }
        }
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living && random.nextInt(3) == 0) {
            living.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 140, 0), this);
        }
        return hit;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return GreekSounds.SATYR_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.GOAT_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.GOAT_DEATH;
    }
}
