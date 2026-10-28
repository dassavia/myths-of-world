package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekSounds;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
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
 * Translucent ghost of the dead from the Asphodel Meadows. Its touch drains strength and dims the light, and it
 * feeds on the life it takes. Running is no use: a shade blinks through the mist to appear beside its prey.
 */
public class Shade extends Monster {
    private int blinkCooldown = 100;

    public Shade(EntityType<? extends Monster> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 22.0)
                .add(Attributes.ATTACK_DAMAGE, 3.0)
                .add(Attributes.MOVEMENT_SPEED, 0.26)
                .add(Attributes.FOLLOW_RANGE, 24.0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.0, false));
        goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 0.8));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0), this);
            living.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 80, 0), this);
            heal(2.0F);
        }
        return hit;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        LivingEntity target = getTarget();
        if (--blinkCooldown > 0 || target == null) {
            return;
        }
        blinkCooldown = 40;
        if (distanceToSqr(target) > 64.0 && distanceToSqr(target) < 900.0) {
            blinkTo(target);
            blinkCooldown = 140;
        }
    }

    /** Teleports to a random spot 2-4 blocks from the target. */
    private void blinkTo(LivingEntity target) {
        double fromX = getX();
        double fromY = getY();
        double fromZ = getZ();
        for (int attempt = 0; attempt < 8; attempt++) {
            double angle = random.nextDouble() * Math.PI * 2.0;
            double distance = 2.0 + random.nextDouble() * 2.0;
            if (randomTeleport(target.getX() + Math.cos(angle) * distance, target.getY(),
                    target.getZ() + Math.sin(angle) * distance, false)) {
                if (level() instanceof ServerLevel server) {
                    server.sendParticles(ParticleTypes.SOUL, fromX, fromY + 1.0, fromZ, 10, 0.3, 0.6, 0.3, 0.02);
                    server.sendParticles(ParticleTypes.SOUL, getX(), getY() + 1.0, getZ(), 10, 0.3, 0.6, 0.3, 0.02);
                }
                playSound(GreekSounds.SHADE_TELEPORT.get(), 1.0F, 1.0F);
                return;
            }
        }
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, DamageSource source) {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return GreekSounds.SHADE_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return GreekSounds.SHADE_HURT.get();
    }

    @Override
    protected SoundEvent getDeathSound() {
        return GreekSounds.SHADE_DEATH.get();
    }
}
