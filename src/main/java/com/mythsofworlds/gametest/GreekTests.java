package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.Mythology;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.entity.GreekMerchant;
import com.mythsofworlds.mythology.greek.entity.Hydra;
import com.mythsofworlds.mythology.greek.entity.HydraHatchling;
import com.mythsofworlds.mythology.greek.entity.NemeanLion;
import com.mythsofworlds.mythology.greek.entity.Spartoi;
import com.mythsofworlds.mythology.greek.portal.BrazierBlock;
import com.mythsofworlds.mythology.greek.portal.PoolPortal;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.Holder;
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
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.FeatureSorter;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
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
}
