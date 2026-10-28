package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekEntities;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.animal.horse.AbstractHorse;
import net.minecraft.world.entity.animal.horse.Horse;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * Winged horse of the gods. Tame and saddle it like a horse; it jumps higher than any horse,
 * glides down instead of falling and never takes fall damage. Breeds only with another pegasus.
 */
public class Pegasus extends Horse {
    public Pegasus(EntityType<? extends Horse> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return AbstractHorse.createBaseHorseAttributes()
                .add(Attributes.MAX_HEALTH, 30.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.JUMP_STRENGTH, 1.0);
    }

    /** Every pegasus is equally fine: no random stats like a horse. */
    @Override
    protected void randomizeAttributes(RandomSource random) {
        getAttribute(Attributes.MAX_HEALTH).setBaseValue(30.0);
        getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(0.3);
        getAttribute(Attributes.JUMP_STRENGTH).setBaseValue(1.0);
    }

    @Override
    public void aiStep() {
        super.aiStep();
        Vec3 motion = getDeltaMovement();
        if (!onGround() && motion.y < -0.1) {
            setDeltaMovement(motion.x, motion.y * 0.6, motion.z);
        }
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, DamageSource source) {
        return false;
    }

    public boolean isFlying() {
        return !onGround();
    }

    @Override
    public boolean canMate(Animal other) {
        return other != this && other instanceof Pegasus pegasus && canParent() && pegasus.canParent();
    }

    @Nullable
    @Override
    public AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
        Pegasus foal = GreekEntities.PEGASUS.get().create(level);
        if (foal != null && partner instanceof AbstractHorse horse) {
            setOffspringAttributes(horse, foal);
        }
        return foal;
    }
}
