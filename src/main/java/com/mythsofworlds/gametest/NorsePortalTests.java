package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.portal.MythPortalBlock;
import com.mythsofworlds.core.portal.PortalPlacement;
import com.mythsofworlds.core.portal.PortalShape;
import com.mythsofworlds.mythology.norse.NorseContent;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** Run with {@code ./gradlew runGameTestServer}. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class NorsePortalTests {
    private static final BlockPos INSIDE = new BlockPos(1, 1, 1);

    private static MythPortalBlock portal() {
        return NorseContent.BIFROST_PORTAL.get();
    }

    /** 4x5 runestone frame in the X plane at z=1, interior x=1..2, y=1..3. */
    private static void buildFrame(GameTestHelper helper, boolean closed) {
        for (int x = 0; x <= 3; x++) {
            for (int y = 0; y <= 4; y++) {
                boolean edge = x == 0 || x == 3 || y == 0 || y == 4;
                if (edge && (closed || y != 4)) {
                    helper.setBlock(new BlockPos(x, y, 1), NorseContent.RUNESTONE.get());
                }
            }
        }
    }

    @GameTest(template = "empty")
    public static void runeLightsClosedFrame(GameTestHelper helper) {
        buildFrame(helper, true);
        helper.assertTrue(PortalShape.tryLight(helper.getLevel(), helper.absolutePos(INSIDE), portal()),
                "a closed runestone frame should light");
        for (int x = 1; x <= 2; x++) {
            for (int y = 1; y <= 3; y++) {
                helper.assertBlockPresent(portal(), new BlockPos(x, y, 1));
            }
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void runeIgnoresOpenFrame(GameTestHelper helper) {
        buildFrame(helper, false);
        helper.assertTrue(!PortalShape.tryLight(helper.getLevel(), helper.absolutePos(INSIDE), portal()),
                "a frame without a top must not light");
        helper.assertBlockNotPresent(portal(), INSIDE);
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void portalCollapsesWhenFrameBreaks(GameTestHelper helper) {
        buildFrame(helper, true);
        PortalShape.tryLight(helper.getLevel(), helper.absolutePos(INSIDE), portal());
        helper.setBlock(new BlockPos(0, 2, 1), Blocks.AIR);
        helper.succeedWhen(() -> {
            for (int x = 1; x <= 2; x++) {
                for (int y = 1; y <= 3; y++) {
                    helper.assertBlockNotPresent(portal(), new BlockPos(x, y, 1));
                }
            }
        });
    }

    /**
     * The game-test server only creates vanilla levels, so Jotunheim itself is not loaded here.
     * Instead check that its dimension type and biomes parsed, which catches most JSON mistakes.
     */
    @GameTest(template = "empty")
    public static void jotunheimDataLoads(GameTestHelper helper) {
        var registries = helper.getLevel().registryAccess();
        helper.assertTrue(registries.registryOrThrow(Registries.DIMENSION_TYPE).containsKey(NorseContent.JOTUNHEIM.location()),
                "dimension_type/jotunheim.json did not load");
        for (String biome : new String[]{"frost_wastes", "giants_taiga"}) {
            helper.assertTrue(registries.registryOrThrow(Registries.BIOME).containsKey(MythsOfWorlds.id(biome)),
                    "worldgen/biome/" + biome + ".json did not load");
        }
        helper.succeed();
    }

    /** Arrival portal: built on the surface the first time, found again (not rebuilt) the second time. */
    @GameTest(template = "empty")
    public static void arrivalPortalIsBuiltThenReused(GameTestHelper helper) {
        BlockPos near = helper.absolutePos(new BlockPos(1, 1, 1)).offset(200, 0, 200);
        BlockPos built = PortalPlacement.findOrCreate(helper.getLevel(), near, portal());
        helper.assertTrue(helper.getLevel().getBlockState(built).is(portal()), "arrival portal was not built at " + built);
        BlockPos found = PortalPlacement.findOrCreate(helper.getLevel(), near.offset(3, 0, 3), portal());
        helper.assertTrue(built.equals(found), "expected to reuse portal at " + built + " but got " + found);
        helper.succeed();
    }
}
