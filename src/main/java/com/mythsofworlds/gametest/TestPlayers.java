package com.mythsofworlds.gametest;

import com.mojang.authlib.GameProfile;
import io.netty.channel.embedded.EmbeddedChannel;
import java.util.UUID;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.network.Connection;
import net.minecraft.network.protocol.PacketFlow;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.server.network.CommonListenerCookie;
import net.minecraft.server.network.ServerGamePacketListenerImpl;

/** Players for the game tests that need a real {@link ServerPlayer} (teleports, milestones, the Codex). */
final class TestPlayers {
    private TestPlayers() {
    }

    /**
     * A server player in the test's level with a mock connection that never joins the server: joining would send it
     * the packets of Curios, which a mock connection cannot carry. It is not in the level's player list.
     */
    static ServerPlayer serverPlayer(GameTestHelper helper, String name) {
        CommonListenerCookie cookie = CommonListenerCookie.createInitial(new GameProfile(UUID.randomUUID(), name), false);
        ServerPlayer player = new ServerPlayer(helper.getLevel().getServer(), helper.getLevel(), cookie.gameProfile(),
                cookie.clientInformation());
        Connection connection = new Connection(PacketFlow.SERVERBOUND);
        new EmbeddedChannel(connection);
        new ServerGamePacketListenerImpl(helper.getLevel().getServer(), connection, player, cookie);
        return player;
    }
}
