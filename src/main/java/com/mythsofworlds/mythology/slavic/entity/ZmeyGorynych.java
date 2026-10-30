package com.mythsofworlds.mythology.slavic.entity;

import com.mythsofworlds.core.entity.MythBoss;
import com.mythsofworlds.mythology.norse.entity.FireGiant;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
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
 * Zmey Gorynych, the three-headed dragon who guards the Kalinov bridge over the fiery river Smorodina. Each head
 * breathes fire: up close all three spit flame at once, from afar he hurls fireballs. Fire does not hurt him, and
 * while no one wounds him his heads heal the wounds of the body, {@link #REGEN} health a second. He drops the
 * sword-kladenets and his scales.
 */
public class ZmeyGorynych extends MythBoss {
    public static final int HEADS = 3;
    public static final float REGEN = 2.0F;
    public static final int CALM_TICKS = 100;

    private int breathCooldown = 60;
    private int fireballCooldown = 40;

    public ZmeyGorynych(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.RED, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 500.0)
                .add(Attributes.ATTACK_DAMAGE, 15.0)
                .add(Attributes.ATTACK_KNOCKBACK, 1.2)
                .add(Attributes.MOVEMENT_SPEED, 0.27)
                .add(Attributes.ARMOR, 14.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.FOLLOW_RANGE, 40.0)
                .add(Attributes.STEP_HEIGHT, 1.5);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit) {
            target.igniteForSeconds(5.0F);
        }
        return hit;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (!(level() instanceof ServerLevel server)) {
            return;
        }
        if (tickCount % 20 == 0 && getHealth() < getMaxHealth() && tickCount - getLastHurtByMobTimestamp() > CALM_TICKS) {
            heal(REGEN);
        }
        LivingEntity target = getTarget();
        if (target == null || !hasLineOfSight(target)) {
            return;
        }
        double distance = distanceToSqr(target);
        if (--breathCooldown <= 0 && distance < 12.0 * 12.0) {
            breathCooldown = enraged() ? 50 : 90;
            breathe(server, target);
        } else if (--fireballCooldown <= 0 && distance > 12.0 * 12.0 && distance < 40.0 * 40.0) {
            fireballCooldown = enraged() ? 30 : 60;
            FireGiant.throwFire(this, target);
        }
    }

    /** Three streams of fire, one from each head, fanned out towards the target. */
    public void breathe(ServerLevel server, LivingEntity target) {
        Vec3 aim = target.position().add(0.0, target.getBbHeight() * 0.5, 0.0).subtract(getX(), getY(0.8), getZ()).normalize();
        for (int head = 0; head < HEADS; head++) {
            double angle = (head - 1) * 0.25;
            Vec3 dir = new Vec3(aim.x * Math.cos(angle) - aim.z * Math.sin(angle), aim.y, aim.x * Math.sin(angle) + aim.z * Math.cos(angle));
            SmallFireball fireball = new SmallFireball(server, this, dir);
            fireball.setPos(getX() + dir.x * 2.0, getY(0.8), getZ() + dir.z * 2.0);
            server.addFreshEntity(fireball);
        }
        server.sendParticles(ParticleTypes.FLAME, getX() + aim.x * 2.0, getY(0.8), getZ() + aim.z * 2.0, 30, 0.6, 0.4, 0.6, 0.05);
        playSound(SoundEvents.ENDER_DRAGON_SHOOT, 2.0F, 0.6F);
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.ENDER_DRAGON_GROWL;
    }

    @Override
    protected float getSoundVolume() {
        return 1.5F;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.ENDER_DRAGON_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.ENDER_DRAGON_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.8F;
    }
}
