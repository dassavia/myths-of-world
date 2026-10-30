package com.mythsofworlds.mythology.relic;

import com.mythsofworlds.core.ServerConfig;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;

/** What each relic does while worn (see {@link RelicArmorItem}). */
public final class Relics {
    private Relics() {
    }

    /** Winged sandals of Hermes: the messenger of the gods is swift, leaps high and never falls hard. */
    public static void talaria(Player player) {
        player.resetFallDistance();
        if (player.tickCount % 20 == 0) {
            RelicArmorItem.keep(player, MobEffects.MOVEMENT_SPEED, 1);
            RelicArmorItem.keep(player, MobEffects.JUMP, 1);
        }
    }

    /** Breastplate of a Titan, forged for the giants who held up the sky: strength and endurance. */
    public static void titan(Player player) {
        if (player.tickCount % 20 == 0) {
            RelicArmorItem.keep(player, MobEffects.DAMAGE_BOOST, 0);
            RelicArmorItem.keep(player, MobEffects.DAMAGE_RESISTANCE, 0);
        }
    }

    /** How often the helmet of Heimdall looks around, in ticks; the glow lasts a little longer so that it never flickers. */
    public static final int HEIMDALL_PERIOD = 40;

    /** How far the helmet of Heimdall sees, in blocks ({@code heimdallRange} in the server config, 100 by default). */
    public static double heimdallRange() {
        return ServerConfig.get(ServerConfig.HEIMDALL_RANGE);
    }

    /** Helmet set with the eye of Heimdall, who sees a hundred leagues by night and day: night vision, and every
     *  creature within {@link #heimdallRange()} blocks glows through the walls. A creature that still glows (another
     *  wearer saw it a moment ago) is skipped, so that crowded servers do not resend the effect over and over. */
    public static void heimdall(Player player) {
        if (player.tickCount % HEIMDALL_PERIOD == 0) {
            RelicArmorItem.keep(player, MobEffects.NIGHT_VISION, 0);
            double range = heimdallRange();
            for (Mob mob : player.level().getEntitiesOfClass(Mob.class, player.getBoundingBox().inflate(range),
                    mob -> mob.isAlive() && mob.distanceToSqr(player) < range * range)) {
                MobEffectInstance glow = mob.getEffect(MobEffects.GLOWING);
                if (glow == null || glow.getDuration() < HEIMDALL_PERIOD / 2) {
                    mob.addEffect(new MobEffectInstance(MobEffects.GLOWING, HEIMDALL_PERIOD + 20, 0, true, false));
                }
            }
        }
    }
}
