package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
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

/**
 * Osiris, the green-skinned king of the dead, enthroned in the Hall of Judgment. He raises the dead to fight for him,
 * and as Isis once brought him back to life, he rises once from a death blow with half his health. He drops the djed
 * of Osiris, the pillar of his backbone.
 */
public class OsirisGod extends EgyptianGod {
    private boolean reborn;

    public OsirisGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.GREEN, EgyptianContent.FLAIL_OF_OSIRIS);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 400.0)
                .add(Attributes.ATTACK_DAMAGE, 12.0)
                .add(Attributes.MOVEMENT_SPEED, 0.26)
                .add(Attributes.ARMOR, 8.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.9)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected int powerInterval() {
        return 240;
    }

    /** The dead rise for their king: two mummies. */
    @Override
    public void power(ServerLevel server, LivingEntity target) {
        summon(server, EgyptianEntities.MUMMY.get(), 2, target);
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 80, 1), this);
        server.sendParticles(ParticleTypes.SCULK_SOUL, getX(), getY(0.5), getZ(), 30, 2.0, 0.5, 2.0, 0.02);
        playSound(SoundEvents.ZOMBIE_VILLAGER_CURE, 2.0F, 0.6F);
    }

    /** Whether Osiris has already risen from the dead. */
    public boolean reborn() {
        return reborn;
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (!reborn && !level().isClientSide && amount >= getHealth() && !source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) {
            reborn = true;
            setHealth(getMaxHealth() / 2.0F);
            addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 100, 2), this);
            if (level() instanceof ServerLevel server) {
                server.sendParticles(ParticleTypes.TOTEM_OF_UNDYING, getX(), getY(0.6), getZ(), 80, 0.8, 1.2, 0.8, 0.4);
            }
            playSound(SoundEvents.TOTEM_USE, 2.0F, 0.8F);
            return false;
        }
        return super.hurt(source, amount);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("Reborn", reborn);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        reborn = tag.getBoolean("Reborn");
    }

    @Override
    public float getVoicePitch() {
        return 0.6F;
    }
}
