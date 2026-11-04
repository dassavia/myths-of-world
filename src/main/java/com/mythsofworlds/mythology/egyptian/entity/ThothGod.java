package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import net.minecraft.core.particles.ParticleTypes;
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
import net.minecraft.world.phys.Vec3;

/**
 * Thoth, the ibis-headed scribe of the gods and lord of the moon, who records the judgment of the dead. He speaks
 * words of power: his foe is lifted into the air and struck by magic. Below half health he steps away through the
 * moonlight after every spell. He drops the tablet of Thoth.
 */
public class ThothGod extends EgyptianGod {
    public ThothGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.WHITE, EgyptianContent.STAFF_OF_THOTH);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 340.0)
                .add(Attributes.ATTACK_DAMAGE, 9.0)
                .add(Attributes.MOVEMENT_SPEED, 0.28)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.7)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected int powerInterval() {
        return 90;
    }

    @Override
    protected double powerRange() {
        return 20.0;
    }

    /** Words of power: levitation and a blow of magic; enraged, he steps away afterwards. */
    @Override
    public void power(ServerLevel server, LivingEntity target) {
        if (!hasLineOfSight(target)) {
            return;
        }
        target.hurt(damageSources().indirectMagic(this, this), 5.0F);
        target.addEffect(new MobEffectInstance(MobEffects.LEVITATION, 30, 1), this);
        server.sendParticles(ParticleTypes.ENCHANT, target.getX(), target.getY(0.5), target.getZ(), 40, 0.4, 0.8, 0.4, 0.5);
        playSound(SoundEvents.EVOKER_CAST_SPELL, 2.5F, 1.0F);
        if (enraged()) {
            Vec3 away = position().subtract(target.position()).multiply(1.0, 0.0, 1.0);
            if (away.lengthSqr() > 1.0E-4) {
                away = away.normalize().scale(6.0);
                server.sendParticles(ParticleTypes.REVERSE_PORTAL, getX(), getY(0.5), getZ(), 20, 0.4, 0.8, 0.4, 0.05);
                randomTeleport(getX() + away.x, getY(), getZ() + away.z, true);
            }
        }
    }

    @Override
    public float getVoicePitch() {
        return 1.2F;
    }
}
