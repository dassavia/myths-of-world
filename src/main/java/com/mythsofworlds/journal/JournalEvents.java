package com.mythsofworlds.journal;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.codex.CodexBook;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.core.ServerConfig;
import com.mythsofworlds.mythology.Mythology;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

/** Writes journal entries (shown in the Codex of Myths) as players explore the worlds. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class JournalEvents {
    private JournalEvents() {
    }

    /** Adds the entry and tells the player, if it is new. */
    public static void unlock(Player player, Journal.Entry entry) {
        if (PlayerData.addEntry(player, entry.id())) {
            player.displayClientMessage(Component.translatable("journal.mythsofworlds.new_entry", entry.title())
                    .withStyle(ChatFormatting.GOLD), false);
            player.level().playSound(null, player.blockPosition(), SoundEvents.BOOK_PAGE_TURN, SoundSource.PLAYERS, 1.0F, 1.0F);
            if (player instanceof ServerPlayer serverPlayer) {
                CodexBook.sync(serverPlayer);
            }
        }
    }

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player) || player.tickCount % 40 != 0 || player.isSpectator()) {
            return;
        }
        ServerLevel level = player.serverLevel();
        Optional<String> volume = Mythology.of(level.dimension()).flatMap(Mythology::journal);
        if (volume.isEmpty()) {
            return;
        }
        // One look around per check, however many entries are still closed: the structures the player stands in,
        // and the kinds of creatures in sight.
        var here = level.structureManager().getAllStructuresAt(player.blockPosition());
        double sight = ServerConfig.get(ServerConfig.JOURNAL_SIGHT_RANGE);
        Set<EntityType<?>> nearby = new HashSet<>();
        for (Entity entity : level.getEntities(player, player.getBoundingBox().inflate(sight), e -> e.distanceToSqr(player) < sight * sight)) {
            nearby.add(entity.getType());
        }
        Set<EntityType<?>> seen = new HashSet<>();
        var structures = level.registryAccess().registryOrThrow(Registries.STRUCTURE);
        for (Journal.Entry entry : Journal.volume(volume.get())) {
            if (PlayerData.hasEntry(player, entry.id())) {
                continue;
            }
            if (entry.structure().isPresent() && !here.isEmpty()) {
                Structure structure = structures.get(entry.structure().get());
                if (structure != null && here.containsKey(structure)
                        && level.structureManager().getStructureWithPieceAt(player.blockPosition(), structure).isValid()) {
                    unlock(player, entry);
                }
            }
            if (entry.entity().isPresent()) {
                EntityType<?> type = BuiltInRegistries.ENTITY_TYPE.get(entry.entity().get());
                if (nearby.contains(type) && (seen.contains(type) || inSight(level, player, type, sight))) {
                    seen.add(type);
                    unlock(player, entry);
                }
            }
        }
    }

    /** Whether the player has a creature of this kind in sight. */
    private static boolean inSight(ServerLevel level, ServerPlayer player, EntityType<?> type, double sight) {
        return !level.getEntities(player, player.getBoundingBox().inflate(sight),
                e -> e.getType() == type && player.hasLineOfSight(e)).isEmpty();
    }

    @SubscribeEvent
    public static void onKill(LivingDeathEvent event) {
        if (!(event.getSource().getEntity() instanceof ServerPlayer player)) {
            return;
        }
        var id = BuiltInRegistries.ENTITY_TYPE.getKey(event.getEntity().getType());
        for (Mythology mythology : Mythology.values()) {
            for (Journal.Entry entry : mythology.journal().map(Journal::volume).orElse(List.of())) {
                if (entry.entity().isPresent() && entry.entity().get().equals(id)) {
                    unlock(player, entry);
                }
            }
        }
    }
}
