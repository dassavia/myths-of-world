package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.portal.MythPortalBlock;
import com.mythsofworlds.core.portal.PortalShape;
import com.mythsofworlds.mythology.Mythology;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.entity.Hydra;
import com.mythsofworlds.mythology.greek.entity.NemeanLion;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.NbtAccounter;
import net.minecraft.nbt.NbtIo;
import net.minecraft.nbt.Tag;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.FeatureSorter;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** Greek content: portal, data files, structures and mobs. Run with {@code ./gradlew runGameTestServer}. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class GreekTests {
    private static final BlockPos INSIDE = new BlockPos(1, 1, 1);

    private static MythPortalBlock portal() {
        return GreekContent.HELLAS_PORTAL.get();
    }

    @GameTest(template = "empty")
    public static void torchLightsMarbleFrame(GameTestHelper helper) {
        for (int x = 0; x <= 3; x++) {
            for (int y = 0; y <= 4; y++) {
                if (x == 0 || x == 3 || y == 0 || y == 4) {
                    helper.setBlock(new BlockPos(x, y, 1), GreekContent.OLYMPIAN_MARBLE.get());
                }
            }
        }
        helper.assertTrue(PortalShape.tryLight(helper.getLevel(), helper.absolutePos(INSIDE), portal()),
                "a closed Olympian marble frame should light");
        helper.assertBlockPresent(portal(), new BlockPos(2, 3, 1));
        helper.succeed();
    }

    /** Plain marble is decoration only: it must not open the portal. */
    @GameTest(template = "empty")
    public static void torchIgnoresPlainMarble(GameTestHelper helper) {
        for (int x = 0; x <= 3; x++) {
            for (int y = 0; y <= 4; y++) {
                if (x == 0 || x == 3 || y == 0 || y == 4) {
                    helper.setBlock(new BlockPos(x, y, 1), GreekContent.MARBLE.get());
                }
            }
        }
        helper.assertTrue(!PortalShape.tryLight(helper.getLevel(), helper.absolutePos(INSIDE), portal()),
                "a plain marble frame must not light");
        helper.succeed();
    }

    /** Every mythology's dimension type and every biome of Hellas parsed. */
    @GameTest(template = "empty")
    public static void worldDataLoads(GameTestHelper helper) {
        var registries = helper.getLevel().registryAccess();
        for (Mythology mythology : Mythology.values()) {
            helper.assertTrue(registries.registryOrThrow(Registries.DIMENSION_TYPE).containsKey(mythology.dimension().location()),
                    "dimension_type for " + mythology + " did not load");
        }
        for (String biome : GreekContent.BIOMES) {
            helper.assertTrue(registries.registryOrThrow(Registries.BIOME).containsKey(MythsOfWorlds.id(biome)),
                    "worldgen/biome/" + biome + ".json did not load");
        }
        helper.succeed();
    }

    /** The biomes of one dimension must list shared features in the same order, or the world fails to load. */
    @GameTest(template = "empty")
    public static void hellasFeatureOrderIsConsistent(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        List<Holder<Biome>> hellas = new ArrayList<>();
        for (String biome : GreekContent.BIOMES) {
            hellas.add(biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME, MythsOfWorlds.id(biome))));
        }
        FeatureSorter.buildFeaturesPerStep(hellas, holder -> holder.value().getGenerationSettings().features(), true);
        helper.succeed();
    }

    /** Structures are registered, their templates load, and every mob inside a template is a real entity type. */
    @GameTest(template = "empty")
    public static void structuresLoad(GameTestHelper helper) throws Exception {
        var server = helper.getLevel().getServer();
        var structures = helper.getLevel().registryAccess().registryOrThrow(Registries.STRUCTURE);
        for (String name : GreekContent.STRUCTURES) {
            helper.assertTrue(structures.containsKey(MythsOfWorlds.id(name)), "worldgen/structure/" + name + ".json did not load");
            ResourceLocation template = MythsOfWorlds.id("greek/" + name);
            helper.assertTrue(server.getStructureManager().get(template).isPresent(), "template " + template + " missing");
            Resource file = server.getResourceManager().getResourceOrThrow(MythsOfWorlds.id("structure/greek/" + name + ".nbt"));
            try (InputStream in = file.open()) {
                CompoundTag root = NbtIo.readCompressed(in, NbtAccounter.unlimitedHeap());
                for (Tag entity : root.getList("entities", Tag.TAG_COMPOUND)) {
                    CompoundTag tag = ((CompoundTag) entity).getCompound("nbt");
                    helper.assertTrue(EntityType.by(tag).isPresent(), name + ": unknown entity " + tag.getString("id"));
                }
            }
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void everyMobSpawns(GameTestHelper helper) {
        for (var type : GreekEntities.all()) {
            Mob mob = helper.spawn(type.get(), new BlockPos(1, 2, 1));
            helper.assertTrue(mob.isAlive() && mob.getHealth() > 0, type.getId() + " did not spawn alive");
            mob.discard();
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void nemeanLionShrugsOffProjectiles(GameTestHelper helper) {
        NemeanLion lion = helper.spawn(GreekEntities.NEMEAN_LION.get(), new BlockPos(1, 2, 1));
        lion.hurt(helper.getLevel().damageSources().thrown(lion, null), 20.0F);
        helper.assertTrue(lion.getHealth() == lion.getMaxHealth(), "projectiles must not hurt the Nemean lion");
        lion.hurt(helper.getLevel().damageSources().generic(), 20.0F);
        helper.assertTrue(lion.getHealth() < lion.getMaxHealth(), "melee and other damage must hurt it");
        lion.discard();
        helper.succeed();
    }

    @GameTest(template = "empty", timeoutTicks = 120)
    public static void hydraRegeneratesUnlessBurned(GameTestHelper helper) {
        Hydra healing = helper.spawn(GreekEntities.HYDRA.get(), new BlockPos(1, 2, 1));
        healing.setHealth(100.0F);
        Hydra burned = helper.spawn(GreekEntities.HYDRA.get(), new BlockPos(1, 2, 1));
        burned.setHealth(101.0F);
        burned.hurt(helper.getLevel().damageSources().inFire(), 1.0F);
        float burnedStart = burned.getHealth();
        helper.runAfterDelay(80, () -> {
            helper.assertTrue(healing.getHealth() > 100.0F, "the hydra should regenerate");
            helper.assertTrue(burned.getHealth() <= burnedStart, "fire should stop the hydra regenerating");
            healing.discard();
            burned.discard();
            helper.succeed();
        });
    }
}
