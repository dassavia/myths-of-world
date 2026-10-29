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

/** What the mod remembers about each player. Both survive death and are saved with the player. */
public final class PlayerData {
    /** Ids of the journal entries the player has unlocked (see {@link com.mythsofworlds.journal.Journal}). */
    public static final Supplier<AttachmentType<List<String>>> JOURNAL = ATTACHMENT_TYPES.register("journal",
            () -> AttachmentType.<List<String>>builder(() -> new ArrayList<>())
                    .serialize(Codec.STRING.listOf())
                    .copyOnDeath()
                    .build());
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
}
