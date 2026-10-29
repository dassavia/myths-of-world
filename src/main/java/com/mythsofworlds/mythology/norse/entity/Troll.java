package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.norse.item.MjolnirItem;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.RestrictSunGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;

/**
 * Troll of the mountains and the dark taiga. Huge, very strong, and its wounds close by themselves unless they were
 * burned. Trolls hide from the sun for a reason: a troll caught in daylight turns to stone where it stands.
 */
public class Troll extends Monster {
    public static final int FIRE_STOPS_HEALING_TICKS = 200;

    private int noHealTicks;

    public Troll(EntityType<? extends Monster> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 70.0)
                .add(Attributes.ATTACK_DAMAGE, 11.0)
                .add(Attributes.ATTACK_KNOCKBACK, 1.5)
                .add(Attributes.MOVEMENT_SPEED, 0.24)
                .add(Attributes.ARMOR, 4.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.7)
                .add(Attributes.FOLLOW_RANGE, 24.0)
                .add(Attributes.STEP_HEIGHT, 1.2);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new RestrictSunGoal(this));
        goalSelector.addGoal(4, new MeleeAttackGoal(this, 1.0, true));
        goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 0.7));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 12.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (MjolnirItem.struckWith(source)) {
            amount *= 2.0F;
        }
        if (source.is(DamageTypeTags.IS_FIRE)) {
            noHealTicks = FIRE_STOPS_HEALING_TICKS;
        }
        return super.hurt(source, amount);
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (level().isClientSide || !isAlive()) {
            return;
        }
        if (isOnFire()) {
            noHealTicks = FIRE_STOPS_HEALING_TICKS;
        }
        if (noHealTicks > 0) {
            noHealTicks--;
        } else if (tickCount % 20 == 0) {
            heal(1.0F);
        }
        if (inSunlight()) {
            petrify();
        }
    }

    public boolean inSunlight() {
        return level().isDay() && !level().isRaining() && level().canSeeSky(BlockPos.containing(getX(), getEyeY(), getZ()))
                && getLightLevelDependentMagicValue() > 0.5F;
    }

    /** Turns to a mossy stone statue, leaving only a tusk behind. */
    public void petrify() {
        if (!(level() instanceof ServerLevel server)) {
            return;
        }
        BlockPos feet = blockPosition();
        for (int dy = 0; dy < 3; dy++) {
            BlockPos pos = feet.above(dy);
            if (server.getBlockState(pos).canBeReplaced()) {
                server.setBlockAndUpdate(pos, dy == 0 ? Blocks.MOSSY_COBBLESTONE.defaultBlockState()
                        : dy == 1 ? Blocks.COBBLESTONE.defaultBlockState() : Blocks.MOSSY_COBBLESTONE_WALL.defaultBlockState());
            }
        }
        server.sendParticles(ParticleTypes.CLOUD, getX(), getY() + 1.5, getZ(), 30, 0.6, 1.0, 0.6, 0.02);
        playSound(SoundEvents.STONE_PLACE, 2.0F, 0.5F);
        ItemEntity tusk = new ItemEntity(server, getX(), getY() + 3.2, getZ(), new ItemStack(NorseContent.TROLL_TUSK.get()));
        server.addFreshEntity(tusk);
        discard();
    }

    public boolean healingStopped() {
        return noHealTicks > 0;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.RAVAGER_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.RAVAGER_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.RAVAGER_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return super.getVoicePitch() * 0.8F;
    }
}
