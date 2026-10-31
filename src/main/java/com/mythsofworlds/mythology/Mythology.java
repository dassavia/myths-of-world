package com.mythsofworlds.mythology;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.indian.IndianContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.oceanic.OceanicContent;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * The six mythologies of the mod and what the shared systems need to know about each: the world (dimension) it leads
 * to, whether it can be reached by a portal yet, its volume of the Codex (tools/journal_&lt;volume&gt;.py) and its bosses
 * with the lairs they guard; their deaths are milestones of the hero's path. A new mythology is one line here plus its own content class.
 * <p>
 * Greek, Norse and Slavic are complete; the others are stubs: their dimension exists (reach it with
 * {@code /execute in mythsofworlds:<id> run tp @s ~ 120 ~}) but has no portal or own content yet.
 */
public enum Mythology {
    GREEK(GreekContent.HELLAS, true, "greek", lairs("cyclops", "cyclops_cave", "medusa", "medusa_lair", "nemean_lion", "nemean_lion_den",
            "minotaur", "labyrinth", "hydra", "hydra_lair", "cerberus", "gates_of_hades")),
    NORSE(NorseContent.JOTUNHEIM, true, "norse", lairs("draugr_chieftain", "barrow", "garm", "helgrind", "heimdall", "himinbjorg",
            "thrym", "utgard", "fenrir", "fenrir_island", "surtr", "muspel_fortress")),
    SLAVIC(SlavicContent.NAV, true, "slavic", lairs("solovei", "solovei_nest", "zmey_gorynych", "kalinov_bridge", "koschei", "koschei_castle")),
    OCEANIC(OceanicContent.HAWAIKI, false, null, Map.of()),
    EGYPTIAN(EgyptianContent.DUAT, false, null, Map.of()),
    INDIAN(IndianContent.SVARGA, false, null, Map.of());

    private final ResourceKey<Level> dimension;
    private final boolean hasPortal;
    @Nullable
    private final String journal;
    /** Boss id -> the structure it guards, in the order the path meets them. */
    private final Map<String, String> lairs;

    Mythology(ResourceKey<Level> dimension, boolean hasPortal, @Nullable String journal, Map<String, String> lairs) {
        this.dimension = dimension;
        this.hasPortal = hasPortal;
        this.journal = journal;
        this.lairs = lairs;
    }

    /** Pairs of boss id and lair structure id, kept in order. */
    private static Map<String, String> lairs(String... pairs) {
        Map<String, String> map = new LinkedHashMap<>();
        for (int i = 0; i < pairs.length; i += 2) {
            map.put(pairs[i], pairs[i + 1]);
        }
        return Collections.unmodifiableMap(map);
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
        return lairs.keySet();
    }

    /** Boss id -> id (path) of the structure where it waits: what the prophecies of Delphi and the yarn ball of Nav find. */
    public Map<String, String> lairs() {
        return lairs;
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
        return Arrays.stream(values()).flatMap(m -> m.bosses().stream()).collect(Collectors.toUnmodifiableSet());
    }
}
