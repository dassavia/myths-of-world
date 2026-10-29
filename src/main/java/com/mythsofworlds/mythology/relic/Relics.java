package com.mythsofworlds.mythology.relic;

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

    /** Helmet set with the eye of Heimdall, who sees a hundred leagues by night and day: night vision, and every
     *  creature within 32 blocks glows through the walls. */
    public static void heimdall(Player player) {
        if (player.tickCount % 20 == 0) {
            RelicArmorItem.keep(player, MobEffects.NIGHT_VISION, 0);
            for (Mob mob : player.level().getEntitiesOfClass(Mob.class, player.getBoundingBox().inflate(32.0),
                    Mob::isAlive)) {
                mob.addEffect(new MobEffectInstance(MobEffects.GLOWING, 40, 0, true, false));
            }
        }
    }
}
