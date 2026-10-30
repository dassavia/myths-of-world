package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.mythology.norse.NorseSounds;
import com.mythsofworlds.core.entity.MythBoss;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
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
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * Heimdall, the watchman of the gods, guarding the end of the Bifrost at Himinbjorg. He sees a hundred leagues and
 * hears the grass grow: arrows he sees coming hurt him only a third as much, and nothing sneaks up on him. Every few
 * seconds he blows the Gjallarhorn, and the blast throws back, slows and stuns everyone around him; at half health he
 * blows it twice as often. He drops his all-seeing eye.
 */
public class Heimdall extends MythBoss {
    public static final double HORN_RADIUS = 14.0;

    private int hornCooldown = 160;

    public Heimdall(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.YELLOW, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 450.0)
                .add(Attributes.ATTACK_DAMAGE, 13.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 12.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8)
                .add(Attributes.FOLLOW_RANGE, 48.0)
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

    /** Hofund, his golden sword, and a gilded helmet. */
    private void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.GOLDEN_SWORD));
        setItemSlot(EquipmentSlot.HEAD, new ItemStack(Items.GOLDEN_HELMET));
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
            amount /= 3.0F;
        }
        return super.hurt(source, amount);
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        LivingEntity target = getTarget();
        if (target != null && --hornCooldown <= 0 && distanceToSqr(target) < HORN_RADIUS * HORN_RADIUS
                && level() instanceof ServerLevel server) {
            hornCooldown = enraged() ? 100 : 200;
            blowHorn(server);
        }
    }

    /** The Gjallarhorn: everyone within {@link #HORN_RADIUS} blocks is thrown back, slowed and stunned. */
    public void blowHorn(ServerLevel server) {
        playSpecial();
        server.playSound(null, blockPosition(), NorseSounds.GJALLARHORN.get(), getSoundSource(), 4.0F, 1.0F);
        server.sendParticles(ParticleTypes.SONIC_BOOM, getX(), getY(0.6), getZ(), 1, 0.0, 0.0, 0.0, 0.0);
        for (Player player : server.getEntitiesOfClass(Player.class, getBoundingBox().inflate(HORN_RADIUS),
                p -> p.isAlive() && !p.isSpectator() && !p.isCreative())) {
            Vec3 away = player.position().subtract(position()).multiply(1.0, 0.0, 1.0);
            if (away.lengthSqr() < 1.0E-4) {
                away = new Vec3(1.0, 0.0, 0.0);
            }
            away = away.normalize().scale(1.6);
            player.push(away.x, 0.5, away.z);
            player.hurtMarked = true;
            player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 80, 1));
            player.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 120, 0));
            player.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0));
        }
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.VINDICATOR_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.VINDICATOR_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.VINDICATOR_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.7F;
    }
}
