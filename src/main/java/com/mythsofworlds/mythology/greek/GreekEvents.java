package com.mythsofworlds.mythology.greek;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.item.GirdleItem;
import com.mythsofworlds.mythology.greek.item.WingsItem;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

/** Effects of the Greek items a player wears: the wings of Daedalus and the girdle of Hippolyta. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class GreekEvents {
    private GreekEvents() {
    }

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        Player player = event.getEntity();
        if (player.level().isClientSide) {
            return;
        }
        ItemStack chest = player.getItemBySlot(EquipmentSlot.CHEST);
        if (chest.is(GreekContent.WINGS_OF_DAEDALUS.get())) {
            WingsItem.wornTick(player, chest);
        }
        if (GirdleItem.isWorn(player)) {
            GirdleItem.wornTick(player);
        }
    }
}
