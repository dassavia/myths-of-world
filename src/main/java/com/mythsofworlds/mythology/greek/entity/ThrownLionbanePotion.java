package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.ThrowableItemProjectile;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.LevelEvent;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * The thrown splash potion of lionbane. Where it bursts, every Nemean Lion within {@link #RADIUS} takes a sixth of
 * its full health and a little more as magic, which its hide does not stop: six bottles bring down a full-health lion.
 */
public class ThrownLionbanePotion extends ThrowableItemProjectile {
    public static final double RADIUS = 4.0;
    public static final int COLOR = 0xE8A21E;
    /** How many bottles kill a lion at full health. */
    public static final int BOTTLES_TO_KILL = 6;

    public ThrownLionbanePotion(EntityType<? extends ThrownLionbanePotion> type, Level level) {
        super(type, level);
    }

    public ThrownLionbanePotion(Level level, LivingEntity thrower) {
        super(GreekEntities.LIONBANE_POTION.get(), thrower, level);
    }

    @Override
    protected Item getDefaultItem() {
        return GreekContent.LIONBANE_POTION.get();
    }

    @Override
    protected double getDefaultGravity() {
        return 0.05;
    }

    @Override
    protected void onHit(HitResult result) {
        super.onHit(result);
        if (level() instanceof ServerLevel server) {
            burst(server, result.getLocation(), this, getOwner());
            discard();
        }
    }

    /** A sixth of the lion's full health and one point more, so that six bottles always finish it. */
    public static float damageTo(LivingEntity lion) {
        return lion.getMaxHealth() / BOTTLES_TO_KILL + 1.0F;
    }

    /** Burns every Nemean Lion around the point and returns how many were hit. */
    public static int burst(ServerLevel level, Vec3 at, @Nullable Entity potion, @Nullable Entity thrower) {
        level.levelEvent(LevelEvent.PARTICLES_SPELL_POTION_SPLASH, BlockPos.containing(at), COLOR);
        int hit = 0;
        for (NemeanLion lion : level.getEntitiesOfClass(NemeanLion.class, new AABB(at, at).inflate(RADIUS, RADIUS / 2.0, RADIUS),
                LivingEntity::isAlive)) {
            DamageSource source = level.damageSources().indirectMagic(potion == null ? lion : potion, thrower);
            // Each bottle counts in full, even when two burst within the same second.
            lion.invulnerableTime = 0;
            lion.hurt(source, damageTo(lion));
            level.sendParticles(ParticleTypes.FLAME, lion.getX(), lion.getY() + lion.getBbHeight() / 2.0, lion.getZ(),
                    20, 0.6, 0.6, 0.6, 0.02);
            hit++;
        }
        return hit;
    }
}
