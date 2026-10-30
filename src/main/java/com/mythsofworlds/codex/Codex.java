package com.mythsofworlds.codex;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.mythsofworlds.MythsOfWorlds;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.resources.ResourceLocation;

/**
 * The chapters of the Codex of Myths, read from data/mythsofworlds/journal/codex.json (written by
 * tools/gen_codex.py). Each chapter shows one journal volume and opens once the player has every milestone it
 * {@code requires}; its {@code steps} are the milestones of that world in their intended order, drawn on the map of
 * the path.
 */
public final class Codex {
    public record Step(String milestone, ResourceLocation icon) {
    }

    public record Chapter(String id, String volume, ResourceLocation icon, List<String> requires, List<Step> steps) {
    }

    private static List<Chapter> chapters;

    private Codex() {
    }

    public static synchronized List<Chapter> chapters() {
        if (chapters == null) {
            chapters = load();
        }
        return chapters;
    }

    public static Chapter chapter(String id) {
        for (Chapter chapter : chapters()) {
            if (chapter.id().equals(id)) {
                return chapter;
            }
        }
        return null;
    }

    /** The chapter that shows a journal volume, or null. */
    public static Chapter forVolume(String volume) {
        for (Chapter chapter : chapters()) {
            if (chapter.volume().equals(volume)) {
                return chapter;
            }
        }
        return null;
    }

    private static List<Chapter> load() {
        String path = "/data/" + MythsOfWorlds.MODID + "/journal/codex.json";
        List<Chapter> list = new ArrayList<>();
        try (InputStream in = Codex.class.getResourceAsStream(path)) {
            if (in == null) {
                throw new IllegalStateException(path + " is missing");
            }
            JsonObject root = JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
            for (JsonElement element : root.getAsJsonArray("chapters")) {
                JsonObject c = element.getAsJsonObject();
                List<String> requires = new ArrayList<>();
                c.getAsJsonArray("requires").forEach(e -> requires.add(e.getAsString()));
                List<Step> steps = new ArrayList<>();
                c.getAsJsonArray("steps").forEach(e -> steps.add(new Step(e.getAsJsonObject().get("milestone").getAsString(),
                        ResourceLocation.parse(e.getAsJsonObject().get("icon").getAsString()))));
                list.add(new Chapter(c.get("id").getAsString(), c.get("volume").getAsString(),
                        ResourceLocation.parse(c.get("icon").getAsString()), List.copyOf(requires), List.copyOf(steps)));
            }
        } catch (Exception e) {
            throw new IllegalStateException("cannot read " + path, e);
        }
        return List.copyOf(list);
    }
}
