package com.mythsofworlds.mythology.slavic;

import com.mythsofworlds.mythology.relic.RelicArmorItem;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;

/** What the Slavic relics do while worn (see {@link RelicArmorItem}). */
public final class SlavicRelics {
    private SlavicRelics() {
    }

    /** Seven-league boots: Speed III and Jump Boost. */
    public static void skorokhody(Player player) {
        if (player.tickCount % 20 == 0) {
            RelicArmorItem.keep(player, MobEffects.MOVEMENT_SPEED, 2);
            RelicArmorItem.keep(player, MobEffects.JUMP, 0);
        }
    }

    /** Cap of invisibility: while you crouch, you cannot be seen. */
    public static void shapka(Player player) {
        if (player.isShiftKeyDown() && player.tickCount % 5 == 0) {
            player.addEffect(new MobEffectInstance(MobEffects.INVISIBILITY, 15, 0, true, false, true));
        }
    }
}
