package com.mythsofworlds.mythology.slavic.entity;

import com.mythsofworlds.mythology.slavic.SlavicSounds;
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
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/**
 * Leshy, the master of the forest: a tall old man of bark and moss. He leaves alone those who leave him alone; anger
 * him and every blow blinds you and leads you astray, throwing you somewhere else in his woods.
 */
public class Leshy extends Monster {
    public static final double ASTRAY = 10.0;

    public Leshy(EntityType<? extends Monster> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 44.0)
                .add(Attributes.ATTACK_DAMAGE, 6.0)
                .add(Attributes.ARMOR, 4.0)
                .add(Attributes.MOVEMENT_SPEED, 0.28)
                .add(Attributes.FOLLOW_RANGE, 24.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.1, true));
        goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 0.6));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 10.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers());
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            leadAstray(living);
        }
        return hit;
    }

    /** Blinds the victim and throws them up to {@link #ASTRAY} blocks away into the trees. */
    public void leadAstray(LivingEntity living) {
        living.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 80, 0), this);
        living.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 120, 0), this);
        if (level() instanceof ServerLevel server) {
            server.sendParticles(ParticleTypes.SPORE_BLOSSOM_AIR, living.getX(), living.getY(1.0), living.getZ(), 20, 0.5, 0.5, 0.5, 0.0);
            for (int attempt = 0; attempt < 16; attempt++) {
                double x = living.getX() + (random.nextDouble() - 0.5) * 2.0 * ASTRAY;
                double z = living.getZ() + (random.nextDouble() - 0.5) * 2.0 * ASTRAY;
                double y = living.getY() + random.nextInt(7) - 3;
                if (living.randomTeleport(x, y, z, true)) {
                    break;
                }
            }
        }
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SlavicSounds.LESHY_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.WOOD_HIT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.WOOD_BREAK;
    }

    @Override
    public float getVoicePitch() {
        return 0.6F;
    }
}
