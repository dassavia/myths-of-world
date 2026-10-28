package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.portal.PortalPlacement;
import com.mythsofworlds.mythology.Mythology;
import com.mythsofworlds.mythology.greek.GreekContent;
import java.util.ArrayList;
import java.util.List;
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
 * generates terrain, finds every biome and structure of Hellas, generates them, then exits with code 0 or 1.
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
                BlockPos portal = PortalPlacement.findOrCreate(hellas, new BlockPos(0, 64, 0), GreekContent.HELLAS_PORTAL.get());
                report("arrival portal built at " + portal);
            });
            for (String biome : GreekContent.BIOMES) {
                check(failures, "biome " + biome, () -> {
                    ResourceKey<Biome> key = ResourceKey.create(Registries.BIOME, MythsOfWorlds.id(biome));
                    var found = hellas.findClosestBiome3d(holder -> holder.is(key), new BlockPos(0, 80, 0), 6400, 32, 64);
                    if (found == null) {
                        throw new IllegalStateException("not found within 6400 blocks");
                    }
                    report("biome " + biome + " at " + found.getFirst());
                });
            }
            var structures = server.registryAccess().registryOrThrow(Registries.STRUCTURE);
            for (String name : GreekContent.STRUCTURES) {
                check(failures, "structure " + name, () -> {
                    Holder<Structure> holder = structures.getHolderOrThrow(ResourceKey.create(Registries.STRUCTURE, MythsOfWorlds.id(name)));
                    var found = hellas.getChunkSource().getGenerator()
                            .findNearestMapStructure(hellas, HolderSet.direct(holder), BlockPos.ZERO, 150, false);
                    if (found == null) {
                        throw new IllegalStateException("not found within 150 chunks");
                    }
                    BlockPos pos = found.getFirst();
                    for (int dx = -1; dx <= 1; dx++) {
                        for (int dz = -1; dz <= 1; dz++) {
                            hellas.getChunk((pos.getX() >> 4) + dx, (pos.getZ() >> 4) + dz);
                        }
                    }
                    int mobs = hellas.getEntitiesOfClass(Mob.class, new AABB(pos).inflate(48, 128, 48)).size();
                    report("structure " + name + " generated at " + pos + ", mobs around: " + mobs);
                });
            }
        } else {
            failures.add("Hellas is not loaded");
        }
        report(failures.isEmpty() ? "OK" : "FAILED " + failures.size() + ": " + failures);
        Runtime.getRuntime().halt(failures.isEmpty() ? 0 : 1);
    }
}
