package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekEntities;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.animal.horse.AbstractHorse;
import net.minecraft.world.entity.animal.horse.Horse;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * The Ceryneian Hind, sacred to Artemis: a deer with golden antlers, faster than any arrow.
 * Tame and saddle it like a horse; it is the fastest mount in the game. Lives in the groves of Arcadia.
 */
public class GoldenHind extends Horse {
    public GoldenHind(EntityType<? extends Horse> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return AbstractHorse.createBaseHorseAttributes()
                .add(Attributes.MAX_HEALTH, 22.0)
                .add(Attributes.MOVEMENT_SPEED, 0.42)
                .add(Attributes.JUMP_STRENGTH, 0.9);
    }

    @Override
    protected void randomizeAttributes(RandomSource random) {
        getAttribute(Attributes.MAX_HEALTH).setBaseValue(22.0);
        getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(0.42);
        getAttribute(Attributes.JUMP_STRENGTH).setBaseValue(0.9);
    }

    @Override
    public boolean canMate(Animal other) {
        return other != this && other instanceof GoldenHind hind && canParent() && hind.canParent();
    }

    @Nullable
    @Override
    public AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
        GoldenHind fawn = GreekEntities.GOLDEN_HIND.get().create(level);
        if (fawn != null && partner instanceof AbstractHorse horse) {
            setOffspringAttributes(horse, fawn);
        }
        return fawn;
    }
}
