package com.mythsofworlds.mythology.slavic.entity;

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
 * Solovei the Robber (Соловей-разбойник), who sits in his nest on nine oaks over the road. His whistle is a storm:
 * every few seconds everyone within {@link #WHISTLE_RADIUS} blocks is hurt, thrown far back and dazed. He drops the
 * seven-league boots.
 */
public class Solovei extends MythBoss {
    public static final double WHISTLE_RADIUS = 16.0;

    private int whistleCooldown = 120;

    public Solovei(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.GREEN, true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 300.0)
                .add(Attributes.ATTACK_DAMAGE, 11.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.6)
                .add(Attributes.FOLLOW_RANGE, 32.0)
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

    /** A robber's axe, not dropped. */
    private void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.IRON_AXE));
        setDropChance(EquipmentSlot.MAINHAND, 0.0F);
    }

    @Override
    public void tick() {
        super.tick();
        if (!level().isClientSide && tickCount == 1 && getMainHandItem().isEmpty()) {
            arm();
        }
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        LivingEntity target = getTarget();
        if (target != null && --whistleCooldown <= 0 && distanceToSqr(target) < WHISTLE_RADIUS * WHISTLE_RADIUS
                && level() instanceof ServerLevel server) {
            whistleCooldown = enraged() ? 90 : 160;
            whistle(server);
        }
    }

    /** The robber's whistle: everyone around is hurt, thrown back and dazed. */
    public void whistle(ServerLevel server) {
        server.playSound(null, blockPosition(), SoundEvents.WARDEN_SONIC_BOOM, getSoundSource(), 3.0F, 1.6F);
        server.sendParticles(ParticleTypes.SONIC_BOOM, getX(), getY(0.8), getZ(), 1, 0.0, 0.0, 0.0, 0.0);
        server.sendParticles(ParticleTypes.CLOUD, getX(), getY(0.8), getZ(), 40, 3.0, 1.0, 3.0, 0.2);
        for (Player player : server.getEntitiesOfClass(Player.class, getBoundingBox().inflate(WHISTLE_RADIUS),
                p -> p.isAlive() && !p.isSpectator() && !p.isCreative())) {
            Vec3 away = player.position().subtract(position()).multiply(1.0, 0.0, 1.0);
            if (away.lengthSqr() < 1.0E-4) {
                away = new Vec3(1.0, 0.0, 0.0);
            }
            away = away.normalize().scale(2.4);
            player.hurt(damageSources().sonicBoom(this), 4.0F);
            player.push(away.x, 0.7, away.z);
            player.hurtMarked = true;
            player.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 160, 0));
            player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
        }
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.PILLAGER_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.PILLAGER_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.PILLAGER_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.8F;
    }
}
