package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekSounds;
import net.minecraft.core.component.DataComponents;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.control.FlyingMoveControl;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomFlyingGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.ai.navigation.FlyingPathNavigation;
import net.minecraft.world.entity.ai.navigation.PathNavigation;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Winged storm spirit, half woman, half bird. Swoops at travellers on the peaks and the coast, day and night.
 * Like the harpies that tormented Phineus, it snatches food: a hit steals one piece of food from your inventory,
 * and the harpy flies off with it. Kill it to get your food back.
 */
public class Harpy extends Monster {
    private static final int FLEE_TICKS = 100;

    private int fleeTicks;

    public Harpy(EntityType<? extends Monster> type, Level level) {
        super(type, level);
        this.moveControl = new FlyingMoveControl(this, 20, true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 20.0)
                .add(Attributes.ATTACK_DAMAGE, 4.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.FLYING_SPEED, 0.6)
                .add(Attributes.FOLLOW_RANGE, 32.0);
    }

    @Override
    protected PathNavigation createNavigation(Level level) {
        FlyingPathNavigation navigation = new FlyingPathNavigation(this, level);
        navigation.setCanOpenDoors(false);
        navigation.setCanFloat(true);
        navigation.setCanPassDoors(true);
        return navigation;
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.3, true));
        goalSelector.addGoal(7, new WaterAvoidingRandomFlyingGoal(this, 1.0));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 12.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers());
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof Player player && getMainHandItem().isEmpty() && stealFood(player)) {
            fleeTicks = FLEE_TICKS;
            setTarget(null);
        }
        return hit;
    }

    private boolean stealFood(Player player) {
        for (ItemStack stack : player.getInventory().items) {
            if (!stack.isEmpty() && stack.has(DataComponents.FOOD)) {
                setItemSlot(EquipmentSlot.MAINHAND, stack.split(1));
                setGuaranteedDrop(EquipmentSlot.MAINHAND);
                playSound(GreekSounds.HARPY_AMBIENT.get(), 1.2F, 1.4F);
                return true;
            }
        }
        return false;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (fleeTicks > 0) {
            fleeTicks--;
            setTarget(null);
            Player player = level().getNearestPlayer(this, 24.0);
            if (player != null) {
                Vec3 away = position().subtract(player.position()).normalize().scale(10.0);
                getMoveControl().setWantedPosition(getX() + away.x, Math.max(getY(), player.getY()) + 4.0, getZ() + away.z, 1.4);
            }
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
    protected SoundEvent getAmbientSound() {
        return GreekSounds.HARPY_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return GreekSounds.HARPY_HURT.get();
    }

    @Override
    protected SoundEvent getDeathSound() {
        return GreekSounds.HARPY_DEATH.get();
    }
}
