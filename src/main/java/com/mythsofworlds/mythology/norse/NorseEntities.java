package com.mythsofworlds.mythology.norse;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.norse.entity.Draugr;
import com.mythsofworlds.mythology.norse.entity.DraugrChieftain;
import com.mythsofworlds.mythology.norse.entity.Fenrir;
import com.mythsofworlds.mythology.norse.entity.FireGiant;
import com.mythsofworlds.mythology.norse.entity.FrostGiant;
import com.mythsofworlds.mythology.norse.entity.Garm;
import com.mythsofworlds.mythology.norse.entity.NorseMerchant;
import com.mythsofworlds.mythology.norse.entity.Raven;
import com.mythsofworlds.mythology.norse.entity.Surtr;
import com.mythsofworlds.mythology.norse.entity.Thrym;
import com.mythsofworlds.mythology.norse.entity.Troll;
import com.mythsofworlds.mythology.norse.entity.Warg;
import java.util.List;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.Parrot;
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
 * Creatures of Jotunheim. Which biomes they spawn in is set in data/mythsofworlds/worldgen/biome/*.json ("spawners");
 * bosses and mini-bosses wait in their structures (data/mythsofworlds/structure/norse). Renderers are in the client package.
 */
public final class NorseEntities {
    // ---- Creatures ----
    public static final DeferredHolder<EntityType<?>, EntityType<Draugr>> DRAUGR = register("draugr",
            EntityType.Builder.of(Draugr::new, MobCategory.MONSTER).sized(0.6F, 1.95F).eyeHeight(1.74F));
    public static final DeferredHolder<EntityType<?>, EntityType<Warg>> WARG = register("warg",
            EntityType.Builder.of(Warg::new, MobCategory.MONSTER).sized(1.1F, 1.25F).eyeHeight(1.05F));
    public static final DeferredHolder<EntityType<?>, EntityType<Troll>> TROLL = register("troll",
            EntityType.Builder.of(Troll::new, MobCategory.MONSTER).sized(1.2F, 2.9F).eyeHeight(2.5F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<FrostGiant>> FROST_GIANT = register("frost_giant",
            EntityType.Builder.of(FrostGiant::new, MobCategory.MONSTER).sized(1.3F, 3.6F).eyeHeight(3.2F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<FireGiant>> FIRE_GIANT = register("fire_giant",
            EntityType.Builder.of(FireGiant::new, MobCategory.MONSTER).sized(1.3F, 3.6F).eyeHeight(3.2F).fireImmune()
                    .clientTrackingRange(10));
    /** Odin's bird: tamed with seeds, it marks hidden monsters for its master. */
    public static final DeferredHolder<EntityType<?>, EntityType<Raven>> RAVEN = register("raven",
            EntityType.Builder.of(Raven::new, MobCategory.CREATURE).sized(0.5F, 0.9F).eyeHeight(0.54F).clientTrackingRange(8));
    /** Trader of the Viking villages: the jarl's steward, a dwarf smith or a volva. */
    public static final DeferredHolder<EntityType<?>, EntityType<NorseMerchant>> NORSE_MERCHANT = register("norse_merchant",
            EntityType.Builder.of(NorseMerchant::new, MobCategory.CREATURE).sized(0.6F, 1.95F).eyeHeight(1.62F)
                    .clientTrackingRange(10));

    // ---- Mini-bosses ----
    public static final DeferredHolder<EntityType<?>, EntityType<DraugrChieftain>> DRAUGR_CHIEFTAIN = register("draugr_chieftain",
            EntityType.Builder.of(DraugrChieftain::new, MobCategory.MONSTER).sized(0.75F, 2.3F).eyeHeight(2.05F)
                    .clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Garm>> GARM = register("garm",
            EntityType.Builder.of(Garm::new, MobCategory.MONSTER).sized(1.7F, 2.0F).eyeHeight(1.7F).clientTrackingRange(10));

    // ---- Bosses ----
    public static final DeferredHolder<EntityType<?>, EntityType<Thrym>> THRYM = register("thrym",
            EntityType.Builder.of(Thrym::new, MobCategory.MONSTER).sized(1.6F, 4.7F).eyeHeight(4.2F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Fenrir>> FENRIR = register("fenrir",
            EntityType.Builder.of(Fenrir::new, MobCategory.MONSTER).sized(2.6F, 3.0F).eyeHeight(2.6F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Surtr>> SURTR = register("surtr",
            EntityType.Builder.of(Surtr::new, MobCategory.MONSTER).sized(1.6F, 4.7F).eyeHeight(4.2F).fireImmune()
                    .clientTrackingRange(10));

    // ---- Spawn eggs (creative tab) ----
    public static final DeferredItem<DeferredSpawnEggItem> DRAUGR_SPAWN_EGG = egg("draugr", DRAUGR, 0x5E7A82, 0xBFD9E0);
    public static final DeferredItem<DeferredSpawnEggItem> WARG_SPAWN_EGG = egg("warg", WARG, 0x5A5A5E, 0xC9C2B4);
    public static final DeferredItem<DeferredSpawnEggItem> TROLL_SPAWN_EGG = egg("troll", TROLL, 0x6E7A52, 0x8A7356);
    public static final DeferredItem<DeferredSpawnEggItem> FROST_GIANT_SPAWN_EGG = egg("frost_giant", FROST_GIANT, 0x9FC4D8, 0xE8F4FA);
    public static final DeferredItem<DeferredSpawnEggItem> FIRE_GIANT_SPAWN_EGG = egg("fire_giant", FIRE_GIANT, 0x3A2A24, 0xF2702A);
    public static final DeferredItem<DeferredSpawnEggItem> RAVEN_SPAWN_EGG = egg("raven", RAVEN, 0x1A1A22, 0x4A4A6A);
    public static final DeferredItem<DeferredSpawnEggItem> NORSE_MERCHANT_SPAWN_EGG = egg("norse_merchant", NORSE_MERCHANT, 0x6B4A2B, 0x3A6EA5);
    public static final DeferredItem<DeferredSpawnEggItem> DRAUGR_CHIEFTAIN_SPAWN_EGG = egg("draugr_chieftain", DRAUGR_CHIEFTAIN, 0x3E525A, 0xD4A93A);
    public static final DeferredItem<DeferredSpawnEggItem> GARM_SPAWN_EGG = egg("garm", GARM, 0x2A2224, 0x8A1E1E);
    public static final DeferredItem<DeferredSpawnEggItem> THRYM_SPAWN_EGG = egg("thrym", THRYM, 0x7FA8C4, 0x1E3A5A);
    public static final DeferredItem<DeferredSpawnEggItem> FENRIR_SPAWN_EGG = egg("fenrir", FENRIR, 0x3A3A40, 0xB3261E);
    public static final DeferredItem<DeferredSpawnEggItem> SURTR_SPAWN_EGG = egg("surtr", SURTR, 0x1E1414, 0xFF8A1E);

    /** Every mob of Jotunheim, used by the tests. */
    public static List<DeferredHolder<EntityType<?>, ? extends EntityType<? extends Mob>>> all() {
        return List.of(DRAUGR, WARG, TROLL, FROST_GIANT, FIRE_GIANT, RAVEN, NORSE_MERCHANT, DRAUGR_CHIEFTAIN, GARM,
                THRYM, FENRIR, SURTR);
    }

    private NorseEntities() {
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
        modBus.addListener(NorseEntities::registerAttributes);
        modBus.addListener(NorseEntities::registerSpawnPlacements);
    }

    private static void registerAttributes(EntityAttributeCreationEvent event) {
        event.put(DRAUGR.get(), Draugr.createAttributes().build());
        event.put(WARG.get(), Warg.createAttributes().build());
        event.put(TROLL.get(), Troll.createAttributes().build());
        event.put(FROST_GIANT.get(), FrostGiant.createAttributes().build());
        event.put(FIRE_GIANT.get(), FireGiant.createAttributes().build());
        event.put(RAVEN.get(), Parrot.createAttributes().build());
        event.put(NORSE_MERCHANT.get(), Mob.createMobAttributes().add(Attributes.MOVEMENT_SPEED, 0.5).build());
        event.put(DRAUGR_CHIEFTAIN.get(), DraugrChieftain.createAttributes().build());
        event.put(GARM.get(), Garm.createAttributes().build());
        event.put(THRYM.get(), Thrym.createAttributes().build());
        event.put(FENRIR.get(), Fenrir.createAttributes().build());
        event.put(SURTR.get(), Surtr.createAttributes().build());
    }

    /** Rules for natural spawning; the biomes decide where and how often. */
    private static void registerSpawnPlacements(RegisterSpawnPlacementsEvent event) {
        var replace = RegisterSpawnPlacementsEvent.Operation.REPLACE;
        var ground = Heightmap.Types.MOTION_BLOCKING_NO_LEAVES;
        // The dead and the trolls need darkness; wolves and giants roam by day as well.
        event.register(DRAUGR.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(TROLL.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(WARG.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkAnyLightMonsterSpawnRules, replace);
        event.register(FROST_GIANT.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkAnyLightMonsterSpawnRules, replace);
        event.register(FIRE_GIANT.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkAnyLightMonsterSpawnRules, replace);
        event.register(RAVEN.get(), SpawnPlacementTypes.ON_GROUND, ground, Mob::checkMobSpawnRules, replace);
    }
}
