package com.mythsofworlds.mythology.relic;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.core.ServerConfig;
import io.netty.buffer.ByteBuf;
import net.minecraft.network.chat.Component;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.handling.IPayloadContext;

/**
 * The vision of the helmet of Heimdall ({@link Relics#heimdall}) can be switched off and on again: by each player with
 * a key (client: {@code HeimdallVisionClient}, kept in their client config) and for the whole server in
 * {@link ServerConfig#HEIMDALL_VISION}. The player's choice is kept on the server ({@link PlayerData#HEIMDALL_VISION}),
 * so it survives death and relogging; it is on by default, as before. While it is off the helmet does nothing at all:
 * no night vision, no glowing creatures, and so no extra packets.
 */
public final class HeimdallVision {
    private HeimdallVision() {
    }

    /** Whether the helmet's vision works for this player now. */
    public static boolean on(Player player) {
        return ServerConfig.HEIMDALL_VISION.get() && player.getData(PlayerData.HEIMDALL_VISION);
    }

    /** Switches the player's vision; when it goes off, its night vision and the glow it gave go at once. */
    public static void set(ServerPlayer player, boolean enabled, boolean tell) {
        boolean was = on(player);
        player.setData(PlayerData.HEIMDALL_VISION, enabled);
        if (was && !on(player)) {
            clear(player);
        }
        if (tell) {
            String key = !ServerConfig.HEIMDALL_VISION.get() ? "disabled" : enabled ? "on" : "off";
            player.displayClientMessage(Component.translatable("hud.mythsofworlds.heimdall_vision." + key), true);
        }
    }

    /** Takes away the night vision the helmet keeps up and the glow it put on the creatures around. */
    public static void clear(Player player) {
        MobEffectInstance night = player.getEffect(MobEffects.NIGHT_VISION);
        if (night != null && night.isAmbient() && !night.isInfiniteDuration()) {
            player.removeEffect(MobEffects.NIGHT_VISION);
        }
        for (Mob mob : player.level().getEntitiesOfClass(Mob.class, player.getBoundingBox().inflate(Relics.HEIMDALL_RANGE))) {
            MobEffectInstance glow = mob.getEffect(MobEffects.GLOWING);
            if (glow != null && glow.isAmbient() && glow.getDuration() <= Relics.HEIMDALL_GLOW_TICKS) {
                mob.removeEffect(MobEffects.GLOWING);
            }
        }
    }

    /**
     * Client to server: the player's choice, sent when they press the key, when they join and when they change it in
     * the settings. {@code tell}: answer with a message over the hotbar.
     */
    public record Payload(boolean enabled, boolean tell) implements CustomPacketPayload {
        public static final Type<Payload> TYPE = new Type<>(MythsOfWorlds.id("heimdall_vision"));
        public static final StreamCodec<ByteBuf, Payload> STREAM_CODEC = StreamCodec.composite(ByteBufCodecs.BOOL, Payload::enabled,
                ByteBufCodecs.BOOL, Payload::tell, Payload::new);

        @Override
        public Type<Payload> type() {
            return TYPE;
        }

        public static void handle(Payload payload, IPayloadContext context) {
            context.enqueueWork(() -> {
                if (context.player() instanceof ServerPlayer player) {
                    set(player, payload.enabled(), payload.tell());
                }
            });
        }
    }
}
