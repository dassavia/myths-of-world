package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.norse.BifrostPortalBlock;
import com.mythsofworlds.norse.BifrostPortalShape;
import com.mythsofworlds.registry.ModBlocks;
import com.mythsofworlds.world.ModDimensions;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** Run with {@code ./gradlew runGameTestServer}. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class NorsePortalTests {
    private static final BlockPos INSIDE = new BlockPos(1, 1, 1);

    /** 4x5 runestone frame in the X plane at z=1, interior x=1..2, y=1..3. */
    private static void buildFrame(GameTestHelper helper, boolean closed) {
        for (int x = 0; x <= 3; x++) {
            for (int y = 0; y <= 4; y++) {
                boolean edge = x == 0 || x == 3 || y == 0 || y == 4;
                if (edge && (closed || y != 4)) {
                    helper.setBlock(new BlockPos(x, y, 1), ModBlocks.RUNESTONE.get());
                }
            }
        }
    }

    @GameTest(template = "empty")
    public static void runeLightsClosedFrame(GameTestHelper helper) {
        buildFrame(helper, true);
        helper.assertTrue(BifrostPortalShape.tryLight(helper.getLevel(), helper.absolutePos(INSIDE)),
                "a closed runestone frame should light");
        for (int x = 1; x <= 2; x++) {
            for (int y = 1; y <= 3; y++) {
                helper.assertBlockPresent(ModBlocks.BIFROST_PORTAL.get(), new BlockPos(x, y, 1));
            }
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void runeIgnoresOpenFrame(GameTestHelper helper) {
        buildFrame(helper, false);
        helper.assertTrue(!BifrostPortalShape.tryLight(helper.getLevel(), helper.absolutePos(INSIDE)),
                "a frame without a top must not light");
        helper.assertBlockNotPresent(ModBlocks.BIFROST_PORTAL.get(), INSIDE);
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void portalCollapsesWhenFrameBreaks(GameTestHelper helper) {
        buildFrame(helper, true);
        BifrostPortalShape.tryLight(helper.getLevel(), helper.absolutePos(INSIDE));
        helper.setBlock(new BlockPos(0, 2, 1), Blocks.AIR);
        helper.succeedWhen(() -> {
            for (int x = 1; x <= 2; x++) {
                for (int y = 1; y <= 3; y++) {
                    helper.assertBlockNotPresent(ModBlocks.BIFROST_PORTAL.get(), new BlockPos(x, y, 1));
                }
            }
        });
    }

    /** Loads Jotunheim (validating its worldgen JSON), builds an arrival portal there and finds it again. */
    @GameTest(template = "empty", timeoutTicks = 400)
    public static void jotunheimArrivalPortal(GameTestHelper helper) {
        ServerLevel jotunheim = helper.getLevel().getServer().getLevel(ModDimensions.JOTUNHEIM);
        helper.assertTrue(jotunheim != null, "Jotunheim dimension is not loaded");
        BlockPos built = BifrostPortalBlock.findOrCreatePortal(jotunheim, new BlockPos(0, 64, 0));
        helper.assertTrue(jotunheim.getBlockState(built).is(ModBlocks.BIFROST_PORTAL.get()),
                "arrival portal was not built at " + built);
        BlockPos found = BifrostPortalBlock.findPortal(jotunheim, new BlockPos(3, 64, 3));
        helper.assertTrue(built.equals(found), "expected to find portal at " + built + " but got " + found);
        helper.succeed();
    }
}
