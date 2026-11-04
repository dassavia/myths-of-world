package com.mythsofworlds.core;

/**
 * Timing and layout of the banner with the world's name that appears when the player enters a world of the myths
 * (drawn by core/client/MythHud). Plain arithmetic with no client classes, so the game tests can check it for every GUI
 * scale: it fades in, stays about two seconds and fades out, never fully opaque; it sits at the top centre of the
 * screen, below any boss bars; and it is drawn at {@link ClientConfig#WORLD_BANNER_SCALE} of the full scroll, but
 * never so small that the letters drop under {@value #MIN_TEXT_PIXELS} pixels of the real screen.
 */
public final class WorldBanner {
    /** The scroll at full size, in GUI pixels. */
    public static final int WIDTH = 104;
    public static final int HEIGHT = 18;
    public static final long FADE_IN_MS = 400;
    public static final long HOLD_MS = 1600;
    public static final long FADE_OUT_MS = 500;
    public static final long TOTAL_MS = FADE_IN_MS + HOLD_MS + FADE_OUT_MS;
    /** How opaque the banner gets at most: the world behind it shows through. */
    public static final float MAX_ALPHA = 0.85F;
    /** The smallest height of the letters on the real screen, in pixels, for the Cyrillic to stay readable. */
    public static final float MIN_TEXT_PIXELS = 8.0F;
    /** Height of a line of the font, in GUI pixels. */
    public static final int LINE_HEIGHT = 9;
    /** Space between the top of the screen (or the last boss bar) and the banner. */
    public static final int MARGIN = 4;

    private WorldBanner() {
    }

    /** Opacity {@code ageMs} milliseconds after entering the world; 0 before and after. */
    public static float alpha(long ageMs) {
        if (ageMs < 0 || ageMs >= TOTAL_MS) {
            return 0.0F;
        }
        if (ageMs < FADE_IN_MS) {
            return MAX_ALPHA * ageMs / FADE_IN_MS;
        }
        if (ageMs < FADE_IN_MS + HOLD_MS) {
            return MAX_ALPHA;
        }
        return MAX_ALPHA * (TOTAL_MS - ageMs) / FADE_OUT_MS;
    }

    /** The scale the banner is drawn at for the configured scale and the GUI scale of the window. */
    public static float scale(double configured, double guiScale) {
        float readable = (float) (MIN_TEXT_PIXELS / (LINE_HEIGHT * Math.max(1.0, guiScale)));
        return Math.min(1.0F, Math.max((float) configured, readable));
    }

    /** Left edge, in GUI pixels, that centres the banner on a screen {@code guiWidth} wide. */
    public static int left(int guiWidth, float scale) {
        return Math.round((guiWidth - WIDTH * scale) / 2.0F);
    }

    /** Top edge, in GUI pixels: at the top of the screen, or just below the boss bars that reach down to {@code bossBottom}. */
    public static int top(int bossBottom) {
        return Math.max(MARGIN, bossBottom + MARGIN);
    }
}
