package com.mythsofworlds.mythology.greek;

import com.mythsofworlds.mythology.greek.feature.CloudIslandFeature;
import com.mythsofworlds.mythology.greek.feature.MarbleRuinFeature;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.configurations.NoneFeatureConfiguration;
import net.neoforged.neoforge.registries.DeferredHolder;

import static com.mythsofworlds.registry.ModRegistries.FEATURES;

/**
 * World generation features of Hellas that cannot be expressed as vanilla data. Where they appear is set in
 * data/mythsofworlds/worldgen/configured_feature and placed_feature (written by tools/gen_greek_assets.py).
 */
public final class GreekFeatures {
    /** Floating island of cloud, sometimes with a small marble shrine on top. */
    public static final DeferredHolder<Feature<?>, CloudIslandFeature> CLOUD_ISLAND = FEATURES.register("cloud_island",
            () -> new CloudIslandFeature(NoneFeatureConfiguration.CODEC));
    /** Broken colonnade, altar or toppled statue of a forgotten temple. */
    public static final DeferredHolder<Feature<?>, MarbleRuinFeature> MARBLE_RUIN = FEATURES.register("marble_ruin",
            () -> new MarbleRuinFeature(NoneFeatureConfiguration.CODEC));

    private GreekFeatures() {
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
