package com.mythsofworlds.mythology.greek.entity;

import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.projectile.SmallFireball;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Cerberus, the three-headed hound guarding the Gates of Hades. Immune to fire; its bite sets the target
 * ablaze and every few seconds each head breathes a fireball.
 */
public class Cerberus extends GreekBoss {
    private int breathCooldown = 60;

    public Cerberus(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.PURPLE, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 350.0)
                .add(Attributes.ATTACK_DAMAGE, 12.0)
                .add(Attributes.MOVEMENT_SPEED, 0.32)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8)
                .add(Attributes.FOLLOW_RANGE, 32.0);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit) {
            target.igniteForSeconds(4.0F);
        }
        return hit;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        LivingEntity target = getTarget();
        if (--breathCooldown <= 0) {
            breathCooldown = 20;
            if (target != null && distanceToSqr(target) < 400.0 && hasLineOfSight(target)) {
                breathFire(target);
                breathCooldown = 70;
            }
        }
    }

    /** One fireball per head, slightly spread. */
    private void breathFire(LivingEntity target) {
        double dx = target.getX() - getX();
        double dy = target.getY(0.5) - getY(0.6);
        double dz = target.getZ() - getZ();
        Vec3 side = new Vec3(-dz, 0.0, dx).normalize();
        for (int head = -1; head <= 1; head++) {
            Vec3 direction = new Vec3(dx, dy, dz).normalize().add(side.scale(head * 0.12));
            SmallFireball fireball = new SmallFireball(level(), this, direction.normalize());
            fireball.setPos(getX() + side.x * head * 0.6, getY(0.6), getZ() + side.z * head * 0.6);
            level().addFreshEntity(fireball);
        }
        playSound(SoundEvents.BLAZE_SHOOT, 2.0F, 0.7F);
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
