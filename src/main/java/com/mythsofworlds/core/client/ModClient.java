package com.mythsofworlds.core.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.back.BackSlot;
import com.mythsofworlds.mythology.relic.DoubleJumpPayload;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.inventory.CreativeModeInventoryScreen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.entity.player.PlayerRenderer;
import net.minecraft.client.resources.PlayerSkin;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.phys.Vec3;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.ContainerScreenEvent;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.neoforged.neoforge.network.PacketDistributor;

/** Client side of the back slot and of the talaria's double jump. */
public final class ModClient {
    private ModClient() {
    }

    @EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
    public static final class ModBus {
        private ModBus() {
        }

        @SubscribeEvent
        public static void setup(FMLClientSetupEvent event) {
            // The creative inventory has no room for the back slot: hide it there.
            BackSlot.hidden = () -> Minecraft.getInstance().screen instanceof CreativeModeInventoryScreen;
        }

        @SubscribeEvent
        public static void addLayers(EntityRenderersEvent.AddLayers event) {
            for (PlayerSkin.Model skin : event.getSkins()) {
                if (event.getSkin(skin) instanceof PlayerRenderer renderer) {
                    renderer.addLayer(new BackLayer(renderer, event.getEntityModels()));
                }
            }
        }
    }

    @EventBusSubscriber(modid = MythsOfWorlds.MODID, value = Dist.CLIENT)
    public static final class GameBus {
        private static boolean wasJumping;
        private static boolean leapt;

        private GameBus() {
        }

        /** The frame of the back slot, drawn into the inventory next to the player. */
        @SubscribeEvent
        public static void drawSlot(ContainerScreenEvent.Render.Background event) {
            if (!(event.getContainerScreen() instanceof InventoryScreen screen)) {
                return;
            }
            GuiGraphics graphics = event.getGuiGraphics();
            int x = screen.getGuiLeft() + BackSlot.X - 1;
            int y = screen.getGuiTop() + BackSlot.Y - 1;
            graphics.fill(x, y, x + 18, y + 18, 0xFF8B8B8B);
            graphics.fill(x, y, x + 17, y + 1, 0xFF373737);
            graphics.fill(x, y, x + 1, y + 17, 0xFF373737);
            graphics.fill(x + 1, y + 17, x + 18, y + 18, 0xFFFFFFFF);
            graphics.fill(x + 17, y + 1, x + 18, y + 18, 0xFFFFFFFF);
        }

        /** The talaria of Hermes: press jump again in mid-air to leap once more. */
        @SubscribeEvent
        public static void onClientTick(ClientTickEvent.Post event) {
            LocalPlayer player = Minecraft.getInstance().player;
            if (player == null) {
                return;
            }
            boolean jumping = player.input != null && player.input.jumping;
            if (player.onGround() || player.isInWater() || player.onClimbable()) {
                leapt = false;
            } else if (jumping && !wasJumping && !leapt && DoubleJumpPayload.canDoubleJump(player)) {
                leapt = true;
                MobEffectInstance jump = player.getEffect(MobEffects.JUMP);
                double power = 0.42 + (jump == null ? 0.0 : 0.1 * (jump.getAmplifier() + 1));
                Vec3 motion = player.getDeltaMovement();
                Vec3 look = player.getLookAngle();
                player.setDeltaMovement(motion.x + look.x * 0.15, Math.max(motion.y, power), motion.z + look.z * 0.15);
                player.resetFallDistance();
                PacketDistributor.sendToServer(DoubleJumpPayload.INSTANCE);
            }
            wasJumping = jumping;
        }
    }
}
