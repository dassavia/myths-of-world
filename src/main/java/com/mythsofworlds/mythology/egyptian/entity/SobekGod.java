package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.pathfinder.PathType;

/**
 * Sobek, the crocodile-headed lord of the Nile and its waters, in his shrine on the river bank among his crocodiles.
 * He is no friend of strangers and attacks on sight. His bite drags his foe down in the death roll, he calls the
 * crocodiles of the river, and in the water he heals. He drops a fang of Sobek.
 */
public class SobekGod extends EgyptianGod {
    public SobekGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.GREEN, EgyptianContent.KHOPESH_OF_SOBEK);
        setPathfindingMalus(PathType.WATER, 0.0F);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 450.0)
                .add(Attributes.ATTACK_DAMAGE, 15.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 12.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.9)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected boolean hostile() {
        return true;
    }

    @Override
    protected int powerInterval() {
        return 160;
    }

    /** The death roll on a foe close by, else his crocodiles come. */
    @Override
    public void power(ServerLevel server, LivingEntity target) {
        if (distanceToSqr(target) < 12.0) {
            deathRoll(server, target);
        } else {
            summon(server, EgyptianEntities.CROCODILE.get(), 2, target);
            playSound(SoundEvents.RAVAGER_ROAR, 2.0F, 1.4F);
        }
    }

    public void deathRoll(ServerLevel server, LivingEntity target) {
        target.hurt(damageSources().mobAttack(this), 8.0F);
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 80, 2), this);
        target.setDeltaMovement(target.getDeltaMovement().multiply(0.2, 1.0, 0.2).add(0.0, -0.4, 0.0));
        target.hurtMarked = true;
        server.sendParticles(ParticleTypes.SPLASH, target.getX(), target.getY(0.5), target.getZ(), 40, 0.6, 0.4, 0.6, 0.2);
        playSound(SoundEvents.PLAYER_SPLASH_HIGH_SPEED, 2.0F, 0.6F);
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (!level().isClientSide && isInWater() && tickCount % 20 == 0) {
            heal(3.0F);
        }
    }

    @Override
    public boolean isPushedByFluid() {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.RAVAGER_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.RAVAGER_HURT;
    }

    @Override
    public float getVoicePitch() {
        return 0.6F;
    }
}
