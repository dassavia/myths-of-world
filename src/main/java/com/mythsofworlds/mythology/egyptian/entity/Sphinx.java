package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianSounds;
import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;

/**
 * The Great Sphinx, a lion of stone with the head of a king that guards the sands of the Duat. It lies still and lets
 * travellers pass, until someone strikes it. Then it roars, throwing back everyone within {@link #ROAR_RADIUS}
 * blocks, and leaps on its foes; below half health its roar raises a blinding cloud of sand. Its body is stone:
 * arrows and other shots only scratch it (half damage), but a pickaxe breaks the stone (twice the damage). It drops
 * its nemes and its claws.
 */
public class Sphinx extends GreekBoss {
    public static final double ROAR_RADIUS = 10.0;

    private int roarCooldown = 60;
    private int leapCooldown = 80;

    public Sphinx(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.YELLOW, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 350.0)
                .add(Attributes.ATTACK_DAMAGE, 13.0)
                .add(Attributes.ATTACK_KNOCKBACK, 1.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.5);
    }

    /** The guardian does not attack first. */
    @Override
    protected boolean hostile() {
        return false;
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (source.is(DamageTypeTags.IS_PROJECTILE)) {
            amount *= 0.5F;
        } else if (source.getWeaponItem() != null && source.getWeaponItem().is(ItemTags.PICKAXES)) {
            amount *= 2.0F;
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
        double distance = distanceToSqr(target);
        if (--roarCooldown <= 0 && distance < ROAR_RADIUS * ROAR_RADIUS) {
            roarCooldown = enraged() ? 100 : 160;
            roar(server);
        }
        if (--leapCooldown <= 0) {
            leapCooldown = 20;
            if (onGround() && distance > 16.0 && distance < 256.0) {
                Vec3 jump = new Vec3(target.getX() - getX(), 0.0, target.getZ() - getZ()).normalize().scale(1.3);
                setDeltaMovement(jump.x, 0.55, jump.z);
                hurtMarked = true;
                leapCooldown = 100;
            }
        }
    }

    /** The roar of the Sphinx: everyone around is thrown back and slowed, and blinded once it is enraged. */
    public int roar(ServerLevel server) {
        int struck = 0;
        playSound(EgyptianSounds.SPHINX_ROAR.get(), 3.0F, 1.0F);
        server.sendParticles(new BlockParticleOption(ParticleTypes.BLOCK, Blocks.SAND.defaultBlockState()),
                getX(), getY(0.5), getZ(), 80, 3.0, 0.6, 3.0, 0.2);
        for (Player player : server.getEntitiesOfClass(Player.class, getBoundingBox().inflate(ROAR_RADIUS),
                p -> p.isAlive() && !p.isSpectator() && !p.isCreative())) {
            Vec3 away = player.position().subtract(position()).multiply(1.0, 0.0, 1.0);
            if (away.lengthSqr() < 1.0E-4) {
                away = new Vec3(1.0, 0.0, 0.0);
            }
            away = away.normalize().scale(2.0);
            player.push(away.x, 0.6, away.z);
            player.hurtMarked = true;
            player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 80, 1), this);
            if (enraged()) {
                player.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 60, 0), this);
            }
            struck++;
        }
        return struck;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return getTarget() != null ? SoundEvents.RAVAGER_AMBIENT : null;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.STONE_HIT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.RAVAGER_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.6F;
    }
}
