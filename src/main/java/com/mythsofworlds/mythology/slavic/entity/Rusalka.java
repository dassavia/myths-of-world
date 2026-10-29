package com.mythsofworlds.mythology.slavic.entity;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.RandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.pathfinder.PathType;
import net.minecraft.world.phys.Vec3;

/**
 * Rusalka, the pale water maiden with green hair. She sings: every few seconds anyone she sees within
 * {@link #SONG_RANGE} blocks is drawn a step towards her, and her cold touch takes the strength from your hands.
 * She breathes under water and swims as fast as she walks.
 */
public class Rusalka extends Monster {
    public static final double SONG_RANGE = 14.0;
    private int songCooldown = 40;

    public Rusalka(EntityType<? extends Monster> type, Level level) {
        super(type, level);
        setPathfindingMalus(PathType.WATER, 0.0F);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 22.0)
                .add(Attributes.ATTACK_DAMAGE, 4.0)
                .add(Attributes.MOVEMENT_SPEED, 0.28)
                .add(Attributes.FOLLOW_RANGE, 24.0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.0, true));
        goalSelector.addGoal(7, new RandomStrollGoal(this, 0.7));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 12.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (isInWater()) {
            setDeltaMovement(getDeltaMovement().multiply(1.12, 1.0, 1.12));
        }
        if (level() instanceof ServerLevel server && --songCooldown <= 0) {
            songCooldown = 60;
            LivingEntity target = getTarget();
            if (target instanceof Player player && distanceToSqr(player) < SONG_RANGE * SONG_RANGE && hasLineOfSight(player)) {
                sing(server, player);
            }
        }
    }

    /** Pulls the player towards her. */
    public void sing(ServerLevel server, Player player) {
        Vec3 towards = position().subtract(player.position()).multiply(1.0, 0.0, 1.0);
        if (towards.lengthSqr() > 1.0E-4) {
            towards = towards.normalize().scale(0.7);
            player.push(towards.x, 0.15, towards.z);
            player.hurtMarked = true;
        }
        server.sendParticles(ParticleTypes.NOTE, getX(), getY(1.1), getZ(), 3, 0.3, 0.2, 0.3, 1.0);
        playSound(SoundEvents.ALLAY_AMBIENT_WITHOUT_ITEM, 1.2F, 0.7F);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 120, 0), this);
            living.setTicksFrozen(Math.min(living.getTicksRequiredToFreeze() + 20, living.getTicksFrozen() + 40));
        }
        return hit;
    }

    @Override
    public boolean canBreatheUnderwater() {
        return true;
    }

    @Override
    public boolean isPushedByFluid() {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.ALLAY_AMBIENT_WITH_ITEM;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.ALLAY_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.ALLAY_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.75F;
    }
}
