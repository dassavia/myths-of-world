package com.mythsofworlds.mythology.greek.entity;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.AbstractSkeleton;
import net.minecraft.world.entity.monster.Skeleton;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;

/**
 * Spartoi, skeleton warriors sown from dragon's teeth. Fight with swords in golden helmets, do not burn in the sun.
 * Haunt the Asphodel Meadows and guard the Labyrinth. Cut one down and there is a chance it pulls itself together
 * and rises again, once.
 */
public class Spartoi extends Skeleton {
    /** Chance to rise again after the first death. */
    public static final float REBIRTH_CHANCE = 0.3F;

    private boolean reborn;

    public Spartoi(EntityType<? extends Skeleton> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return AbstractSkeleton.createAttributes()
                .add(Attributes.MAX_HEALTH, 26.0)
                .add(Attributes.ATTACK_DAMAGE, 3.0)
                .add(Attributes.ARMOR, 4.0);
    }

    @Override
    protected void populateDefaultEquipmentSlots(RandomSource random, DifficultyInstance difficulty) {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(random.nextInt(4) == 0 ? Items.IRON_AXE : Items.IRON_SWORD));
        setItemSlot(EquipmentSlot.HEAD, new ItemStack(Items.GOLDEN_HELMET));
        setDropChance(EquipmentSlot.HEAD, 0.05F);
    }

    @Override
    protected void actuallyHurt(DamageSource source, float amount) {
        super.actuallyHurt(source, amount);
        if (isDeadOrDying() && !reborn && !source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)
                && random.nextFloat() < REBIRTH_CHANCE) {
            rise();
        }
    }

    /** Pulls itself together with half of its health. */
    public void rise() {
        reborn = true;
        setHealth(getMaxHealth() / 2.0F);
        playSound(SoundEvents.SKELETON_CONVERTED_TO_STRAY, 1.0F, 0.6F);
        if (level() instanceof ServerLevel server) {
            server.sendParticles(ParticleTypes.SOUL, getX(), getY() + 1.0, getZ(), 16, 0.3, 0.8, 0.3, 0.02);
        }
    }

    public boolean isReborn() {
        return reborn;
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
    protected boolean isSunBurnTick() {
        return false;
    }
}
