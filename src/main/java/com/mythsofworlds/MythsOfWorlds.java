package com.mythsofworlds;

import com.mythsofworlds.registry.ModBlocks;
import com.mythsofworlds.registry.ModCreativeTabs;
import com.mythsofworlds.registry.ModItems;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(MythsOfWorlds.MODID)
public final class MythsOfWorlds {
    public static final String MODID = "mythsofworlds";

    public MythsOfWorlds(IEventBus modBus) {
        ModBlocks.BLOCKS.register(modBus);
        ModItems.ITEMS.register(modBus);
        ModCreativeTabs.TABS.register(modBus);
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MODID, path);
    }
}
