package com.mythsofworlds.codex;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import net.minecraft.advancements.AdvancementHolder;
import net.minecraft.advancements.AdvancementProgress;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.PlayerAdvancements;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.GameType;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import vazkii.patchouli.api.PatchouliAPI;

/**
 * The Codex of Myths is a Patchouli book (data/mythsofworlds/patchouli_books/codex, written by tools/gen_book.py). Its
 * pages are locked by hidden advancements under {@code mythsofworlds:codex/}, which this class keeps in step with what
 * the player has done: {@code codex/entry/<entry>} for each journal entry found, {@code codex/milestone/<step>} for each
 * step of the path and {@code codex/chapter/<world>} once the path reaches that world. A player in creative mode has
 * all of them, so the whole book is open; leaving creative takes back what was not earned.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class CodexBook {
    public static final ResourceLocation ID = MythsOfWorlds.id("codex");
    private static final String PREFIX = "codex/";
    private static final String CRITERION = "granted";

    private CodexBook() {
    }

    /** Opens the Codex for {@code player}. */
    public static void open(ServerPlayer player) {
        PatchouliAPI.get().openBookGUI(player, ID);
    }

    /** The advancement that stands for a journal entry, a milestone or a chapter. */
    public static ResourceLocation lock(String kind, String name) {
        return MythsOfWorlds.id(PREFIX + kind + "/" + name.replace('.', '_'));
    }

    /** The locks {@code player} has earned, by their ids. */
    public static Set<ResourceLocation> earned(ServerPlayer player) {
        Set<ResourceLocation> earned = new HashSet<>();
        player.getData(PlayerData.JOURNAL).forEach(entry -> earned.add(lock("entry", entry)));
        List<String> milestones = player.getData(PlayerData.MILESTONES);
        milestones.forEach(milestone -> earned.add(lock("milestone", milestone)));
        for (Codex.Chapter chapter : Codex.chapters()) {
            if (milestones.containsAll(chapter.requires())) {
                earned.add(lock("chapter", chapter.id()));
            }
        }
        return earned;
    }

    /** Grants the player the locks they have earned, or all of them in creative mode, and takes back the rest. */
    public static void sync(ServerPlayer player) {
        sync(player, player.isCreative());
    }

    private static void sync(ServerPlayer player, boolean everything) {
        Set<ResourceLocation> earned = everything ? Set.of() : earned(player);
        PlayerAdvancements advancements = player.getAdvancements();
        for (AdvancementHolder holder : player.server.getAdvancements().getAllAdvancements()) {
            ResourceLocation id = holder.id();
            if (!id.getNamespace().equals(MythsOfWorlds.MODID) || !id.getPath().startsWith(PREFIX)) {
                continue;
            }
            boolean want = everything || earned.contains(id);
            AdvancementProgress progress = advancements.getOrStartProgress(holder);
            if (want && !progress.isDone()) {
                advancements.award(holder, CRITERION);
            } else if (!want && progress.isDone()) {
                advancements.revoke(holder, CRITERION);
            }
        }
    }

    @SubscribeEvent
    public static void onGameModeChange(PlayerEvent.PlayerChangeGameModeEvent event) {
        if (event.getEntity() instanceof ServerPlayer player) {
            sync(player, event.getNewGameMode() == GameType.CREATIVE);
        }
    }
}
