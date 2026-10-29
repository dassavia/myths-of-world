package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.Mythology;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.greek.entity.GreekMerchant;
import com.mythsofworlds.mythology.greek.entity.Hippolyta;
import com.mythsofworlds.mythology.greek.portal.PoolPortal;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.norse.entity.DraugrChieftain;
import com.mythsofworlds.mythology.norse.entity.Fenrir;
import com.mythsofworlds.mythology.norse.entity.Garm;
import com.mythsofworlds.mythology.norse.entity.NorseMerchant;
import com.mythsofworlds.mythology.norse.entity.Surtr;
import com.mythsofworlds.mythology.norse.entity.Thrym;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.HolderSet;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;
import net.minecraft.world.phys.AABB;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.server.ServerStartedEvent;

/**
 * The game-test server only creates vanilla levels, so this check runs on a real dedicated server instead:
 * {@code ./gradlew runSmokeTest} (needs eula=true in run/smoke/eula.txt). It loads every mythology's dimension,
 * generates terrain, finds every biome and structure of Hellas and Jotunheim, generates them, then exits with code 0 or 1.
 * It does nothing unless the system property {@value #PROPERTY} is set.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class WorldSmokeTest {
    public static final String PROPERTY = "mythsofworlds.smokeTest";

    private WorldSmokeTest() {
    }

    private interface Check {
        void run() throws Exception;
    }

    private static void check(List<String> failures, String what, Check check) {
        try {
            check.run();
        } catch (Throwable e) {
            failures.add(what + ": " + e);
            System.out.println("[smoke] FAIL " + what);
            e.printStackTrace(System.out);
        }
    }

    private static void report(String line) {
        System.out.println("[smoke] " + line);
        System.out.flush();
    }

    /** Finds every biome and structure of one world, generates the structures and checks who lives in them. */
    private static void checkWorld(MinecraftServer server, List<String> failures, ServerLevel level, List<String> biomes,
                                   List<String> structureNames) {
        String world = level.dimension().location().getPath();
        for (String biome : biomes) {
            check(failures, world + " biome " + biome, () -> {
                ResourceKey<Biome> key = ResourceKey.create(Registries.BIOME, MythsOfWorlds.id(biome));
                var found = level.findClosestBiome3d(holder -> holder.is(key), new BlockPos(0, 80, 0), 6400, 32, 64);
                if (found == null) {
                    throw new IllegalStateException("not found within 6400 blocks");
                }
                report("biome " + biome + " at " + found.getFirst());
            });
        }
        var structures = server.registryAccess().registryOrThrow(Registries.STRUCTURE);
        for (String name : structureNames) {
            check(failures, world + " structure " + name, () -> {
                Holder<Structure> holder = structures.getHolderOrThrow(ResourceKey.create(Registries.STRUCTURE, MythsOfWorlds.id(name)));
                var found = level.getChunkSource().getGenerator()
                        .findNearestMapStructure(level, HolderSet.direct(holder), BlockPos.ZERO, 250, false);
                if (found == null) {
                    throw new IllegalStateException("not found within 250 chunks");
                }
                BlockPos pos = found.getFirst();
                for (int dx = -4; dx <= 4; dx++) {
                    for (int dz = -4; dz <= 4; dz++) {
                        level.getChunk((pos.getX() >> 4) + dx, (pos.getZ() >> 4) + dz);
                    }
                }
                // The located position sits at y=0; in Jotunheim's amplified mountains a lair can stand far above that.
                AABB around = new AABB(pos.getX() - 72, level.getMinBuildHeight(), pos.getZ() - 72,
                        pos.getX() + 72, level.getMaxBuildHeight(), pos.getZ() + 72);
                int mobs = level.getEntitiesOfClass(Mob.class, around).size();
                Class<? extends Mob> resident = RESIDENTS.get(name);
                if (resident != null && level.getEntitiesOfClass(resident, around).isEmpty()) {
                    throw new IllegalStateException(name + " has no " + resident.getSimpleName());
                }
                if (name.equals("labyrinth")) {
                    int surface = level.getHeight(Heightmap.Types.WORLD_SURFACE_WG, pos.getX(), pos.getZ());
                    var start = level.structureManager().getStructureWithPieceAt(pos.atY(surface - 18), holder.value());
                    report("labyrinth: surface y=" + surface + ", maze below the surface: " + start.isValid());
                }
                report("structure " + name + " generated at " + pos + " (surface y="
                        + level.getHeight(Heightmap.Types.WORLD_SURFACE_WG, pos.getX(), pos.getZ()) + "), mobs around: " + mobs);
            });
        }
    }

    /** Structures that must have someone living in them once generated. */
    private static final Map<String, Class<? extends Mob>> RESIDENTS = Map.ofEntries(
            Map.entry("agora", GreekMerchant.class),
            Map.entry("amazon_camp", Amazon.class),
            Map.entry("themiscyra", Hippolyta.class),
            Map.entry("viking_village", NorseMerchant.class),
            Map.entry("dwarf_forge", NorseMerchant.class),
            Map.entry("barrow", DraugrChieftain.class),
            Map.entry("utgard", Thrym.class),
            Map.entry("fenrir_island", Fenrir.class),
            Map.entry("muspel_fortress", Surtr.class),
            Map.entry("helgrind", Garm.class));

    @SubscribeEvent
    public static void onServerStarted(ServerStartedEvent event) {
        if (!Boolean.getBoolean(PROPERTY)) {
            return;
        }
        MinecraftServer server = event.getServer();
        List<String> failures = new ArrayList<>();
        for (Mythology mythology : Mythology.values()) {
            check(failures, "dimension " + mythology, () -> {
                ServerLevel level = server.getLevel(mythology.dimension());
                if (level == null) {
                    throw new IllegalStateException(mythology.dimension().location() + " is not loaded");
                }
                level.getChunk(0, 0);
                report(mythology.dimension().location() + ": surface at 0,0 is y="
                        + level.getHeight(Heightmap.Types.WORLD_SURFACE, 0, 0));
            });
        }
        ServerLevel hellas = server.getLevel(GreekContent.HELLAS);
        if (hellas != null) {
            check(failures, "arrival portal", () -> {
                BlockPos portal = PoolPortal.findOrCreate(hellas, new BlockPos(0, 64, 0));
                report("arrival portal built at " + portal);
            });
            checkWorld(server, failures, hellas, GreekContent.BIOMES, GreekContent.STRUCTURES);
        } else {
            failures.add("Hellas is not loaded");
        }
        ServerLevel jotunheim = server.getLevel(NorseContent.JOTUNHEIM);
        if (jotunheim != null) {
            checkWorld(server, failures, jotunheim, NorseContent.BIOMES, NorseContent.STRUCTURES);
        } else {
            failures.add("Jotunheim is not loaded");
        }
        report(failures.isEmpty() ? "OK" : "FAILED " + failures.size() + ": " + failures);
        Runtime.getRuntime().halt(failures.isEmpty() ? 0 : 1);
    }
}
