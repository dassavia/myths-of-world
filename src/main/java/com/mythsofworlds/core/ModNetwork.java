package com.mythsofworlds.core;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.relic.DoubleJumpPayload;
import com.mythsofworlds.mythology.relic.HeimdallVision;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.network.event.RegisterPayloadHandlersEvent;
import net.neoforged.neoforge.network.registration.PayloadRegistrar;

/** The mod's own packets: the double jump of the talaria, the switch of the vision of Heimdall. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD)
public final class ModNetwork {
    private ModNetwork() {
    }

    @SubscribeEvent
    public static void register(RegisterPayloadHandlersEvent event) {
        PayloadRegistrar registrar = event.registrar("4");
        registrar.playToServer(DoubleJumpPayload.TYPE, DoubleJumpPayload.STREAM_CODEC, DoubleJumpPayload::handle);
        registrar.playToServer(HeimdallVision.Payload.TYPE, HeimdallVision.Payload.STREAM_CODEC, HeimdallVision.Payload::handle);
    }
}
