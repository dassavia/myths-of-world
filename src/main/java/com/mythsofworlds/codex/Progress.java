package com.mythsofworlds.codex;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.core.ServerConfig;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import java.util.List;
import java.util.Map;
import java.util.Set;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;

/**
 * The hero's path through the myths. Milestones are earned by entering a world ({@code enter.hellas}) and by felling
 * a boss ({@code kill.minotaur}); they open the chapters of the Codex (data/mythsofworlds/journal/codex.json).
 * <p>
 * The order of the worlds: Hellas is open from the start. The horn of the Minotaur goes into the acorn of the World
 * Tree, so Nav opens after the first boss of Hellas, and the two can be travelled side by side. The rune igniter of
 * Bifrost needs a fang of Cerberus and a scale of Zmey Gorynych, so Jotunheim, the hardest world, opens once both
 * are slain. Surtr, the last boss of Jotunheim, ends the path and opens the chapter of the far worlds.
 * <p>
 * A boss counts for every player within {@link #shareRange()} blocks, so friends who fight together on a server
 * all go on.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class Progress {
    /** Bosses and half-bosses whose death is a milestone, by entity id path. */
    public static final Set<String> BOSSES = Set.of("cyclops", "medusa", "nemean_lion", "minotaur", "hydra", "cerberus",
            "solovei", "zmey_gorynych", "koschei", "draugr_chieftain", "garm", "heimdall", "thrym", "fenrir", "surtr");
    public static final Map<ResourceKey<Level>, String> WORLDS = Map.of(
            GreekContent.HELLAS, "hellas", NorseContent.JOTUNHEIM, "jotunheim", SlavicContent.NAV, "nav");
    /** Players this close to a boss when it falls share the victory (blocks; {@code bossShareRange} in the server config). */
    public static double shareRange() {
        return ServerConfig.get(ServerConfig.BOSS_SHARE_RANGE);
    }

    private Progress() {
    }

    /** Gives {@code player} the milestone; tells them and opens its pages in the Codex if it is new. */
    public static void award(ServerPlayer player, String milestone) {
        if (PlayerData.addMilestone(player, milestone)) {
            player.displayClientMessage(Component.translatable("codex.mythsofworlds.milestone",
                    Component.translatable("codex.mythsofworlds.milestone." + milestone)).withStyle(ChatFormatting.GOLD), false);
            player.level().playSound(null, player.blockPosition(), SoundEvents.UI_TOAST_CHALLENGE_COMPLETE, SoundSource.PLAYERS,
                    0.5F, 1.2F);
            CodexBook.sync(player);
        }
    }

    /** Gives the milestone to every player around {@code source}. */
    public static void awardAround(Entity source, String milestone) {
        if (source.level() instanceof ServerLevel level) {
            double range = shareRange();
            for (ServerPlayer player : level.players()) {
                if (player.distanceToSqr(source) < range * range && !player.isSpectator()) {
                    award(player, milestone);
                }
            }
        }
    }

    @SubscribeEvent(priority = EventPriority.LOWEST)
    public static void onDeath(LivingDeathEvent event) {
        if (event.isCanceled() || event.getEntity().level().isClientSide) {
            return;
        }
        ResourceLocation id = BuiltInRegistries.ENTITY_TYPE.getKey(event.getEntity().getType());
        if (id.getNamespace().equals(MythsOfWorlds.MODID) && BOSSES.contains(id.getPath())) {
            awardAround(event.getEntity(), "kill." + id.getPath());
            if (event.getSource().getEntity() instanceof ServerPlayer killer) {
                award(killer, "kill." + id.getPath());
            }
        }
    }

    @SubscribeEvent
    public static void onChangedDimension(PlayerEvent.PlayerChangedDimensionEvent event) {
        String world = WORLDS.get(event.getTo());
        if (world != null && event.getEntity() instanceof ServerPlayer player) {
            award(player, "enter." + world);
        }
    }

    /** Every hero gets the Codex the first time they join, and its pages are brought up to date. */
    @SubscribeEvent
    public static void onLogin(PlayerEvent.PlayerLoggedInEvent event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) {
            return;
        }
        if (PlayerData.addMilestone(player, "codex_given")) {
            ItemStack codex = new ItemStack(CodexContent.CODEX.get());
            if (!player.getInventory().add(codex)) {
                player.drop(codex, false);
            }
        }
        CodexBook.sync(player);
    }

    /** Whether {@code player} has everything {@code requires} lists. Creative players have walked every path. */
    public static boolean has(Player player, Set<String> milestones, List<String> requires) {
        if (player.isCreative()) {
            return true;
        }
        for (String need : requires) {
            if (!milestones.contains(need)) {
                return false;
            }
        }
        return true;
    }
}
