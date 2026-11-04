package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Bastet, the cat-headed protector of homes, in her temple of Bubastis among her cats. Quick as a cat, she pounces
 * on her foe and her claws leave bleeding wounds; she always lands on her feet. She drops a claw of Bastet.
 */
public class BastetGod extends EgyptianGod {
    public BastetGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.PINK, EgyptianContent.DAGGER_OF_BASTET);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 340.0)
                .add(Attributes.ATTACK_DAMAGE, 10.0)
                .add(Attributes.MOVEMENT_SPEED, 0.4)
                .add(Attributes.ARMOR, 4.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.6)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected int powerInterval() {
        return 80;
    }

    /** The pounce: a leap onto the foe, claws that make them bleed (poison) and slow them. */
    @Override
    public void power(ServerLevel server, LivingEntity target) {
        Vec3 towards = target.position().subtract(position());
        if (towards.lengthSqr() > 1.0E-4) {
            towards = towards.multiply(1.0, 0.0, 1.0).normalize().scale(Math.min(1.4, Math.sqrt(distanceToSqr(target)) * 0.2));
            setDeltaMovement(towards.x, 0.5, towards.z);
            hurtMarked = true;
        }
        if (distanceToSqr(target) < 9.0) {
            target.hurt(damageSources().mobAttack(this), 6.0F);
            target.addEffect(new MobEffectInstance(MobEffects.POISON, 80, 1), this);
            target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1), this);
        }
        server.sendParticles(ParticleTypes.CRIT, getX(), getY(0.5), getZ(), 15, 0.4, 0.4, 0.4, 0.2);
        playSound(SoundEvents.CAT_HISS, 3.0F, 0.7F);
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, DamageSource source) {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.CAT_PURREOW;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.CAT_HURT;
    }

    @Override
    public float getVoicePitch() {
        return 0.8F;
    }
}
