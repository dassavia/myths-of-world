package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
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
import net.minecraft.world.entity.projectile.SmallFireball;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Sekhmet, the lioness of slaughter, the eye of Ra sent to punish mankind, in her shrine by the Lake of Fire. She
 * hunts every stranger on sight. Her breath is the hot desert wind: a fireball and a plague of hunger and poison on
 * everyone around. Below half health her bloodlust makes her stronger. Fire cannot harm her. She drops an ember of
 * Sekhmet.
 */
public class SekhmetGod extends EgyptianGod {
    public static final double PLAGUE_RADIUS = 8.0;

    public SekhmetGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.RED, EgyptianContent.SPEAR_OF_SEKHMET);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 480.0)
                .add(Attributes.ATTACK_DAMAGE, 15.0)
                .add(Attributes.MOVEMENT_SPEED, 0.34)
                .add(Attributes.ARMOR, 8.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.9)
                .add(Attributes.FOLLOW_RANGE, 40.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected boolean hostile() {
        return true;
    }

    @Override
    protected int powerInterval() {
        return 100;
    }

    @Override
    public void power(ServerLevel server, LivingEntity target) {
        Vec3 start = new Vec3(getX(), getEyeY() - 0.3, getZ());
        Vec3 aim = target.getEyePosition().subtract(start).normalize();
        SmallFireball fireball = new SmallFireball(server, this, aim);
        fireball.setPos(start.add(aim.scale(1.2)));
        server.addFreshEntity(fireball);
        plague(server);
        if (enraged()) {
            addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, 200, 1), this);
        }
    }

    /** The breath of Sekhmet: hunger and poison on everyone around. Returns how many were struck. */
    public int plague(ServerLevel server) {
        int struck = 0;
        for (Player player : foesAround(server, PLAGUE_RADIUS)) {
            player.addEffect(new MobEffectInstance(MobEffects.HUNGER, 200, 1), this);
            player.addEffect(new MobEffectInstance(MobEffects.POISON, 60, 0), this);
            struck++;
        }
        server.sendParticles(ParticleTypes.FLAME, getX(), getY(0.5), getZ(), 60, PLAGUE_RADIUS * 0.4, 0.6, PLAGUE_RADIUS * 0.4, 0.03);
        playSound(SoundEvents.RAVAGER_ROAR, 2.5F, 1.2F);
        return struck;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.RAVAGER_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.RAVAGER_HURT;
    }

    @Override
    public float getVoicePitch() {
        return 1.2F;
    }
}
