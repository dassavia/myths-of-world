package com.mythsofworlds;

import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.registry.ModRegistries;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(MythsOfWorlds.MODID)
public final class MythsOfWorlds {
    public static final String MODID = "mythsofworlds";

    public MythsOfWorlds(IEventBus modBus) {
        // One line per mythology. Add e.g. GreekContent.init() here when it exists.
        NorseContent.init();

        ModRegistries.register(modBus);
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MODID, path);
    }
}
