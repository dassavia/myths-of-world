package com.mythsofworlds.mythology.slavic;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.sounds.SoundEvent;
import net.neoforged.neoforge.registries.DeferredHolder;

import static com.mythsofworlds.registry.ModRegistries.SOUNDS;

/**
 * Sounds of Nav. What each one plays is set in assets/mythsofworlds/sounds.json, written by
 * tools/gen_greek_sounds.py from the table in tools/sounds_nav_jotunheim.py (the .ogg files are synthesized there too).
 */
public final class SlavicSounds {
    public static final DeferredHolder<SoundEvent, SoundEvent> SOLOVEI_WHISTLE = sound("entity.solovei.whistle");
    public static final DeferredHolder<SoundEvent, SoundEvent> ZMEY_ROAR = sound("entity.zmey_gorynych.roar");
    public static final DeferredHolder<SoundEvent, SoundEvent> ZMEY_BREATH = sound("entity.zmey_gorynych.breath");
    public static final DeferredHolder<SoundEvent, SoundEvent> KOSCHEI_LAUGH = sound("entity.koschei.laugh");
    public static final DeferredHolder<SoundEvent, SoundEvent> KOSCHEI_SUMMON = sound("entity.koschei.summon");
    public static final DeferredHolder<SoundEvent, SoundEvent> RUSALKA_SONG = sound("entity.rusalka.song");
    public static final DeferredHolder<SoundEvent, SoundEvent> LESHY_AMBIENT = sound("entity.leshy.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> GUSLI = sound("item.gusli.play");
    // Biome music (data/mythsofworlds/worldgen/biome/*.json).
    public static final DeferredHolder<SoundEvent, SoundEvent> MUSIC_FOREST = sound("music.nav.forest");
    public static final DeferredHolder<SoundEvent, SoundEvent> MUSIC_DARK = sound("music.nav.dark");

    private SlavicSounds() {
    }

    private static DeferredHolder<SoundEvent, SoundEvent> sound(String name) {
        return SOUNDS.register(name, () -> SoundEvent.createVariableRangeEvent(MythsOfWorlds.id(name)));
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
