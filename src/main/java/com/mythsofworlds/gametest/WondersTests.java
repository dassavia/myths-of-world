package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.Prophecy;
import com.mythsofworlds.core.family.WarriorMaiden;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.norse.NorseEntities;
import com.mythsofworlds.mythology.norse.ValkyrieRescue;
import com.mythsofworlds.mythology.norse.entity.Valkyrie;
import com.mythsofworlds.mythology.norse.item.DraupnirItem;
import com.mythsofworlds.mythology.norse.item.GungnirItem;
import com.mythsofworlds.mythology.norse.item.RuneItem;
import com.mythsofworlds.mythology.greek.Offerings;
import com.mythsofworlds.mythology.greek.item.AriadneThreadItem;
import com.mythsofworlds.mythology.greek.item.DelphicLaurelItem;
import com.mythsofworlds.core.StackData;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.mythology.slavic.SlavicEntities;
import com.mythsofworlds.mythology.slavic.entity.Koschei;
import com.mythsofworlds.mythology.slavic.item.FernFlowerItem;
import com.mythsofworlds.mythology.slavic.item.GusliItem;
import com.mythsofworlds.mythology.slavic.item.SamobrankaItem;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** The wonders of the three worlds: relics and rites drawn from the myths. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class WondersTests {
    // ---------------------------------------------------------------- Hellas

    /** Ariadne's thread brings its holder back to where its end was tied, and wears a little. */
    @GameTest(template = "empty")
    public static void ariadneThreadLeadsBack(GameTestHelper helper) {
        ServerPlayer player = TestPlayers.serverPlayer(helper, "theseus");
        BlockPos knot = helper.absolutePos(new BlockPos(1, 2, 1));
        ItemStack thread = new ItemStack(GreekContent.ARIADNE_THREAD.get());
        player.setItemInHand(InteractionHand.MAIN_HAND, thread);
        AriadneThreadItem.tie(thread, knot, helper.getLevel());
        player.teleportTo(knot.getX() + 40.5, knot.getY() + 10, knot.getZ() + 0.5);
        AriadneThreadItem.follow(player, thread, InteractionHand.MAIN_HAND);
        helper.assertTrue(player.blockPosition().equals(knot), "the thread should lead back to " + knot + ", got " + player.blockPosition());
        helper.assertTrue(thread.getDamageValue() == 1, "each return wears the thread");
        helper.succeed();
    }

    /** A gift on a lit brazier blesses the giver; the gods hear one gift at a time. */
    @GameTest(template = "empty")
    public static void offeringsBlessTheGiver(GameTestHelper helper) {
        ServerPlayer player = TestPlayers.serverPlayer(helper, "pious");
        BlockPos brazier = helper.absolutePos(new BlockPos(1, 2, 1));
        ItemStack gold = new ItemStack(Items.GOLD_INGOT, 2);
        var zeus = Offerings.godOf(gold);
        helper.assertTrue(zeus.isPresent() && zeus.get().id().equals("zeus"), "gold is a gift for Zeus");
        helper.assertTrue(Offerings.godOf(new ItemStack(Items.DIRT)).isEmpty(), "dirt pleases no god");
        helper.assertTrue(Offerings.offer(helper.getLevel(), brazier, player, gold, zeus.get()), "Zeus should accept the gold");
        helper.assertTrue(player.hasEffect(MobEffects.DAMAGE_BOOST) && gold.getCount() == 1, "Zeus gives strength and takes one ingot");
        helper.assertTrue(!Offerings.offer(helper.getLevel(), brazier, player, gold, zeus.get()) && gold.getCount() == 1,
                "a second gift right away is not heard and not used up");
        helper.succeed();
    }

    /** Outside the worlds of the myths the Pythia is silent; the compass of the prophecy points the right way. */
    @GameTest(template = "empty")
    public static void prophecyKnowsItsWorld(GameTestHelper helper) {
        ServerPlayer player = TestPlayers.serverPlayer(helper, "seeker");
        helper.assertTrue(Prophecy.nextLair(player).isEmpty() && DelphicLaurelItem.prophesy(player).isEmpty(),
                "no lairs to foretell in the overworld");
        BlockPos o = BlockPos.ZERO;
        helper.assertTrue(Prophecy.direction(o, new BlockPos(0, 0, -100)).equals("n"), "-z is north");
        helper.assertTrue(Prophecy.direction(o, new BlockPos(100, 0, 0)).equals("e"), "+x is east");
        helper.assertTrue(Prophecy.direction(o, new BlockPos(-70, 0, 70)).equals("sw"), "-x +z is south-west");
        helper.assertTrue(Prophecy.distance(o, new BlockPos(30, 64, 40)) == 50, "distance is horizontal");
        helper.succeed();
    }

    // ---------------------------------------------------------------- Nav

    /** The fern flower finds the ore and the chest buried around it. */
    @GameTest(template = "empty")
    public static void fernFlowerRevealsTreasure(GameTestHelper helper) {
        ServerLevel level = helper.getLevel();
        BlockPos centre = helper.absolutePos(new BlockPos(1, 2, 1));
        int before = FernFlowerItem.revealTreasure(level, centre);
        level.setBlock(centre.offset(3, -1, 2), Blocks.GOLD_ORE.defaultBlockState(), Block.UPDATE_ALL);
        level.setBlock(centre.offset(-2, 0, 1), Blocks.CHEST.defaultBlockState(), Block.UPDATE_ALL);
        int after = FernFlowerItem.revealTreasure(level, centre);
        helper.assertTrue(after == before + 2, "the ore and the chest should be found: " + before + " then " + after);
        level.setBlock(centre.offset(3, -1, 2), Blocks.AIR.defaultBlockState(), Block.UPDATE_ALL);
        level.setBlock(centre.offset(-2, 0, 1), Blocks.AIR.defaultBlockState(), Block.UPDATE_ALL);
        helper.succeed();
    }

    /** The tablecloth lays a feast, then rests until the next day. */
    @GameTest(template = "empty")
    public static void samobrankaFeastsOnceADay(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        ItemStack cloth = new ItemStack(SlavicContent.SAMOBRANKA.get());
        helper.assertTrue(SamobrankaItem.feast(helper.getLevel(), player, cloth), "the first feast is laid");
        helper.assertTrue(player.getInventory().contains(new ItemStack(SlavicContent.KARAVAI.get())), "a karavai is on the cloth");
        helper.assertTrue(!SamobrankaItem.feast(helper.getLevel(), player, cloth), "a second feast the same day is not");
        StackData.putLong(cloth, SamobrankaItem.LAST_FEAST, helper.getLevel().getGameTime() - SamobrankaItem.DAY);
        helper.assertTrue(SamobrankaItem.feast(helper.getLevel(), player, cloth), "a day later it feasts again");
        helper.succeed();
    }

    /** The gusli set a monster dancing: it forgets its prey; a boss does not hear them. */
    @GameTest(template = "empty")
    public static void gusliSetMonstersDancing(GameTestHelper helper) {
        ServerPlayer player = TestPlayers.serverPlayer(helper, "sadko");
        player.moveTo(helper.absoluteVec(new Vec3(1.5, 2, 1.5)));
        Zombie zombie = helper.spawn(EntityType.ZOMBIE, new BlockPos(3, 2, 3));
        Koschei koschei = helper.spawn(SlavicEntities.KOSCHEI.get(), new BlockPos(1, 2, 4));
        zombie.setTarget(player);
        helper.assertTrue(GusliItem.play(helper.getLevel(), player) == 1, "only the zombie dances");
        helper.assertTrue(zombie.hasEffect(SlavicContent.DANCE) && !koschei.hasEffect(SlavicContent.DANCE), "the zombie dances, Koschei does not");
        helper.runAfterDelay(2, () -> {
            helper.assertTrue(zombie.getTarget() == null, "a dancing zombie forgets its prey");
            zombie.discard();
            koschei.discard();
            helper.succeed();
        });
    }

    // ---------------------------------------------------------------- Jotunheim

    /** Each rune gives its power; Thurisaz pricks whoever strikes its bearer. */
    @GameTest(template = "empty")
    public static void runesGiveTheirPower(GameTestHelper helper) {
        ServerLevel level = helper.getLevel();
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        RuneItem.speak(level, player, RuneItem.Rune.FEHU);
        RuneItem.speak(level, player, RuneItem.Rune.ALGIZ);
        helper.assertTrue(player.hasEffect(MobEffects.LUCK) && player.hasEffect(MobEffects.DAMAGE_RESISTANCE), "Fehu and Algiz");
        Zombie bearer = helper.spawn(EntityType.ZOMBIE, new BlockPos(1, 2, 1));
        Zombie attacker = helper.spawn(EntityType.ZOMBIE, new BlockPos(2, 2, 1));
        bearer.addEffect(new net.minecraft.world.effect.MobEffectInstance(NorseContent.THURISAZ, 200, 0));
        bearer.hurt(level.damageSources().mobAttack(attacker), 2.0F);
        helper.assertTrue(attacker.getHealth() < attacker.getMaxHealth(), "Thurisaz pricks the attacker");
        bearer.discard();
        attacker.discard();
        helper.succeed();
    }

    /** Draupnir starts counting when it comes to you, and drips eight nuggets a day. */
    @GameTest(template = "empty")
    public static void draupnirDripsGold(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        ItemStack ring = new ItemStack(NorseContent.DRAUPNIR.get());
        helper.assertTrue(DraupnirItem.drip(helper.getLevel(), player, ring) == 0, "nothing drips at once");
        StackData.putLong(ring, DraupnirItem.LAST_DRIP, helper.getLevel().getGameTime() - DraupnirItem.PERIOD);
        helper.assertTrue(DraupnirItem.drip(helper.getLevel(), player, ring) == DraupnirItem.DRIP, "a day later it drips");
        helper.assertTrue(player.getInventory().countItem(Items.GOLD_NUGGET) == DraupnirItem.DRIP, "eight nuggets in the bag");
        helper.assertTrue(DraupnirItem.drip(helper.getLevel(), player, ring) == 0, "and not again the same day");
        helper.succeed();
    }

    /** Gungnir finds the creature the thrower looks at, not the one beside, and strikes it. */
    @GameTest(template = "empty")
    public static void gungnirNeverMisses(GameTestHelper helper) {
        ServerLevel level = helper.getLevel();
        ServerPlayer player = TestPlayers.serverPlayer(helper, "odin");
        // The empty template is 5 x 6 x 3: the thrower stands at one end, the mark at the other, a decoy to the side.
        Vec3 eye = helper.absoluteVec(new Vec3(2.5, 2, 0.5));
        player.moveTo(eye.x, eye.y, eye.z, 0.0F, 0.0F);
        Zombie ahead = helper.spawn(EntityType.ZOMBIE, new BlockPos(2, 2, 2));
        Zombie aside = helper.spawn(EntityType.ZOMBIE, new BlockPos(4, 2, 0));
        player.setYRot(0.0F);
        player.setXRot(0.0F);
        var mark = GungnirItem.findMark(level, player);
        helper.assertTrue(mark == ahead, "the mark is the zombie straight ahead, got " + mark);
        GungnirItem.strike(level, player, ahead);
        helper.assertTrue(ahead.getHealth() < ahead.getMaxHealth() && aside.getHealth() == aside.getMaxHealth(), "only the mark is hit");
        ahead.discard();
        aside.discard();
        helper.succeed();
    }

    /** A valkyrie wife carries her husband out of a deadly fight, once a day. */
    @GameTest(template = "empty")
    public static void valkyrieCarriesHerHusband(GameTestHelper helper) {
        ServerPlayer player = TestPlayers.serverPlayer(helper, "sigurd");
        player.moveTo(helper.absoluteVec(new Vec3(1.5, 2, 1.5)));
        Valkyrie valkyrie = helper.spawn(NorseEntities.VALKYRIE.get(), new BlockPos(3, 2, 3));
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.WEDDING_RING.get()));
        valkyrie.setAffection(player, WarriorMaiden.LOVE);
        valkyrie.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(valkyrie.bond() == WarriorMaiden.Bond.WIFE, "she should be his wife");
        player.setHealth(0.5F);
        helper.assertTrue(ValkyrieRescue.rescue(player, valkyrie) && player.getHealth() == 6.0F, "she carries him out");
        helper.assertTrue(!ValkyrieRescue.rescue(player, valkyrie), "not twice the same day");
        valkyrie.discard();
        helper.succeed();
    }
}
