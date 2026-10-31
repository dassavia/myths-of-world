package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.codex.CodexContent;
import com.mythsofworlds.codex.Progress;
import com.mythsofworlds.core.entity.MythBoss;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.norse.NorseEntities;
import com.mythsofworlds.mythology.relic.MythAttributes;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.mythology.slavic.SlavicEntities;
import com.mythsofworlds.registry.MetalSet;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.GameRules;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

/**
 * The server half of the join test ({@code ./gradlew runJoinServer} with {@code runJoinClient}, used by CI): a real
 * dedicated server that a real client joins over the network. The server gives the player the Codex, awards a
 * milestone and dresses them in each suit of the myths in turn, checking that the Codex was handed out and that the
 * armour powers reach the player; then it shows each boss drawn with GeckoLib in turn and has it play its special
 * animation. The client (JoinTestClient) checks that the milestone and the powers arrived, draws the armour, the
 * swings, the bosses, the HUD and the Codex, and takes a screenshot of each. When the client leaves, the
 * server exits with 0 if everything held, else 1. Does nothing unless the system property {@value #PROPERTY} is set.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class JoinTest {
    public static final String PROPERTY = "mythsofworlds.joinTest";
    /** Ticks each suit is worn; the client times its screenshots by the same clock. */
    public static final int STAGE_TICKS = 80;
    /** Ticks each boss of the gallery stands before the player; the client times its screenshots by the same clock. */
    public static final int BOSS_TICKS = 60;
    /** Ticks after a boss appears when it plays its special animation (sent to the client by GeckoLib). */
    public static final int BOSS_SPECIAL = 22;
    /** Ticks after joining when the first suit is put on and the milestone awarded. */
    public static final int FIRST_STAGE = 20;
    private static final int GIVE_UP = 20 * 60 * 6;

    private static final List<String> failures = new ArrayList<>();
    private static ServerPlayer player;
    private static int ticks;
    private static int joinedAt = -1;
    private static boolean checkedCodex;
    private static MythBoss shown;

    private JoinTest() {
    }

    private static boolean active() {
        return Boolean.getBoolean(PROPERTY);
    }

    private static void report(String line) {
        System.out.println("[join-test] " + line);
        System.out.flush();
    }

    /** The suits worn in turn: head, chest, legs, feet and the weapon in hand. */
    public static List<List<Item>> stages() {
        MetalSet ori = GreekContent.ORICHALCUM;
        MetalSet bulat = SlavicContent.BULAT;
        MetalSet dark = NorseContent.DARK_IRON;
        return List.of(
                List.of(ori.helmet.get(), ori.chestplate.get(), ori.leggings.get(), ori.boots.get(), ori.sword.get()),
                List.of(bulat.helmet.get(), bulat.chestplate.get(), bulat.leggings.get(), bulat.boots.get(), bulat.axe.get()),
                List.of(dark.helmet.get(), dark.chestplate.get(), dark.leggings.get(), dark.boots.get(),
                        NorseContent.MJOLNIR.get()),
                List.of(NorseContent.HEIMDALL_HELMET.get(), GreekContent.TITAN_BREASTPLATE.get(),
                        GreekContent.NEMEAN_LEGGINGS.get(), GreekContent.TALARIA.get(), NorseContent.SURTR_SWORD.get()),
                List.of(GreekContent.NEMEAN_HELMET.get(), GreekContent.NEMEAN_CHESTPLATE.get(), bulat.leggings.get(),
                        SlavicContent.SKOROKHODY.get(), GreekContent.BIDENT_OF_HADES.get()),
                List.of(SlavicContent.SHAPKA_NEVIDIMKA.get(), dark.chestplate.get(), dark.leggings.get(),
                        GreekContent.NEMEAN_BOOTS.get(), SlavicContent.KLADENETS.get()));
    }

    /** The bosses drawn with GeckoLib, shown to the client one after another after the suits. */
    public static List<Supplier<? extends EntityType<? extends MythBoss>>> gallery() {
        return List.of(GreekEntities.MINOTAUR, GreekEntities.HYDRA, GreekEntities.CERBERUS, GreekEntities.MEDUSA,
                GreekEntities.CYCLOPS, GreekEntities.NEMEAN_LION, SlavicEntities.KOSCHEI, SlavicEntities.SOLOVEI, SlavicEntities.ZMEY_GORYNYCH, NorseEntities.HEIMDALL,
                NorseEntities.DRAUGR_CHIEFTAIN, NorseEntities.THRYM, NorseEntities.SURTR, NorseEntities.FENRIR, NorseEntities.GARM);
    }

    /** The boss stands far enough north of the player, facing them, to be seen whole. */
    private static MythBoss showBoss(ServerPlayer player, EntityType<? extends MythBoss> type) {
        MythBoss boss = type.create(player.serverLevel());
        if (boss == null) {
            failures.add("could not create " + type);
            return null;
        }
        double distance = 3.0 + boss.getBbHeight() * 1.4 + boss.getBbWidth();
        boss.moveTo(player.getX(), player.getY(), player.getZ() - distance, 0.0F, 0.0F);
        boss.setYHeadRot(0.0F);
        boss.setYBodyRot(0.0F);
        boss.setNoAi(true);
        boss.setPersistenceRequired();
        player.serverLevel().addFreshEntity(boss);
        return boss;
    }

    private static void dress(ServerPlayer player, List<Item> suit) {
        EquipmentSlot[] slots = {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET,
                EquipmentSlot.MAINHAND};
        for (int i = 0; i < slots.length; i++) {
            player.setItemSlot(slots[i], new ItemStack(suit.get(i)));
        }
    }

    @SubscribeEvent
    public static void onLogin(PlayerEvent.PlayerLoggedInEvent event) {
        if (active() && event.getEntity() instanceof ServerPlayer joined && player == null) {
            player = joined;
            joinedAt = ticks;
            report("player joined: " + joined.getGameProfile().getName());
            joined.serverLevel().setDayTime(6000);
            joined.serverLevel().getGameRules().getRule(GameRules.RULE_DAYLIGHT).set(false, joined.server);
            joined.serverLevel().getGameRules().getRule(GameRules.RULE_DOMOBSPAWNING).set(false, joined.server);
        }
    }

    @SubscribeEvent
    public static void onTick(ServerTickEvent.Post event) {
        if (!active()) {
            return;
        }
        ticks++;
        if (player == null) {
            if (ticks > GIVE_UP) {
                report("FAIL: no player joined");
                Runtime.getRuntime().halt(1);
            }
            return;
        }
        int t = ticks - joinedAt;
        if (t == FIRST_STAGE - 5 && !checkedCodex) {
            checkedCodex = true;
            if (!player.getInventory().contains(new ItemStack(CodexContent.CODEX.get()))) {
                failures.add("the Codex was not given on first login");
            }
        }
        if (t == FIRST_STAGE) {
            Progress.award(player, "kill.minotaur");
        }
        List<List<Item>> stages = stages();
        int stage = (t - FIRST_STAGE) / STAGE_TICKS;
        if (t >= FIRST_STAGE && (t - FIRST_STAGE) % STAGE_TICKS == 0 && stage < stages.size()) {
            dress(player, stages.get(stage));
            report("stage " + stage + ": " + stages.get(stage).get(0));
        }
        if (t == FIRST_STAGE + 10 && player.getAttributeValue(MythAttributes.REFLECTION) < 0.19) {
            failures.add("orichalcum armour gives reflection " + player.getAttributeValue(MythAttributes.REFLECTION));
        }
        int galleryStart = FIRST_STAGE + STAGE_TICKS * stages.size();
        if (t >= galleryStart) {
            int index = (t - galleryStart) / BOSS_TICKS;
            int at = (t - galleryStart) % BOSS_TICKS;
            var gallery = gallery();
            if (index < gallery.size()) {
                if (index == 0 && at == 0) {
                    player.setItemSlot(EquipmentSlot.HEAD, ItemStack.EMPTY);
                    player.teleportTo(player.serverLevel(), player.getX(), player.getY(), player.getZ(), 180.0F, 0.0F);
                }
                if (at == 0) {
                    shown = showBoss(player, gallery.get(index).get());
                    report("boss " + index + ": " + gallery.get(index).get());
                } else if (at == BOSS_SPECIAL && shown != null) {
                    shown.triggerAnim("action", "special");
                } else if (at == BOSS_TICKS - 2 && shown != null) {
                    shown.discard();
                    shown = null;
                }
            }
        }
        if (t > GIVE_UP) {
            report("FAIL: the client did not finish");
            Runtime.getRuntime().halt(1);
        }
    }

    @SubscribeEvent
    public static void onLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        if (!active() || event.getEntity() != player) {
            return;
        }
        if (ticks - joinedAt < FIRST_STAGE + STAGE_TICKS * stages().size() + BOSS_TICKS * gallery().size()) {
            failures.add("the client left early, after " + (ticks - joinedAt) + " ticks");
        }
        if (failures.isEmpty()) {
            report("OK: the client joined, got the Codex, the milestone and every suit");
            Runtime.getRuntime().halt(0);
        }
        failures.forEach(failure -> report("FAIL: " + failure));
        Runtime.getRuntime().halt(1);
    }
}
