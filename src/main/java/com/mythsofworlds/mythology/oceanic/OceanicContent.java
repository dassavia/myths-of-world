package com.mythsofworlds.mythology.oceanic;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;

/**
 * Oceanic (Polynesian) mythology: Hawaiki, the ancestral island homeland in the warm sea.
 * Stub: the dimension (data/mythsofworlds/dimension/hawaiki.json) exists and uses vanilla biomes.
 * To grow it, follow GreekContent: frame block, portal, igniter, own biomes, structures and mobs.
 */
public final class OceanicContent {
    /** Defined in data/mythsofworlds/dimension/hawaiki.json. */
    public static final ResourceKey<Level> HAWAIKI =
            ResourceKey.create(Registries.DIMENSION, MythsOfWorlds.id("hawaiki"));

    private OceanicContent() {
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
