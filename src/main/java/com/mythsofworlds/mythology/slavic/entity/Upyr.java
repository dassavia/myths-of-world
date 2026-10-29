package com.mythsofworlds.mythology.slavic.entity;

import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.level.Level;
import org.joml.Vector3f;

/**
 * Upyr, the blood-drinking dead of the old tales. Every bite heals it by {@link #DRINK} health. The sun burns it,
 * as it burns all the restless dead; it never rises as a baby or drowns into anything else.
 */
public class Upyr extends Zombie {
    public static final float DRINK = 4.0F;
    private static final DustParticleOptions BLOOD = new DustParticleOptions(new Vector3f(0.6F, 0.05F, 0.05F), 1.0F);

    public Upyr(EntityType<? extends Zombie> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Zombie.createAttributes()
                .add(Attributes.MAX_HEALTH, 28.0)
                .add(Attributes.ATTACK_DAMAGE, 5.0)
                .add(Attributes.MOVEMENT_SPEED, 0.27)
                .add(Attributes.SPAWN_REINFORCEMENTS_CHANCE, 0.0);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit) {
            heal(DRINK);
            if (level() instanceof ServerLevel server) {
                server.sendParticles(BLOOD, target.getX(), target.getY(0.6), target.getZ(), 8, 0.2, 0.3, 0.2, 0.0);
            }
        }
        return hit;
    }

    @Override
    protected boolean convertsInWater() {
        return false;
    }

    @Override
    public void setBaby(boolean baby) {
    }

    @Override
    public float getVoicePitch() {
        return super.getVoicePitch() * 0.8F;
    }
}
