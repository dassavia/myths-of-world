package com.mythsofworlds.journal;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.network.Filterable;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.component.WrittenBookContent;

/**
 * The journals: one book per mythology ("volume") with an entry for each creature, boss and place. Which entries exist,
 * what unlocks them and how many pages each has is read from data/mythsofworlds/journal/&lt;volume&gt;.json; the text
 * is in the lang files (journal.mythsofworlds.&lt;entry&gt;.title / .page&lt;n&gt;), both written by tools/gen_greek_assets.py.
 * In survival an entry appears once the player has seen the creature, killed it or walked into the place.
 */
public final class Journal {
    public enum Category { INTRO, CREATURE, BOSS, PLACE }

    /**
     * @param entity    id of the mob whose sighting unlocks the entry, if any
     * @param structure id of the structure whose visit unlocks it, if any
     */
    public record Entry(String id, Category category, Optional<ResourceLocation> entity, Optional<ResourceLocation> structure,
                        int pages) {
        public Component title() {
            return Component.translatable("journal.mythsofworlds." + id + ".title");
        }
    }

    private static final Map<String, List<Entry>> VOLUMES = new LinkedHashMap<>();

    private Journal() {
    }

    public static synchronized List<Entry> volume(String volume) {
        return VOLUMES.computeIfAbsent(volume, Journal::load);
    }

    private static List<Entry> load(String volume) {
        String path = "/data/" + MythsOfWorlds.MODID + "/journal/" + volume + ".json";
        List<Entry> entries = new ArrayList<>();
        try (InputStream in = Journal.class.getResourceAsStream(path)) {
            if (in == null) {
                throw new IllegalStateException(path + " is missing");
            }
            JsonObject root = JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
            for (JsonElement element : root.getAsJsonArray("entries")) {
                JsonObject e = element.getAsJsonObject();
                entries.add(new Entry(e.get("id").getAsString(),
                        Category.valueOf(e.get("category").getAsString().toUpperCase()),
                        e.has("entity") ? Optional.of(ResourceLocation.parse(e.get("entity").getAsString())) : Optional.empty(),
                        e.has("structure") ? Optional.of(ResourceLocation.parse(e.get("structure").getAsString())) : Optional.empty(),
                        e.get("pages").getAsInt()));
            }
        } catch (Exception e) {
            throw new IllegalStateException("cannot read journal " + path, e);
        }
        return List.copyOf(entries);
    }

    public static boolean isUnlocked(Player player, Entry entry) {
        return entry.category() == Category.INTRO || PlayerData.hasEntry(player, entry.id());
    }

    /** The book as {@code player} should see it: every entry if {@code complete}, otherwise only those they found. */
    public static WrittenBookContent book(String volume, Player player, boolean complete) {
        List<Entry> entries = volume(volume);
        List<Filterable<Component>> pages = new ArrayList<>();
        int unlocked = 0;
        int total = 0;
        for (Entry entry : entries) {
            if (entry.category() != Category.INTRO) {
                total++;
                if (complete || isUnlocked(player, entry)) {
                    unlocked++;
                }
            }
        }
        String prefix = "journal.mythsofworlds." + volume;
        pages.add(Filterable.passThrough(Component.empty()
                .append(Component.translatable(prefix + ".title").withStyle(ChatFormatting.BOLD))
                .append("\n\n")
                .append(Component.translatable(prefix + ".intro"))
                .append("\n\n")
                .append(Component.translatable("journal.mythsofworlds.progress", unlocked, total).withStyle(ChatFormatting.DARK_GRAY))));
        for (Category category : Category.values()) {
            for (Entry entry : entries) {
                if (entry.category() != category || !(complete || isUnlocked(player, entry))) {
                    continue;
                }
                for (int page = 1; page <= entry.pages(); page++) {
                    MutableComponent text = Component.empty();
                    if (page == 1) {
                        text.append(Component.translatable("journal.mythsofworlds.category." + category.name().toLowerCase())
                                .withStyle(ChatFormatting.DARK_GRAY)).append("\n");
                        text.append(entry.title().copy().withStyle(ChatFormatting.BOLD)).append("\n\n");
                    }
                    text.append(Component.translatable("journal.mythsofworlds." + entry.id() + ".page" + page));
                    pages.add(Filterable.passThrough(text));
                    if (pages.size() >= WrittenBookContent.MAX_PAGES) {
                        break;
                    }
                }
            }
        }
        return new WrittenBookContent(Filterable.passThrough("journal"), "", 0, pages, true);
    }
}
