package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.core.entity.MythBoss;
import com.mythsofworlds.mythology.greek.GreekSounds;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.sounds.SoundEvent;
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
import net.minecraft.world.entity.projectile.AbstractArrow;
import net.minecraft.world.entity.projectile.ThrownPotion;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.alchemy.PotionContents;
import net.minecraft.world.item.alchemy.Potions;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import net.minecraft.world.item.enchantment.Enchantments;
import net.minecraft.world.level.Level;

/**
 * The Lernaean Hydra, boss of the Stygian Marsh. Five heads spit poison, and its wounds close by themselves
 * unless they are burned: like Heracles and Iolaus, use fire (fire aspect, flame arrows, lava) to stop the
 * regeneration for 10 seconds. Fire burns it three times as hard, and a blade enchanted with fire aspect cuts it
 * (1 + 1.5 x level) times as deep. Below half health it spits twice as often, and Karkinos, the giant crab Hera
 * sent to help it, guards its lair.
 * Drops a Hydra Egg, from which a tame little hydra hatches.
 */
public class Hydra extends MythBoss {
    /** How long after a fire hit the hydra cannot regenerate. */
    public static final int CAUTERIZED_TICKS = 200;

    private int lastFireHurt = -CAUTERIZED_TICKS;
    private int spitCooldown = 40;

    public Hydra(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.GREEN, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 400.0)
                .add(Attributes.ATTACK_DAMAGE, 10.0)
                .add(Attributes.MOVEMENT_SPEED, 0.22)
                .add(Attributes.ARMOR, 8.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.FOLLOW_RANGE, 32.0);
    }

    public boolean isCauterized() {
        return tickCount - lastFireHurt < CAUTERIZED_TICKS || isOnFire();
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (source.is(DamageTypeTags.IS_FIRE)) {
            lastFireHurt = tickCount;
            amount *= 3.0F;
        }
        int fireAspect = fireAspectLevel(source);
        if (fireAspect > 0) {
            lastFireHurt = tickCount;
            amount *= 1.0F + 1.5F * fireAspect;
        } else if (source.getDirectEntity() instanceof AbstractArrow arrow && arrow.isOnFire()) {
            lastFireHurt = tickCount;
            amount *= 2.0F;
        }
        return super.hurt(source, amount);
    }

    /** Level of fire aspect on the weapon of whoever struck this blow in melee, 0 if none. */
    private int fireAspectLevel(DamageSource source) {
        if (!source.isDirect() || !(source.getEntity() instanceof LivingEntity attacker)) {
            return 0;
        }
        Holder<Enchantment> fireAspect = level().registryAccess().registryOrThrow(Registries.ENCHANTMENT)
                .getHolderOrThrow(Enchantments.FIRE_ASPECT);
        return EnchantmentHelper.getItemEnchantmentLevel(fireAspect, attacker.getMainHandItem());
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (tickCount % 20 == 0 && getHealth() < getMaxHealth() && !isCauterized()) {
            heal(3.0F);
        }
        LivingEntity target = getTarget();
        if (--spitCooldown <= 0) {
            spitCooldown = 20;
            if (target != null && distanceToSqr(target) > 16.0 && distanceToSqr(target) < 400.0 && hasLineOfSight(target)) {
                spitPoison(target);
                spitCooldown = enraged() ? 30 : 60;
            }
        }
    }

    private void spitPoison(LivingEntity target) {
        double dx = target.getX() + target.getDeltaMovement().x - getX();
        double dy = target.getEyeY() - 1.1 - getEyeY();
        double dz = target.getZ() + target.getDeltaMovement().z - getZ();
        double horizontal = Math.sqrt(dx * dx + dz * dz);
        ThrownPotion potion = new ThrownPotion(level(), this);
        potion.setItem(PotionContents.createItemStack(Items.SPLASH_POTION, Potions.STRONG_POISON));
        potion.setPos(getX(), getEyeY(), getZ());
        potion.shoot(dx, dy + horizontal * 0.2, dz, 0.9F, 6.0F);
        level().addFreshEntity(potion);
        playSound(GreekSounds.HYDRA_SPIT.get(), 1.5F, 1.0F);
    }

    /** Its own venom does not harm it. */
    @Override
    public boolean canBeAffected(MobEffectInstance effect) {
        return !effect.is(MobEffects.POISON) && super.canBeAffected(effect);
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return GreekSounds.HYDRA_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return GreekSounds.HYDRA_HURT.get();
    }

    @Override
    protected SoundEvent getDeathSound() {
        return GreekSounds.HYDRA_DEATH.get();
    }
}
