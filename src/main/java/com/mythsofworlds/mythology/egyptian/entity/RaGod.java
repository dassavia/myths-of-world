package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.BossEvent;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.SmallFireball;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Ra, the falcon-headed sun, king of the gods, standing on the deck of his solar barque on the Celestial Nile. He
 * hurls the fire of the sun disc: three fireballs at his foe, and below half health the eye of Ra blazes and sets
 * everyone around on fire and blinds them. Fire cannot harm him. He drops the sun disc of Ra.
 */
public class RaGod extends EgyptianGod {
    public static final double FLARE_RADIUS = 10.0;
    private boolean flare;

    public RaGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.YELLOW, EgyptianContent.STAFF_OF_RA);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 550.0)
                .add(Attributes.ATTACK_DAMAGE, 14.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.9)
                .add(Attributes.FOLLOW_RANGE, 40.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected int powerInterval() {
        return 70;
    }

    @Override
    public void power(ServerLevel server, LivingEntity target) {
        flare = !flare;
        if (enraged() && flare) {
            sunFlare(server);
        } else {
            fireballs(server, target);
        }
    }

    /** Three fireballs of the sun, fanned out towards the foe. */
    public void fireballs(ServerLevel server, LivingEntity target) {
        Vec3 start = new Vec3(getX(), getEyeY() - 0.3, getZ());
        Vec3 aim = target.getEyePosition().subtract(start).normalize();
        Vec3 side = new Vec3(-aim.z, 0.0, aim.x).scale(0.15);
        for (int i = -1; i <= 1; i++) {
            SmallFireball fireball = new SmallFireball(server, this, aim.add(side.scale(i)).normalize());
            fireball.setPos(start.add(aim.scale(1.2)));
            server.addFreshEntity(fireball);
        }
        playSound(SoundEvents.BLAZE_SHOOT, 2.0F, 0.7F);
    }

    /** The eye of Ra blazes: everyone around burns and is blinded. Returns how many were struck. */
    public int sunFlare(ServerLevel server) {
        int struck = 0;
        for (Player player : foesAround(server, FLARE_RADIUS)) {
            player.setRemainingFireTicks(100);
            player.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 60, 0), this);
            struck++;
        }
        server.sendParticles(ParticleTypes.FLAME, getX(), getY(0.6), getZ(), 120, FLARE_RADIUS * 0.4, 1.2, FLARE_RADIUS * 0.4, 0.05);
        server.sendParticles(ParticleTypes.END_ROD, getX(), getY(1.1), getZ(), 40, 0.6, 0.6, 0.6, 0.2);
        playSound(SoundEvents.FIRECHARGE_USE, 3.0F, 0.6F);
        return struck;
    }

    @Override
    public float getVoicePitch() {
        return 0.7F;
    }
}
