package com.mythsofworlds.codex;

import com.mythsofworlds.MythsOfWorlds;
import java.util.List;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.neoforged.neoforge.network.handling.IPayloadContext;

/** Server to client: the journal entries and milestones of the player, which the Codex screen shows. */
public record CodexSyncPayload(List<String> entries, List<String> milestones) implements CustomPacketPayload {
    public static final Type<CodexSyncPayload> TYPE = new Type<>(MythsOfWorlds.id("codex_sync"));
    public static final StreamCodec<RegistryFriendlyByteBuf, CodexSyncPayload> STREAM_CODEC = StreamCodec.composite(
            ByteBufCodecs.STRING_UTF8.apply(ByteBufCodecs.list()), CodexSyncPayload::entries,
            ByteBufCodecs.STRING_UTF8.apply(ByteBufCodecs.list()), CodexSyncPayload::milestones,
            CodexSyncPayload::new);

    @Override
    public Type<CodexSyncPayload> type() {
        return TYPE;
    }

    public static void handle(CodexSyncPayload payload, IPayloadContext context) {
        context.enqueueWork(() -> CodexState.set(payload.entries(), payload.milestones()));
    }
}
