package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekSounds;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;

/**
 * A one-eyed giant shepherd like Polyphemus, mini-boss of the mountains and coast.
 * Neutral: it tends its sheep and ignores travellers until someone attacks it. Then it hits very hard,
 * and stomps the ground, hurting and tossing everyone nearby.
 */
public class Cyclops extends GreekBoss {
    private static final double STOMP_RADIUS = 5.0;

    private int stompCooldown = 60;

    public Cyclops(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.YELLOW, true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 220.0)
                .add(Attributes.ATTACK_DAMAGE, 16.0)
                .add(Attributes.ATTACK_KNOCKBACK, 2.0)
                .add(Attributes.MOVEMENT_SPEED, 0.25)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.FOLLOW_RANGE, 24.0)
                .add(Attributes.STEP_HEIGHT, 1.5);
    }

    @Override
    protected boolean hostile() {
        return false;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        LivingEntity target = getTarget();
        if (--stompCooldown <= 0) {
            stompCooldown = 20;
            if (target != null && onGround() && distanceToSqr(target) < STOMP_RADIUS * STOMP_RADIUS) {
                stomp();
                stompCooldown = 100;
            }
        }
    }

    private void stomp() {
        for (LivingEntity victim : level().getEntitiesOfClass(LivingEntity.class, getBoundingBox().inflate(STOMP_RADIUS),
                e -> e != this && !(e instanceof GreekBoss))) {
            victim.hurt(damageSources().mobAttack(this), 8.0F);
            victim.setDeltaMovement(victim.getDeltaMovement().add(0.0, 0.8, 0.0));
            victim.hurtMarked = true;
        }
        if (level() instanceof ServerLevel server) {
            server.sendParticles(ParticleTypes.EXPLOSION, getX(), getY() + 0.2, getZ(), 8, 2.0, 0.2, 2.0, 0.0);
        }
        playSound(GreekSounds.CYCLOPS_STOMP.get(), 2.0F, 1.0F);
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return GreekSounds.CYCLOPS_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return GreekSounds.CYCLOPS_HURT.get();
    }

    @Override
    protected SoundEvent getDeathSound() {
        return GreekSounds.CYCLOPS_DEATH.get();
    }

}
