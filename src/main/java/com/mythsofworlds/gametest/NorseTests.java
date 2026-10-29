package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.journal.Journal;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.norse.NorseEntities;
import com.mythsofworlds.mythology.norse.entity.Draugr;
import com.mythsofworlds.mythology.norse.entity.Fenrir;
import com.mythsofworlds.mythology.norse.entity.NorseMerchant;
import com.mythsofworlds.mythology.norse.entity.Troll;
import com.mythsofworlds.mythology.norse.item.MjolnirItem;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.BlockPos;
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
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.FeatureSorter;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.AABB;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** Norse content: data files, structures, mobs, the relics of the gods and the saga. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class NorseTests {
    @GameTest(template = "empty")
    public static void jotunheimBiomesLoadInOrder(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        List<Holder<Biome>> jotunheim = new ArrayList<>();
        for (String biome : NorseContent.BIOMES) {
            helper.assertTrue(biomes.containsKey(MythsOfWorlds.id(biome)), "worldgen/biome/" + biome + ".json did not load");
            jotunheim.add(biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME, MythsOfWorlds.id(biome))));
        }
        FeatureSorter.buildFeaturesPerStep(jotunheim, holder -> holder.value().getGenerationSettings().features(), true);
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void norseStructuresLoad(GameTestHelper helper) throws Exception {
        var server = helper.getLevel().getServer();
        var structures = helper.getLevel().registryAccess().registryOrThrow(Registries.STRUCTURE);
        for (String name : NorseContent.STRUCTURES) {
            helper.assertTrue(structures.containsKey(MythsOfWorlds.id(name)), "worldgen/structure/" + name + ".json did not load");
            ResourceLocation template = MythsOfWorlds.id("norse/" + name);
            helper.assertTrue(server.getStructureManager().get(template).isPresent(), "template " + template + " missing");
            Resource file = server.getResourceManager().getResourceOrThrow(MythsOfWorlds.id("structure/norse/" + name + ".nbt"));
            try (InputStream in = file.open()) {
                CompoundTag root = NbtIo.readCompressed(in, NbtAccounter.unlimitedHeap());
                for (Tag entity : root.getList("entities", Tag.TAG_COMPOUND)) {
                    CompoundTag tag = ((CompoundTag) entity).getCompound("nbt");
                    helper.assertTrue(EntityType.by(tag).isPresent(),
                            name + ": unknown entity " + tag.getString("id"));
                }
            }
        }
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void everyNorseMobSpawns(GameTestHelper helper) {
        for (var type : NorseEntities.all()) {
            Mob mob = helper.spawn(type.get(), new BlockPos(1, 2, 1));
            helper.assertTrue(mob.isAlive() && mob.getHealth() > 0, type.getId() + " did not spawn alive");
            mob.discard();
        }
        helper.succeed();
    }

    /** A sword only knocks a draugr down once; an axe or fire lays it to rest. */
    @GameTest(template = "empty")
    public static void draugrRisesUnlessAxeOrFire(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var sources = helper.getLevel().damageSources();
        Draugr swordKill = helper.spawn(NorseEntities.DRAUGR.get(), new BlockPos(1, 2, 1));
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
        swordKill.hurt(sources.playerAttack(player), 1000.0F);
        helper.assertTrue(swordKill.isAlive() && swordKill.hasRisen(), "a draugr killed with a sword should rise again");
        swordKill.invulnerableTime = 0;
        swordKill.hurt(sources.playerAttack(player), 1000.0F);
        helper.assertTrue(swordKill.isDeadOrDying(), "a draugr rises only once");
        Draugr axeKill = helper.spawn(NorseEntities.DRAUGR.get(), new BlockPos(1, 2, 1));
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_AXE));
        axeKill.hurt(sources.playerAttack(player), 1000.0F);
        helper.assertTrue(axeKill.isDeadOrDying(), "an axe should lay a draugr to rest");
        Draugr burned = helper.spawn(NorseEntities.DRAUGR.get(), new BlockPos(1, 2, 1));
        burned.hurt(sources.inFire(), 1000.0F);
        helper.assertTrue(burned.isDeadOrDying(), "fire should lay a draugr to rest");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void trollTurnsToStone(GameTestHelper helper) {
        Troll troll = helper.spawn(NorseEntities.TROLL.get(), new BlockPos(1, 2, 1));
        BlockPos feet = troll.blockPosition();
        troll.petrify();
        helper.assertTrue(troll.isRemoved(), "a petrified troll should be gone");
        helper.assertTrue(helper.getLevel().getBlockState(feet).is(Blocks.MOSSY_COBBLESTONE), "the troll should leave a statue");
        var tusks = helper.getLevel().getEntitiesOfClass(ItemEntity.class, new AABB(feet).inflate(4.0),
                item -> item.getItem().is(NorseContent.TROLL_TUSK.get()));
        helper.assertTrue(tusks.size() == 1, "a petrified troll should leave its tusk");
        tusks.forEach(ItemEntity::discard);
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void gleipnirBindsFenrir(GameTestHelper helper) {
        Fenrir fenrir = helper.spawn(NorseEntities.FENRIR.get(), new BlockPos(1, 2, 1));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        ItemStack gleipnir = new ItemStack(NorseContent.GLEIPNIR.get());
        player.setItemInHand(InteractionHand.MAIN_HAND, gleipnir);
        fenrir.hurt(helper.getLevel().damageSources().generic(), 10.0F);
        float freeLoss = fenrir.getMaxHealth() - fenrir.getHealth();
        gleipnir.interactLivingEntity(player, fenrir, InteractionHand.MAIN_HAND);
        helper.assertTrue(fenrir.isBound(), "Gleipnir should bind Fenrir");
        helper.assertTrue(!fenrir.bind(), "he cannot be bound twice at once");
        float before = fenrir.getHealth();
        fenrir.invulnerableTime = 0;
        fenrir.hurt(helper.getLevel().damageSources().generic(), 10.0F);
        helper.assertTrue(before - fenrir.getHealth() > freeLoss, "a bound Fenrir should take more damage");
        fenrir.discard();
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void mjolnirCallsLightning(GameTestHelper helper) {
        BlockPos target = helper.absolutePos(new BlockPos(1, 1, 1));
        MjolnirItem.strike(helper.getLevel(), target, null);
        var bolts = helper.getLevel().getEntitiesOfClass(LightningBolt.class, new AABB(target).inflate(3.0));
        helper.assertTrue(!bolts.isEmpty(), "Mjolnir should call down lightning");
        bolts.forEach(LightningBolt::discard);
        helper.succeed();
    }

    /** Every kind of Norse merchant has trades, and the dwarven smith sells Gleipnir. */
    @GameTest(template = "empty")
    public static void norseMerchantsTrade(GameTestHelper helper) {
        boolean sellsGleipnir = false;
        for (int kind = 0; kind < NorseMerchant.KINDS; kind++) {
            NorseMerchant merchant = helper.spawn(NorseEntities.NORSE_MERCHANT.get(), new BlockPos(1, 2, 1));
            merchant.setKind(kind);
            var offers = merchant.getOffers();
            helper.assertTrue(!offers.isEmpty(), "merchant kind " + kind + " has no trades");
            for (var offer : offers) {
                sellsGleipnir |= offer.getResult().is(NorseContent.GLEIPNIR.get());
            }
            merchant.discard();
        }
        helper.assertTrue(sellsGleipnir, "nobody sells Gleipnir");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void sagaShowsWhatWasFound(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var entries = Journal.volume("norse");
        helper.assertTrue(entries.size() > 20, "the saga of Jotunheim has only " + entries.size() + " entries");
        int fresh = Journal.book("norse", player, false).pages().size();
        int complete = Journal.book("norse", player, true).pages().size();
        PlayerData.addEntry(player, "norse.fenrir");
        int afterFenrir = Journal.book("norse", player, false).pages().size();
        helper.assertTrue(complete > afterFenrir && afterFenrir > fresh, "pages: new " + fresh + ", after Fenrir " + afterFenrir
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
