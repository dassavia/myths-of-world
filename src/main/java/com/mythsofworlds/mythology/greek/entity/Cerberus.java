package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.GreekSounds;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.projectile.SmallFireball;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Cerberus, the three-headed hound guarding the Gates of Hades. Immune to fire; its bite sets the target
 * ablaze and every few seconds each head breathes a fireball. At half health it howls and calls three shades
 * of the dead to its side.
 */
public class Cerberus extends GreekBoss {
    private int breathCooldown = 60;
    private boolean summoned;

    public Cerberus(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.PURPLE, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 450.0)
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
        if (!summoned && enraged() && level() instanceof ServerLevel server) {
            summoned = true;
            summonShades(server);
        }
        LivingEntity target = getTarget();
        if (--breathCooldown <= 0) {
            breathCooldown = 20;
            if (target != null && distanceToSqr(target) < 400.0 && hasLineOfSight(target)) {
                breathFire(target);
                breathCooldown = 70;
            }
        }
    }

    private void summonShades(ServerLevel server) {
        for (int i = 0; i < 3; i++) {
            Shade shade = GreekEntities.SHADE.get().create(server);
            if (shade == null) {
                continue;
            }
            double angle = i * Math.PI * 2.0 / 3.0;
            shade.moveTo(getX() + Math.cos(angle) * 2.5, getY(), getZ() + Math.sin(angle) * 2.5, getYRot(), 0.0F);
            shade.finalizeSpawn(server, server.getCurrentDifficultyAt(shade.blockPosition()), MobSpawnType.MOB_SUMMONED, null);
            shade.setTarget(getTarget());
            server.addFreshEntity(shade);
            server.sendParticles(ParticleTypes.SOUL, shade.getX(), shade.getY() + 1.0, shade.getZ(), 12, 0.3, 0.6, 0.3, 0.02);
        }
        playSound(GreekSounds.CERBERUS_AMBIENT.get(), 3.0F, 0.6F);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("SummonedShades", summoned);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        summoned = tag.getBoolean("SummonedShades");
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
        playSound(GreekSounds.CERBERUS_BREATH.get(), 2.0F, 1.0F);
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return GreekSounds.CERBERUS_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return GreekSounds.CERBERUS_HURT.get();
    }

    @Override
    protected SoundEvent getDeathSound() {
        return GreekSounds.CERBERUS_DEATH.get();
    }

}
