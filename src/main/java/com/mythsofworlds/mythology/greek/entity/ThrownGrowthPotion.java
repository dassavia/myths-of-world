package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.projectile.ThrowableItemProjectile;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.LevelEvent;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/** The thrown splash potion of growth. Where it bursts, every young creature within {@link #RADIUS} grows up. */
public class ThrownGrowthPotion extends ThrowableItemProjectile {
    public static final double RADIUS = 4.0;
    public static final int COLOR = 0x7FD05A;

    public ThrownGrowthPotion(EntityType<? extends ThrownGrowthPotion> type, Level level) {
        super(type, level);
    }

    public ThrownGrowthPotion(Level level, LivingEntity thrower) {
        super(GreekEntities.GROWTH_POTION.get(), thrower, level);
    }

    @Override
    protected Item getDefaultItem() {
        return GreekContent.GROWTH_POTION.get();
    }

    @Override
    protected double getDefaultGravity() {
        return 0.05;
    }

    @Override
    protected void onHit(HitResult result) {
        super.onHit(result);
        if (level() instanceof ServerLevel server) {
            burst(server, result.getLocation());
            discard();
        }
    }

    /** Grows up every baby around the point and returns how many there were. */
    public static int burst(ServerLevel level, Vec3 at) {
        level.levelEvent(LevelEvent.PARTICLES_SPELL_POTION_SPLASH, BlockPos.containing(at), COLOR);
        int grown = 0;
        for (Mob mob : level.getEntitiesOfClass(Mob.class, new AABB(at, at).inflate(RADIUS, RADIUS / 2.0, RADIUS), Mob::isBaby)) {
            mob.setBaby(false);
            level.sendParticles(ParticleTypes.HAPPY_VILLAGER, mob.getX(), mob.getY() + mob.getBbHeight() / 2.0, mob.getZ(),
                    10, 0.4, 0.5, 0.4, 0.0);
            grown++;
        }
        return grown;
    }
}
