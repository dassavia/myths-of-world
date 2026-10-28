package com.mythsofworlds.registry;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.norse.BifrostRuneItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModItems {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MythsOfWorlds.MODID);

    public static final DeferredItem<BlockItem> RUNESTONE = ITEMS.registerSimpleBlockItem(ModBlocks.RUNESTONE);

    public static final DeferredItem<BifrostRuneItem> BIFROST_RUNE = ITEMS.register("bifrost_rune",
            () -> new BifrostRuneItem(new Item.Properties().durability(16).rarity(Rarity.RARE)));

    private ModItems() {
    }
}
