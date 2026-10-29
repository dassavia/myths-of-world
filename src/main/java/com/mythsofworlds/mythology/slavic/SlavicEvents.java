package com.mythsofworlds.mythology.slavic;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.relic.RelicArmorItem;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

/** Small game rules of Nav: the Firebird's feather lights the dusk for whoever holds it. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class SlavicEvents {
    private SlavicEvents() {
    }

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        Player player = event.getEntity();
        if (player.level().isClientSide || player.tickCount % 20 != 0) {
            return;
        }
        if (player.getMainHandItem().is(SlavicContent.FIREBIRD_FEATHER.get())
                || player.getOffhandItem().is(SlavicContent.FIREBIRD_FEATHER.get())) {
            RelicArmorItem.keep(player, MobEffects.NIGHT_VISION, 0);
        }
    }
}
