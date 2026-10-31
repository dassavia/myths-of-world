package com.mythsofworlds.core;

import com.mojang.serialization.Codec;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Supplier;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.attachment.AttachmentType;

import static com.mythsofworlds.registry.ModRegistries.ATTACHMENT_TYPES;

/** What the mod remembers about each player. All of it survives death and is saved with the player. */
public final class PlayerData {
    /** Ids of the journal entries the player has unlocked (see {@link com.mythsofworlds.journal.Journal}). */
    public static final Supplier<AttachmentType<List<String>>> JOURNAL = ATTACHMENT_TYPES.register("journal",
            () -> AttachmentType.<List<String>>builder(() -> new ArrayList<>())
                    .serialize(Codec.STRING.listOf())
                    .copyOnDeath()
                    .build());
    /**
     * Milestones of the player's journey through the myths ({@code enter.<world>}, {@code kill.<boss>}, ...): they open
     * the chapters of the Codex (see {@link com.mythsofworlds.codex.Progress}).
     */
    public static final Supplier<AttachmentType<List<String>>> MILESTONES = ATTACHMENT_TYPES.register("milestones",
            () -> AttachmentType.<List<String>>builder(() -> new ArrayList<>())
                    .serialize(Codec.STRING.listOf())
                    .copyOnDeath()
                    .build());
    /** Game time of the player's last offering to the gods of Hellas (see Offerings), 0 if none yet. */
    public static final Supplier<AttachmentType<Long>> LAST_OFFERING = ATTACHMENT_TYPES.register("last_offering",
            () -> AttachmentType.builder(() -> 0L).serialize(Codec.LONG).copyOnDeath().build());
    /** UUID of the player's wife (an amazon or Hippolyta), empty if unmarried. */
    public static final Supplier<AttachmentType<String>> SPOUSE = ATTACHMENT_TYPES.register("spouse",
            () -> AttachmentType.builder(() -> "").serialize(Codec.STRING).copyOnDeath().build());

    private PlayerData() {
    }

    public static void init() {
    }

    public static Optional<UUID> spouse(Player player) {
        String value = player.getData(SPOUSE);
        return value.isEmpty() ? Optional.empty() : Optional.of(UUID.fromString(value));
    }

    public static void setSpouse(Player player, Optional<UUID> spouse) {
        player.setData(SPOUSE, spouse.map(UUID::toString).orElse(""));
    }

    public static boolean hasEntry(Player player, String id) {
        return player.getData(JOURNAL).contains(id);
    }

    /** @return true if the entry is new */
    public static boolean addEntry(Player player, String id) {
        List<String> entries = player.getData(JOURNAL);
        if (entries.contains(id)) {
            return false;
        }
        List<String> copy = new ArrayList<>(entries);
        copy.add(id);
        player.setData(JOURNAL, copy);
        return true;
    }

    public static boolean hasMilestone(Player player, String id) {
        return player.getData(MILESTONES).contains(id);
    }

    /** @return true if the milestone is new */
    public static boolean addMilestone(Player player, String id) {
        List<String> milestones = player.getData(MILESTONES);
        if (milestones.contains(id)) {
            return false;
        }
        List<String> copy = new ArrayList<>(milestones);
        copy.add(id);
        player.setData(MILESTONES, copy);
        return true;
    }
}
