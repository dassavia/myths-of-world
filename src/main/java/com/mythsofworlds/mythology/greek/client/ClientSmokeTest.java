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
            var resources = net.minecraft.client.Minecraft.getInstance().getResourceManager();
            java.util.List<String> textures = new java.util.ArrayList<>(java.util.List.of("hippolyta", "isis"));
            for (int i = 0; i < com.mythsofworlds.mythology.greek.entity.Amazon.VARIANTS; i++) {
                textures.add("amazon_" + i);
            }
            for (int i = 0; i < 8; i++) {
                textures.add("valkyrie_" + i);
                textures.add("priestess_" + i);
            }
            for (String name : textures) {
                if (resources.getResource(MythsOfWorlds.id("textures/entity/" + name + ".png")).isEmpty()) {
                    System.out.println("[client-smoke] FAIL: missing texture textures/entity/" + name + ".png");
                    System.out.flush();
                    Runtime.getRuntime().halt(1);
                }
            }
            System.out.println("[client-smoke] OK: title screen reached, all renderers, models and the women's textures loaded"
                    + (net.neoforged.fml.ModList.get().isLoaded("mca") ? ", MCA looks " + (com.mythsofworlds.compat.mca.McaSkins.INSTANCE.active()
                    ? "found" : "MISSING") : ""));
            System.out.flush();
            Runtime.getRuntime().halt(0);
        }
    }
}
