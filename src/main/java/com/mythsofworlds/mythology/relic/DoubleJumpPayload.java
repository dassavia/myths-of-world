package com.mythsofworlds.mythology.relic;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.GreekContent;
import io.netty.buffer.ByteBuf;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.neoforged.neoforge.network.handling.IPayloadContext;

/**
 * Client to server: the player wearing the talaria leapt again in mid-air (the client moves itself, see
 * {@code RelicClient}); the server adds the puff of wind and the sound for everyone around.
 */
public record DoubleJumpPayload() implements CustomPacketPayload {
    public static final DoubleJumpPayload INSTANCE = new DoubleJumpPayload();
    public static final Type<DoubleJumpPayload> TYPE = new Type<>(MythsOfWorlds.id("double_jump"));
    public static final StreamCodec<ByteBuf, DoubleJumpPayload> STREAM_CODEC = StreamCodec.unit(INSTANCE);

    @Override
    public Type<DoubleJumpPayload> type() {
        return TYPE;
    }

    /** Whether {@code player} may leap again in the air: the talaria are on and nothing else holds them up. */
    public static boolean canDoubleJump(Player player) {
        return player.getItemBySlot(EquipmentSlot.FEET).is(GreekContent.TALARIA.get()) && !player.onGround()
                && !player.isFallFlying() && !player.getAbilities().flying && !player.isInWater() && !player.isPassenger()
                && !player.onClimbable();
    }

    public static void handle(DoubleJumpPayload payload, IPayloadContext context) {
        context.enqueueWork(() -> {
            Player player = context.player();
            if (!player.getItemBySlot(EquipmentSlot.FEET).is(GreekContent.TALARIA.get())) {
                return;
            }
            player.resetFallDistance();
            if (player.level() instanceof ServerLevel level) {
                level.sendParticles(ParticleTypes.CLOUD, player.getX(), player.getY(), player.getZ(), 8, 0.3, 0.05, 0.3, 0.02);
                level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.PHANTOM_FLAP, SoundSource.PLAYERS,
                        0.6F, 1.6F);
            }
        });
    }
}
