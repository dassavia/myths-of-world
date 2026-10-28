package com.mythsofworlds.world;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;

/** Dimension keys. The dimensions themselves are defined as JSON in data/mythsofworlds/dimension. */
public final class ModDimensions {
    public static final ResourceKey<Level> JOTUNHEIM = ResourceKey.create(Registries.DIMENSION, MythsOfWorlds.id("jotunheim"));

    private ModDimensions() {
    }
}
