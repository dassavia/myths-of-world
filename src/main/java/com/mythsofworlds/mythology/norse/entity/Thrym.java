package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import com.mythsofworlds.mythology.norse.NorseEntities;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Thrym, king of the frost giants, on his throne in Utgard. He stole Thor's hammer and keeps it until someone takes it
 * back. Breathes a cone of frost that freezes everyone in front of him, stamps the ice, and at half health calls two
 * frost giants of his court. Fire hurts him twice as much.
 */
public class Thrym extends GreekBoss {
    public static final double BREATH_RANGE = 10.0;
    public static final double STOMP_RADIUS = 5.0;

    private int breathCooldown = 80;
    private int stompCooldown = 120;
    private boolean summoned;

    public Thrym(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.BLUE, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 450.0)
                .add(Attributes.ATTACK_DAMAGE, 17.0)
                .add(Attributes.ATTACK_KNOCKBACK, 2.0)
                .add(Attributes.MOVEMENT_SPEED, 0.25)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.5);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            FrostGiant.chill(living, this, 4);
        }
        return hit;
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (source.is(DamageTypeTags.IS_FIRE)) {
            amount *= 2.0F;
        }
        return super.hurt(source, amount);
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (!(level() instanceof ServerLevel server)) {
            return;
        }
        if (!summoned && enraged()) {
            summoned = true;
            callCourt(server);
        }
        LivingEntity target = getTarget();
        if (target == null) {
            return;
        }
        if (--breathCooldown <= 0) {
            breathCooldown = 20;
            if (distanceToSqr(target) < BREATH_RANGE * BREATH_RANGE && hasLineOfSight(target)) {
                breatheFrost(server);
                breathCooldown = enraged() ? 70 : 110;
            }
        }
        if (--stompCooldown <= 0) {
            stompCooldown = 20;
            if (onGround() && distanceToSqr(target) < STOMP_RADIUS * STOMP_RADIUS) {
                stomp(server);
                stompCooldown = 140;
            }
        }
    }

    /** Everyone in a cone in front of him is hurt and frozen. */
    public void breatheFrost(ServerLevel server) {
        Vec3 look = getViewVector(1.0F).normalize();
        Vec3 mouth = getEyePosition();
        for (LivingEntity victim : server.getEntitiesOfClass(LivingEntity.class, getBoundingBox().inflate(BREATH_RANGE),
                e -> e != this && !(e instanceof FrostGiant) && e.isAlive()
                        && e.position().add(0, e.getBbHeight() / 2, 0).subtract(mouth).normalize().dot(look) > 0.6)) {
            victim.hurt(damageSources().freeze(), 6.0F);
            FrostGiant.chill(victim, this, 5);
        }
        for (int i = 1; i <= 8; i++) {
            Vec3 p = mouth.add(look.scale(i * 1.2));
            server.sendParticles(ParticleTypes.SNOWFLAKE, p.x, p.y, p.z, 8, 0.25 * i * 0.3, 0.2, 0.25 * i * 0.3, 0.02);
        }
        playSound(SoundEvents.POWDER_SNOW_BREAK, 3.0F, 0.5F);
    }

    private void stomp(ServerLevel server) {
        for (LivingEntity victim : server.getEntitiesOfClass(LivingEntity.class, getBoundingBox().inflate(STOMP_RADIUS),
                e -> e != this && !(e instanceof FrostGiant))) {
            victim.hurt(damageSources().mobAttack(this), 8.0F);
            victim.setDeltaMovement(victim.getDeltaMovement().add(0.0, 0.7, 0.0));
            victim.hurtMarked = true;
            FrostGiant.chill(victim, this, 2);
        }
        server.sendParticles(ParticleTypes.EXPLOSION, getX(), getY() + 0.2, getZ(), 8, 2.0, 0.2, 2.0, 0.0);
        playSound(SoundEvents.GLASS_BREAK, 2.0F, 0.5F);
    }

    private void callCourt(ServerLevel server) {
        for (int i = 0; i < 2; i++) {
            FrostGiant giant = NorseEntities.FROST_GIANT.get().create(server);
            if (giant == null) {
                continue;
            }
            double angle = Math.PI * i + getYRot() * Math.PI / 180.0;
            giant.moveTo(getX() + Math.cos(angle) * 3.0, getY(), getZ() + Math.sin(angle) * 3.0, getYRot(), 0.0F);
            giant.finalizeSpawn(server, server.getCurrentDifficultyAt(giant.blockPosition()), MobSpawnType.MOB_SUMMONED, null);
            giant.setTarget(getTarget());
            server.addFreshEntity(giant);
            server.sendParticles(ParticleTypes.SNOWFLAKE, giant.getX(), giant.getY() + 2.0, giant.getZ(), 30, 0.6, 1.2, 0.6, 0.05);
        }
        playSound(SoundEvents.RAVAGER_ROAR, 3.0F, 0.5F);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("CalledCourt", summoned);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        summoned = tag.getBoolean("CalledCourt");
    }

    @Override
    public boolean canFreeze() {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.POLAR_BEAR_WARNING;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.IRON_GOLEM_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.IRON_GOLEM_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.4F;
    }
}
