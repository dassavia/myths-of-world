package com.mythsofworlds.core.back;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.network.handling.IPayloadContext;

/** Server to client: what a player carries on the back (see {@link BackSlot}), so it can be drawn. */
public record BackPayload(int entityId, ItemStack stack) implements CustomPacketPayload {
    public static final Type<BackPayload> TYPE = new Type<>(MythsOfWorlds.id("back"));
    public static final StreamCodec<RegistryFriendlyByteBuf, BackPayload> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.VAR_INT, BackPayload::entityId,
            ItemStack.OPTIONAL_STREAM_CODEC, BackPayload::stack,
            BackPayload::new);

    @Override
    public Type<BackPayload> type() {
        return TYPE;
    }

    public static void handle(BackPayload payload, IPayloadContext context) {
        context.enqueueWork(() -> {
            Entity entity = context.player().level().getEntity(payload.entityId());
            if (entity instanceof Player player) {
                BackSlot.set(player, payload.stack());
            }
        });
    }
}
