package com.mythsofworlds.mythology.slavic.entity;

import com.mythsofworlds.mythology.norse.entity.Raven;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Parrot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;

/**
 * Zhar-ptitsa, the Firebird, whose feathers glow like embers. Stroke her with an empty hand and she lets fall a
 * feather, once every {@link #FEATHER_COOLDOWN} ticks. Tamed with seeds, she follows you like a raven, and her light
 * shows the monsters hiding around you.
 */
public class Firebird extends Raven {
    public static final int FEATHER_COOLDOWN = 2400;
    private int featherCooldown;

    public Firebird(EntityType<? extends Parrot> type, Level level) {
        super(type, level);
    }

    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        if (player.getItemInHand(hand).isEmpty() && !isBaby()) {
            if (!level().isClientSide) {
                if (featherCooldown > 0) {
                    playSound(SoundEvents.PARROT_HURT, 0.6F, 1.6F);
                    return InteractionResult.CONSUME;
                }
                dropFeather();
            }
            return InteractionResult.sidedSuccess(level().isClientSide);
        }
        return super.mobInteract(player, hand);
    }

    public void dropFeather() {
        featherCooldown = FEATHER_COOLDOWN;
        spawnAtLocation(new ItemStack(SlavicContent.FIREBIRD_FEATHER.get()));
        playSound(SoundEvents.AMETHYST_BLOCK_CHIME, 1.0F, 1.4F);
    }

    public int featherCooldown() {
        return featherCooldown;
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (featherCooldown > 0) {
            featherCooldown--;
        }
        if (level().isClientSide && random.nextInt(4) == 0) {
            level().addParticle(random.nextBoolean() ? ParticleTypes.FLAME : ParticleTypes.SMALL_FLAME,
                    getRandomX(0.5), getRandomY(), getRandomZ(0.5), 0.0, 0.01, 0.0);
        }
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("FeatherCooldown", featherCooldown);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        featherCooldown = tag.getInt("FeatherCooldown");
    }

    @Override
    public float getVoicePitch() {
        return 1.3F;
    }
}
