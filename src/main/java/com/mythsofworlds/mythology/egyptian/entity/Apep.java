package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import com.mythsofworlds.mythology.egyptian.EgyptianSounds;
import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.AreaEffectCloud;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Apep, the great serpent of chaos who lies in wait in the lake of fire to swallow the barque of Ra every night. Its
 * bite is a deadly venom; from afar it spits venom that pools on the ground; its tail sweeps away whoever comes too
 * close; below half health it calls swarms of scarabs. Fire cannot hurt it. In the myth Ra, in the shape of a great
 * cat, slew Apep: the serpent takes only half the harm from a hero who has no tame cat of Bastet within
 * {@link #CAT_RANGE} blocks, and half as much again from one who has; the cats themselves bite it four times as hard.
 */
public class Apep extends GreekBoss {
    public static final double CAT_RANGE = 16.0;
    public static final float WITHOUT_CAT = 0.5F;
    public static final float WITH_CAT = 1.5F;

    private int spitCooldown = 60;
    private int sweepCooldown = 100;
    private int swarmCooldown = 100;

    public Apep(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.PURPLE, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 600.0)
                .add(Attributes.ATTACK_DAMAGE, 15.0)
                .add(Attributes.ATTACK_KNOCKBACK, 1.0)
                .add(Attributes.MOVEMENT_SPEED, 0.28)
                .add(Attributes.ARMOR, 12.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.FOLLOW_RANGE, 40.0)
                .add(Attributes.STEP_HEIGHT, 1.5);
    }

    /** Whether {@code player} has a tame cat of Bastet of their own nearby. */
    public static boolean hasCat(Player player) {
        return !player.level().getEntitiesOfClass(BastetCat.class, player.getBoundingBox().inflate(CAT_RANGE),
                cat -> cat.isTame() && player.getUUID().equals(cat.getOwnerUUID()) && cat.isAlive()).isEmpty();
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (!source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) {
            if (source.getEntity() instanceof BastetCat) {
                amount *= 4.0F;
            } else if (source.getEntity() instanceof Player player) {
                amount *= hasCat(player) ? WITH_CAT : WITHOUT_CAT;
            } else {
                amount *= WITHOUT_CAT;
            }
        }
        return super.hurt(source, amount);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.POISON, 120, 1), this);
        }
        return hit;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        LivingEntity target = getTarget();
        if (target == null || !(level() instanceof ServerLevel server)) {
            return;
        }
        double distance = distanceToSqr(target);
        if (--spitCooldown <= 0 && distance > 25.0 && distance < 900.0 && hasLineOfSight(target)) {
            spitCooldown = enraged() ? 40 : 70;
            spit(server, target);
        }
        if (--sweepCooldown <= 0 && distance < 25.0) {
            sweepCooldown = 120;
            sweep(server);
        }
        if (enraged() && --swarmCooldown <= 0) {
            swarmCooldown = 400;
            swarm(server);
        }
    }

    /** A pool of venom where the target stands. */
    public void spit(ServerLevel server, LivingEntity target) {
        AreaEffectCloud cloud = new AreaEffectCloud(server, target.getX(), target.getY(), target.getZ());
        cloud.setOwner(this);
        cloud.setRadius(2.5F);
        cloud.setRadiusOnUse(-0.3F);
        cloud.setWaitTime(5);
        cloud.setDuration(120);
        cloud.setRadiusPerTick(-cloud.getRadius() / cloud.getDuration());
        cloud.addEffect(new MobEffectInstance(MobEffects.POISON, 100, 1));
        server.addFreshEntity(cloud);
        Vec3 from = new Vec3(getX(), getY(0.9), getZ());
        Vec3 step = target.position().add(0.0, 1.0, 0.0).subtract(from).scale(1.0 / 12.0);
        for (int i = 1; i <= 12; i++) {
            server.sendParticles(ParticleTypes.ITEM_SLIME, from.x + step.x * i, from.y + step.y * i, from.z + step.z * i,
                    2, 0.05, 0.05, 0.05, 0.0);
        }
        playSound(EgyptianSounds.APEP_HISS.get(), 2.0F, 1.0F);
    }

    /** The tail sweeps everyone close by far away. */
    public int sweep(ServerLevel server) {
        int struck = 0;
        for (Player player : server.getEntitiesOfClass(Player.class, getBoundingBox().inflate(4.0),
                p -> p.isAlive() && !p.isSpectator() && !p.isCreative())) {
            Vec3 away = player.position().subtract(position()).multiply(1.0, 0.0, 1.0);
            if (away.lengthSqr() < 1.0E-4) {
                away = new Vec3(1.0, 0.0, 0.0);
            }
            away = away.normalize().scale(2.2);
            player.hurt(damageSources().mobAttack(this), 6.0F);
            player.push(away.x, 0.5, away.z);
            player.hurtMarked = true;
            struck++;
        }
        server.sendParticles(ParticleTypes.SWEEP_ATTACK, getX(), getY(0.3), getZ(), 6, 2.0, 0.2, 2.0, 0.0);
        playSound(SoundEvents.PLAYER_ATTACK_SWEEP, 2.0F, 0.5F);
        return struck;
    }

    /** Four scarabs crawl out of the ground. */
    public void swarm(ServerLevel server) {
        for (int i = 0; i < 4; i++) {
            Scarab scarab = EgyptianEntities.SCARAB.get().create(server);
            if (scarab == null) {
                continue;
            }
            double angle = random.nextDouble() * Math.PI * 2.0;
            scarab.moveTo(getX() + Math.cos(angle) * 3.0, getY(), getZ() + Math.sin(angle) * 3.0, random.nextFloat() * 360.0F, 0.0F);
            scarab.finalizeSpawn(server, server.getCurrentDifficultyAt(scarab.blockPosition()), MobSpawnType.MOB_SUMMONED, null);
            scarab.setTarget(getTarget());
            server.addFreshEntity(scarab);
        }
        playSound(SoundEvents.SILVERFISH_AMBIENT, 2.0F, 0.6F);
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return EgyptianSounds.APEP_HISS.get();
    }

    @Override
    protected float getSoundVolume() {
        return 1.5F;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.ENDER_DRAGON_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.ENDER_DRAGON_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.7F;
    }
}
