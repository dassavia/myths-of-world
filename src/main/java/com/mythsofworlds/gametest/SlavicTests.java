package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.journal.Journal;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.mythology.slavic.SlavicEntities;
import com.mythsofworlds.mythology.slavic.block.WorldTree;
import com.mythsofworlds.mythology.slavic.block.WorldTreeHollowBlock;
import com.mythsofworlds.mythology.slavic.entity.Firebird;
import com.mythsofworlds.mythology.slavic.entity.Koschei;
import com.mythsofworlds.mythology.slavic.entity.SlavicMerchant;
import com.mythsofworlds.mythology.slavic.entity.Upyr;
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
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.packs.resources.Resource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.FeatureSorter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** Slavic content: the World Tree, data files, structures, mobs, Koschei's death and the tales of Boyan. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class SlavicTests {
    @GameTest(template = "empty")
    public static void navBiomesLoadInOrder(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        List<Holder<Biome>> nav = new ArrayList<>();
        for (String biome : SlavicContent.BIOMES) {
            helper.assertTrue(biomes.containsKey(MythsOfWorlds.id(biome)), "worldgen/biome/" + biome + ".json did not load");
            nav.add(biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME, MythsOfWorlds.id(biome))));
        }
        FeatureSorter.buildFeaturesPerStep(nav, holder -> holder.value().getGenerationSettings().features(), true);
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void slavicStructuresLoad(GameTestHelper helper) throws Exception {
        var server = helper.getLevel().getServer();
        var structures = helper.getLevel().registryAccess().registryOrThrow(Registries.STRUCTURE);
        for (String name : SlavicContent.STRUCTURES) {
            helper.assertTrue(structures.containsKey(MythsOfWorlds.id(name)), "worldgen/structure/" + name + ".json did not load");
            ResourceLocation template = MythsOfWorlds.id("slavic/" + name);
            helper.assertTrue(server.getStructureManager().get(template).isPresent(), "template " + template + " missing");
            Resource file = server.getResourceManager().getResourceOrThrow(MythsOfWorlds.id("structure/slavic/" + name + ".nbt"));
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
    public static void everySlavicMobSpawns(GameTestHelper helper) {
        for (var type : SlavicEntities.all()) {
            Mob mob = helper.spawn(type.get(), new BlockPos(1, 2, 1));
            helper.assertTrue(mob.isAlive() && mob.getHealth() > 0, type.getId() + " did not spawn alive");
            mob.discard();
        }
        helper.succeed();
    }

    /**
     * The acorn grows a whole oak with a two-block hollow facing the planter; a second tree does not fit in its
     * place, the hollow is found again, and it closes when the trunk beside it is cut. Grown high above the test
     * area so that the crown does not reach the other tests.
     */
    @GameTest(template = "empty")
    public static void worldTreeGrowsWithHollow(GameTestHelper helper) {
        ServerLevel level = helper.getLevel();
        BlockPos corner = helper.absolutePos(BlockPos.ZERO);
        BlockPos centre = new BlockPos(corner.getX(), 200, corner.getZ());
        int flags = Block.UPDATE_ALL;
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                level.setBlock(centre.offset(dx, -1, dz), Blocks.GRASS_BLOCK.defaultBlockState(), flags);
            }
        }
        helper.assertTrue(WorldTree.canGrow(level, centre, Direction.SOUTH), "there is room for the World Tree");
        BlockPos hollow = WorldTree.grow(level, centre, Direction.SOUTH, level.getRandom());
        helper.assertTrue(hollow.equals(centre.south()), "the hollow is at the front of the trunk");
        for (BlockPos pos : new BlockPos[]{hollow, hollow.above()}) {
            var state = level.getBlockState(pos);
            helper.assertTrue(state.is(SlavicContent.WORLD_TREE_HOLLOW.get()) && state.getValue(WorldTreeHollowBlock.FACING) == Direction.SOUTH,
                    "a two-block hollow facing south at " + pos);
        }
        helper.assertTrue(level.getBlockState(centre.above(WorldTree.HEIGHT - 1)).is(Blocks.OAK_LOG), "the trunk is tall");
        helper.assertTrue(level.getBlockState(hollow.south()).isAir() && level.getBlockState(hollow.south().above()).isAir(),
                "the doorway is open");
        helper.assertTrue(!WorldTree.canGrow(level, centre, Direction.SOUTH), "a second tree does not fit in the first one");
        BlockPos found = WorldTree.find(level, centre.offset(5, 0, 5));
        helper.assertTrue(hollow.equals(found), "the hollow is found again, got " + found);
        level.setBlock(hollow.east(), Blocks.AIR.defaultBlockState(), flags);
        helper.assertTrue(!level.getBlockState(hollow).is(SlavicContent.WORLD_TREE_HOLLOW.get()), "cutting the trunk closes the hollow");
        BlockPos.betweenClosed(centre.offset(-8, -1, -8), centre.offset(8, WorldTree.HEIGHT + 6, 8))
                .forEach(pos -> level.setBlock(pos, Blocks.AIR.defaultBlockState(), Block.UPDATE_CLIENTS));
        helper.succeed();
    }

    /** Koschei gets up again with full health, unless his killer carries the needle; then he dies and it breaks. */
    @GameTest(template = "empty")
    public static void koscheiDiesOnlyToTheNeedle(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var sources = helper.getLevel().damageSources();
        Koschei koschei = helper.spawn(SlavicEntities.KOSCHEI.get(), new BlockPos(1, 2, 1));
        koschei.hurt(sources.playerAttack(player), 10000.0F);
        helper.assertTrue(koschei.isAlive() && koschei.getHealth() == koschei.getMaxHealth(), "Koschei should rise again");
        player.getInventory().add(new ItemStack(SlavicContent.KOSCHEI_NEEDLE.get()));
        koschei.invulnerableTime = 0;
        koschei.hurt(sources.playerAttack(player), 10000.0F);
        helper.assertTrue(koschei.isDeadOrDying(), "with the needle Koschei should die");
        helper.assertTrue(!player.getInventory().contains(new ItemStack(SlavicContent.KOSCHEI_NEEDLE.get())), "the needle breaks");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void koscheiEggHoldsTheNeedle(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(SlavicContent.KOSCHEI_EGG.get()));
        var result = SlavicContent.KOSCHEI_EGG.get().use(helper.getLevel(), player, InteractionHand.MAIN_HAND);
        helper.assertTrue(result.getObject().is(SlavicContent.KOSCHEI_NEEDLE.get()), "the egg should give the needle");
        helper.succeed();
    }

    /** Stroking the Firebird gives one feather, then she needs time to grow another. */
    @GameTest(template = "empty")
    public static void firebirdGivesFeather(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        Firebird bird = helper.spawn(SlavicEntities.FIREBIRD.get(), new BlockPos(1, 2, 1));
        bird.mobInteract(player, InteractionHand.MAIN_HAND);
        bird.mobInteract(player, InteractionHand.MAIN_HAND);
        var feathers = helper.getLevel().getEntitiesOfClass(ItemEntity.class, bird.getBoundingBox().inflate(4.0),
                item -> item.getItem().is(SlavicContent.FIREBIRD_FEATHER.get()));
        helper.assertTrue(feathers.size() == 1, "one stroke, one feather; got " + feathers.size());
        helper.assertTrue(bird.featherCooldown() > 0, "the next feather takes time");
        feathers.forEach(ItemEntity::discard);
        bird.discard();
        helper.succeed();
    }

    /** Every kind of trader has trades, and Baba Yaga sells the waters and the acorn of the World Tree. */
    @GameTest(template = "empty")
    public static void slavicMerchantsTrade(GameTestHelper helper) {
        boolean living = false, acorn = false;
        for (int kind = 0; kind < SlavicMerchant.KINDS; kind++) {
            SlavicMerchant merchant = helper.spawn(SlavicEntities.SLAVIC_MERCHANT.get(), new BlockPos(1, 2, 1));
            merchant.setKind(kind);
            var offers = merchant.getOffers();
            helper.assertTrue(!offers.isEmpty(), "trader kind " + kind + " has no trades");
            for (var offer : offers) {
                living |= kind == SlavicMerchant.BABA_YAGA && offer.getResult().is(SlavicContent.LIVING_WATER.get());
                acorn |= offer.getResult().is(SlavicContent.WORLD_TREE_ACORN.get());
            }
            merchant.discard();
        }
        helper.assertTrue(living && acorn, "Baba Yaga sells living water: " + living + ", someone sells acorns: " + acorn);
        helper.succeed();
    }

    /** A blow of the kladenets also cuts the foes standing around the one struck. */
    @GameTest(template = "empty")
    public static void kladenetsStrikesAround(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        Upyr target = helper.spawn(SlavicEntities.UPYR.get(), new BlockPos(1, 2, 1));
        Upyr beside = helper.spawn(SlavicEntities.UPYR.get(), new BlockPos(2, 2, 1));
        ItemStack sword = new ItemStack(SlavicContent.KLADENETS.get());
        sword.getItem().hurtEnemy(sword, target, player);
        helper.assertTrue(beside.getHealth() < beside.getMaxHealth(), "the upyr beside should be cut too");
        target.discard();
        beside.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void talesOfBoyanShowWhatWasFound(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var entries = Journal.volume("slavic");
        helper.assertTrue(entries.size() > 15, "the tales of Nav have only " + entries.size() + " entries");
        int fresh = Journal.book("slavic", player, false).pages().size();
        int complete = Journal.book("slavic", player, true).pages().size();
        PlayerData.addEntry(player, "slavic.koschei");
        int afterKoschei = Journal.book("slavic", player, false).pages().size();
        helper.assertTrue(complete > afterKoschei && afterKoschei > fresh, "pages: new " + fresh + ", after Koschei " + afterKoschei
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
}
