package com.mythsofworlds.mythology.greek;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.sounds.SoundEvent;
import net.neoforged.neoforge.registries.DeferredHolder;

import static com.mythsofworlds.registry.ModRegistries.SOUNDS;

/**
 * Sounds of Hellas. What each one plays is set in assets/mythsofworlds/sounds.json: some are our own recordings
 * (assets/mythsofworlds/sounds/*.ogg, made by tools/gen_greek_sounds.py), others re-voice vanilla sounds.
 */
public final class GreekSounds {
    public static final DeferredHolder<SoundEvent, SoundEvent> PAN_FLUTE = sound("entity.satyr.pan_flute");
    public static final DeferredHolder<SoundEvent, SoundEvent> SATYR_AMBIENT = sound("entity.satyr.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> HARPY_AMBIENT = sound("entity.harpy.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> HARPY_HURT = sound("entity.harpy.hurt");
    public static final DeferredHolder<SoundEvent, SoundEvent> HARPY_DEATH = sound("entity.harpy.death");
    public static final DeferredHolder<SoundEvent, SoundEvent> SHADE_AMBIENT = sound("entity.shade.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> SHADE_HURT = sound("entity.shade.hurt");
    public static final DeferredHolder<SoundEvent, SoundEvent> SHADE_DEATH = sound("entity.shade.death");
    public static final DeferredHolder<SoundEvent, SoundEvent> SHADE_TELEPORT = sound("entity.shade.teleport");
    public static final DeferredHolder<SoundEvent, SoundEvent> MINOTAUR_AMBIENT = sound("entity.minotaur.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> MINOTAUR_ROAR = sound("entity.minotaur.roar");
    public static final DeferredHolder<SoundEvent, SoundEvent> MINOTAUR_HURT = sound("entity.minotaur.hurt");
    public static final DeferredHolder<SoundEvent, SoundEvent> MINOTAUR_DEATH = sound("entity.minotaur.death");
    public static final DeferredHolder<SoundEvent, SoundEvent> HYDRA_AMBIENT = sound("entity.hydra.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> HYDRA_SPIT = sound("entity.hydra.spit");
    public static final DeferredHolder<SoundEvent, SoundEvent> HYDRA_HURT = sound("entity.hydra.hurt");
    public static final DeferredHolder<SoundEvent, SoundEvent> HYDRA_DEATH = sound("entity.hydra.death");
    public static final DeferredHolder<SoundEvent, SoundEvent> CERBERUS_AMBIENT = sound("entity.cerberus.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> CERBERUS_BREATH = sound("entity.cerberus.breath");
    public static final DeferredHolder<SoundEvent, SoundEvent> CERBERUS_HURT = sound("entity.cerberus.hurt");
    public static final DeferredHolder<SoundEvent, SoundEvent> CERBERUS_DEATH = sound("entity.cerberus.death");
    public static final DeferredHolder<SoundEvent, SoundEvent> CYCLOPS_AMBIENT = sound("entity.cyclops.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> CYCLOPS_STOMP = sound("entity.cyclops.stomp");
    public static final DeferredHolder<SoundEvent, SoundEvent> CYCLOPS_HURT = sound("entity.cyclops.hurt");
    public static final DeferredHolder<SoundEvent, SoundEvent> CYCLOPS_DEATH = sound("entity.cyclops.death");
    public static final DeferredHolder<SoundEvent, SoundEvent> MEDUSA_AMBIENT = sound("entity.medusa.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> MEDUSA_GAZE = sound("entity.medusa.gaze");
    public static final DeferredHolder<SoundEvent, SoundEvent> MEDUSA_HURT = sound("entity.medusa.hurt");
    public static final DeferredHolder<SoundEvent, SoundEvent> MEDUSA_DEATH = sound("entity.medusa.death");
    public static final DeferredHolder<SoundEvent, SoundEvent> LION_AMBIENT = sound("entity.nemean_lion.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> LION_HURT = sound("entity.nemean_lion.hurt");
    public static final DeferredHolder<SoundEvent, SoundEvent> LION_DEATH = sound("entity.nemean_lion.death");
    public static final DeferredHolder<SoundEvent, SoundEvent> MERCHANT_GREET = sound("entity.greek_merchant.greet");
    public static final DeferredHolder<SoundEvent, SoundEvent> PORTAL_IGNITE = sound("block.brazier.ignite");
    // Biome music and ambience (data/mythsofworlds/worldgen/biome/*.json).
    public static final DeferredHolder<SoundEvent, SoundEvent> MUSIC_ELYSIUM = sound("music.hellas.elysium");
    public static final DeferredHolder<SoundEvent, SoundEvent> MUSIC_UNDERWORLD = sound("music.hellas.underworld");
    public static final DeferredHolder<SoundEvent, SoundEvent> AMBIENT_CHIMES = sound("ambient.hellas.chimes");

    private GreekSounds() {
    }

    private static DeferredHolder<SoundEvent, SoundEvent> sound(String name) {
        return SOUNDS.register(name, () -> SoundEvent.createVariableRangeEvent(MythsOfWorlds.id(name)));
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
