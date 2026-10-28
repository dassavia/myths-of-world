package com.mythsofworlds.mythology.egyptian;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;

/**
 * Egyptian mythology: the Duat, the desert underworld that Ra crosses every night.
 * Stub: the dimension (data/mythsofworlds/dimension/duat.json) exists and uses vanilla biomes.
 * To grow it, follow GreekContent: frame block, portal, igniter, own biomes, structures and mobs.
 */
public final class EgyptianContent {
    /** Defined in data/mythsofworlds/dimension/duat.json. */
    public static final ResourceKey<Level> DUAT =
            ResourceKey.create(Registries.DIMENSION, MythsOfWorlds.id("duat"));

    private EgyptianContent() {
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
