package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.journal.Journal;
import com.mythsofworlds.mythology.Mythology;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.GreekEvents;
import com.mythsofworlds.mythology.greek.block.FruitLeavesBlock;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.greek.entity.Cerberus;
import com.mythsofworlds.mythology.greek.entity.GreekMerchant;
import com.mythsofworlds.mythology.greek.entity.Hippolyta;
import com.mythsofworlds.mythology.greek.entity.Hydra;
import com.mythsofworlds.mythology.greek.entity.HydraHatchling;
import com.mythsofworlds.mythology.greek.entity.Medusa;
import com.mythsofworlds.mythology.greek.entity.NemeanLion;
import com.mythsofworlds.mythology.greek.entity.Spartoi;
import com.mythsofworlds.mythology.greek.entity.ThrownGrowthPotion;
import com.mythsofworlds.mythology.greek.item.HornOfThemiscyraItem;
import com.mythsofworlds.mythology.greek.portal.BrazierBlock;
import com.mythsofworlds.mythology.greek.portal.PoolPortal;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.NbtAccounter;
import net.minecraft.nbt.NbtIo;
import net.minecraft.nbt.Tag;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.item.enchantment.Enchantments;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.FeatureSorter;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LeavesBlock;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.storage.loot.BuiltInLootTables;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** Greek content: portal, data files, structures and mobs. Run with {@code ./gradlew runGameTestServer}. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class GreekTests {
    /** Builds a 1x1 sacred pool at (1, 1, 1) with braziers on the rim corners; {@code lit} of them burn. */
    private static void buildPool(GameTestHelper helper, int lit) {
        BlockState brazier = GreekContent.BRAZIER.get().defaultBlockState();
        int corner = 0;
        for (int x = 0; x <= 2; x++) {
            for (int z = 0; z <= 2; z++) {
                helper.setBlock(new BlockPos(x, 0, z), GreekContent.MARBLE_BRICKS.get());
                boolean water = x == 1 && z == 1;
                helper.setBlock(new BlockPos(x, 1, z), water ? Blocks.WATER : GreekContent.OLYMPIAN_MARBLE.get());
                if (x != 1 && z != 1) {
                    helper.setBlock(new BlockPos(x, 2, z), brazier.setValue(BrazierBlock.LIT, corner++ < lit));
                }
            }
        }
    }

    @GameTest(template = "empty")
    public static void poolOpensWhenFourBraziersBurn(GameTestHelper helper) {
        buildPool(helper, 3);
        BlockPos last = new BlockPos(2, 2, 2);
        helper.assertTrue(!PoolPortal.tryLight(helper.getLevel(), helper.absolutePos(last)), "three fires must not open the pool");
        helper.setBlock(last, GreekContent.BRAZIER.get().defaultBlockState().setValue(BrazierBlock.LIT, true));
        helper.assertTrue(PoolPortal.tryLight(helper.getLevel(), helper.absolutePos(last)), "four fires should open the pool");
        helper.assertBlockPresent(GreekContent.HELLAS_PORTAL.get(), new BlockPos(1, 1, 1));
        helper.setBlock(new BlockPos(0, 2, 0), Blocks.AIR);
        helper.assertBlockPresent(Blocks.WATER, new BlockPos(1, 1, 1));
        helper.succeed();
    }

    /** Plain marble is decoration only: it must not open the portal. */
    @GameTest(template = "empty")
    public static void poolNeedsOlympianMarble(GameTestHelper helper) {
        buildPool(helper, 4);
        helper.setBlock(new BlockPos(1, 1, 0), GreekContent.MARBLE.get());
        helper.assertTrue(!PoolPortal.tryLight(helper.getLevel(), helper.absolutePos(new BlockPos(0, 2, 0))),
                "a pool rimmed with plain marble must not open");
        helper.succeed();
    }

    /** Every mythology's dimension type and every biome of Hellas parsed. */
    @GameTest(template = "empty")
    public static void worldDataLoads(GameTestHelper helper) {
        var registries = helper.getLevel().registryAccess();
        for (Mythology mythology : Mythology.values()) {
            helper.assertTrue(registries.registryOrThrow(Registries.DIMENSION_TYPE).containsKey(mythology.dimension().location()),
                    "dimension_type for " + mythology + " did not load");
        }
        for (String biome : GreekContent.BIOMES) {
            helper.assertTrue(registries.registryOrThrow(Registries.BIOME).containsKey(MythsOfWorlds.id(biome)),
                    "worldgen/biome/" + biome + ".json did not load");
        }
        helper.succeed();
    }

    /** The biomes of one dimension must list shared features in the same order, or the world fails to load. */
    @GameTest(template = "empty")
    public static void hellasFeatureOrderIsConsistent(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        List<Holder<Biome>> hellas = new ArrayList<>();
        for (String biome : GreekContent.BIOMES) {
            hellas.add(biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME, MythsOfWorlds.id(biome))));
        }
        FeatureSorter.buildFeaturesPerStep(hellas, holder -> holder.value().getGenerationSettings().features(), true);
        helper.succeed();
    }

    /** Structures are registered, their templates load, and every mob inside a template is a real entity type. */
    @GameTest(template = "empty")
    public static void structuresLoad(GameTestHelper helper) throws Exception {
        var server = helper.getLevel().getServer();
        var structures = helper.getLevel().registryAccess().registryOrThrow(Registries.STRUCTURE);
        for (String name : GreekContent.STRUCTURES) {
            helper.assertTrue(structures.containsKey(MythsOfWorlds.id(name)), "worldgen/structure/" + name + ".json did not load");
            ResourceLocation template = MythsOfWorlds.id("greek/" + name);
            helper.assertTrue(server.getStructureManager().get(template).isPresent(), "template " + template + " missing");
            Resource file = server.getResourceManager().getResourceOrThrow(MythsOfWorlds.id("structure/greek/" + name + ".nbt"));
            try (InputStream in = file.open()) {
                CompoundTag root = NbtIo.readCompressed(in, NbtAccounter.unlimitedHeap());
                for (Tag entity : root.getList("entities", Tag.TAG_COMPOUND)) {
                    CompoundTag tag = ((CompoundTag) entity).getCompound("nbt");
                    helper.assertTrue(EntityType.by(tag).isPresent(), name + ": unknown entity " + tag.getString("id"));
                }
            }
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void everyMobSpawns(GameTestHelper helper) {
        for (var type : GreekEntities.all()) {
            Mob mob = helper.spawn(type.get(), new BlockPos(1, 2, 1));
            helper.assertTrue(mob.isAlive() && mob.getHealth() > 0, type.getId() + " did not spawn alive");
            mob.discard();
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void nemeanLionHideStopsDirectDamage(GameTestHelper helper) {
        NemeanLion lion = helper.spawn(GreekEntities.NEMEAN_LION.get(), new BlockPos(1, 2, 1));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var sources = helper.getLevel().damageSources();
        lion.hurt(sources.thrown(lion, null), 20.0F);
        lion.hurt(sources.playerAttack(player), 20.0F);
        lion.hurt(sources.generic(), 20.0F);
        helper.assertTrue(lion.getHealth() == lion.getMaxHealth(), "arrows, fists and swords must not hurt the Nemean lion");
        lion.hurt(sources.magic(), 10.0F);
        float afterPotion = lion.getHealth();
        helper.assertTrue(afterPotion < lion.getMaxHealth(), "potions must hurt it");
        lion.invulnerableTime = 0;
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.NEMEAN_CLAW_DAGGER.get()));
        lion.hurt(sources.playerAttack(player), 10.0F);
        helper.assertTrue(lion.getHealth() < afterPotion, "the claw dagger must cut its hide");
        lion.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void hydraEggHatchesTamePet(GameTestHelper helper) {
        helper.setBlock(new BlockPos(1, 0, 1), Blocks.STONE);
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.HYDRA_EGG.get()));
        BlockPos ground = helper.absolutePos(new BlockPos(1, 0, 1));
        GreekContent.HYDRA_EGG.get().useOn(new UseOnContext(player, InteractionHand.MAIN_HAND,
                new BlockHitResult(Vec3.atCenterOf(ground), Direction.UP, ground, false)));
        var pets = helper.getLevel().getEntitiesOfClass(HydraHatchling.class, new AABB(ground).inflate(2.0));
        helper.assertTrue(pets.size() == 1, "one hatchling should hatch, got " + pets.size());
        helper.assertTrue(pets.get(0).isTame() && player.getUUID().equals(pets.get(0).getOwnerUUID()), "the hatchling should belong to whoever hatched it");
        helper.assertTrue(player.getMainHandItem().isEmpty(), "the egg should be used up");
        pets.get(0).discard();
        helper.succeed();
    }

    /** Every kind of agora merchant has trades, and the trophy dealer buys the Minotaur's horn. */
    @GameTest(template = "empty")
    public static void merchantsTrade(GameTestHelper helper) {
        boolean buysHorn = false;
        for (int kind = 0; kind < GreekMerchant.KINDS; kind++) {
            GreekMerchant merchant = helper.spawn(GreekEntities.GREEK_MERCHANT.get(), new BlockPos(1, 2, 1));
            merchant.setKind(kind);
            var offers = merchant.getOffers();
            helper.assertTrue(!offers.isEmpty(), "merchant kind " + kind + " has no trades");
            for (var offer : offers) {
                buysHorn |= offer.getCostA().is(GreekContent.MINOTAUR_HORN.get());
            }
            merchant.discard();
        }
        helper.assertTrue(buysHorn, "nobody buys the Minotaur horn");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void spartoiRiseAgainOnlyOnce(GameTestHelper helper) {
        Spartoi spartoi = helper.spawn(GreekEntities.SPARTOI.get(), new BlockPos(1, 2, 1));
        spartoi.rise();
        helper.assertTrue(spartoi.isReborn() && spartoi.isAlive(), "a risen spartoi should be alive");
        spartoi.hurt(helper.getLevel().damageSources().generic(), 1000.0F);
        helper.assertTrue(spartoi.isDeadOrDying(), "a spartoi rises only once");
        helper.succeed();
    }

    @GameTest(template = "empty", timeoutTicks = 120)
    public static void hydraRegeneratesUnlessBurned(GameTestHelper helper) {
        Hydra healing = helper.spawn(GreekEntities.HYDRA.get(), new BlockPos(1, 2, 1));
        healing.setHealth(100.0F);
        Hydra burned = helper.spawn(GreekEntities.HYDRA.get(), new BlockPos(1, 2, 1));
        burned.setHealth(101.0F);
        burned.hurt(helper.getLevel().damageSources().inFire(), 1.0F);
        float burnedStart = burned.getHealth();
        helper.runAfterDelay(80, () -> {
            helper.assertTrue(healing.getHealth() > 100.0F, "the hydra should regenerate");
            helper.assertTrue(burned.getHealth() <= burnedStart, "fire should stop the hydra regenerating");
            healing.discard();
            burned.discard();
            helper.succeed();
        });
    }

    /** The labyrinth of Daedalus cannot be dug through. */
    @GameTest(template = "empty")
    public static void labyrinthWallsAreUnbreakable(GameTestHelper helper) {
        BlockPos pos = new BlockPos(1, 1, 1);
        for (var block : List.of(GreekContent.LABYRINTH_BRICKS, GreekContent.MOSSY_LABYRINTH_BRICKS, GreekContent.CRACKED_LABYRINTH_BRICKS)) {
            helper.setBlock(pos, block.get());
            BlockState state = helper.getBlockState(pos);
            helper.assertTrue(state.getDestroySpeed(helper.getLevel(), helper.absolutePos(pos)) < 0, block.getId() + " can be broken");
            helper.assertTrue(state.getBlock().getExplosionResistance() >= 3600000.0F, block.getId() + " can be blown up");
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void pumpkinHidesTheEyesFromMedusa(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        helper.assertTrue(!Medusa.isShielded(player), "a bare-headed player must see Medusa's gaze");
        player.setItemSlot(EquipmentSlot.HEAD, new ItemStack(Items.CARVED_PUMPKIN));
        helper.assertTrue(Medusa.isShielded(player), "a carved pumpkin must protect from the gaze");
        helper.succeed();
    }

    /** Fire aspect cuts the hydra far deeper than a plain blade. */
    @GameTest(template = "empty")
    public static void fireAspectHurtsTheHydra(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var sources = helper.getLevel().damageSources();
        Hydra plain = helper.spawn(GreekEntities.HYDRA.get(), new BlockPos(1, 2, 1));
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
        plain.hurt(sources.playerAttack(player), 10.0F);
        float plainLoss = plain.getMaxHealth() - plain.getHealth();
        Hydra burned = helper.spawn(GreekEntities.HYDRA.get(), new BlockPos(1, 2, 1));
        ItemStack fireSword = new ItemStack(Items.IRON_SWORD);
        fireSword.enchant(helper.getLevel().registryAccess().registryOrThrow(Registries.ENCHANTMENT)
                .getHolderOrThrow(Enchantments.FIRE_ASPECT), 2);
        player.setItemInHand(InteractionHand.MAIN_HAND, fireSword);
        burned.hurt(sources.playerAttack(player), 10.0F);
        float fireLoss = burned.getMaxHealth() - burned.getHealth();
        helper.assertTrue(fireLoss > plainLoss * 3.0F, "fire aspect II should hurt the hydra 4 times as much: " + fireLoss + " vs " + plainLoss);
        helper.assertTrue(burned.isCauterized(), "a fire aspect blow should stop the regeneration");
        plain.discard();
        burned.discard();
        helper.succeed();
    }

    /** Courtship from first gift to a daughter. */
    @GameTest(template = "empty")
    public static void amazonMarriesAndHasADaughter(GameTestHelper helper) {
        Amazon amazon = helper.spawn(GreekEntities.AMAZON.get(), new BlockPos(1, 2, 1));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.GOLD_INGOT));
        amazon.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(amazon.affection(player) >= 10, "a gold ingot should win some affection");
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.WEDDING_RING.get()));
        amazon.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(amazon.bond() == Amazon.Bond.NONE, "she must not marry before she loves you");
        amazon.setAffection(player, Amazon.LOVE);
        amazon.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(amazon.bond() == Amazon.Bond.WIFE && amazon.isFamily(player), "she should accept the ring");
        helper.assertTrue(PlayerData.spouse(player).filter(amazon.getUUID()::equals).isPresent(), "the player should be married to her");
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.CAKE));
        amazon.mobInteract(player, InteractionHand.MAIN_HAND);
        var daughters = helper.getLevel().getEntitiesOfClass(Amazon.class, amazon.getBoundingBox().inflate(3.0),
                a -> a.isBaby() && a.bond() == Amazon.Bond.DAUGHTER && a.isFamily(player));
        helper.assertTrue(daughters.size() == 1, "a cake should bring one daughter, got " + daughters.size());
        Amazon other = helper.spawn(GreekEntities.AMAZON.get(), new BlockPos(1, 2, 1));
        other.setAffection(player, Amazon.LOVE);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.WEDDING_RING.get()));
        other.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(other.bond() == Amazon.Bond.NONE && other.rival() == amazon && amazon.rival() == other,
                "a second proposal should start a duel with the wife");
        amazon.hurt(helper.getLevel().damageSources().mobAttack(other), 1000.0F);
        helper.assertTrue(amazon.isAlive() && amazon.rival() == null && other.rival() == null, "the beaten wife should yield, not die");
        helper.assertTrue(other.bond() == Amazon.Bond.WIFE && amazon.bond() == Amazon.Bond.NONE
                && PlayerData.spouse(player).filter(other.getUUID()::equals).isPresent(), "the winner of the duel becomes the wife");
        daughters.forEach(Amazon::discard);
        amazon.discard();
        other.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void hippolytaYieldsAndGivesHerGirdle(GameTestHelper helper) {
        Hippolyta queen = helper.spawn(GreekEntities.HIPPOLYTA.get(), new BlockPos(1, 2, 1));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.DIAMOND));
        queen.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(queen.affection(player) == 0, "she ignores gifts from someone who has not beaten her");
        queen.hurt(helper.getLevel().damageSources().playerAttack(player), 1000.0F);
        helper.assertTrue(queen.isAlive() && queen.hasYielded() && queen.isWorthy(player), "she should yield instead of dying");
        var girdles = helper.getLevel().getEntitiesOfClass(ItemEntity.class, queen.getBoundingBox().inflate(3.0),
                item -> item.getItem().is(GreekContent.GIRDLE_OF_HIPPOLYTA.get()));
        helper.assertTrue(girdles.size() == 1, "she should give up her girdle");
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.MINOTAUR_HORN.get()));
        queen.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(queen.affection(player) > 0, "a worthy trophy should please her");
        girdles.forEach(ItemEntity::discard);
        queen.discard();
        helper.succeed();
    }

    /** The necklace of Harmonia wins an amazon's heart at once; Hippolyta takes it only from her victor. */
    @GameTest(template = "empty")
    public static void necklaceOfHarmoniaWinsAmazons(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        Amazon amazon = helper.spawn(GreekEntities.AMAZON.get(), new BlockPos(1, 2, 1));
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.NECKLACE_OF_HARMONIA.get()));
        amazon.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(amazon.affection(player) >= Amazon.LOVE, "the necklace should make her fall in love");
        helper.assertTrue(player.getMainHandItem().isEmpty(), "the necklace should be given away");
        Hippolyta queen = helper.spawn(GreekEntities.HIPPOLYTA.get(), new BlockPos(1, 2, 1));
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.NECKLACE_OF_HARMONIA.get()));
        queen.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(queen.affection(player) == 0, "the queen ignores it from someone who has not beaten her");
        amazon.discard();
        queen.discard();
        helper.succeed();
    }

    /** Beating Hippolyta does not ruin the courtship, and the same kind of treasure can be given again. */
    @GameTest(template = "empty")
    public static void hippolytaCanBeWon(GameTestHelper helper) {
        Hippolyta queen = helper.spawn(GreekEntities.HIPPOLYTA.get(), new BlockPos(1, 2, 1));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var sources = helper.getLevel().damageSources();
        for (int i = 0; i < 5; i++) {
            queen.invulnerableTime = 0;
            queen.hurt(sources.playerAttack(player), 10.0F);
        }
        queen.invulnerableTime = 0;
        queen.hurt(sources.playerAttack(player), 1000.0F);
        helper.assertTrue(queen.hasYielded() && queen.affection(player) >= 0, "the duel should be forgiven, affection "
                + queen.affection(player));
        for (int i = 0; i < 9; i++) {
            player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.NETHERITE_INGOT));
            queen.mobInteract(player, InteractionHand.MAIN_HAND);
        }
        helper.assertTrue(queen.affection(player) >= Amazon.LOVE, "repeated treasures should win her in the end, affection "
                + queen.affection(player));
        helper.getLevel().getEntitiesOfClass(ItemEntity.class, queen.getBoundingBox().inflate(4.0)).forEach(ItemEntity::discard);
        queen.discard();
        helper.succeed();
    }

    /** An amazon keeps to her camp, and the horn of Themiscyra sends a stray back. */
    @GameTest(template = "empty", timeoutTicks = 40)
    public static void hornCallsAmazonsHome(GameTestHelper helper) {
        Amazon amazon = helper.spawn(GreekEntities.AMAZON.get(), new BlockPos(1, 2, 1));
        helper.runAfterDelay(2, () -> {
            helper.assertTrue(amazon.home() != null, "an amazon should remember her camp");
            // Pretend her camp is far away: she has strayed 52 blocks from it.
            BlockPos home = amazon.blockPosition().offset(52, 0, 0);
            amazon.setHome(home, Amazon.HOME_RADIUS);
            Player player = helper.makeMockPlayer(GameType.SURVIVAL);
            player.moveTo(amazon.getX(), amazon.getY(), amazon.getZ());
            int called = HornOfThemiscyraItem.callAmazons(helper.getLevel(), player);
            helper.assertTrue(called == 1, "the horn should call her, called " + called);
            helper.assertTrue(amazon.distanceToSqr(home.getX() + 0.5, home.getY(), home.getZ() + 0.5) < 4.0,
                    "a far stray should come home at once");
            amazon.discard();
            helper.succeed();
        });
    }

    /** A wife follows, waits, or walks freely, in turn on shift + right-click. */
    @GameTest(template = "empty")
    public static void wifeCanWanderFreely(GameTestHelper helper) {
        Amazon amazon = helper.spawn(GreekEntities.AMAZON.get(), new BlockPos(1, 2, 1));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        amazon.setAffection(player, Amazon.LOVE);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.WEDDING_RING.get()));
        amazon.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(amazon.mode() == Amazon.Mode.FOLLOW && amazon.home() == null, "a new wife follows her husband");
        player.setShiftKeyDown(true);
        amazon.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(amazon.mode() == Amazon.Mode.STAY, "first she waits");
        amazon.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(amazon.mode() == Amazon.Mode.WANDER && amazon.home() != null, "then she walks freely around here");
        amazon.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(amazon.mode() == Amazon.Mode.FOLLOW, "then she follows again");
        PlayerData.setSpouse(player, java.util.Optional.empty());
        amazon.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void ripeOlivesCanBePicked(GameTestHelper helper) {
        BlockPos pos = new BlockPos(1, 2, 1);
        helper.setBlock(pos, GreekContent.OLIVE_LEAVES.get().defaultBlockState()
                .setValue(FruitLeavesBlock.AGE, FruitLeavesBlock.RIPE).setValue(LeavesBlock.PERSISTENT, true));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        BlockPos abs = helper.absolutePos(pos);
        helper.getBlockState(pos).useWithoutItem(helper.getLevel(), player, new BlockHitResult(Vec3.atCenterOf(abs), Direction.UP, abs, false));
        helper.assertTrue(helper.getBlockState(pos).getValue(FruitLeavesBlock.AGE) == 0, "picking should leave unripe leaves");
        var olives = helper.getLevel().getEntitiesOfClass(ItemEntity.class, new AABB(abs).inflate(2.0),
                item -> item.getItem().is(GreekContent.OLIVES.get()));
        helper.assertTrue(!olives.isEmpty(), "picking ripe leaves should drop olives");
        olives.forEach(ItemEntity::discard);
        helper.succeed();
    }

    /** The journal loads, the complete copy holds every entry, and a new hero's copy only the introduction. */
    @GameTest(template = "empty")
    public static void journalShowsWhatWasFound(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var entries = Journal.volume("greek");
        helper.assertTrue(entries.size() > 30, "the journal of Hellas has only " + entries.size() + " entries");
        int fresh = Journal.book("greek", player, false).pages().size();
        int complete = Journal.book("greek", player, true).pages().size();
        PlayerData.addEntry(player, "greek.hydra");
        int afterHydra = Journal.book("greek", player, false).pages().size();
        helper.assertTrue(complete > afterHydra && afterHydra > fresh, "pages: new " + fresh + ", after the hydra " + afterHydra
                + ", complete " + complete);
        for (var entry : entries) {
            if (entry.entity().isPresent()) {
                helper.assertTrue(BuiltInRegistries.ENTITY_TYPE.containsKey(entry.entity().get()), "unknown mob " + entry.entity().get());
            }
            if (entry.structure().isPresent()) {
                helper.assertTrue(helper.getLevel().registryAccess().registryOrThrow(Registries.STRUCTURE).containsKey(entry.structure().get()),
                        "unknown structure " + entry.structure().get());
            }
        }
        helper.succeed();
    }

    /** The splash potion of growth grows up every young creature where it bursts: a little amazon, a calf, a zombie. */
    @GameTest(template = "empty")
    public static void growthPotionGrowsTheYoung(GameTestHelper helper) {
        Amazon girl = helper.spawn(GreekEntities.AMAZON.get(), new BlockPos(1, 2, 1));
        girl.setBaby(true);
        Mob calf = helper.spawn(EntityType.COW, new BlockPos(2, 2, 1));
        calf.setBaby(true);
        Mob zombie = helper.spawn(EntityType.ZOMBIE, new BlockPos(1, 2, 2));
        zombie.setBaby(true);
        helper.assertTrue(girl.isBaby() && calf.isBaby() && zombie.isBaby(), "they should start young");
        int grown = ThrownGrowthPotion.burst(helper.getLevel(), Vec3.atCenterOf(helper.absolutePos(new BlockPos(1, 2, 1))));
        helper.assertTrue(grown == 3, "grew up " + grown + " of 3");
        helper.assertTrue(!girl.isBaby() && !calf.isBaby() && !zombie.isBaby(), "everyone should be grown");
        girl.discard();
        calf.discard();
        zombie.discard();
        helper.succeed();
    }

    /** The girdle is worn as armour on the legs, so others see it on the wearer. */
    @GameTest(template = "empty")
    public static void girdleIsWornArmour(GameTestHelper helper) {
        var girdle = GreekContent.GIRDLE_OF_HIPPOLYTA.get();
        helper.assertTrue(girdle.getEquipmentSlot() == EquipmentSlot.LEGS, "the girdle goes in the legs slot");
        helper.assertTrue(!girdle.getMaterial().value().layers().isEmpty(), "the girdle needs an armour layer to be seen");
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemSlot(EquipmentSlot.LEGS, new ItemStack(girdle));
        helper.assertTrue(com.mythsofworlds.mythology.greek.item.GirdleItem.isWorn(player), "the girdle should count as worn");
        helper.succeed();
    }

    /** The bident of Hades fells Cerberus at once, as if the player had slain him, and is used up. */
    @GameTest(template = "empty")
    public static void bidentOfHadesBanishesCerberus(GameTestHelper helper) {
        Cerberus cerberus = helper.spawn(GreekEntities.CERBERUS.get(), new BlockPos(1, 2, 1));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.BIDENT_OF_HADES.get()));
        InteractionResult result = player.getMainHandItem().interactLivingEntity(player, cerberus, InteractionHand.MAIN_HAND);
        helper.assertTrue(result.consumesAction(), "using the bident on Cerberus should work, got " + result);
        helper.assertTrue(!cerberus.isAlive(), "Cerberus should fall at once");
        helper.assertTrue(player.getMainHandItem().isEmpty(), "the bident works only once");
        helper.assertTrue(GreekEvents.BIDENT_CHESTS.containsKey(BuiltInLootTables.NETHER_BRIDGE.location()),
                "the bident should be hidden in Nether fortresses");
        helper.succeed();
    }
}
