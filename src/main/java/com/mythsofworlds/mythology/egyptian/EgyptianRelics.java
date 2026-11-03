package com.mythsofworlds.mythology.egyptian;

import com.mythsofworlds.mythology.relic.RelicArmorItem;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;

/** What the Egyptian relics do while worn (see {@link RelicArmorItem}). */
public final class EgyptianRelics {
    private EgyptianRelics() {
    }

    /** Nemes of the Sphinx: Night Vision, for the night of the Duat never ends. */
    public static void nemes(Player player) {
        if (player.tickCount % 20 == 0) {
            RelicArmorItem.keep(player, MobEffects.NIGHT_VISION, 0);
        }
    }

    /** Pectoral of Ra: Fire Resistance and Strength. */
    public static void pectoral(Player player) {
        if (player.tickCount % 20 == 0) {
            RelicArmorItem.keep(player, MobEffects.FIRE_RESISTANCE, 0);
            RelicArmorItem.keep(player, MobEffects.DAMAGE_BOOST, 0);
        }
    }
}
