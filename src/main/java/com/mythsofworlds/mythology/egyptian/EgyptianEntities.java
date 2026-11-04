package com.mythsofworlds.mythology.egyptian;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.egyptian.entity.AnubisGod;
import com.mythsofworlds.mythology.egyptian.entity.Apep;
import com.mythsofworlds.mythology.egyptian.entity.BastetCat;
import com.mythsofworlds.mythology.egyptian.entity.BastetGod;
import com.mythsofworlds.mythology.egyptian.entity.Crocodile;
import com.mythsofworlds.mythology.egyptian.entity.EgyptianMerchant;
import com.mythsofworlds.mythology.egyptian.entity.HathorGod;
import com.mythsofworlds.mythology.egyptian.entity.HorusGod;
import com.mythsofworlds.mythology.egyptian.entity.IsisGod;
import com.mythsofworlds.mythology.egyptian.entity.Jackal;
import com.mythsofworlds.mythology.egyptian.entity.Mummy;
import com.mythsofworlds.mythology.egyptian.entity.OsirisGod;
import com.mythsofworlds.mythology.egyptian.entity.PharaohMummy;
import com.mythsofworlds.mythology.egyptian.entity.Priestess;
import com.mythsofworlds.mythology.egyptian.entity.PtahGod;
import com.mythsofworlds.mythology.egyptian.entity.RaGod;
import com.mythsofworlds.mythology.egyptian.entity.Scarab;
import com.mythsofworlds.mythology.egyptian.entity.Scorpion;
import com.mythsofworlds.mythology.egyptian.entity.SekhmetGod;
import com.mythsofworlds.mythology.egyptian.entity.SetGod;
import com.mythsofworlds.mythology.egyptian.entity.SobekGod;
import com.mythsofworlds.mythology.egyptian.entity.Sphinx;
import com.mythsofworlds.mythology.egyptian.entity.ThothGod;
import com.mythsofworlds.mythology.egyptian.entity.Ushabti;
import java.util.List;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.levelgen.Heightmap;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import net.neoforged.neoforge.event.entity.RegisterSpawnPlacementsEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;

import static com.mythsofworlds.registry.ModRegistries.ENTITY_TYPES;
import static com.mythsofworlds.registry.ModRegistries.ITEMS;

/**
 * Creatures of the Duat. Which biomes they spawn in is set in data/mythsofworlds/worldgen/biome/*.json ("spawners"),
 * for crocodiles and scorpions by biome modifiers (data/mythsofworlds/neoforge/biome_modifier);
 * bosses wait in their structures (data/mythsofworlds/structure/egyptian). Renderers are in the client package.
 */
public final class EgyptianEntities {
    // ---- Creatures ----
    public static final DeferredHolder<EntityType<?>, EntityType<Mummy>> MUMMY = register("mummy",
            EntityType.Builder.of(Mummy::new, MobCategory.MONSTER).sized(0.6F, 1.95F).eyeHeight(1.74F));
    public static final DeferredHolder<EntityType<?>, EntityType<Scarab>> SCARAB = register("scarab",
            EntityType.Builder.of(Scarab::new, MobCategory.MONSTER).sized(0.6F, 0.4F).eyeHeight(0.25F));
    public static final DeferredHolder<EntityType<?>, EntityType<Jackal>> JACKAL = register("jackal",
            EntityType.Builder.of(Jackal::new, MobCategory.MONSTER).sized(0.8F, 0.95F).eyeHeight(0.8F));
    public static final DeferredHolder<EntityType<?>, EntityType<Scorpion>> SCORPION = register("scorpion",
            EntityType.Builder.of(Scorpion::new, MobCategory.MONSTER).sized(1.2F, 0.7F).eyeHeight(0.5F));
    public static final DeferredHolder<EntityType<?>, EntityType<Ushabti>> USHABTI = register("ushabti",
            EntityType.Builder.of(Ushabti::new, MobCategory.MONSTER).sized(0.6F, 1.95F).eyeHeight(1.7F));
    /** The crocodile of the Nile, in the shallows and on the banks. */
    public static final DeferredHolder<EntityType<?>, EntityType<Crocodile>> CROCODILE = register("crocodile",
            EntityType.Builder.of(Crocodile::new, MobCategory.MONSTER).sized(1.3F, 0.6F).eyeHeight(0.45F));
    /** The black temple cat of Bastet: tamed with fish, the creatures of the dark flee it. */
    public static final DeferredHolder<EntityType<?>, EntityType<BastetCat>> BASTET_CAT = register("bastet_cat",
            EntityType.Builder.of(BastetCat::new, MobCategory.CREATURE).sized(0.6F, 0.7F).eyeHeight(0.35F).clientTrackingRange(8));
    /** Priestess of Isis in the temples on the Nile; can be courted and married, like an amazon. */
    public static final DeferredHolder<EntityType<?>, EntityType<Priestess>> PRIESTESS = register("priestess",
            EntityType.Builder.of(Priestess::new, MobCategory.CREATURE).sized(0.6F, 1.9F).eyeHeight(1.65F)
                    .clientTrackingRange(10));
    /** Trader of the villages on the Nile: a trader of the market, a priest of Anubis or a smith. */
    public static final DeferredHolder<EntityType<?>, EntityType<EgyptianMerchant>> EGYPTIAN_MERCHANT = register("egyptian_merchant",
            EntityType.Builder.of(EgyptianMerchant::new, MobCategory.CREATURE).sized(0.6F, 1.95F).eyeHeight(1.62F)
                    .clientTrackingRange(10));

