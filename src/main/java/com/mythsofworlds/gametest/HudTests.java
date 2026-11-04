package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.WorldBanner;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** The banner with the world's name: short, see-through, at the top, small but readable at every GUI scale. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class HudTests {
    @GameTest(template = "empty")
    public static void worldBannerFadesInAndOut(GameTestHelper helper) {
        helper.assertTrue(WorldBanner.alpha(-1) == 0.0F && WorldBanner.alpha(0) == 0.0F, "the banner shows before entering");
        helper.assertTrue(WorldBanner.alpha(WorldBanner.FADE_IN_MS / 2) > 0.0F
                && WorldBanner.alpha(WorldBanner.FADE_IN_MS / 2) < WorldBanner.MAX_ALPHA, "the banner does not fade in");
        helper.assertTrue(WorldBanner.alpha(1000) == WorldBanner.MAX_ALPHA && WorldBanner.MAX_ALPHA < 1.0F, "the banner is not see-through");
        helper.assertTrue(WorldBanner.alpha(WorldBanner.TOTAL_MS - 100) < WorldBanner.MAX_ALPHA, "the banner does not fade out");
        helper.assertTrue(WorldBanner.alpha(WorldBanner.TOTAL_MS) == 0.0F, "the banner stays");
        helper.assertTrue(WorldBanner.TOTAL_MS >= 1800 && WorldBanner.TOTAL_MS <= 3000, "the banner should show about two seconds");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void worldBannerFitsEveryGuiScale(GameTestHelper helper) {
        int[][] screens = {{854, 480}, {1280, 720}, {1920, 1080}, {2560, 1440}};
        for (int[] screen : screens) {
            for (int guiScale = 1; guiScale <= 4; guiScale++) {
                int guiWidth = (int) Math.ceil(screen[0] / (double) guiScale);
                int guiHeight = (int) Math.ceil(screen[1] / (double) guiScale);
                float scale = WorldBanner.scale(0.5, guiScale);
                int left = WorldBanner.left(guiWidth, scale);
                float width = WorldBanner.WIDTH * scale;
                String where = screen[0] + "x" + screen[1] + " at GUI scale " + guiScale;
                helper.assertTrue(left >= 0 && left + width <= guiWidth, "the banner leaves the screen at " + where);
                helper.assertTrue(Math.abs(left + width / 2 - guiWidth / 2.0F) <= 1.0F, "the banner is not centred at " + where);
                helper.assertTrue(WorldBanner.LINE_HEIGHT * scale * guiScale >= WorldBanner.MIN_TEXT_PIXELS - 0.01F,
                        "the name is too small to read at " + where);
                helper.assertTrue(WorldBanner.top(0) + WorldBanner.HEIGHT * scale < guiHeight / 6.0F,
                        "the banner reaches too far down at " + where);
                if (guiScale >= 2) {
                    helper.assertTrue(scale <= 0.5F, "the banner is not half size at " + where);
                }
            }
        }
        // Below the boss bars (a god's bar ends at about 12 + 19 pixels), never over them.
        helper.assertTrue(WorldBanner.top(31) > 31, "the banner covers the boss bars");
        helper.assertTrue(WorldBanner.scale(0.1, 4) >= 0.22F && WorldBanner.scale(2.0, 1) == 1.0F, "the scale is not clamped");
        helper.succeed();
    }
}
