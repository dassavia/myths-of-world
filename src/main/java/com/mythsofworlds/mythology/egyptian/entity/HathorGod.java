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
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/**
 * Hathor, the lady of joy, music and love, with the cow horns and the sun disc, in her shrine in the Fields of Aaru.
 * Her song of the sistrum makes heads spin and feet slow. But she was also the eye of Ra that raged as Sekhmet:
 * below half health her rage returns and she strikes with the strength of the lioness. She drops a horn of Hathor.
 */
public class HathorGod extends EgyptianGod {
    public static final double SONG_RADIUS = 12.0;

    public HathorGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.PINK, EgyptianContent.SCEPTRE_OF_HATHOR);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 360.0)
                .add(Attributes.ATTACK_DAMAGE, 10.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected int powerInterval() {
        return 130;
    }

    @Override
    public void power(ServerLevel server, LivingEntity target) {
        song(server);
        if (enraged()) {
            addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, 200, 1), this);
            server.sendParticles(ParticleTypes.ANGRY_VILLAGER, getX(), getY(1.1), getZ(), 6, 0.5, 0.3, 0.5, 0.1);
        }
    }

    /** The song of the sistrum: nausea and slowness on everyone around. Returns how many heard it. */
    public int song(ServerLevel server) {
        int heard = 0;
        for (Player player : foesAround(server, SONG_RADIUS)) {
            player.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 160, 0), this);
            player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 100, 1), this);
            heard++;
        }
        server.sendParticles(ParticleTypes.NOTE, getX(), getY(1.1), getZ(), 12, 1.5, 0.6, 1.5, 1.0);
        playSound(SoundEvents.NOTE_BLOCK_CHIME.value(), 3.0F, 0.8F);
        return heard;
    }

    @Override
    public float getVoicePitch() {
        return 1.25F;
    }
}