    // ---- Half-boss and bosses ----
    public static final DeferredHolder<EntityType<?>, EntityType<PharaohMummy>> PHARAOH_MUMMY = register("pharaoh_mummy",
            EntityType.Builder.of(PharaohMummy::new, MobCategory.MONSTER).sized(0.7F, 2.3F).eyeHeight(2.05F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Sphinx>> SPHINX = register("sphinx",
            EntityType.Builder.of(Sphinx::new, MobCategory.MONSTER).sized(2.4F, 2.6F).eyeHeight(2.3F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<SetGod>> SET = register("set",
            EntityType.Builder.of(SetGod::new, MobCategory.MONSTER).sized(0.8F, 2.8F).eyeHeight(2.5F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Apep>> APEP = register("apep",
            EntityType.Builder.of(Apep::new, MobCategory.MONSTER).sized(2.8F, 3.0F).eyeHeight(2.6F).fireImmune()
                    .clientTrackingRange(10));

    // ---- The gods of Egypt (Set is above with the bosses) ----
    public static final DeferredHolder<EntityType<?>, EntityType<RaGod>> RA = register("ra",
            EntityType.Builder.of(RaGod::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).fireImmune().clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<OsirisGod>> OSIRIS = register("osiris",
            EntityType.Builder.of(OsirisGod::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<IsisGod>> ISIS = register("isis",
            EntityType.Builder.of(IsisGod::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<HorusGod>> HORUS = register("horus",
            EntityType.Builder.of(HorusGod::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<AnubisGod>> ANUBIS = register("anubis",
            EntityType.Builder.of(AnubisGod::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<ThothGod>> THOTH = register("thoth",
            EntityType.Builder.of(ThothGod::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<BastetGod>> BASTET = register("bastet",
            EntityType.Builder.of(BastetGod::new, MobCategory.MONSTER).sized(0.6F, 2.0F).eyeHeight(1.75F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<SobekGod>> SOBEK = register("sobek",
            EntityType.Builder.of(SobekGod::new, MobCategory.MONSTER).sized(0.8F, 2.4F).eyeHeight(2.1F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<HathorGod>> HATHOR = register("hathor",
            EntityType.Builder.of(HathorGod::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<PtahGod>> PTAH = register("ptah",
            EntityType.Builder.of(PtahGod::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<SekhmetGod>> SEKHMET = register("sekhmet",
            EntityType.Builder.of(SekhmetGod::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).fireImmune().clientTrackingRange(10));

    // ---- Spawn eggs (creative tab) ----
    public static final DeferredItem<DeferredSpawnEggItem> MUMMY_SPAWN_EGG = egg("mummy", MUMMY, 0xD8CCA8, 0x6B5A3A);
    public static final DeferredItem<DeferredSpawnEggItem> SCARAB_SPAWN_EGG = egg("scarab", SCARAB, 0x1A2A3A, 0x3AA88A);
    public static final DeferredItem<DeferredSpawnEggItem> JACKAL_SPAWN_EGG = egg("jackal", JACKAL, 0x1E1A1A, 0xE2B33C);
    public static final DeferredItem<DeferredSpawnEggItem> SCORPION_SPAWN_EGG = egg("scorpion", SCORPION, 0xC89A5A, 0x3A2A1A);
    public static final DeferredItem<DeferredSpawnEggItem> USHABTI_SPAWN_EGG = egg("ushabti", USHABTI, 0x2A8AB0, 0x1A1A2A);
    public static final DeferredItem<DeferredSpawnEggItem> BASTET_CAT_SPAWN_EGG = egg("bastet_cat", BASTET_CAT, 0x1A1A1E, 0xFFD040);
    public static final DeferredItem<DeferredSpawnEggItem> PRIESTESS_SPAWN_EGG = egg("priestess", PRIESTESS, 0xF4F0E4, 0x2A5AB0);
    public static final DeferredItem<DeferredSpawnEggItem> EGYPTIAN_MERCHANT_SPAWN_EGG = egg("egyptian_merchant", EGYPTIAN_MERCHANT,
            0xE8E0C8, 0x2A6AB0);
    public static final DeferredItem<DeferredSpawnEggItem> PHARAOH_MUMMY_SPAWN_EGG = egg("pharaoh_mummy", PHARAOH_MUMMY, 0xD8CCA8, 0xE2B33C);
    public static final DeferredItem<DeferredSpawnEggItem> SPHINX_SPAWN_EGG = egg("sphinx", SPHINX, 0xD8B878, 0x2A5AB0);
    public static final DeferredItem<DeferredSpawnEggItem> SET_SPAWN_EGG = egg("set", SET, 0x8A2A1E, 0x1E1414);
    public static final DeferredItem<DeferredSpawnEggItem> APEP_SPAWN_EGG = egg("apep", APEP, 0x2A1A3A, 0xC0262E);
    public static final DeferredItem<DeferredSpawnEggItem> CROCODILE_SPAWN_EGG = egg("crocodile", CROCODILE, 0x4A5A2A, 0xC8B870);
    public static final DeferredItem<DeferredSpawnEggItem> RA_SPAWN_EGG = egg("ra", RA, 0xE2B33C, 0xC0402A);
    public static final DeferredItem<DeferredSpawnEggItem> OSIRIS_SPAWN_EGG = egg("osiris", OSIRIS, 0x3A8A4A, 0xF4F0E4);
    public static final DeferredItem<DeferredSpawnEggItem> ISIS_SPAWN_EGG = egg("isis", ISIS, 0xF4F0E4, 0x2A5AB0);
    public static final DeferredItem<DeferredSpawnEggItem> HORUS_SPAWN_EGG = egg("horus", HORUS, 0x6A4A2A, 0xC0262E);
    public static final DeferredItem<DeferredSpawnEggItem> ANUBIS_SPAWN_EGG = egg("anubis", ANUBIS, 0x141414, 0xE2B33C);
    public static final DeferredItem<DeferredSpawnEggItem> THOTH_SPAWN_EGG = egg("thoth", THOTH, 0xF4F0E4, 0x1A1A2A);
    public static final DeferredItem<DeferredSpawnEggItem> BASTET_SPAWN_EGG = egg("bastet", BASTET, 0x16161C, 0x3AB8A8);
    public static final DeferredItem<DeferredSpawnEggItem> SOBEK_SPAWN_EGG = egg("sobek", SOBEK, 0x4A6A2A, 0xE2B33C);
    public static final DeferredItem<DeferredSpawnEggItem> HATHOR_SPAWN_EGG = egg("hathor", HATHOR, 0xC0402A, 0xE2B33C);
    public static final DeferredItem<DeferredSpawnEggItem> PTAH_SPAWN_EGG = egg("ptah", PTAH, 0x2A5AB0, 0x3A8A4A);
    public static final DeferredItem<DeferredSpawnEggItem> SEKHMET_SPAWN_EGG = egg("sekhmet", SEKHMET, 0xD8A050, 0xC0262E);

    /** Every mob of the Duat, used by the tests. */
    public static List<DeferredHolder<EntityType<?>, ? extends EntityType<? extends Mob>>> all() {
        return List.of(MUMMY, SCARAB, JACKAL, SCORPION, USHABTI, CROCODILE, BASTET_CAT, PRIESTESS, EGYPTIAN_MERCHANT, PHARAOH_MUMMY,
                SPHINX, SET, APEP, RA, OSIRIS, ISIS, HORUS, ANUBIS, THOTH, BASTET, SOBEK, HATHOR, PTAH, SEKHMET);
    }

    /** The gods of Egypt who wait in their shrines, used by the tests. */
    public static List<DeferredHolder<EntityType<?>, ? extends EntityType<? extends Mob>>> gods() {
        return List.of(RA, OSIRIS, ISIS, HORUS, ANUBIS, THOTH, BASTET, SOBEK, HATHOR, PTAH, SEKHMET);
    }

    private EgyptianEntities() {
    }

    private static <T extends Entity> DeferredHolder<EntityType<?>, EntityType<T>> register(String name, EntityType.Builder<T> builder) {
        return ENTITY_TYPES.register(name, () -> builder.build(MythsOfWorlds.id(name).toString()));
    }

    private static DeferredItem<DeferredSpawnEggItem> egg(String name, DeferredHolder<EntityType<?>, ? extends EntityType<? extends Mob>> type,
                                                          int background, int highlight) {
        return ITEMS.register(name + "_spawn_egg", () -> new DeferredSpawnEggItem(type, background, highlight, new Item.Properties()));
    }

    /** Called from the mod constructor. */
    public static void init(IEventBus modBus) {
        modBus.addListener(EgyptianEntities::registerAttributes);
        modBus.addListener(EgyptianEntities::registerSpawnPlacements);
    }

    private static void registerAttributes(EntityAttributeCreationEvent event) {
        event.put(MUMMY.get(), Mummy.createAttributes().build());
        event.put(SCARAB.get(), Scarab.createAttributes().build());
        event.put(JACKAL.get(), Jackal.createAttributes().build());
        event.put(SCORPION.get(), Scorpion.createAttributes().build());
        event.put(USHABTI.get(), Ushabti.createAttributes().build());
        event.put(BASTET_CAT.get(), BastetCat.createAttributes().build());
        event.put(PRIESTESS.get(), Priestess.createAttributes().build());
        event.put(EGYPTIAN_MERCHANT.get(), Mob.createMobAttributes().add(Attributes.MOVEMENT_SPEED, 0.5).build());
        event.put(PHARAOH_MUMMY.get(), PharaohMummy.createAttributes().build());
        event.put(SPHINX.get(), Sphinx.createAttributes().build());
        event.put(SET.get(), SetGod.createAttributes().build());
        event.put(APEP.get(), Apep.createAttributes().build());
        event.put(CROCODILE.get(), Crocodile.createAttributes().build());
        event.put(RA.get(), RaGod.createAttributes().build());
        event.put(OSIRIS.get(), OsirisGod.createAttributes().build());
        event.put(ISIS.get(), IsisGod.createAttributes().build());
        event.put(HORUS.get(), HorusGod.createAttributes().build());
        event.put(ANUBIS.get(), AnubisGod.createAttributes().build());
        event.put(THOTH.get(), ThothGod.createAttributes().build());
        event.put(BASTET.get(), BastetGod.createAttributes().build());
        event.put(SOBEK.get(), SobekGod.createAttributes().build());
        event.put(HATHOR.get(), HathorGod.createAttributes().build());
        event.put(PTAH.get(), PtahGod.createAttributes().build());
        event.put(SEKHMET.get(), SekhmetGod.createAttributes().build());
    }

    /** Rules for natural spawning; the biomes decide where and how often. The night of the Duat never ends. */
    private static void registerSpawnPlacements(RegisterSpawnPlacementsEvent event) {
        var replace = RegisterSpawnPlacementsEvent.Operation.REPLACE;
        var ground = Heightmap.Types.MOTION_BLOCKING_NO_LEAVES;
        event.register(MUMMY.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(SCARAB.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(USHABTI.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(JACKAL.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkAnyLightMonsterSpawnRules, replace);
        // Scorpions only in deserts on sand or terracotta, mostly in the dark; crocodiles only on the shore or in the
        // shallows. Where they may spawn at all is set by the biome modifiers in data/mythsofworlds/neoforge/biome_modifier.
        event.register(SCORPION.get(), SpawnPlacementTypes.ON_GROUND, ground, Scorpion::checkScorpionSpawnRules, replace);
        event.register(CROCODILE.get(), SpawnPlacementTypes.NO_RESTRICTIONS, ground, Crocodile::checkCrocodileSpawnRules, replace);
        event.register(BASTET_CAT.get(), SpawnPlacementTypes.ON_GROUND, ground, Mob::checkMobSpawnRules, replace);
        // Camels roam the sands of the Duat; vanilla has no natural spawn rule for them, as they only come with villages.
        event.register(EntityType.CAMEL, SpawnPlacementTypes.ON_GROUND, ground, Mob::checkMobSpawnRules, replace);
    }
}
