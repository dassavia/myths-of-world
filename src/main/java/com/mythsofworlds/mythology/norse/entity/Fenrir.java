package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import com.mythsofworlds.mythology.norse.NorseEntities;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
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
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Fenrir, the monstrous wolf of Loki, on his island in the Iron Wood. Fast, leaps at his prey, and his wounds close
 * while he is free. At half health he howls for three wargs of his kin. While he is free no weapon of men does him
 * much harm: every wound is a quarter of what it would be. Only Gleipnir holds him: bound, he cannot move or bite,
 * stops healing and takes half again as much damage, until he tears loose.
 */
public class Fenrir extends GreekBoss {
    public static final int BOUND_TICKS = 160;
    public static final int REBIND_TICKS = 200;
    public static final float FREE_DAMAGE = 0.25F;
    private static final EntityDataAccessor<Boolean> BOUND = SynchedEntityData.defineId(Fenrir.class, EntityDataSerializers.BOOLEAN);

    private int boundTicks;
    private int rebindCooldown;
    private int leapCooldown = 80;
    private boolean howled;

    public Fenrir(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.RED, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 650.0)
                .add(Attributes.ATTACK_DAMAGE, 14.0)
                .add(Attributes.MOVEMENT_SPEED, 0.36)
                .add(Attributes.ARMOR, 8.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.FOLLOW_RANGE, 40.0)
                .add(Attributes.STEP_HEIGHT, 1.5);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(BOUND, false);
    }

    public boolean isBound() {
        return entityData.get(BOUND);
    }

    /** Called by Gleipnir. False if he has only just torn loose. */
    public boolean bind() {
        if (isBound() || rebindCooldown > 0) {
            return false;
        }
        entityData.set(BOUND, true);
        boundTicks = BOUND_TICKS;
        getNavigation().stop();
        playSound(SoundEvents.CHAIN_PLACE, 2.0F, 0.5F);
        playSound(SoundEvents.WOLF_WHINE, 2.0F, 0.4F);
        return true;
    }

    private void tearLoose() {
        entityData.set(BOUND, false);
        rebindCooldown = REBIND_TICKS;
        playSound(SoundEvents.CHAIN_BREAK, 2.0F, 0.5F);
        playSound(SoundEvents.WOLF_GROWL, 3.0F, 0.4F);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        if (isBound()) {
            return false;
        }
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.WITHER, 60, 1), this);
        }
        return hit;
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (isBound()) {
            amount *= 1.5F;
        } else if (!source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) {
            amount *= FREE_DAMAGE;
        }
        return super.hurt(source, amount);
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (!(level() instanceof ServerLevel server)) {
            return;
        }
        if (rebindCooldown > 0) {
            rebindCooldown--;
        }
        if (isBound()) {
            getNavigation().stop();
            addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 10, 9, false, false));
            setDeltaMovement(0.0, Math.min(0.0, getDeltaMovement().y), 0.0);
            if (tickCount % 10 == 0) {
                server.sendParticles(ParticleTypes.ENCHANT, getX(), getY() + 1.0, getZ(), 6, 0.8, 0.5, 0.8, 0.0);
            }
            if (--boundTicks <= 0) {
                tearLoose();
            }
            return;
        }
        if (tickCount % 40 == 0 && getHealth() < getMaxHealth()) {
            heal(2.0F);
        }
        if (!howled && enraged()) {
            howled = true;
            howl(server);
        }
        LivingEntity target = getTarget();
        if (target != null && --leapCooldown <= 0) {
            leapCooldown = 20;
            double distance = distanceToSqr(target);
            if (onGround() && distance > 16.0 && distance < 256.0) {
                Vec3 jump = new Vec3(target.getX() - getX(), 0.0, target.getZ() - getZ()).normalize().scale(1.4);
                setDeltaMovement(jump.x, 0.6, jump.z);
                hurtMarked = true;
                leapCooldown = 100;
            }
        }
    }

    private void howl(ServerLevel server) {
        for (int i = 0; i < 3; i++) {
            Warg warg = NorseEntities.WARG.get().create(server);
            if (warg == null) {
                continue;
            }
            double angle = i * Math.PI * 2.0 / 3.0;
            warg.moveTo(getX() + Math.cos(angle) * 3.0, getY(), getZ() + Math.sin(angle) * 3.0, getYRot(), 0.0F);
            warg.finalizeSpawn(server, server.getCurrentDifficultyAt(warg.blockPosition()), MobSpawnType.MOB_SUMMONED, null);
            warg.setTarget(getTarget());
            server.addFreshEntity(warg);
        }
        playSound(SoundEvents.WOLF_HOWL, 4.0F, 0.5F);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("Howled", howled);
        tag.putInt("BoundTicks", isBound() ? boundTicks : 0);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        howled = tag.getBoolean("Howled");
        boundTicks = tag.getInt("BoundTicks");
        entityData.set(BOUND, boundTicks > 0);
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
        return 0.4F;
    }
}
