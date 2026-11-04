package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.codex.CodexBook;
import com.mythsofworlds.codex.CodexContent;
import com.mythsofworlds.codex.Progress;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.norse.NorseEntities;
import com.mythsofworlds.mythology.relic.MythAttributes;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.registry.MetalSet;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.GameRules;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

/**
 * The server half of the join test ({@code ./gradlew runJoinServer} with {@code runJoinClient}, used by CI): a real
 * dedicated server that a real client joins over the network. The server gives the player the Codex, awards a
 * milestone and dresses them in each suit of the myths in turn, checking that the Codex was handed out and that the
 * armour powers reach the player; the client (JoinTestClient) checks that the milestone and the powers arrived,
 * draws the armour, the swings, the HUD and the Codex, and takes a screenshot of each. When the client leaves, the
 * server exits with 0 if everything held, else 1. Does nothing unless the system property {@value #PROPERTY} is set.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class JoinTest {
    public static final String PROPERTY = "mythsofworlds.joinTest";
    /** Ticks each suit is worn; the client times its screenshots by the same clock. */
    public static final int STAGE_TICKS = 80;
    /** Ticks after joining when the first suit is put on and the milestone awarded. */
    public static final int FIRST_STAGE = 20;
    private static final int GIVE_UP = 20 * 60 * 6;

    private static final List<String> failures = new ArrayList<>();
    private static ServerPlayer player;
    private static int ticks;
    private static int joinedAt = -1;
    private static boolean checkedCodex;

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
        MetalSet meteoric = com.mythsofworlds.mythology.egyptian.EgyptianContent.METEORIC_IRON;
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
                        GreekContent.NEMEAN_BOOTS.get(), SlavicContent.KLADENETS.get()),
                List.of(meteoric.helmet.get(), meteoric.chestplate.get(), meteoric.leggings.get(), meteoric.boots.get(),
                        meteoric.sword.get()),
                List.of(com.mythsofworlds.mythology.egyptian.EgyptianContent.NEMES.get(),
                        com.mythsofworlds.mythology.egyptian.EgyptianContent.PECTORAL_OF_RA.get(), meteoric.leggings.get(),
                        meteoric.boots.get(), com.mythsofworlds.mythology.egyptian.EgyptianContent.KHOPESH.get()));
    }

    /**
     * A priestess, an amazon, a valkyrie and Isis stand still in front of the player, for the client to draw (with
     * MCA's looks when CI runs with MCA Reborn) and photograph.
     */
    private static void heroines(ServerPlayer player) {
        var level = player.serverLevel();
        Vec3 ahead = player.getLookAngle().multiply(1.0, 0.0, 1.0).normalize();
        Vec3 side = new Vec3(-ahead.z, 0.0, ahead.x);
        List<EntityType<? extends Mob>> types = List.of(EgyptianEntities.PRIESTESS.get(), GreekEntities.AMAZON.get(),
                NorseEntities.VALKYRIE.get(), EgyptianEntities.ISIS.get());
        for (int i = 0; i < types.size(); i++) {
            Mob mob = types.get(i).create(level);
            if (mob == null) {
                failures.add("could not create " + types.get(i));
                continue;
            }
            Vec3 at = player.position().add(ahead.scale(4.0)).add(side.scale((i - 1.5) * 1.3));
            mob.moveTo(at.x, player.getY(), at.z, player.getYRot() + 180.0F, 0.0F);
            mob.finalizeSpawn(level, level.getCurrentDifficultyAt(mob.blockPosition()), MobSpawnType.COMMAND, null);
            mob.setNoAi(true);
            mob.setYHeadRot(player.getYRot() + 180.0F);
            level.addFreshEntity(mob);
        }
        report("heroines spawned in front of the player");
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
            // Every page of the Codex open, so the client can draw any of them.
            CodexBook.sync(player, true);
        }
        List<List<Item>> stages = stages();
        int stage = (t - FIRST_STAGE) / STAGE_TICKS;
        if (t >= FIRST_STAGE && (t - FIRST_STAGE) % STAGE_TICKS == 0 && stage < stages.size()) {
            dress(player, stages.get(stage));
            report("stage " + stage + ": " + stages.get(stage).get(0));
        }
        if (t == FIRST_STAGE + STAGE_TICKS * stages.size() + 40) {
            heroines(player);
        }
        if (t == FIRST_STAGE + 10 && player.getAttributeValue(MythAttributes.REFLECTION) < 0.19) {
            failures.add("orichalcum armour gives reflection " + player.getAttributeValue(MythAttributes.REFLECTION));
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
        if (ticks - joinedAt < FIRST_STAGE + STAGE_TICKS * stages().size()) {
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
