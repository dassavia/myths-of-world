package com.mythsofworlds.mythology.norse;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.sounds.SoundEvent;
import net.neoforged.neoforge.registries.DeferredHolder;

import static com.mythsofworlds.registry.ModRegistries.SOUNDS;

/**
 * Sounds of Jotunheim. What each one plays is set in assets/mythsofworlds/sounds.json, written by
 * tools/gen_greek_sounds.py from the table in tools/sounds_nav_jotunheim.py (the .ogg files are synthesized there too).
 */
public final class NorseSounds {
    public static final DeferredHolder<SoundEvent, SoundEvent> GJALLARHORN = sound("entity.heimdall.gjallarhorn");
    public static final DeferredHolder<SoundEvent, SoundEvent> THRYM_STOMP = sound("entity.thrym.stomp");
    public static final DeferredHolder<SoundEvent, SoundEvent> SURTR_FLAMES = sound("entity.surtr.flames");
    public static final DeferredHolder<SoundEvent, SoundEvent> DRAUGR_CALL = sound("entity.draugr_chieftain.call");
    public static final DeferredHolder<SoundEvent, SoundEvent> FENRIR_HOWL = sound("entity.fenrir.howl");
    public static final DeferredHolder<SoundEvent, SoundEvent> GARM_HOWL = sound("entity.garm.howl");
    // Biome music (data/mythsofworlds/worldgen/biome/*.json).
    public static final DeferredHolder<SoundEvent, SoundEvent> MUSIC_NORTH = sound("music.jotunheim.north");
    public static final DeferredHolder<SoundEvent, SoundEvent> MUSIC_NIFLHEIM = sound("music.jotunheim.niflheim");

    private NorseSounds() {
    }

    private static DeferredHolder<SoundEvent, SoundEvent> sound(String name) {
        return SOUNDS.register(name, () -> SoundEvent.createVariableRangeEvent(MythsOfWorlds.id(name)));
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
