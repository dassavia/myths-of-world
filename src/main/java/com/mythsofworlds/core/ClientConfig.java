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
    public static final ModConfigSpec.BooleanValue CODEX_FONT;
    public static final ModConfigSpec.DoubleValue WORLD_BANNER_SCALE;
    public static final ModConfigSpec.BooleanValue MCA_SKINS;
    public static final ModConfigSpec.BooleanValue HEIMDALL_VISION;

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();
        HUD_ENABLED = builder.comment("Carved bars of health, armour, hunger, air and experience in place of the vanilla ones")
                .translation("mythsofworlds.configuration.hudEnabled").define("hudEnabled", true);
        SHOW_WORLD_NAME = builder.comment("A banner with the name of the world of the myths, for two seconds at the top of the screen each time you enter it")
                .translation("mythsofworlds.configuration.showWorldName").define("showWorldName", true);
        WORLD_BANNER_SCALE = builder.comment("Size of that banner, from a quarter to the full scroll (it never gets too small to read)")
                .translation("mythsofworlds.configuration.worldBannerScale").defineInRange("worldBannerScale", 0.5, 0.25, 1.0);
        SHOW_NUMBERS = builder.comment("Write health, armour, hunger and air as numbers on the bars")
                .translation("mythsofworlds.configuration.showNumbers").define("showNumbers", true);
        CODEX_FONT = builder.comment("Write the Codex of Myths in the clean font of the mod (full Cyrillic) instead of Patchouli's Unifont")
                .translation("mythsofworlds.configuration.codexFont").define("codexFont", true);
        HEIMDALL_VISION = builder.comment("The vision of the helmet of Heimdall: night vision and every creature within 100 blocks glowing "
                        + "through walls. Also switched with its key (N by default)")
                .translation("mythsofworlds.configuration.heimdallVision").define("heimdallVision", true);
        MCA_SKINS = builder.comment("With MCA Reborn installed, priestesses, amazons and valkyries wear MCA's women's looks (each her own); "
                        + "Isis keeps hers. Without MCA the mod's own textures are always used")
                .translation("mythsofworlds.configuration.mcaSkins").define("mcaSkins", true);
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
