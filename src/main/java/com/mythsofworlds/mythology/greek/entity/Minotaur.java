package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.GreekSounds;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Boss of the Labyrinth. Besides normal blows it charges: lowers its horns and rushes at a player
 * 5-18 blocks away, throwing them back. Hitting a wall ends the charge. Below half health it is enraged:
 * faster, and it charges twice as often.
 */
public class Minotaur extends GreekBoss {
    private static final int CHARGE_TICKS = 20;
    private static final int CHARGE_COOLDOWN = 120;
    private static final AttributeModifier ENRAGED_SPEED = new AttributeModifier(MythsOfWorlds.id("enraged"), 0.3,
            AttributeModifier.Operation.ADD_MULTIPLIED_BASE);

    private int chargeCooldown = 60;
    private int chargeTicks;
    private Vec3 chargeDirection = Vec3.ZERO;

    public Minotaur(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.RED, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 300.0)
                .add(Attributes.ATTACK_DAMAGE, 14.0)
                .add(Attributes.ATTACK_KNOCKBACK, 1.5)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.9)
                .add(Attributes.FOLLOW_RANGE, 32.0);
    }

    public boolean isCharging() {
        return chargeTicks > 0;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (enraged() && !getAttribute(Attributes.MOVEMENT_SPEED).hasModifier(ENRAGED_SPEED.id())) {
            getAttribute(Attributes.MOVEMENT_SPEED).addTransientModifier(ENRAGED_SPEED);
            playSound(GreekSounds.MINOTAUR_ROAR.get(), 3.0F, 0.7F);
        }
        LivingEntity target = getTarget();
        if (chargeTicks > 0) {
            chargeTicks--;
            setDeltaMovement(chargeDirection.x * 0.9, getDeltaMovement().y, chargeDirection.z * 0.9);
            if (target != null && getBoundingBox().inflate(0.6).intersects(target.getBoundingBox())) {
                target.hurt(damageSources().mobAttack(this), (float) getAttributeValue(Attributes.ATTACK_DAMAGE) * 1.5F);
                target.knockback(2.5, -chargeDirection.x, -chargeDirection.z);
                target.hurtMarked = true;
                chargeTicks = 0;
            } else if (horizontalCollision) {
                chargeTicks = 0;
            }
        } else if (--chargeCooldown <= 0) {
            chargeCooldown = 20;
            if (target != null && onGround() && hasLineOfSight(target)) {
                double distance = distanceTo(target);
                if (distance > 5.0 && distance < 18.0) {
                    chargeDirection = new Vec3(target.getX() - getX(), 0.0, target.getZ() - getZ()).normalize();
                    chargeTicks = CHARGE_TICKS;
                    chargeCooldown = enraged() ? CHARGE_COOLDOWN / 2 : CHARGE_COOLDOWN;
                    getNavigation().stop();
                    playSound(GreekSounds.MINOTAUR_ROAR.get(), 2.0F, 1.0F);
                }
            }
        }
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return GreekSounds.MINOTAUR_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return GreekSounds.MINOTAUR_HURT.get();
    }

    @Override
    protected SoundEvent getDeathSound() {
        return GreekSounds.MINOTAUR_DEATH.get();
    }
}
