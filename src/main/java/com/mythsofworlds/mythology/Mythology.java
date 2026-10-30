package com.mythsofworlds.mythology;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.indian.IndianContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.oceanic.OceanicContent;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import java.util.Arrays;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * The six mythologies of the mod and what the shared systems need to know about each: the world (dimension) it leads
 * to, whether it can be reached by a portal yet, its volume of the Codex (tools/journal_&lt;volume&gt;.py) and its bosses,
 * whose deaths are milestones of the hero's path. A new mythology is one line here plus its own content class.
 * <p>
 * Greek, Norse and Slavic are complete; the others are stubs: their dimension exists (reach it with
 * {@code /execute in mythsofworlds:<id> run tp @s ~ 120 ~}) but has no portal or own content yet.
 */
public enum Mythology {
    GREEK(GreekContent.HELLAS, true, "greek", "cyclops", "medusa", "nemean_lion", "minotaur", "hydra", "cerberus"),
    NORSE(NorseContent.JOTUNHEIM, true, "norse", "draugr_chieftain", "garm", "heimdall", "thrym", "fenrir", "surtr"),
    SLAVIC(SlavicContent.NAV, true, "slavic", "solovei", "zmey_gorynych", "koschei"),
    OCEANIC(OceanicContent.HAWAIKI, false, null),
    EGYPTIAN(EgyptianContent.DUAT, false, null),
    INDIAN(IndianContent.SVARGA, false, null);

    private final ResourceKey<Level> dimension;
    private final boolean hasPortal;
    @Nullable
    private final String journal;
    private final Set<String> bosses;

    Mythology(ResourceKey<Level> dimension, boolean hasPortal, @Nullable String journal, String... bosses) {
        this.dimension = dimension;
        this.hasPortal = hasPortal;
        this.journal = journal;
        this.bosses = Set.of(bosses);
    }

    public ResourceKey<Level> dimension() {
        return dimension;
    }

    public boolean hasPortal() {
        return hasPortal;
    }

    /** The id of its world ({@code hellas}, {@code nav}...): the dimension's name, used by the Codex and the HUD. */
    public String world() {
        return dimension.location().getPath();
    }

    /** Its volume of the Codex, the {@code journal/<volume>.json} written by tools/journal_&lt;volume&gt;.py. */
    public Optional<String> journal() {
        return Optional.ofNullable(journal);
    }

    /** Entity ids (paths) of its bosses and half-bosses. */
    public Set<String> bosses() {
        return bosses;
    }

    /** The mythology whose world this is, if any. */
    public static Optional<Mythology> of(ResourceKey<Level> dimension) {
        for (Mythology mythology : values()) {
            if (mythology.dimension.equals(dimension)) {
                return Optional.of(mythology);
            }
        }
        return Optional.empty();
    }

    /** The bosses of every mythology. */
    public static Set<String> allBosses() {
        return Arrays.stream(values()).flatMap(m -> m.bosses.stream()).collect(Collectors.toUnmodifiableSet());
    }
}
