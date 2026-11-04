package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.journal.Journal;
import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import com.mythsofworlds.mythology.egyptian.block.Pyramid;
import com.mythsofworlds.mythology.egyptian.block.PyramidGateBlock;
import com.mythsofworlds.mythology.egyptian.entity.Apep;
import com.mythsofworlds.mythology.egyptian.entity.BastetCat;
import com.mythsofworlds.mythology.egyptian.entity.Crocodile;
import com.mythsofworlds.mythology.egyptian.entity.EgyptianMerchant;
import com.mythsofworlds.mythology.egyptian.entity.IsisGod;
import com.mythsofworlds.mythology.egyptian.entity.Mummy;
import com.mythsofworlds.mythology.egyptian.entity.OsirisGod;
import com.mythsofworlds.mythology.egyptian.entity.PharaohMummy;
import com.mythsofworlds.mythology.egyptian.entity.Priestess;
import com.mythsofworlds.mythology.egyptian.entity.Scorpion;
import com.mythsofworlds.mythology.egyptian.entity.SetGod;
import com.mythsofworlds.mythology.egyptian.entity.Sphinx;
import com.mythsofworlds.mythology.egyptian.entity.TravelersBoat;
import com.mythsofworlds.mythology.egyptian.item.HapiGiftItem;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.relic.ArmourSets;
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
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Biomes;
import net.minecraft.world.level.biome.FeatureSorter;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.CropBlock;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/**
 * Egyptian content: the pyramid and its gate, data files, structures, mobs, the weaknesses of the bosses, the
 * priestesses of Isis, the cats of Bastet and the Book of the Dead.
 */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class EgyptianTests {
    @GameTest(template = "empty")
    public static void duatBiomesLoadInOrder(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        List<Holder<Biome>> duat = new ArrayList<>();
        for (String biome : EgyptianContent.BIOMES) {
            helper.assertTrue(biomes.containsKey(MythsOfWorlds.id(biome)), "worldgen/biome/" + biome + ".json did not load");
            duat.add(biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME, MythsOfWorlds.id(biome))));
        }
        FeatureSorter.buildFeaturesPerStep(duat, holder -> holder.value().getGenerationSettings().features(), true);
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void egyptianStructuresLoad(GameTestHelper helper) throws Exception {
        var server = helper.getLevel().getServer();
        var structures = helper.getLevel().registryAccess().registryOrThrow(Registries.STRUCTURE);
        for (String name : EgyptianContent.STRUCTURES) {
            helper.assertTrue(structures.containsKey(MythsOfWorlds.id(name)), "worldgen/structure/" + name + ".json did not load");
            ResourceLocation template = MythsOfWorlds.id("egyptian/" + name);
            helper.assertTrue(server.getStructureManager().get(template).isPresent(), "template " + template + " missing");
            Resource file = server.getResourceManager().getResourceOrThrow(MythsOfWorlds.id("structure/egyptian/" + name + ".nbt"));
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
    public static void everyEgyptianMobSpawns(GameTestHelper helper) {
        for (var type : EgyptianEntities.all()) {
            Mob mob = helper.spawn(type.get(), new BlockPos(1, 2, 1));
            helper.assertTrue(mob.isAlive() && mob.getHealth() > 0, type.getId() + " did not spawn alive");
            mob.discard();
        }
        helper.succeed();
    }

    /** Builds the 5x5, 3x3 and gold pyramid by hand at {@code base} (centre of the base), doorway to the south. */
    private static void buildByHand(ServerLevel level, BlockPos base) {
        int flags = Block.UPDATE_ALL;
        for (int dx = -2; dx <= 2; dx++) {
            for (int dz = -2; dz <= 2; dz++) {
                level.setBlock(base.offset(dx, -1, dz), Blocks.SANDSTONE.defaultBlockState(), flags);
                if (!(dx == 0 && dz == 2)) {
                    level.setBlock(base.offset(dx, 0, dz), EgyptianContent.PYRAMID_STONE.get().defaultBlockState(), flags);
                }
                if (Math.abs(dx) <= 1 && Math.abs(dz) <= 1) {
                    level.setBlock(base.offset(dx, 1, dz), EgyptianContent.HIEROGLYPH_STONE.get().defaultBlockState(), flags);
                }
            }
        }
        level.setBlock(base.above(2), Blocks.GOLD_BLOCK.defaultBlockState(), flags);
    }

    private static void clear(ServerLevel level, BlockPos base) {
        BlockPos.betweenClosed(base.offset(-4, -1, -4), base.offset(4, 4, 4))
                .forEach(pos -> level.setBlock(pos, Blocks.AIR.defaultBlockState(), Block.UPDATE_CLIENTS));
    }

    /**
     * A pyramid built by hand is found from any of its blocks; the ankh opens a two-block gate in the doorway facing
     * out; the gate is found again; and it fades when the stone beside it is broken. Without the golden capstone it
     * is no pyramid. Built high above the test area.
     */
    @GameTest(template = "empty")
    public static void ankhOpensThePyramid(GameTestHelper helper) {
        ServerLevel level = helper.getLevel();
        BlockPos corner = helper.absolutePos(BlockPos.ZERO);
        BlockPos base = new BlockPos(corner.getX(), 210, corner.getZ());
        buildByHand(level, base);
        level.setBlock(base.above(2), Blocks.SANDSTONE.defaultBlockState(), Block.UPDATE_ALL);
        helper.assertTrue(Pyramid.find(level, base.offset(1, 0, -1)) == null, "without the benben it is no pyramid");
        level.setBlock(base.above(2), Blocks.GOLD_BLOCK.defaultBlockState(), Block.UPDATE_ALL);
        Pyramid.Gate gate = Pyramid.find(level, base.offset(-2, 0, 1));
        helper.assertTrue(gate != null && gate.facing() == Direction.SOUTH && gate.lower().equals(base.south(2)),
                "the doorway faces south, got " + gate);
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        ItemStack ankh = new ItemStack(EgyptianContent.ANKH.get());
        player.setItemInHand(InteractionHand.MAIN_HAND, ankh);
        var hit = new net.minecraft.world.phys.BlockHitResult(net.minecraft.world.phys.Vec3.atCenterOf(base.offset(1, 1, 0)),
                Direction.UP, base.offset(1, 1, 0), false);
        ankh.useOn(new net.minecraft.world.item.context.UseOnContext(player, InteractionHand.MAIN_HAND, hit));
        for (BlockPos pos : new BlockPos[]{gate.lower(), gate.lower().above()}) {
            var state = level.getBlockState(pos);
            helper.assertTrue(state.is(EgyptianContent.PYRAMID_GATE.get()) && state.getValue(PyramidGateBlock.FACING) == Direction.SOUTH,
                    "a gate facing south at " + pos);
        }
        helper.assertTrue(ankh.getDamageValue() == 1, "opening the gate costs one use of the ankh");
        helper.assertTrue(gate.lower().equals(Pyramid.findGate(level, base.offset(6, 0, 6))), "the gate is found again");
        level.setBlock(gate.lower().east(), Blocks.AIR.defaultBlockState(), Block.UPDATE_ALL);
        helper.assertTrue(!level.getBlockState(gate.lower()).is(EgyptianContent.PYRAMID_GATE.get()), "breaking the stone closes the gate");
        clear(level, base);
        helper.succeed();
    }

    /** The pyramid built for an arrival is whole: the gate stands in it, and Pyramid.check recognises it. */
    @GameTest(template = "empty")
    public static void arrivalPyramidIsWhole(GameTestHelper helper) {
        ServerLevel level = helper.getLevel();
        BlockPos corner = helper.absolutePos(BlockPos.ZERO);
        BlockPos base = new BlockPos(corner.getX(), 220, corner.getZ());
        Pyramid.Gate gate = Pyramid.build(level, base, Direction.SOUTH);
        helper.assertTrue(level.getBlockState(gate.lower().above()).is(EgyptianContent.PYRAMID_GATE.get()), "the gate is two blocks high");
        Pyramid.Gate found = Pyramid.check(level, base.above(2));
        helper.assertTrue(found != null && found.lower().equals(gate.lower()), "the built pyramid is a real pyramid");
        helper.assertTrue(level.getBlockState(gate.lower().south()).isAir(), "the doorstep is free");
        clear(level, base);
        helper.succeed();
    }

    /** Set takes only a quarter of the harm from a hero without the eye of Horus, and full harm from one who has it. */
    @GameTest(template = "empty")
    public static void setFearsTheEyeOfHorus(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var sources = helper.getLevel().damageSources();
        SetGod set = helper.spawn(EgyptianEntities.SET.get(), new BlockPos(1, 2, 1));
        float before = set.getHealth();
        set.hurt(sources.playerAttack(player), 40.0F);
        float without = before - set.getHealth();
        player.getInventory().add(new ItemStack(EgyptianContent.EYE_OF_HORUS.get()));
        set.invulnerableTime = 0;
        before = set.getHealth();
        set.hurt(sources.playerAttack(player), 40.0F);
        float with = before - set.getHealth();
        helper.assertTrue(with > without * 2.5F, "the eye of Horus should let the blow through: " + without + " then " + with);
        helper.assertTrue(SetGod.carriesEye(player), "the eye is carried");
        set.discard();
        helper.succeed();
    }

    /** Apep takes little harm from a hero alone, more with a cat of Bastet by their side, and the cat's bite most. */
    @GameTest(template = "empty")
    public static void apepFearsTheCatsOfBastet(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var sources = helper.getLevel().damageSources();
        player.moveTo(helper.absoluteVec(new net.minecraft.world.phys.Vec3(4.5, 2.0, 4.5)));
        Apep apep = helper.spawnWithNoFreeWill(EgyptianEntities.APEP.get(), 1, 2, 1);
        float before = apep.getHealth();
        apep.hurt(sources.playerAttack(player), 40.0F);
        float alone = before - apep.getHealth();
        helper.assertTrue(!Apep.hasCat(player), "no cat yet");
        BastetCat cat = helper.spawnWithNoFreeWill(EgyptianEntities.BASTET_CAT.get(), 3, 2, 3);
        cat.tame(player);
        helper.assertTrue(Apep.hasCat(player), "the tame cat of Bastet is by the hero's side");
        apep.invulnerableTime = 0;
        before = apep.getHealth();
        apep.hurt(sources.playerAttack(player), 40.0F);
        float withCat = before - apep.getHealth();
        helper.assertTrue(withCat > alone * 2.0F, "a cat by the hero's side lets the blow through: " + alone + " then " + withCat);
        apep.invulnerableTime = 0;
        before = apep.getHealth();
        apep.hurt(sources.mobAttack(cat), 10.0F);
        helper.assertTrue(before - apep.getHealth() > 10.0F * 2.0F, "the cat's bite tears the serpent");
        cat.discard();
        apep.discard();
        helper.succeed();
    }

    /** The Sphinx is stone: arrows barely scratch it, a pickaxe breaks it; it does not attack first. */
    @GameTest(template = "empty")
    public static void sphinxIsStone(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        Sphinx sphinx = helper.spawnWithNoFreeWill(EgyptianEntities.SPHINX.get(), 1, 2, 1);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_SWORD));
        float before = sphinx.getHealth();
        sphinx.hurt(helper.getLevel().damageSources().playerAttack(player), 20.0F);
        float sword = before - sphinx.getHealth();
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.IRON_PICKAXE));
        sphinx.invulnerableTime = 0;
        before = sphinx.getHealth();
        sphinx.hurt(helper.getLevel().damageSources().playerAttack(player), 20.0F);
        float pickaxe = before - sphinx.getHealth();
        helper.assertTrue(pickaxe > sword * 1.5F, "a pickaxe breaks the stone: sword " + sword + ", pickaxe " + pickaxe);
        sphinx.discard();
        helper.succeed();
    }

    /** The curse of the pharaoh's tomb slows the work of whoever stands near; fire burns his wrappings twice. */
    @GameTest(template = "empty")
    public static void pharaohCursesAndBurns(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.moveTo(helper.absoluteVec(new net.minecraft.world.phys.Vec3(3.5, 2.0, 3.5)));
        PharaohMummy pharaoh = helper.spawnWithNoFreeWill(EgyptianEntities.PHARAOH_MUMMY.get(), 1, 2, 1);
        pharaoh.curse(player);
        helper.assertTrue(player.hasEffect(MobEffects.DIG_SLOWDOWN), "the curse slows the hero's work");
        Mummy mummy = helper.spawnWithNoFreeWill(EgyptianEntities.MUMMY.get(), 2, 2, 2);
        float before = mummy.getHealth();
        mummy.hurt(helper.getLevel().damageSources().inFire(), 4.0F);
        helper.assertTrue(before - mummy.getHealth() > 6.0F, "fire burns a mummy twice, took " + (before - mummy.getHealth()));
        mummy.discard();
        pharaoh.discard();
        helper.succeed();
    }

    /** Every kind of trader has trades, and the priest of Anubis sells the ankh and the eye of Horus. */
    @GameTest(template = "empty")
    public static void egyptianMerchantsTrade(GameTestHelper helper) {
        boolean ankh = false, eye = false;
        for (int kind = 0; kind < EgyptianMerchant.KINDS; kind++) {
            EgyptianMerchant merchant = helper.spawn(EgyptianEntities.EGYPTIAN_MERCHANT.get(), new BlockPos(1, 2, 1));
            merchant.setKind(kind);
            var offers = merchant.getOffers();
            helper.assertTrue(!offers.isEmpty(), "trader kind " + kind + " has no trades");
            for (var offer : offers) {
                ankh |= kind == EgyptianMerchant.PRIEST && offer.getResult().is(EgyptianContent.ANKH.get());
                eye |= offer.getResult().is(EgyptianContent.EYE_OF_HORUS.get());
            }
            merchant.discard();
        }
        helper.assertTrue(ankh && eye, "the priest sells the ankh: " + ankh + ", someone sells the eye: " + eye);
        helper.succeed();
    }

    /** A priestess of Isis loves lapis and gold; she takes the ring, and a honey cake brings a daughter. */
    @GameTest(template = "empty")
    public static void priestessMarriesAndHasADaughter(GameTestHelper helper) {
        Priestess priestess = helper.spawn(EgyptianEntities.PRIESTESS.get(), new BlockPos(1, 2, 1));
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(Items.LAPIS_BLOCK));
        priestess.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(priestess.affection(player) >= 40, "a block of lapis should please her, affection " + priestess.affection(player));
        priestess.setAffection(player, Amazon.LOVE);
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(GreekContent.WEDDING_RING.get()));
        priestess.mobInteract(player, InteractionHand.MAIN_HAND);
        helper.assertTrue(priestess.bond() == Amazon.Bond.WIFE && priestess.isFamily(player), "she should accept the ring");
        player.setItemInHand(InteractionHand.MAIN_HAND, new ItemStack(EgyptianContent.HONEY_CAKE.get()));
        priestess.mobInteract(player, InteractionHand.MAIN_HAND);
        var daughters = helper.getLevel().getEntitiesOfClass(Priestess.class, priestess.getBoundingBox().inflate(3.0),
                p -> p.isBaby() && p.bond() == Amazon.Bond.DAUGHTER && p.isFamily(player));
        helper.assertTrue(daughters.size() == 1, "a honey cake should bring one daughter, got " + daughters.size());
        helper.assertTrue(daughters.get(0).textureName().startsWith("priestess_"), "the daughter should look like a priestess");
        helper.assertTrue(priestess.horn() == EgyptianContent.SISTRUM.get(), "priestesses answer the sistrum");
        PlayerData.setSpouse(player, java.util.Optional.empty());
        daughters.forEach(Priestess::discard);
        priestess.discard();
        helper.succeed();
    }

    /** A tame cat of Bastet blesses its master with Regeneration; mummies keep away from it. */
    @GameTest(template = "empty")
    public static void catOfBastetBlessesItsMaster(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        player.moveTo(helper.absoluteVec(new net.minecraft.world.phys.Vec3(2.5, 2.0, 2.5)));
        BastetCat cat = helper.spawn(EgyptianEntities.BASTET_CAT.get(), new BlockPos(1, 2, 1));
        cat.tame(player);
        helper.assertTrue(cat.isTame() && player.getUUID().equals(cat.getOwnerUUID()), "the cat is tamed");
        helper.assertTrue(cat.bless(player), "the master is near");
        helper.assertTrue(player.hasEffect(MobEffects.REGENERATION), "the cat of Bastet should bless its master");
        player.moveTo(cat.getX() + 40.0, cat.getY(), cat.getZ());
        helper.assertTrue(!cat.bless(player), "a master far away is not blessed");
        cat.discard();
        helper.succeed();
    }

    /** Four pieces of meteoric iron and the relics count as Egyptian and give the blessing of Ra. */
    @GameTest(template = "empty")
    public static void blessingOfRa(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var iron = EgyptianContent.METEORIC_IRON;
        player.setItemSlot(EquipmentSlot.HEAD, new ItemStack(EgyptianContent.NEMES.get()));
        player.setItemSlot(EquipmentSlot.CHEST, new ItemStack(EgyptianContent.PECTORAL_OF_RA.get()));
        player.setItemSlot(EquipmentSlot.LEGS, new ItemStack(iron.leggings.get()));
        player.setItemSlot(EquipmentSlot.FEET, new ItemStack(iron.boots.get()));
        helper.assertTrue(ArmourSets.count(player)[3] == 4, "four Egyptian pieces, counted " + ArmourSets.count(player)[3]);
        ArmourSets.apply(player);
        helper.assertTrue(player.hasEffect(MobEffects.FIRE_RESISTANCE) && player.hasEffect(MobEffects.DIG_SPEED),
                "the blessing of Ra gives fire resistance and haste");
        helper.succeed();
    }

    @GameTest(template = "empty")
    public static void bookOfTheDeadShowsWhatWasFound(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        var entries = Journal.volume("egyptian");
        helper.assertTrue(entries.size() > 15, "the Book of the Dead has only " + entries.size() + " entries");
        int fresh = Journal.book("egyptian", player, false).pages().size();
        int complete = Journal.book("egyptian", player, true).pages().size();
        PlayerData.addEntry(player, "egyptian.apep");
        int afterApep = Journal.book("egyptian", player, false).pages().size();
        helper.assertTrue(complete > afterApep && afterApep > fresh, "pages: new " + fresh + ", after Apep " + afterApep
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

    /** Osiris rises once from a death blow with half his health; the second death blow is the last. */
    @GameTest(template = "empty")
    public static void osirisRisesOnce(GameTestHelper helper) {
        OsirisGod osiris = helper.spawn(EgyptianEntities.OSIRIS.get(), new BlockPos(1, 2, 1));
        osiris.hurt(helper.getLevel().damageSources().generic(), 10000.0F);
        helper.assertTrue(osiris.isAlive() && osiris.reborn(), "Osiris should rise from the first death blow");
        helper.assertTrue(Math.abs(osiris.getHealth() - osiris.getMaxHealth() / 2.0F) < 0.01F, "he rises with half his health");
        osiris.invulnerableTime = 0;
        osiris.hurt(helper.getLevel().damageSources().generic(), 10000.0F);
        helper.assertTrue(!osiris.isAlive() || osiris.getHealth() <= 0.0F, "the second death blow is the last");
        osiris.discard();
        helper.succeed();
    }

    /** The gift of Hapi feeds the wheat around it three times over, nearly or fully ripening a fresh field. */
    @GameTest(template = "empty")
    public static void giftOfHapiRipensTheField(GameTestHelper helper) {
        for (int x = 0; x < 3; x++) {
            helper.setBlock(new BlockPos(x, 1, 1), Blocks.FARMLAND);
            helper.setBlock(new BlockPos(x, 2, 1), Blocks.WHEAT);
        }
        int fed = HapiGiftItem.flood(helper.getLevel(), helper.absolutePos(new BlockPos(1, 2, 1)));
        helper.assertTrue(fed == 3, "three wheat plants should be fed, fed " + fed);
        for (int x = 0; x < 3; x++) {
            int age = helper.getBlockState(new BlockPos(x, 2, 1)).getValue(CropBlock.AGE);
            helper.assertTrue(age >= 6, "wheat at " + x + " only reached age " + age);
        }
        helper.succeed();
    }

    /** Every god of Egypt spawns with the weapon of its myth in hand and does not drop it. */
    @GameTest(template = "empty")
    public static void godsHoldTheirWeapons(GameTestHelper helper) {
        for (var type : EgyptianEntities.gods()) {
            Mob god = helper.spawn(type.get(), new BlockPos(1, 2, 1));
            god.tick();
            helper.assertTrue(!god.getMainHandItem().isEmpty(), type.getId() + " has nothing in hand");
            god.discard();
        }
        helper.succeed();
    }

    /** Isis speaks with her own voice: every sound she makes is one of ours, none a villager's or an illager's. */
    @GameTest(template = "empty")
    public static void isisHasHerOwnVoice(GameTestHelper helper) {
        IsisGod isis = helper.spawn(EgyptianEntities.ISIS.get(), new BlockPos(1, 2, 1));
        Player foe = helper.makeMockPlayer(GameType.SURVIVAL);
        List<SoundEvent> voice = new ArrayList<>(List.of(isis.getAmbientSound(), isis.getHurtSound(helper.getLevel().damageSources().generic()),
                isis.getDeathSound(), isis.answer()));
        isis.setTarget(foe);
        voice.add(isis.getAmbientSound());
        voice.add(isis.answer());
        List<SoundEvent> vanilla = List.of(SoundEvents.VILLAGER_AMBIENT, SoundEvents.VILLAGER_HURT, SoundEvents.VILLAGER_DEATH,
                SoundEvents.VILLAGER_YES, SoundEvents.VILLAGER_NO, SoundEvents.VILLAGER_TRADE, SoundEvents.VILLAGER_CELEBRATE,
                SoundEvents.EVOKER_AMBIENT, SoundEvents.EVOKER_HURT, SoundEvents.EVOKER_DEATH);
        for (SoundEvent sound : voice) {
            helper.assertTrue(sound != null && sound.getLocation().getNamespace().equals(MythsOfWorlds.MODID)
                    && sound.getLocation().getPath().startsWith("entity.isis."), "Isis plays " + (sound == null ? null : sound.getLocation()));
            helper.assertFalse(vanilla.contains(sound), "Isis plays a vanilla sound: " + sound.getLocation());
        }
        helper.assertTrue(voice.stream().map(SoundEvent::getLocation).distinct().count() == 6,
                "Isis should have six sounds of her own (idle, ambient, hurt, death, yes, no): " + voice);
        float low = Float.MAX_VALUE;
        float high = -Float.MAX_VALUE;
        for (int i = 0; i < 40; i++) {
            float pitch = isis.getVoicePitch();
            low = Math.min(low, pitch);
            high = Math.max(high, pitch);
        }
        helper.assertTrue(low < high && low > 0.9F && high < 1.1F, "her pitch should vary a little: " + low + ".." + high);
        isis.discard();
        helper.succeed();
    }

    /** A crocodile spawns only on the shore or in the shallows: within four blocks of water, never in deep water. */
    @GameTest(template = "empty")
    public static void crocodileSpawnsOnlyNearWater(GameTestHelper helper) {
        ServerLevel level = helper.getLevel();
        for (int x = 0; x <= 4; x++) {
            helper.setBlock(new BlockPos(x, 1, 1), Blocks.STONE);
            for (int y = 2; y <= 5; y++) {
                helper.setBlock(new BlockPos(x, y, 1), Blocks.AIR);
            }
        }
        BlockPos spot = helper.absolutePos(new BlockPos(0, 2, 1));
        helper.assertFalse(Crocodile.onShore(level, spot), "a crocodile spawned far from water");
        helper.setBlock(new BlockPos(4, 2, 1), Blocks.WATER);
        helper.assertTrue(Crocodile.onShore(level, spot), "no crocodile on the shore, four blocks from water");
        helper.setBlock(new BlockPos(4, 2, 1), Blocks.AIR);
        helper.setBlock(new BlockPos(2, 2, 1), Blocks.WATER);
        helper.assertTrue(Crocodile.onShore(level, helper.absolutePos(new BlockPos(2, 2, 1))), "no crocodile in shallow water");
        helper.setBlock(new BlockPos(2, 3, 1), Blocks.WATER);
        helper.setBlock(new BlockPos(2, 4, 1), Blocks.WATER);
        helper.assertFalse(Crocodile.onShore(level, helper.absolutePos(new BlockPos(2, 2, 1))), "a crocodile spawned in deep water");
        var biomes = level.registryAccess().registryOrThrow(Registries.BIOME);
        TagKey<Biome> crocodileBiomes = TagKey.create(Registries.BIOME, MythsOfWorlds.id("spawns/crocodile"));
        helper.assertTrue(biomes.getHolderOrThrow(Biomes.RIVER).is(crocodileBiomes), "no crocodiles by rivers");
        helper.assertTrue(biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME, MythsOfWorlds.id("nile_banks"))).is(crocodileBiomes),
                "no crocodiles on the banks of the Nile");
        for (ResourceKey<Biome> dry : List.of(Biomes.DEEP_OCEAN, Biomes.OCEAN, Biomes.DESERT, Biomes.PLAINS)) {
            helper.assertFalse(biomes.getHolderOrThrow(dry).is(crocodileBiomes), "crocodiles in " + dry.location());
        }
        helper.succeed();
    }

    /** A scorpion spawns only in a desert-type biome, on sand or terracotta. */
    @GameTest(template = "empty")
    public static void scorpionSpawnsOnlyInDeserts(GameTestHelper helper) {
        var biomes = helper.getLevel().registryAccess().registryOrThrow(Registries.BIOME);
        var desert = biomes.getHolderOrThrow(Biomes.DESERT);
        var badlands = biomes.getHolderOrThrow(Biomes.BADLANDS);
        var duat = biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME, MythsOfWorlds.id("duat_sands")));
        helper.assertTrue(Scorpion.canSpawnAt(desert, Blocks.SAND.defaultBlockState()), "no scorpion on desert sand");
        helper.assertTrue(Scorpion.canSpawnAt(badlands, Blocks.ORANGE_TERRACOTTA.defaultBlockState()), "no scorpion on badlands terracotta");
        helper.assertTrue(Scorpion.canSpawnAt(duat, Blocks.RED_SAND.defaultBlockState()), "no scorpion in the sands of the Duat");
        helper.assertFalse(Scorpion.canSpawnAt(desert, Blocks.STONE.defaultBlockState()), "a scorpion on stone");
        for (ResourceKey<Biome> other : List.of(Biomes.PLAINS, Biomes.BEACH, Biomes.RIVER, Biomes.SWAMP, Biomes.JUNGLE)) {
            helper.assertFalse(Scorpion.canSpawnAt(biomes.getHolderOrThrow(other), Blocks.SAND.defaultBlockState()),
                    "a scorpion in " + other.location());
        }
        helper.assertFalse(Scorpion.canSpawnAt(biomes.getHolderOrThrow(ResourceKey.create(Registries.BIOME, MythsOfWorlds.id("nile_banks"))),
                Blocks.SAND.defaultBlockState()), "a scorpion on the green banks of the Nile");
        helper.succeed();
    }

    /** The traveler's boat is crafted from papyrus, linen and crocodile hide, carries two and breaks into itself. */
    @GameTest(template = "empty")
    public static void travelersBoatCraftsAndSeatsTwo(GameTestHelper helper) {
        var recipe = helper.getLevel().getRecipeManager().byKey(MythsOfWorlds.id("travelers_boat"));
        helper.assertTrue(recipe.isPresent() && recipe.get().value().getResultItem(helper.getLevel().registryAccess())
                .is(EgyptianContent.TRAVELERS_BOAT.get()), "no recipe for the traveler's boat");
        TravelersBoat boat = helper.spawn(EgyptianEntities.TRAVELERS_BOAT.get(), new BlockPos(1, 2, 1));
        helper.assertTrue(boat.getDropItem() == EgyptianContent.TRAVELERS_BOAT.get(), "the boat does not break into itself");
        Player first = helper.makeMockPlayer(GameType.SURVIVAL);
        Player second = helper.makeMockPlayer(GameType.SURVIVAL);
        Player third = helper.makeMockPlayer(GameType.SURVIVAL);
        helper.assertTrue(first.startRiding(boat) && second.startRiding(boat), "two cannot ride the boat");
        helper.assertFalse(third.startRiding(boat), "a third rides the boat");
        helper.assertTrue(boat.getControllingPassenger() == first, "the first aboard does not steer");
        boat.ejectPassengers();
        boat.discard();
        helper.succeed();
    }
}
