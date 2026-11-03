package com.mythsofworlds.mythology.egyptian;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.sounds.SoundEvent;
import net.neoforged.neoforge.registries.DeferredHolder;

import static com.mythsofworlds.registry.ModRegistries.SOUNDS;

/**
 * Sounds of the Duat. What each one plays is set in assets/mythsofworlds/sounds.json (tools/gen_greek_sounds.py):
 * vanilla sounds re-voiced, each with its own subtitle.
 */
public final class EgyptianSounds {
    public static final DeferredHolder<SoundEvent, SoundEvent> MUMMY_AMBIENT = sound("entity.mummy.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> SCARAB_AMBIENT = sound("entity.scarab.ambient");
    public static final DeferredHolder<SoundEvent, SoundEvent> PHARAOH_CURSE = sound("entity.pharaoh_mummy.curse");
    public static final DeferredHolder<SoundEvent, SoundEvent> SPHINX_ROAR = sound("entity.sphinx.roar");
    public static final DeferredHolder<SoundEvent, SoundEvent> SANDSTORM = sound("entity.set.sandstorm");
    public static final DeferredHolder<SoundEvent, SoundEvent> APEP_HISS = sound("entity.apep.hiss");
    public static final DeferredHolder<SoundEvent, SoundEvent> GATE_OPEN = sound("block.pyramid_gate.open");

    private EgyptianSounds() {
    }

    private static DeferredHolder<SoundEvent, SoundEvent> sound(String name) {
        return SOUNDS.register(name, () -> SoundEvent.createVariableRangeEvent(MythsOfWorlds.id(name)));
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
