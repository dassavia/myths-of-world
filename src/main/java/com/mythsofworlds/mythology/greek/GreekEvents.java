package com.mythsofworlds.mythology.greek;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.back.BackSlot;
import com.mythsofworlds.mythology.greek.item.GirdleItem;
import com.mythsofworlds.mythology.greek.item.WingsItem;
import java.util.Map;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.storage.loot.BuiltInLootTables;
import net.minecraft.world.level.storage.loot.LootPool;
import net.minecraft.world.level.storage.loot.entries.LootItem;
import net.minecraft.world.level.storage.loot.predicates.LootItemRandomChanceCondition;
import net.minecraft.world.level.storage.loot.providers.number.ConstantValue;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.LootTableLoadEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

/**
 * Effects of the Greek items a player wears (the wings of Daedalus and the girdle of Hippolyta), and the bident of
 * Hades hidden in the chests of the Nether.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class GreekEvents {
    private GreekEvents() {
    }

    /** Chance of a bident of Hades in each chest of the Nether. */
    public static final Map<ResourceLocation, Float> BIDENT_CHESTS = Map.of(
            BuiltInLootTables.NETHER_BRIDGE.location(), 0.12F,
            BuiltInLootTables.BASTION_OTHER.location(), 0.08F,
            BuiltInLootTables.BASTION_TREASURE.location(), 0.5F);

    @SubscribeEvent
    public static void onLootTableLoad(LootTableLoadEvent event) {
        Float chance = BIDENT_CHESTS.get(event.getName());
        if (chance != null) {
            event.getTable().addPool(LootPool.lootPool()
                    .name(MythsOfWorlds.MODID + ":bident_of_hades")
                    .setRolls(ConstantValue.exactly(1.0F))
                    .add(LootItem.lootTableItem(GreekContent.BIDENT_OF_HADES.get()))
                    .when(LootItemRandomChanceCondition.randomChance(chance))
                    .build());
        }
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
        } else if (BackSlot.get(player).is(GreekContent.WINGS_OF_DAEDALUS.get())) {
            WingsItem.wornTick(player, BackSlot.get(player));
        }
        if (GirdleItem.isWorn(player)) {
            GirdleItem.wornTick(player);
        }
    }
}
