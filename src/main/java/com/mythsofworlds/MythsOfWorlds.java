package com.mythsofworlds;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.GreekFeatures;
import com.mythsofworlds.mythology.greek.GreekSounds;
import com.mythsofworlds.mythology.indian.IndianContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.oceanic.OceanicContent;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.registry.ModRegistries;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;

@Mod(MythsOfWorlds.MODID)
public final class MythsOfWorlds {
    public static final String MODID = "mythsofworlds";

    public MythsOfWorlds(IEventBus modBus) {
        // One line per mythology (see mythology/Mythology.java for the list).
        GreekContent.init();
        GreekSounds.init();
        GreekFeatures.init();
        GreekEntities.init(modBus);
        NorseContent.init();
        SlavicContent.init();
        OceanicContent.init();
        EgyptianContent.init();
        IndianContent.init();

        ModRegistries.register(modBus);
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MODID, path);
    }
}
