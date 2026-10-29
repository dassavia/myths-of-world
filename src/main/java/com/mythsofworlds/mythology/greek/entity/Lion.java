package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.GreekSounds;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.BreedGoal;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.FollowParentGoal;
import net.minecraft.world.entity.ai.goal.LeapAtTargetGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.animal.Animal;
import net.minecraft.world.entity.animal.Rabbit;
import net.minecraft.world.entity.animal.Sheep;
import net.minecraft.world.entity.animal.goat.Goat;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * Lion of the pride that roams the Nemean Forest. Hunts sheep, goats and rabbits; leaves people alone unless one of
 * the pride is attacked, then the whole pride comes. Breeds on raw beef. Unlike the Nemean Lion, any blade hurts it.
 */
public class Lion extends Animal {
    public Lion(EntityType<? extends Animal> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Animal.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 30.0)
                .add(Attributes.ATTACK_DAMAGE, 6.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.FOLLOW_RANGE, 24.0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new LeapAtTargetGoal(this, 0.4F));
        goalSelector.addGoal(3, new MeleeAttackGoal(this, 1.2, true));
        goalSelector.addGoal(4, new BreedGoal(this, 1.0));
        goalSelector.addGoal(5, new FollowParentGoal(this, 1.1));
        goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 0.8));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 10.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers());
        targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(this, Sheep.class, false));
        targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(this, Goat.class, false));
        targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(this, Rabbit.class, false));
    }

    @Override
    public boolean isFood(ItemStack stack) {
        return stack.is(Items.BEEF);
    }

    @Nullable
    @Override
    public AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
        return GreekEntities.LION.get().create(level);
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

    @Override
    public float getVoicePitch() {
        return isBaby() ? 1.6F : 1.2F;
    }
}
