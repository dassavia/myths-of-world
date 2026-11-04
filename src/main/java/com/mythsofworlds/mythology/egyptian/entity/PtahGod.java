package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
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

/**
 * Ptah, the craftsman who made the world by the thought of his heart and the word of his tongue, in his forge-temple
 * of Memphis. Wrapped like a mummy under his blue cap, slow and heavy in armour, he speaks and ushabti servants of
 * faience come to life; his blow numbs the hands. He drops the chisel of Ptah.
 */
public class PtahGod extends EgyptianGod {
    public PtahGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.BLUE, EgyptianContent.AXE_OF_PTAH);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 420.0)
                .add(Attributes.ATTACK_DAMAGE, 14.0)
                .add(Attributes.MOVEMENT_SPEED, 0.24)
                .add(Attributes.ARMOR, 16.0)
                .add(Attributes.ARMOR_TOUGHNESS, 4.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected int powerInterval() {
        return 220;
    }

    /** The word of creation: two ushabti wake, and the foe's hands grow numb. */
    @Override
    public void power(ServerLevel server, LivingEntity target) {
        summon(server, EgyptianEntities.USHABTI.get(), 2, target);
        target.addEffect(new MobEffectInstance(MobEffects.DIG_SLOWDOWN, 200, 1), this);
        target.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0), this);
        server.sendParticles(ParticleTypes.LAVA, getX(), getY(1.0), getZ(), 12, 1.0, 0.5, 1.0, 0.1);
        playSound(SoundEvents.ANVIL_USE, 2.0F, 0.6F);
    }

    @Override
    public float getVoicePitch() {
        return 0.85F;
    }
}
