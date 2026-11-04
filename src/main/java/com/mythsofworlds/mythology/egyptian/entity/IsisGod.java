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
import net.minecraft.world.level.Level;

/**
 * Isis, the great of magic, on the throne of her temple on the Nile. She beats her winged arms and the wind throws
 * back everyone around her, and with the words that healed Horus she heals herself. She drops a wing of Isis.
 */
public class IsisGod extends EgyptianGod {
    public static final double WING_RADIUS = 9.0;

    public IsisGod(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.BLUE, EgyptianContent.SCEPTRE_OF_ISIS);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 360.0)
                .add(Attributes.ATTACK_DAMAGE, 10.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected int powerInterval() {
        return 120;
    }

    @Override
    public void power(ServerLevel server, LivingEntity target) {
        wings(server);
        heal(enraged() ? 24.0F : 12.0F);
        server.sendParticles(ParticleTypes.HEART, getX(), getY(1.1), getZ(), 6, 0.5, 0.4, 0.5, 0.1);
    }

    /** The wind of her wings throws back and slows everyone around. Returns how many were struck. */
    public int wings(ServerLevel server) {
        int struck = 0;
        for (Player player : foesAround(server, WING_RADIUS)) {
            throwBack(player, 1.6, 0.6);
            player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1), this);
            struck++;
        }
        server.sendParticles(ParticleTypes.CLOUD, getX(), getY(0.6), getZ(), 40, 2.5, 0.6, 2.5, 0.15);
        playSound(SoundEvents.PHANTOM_FLAP, 3.0F, 0.6F);
        return struck;
    }

    @Override
    public float getVoicePitch() {
        return 1.3F;
    }
}
