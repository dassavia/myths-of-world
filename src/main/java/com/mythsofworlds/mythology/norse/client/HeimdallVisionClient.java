package com.mythsofworlds.mythology.norse.client;

import com.mojang.blaze3d.platform.InputConstants;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.ClientConfig;
import com.mythsofworlds.mythology.relic.HeimdallVision;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.config.ModConfigEvent;
import net.neoforged.neoforge.client.event.ClientPlayerNetworkEvent;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.network.PacketDistributor;
import org.lwjgl.glfw.GLFW;

/**
 * The key that switches the vision of the helmet of Heimdall off and on again (N by default, in Controls under Myths
 * of Worlds), and the client setting it is kept in ({@link ClientConfig#HEIMDALL_VISION}). The choice goes to the
 * server ({@link HeimdallVision.Payload}) when the key is pressed, on joining and when the setting is changed; the
 * server answers over the hotbar.
 */
public final class HeimdallVisionClient {
    public static final KeyMapping TOGGLE = new KeyMapping("key.mythsofworlds.heimdall_vision", InputConstants.Type.KEYSYM,
            GLFW.GLFW_KEY_N, "key.categories.mythsofworlds");

    private HeimdallVisionClient() {
    }

    private static void send(boolean tell) {
        if (Minecraft.getInstance().getConnection() != null) {
            PacketDistributor.sendToServer(new HeimdallVision.Payload(ClientConfig.HEIMDALL_VISION.get(), tell));
        }
    }

    @EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
    public static final class ModBus {
        private ModBus() {
        }

        @SubscribeEvent
        public static void registerKeys(RegisterKeyMappingsEvent event) {
            event.register(TOGGLE);
        }

        /** Changing the setting in the config screen (or the file) takes effect in the running game. */
        @SubscribeEvent
        public static void configChanged(ModConfigEvent.Reloading event) {
            if (event.getConfig().getSpec() == ClientConfig.SPEC) {
                send(false);
            }
        }
    }

    @EventBusSubscriber(modid = MythsOfWorlds.MODID, value = Dist.CLIENT)
    public static final class GameBus {
        private GameBus() {
        }

        @SubscribeEvent
        public static void onTick(ClientTickEvent.Post event) {
            while (TOGGLE.consumeClick()) {
                ClientConfig.HEIMDALL_VISION.set(!ClientConfig.HEIMDALL_VISION.get());
                ClientConfig.HEIMDALL_VISION.save();
                send(true);
            }
        }

        @SubscribeEvent
        public static void joined(ClientPlayerNetworkEvent.LoggingIn event) {
            send(false);
        }
    }
}
