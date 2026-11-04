package com.mythsofworlds.core.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.codex.CodexBook;
import com.mythsofworlds.gametest.JoinTest;
import com.mythsofworlds.mythology.relic.MythAttributes;
import net.minecraft.client.CameraType;
import java.util.List;
import net.minecraft.client.Minecraft;
import net.minecraft.client.Screenshot;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.network.chat.Component;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemStack;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.network.PacketDistributor;
import top.theillusivec4.curios.client.gui.CuriosScreen;
import top.theillusivec4.curios.common.network.client.CPacketOpenCurios;
import vazkii.patchouli.api.PatchouliAPI;
import vazkii.patchouli.client.base.ClientAdvancements;

/**
 * The client half of the join test ({@code ./gradlew runJoinClient}, see {@link JoinTest}): joins the dedicated
 * server, waits for the milestone the server awards, checks that the armour powers arrived, then for each suit takes a
 * screenshot from the front and one in the middle of a swing in first person, opens the Codex, and leaves. Any
 * rendering error crashes the game, which fails the CI step; the screenshots are kept as a CI artifact.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, value = Dist.CLIENT)
public final class JoinTestClient {
    public static final String PROPERTY = "mythsofworlds.joinTestClient";
    private static final int GIVE_UP = 20 * 60 * 5;
    /** Ticks after the suits when the Codex sweep starts, and how long each of its screenshots takes. */
    private static final int CODEX_SWEEP = 100;
    private static final int SHOT_TICKS = 14;
    /** Pages of the Codex the sweep opens: the path, a large and a small creature of each world, a place, a god. */
    private static final List<String> CODEX_PAGES = List.of("hellas/path", "hellas/hydra", "hellas/satyr", "hellas/agora",
            "duat/apep", "duat/scorpion", "duat/isis", "jotunheim/path", "nav/path");

    private static int ticks;
    /** Client ticks since the milestone arrived, or -1 before. */
    private static int since = -1;
    /** The tick the client left the server, or -1. */
    private static int leftAt = -1;

    private JoinTestClient() {
    }

    private static void report(String line) {
        System.out.println("[join-test-client] " + line);
        System.out.flush();
    }

    private static void fail(String why) {
        report("FAIL: " + why);
        Runtime.getRuntime().halt(1);
    }

    private static void screenshot(Minecraft mc, String name) {
        Screenshot.grab(mc.gameDirectory, name + ".png", mc.getMainRenderTarget(), message -> report("screenshot " + name));
    }

    @SubscribeEvent
    public static void onTick(ClientTickEvent.Post event) {
        if (!Boolean.getBoolean(PROPERTY)) {
            return;
        }
        Minecraft mc = Minecraft.getInstance();
        ticks++;
        if (ticks > GIVE_UP) {
            fail("timed out " + (since < 0 ? "waiting for the milestone from the server" : "at step " + since));
        }
        if (leftAt >= 0) {
            if (ticks - leftAt > 20) {
                Runtime.getRuntime().halt(0);
            }
            return;
        }
        LocalPlayer player = mc.player;
        if (player == null) {
            return;
        }
        if (since < 0) {
            if (ClientAdvancements.hasDone(CodexBook.lock("milestone", "kill.minotaur").toString())) {
                report("milestone synced from the server");
                since = 0;
            }
            return;
        }
        since++;
        int stages = JoinTest.stages().size();
        // The server dresses the player at its own clock: stage k starts STAGE_TICKS * k after the milestone.
        int stage = since / JoinTest.STAGE_TICKS;
        int t = since % JoinTest.STAGE_TICKS;
        if (stage < stages) {
            if (stage == 0 && t == 15) {
                double reflection = player.getAttributeValue(MythAttributes.REFLECTION);
                if (reflection < 0.19) {
                    fail("the orichalcum armour's reflection did not reach the client: " + reflection);
                }
                report("armour powers synced: reflection " + reflection);
            }
            switch (t) {
                case 10 -> mc.options.setCameraType(CameraType.THIRD_PERSON_FRONT);
                case 30 -> screenshot(mc, "suit_" + stage + "_front");
                case 34 -> mc.options.setCameraType(CameraType.THIRD_PERSON_BACK);
                case 44 -> screenshot(mc, "suit_" + stage + "_back");
                case 48 -> mc.options.setCameraType(CameraType.FIRST_PERSON);
                case 60 -> player.swing(InteractionHand.MAIN_HAND);
                case 62 -> screenshot(mc, "suit_" + stage + "_swing");
                default -> {
                }
            }
            return;
        }
        int after = since - stages * JoinTest.STAGE_TICKS;
        switch (after) {
            case 5 -> PatchouliAPI.get().openBookEntry(CodexBook.ID, MythsOfWorlds.id("hellas/path"), 0);
            case 25 -> screenshot(mc, "codex_hellas");
            case 30 -> mc.setScreen(new InventoryScreen(player));
            case 45 -> screenshot(mc, "inventory");
            case 50 -> mc.setScreen(null);
            // The Curios screen (the back slot) is opened by the server, as its button does.
            case 55 -> PacketDistributor.sendToServer(new CPacketOpenCurios(ItemStack.EMPTY));
            case 75 -> {
                if (!(mc.screen instanceof CuriosScreen)) {
                    fail("the Curios screen did not open: " + mc.screen);
                }
                screenshot(mc, "curios");
            }
            case 80 -> {
                if (mc.player != null) {
                    mc.player.closeContainer();
                }
            }
            default -> {
                if (after >= CODEX_SWEEP) {
                    codexSweep(mc, after - CODEX_SWEEP);
                }
            }
        }
    }

    /**
     * Opens a few pages of the Codex (the path, text pages, large and small creatures) at every GUI scale from 1 to 4
     * and takes a screenshot of each, to check that the pictures stay in their frames and the text in its place; then
     * leaves the server.
     */
    private static void codexSweep(Minecraft mc, int tick) {
        int shot = tick / SHOT_TICKS;
        int t = tick % SHOT_TICKS;
        if (shot < CODEX_PAGES.size() * 4) {
            String entry = CODEX_PAGES.get(shot / 4);
            int scale = shot % 4 + 1;
            if (t == 0) {
                mc.options.guiScale().set(scale);
                mc.resizeDisplay();
                PatchouliAPI.get().openBookEntry(CodexBook.ID, MythsOfWorlds.id(entry), 0);
            } else if (t == SHOT_TICKS - 2) {
                screenshot(mc, "codex_" + entry.replace('/', '_') + "_gui" + scale);
            }
            return;
        }
        if (t == 0 && shot == CODEX_PAGES.size() * 4) {
            mc.options.guiScale().set(2);
            mc.resizeDisplay();
            mc.setScreen(null);
            report("OK: joined, synced, every suit and swing drawn, the Codex at every GUI scale, the inventory and the "
                    + "Curios screen opened");
            leftAt = ticks;
            if (mc.getConnection() != null) {
                mc.getConnection().getConnection().disconnect(Component.literal("done"));
            }
        }
    }
}
