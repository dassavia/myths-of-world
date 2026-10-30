package com.mythsofworlds.journal;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.codex.Progress;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import java.util.List;
import java.util.Map;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

/** Writes journal entries (shown in the Codex of Myths) as players explore the worlds. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class JournalEvents {
    /** Which world each volume belongs to. */
    private static final Map<ResourceKey<Level>, Volume> VOLUMES = Map.of(
            GreekContent.HELLAS, new Volume("greek"),
            NorseContent.JOTUNHEIM, new Volume("norse"),
            SlavicContent.NAV, new Volume("slavic"));
    private static final double SIGHT_RANGE = 20.0;

    private record Volume(String id) {
    }

    private JournalEvents() {
    }

    /** Adds the entry and tells the player, if it is new. */
    public static void unlock(Player player, Journal.Entry entry) {
        if (PlayerData.addEntry(player, entry.id())) {
            player.displayClientMessage(Component.translatable("journal.mythsofworlds.new_entry", entry.title())
                    .withStyle(ChatFormatting.GOLD), false);
            player.level().playSound(null, player.blockPosition(), SoundEvents.BOOK_PAGE_TURN, SoundSource.PLAYERS, 1.0F, 1.0F);
            if (player instanceof ServerPlayer serverPlayer) {
                Progress.sync(serverPlayer);
            }
        }
    }

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player) || player.tickCount % 40 != 0 || player.isSpectator()) {
            return;
        }
        ServerLevel level = player.serverLevel();
        Volume volume = VOLUMES.get(level.dimension());
        if (volume == null) {
            return;
        }
        List<Journal.Entry> entries = Journal.volume(volume.id());
        var structures = level.registryAccess().registryOrThrow(Registries.STRUCTURE);
        for (Journal.Entry entry : entries) {
            if (PlayerData.hasEntry(player, entry.id())) {
                continue;
            }
            if (entry.structure().isPresent()) {
                Structure structure = structures.get(entry.structure().get());
                if (structure != null && level.structureManager().getStructureWithPieceAt(player.blockPosition(), structure).isValid()) {
                    unlock(player, entry);
                }
            }
            if (entry.entity().isPresent()) {
                var type = BuiltInRegistries.ENTITY_TYPE.get(entry.entity().get());
                List<Entity> seen = level.getEntities(player, player.getBoundingBox().inflate(SIGHT_RANGE),
                        e -> e.getType() == type && player.hasLineOfSight(e));
                if (!seen.isEmpty()) {
                    unlock(player, entry);
                }
            }
        }
    }

    @SubscribeEvent
    public static void onKill(LivingDeathEvent event) {
        if (!(event.getSource().getEntity() instanceof ServerPlayer player)) {
            return;
        }
        var id = BuiltInRegistries.ENTITY_TYPE.getKey(event.getEntity().getType());
        for (Volume volume : VOLUMES.values()) {
            for (Journal.Entry entry : Journal.volume(volume.id())) {
                if (entry.entity().isPresent() && entry.entity().get().equals(id)) {
                    unlock(player, entry);
                }
            }
        }
    }
}
