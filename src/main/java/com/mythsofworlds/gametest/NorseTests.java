package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.journal.Journal;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.norse.NorseEntities;
import com.mythsofworlds.mythology.norse.entity.Draugr;
import com.mythsofworlds.mythology.norse.entity.Fenrir;
import com.mythsofworlds.mythology.norse.entity.Garm;
import com.mythsofworlds.mythology.norse.entity.Heimdall;
import com.mythsofworlds.mythology.norse.entity.NorseMerchant;
import com.mythsofworlds.mythology.norse.entity.Surtr;
import com.mythsofworlds.mythology.norse.entity.Thrym;
import com.mythsofworlds.mythology.norse.entity.Troll;
import com.mythsofworlds.mythology.norse.entity.Valkyrie;
import com.mythsofworlds.mythology.norse.item.MjolnirItem;
import com.mythsofworlds.mythology.relic.ArmourSets;
import com.mythsofworlds.mythology.relic.RelicArmorItem;
import com.mythsofworlds.registry.MetalSet;
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
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.Arrow;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraft.world.item.crafting.SingleRecipeInput;
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

    /** What each lord of the Nine Worlds fears: Gleipnir, Thor's hammer, a frost heart, fire. */
    @GameTest(template = "empty")
    public static void norseBossesHaveWeaknesses(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var sources = helper.getLevel().damageSources();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
        Fenrir fenrir = helper.spawn(NorseEntities.FENRIR.get(), new BlockPos(1, 2, 1));
        float freeLoss = loss(fenrir, sources.playerAttack(player), 40.0F);
        fenrir.bind();
        float boundLoss = loss(fenrir, sources.playerAttack(player), 40.0F);
        helper.assertTrue(boundLoss > freeLoss * 4.0F, "a free Fenrir lost " + freeLoss + ", a bound one " + boundLoss);
        fenrir.discard();

        Thrym thrym = helper.spawn(NorseEntities.THRYM.get(), new BlockPos(1, 2, 1));
        float swordLoss = loss(thrym, sources.playerAttack(player), 20.0F);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(NorseContent.MJOLNIR.get()));
        float hammerLoss = loss(thrym, sources.playerAttack(player), 20.0F);
        helper.assertTrue(hammerLoss > swordLoss * 2.5F, "Thrym lost " + swordLoss + " to a sword, " + hammerLoss + " to Mjolnir");
        thrym.discard();

        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
        Surtr surtr = helper.spawn(NorseEntities.SURTR.get(), new BlockPos(1, 2, 1));
        float bluntLoss = loss(surtr, sources.playerAttack(player), 20.0F);
        player.setItemInHand(InteractionHand.OFF_HAND, new ItemStack(NorseContent.FROST_HEART.get()));
        float frostLoss = loss(surtr, sources.playerAttack(player), 20.0F);
        helper.assertTrue(frostLoss > bluntLoss * 1.5F, "Surtr lost " + bluntLoss + " without a frost heart, " + frostLoss + " with one");
        surtr.discard();

        Garm garm = helper.spawn(NorseEntities.GARM.get(), new BlockPos(1, 2, 1));
        float coldLoss = loss(garm, sources.playerAttack(player), 20.0F);
        garm.igniteForSeconds(10.0F);
        float burningLoss = loss(garm, sources.playerAttack(player), 20.0F);
        helper.assertTrue(burningLoss > coldLoss * 1.5F, "Garm lost " + coldLoss + " cold, " + burningLoss + " burning");
        garm.discard();
        helper.succeed();
    }

    private static float loss(Mob mob, DamageSource source, float amount) {
        mob.setHealth(mob.getMaxHealth());
        mob.invulnerableTime = 0;
        mob.hurt(source, amount);
        return mob.getMaxHealth() - mob.getHealth();
    }

    /** A valkyrie is courted like an amazon, with northern gifts, and mead brings a valkyrie daughter. */
    @GameTest(template = "empty")
    public static void valkyrieMarriesAndHasADaughter(GameTestHelper helper) {
        Valkyrie valkyrie = helper.spawn(NorseEntities.VALKYRIE.get(), new BlockPos(1, 2, 1));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.POPPY));
        valkyrie.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(valkyrie.affection(player) == 0 && !player.getMainHandItem().isEmpty(), "flowers leave a valkyrie cold");
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(NorseContent.FENRIR_FANG.get()));
        valkyrie.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(valkyrie.affection(player) >= 25, "Fenrir's fang should win her, affection " + valkyrie.affection(player));
        valkyrie.setAffection(player, Amazon.LOVE);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.WEDDING_RING.get()));
        valkyrie.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(valkyrie.bond() == Amazon.Bond.WIFE && valkyrie.isFamily(player), "she should accept the ring");
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(NorseContent.MEAD.get()));
        valkyrie.mobInteract(player, InteractionHand.MAIN_HAND);
        var daughters = helper.getLevel().getEntitiesOfClass(Valkyrie.class, valkyrie.getBoundingBox().inflate(3.0),
                v -> v.isBaby() && v.bond() == Amazon.Bond.DAUGHTER && v.isFamily(player));
        helper.assertTrue(daughters.size() == 1, "mead should bring one valkyrie daughter, got " + daughters.size());
        helper.assertTrue(daughters.get(0).textureName().startsWith("valkyrie_"), "the daughter should look like a valkyrie");
        PlayerData.setSpouse(player, java.util.Optional.empty());
        daughters.forEach(Valkyrie::discard);
        valkyrie.discard();
        helper.succeed();
    }

    /** Orichalcum and dark iron: ores in the worlds, ingots from the furnace, gear better than iron; the new fuels. */
    @GameTest(template = "empty")
    public static void metalsAndFuels(GameTestHelper helper) {
        var level = helper.getLevel();
        var placed = level.registryAccess().registryOrThrow(Registries.PLACED_FEATURE);
        for (String feature : List.of("ore_orichalcum", "ore_hephaestus_coal", "ore_dark_iron", "ore_muspel_ember")) {
            helper.assertTrue(placed.containsKey(MythsOfWorlds.id(feature)), "placed feature " + feature + " did not load");
        }
        for (MetalSet metal : List.of(GreekContent.ORICHALCUM, NorseContent.DARK_IRON)) {
            helper.assertTrue(metal.ore.get().defaultBlockState().requiresCorrectToolForDrops(), metal.name + " ore needs a pickaxe");
            ItemStack ingot = level.getRecipeManager()
                    .getRecipeFor(RecipeType.SMELTING, new SingleRecipeInput(new ItemStack(metal.raw.get())), level)
                    .map(recipe -> recipe.value().getResultItem(level.registryAccess())).orElse(ItemStack.EMPTY);
            helper.assertTrue(ingot.is(metal.ingot.get()), "raw " + metal.name + " should smelt into an ingot, got " + ingot);
            helper.assertTrue(metal.tier.getUses() > Tiers.IRON.getUses() && metal.tier.getSpeed() >= Tiers.IRON.getSpeed(),
                    metal.name + " tools should beat iron");
            int chest = metal.material.value().getDefense(ArmorItem.Type.CHESTPLATE);
            helper.assertTrue(chest > 6, metal.name + " chestplate gives only " + chest);
            helper.assertTrue(new ItemStack(metal.chestplate.get()).getMaxDamage() > new ItemStack(Items.IRON_CHESTPLATE).getMaxDamage(),
                    metal.name + " armour should outlast iron");
        }
        int coal = new ItemStack(Items.COAL).getBurnTime(RecipeType.SMELTING);
        int hephaestus = new ItemStack(GreekContent.HEPHAESTUS_COAL.get()).getBurnTime(RecipeType.SMELTING);
        int ember = new ItemStack(NorseContent.MUSPEL_EMBER.get()).getBurnTime(RecipeType.SMELTING);
        helper.assertTrue(hephaestus == coal * 2 && ember == coal * 3, "burn times: coal " + coal + ", Hephaestus coal "
                + hephaestus + ", Muspel ember " + ember);
        helper.succeed();
    }

    /** Mjolnir's lightning melts sand into glass and chars soil into scorched earth. */
    @GameTest(template = "empty")
    public static void mjolnirScorchesTheGround(GameTestHelper helper) {
        BlockPos sand = new BlockPos(1, 1, 1);
        BlockPos grass = new BlockPos(2, 1, 1);
        helper.setBlock(sand, Blocks.SAND);
        helper.setBlock(grass, Blocks.GRASS_BLOCK);
        helper.setBlock(sand.above(), Blocks.AIR);
        helper.setBlock(grass.above(), Blocks.AIR);
        MjolnirItem.scorch(helper.getLevel(), helper.absolutePos(sand.above()));
        helper.assertBlockPresent(Blocks.GLASS, sand);
        helper.assertBlockPresent(NorseContent.SCORCHED_EARTH.get(), grass);
        helper.succeed();
    }

    /** Heimdall sees arrows coming: they hurt him a third as much as a blow. */
    @GameTest(template = "empty")
    public static void heimdallSeesArrowsComing(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var sources = helper.getLevel().damageSources();
        Heimdall heimdall = helper.spawn(NorseEntities.HEIMDALL.get(), new BlockPos(1, 2, 1));
        float blowLoss = loss(heimdall, sources.playerAttack(player), 30.0F);
        Arrow arrow = EntityType.ARROW.create(helper.getLevel());
        float arrowLoss = loss(heimdall, sources.arrow(arrow, player), 30.0F);
        helper.assertTrue(arrowLoss < blowLoss * 0.5F, "an arrow took " + arrowLoss + ", a blow " + blowLoss);
        heimdall.discard();
        helper.succeed();
    }

    /** Relics give their powers, and armour of two mythologies makes a set. */
    @GameTest(template = "empty")
    public static void armourOfTheGods(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemSlot(EquipmentSlot.HEAD, new ItemStack(NorseContent.HEIMDALL_HELMET.get()));
        player.setItemSlot(EquipmentSlot.FEET, new ItemStack(GreekContent.TALARIA.get()));
        player.fallDistance = 10.0F;
        for (EquipmentSlot slot : List.of(EquipmentSlot.HEAD, EquipmentSlot.FEET)) {
            ((RelicArmorItem) player.getItemBySlot(slot).getItem()).wornTick(player);
        }
        helper.assertTrue(player.hasEffect(MobEffects.NIGHT_VISION), "the helmet of Heimdall gives night vision");
        helper.assertTrue(player.hasEffect(MobEffects.MOVEMENT_SPEED) && player.fallDistance == 0.0F,
                "the talaria give speed and stop falls");
        ArmourSets.apply(player);
        helper.assertTrue(player.hasEffect(MobEffects.DIG_SPEED), "a Greek and a Norse piece make a set: haste");
        helper.assertTrue(!player.hasEffect(MobEffects.FIRE_RESISTANCE), "two pieces give no fire resistance yet");
        player.setItemSlot(EquipmentSlot.CHEST, new ItemStack(GreekContent.TITAN_BREASTPLATE.get()));
        player.setItemSlot(EquipmentSlot.LEGS, new ItemStack(NorseContent.DARK_IRON.leggings.get()));
        ArmourSets.apply(player);
        helper.assertTrue(player.hasEffect(MobEffects.FIRE_RESISTANCE) && player.hasEffect(MobEffects.REGENERATION)
                && player.hasEffect(MobEffects.DAMAGE_RESISTANCE), "two and two give the full union of the pantheons");
        int[] counts = ArmourSets.count(player);
        helper.assertTrue(counts[0] == 2 && counts[1] == 2, "counted " + counts[0] + " Greek and " + counts[1] + " Norse");
        helper.succeed();
    }
}
