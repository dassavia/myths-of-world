package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import com.mythsofworlds.mythology.norse.NorseContent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.RandomSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.SmallFireball;
import net.minecraft.world.entity.projectile.Snowball;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.block.BaseFireBlock;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * Surtr, lord of Muspelheim, in his fortress over the lava. His flaming sword burns, he hurls fire, and every few
 * seconds the ground around him bursts into flame. Below half health fire rains from the sky on his foes. Like all
 * of Muspel's sons he fears water and snow: snowballs hurt him, rain and water burn him, and Thor's lightning
 * strikes him twice as hard.
 */
public class Surtr extends GreekBoss {
    public static final int FIRE_RING_RADIUS = 4;

    private int fireballCooldown = 60;
    private int ringCooldown = 160;
    private int rainCooldown = 100;

    public Surtr(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.RED, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 550.0)
                .add(Attributes.ATTACK_DAMAGE, 16.0)
                .add(Attributes.ATTACK_KNOCKBACK, 1.5)
                .add(Attributes.MOVEMENT_SPEED, 0.27)
                .add(Attributes.ARMOR, 12.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.FOLLOW_RANGE, 36.0)
                .add(Attributes.STEP_HEIGHT, 1.5);
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

    /** He carries his sword, but it is not dropped from his hand: the loot table gives it. */
    private void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(NorseContent.SURTR_SWORD.get()));
        setDropChance(EquipmentSlot.MAINHAND, 0.0F);
    }

    @Override
    public void tick() {
        super.tick();
        if (!level().isClientSide && tickCount == 1 && getMainHandItem().isEmpty()) {
            arm();
        }
        if (level().isClientSide && random.nextInt(3) == 0) {
            level().addParticle(ParticleTypes.FLAME, getRandomX(0.6), getRandomY(), getRandomZ(0.6), 0.0, 0.02, 0.0);
        }
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit) {
            target.igniteForSeconds(8.0F);
        }
        return hit;
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (source.getDirectEntity() instanceof Snowball) {
            amount = Math.max(amount, 5.0F);
        }
        if (source.getDirectEntity() instanceof LightningBolt) {
            amount *= 2.0F;
        }
        return super.hurt(source, amount);
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (!(level() instanceof ServerLevel server)) {
            return;
        }
        LivingEntity target = getTarget();
        if (target == null) {
            return;
        }
        if (--fireballCooldown <= 0) {
            fireballCooldown = 20;
            if (distanceToSqr(target) > 9.0 && distanceToSqr(target) < 900.0 && hasLineOfSight(target)) {
                FireGiant.throwFire(this, target);
                fireballCooldown = enraged() ? 40 : 70;
            }
        }
        if (--ringCooldown <= 0) {
            ringCooldown = 200;
            ringOfFire(server);
        }
        if (enraged() && --rainCooldown <= 0) {
            rainCooldown = 60;
            for (Player player : server.getEntitiesOfClass(Player.class, getBoundingBox().inflate(24.0),
                    p -> !p.isCreative() && !p.isSpectator())) {
                rainFire(server, player);
            }
        }
    }

    /** Sets the ground around him alight. */
    public void ringOfFire(ServerLevel server) {
        BlockPos centre = blockPosition();
        for (int dx = -FIRE_RING_RADIUS; dx <= FIRE_RING_RADIUS; dx++) {
            for (int dz = -FIRE_RING_RADIUS; dz <= FIRE_RING_RADIUS; dz++) {
                double r = Math.sqrt(dx * dx + dz * dz);
                if (r < 2.0 || r > FIRE_RING_RADIUS + 0.5 || random.nextInt(3) == 0) {
                    continue;
                }
                BlockPos pos = centre.offset(dx, 0, dz);
                if (server.getBlockState(pos).isAir() && BaseFireBlock.canBePlacedAt(server, pos, Direction.UP)) {
                    server.setBlockAndUpdate(pos, BaseFireBlock.getState(server, pos));
                }
            }
        }
        server.sendParticles(ParticleTypes.LAVA, getX(), getY() + 0.5, getZ(), 20, 2.0, 0.2, 2.0, 0.0);
        playSound(SoundEvents.FIRECHARGE_USE, 2.0F, 0.5F);
    }

    /** A fireball falling on the player from high above. */
    private void rainFire(ServerLevel server, Player player) {
        Vec3 start = player.position().add(random.nextGaussian() * 2.0, 14.0, random.nextGaussian() * 2.0);
        SmallFireball fireball = new SmallFireball(server, this, player.position().subtract(start).normalize());
        fireball.setPos(start);
        server.addFreshEntity(fireball);
    }

    @Override
    public boolean isSensitiveToWater() {
        return true;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.BLAZE_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.BLAZE_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.WITHER_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.4F;
    }
}
