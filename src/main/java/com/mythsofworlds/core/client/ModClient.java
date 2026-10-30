package com.mythsofworlds.core.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.relic.DoubleJumpPayload;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.renderer.entity.player.PlayerRenderer;
import net.minecraft.client.resources.PlayerSkin;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.phys.Vec3;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.neoforged.neoforge.network.PacketDistributor;

/** Client side of the back slot (drawing what is worn there) and of the talaria's double jump. */
public final class ModClient {
    private ModClient() {
    }

    @EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
    public static final class ModBus {
        private ModBus() {
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
