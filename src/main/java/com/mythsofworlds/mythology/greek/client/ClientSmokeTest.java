package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.client.gui.screens.AccessibilityOnboardingScreen;
import net.minecraft.client.gui.screens.TitleScreen;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ScreenEvent;

/**
 * {@code ./gradlew runClientSmokeTest}: starts the game and quits as soon as the title screen (or, on a first launch, the accessibility screen) opens. By then every
 * entity renderer has been built and every model baked, so a broken model crashes the run instead of a player's game.
 * Does nothing unless the system property {@value #PROPERTY} is set.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, value = Dist.CLIENT)
public final class ClientSmokeTest {
    public static final String PROPERTY = "mythsofworlds.clientSmokeTest";

    private ClientSmokeTest() {
    }

    @SubscribeEvent
    public static void onScreenOpening(ScreenEvent.Opening event) {
        if (Boolean.getBoolean(PROPERTY) && (event.getNewScreen() instanceof TitleScreen
                || event.getNewScreen() instanceof AccessibilityOnboardingScreen)) {
            System.out.println("[client-smoke] OK: title screen reached, all renderers and models loaded");
            System.out.flush();
            Runtime.getRuntime().halt(0);
        }
    }
}
