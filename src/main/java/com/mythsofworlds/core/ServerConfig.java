package com.mythsofworlds.core;

import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * Balance settings of a world (serverconfig/mythsofworlds-server.toml inside the save; on a server the host sets them).
 * The defaults are the mod as designed; owners of servers and modpacks can make the myths gentler or harsher.
 */
public final class ServerConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.DoubleValue BOSS_HEALTH;
    public static final ModConfigSpec.DoubleValue BOSS_DAMAGE;
    public static final ModConfigSpec.DoubleValue BOSS_SHARE_RANGE;
    public static final ModConfigSpec.DoubleValue HEIMDALL_RANGE;
    public static final ModConfigSpec.DoubleValue JOURNAL_SIGHT_RANGE;

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();
        builder.push("bosses");
        BOSS_HEALTH = builder.comment("Multiplies the health of every boss and half-boss of the myths (Minecraft caps any health at 1024)")
                .translation("mythsofworlds.configuration.bossHealth").defineInRange("bossHealth", 1.0, 0.1, 10.0);
        BOSS_DAMAGE = builder.comment("Multiplies all the damage bosses deal: blows, fire and missiles")
                .translation("mythsofworlds.configuration.bossDamage").defineInRange("bossDamage", 1.0, 0.1, 10.0);
        BOSS_SHARE_RANGE = builder.comment("Players this close to a boss when it falls share the victory (blocks)")
                .translation("mythsofworlds.configuration.bossShareRange").defineInRange("bossShareRange", 64.0, 0.0, 256.0);
        builder.pop();
        builder.push("relics");
        HEIMDALL_RANGE = builder.comment("Creatures this close to a player wearing the helmet of Heimdall glow through walls (blocks)."
                        + " Lower it on busy servers")
                .translation("mythsofworlds.configuration.heimdallRange").defineInRange("heimdallRange", 100.0, 16.0, 160.0);
        builder.pop();
        builder.push("codex");
        JOURNAL_SIGHT_RANGE = builder.comment("A creature is written into the Codex once a player sees it this close (blocks)")
                .translation("mythsofworlds.configuration.journalSightRange").defineInRange("journalSightRange", 20.0, 4.0, 64.0);
        builder.pop();
        SPEC = builder.build();
    }

    private ServerConfig() {
    }

    /** The value, or its default while no world is loaded (the server config only exists inside a world). */
    public static double get(ModConfigSpec.DoubleValue value) {
        return SPEC.isLoaded() ? value.get() : value.getDefault();
    }
}
