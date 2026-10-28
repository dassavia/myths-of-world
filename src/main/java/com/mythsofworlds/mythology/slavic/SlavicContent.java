package com.mythsofworlds.mythology.slavic;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;

/**
 * Slavic mythology: Nav, the dark world of spirits and ancestors beyond the Kalinov bridge.
 * Stub: the dimension (data/mythsofworlds/dimension/nav.json) exists and uses vanilla biomes.
 * To grow it, follow GreekContent: frame block, portal, igniter, own biomes, structures and mobs.
 */
public final class SlavicContent {
    /** Defined in data/mythsofworlds/dimension/nav.json. */
    public static final ResourceKey<Level> NAV =
            ResourceKey.create(Registries.DIMENSION, MythsOfWorlds.id("nav"));

    private SlavicContent() {
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
