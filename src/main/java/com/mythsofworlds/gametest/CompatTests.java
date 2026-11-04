package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.compat.mca.McaCompat;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.norse.NorseEntities;
import java.util.List;
import java.util.Map;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.tags.StructureTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.level.block.Block;
import net.neoforged.fml.ModList;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/**
 * Compatibility with Minecraft Comes Alive Reborn. CI runs every test twice: without MCA and with MCA 7.7.32 in the
 * mods folder (environment variable {@code MYTHS_EXPECT_MCA=true}). The data part (tags) must be right in both; the
 * guard priorities must reach MCA's config only when it is there.
 */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class CompatTests {
    private static boolean expectMca() {
        return Boolean.parseBoolean(System.getenv().getOrDefault("MYTHS_EXPECT_MCA", "false"));
    }

    /** Smoke test of both set-ups: the mod runs alone, or MCA is there and the integration is live. */
    @GameTest(template = "empty")
    @SuppressWarnings("unchecked")
    public static void mcaIsOptional(GameTestHelper helper) throws Exception {
        boolean loaded = ModList.get().isLoaded(McaCompat.MODID);
        helper.assertTrue(loaded == expectMca(), "MCA loaded: " + loaded + ", expected: " + expectMca());
        if (!loaded) {
            helper.assertFalse(McaCompat.guardsConfigured(), "guard priorities were set without MCA");
            helper.succeed();
            return;
        }
        String version = ModList.get().getModContainerById(McaCompat.MODID).orElseThrow().getModInfo().getVersion().toString();
        MythsOfWorlds.LOGGER.info("compat test with MCA {}", version);
        helper.assertTrue(McaCompat.guardsConfigured(), "guard priorities were not added to MCA's config");
        Class<?> configClass = Class.forName("net.conczin.mca.Config");
        Object config = configClass.getMethod("getInstance").invoke(null);
        Map<String, Integer> guards = (Map<String, Integer>) configClass.getField("guardsTargetEntities").get(config);
        helper.assertTrue(guards.get("#" + McaCompat.GUARD_IGNORED.location()) < 0, "the ignored tag is not ignored: " + guards);
        helper.assertTrue(guards.get("#" + McaCompat.GUARD_TARGETS.location()) >= 0, "the target tag is not targeted: " + guards);
        helper.assertTrue(guards.keySet().iterator().next().equals("#" + McaCompat.GUARD_IGNORED.location()),
                "the ignored tag must be checked before every other tag");
        helper.assertTrue(guards.containsKey("minecraft:zombie"), "MCA's own priorities were lost: " + guards);
        helper.succeed();
    }

    /** Every monster of ours is either a guard target or ignored, and gods, traders and friends are never targets. */
    @GameTest(template = "empty")
    public static void guardTagsCoverEveryMob(GameTestHelper helper) {
        for (EntityType<?> type : BuiltInRegistries.ENTITY_TYPE) {
            ResourceLocation id = BuiltInRegistries.ENTITY_TYPE.getKey(type);
            if (!id.getNamespace().equals(MythsOfWorlds.MODID) || type.getCategory() == MobCategory.MISC) {
                continue;
            }
            boolean target = type.is(McaCompat.GUARD_TARGETS);
            boolean ignored = type.is(McaCompat.GUARD_IGNORED);
            helper.assertFalse(target && ignored, id + " is both a guard target and ignored");
            if (type.getCategory() == MobCategory.MONSTER) {
                helper.assertTrue(target || ignored, id + " is in neither mca/guard_targets nor mca/guard_ignored");
            } else {
                helper.assertFalse(target, id + " is friendly but a guard target");
            }
        }
        List<EntityType<?>> protectedTypes = new java.util.ArrayList<>();
        EgyptianEntities.gods().forEach(god -> protectedTypes.add(god.get()));
        protectedTypes.add(EgyptianEntities.SET.get());
        protectedTypes.add(NorseEntities.HEIMDALL.get());
        protectedTypes.add(EgyptianEntities.EGYPTIAN_MERCHANT.get());
        protectedTypes.add(EgyptianEntities.PRIESTESS.get());
        for (EntityType<?> type : protectedTypes) {
            helper.assertTrue(type.is(McaCompat.GUARD_IGNORED), BuiltInRegistries.ENTITY_TYPE.getKey(type) + " is not ignored by guards");
        }
        helper.succeed();
    }

    /** The Egyptian village is a village, and the brazier gets MCA's exact pathfinding check. */
    @GameTest(template = "empty")
    public static void villageAndPathfindingTags(GameTestHelper helper) {
        var structures = helper.getLevel().registryAccess().registryOrThrow(Registries.STRUCTURE);
        var village = structures.getHolderOrThrow(ResourceKey.create(Registries.STRUCTURE, MythsOfWorlds.id("egyptian_village")));
        helper.assertTrue(village.is(StructureTags.VILLAGE), "egyptian_village is not in #minecraft:village");
        TagKey<Block> pathfinding = TagKey.create(Registries.BLOCK,
                ResourceLocation.fromNamespaceAndPath(McaCompat.MODID, "villager_pathfinding_collision_checks"));
        helper.assertTrue(GreekContent.BRAZIER.get().defaultBlockState().is(pathfinding), "the brazier is not in " + pathfinding.location());
        helper.succeed();
    }
}
