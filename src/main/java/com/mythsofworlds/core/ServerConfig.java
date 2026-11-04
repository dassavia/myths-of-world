package com.mythsofworlds.core;

import net.neoforged.neoforge.common.ModConfigSpec;

/** Settings of each world (serverconfig/mythsofworlds-server.toml), the same for every player on the server. */
public final class ServerConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.BooleanValue HEIMDALL_VISION;

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();
        HEIMDALL_VISION = builder.comment("The vision of the helmet of Heimdall (night vision, every creature within 100 blocks glowing "
                        + "through walls). If false it is off for everyone on this server; if true each player can switch it with "
                        + "a key")
                .translation("mythsofworlds.configuration.heimdallVisionAllowed").define("heimdallVisionAllowed", true);
        SPEC = builder.build();
    }

    private ServerConfig() {
    }
}
