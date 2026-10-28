package com.mythsofworlds.mythology.indian;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;

/**
 * Indian mythology: Svarga, the heavenly realm of Indra above the jungles.
 * Stub: the dimension (data/mythsofworlds/dimension/svarga.json) exists and uses vanilla biomes.
 * To grow it, follow GreekContent: frame block, portal, igniter, own biomes, structures and mobs.
 */
public final class IndianContent {
    /** Defined in data/mythsofworlds/dimension/svarga.json. */
    public static final ResourceKey<Level> SVARGA =
            ResourceKey.create(Registries.DIMENSION, MythsOfWorlds.id("svarga"));

    private IndianContent() {
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
