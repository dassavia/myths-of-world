package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.animal.Cat;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * Cat of Bastet, the black temple cat with golden eyes, sacred to the goddess who guards the home. Tamed with raw
 * fish like any cat. Mummies, scarabs and the other creatures of the dark shy away from it. A tame cat of Bastet
 * keeps its master well (Regeneration every {@link #BLESSING_TICKS} ticks while near) and hunts scarabs; and as Ra in
 * the shape of the great cat slew the serpent Apep, it throws itself on Apep, who takes full damage only from a hero
 * who has a cat of Bastet by their side.
 */
public class BastetCat extends Cat {
    public static final int BLESSING_TICKS = 200;
    public static final double BLESSING_RANGE = 8.0;

    public BastetCat(EntityType<? extends Cat> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Cat.createAttributes()
                .add(Attributes.MAX_HEALTH, 16.0)
                .add(Attributes.ATTACK_DAMAGE, 4.0);
    }

    @Override
    protected void registerGoals() {
        super.registerGoals();
        targetSelector.addGoal(1, new NearestAttackableTargetGoal<>(this, Apep.class, 10, false, false, e -> isTame()));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Scarab.class, 10, true, false, e -> isTame()));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (!level().isClientSide && isTame() && tickCount % BLESSING_TICKS == 0) {
            bless(getOwner());
        }
    }

    /** Gives its master Regeneration if they are near; false if they are not. */
    public boolean bless(@Nullable LivingEntity owner) {
        if (owner == null || owner.distanceToSqr(this) > BLESSING_RANGE * BLESSING_RANGE) {
            return false;
        }
        owner.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 80, 0, true, true), this);
        return true;
    }

    @Nullable
    @Override
    public Cat getBreedOffspring(ServerLevel level, AgeableMob partner) {
        BastetCat kitten = EgyptianEntities.BASTET_CAT.get().create(level);
        if (kitten != null && isTame() && getOwnerUUID() != null) {
            kitten.setOwnerUUID(getOwnerUUID());
            kitten.setTame(true, true);
        }
        return kitten;
    }

    @Override
    public boolean canMate(net.minecraft.world.entity.animal.Animal other) {
        return other != this && other instanceof BastetCat cat && isTame() && cat.isTame() && isInLove() && cat.isInLove();
    }
}
