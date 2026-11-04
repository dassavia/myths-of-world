package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
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
 * Horus, the falcon-headed avenger, son of Isis and Osiris, in his temple with the falcon statues. He dives on his
 * foe like a falcon from the sky, and his eye, which sees everything, makes the foe glow and saps their strength.
 * Falls do not harm him. He drops a falcon feather of Horus.
 */
public class HorusGod extends EgyptianGod {
    public HorusGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.BLUE, EgyptianContent.BOW_OF_HORUS);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 420.0)
                .add(Attributes.ATTACK_DAMAGE, 13.0)
                .add(Attributes.MOVEMENT_SPEED, 0.34)
                .add(Attributes.ARMOR, 8.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8)
                .add(Attributes.FOLLOW_RANGE, 40.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected int powerInterval() {
        return 100;
    }

    /** The falcon's dive: a leap high towards the foe; the eye of Horus marks and weakens them. */
    @Override
    public void power(ServerLevel server, LivingEntity target) {
        Vec3 towards = target.position().subtract(position()).multiply(1.0, 0.0, 1.0);
        if (towards.lengthSqr() > 1.0E-4) {
            towards = towards.normalize().scale(Math.min(1.6, Math.sqrt(distanceToSqr(target)) * 0.18));
            setDeltaMovement(towards.x, 0.9, towards.z);
            hurtMarked = true;
        }
        target.addEffect(new MobEffectInstance(MobEffects.GLOWING, 160, 0), this);
        target.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0), this);
        server.sendParticles(ParticleTypes.END_ROD, getX(), getY(0.5), getZ(), 20, 0.4, 0.8, 0.4, 0.05);
        playSound(SoundEvents.PARROT_FLY, 3.0F, 0.5F);
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, DamageSource source) {
        return false;
    }

    @Override
    public float getVoicePitch() {
        return 1.1F;
    }
}
