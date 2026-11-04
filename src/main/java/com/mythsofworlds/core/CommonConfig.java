package com.mythsofworlds.core;

import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * Settings shared by the server and the client (config/mythsofworlds-common.toml): how the mod works together with
 * other mods. Everything here only matters when that mod is installed; without it the mod plays exactly the same.
 */
public final class CommonConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.BooleanValue MCA_COMPAT;
    public static final ModConfigSpec.BooleanValue MCA_NO_DOUBLE_RESIDENTS;

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();
        builder.comment("Minecraft Comes Alive Reborn (mod id mca, 7.7.32 or newer). Ignored when it is not installed.")
                .translation("mythsofworlds.configuration.mca").push("mca");
        MCA_COMPAT = builder.comment("Work together with MCA Reborn: its guards fight the monsters of the myths and leave the gods, "
                        + "traders and friendly creatures alone")
                .translation("mythsofworlds.configuration.mcaCompat").define("enabled", true);
        MCA_NO_DOUBLE_RESIDENTS = builder.comment("Inside the villages and temples of the myths, a villager is not added next to a trader "
                        + "or priestess who already lives there, so a house never gets two residents")
                .translation("mythsofworlds.configuration.mcaNoDoubleResidents").define("noDoubleResidents", true);
        builder.pop();
        SPEC = builder.build();
    }

    private CommonConfig() {
    }
}
