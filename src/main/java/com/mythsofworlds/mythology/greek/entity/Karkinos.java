package com.mythsofworlds.mythology.greek.entity;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
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
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.level.Level;

/**
 * Karkinos, the giant crab Hera sent to help the Hydra: it pinched Heracles by the heel while he fought the
 * monster, so he needed Iolaus to win. Guards the Hydra's lair. Its pinch holds the victim in place; its shell
 * turns arrows. Heracles crushed it under his foot: a blow struck while falling (a jump attack) does double damage.
 * A small crab at the hero's heel, so it has no health bar.
 */
public class Karkinos extends GreekBoss {
    public Karkinos(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.RED, true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 40.0)
                .add(Attributes.ATTACK_DAMAGE, 5.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.ARMOR_TOUGHNESS, 4.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8)
                .add(Attributes.FOLLOW_RANGE, 24.0);
    }

    @Override
    protected boolean hasBossBar() {
        return false;
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (source.getDirectEntity() instanceof Projectile) {
            amount *= 0.5F;
        } else if (source.isDirect() && source.getEntity() instanceof Player player && player.fallDistance > 0.0F
                && !player.onGround()) {
            amount *= 2.0F;
        }
        return super.hurt(source, amount);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            // The pinch: the victim cannot get away for a moment.
            living.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 5), this);
        }
        return hit;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.TURTLE_AMBIENT_LAND;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.TURTLE_SHAMBLE;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.TURTLE_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.6F;
    }
}
