package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import com.mythsofworlds.mythology.egyptian.EgyptianSounds;
import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * Set, the red god of the desert, of storms and of chaos, in his temple in the Valley of the Kings. He raises
 * sandstorms that blind, wound and throw back everyone around him, steps through the storm to stand behind his foe,
 * and at half health calls three jackals. Set tore out the eye of Horus, and Horus healed it and beat him with it:
 * a hero who does not carry the eye of Horus does him only a quarter of the harm, and his storms cannot blind one
 * who carries it. He drops his was-sceptre.
 */
public class SetGod extends GreekBoss {
    public static final double STORM_RADIUS = 14.0;
    public static final float WITHOUT_EYE = 0.25F;

    private int stormCooldown = 80;
    private int stepCooldown = 160;
    private boolean calledJackals;

    public SetGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.RED, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 500.0)
                .add(Attributes.ATTACK_DAMAGE, 14.0)
                .add(Attributes.MOVEMENT_SPEED, 0.32)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.9)
                .add(Attributes.FOLLOW_RANGE, 40.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Nullable
    @Override
    public SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, MobSpawnType spawnType,
                                        @Nullable SpawnGroupData data) {
        arm();
        return super.finalizeSpawn(level, difficulty, spawnType, data);
    }

    @Override
    protected void populateDefaultEquipmentSlots(RandomSource random, DifficultyInstance difficulty) {
        arm();
    }

    /** A black axe of war in his hand, not dropped: the loot table gives his sceptre. */
    private void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.NETHERITE_AXE));
        setDropChance(EquipmentSlot.MAINHAND, 0.0F);
    }

    @Override
    public void tick() {
        super.tick();
        if (!level().isClientSide && tickCount == 1 && getMainHandItem().isEmpty()) {
            arm();
        }
    }

    /** Whether {@code player} carries the eye of Horus anywhere in their inventory. */
    public static boolean carriesEye(Player player) {
        for (ItemStack stack : player.getInventory().items) {
            if (stack.is(EgyptianContent.EYE_OF_HORUS.get())) {
                return true;
            }
        }
        for (ItemStack stack : player.getInventory().offhand) {
            if (stack.is(EgyptianContent.EYE_OF_HORUS.get())) {
                return true;
            }
        }
        return false;
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (!source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)
                && !(source.getEntity() instanceof Player player && carriesEye(player))) {
            amount *= WITHOUT_EYE;
        }
        return super.hurt(source, amount);
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        LivingEntity target = getTarget();
        if (target == null || !(level() instanceof ServerLevel server)) {
            return;
        }
        if (--stormCooldown <= 0 && distanceToSqr(target) < STORM_RADIUS * STORM_RADIUS) {
            stormCooldown = enraged() ? 90 : 140;
            sandstorm(server);
        }
        if (--stepCooldown <= 0 && distanceToSqr(target) > 36.0) {
            stepCooldown = 200;
            stepBehind(server, target);
        }
        if (!calledJackals && enraged()) {
            calledJackals = true;
            callJackals(server);
        }
    }

    /** The storm of Set: everyone around is wounded and thrown back, and blinded unless they carry the eye. */
    public int sandstorm(ServerLevel server) {
        int struck = 0;
        playSound(EgyptianSounds.SANDSTORM.get(), 3.0F, 0.8F);
        server.sendParticles(new BlockParticleOption(ParticleTypes.BLOCK, Blocks.RED_SAND.defaultBlockState()),
                getX(), getY(0.5), getZ(), 160, STORM_RADIUS * 0.4, 1.5, STORM_RADIUS * 0.4, 0.3);
        for (Player player : server.getEntitiesOfClass(Player.class, getBoundingBox().inflate(STORM_RADIUS),
                p -> p.isAlive() && !p.isSpectator() && !p.isCreative())) {
            Vec3 away = player.position().subtract(position()).multiply(1.0, 0.0, 1.0);
            if (away.lengthSqr() < 1.0E-4) {
                away = new Vec3(1.0, 0.0, 0.0);
            }
            away = away.normalize().scale(1.4);
            player.hurt(damageSources().mobAttack(this), 3.0F);
            player.push(away.x, 0.4, away.z);
            player.hurtMarked = true;
            if (carriesEye(player)) {
                player.displayClientMessage(Component.translatable("entity.mythsofworlds.set.eye_guards"), true);
            } else {
                player.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 80, 0), this);
            }
            struck++;
        }
        return struck;
    }

    /** Through the storm, to stand at his foe's back. */
    private void stepBehind(ServerLevel server, LivingEntity target) {
        Vec3 behind = target.position().subtract(target.getLookAngle().multiply(2.5, 0.0, 2.5));
        server.sendParticles(ParticleTypes.LARGE_SMOKE, getX(), getY(0.5), getZ(), 20, 0.5, 1.0, 0.5, 0.02);
        if (randomTeleport(behind.x, target.getY(), behind.z, true)) {
            server.sendParticles(ParticleTypes.LARGE_SMOKE, getX(), getY(0.5), getZ(), 20, 0.5, 1.0, 0.5, 0.02);
            playSound(SoundEvents.ENDERMAN_TELEPORT, 1.5F, 0.5F);
        }
    }

    /** Three jackals of the desert run to their lord. */
    public void callJackals(ServerLevel server) {
        for (int i = 0; i < 3; i++) {
            Jackal jackal = EgyptianEntities.JACKAL.get().create(server);
            if (jackal == null) {
                continue;
            }
            double angle = i * Math.PI * 2.0 / 3.0;
            jackal.moveTo(getX() + Math.cos(angle) * 3.0, getY(), getZ() + Math.sin(angle) * 3.0, getYRot(), 0.0F);
            jackal.finalizeSpawn(server, server.getCurrentDifficultyAt(jackal.blockPosition()), MobSpawnType.MOB_SUMMONED, null);
            jackal.setTarget(getTarget());
            server.addFreshEntity(jackal);
        }
        playSound(SoundEvents.WOLF_HOWL, 3.0F, 1.3F);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("CalledJackals", calledJackals);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        calledJackals = tag.getBoolean("CalledJackals");
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
        return SoundEvents.WITHER_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.8F;
    }
}
