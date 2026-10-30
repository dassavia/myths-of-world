package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.core.entity.MythBoss;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekSounds;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.LeapAtTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.projectile.Arrow;
import net.minecraft.world.level.Level;

/**
 * The Nemean Lion, mini-boss of Arcadia. No blade or arrow can pierce its golden hide: direct damage of any kind
 * glances off. Poison, harming and wither potions (thrown, or on tipped arrows) still work, and so does a dagger
 * made from one of its own claws, which drop when it dies. Pounces at its prey.
 */
public class NemeanLion extends MythBoss {
    /** Damage a tipped arrow does on its own; the potion on it does the rest. */
    private static final float TIPPED_ARROW_DAMAGE = 0.5F;

    public NemeanLion(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.YELLOW, true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 120.0)
                .add(Attributes.ATTACK_DAMAGE, 12.0)
                .add(Attributes.MOVEMENT_SPEED, 0.34)
                .add(Attributes.ARMOR, 8.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.6)
                .add(Attributes.FOLLOW_RANGE, 32.0);
    }

    @Override
    protected void registerGoals() {
        super.registerGoals();
        goalSelector.addGoal(1, new LeapAtTargetGoal(this, 0.5F));
    }

    /** True if this damage gets through the hide. */
    public static boolean piercesHide(DamageSource source) {
        if (source.is(DamageTypes.MAGIC) || source.is(DamageTypes.INDIRECT_MAGIC) || source.is(DamageTypes.WITHER)
                || source.is(DamageTypes.DRAGON_BREATH) || source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) {
            return true;
        }
        return !source.isDirect() ? false
                : source.getEntity() instanceof LivingEntity attacker
                        && attacker.getMainHandItem().is(GreekContent.NEMEAN_CLAW_DAGGER.get());
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (piercesHide(source)) {
            return super.hurt(source, amount);
        }
        // A tipped arrow only scratches the hide, but that is enough for its potion to take hold.
        if (source.getDirectEntity() instanceof Arrow arrow && arrow.getColor() != -1) {
            return super.hurt(source, Math.min(amount, TIPPED_ARROW_DAMAGE));
        }
        if (!level().isClientSide && !isInvulnerableTo(source)) {
            playSound(SoundEvents.SHIELD_BLOCK, 1.0F, 0.8F);
        }
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return GreekSounds.LION_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return GreekSounds.LION_HURT.get();
    }

    @Override
    protected SoundEvent getDeathSound() {
        return GreekSounds.LION_DEATH.get();
    }
}
