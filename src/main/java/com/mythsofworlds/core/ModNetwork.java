package com.mythsofworlds.core;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.codex.CodexSyncPayload;
import com.mythsofworlds.core.back.BackPayload;
import com.mythsofworlds.mythology.relic.DoubleJumpPayload;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

/** The mod's own packets: what a player carries on the back, the progress shown in the Codex, and the double jump of
 * the talaria. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD)
public final class ModNetwork {
    private ModNetwork() {
    }

    @SubscribeEvent
    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar("2");
        registrar.playToClient(BackPayload.TYPE, BackPayload.STREAM_CODEC, BackPayload::handle);
        registrar.playToClient(CodexSyncPayload.TYPE, CodexSyncPayload.STREAM_CODEC, CodexSyncPayload::handle);
        registrar.playToServer(DoubleJumpPayload.TYPE, DoubleJumpPayload.STREAM_CODEC, DoubleJumpPayload::handle);
    }
}
