package com.mythsofworlds.core;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.Mythology;
import com.mojang.datafixers.util.Pair;
import java.util.Map;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.HolderSet;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.level.levelgen.structure.Structure;

/**
 * Where the next monster of this world waits: the nearest lair of a boss the player has not beaten yet (from the lists
 * in {@link Mythology}). Read by the Delphic laurel of Hellas and the yarn ball of Nav.
 */
public final class Prophecy {
    /** How far to look, in chunks: the lairs stand about 600 blocks apart. */
    public static final int SEARCH_CHUNKS = 96;

    /** The boss, its lair and where the lair stands. */
    public record Lair(String boss, String structure, BlockPos pos) {
        public Component bossName() {
            return Component.translatable("entity." + MythsOfWorlds.MODID + "." + boss);
        }
    }

    private Prophecy() {
    }

    /** The nearest lair of an unbeaten boss of this world, if any is left within reach. */
    public static Optional<Lair> nextLair(ServerPlayer player) {
        ServerLevel level = player.serverLevel();
        Optional<Mythology> mythology = Mythology.of(level.dimension());
        if (mythology.isEmpty()) {
            return Optional.empty();
        }
        var structures = level.registryAccess().registryOrThrow(Registries.STRUCTURE);
        Lair best = null;
        for (Map.Entry<String, String> entry : mythology.get().lairs().entrySet()) {
            if (PlayerData.hasMilestone(player, "kill." + entry.getKey())) {
                continue;
            }
            Optional<Holder.Reference<Structure>> holder = structures.getHolder(
                    ResourceKey.create(Registries.STRUCTURE, MythsOfWorlds.id(entry.getValue())));
            if (holder.isEmpty()) {
                continue;
            }
            Pair<BlockPos, Holder<Structure>> found = level.getChunkSource().getGenerator().findNearestMapStructure(level,
                    HolderSet.direct(holder.get()), player.blockPosition(), SEARCH_CHUNKS, false);
            if (found != null && (best == null || found.getFirst().distSqr(player.blockPosition()) < best.pos().distSqr(player.blockPosition()))) {
                best = new Lair(entry.getKey(), entry.getValue(), found.getFirst());
            }
        }
        return Optional.ofNullable(best);
    }

    /** "north-east" and the like, as a translation key ending: n, ne, e, se, s, sw, w, nw. */
    public static String direction(BlockPos from, BlockPos to) {
        double angle = Math.toDegrees(Math.atan2(to.getX() - from.getX(), from.getZ() - to.getZ()));
        String[] names = {"n", "ne", "e", "se", "s", "sw", "w", "nw"};
        return names[Math.floorMod(Math.round(angle / 45.0), 8)];
    }

    /** Horizontal distance in blocks. */
    public static int distance(BlockPos from, BlockPos to) {
        return (int) Math.round(Math.hypot(to.getX() - from.getX(), to.getZ() - from.getZ()));
    }
}
