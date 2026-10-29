package com.mythsofworlds.mythology.norse.entity;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.ItemTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;

/**
 * Draugr, the walking dead of the barrows. Its touch carries the cold of the grave. It does not burn in the sun, and
 * it does not stay dead: unless it is cut down with an axe (the old way, taking its head) or burned, it rises again.
 */
public class Draugr extends Zombie {
    private boolean risen;

    public Draugr(EntityType<? extends Zombie> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Zombie.createAttributes()
                .add(Attributes.MAX_HEALTH, 30.0)
                .add(Attributes.ATTACK_DAMAGE, 5.0)
                .add(Attributes.ARMOR, 4.0)
                .add(Attributes.MOVEMENT_SPEED, 0.24)
                .add(Attributes.SPAWN_REINFORCEMENTS_CHANCE, 0.0);
    }

    @Override
    protected void populateDefaultEquipmentSlots(RandomSource random, DifficultyInstance difficulty) {
        int roll = random.nextInt(5);
        if (roll < 2) {
            setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(roll == 0 ? Items.IRON_AXE : Items.STONE_SWORD));
        }
        if (random.nextInt(3) == 0) {
            setItemSlot(EquipmentSlot.HEAD, new ItemStack(Items.CHAINMAIL_HELMET));
            setDropChance(EquipmentSlot.HEAD, 0.05F);
        }
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1), this);
            living.setTicksFrozen(Math.min(living.getTicksRequiredToFreeze() + 40, living.getTicksFrozen() + 60));
        }
        return hit;
    }

    /** An axe blow or fire puts a draugr to rest for good; anything else and it gets up again, once. */
    public static boolean laysToRest(DamageSource source) {
        if (source.is(DamageTypeTags.IS_FIRE) || source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) {
            return true;
        }
        return source.getEntity() instanceof LivingEntity attacker && attacker.getMainHandItem().is(ItemTags.AXES)
                && source.getDirectEntity() == attacker;
    }

    @Override
    protected void actuallyHurt(DamageSource source, float amount) {
        super.actuallyHurt(source, amount);
        if (isDeadOrDying() && !risen && !laysToRest(source)) {
            rise();
        }
    }

    public void rise() {
        risen = true;
        setHealth(getMaxHealth() / 2.0F);
        playSound(SoundEvents.ZOMBIE_VILLAGER_CURE, 0.8F, 0.5F);
        if (level() instanceof ServerLevel server) {
            server.sendParticles(ParticleTypes.SNOWFLAKE, getX(), getY() + 1.0, getZ(), 20, 0.3, 0.8, 0.3, 0.02);
        }
    }

    public boolean hasRisen() {
        return risen;
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("Risen", risen);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        risen = tag.getBoolean("Risen");
    }

    @Override
    protected boolean isSunSensitive() {
        return false;
    }

    @Override
    protected boolean convertsInWater() {
        return false;
    }

    /** The dead of the barrows were all grown warriors. */
    @Override
    public void setBaby(boolean baby) {
    }

    @Override
    public boolean canFreeze() {
        return false;
    }

    @Override
    public float getVoicePitch() {
        return super.getVoicePitch() * 0.7F;
    }
}
