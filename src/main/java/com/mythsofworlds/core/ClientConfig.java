package com.mythsofworlds.core;

import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * Client settings (config/mythsofworlds-client.toml, also editable in the game: Mods, Myths of Worlds, Config).
 * The HUD can be switched on and off at any time with its key or the button in the pause menu.
 */
public final class ClientConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.BooleanValue HUD_ENABLED;
    public static final ModConfigSpec.BooleanValue SHOW_WORLD_NAME;
    public static final ModConfigSpec.BooleanValue SHOW_NUMBERS;

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();
        HUD_ENABLED = builder.comment("Carved bars of health, armour, hunger, air and experience in place of the vanilla ones")
                .translation("mythsofworlds.configuration.hudEnabled").define("hudEnabled", true);
        SHOW_WORLD_NAME = builder.comment("A scroll with the name of the world of the myths at the top left of the screen")
                .translation("mythsofworlds.configuration.showWorldName").define("showWorldName", true);
        SHOW_NUMBERS = builder.comment("Write health, armour, hunger and air as numbers on the bars")
                .translation("mythsofworlds.configuration.showNumbers").define("showNumbers", true);
        SPEC = builder.build();
    }

    private ClientConfig() {
    }

    /** Turns the HUD of the myths on or off and saves the choice. */
    public static boolean toggleHud() {
        boolean enabled = !HUD_ENABLED.get();
        HUD_ENABLED.set(enabled);
        HUD_ENABLED.save();
        return enabled;
    }
}
