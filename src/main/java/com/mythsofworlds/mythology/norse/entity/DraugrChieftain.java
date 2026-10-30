package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import com.mythsofworlds.mythology.norse.NorseEntities;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.RandomSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import org.jetbrains.annotations.Nullable;

/**
 * The barrow-king, mini-boss of the burial mounds. Arrows glance off his old mail, every few seconds he calls the dead
 * of his barrow to rise, and like every draugr he gets up again unless he is felled with an axe or by fire.
 */
public class DraugrChieftain extends GreekBoss {
    public static final int MAX_GUARDS = 6;

    private int summonCooldown = 100;
    private boolean risen;

    public DraugrChieftain(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.BLUE, true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 350.0)
                .add(Attributes.ATTACK_DAMAGE, 13.0)
                .add(Attributes.MOVEMENT_SPEED, 0.27)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.6)
                .add(Attributes.FOLLOW_RANGE, 24.0);
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

    private void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.IRON_AXE));
        setItemSlot(EquipmentSlot.HEAD, new ItemStack(Items.GOLDEN_HELMET));
        setItemSlot(EquipmentSlot.CHEST, new ItemStack(Items.CHAINMAIL_CHESTPLATE));
        for (EquipmentSlot slot : EquipmentSlot.values()) {
            setDropChance(slot, 0.0F);
        }
    }

    @Override
    public void tick() {
        super.tick();
        if (!level().isClientSide && tickCount == 1 && getMainHandItem().isEmpty()) {
            arm();
        }
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (source.getDirectEntity() != null && source.getDirectEntity() != source.getEntity()) {
            amount *= 0.4F;
        }
        return super.hurt(source, amount);
    }

    @Override
    protected void actuallyHurt(DamageSource source, float amount) {
        super.actuallyHurt(source, amount);
        if (isDeadOrDying() && !risen && !Draugr.laysToRest(source)) {
            risen = true;
            setHealth(getMaxHealth() / 2.0F);
            playSound(SoundEvents.ZOMBIE_VILLAGER_CURE, 1.5F, 0.4F);
            if (level() instanceof ServerLevel server) {
                server.sendParticles(ParticleTypes.SNOWFLAKE, getX(), getY() + 1.0, getZ(), 30, 0.4, 1.0, 0.4, 0.02);
            }
        }
    }

    public boolean hasRisen() {
        return risen;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (getTarget() != null && --summonCooldown <= 0 && level() instanceof ServerLevel server) {
            summonCooldown = enraged() ? 200 : 320;
            int guards = server.getEntitiesOfClass(Draugr.class, getBoundingBox().inflate(16.0)).size();
            for (int i = guards; i < Math.min(MAX_GUARDS, guards + 2); i++) {
                Draugr draugr = NorseEntities.DRAUGR.get().create(server);
                if (draugr == null) {
                    continue;
                }
                double angle = random.nextDouble() * Math.PI * 2.0;
                draugr.moveTo(getX() + Math.cos(angle) * 2.0, getY(), getZ() + Math.sin(angle) * 2.0, getYRot(), 0.0F);
                draugr.finalizeSpawn(server, server.getCurrentDifficultyAt(draugr.blockPosition()), MobSpawnType.MOB_SUMMONED, null);
                draugr.setTarget(getTarget());
                server.addFreshEntity(draugr);
                server.sendParticles(ParticleTypes.SOUL, draugr.getX(), draugr.getY() + 0.5, draugr.getZ(), 10, 0.3, 0.5, 0.3, 0.02);
            }
            playSound(SoundEvents.ZOMBIE_AMBIENT, 2.0F, 0.4F);
        }
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
    public boolean canFreeze() {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.ZOMBIE_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.ZOMBIE_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.ZOMBIE_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.5F;
    }
}
