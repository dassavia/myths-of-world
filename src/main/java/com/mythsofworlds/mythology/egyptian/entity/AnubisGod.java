package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.BossEvent;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;

/**
 * Anubis, the jackal-headed guardian of the dead, who weighs the hearts of the dead against the feather of Ma'at in
 * the Hall of Judgment. A heart heavy with wrongdoing withers: his weighing withers and slows his foe and heals him.
 * Below half health his jackals run to him. He drops the feather of Ma'at.
 */
public class AnubisGod extends EgyptianGod {
    private boolean calledJackals;

    public AnubisGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.PURPLE, EgyptianContent.GLAIVE_OF_ANUBIS);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 400.0)
                .add(Attributes.ATTACK_DAMAGE, 13.0)
                .add(Attributes.MOVEMENT_SPEED, 0.32)
                .add(Attributes.ARMOR, 8.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected int powerInterval() {
        return 140;
    }

    /** The weighing of the heart. */
    @Override
    public void power(ServerLevel server, LivingEntity target) {
        target.addEffect(new MobEffectInstance(MobEffects.WITHER, 100, 1), this);
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 100, 0), this);
        heal(10.0F);
        server.sendParticles(ParticleTypes.SOUL, target.getX(), target.getY(1.0), target.getZ(), 20, 0.4, 0.5, 0.4, 0.02);
        playSound(SoundEvents.EVOKER_PREPARE_SUMMON, 3.0F, 0.6F);
        if (!calledJackals && enraged()) {
            calledJackals = true;
            summon(server, EgyptianEntities.JACKAL.get(), 3, target);
            playSound(SoundEvents.WOLF_HOWL, 3.0F, 1.1F);
        }
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("CalledJackals", calledJackals);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        calledJackals = tag.getBoolean("CalledJackals");
    }

    @Override
    public float getVoicePitch() {
        return 0.75F;
    }
}
