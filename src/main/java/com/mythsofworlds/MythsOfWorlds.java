package com.mythsofworlds;

import com.mythsofworlds.codex.CodexContent;
import com.mythsofworlds.core.ClientConfig;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.core.back.BackSlot;
import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.GreekFeatures;
import com.mythsofworlds.mythology.greek.GreekSounds;
import com.mythsofworlds.mythology.indian.IndianContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.norse.NorseEntities;
import com.mythsofworlds.mythology.oceanic.OceanicContent;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.mythology.slavic.SlavicEntities;
import com.mythsofworlds.registry.ModRegistries;
import com.mojang.logging.LogUtils;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import org.slf4j.Logger;

@Mod(MythsOfWorlds.MODID)
public final class MythsOfWorlds {
    public static final String MODID = "mythsofworlds";
    public static final Logger LOGGER = LogUtils.getLogger();

    public MythsOfWorlds(IEventBus modBus, ModContainer container) {
        container.registerConfig(ModConfig.Type.CLIENT, ClientConfig.SPEC);
        // One line per mythology (see mythology/Mythology.java for the list).
        PlayerData.init();
        BackSlot.init();
        CodexContent.init();
        GreekContent.init();
        GreekSounds.init();
        GreekFeatures.init();
        GreekEntities.init(modBus);
        NorseContent.init();
        NorseEntities.init(modBus);
        SlavicContent.init();
        SlavicEntities.init(modBus);
        OceanicContent.init();
        EgyptianContent.init();
        IndianContent.init();

        ModRegistries.register(modBus);
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MODID, path);
    }
}
