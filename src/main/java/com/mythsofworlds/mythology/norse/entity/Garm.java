package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/**
 * Garm, the blood-stained hound chained before Hel's gate in the mists of Niflheim. Mini-boss. His howl casts the
 * darkness of Hel over everyone nearby, and his bite brings the chill of the dead. A creature of the cold mists, he
 * dreads fire: while he burns, every blow hurts him twice as much.
 */
public class Garm extends GreekBoss {
    public static final double HOWL_RANGE = 16.0;

    private int howlCooldown = 100;

    public Garm(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.WHITE, true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 220.0)
                .add(Attributes.ATTACK_DAMAGE, 12.0)
                .add(Attributes.MOVEMENT_SPEED, 0.33)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8)
                .add(Attributes.FOLLOW_RANGE, 32.0);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0), this);
            FrostGiant.chill(living, this, 2);
        }
        return hit;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (getTarget() != null && --howlCooldown <= 0 && level() instanceof ServerLevel server) {
            howlCooldown = enraged() ? 160 : 240;
            howl(server);
        }
    }

    public void howl(ServerLevel server) {
        for (Player player : server.getEntitiesOfClass(Player.class, getBoundingBox().inflate(HOWL_RANGE),
                p -> !p.isCreative() && !p.isSpectator())) {
            player.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 140, 0), this);
            player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 80, 1), this);
        }
        server.sendParticles(ParticleTypes.SCULK_SOUL, getX(), getY() + 1.5, getZ(), 20, 1.0, 0.6, 1.0, 0.02);
        playSound(SoundEvents.WOLF_HOWL, 4.0F, 0.4F);
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (isOnFire() || source.is(DamageTypeTags.IS_FIRE)) {
            amount *= 2.0F;
        }
        return super.hurt(source, amount);
    }

    @Override
    public boolean canFreeze() {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.WOLF_GROWL;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.WOLF_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.WOLF_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.5F;
    }
}
