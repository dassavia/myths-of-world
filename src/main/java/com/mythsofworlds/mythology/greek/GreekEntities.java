package com.mythsofworlds.mythology.greek;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.greek.entity.Cerberus;
import com.mythsofworlds.mythology.greek.entity.Cyclops;
import com.mythsofworlds.mythology.greek.entity.GoldenHind;
import com.mythsofworlds.mythology.greek.entity.GreekMerchant;
import com.mythsofworlds.mythology.greek.entity.Harpy;
import com.mythsofworlds.mythology.greek.entity.Hippolyta;
import com.mythsofworlds.mythology.greek.entity.Hydra;
import com.mythsofworlds.mythology.greek.entity.HydraHatchling;
import com.mythsofworlds.mythology.greek.entity.Karkinos;
import com.mythsofworlds.mythology.greek.entity.Lion;
import com.mythsofworlds.mythology.greek.entity.Medusa;
import com.mythsofworlds.mythology.greek.entity.Minotaur;
import com.mythsofworlds.mythology.greek.entity.NemeanLion;
import com.mythsofworlds.mythology.greek.entity.Pegasus;
import com.mythsofworlds.mythology.greek.entity.Satyr;
import com.mythsofworlds.mythology.greek.entity.Shade;
import com.mythsofworlds.mythology.greek.entity.Spartoi;
import java.util.List;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.animal.Animal;
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
 * Creatures of Hellas. Which biomes they spawn in is set in data/mythsofworlds/worldgen/biome/*.json ("spawners");
 * bosses and mini-bosses do not spawn naturally, they wait in their structures (data/mythsofworlds/structure/greek).
 * Renderers and models are in the client package.
 */
public final class GreekEntities {
    // ---- Creatures ----
    public static final DeferredHolder<EntityType<?>, EntityType<Satyr>> SATYR = register("satyr",
            EntityType.Builder.of(Satyr::new, MobCategory.MONSTER).sized(0.6F, 1.8F).eyeHeight(1.6F));
    public static final DeferredHolder<EntityType<?>, EntityType<Harpy>> HARPY = register("harpy",
            EntityType.Builder.of(Harpy::new, MobCategory.MONSTER).sized(0.7F, 1.7F).eyeHeight(1.5F));
    public static final DeferredHolder<EntityType<?>, EntityType<Spartoi>> SPARTOI = register("spartoi",
            EntityType.Builder.of(Spartoi::new, MobCategory.MONSTER).sized(0.6F, 1.99F).eyeHeight(1.74F));
    public static final DeferredHolder<EntityType<?>, EntityType<Shade>> SHADE = register("shade",
            EntityType.Builder.of(Shade::new, MobCategory.MONSTER).sized(0.6F, 1.95F).eyeHeight(1.74F));
    public static final DeferredHolder<EntityType<?>, EntityType<Pegasus>> PEGASUS = register("pegasus",
            EntityType.Builder.of(Pegasus::new, MobCategory.CREATURE).sized(1.3964844F, 1.6F).eyeHeight(1.52F)
                    .clientTrackingRange(10));
    /** The Ceryneian Hind of Artemis: golden antlers, bronze hooves, tamed and ridden like a horse. */
    public static final DeferredHolder<EntityType<?>, EntityType<GoldenHind>> GOLDEN_HIND = register("golden_hind",
            EntityType.Builder.of(GoldenHind::new, MobCategory.CREATURE).sized(1.2F, 1.6F).eyeHeight(1.5F)
                    .clientTrackingRange(10));
    /** Hatched from a Hydra egg; a loyal pet. */
    public static final DeferredHolder<EntityType<?>, EntityType<HydraHatchling>> HYDRA_HATCHLING = register("hydra_hatchling",
            EntityType.Builder.of(HydraHatchling::new, MobCategory.CREATURE).sized(0.9F, 0.9F).eyeHeight(0.75F));
    /** Merchant of the agora who buys trophies of the monsters of Hellas. */
    public static final DeferredHolder<EntityType<?>, EntityType<GreekMerchant>> GREEK_MERCHANT = register("greek_merchant",
            EntityType.Builder.of(GreekMerchant::new, MobCategory.CREATURE).sized(0.6F, 1.95F).eyeHeight(1.62F)
                    .clientTrackingRange(10));
    /** Lion of the pride of the Nemean Forest: hunts game, fights only if the pride is attacked. */
    public static final DeferredHolder<EntityType<?>, EntityType<Lion>> LION = register("lion",
            EntityType.Builder.of(Lion::new, MobCategory.CREATURE).sized(1.2F, 1.3F).eyeHeight(1.1F));
    /** Warrior woman of Themiscyra; can be courted and married. */
    public static final DeferredHolder<EntityType<?>, EntityType<Amazon>> AMAZON = register("amazon",
            EntityType.Builder.of(Amazon::new, MobCategory.CREATURE).sized(0.6F, 1.9F).eyeHeight(1.65F)
                    .clientTrackingRange(10));

    // ---- Mini-bosses ----
    public static final DeferredHolder<EntityType<?>, EntityType<Cyclops>> CYCLOPS = register("cyclops",
            EntityType.Builder.of(Cyclops::new, MobCategory.MONSTER).sized(1.3F, 4.2F).eyeHeight(3.7F)
                    .clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Medusa>> MEDUSA = register("medusa",
            EntityType.Builder.of(Medusa::new, MobCategory.MONSTER).sized(0.7F, 2.1F).eyeHeight(1.85F)
                    .clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<NemeanLion>> NEMEAN_LION = register("nemean_lion",
            EntityType.Builder.of(NemeanLion::new, MobCategory.MONSTER).sized(1.4F, 1.6F).eyeHeight(1.3F)
                    .clientTrackingRange(10));
    /** The giant crab of Hera, in the Hydra's lair. */
    public static final DeferredHolder<EntityType<?>, EntityType<Karkinos>> KARKINOS = register("karkinos",
            EntityType.Builder.of(Karkinos::new, MobCategory.MONSTER).sized(2.0F, 1.2F).eyeHeight(1.0F)
                    .clientTrackingRange(10));

    // ---- Bosses ----
    public static final DeferredHolder<EntityType<?>, EntityType<Minotaur>> MINOTAUR = register("minotaur",
            EntityType.Builder.of(Minotaur::new, MobCategory.MONSTER).sized(1.0F, 2.9F).eyeHeight(2.6F)
                    .clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Hydra>> HYDRA = register("hydra",
            EntityType.Builder.of(Hydra::new, MobCategory.MONSTER).sized(2.6F, 3.6F).eyeHeight(3.2F)
                    .clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Cerberus>> CERBERUS = register("cerberus",
            EntityType.Builder.of(Cerberus::new, MobCategory.MONSTER).sized(1.8F, 2.2F).eyeHeight(1.9F)
                    .fireImmune().clientTrackingRange(10));
    /** Queen of the Amazons, in Themiscyra. */
    public static final DeferredHolder<EntityType<?>, EntityType<Hippolyta>> HIPPOLYTA = register("hippolyta",
            EntityType.Builder.of(Hippolyta::new, MobCategory.CREATURE).sized(0.6F, 1.95F).eyeHeight(1.7F)
                    .clientTrackingRange(10));

    // ---- Spawn eggs (creative tab) ----
    public static final DeferredItem<DeferredSpawnEggItem> SATYR_SPAWN_EGG = egg("satyr", SATYR, 0x7A5230, 0xD9B77E);
    public static final DeferredItem<DeferredSpawnEggItem> HARPY_SPAWN_EGG = egg("harpy", HARPY, 0x5B4636, 0xC9A66B);
    public static final DeferredItem<DeferredSpawnEggItem> SPARTOI_SPAWN_EGG = egg("spartoi", SPARTOI, 0xD8D3C4, 0xD4A93A);
    public static final DeferredItem<DeferredSpawnEggItem> SHADE_SPAWN_EGG = egg("shade", SHADE, 0x5E6B78, 0xBFD6E3);
    public static final DeferredItem<DeferredSpawnEggItem> PEGASUS_SPAWN_EGG = egg("pegasus", PEGASUS, 0xF4F1EA, 0xE6C35C);
    public static final DeferredItem<DeferredSpawnEggItem> GOLDEN_HIND_SPAWN_EGG = egg("golden_hind", GOLDEN_HIND, 0xC9A23A, 0xFFF1A8);
    public static final DeferredItem<DeferredSpawnEggItem> HYDRA_HATCHLING_SPAWN_EGG = egg("hydra_hatchling", HYDRA_HATCHLING, 0x5E9C4A, 0xD7E88A);
    public static final DeferredItem<DeferredSpawnEggItem> GREEK_MERCHANT_SPAWN_EGG = egg("greek_merchant", GREEK_MERCHANT, 0xE9E1CC, 0x2E5FA8);
    public static final DeferredItem<DeferredSpawnEggItem> CYCLOPS_SPAWN_EGG = egg("cyclops", CYCLOPS, 0x9C7F5F, 0x4E3B2A);
    public static final DeferredItem<DeferredSpawnEggItem> MEDUSA_SPAWN_EGG = egg("medusa", MEDUSA, 0x4F7A3A, 0xB3D16A);
    public static final DeferredItem<DeferredSpawnEggItem> NEMEAN_LION_SPAWN_EGG = egg("nemean_lion", NEMEAN_LION, 0xC9962E, 0x7A4E14);
    public static final DeferredItem<DeferredSpawnEggItem> MINOTAUR_SPAWN_EGG = egg("minotaur", MINOTAUR, 0x4A2E1E, 0xE8DCC0);
    public static final DeferredItem<DeferredSpawnEggItem> HYDRA_SPAWN_EGG = egg("hydra", HYDRA, 0x2F5D3A, 0x8BC34A);
    public static final DeferredItem<DeferredSpawnEggItem> CERBERUS_SPAWN_EGG = egg("cerberus", CERBERUS, 0x1E1A1A, 0xE5501F);
    public static final DeferredItem<DeferredSpawnEggItem> LION_SPAWN_EGG = egg("lion", LION, 0xC4914A, 0x6B4420);
    public static final DeferredItem<DeferredSpawnEggItem> AMAZON_SPAWN_EGG = egg("amazon", AMAZON, 0xB0703A, 0xC9A23A);
    public static final DeferredItem<DeferredSpawnEggItem> KARKINOS_SPAWN_EGG = egg("karkinos", KARKINOS, 0xB3361E, 0xE8B07A);
    public static final DeferredItem<DeferredSpawnEggItem> HIPPOLYTA_SPAWN_EGG = egg("hippolyta", HIPPOLYTA, 0x8A1E2A, 0xE2B33C);

    /** Every mob of Hellas, used by the tests. */
    public static List<DeferredHolder<EntityType<?>, ? extends EntityType<? extends Mob>>> all() {
        return List.of(SATYR, HARPY, SPARTOI, SHADE, PEGASUS, GOLDEN_HIND, HYDRA_HATCHLING, GREEK_MERCHANT, LION, AMAZON, CYCLOPS, MEDUSA, NEMEAN_LION,
                KARKINOS, MINOTAUR, HYDRA, CERBERUS, HIPPOLYTA);
    }

    private GreekEntities() {
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
        modBus.addListener(GreekEntities::registerAttributes);
        modBus.addListener(GreekEntities::registerSpawnPlacements);
    }

    private static void registerAttributes(EntityAttributeCreationEvent event) {
        event.put(SATYR.get(), Satyr.createAttributes().build());
        event.put(HARPY.get(), Harpy.createAttributes().build());
        event.put(SPARTOI.get(), Spartoi.createAttributes().build());
        event.put(SHADE.get(), Shade.createAttributes().build());
        event.put(PEGASUS.get(), Pegasus.createAttributes().build());
        event.put(GOLDEN_HIND.get(), GoldenHind.createAttributes().build());
        event.put(HYDRA_HATCHLING.get(), HydraHatchling.createAttributes().build());
        event.put(GREEK_MERCHANT.get(), Mob.createMobAttributes().add(Attributes.MOVEMENT_SPEED, 0.5).build());
        event.put(CYCLOPS.get(), Cyclops.createAttributes().build());
        event.put(MEDUSA.get(), Medusa.createAttributes().build());
        event.put(NEMEAN_LION.get(), NemeanLion.createAttributes().build());
        event.put(MINOTAUR.get(), Minotaur.createAttributes().build());
        event.put(HYDRA.get(), Hydra.createAttributes().build());
        event.put(CERBERUS.get(), Cerberus.createAttributes().build());
        event.put(LION.get(), Lion.createAttributes().build());
        event.put(AMAZON.get(), Amazon.createAttributes().build());
        event.put(KARKINOS.get(), Karkinos.createAttributes().build());
        event.put(HIPPOLYTA.get(), Hippolyta.createAttributes().build());
    }

    /** Rules for natural spawning; the biomes decide where and how often. */
    private static void registerSpawnPlacements(RegisterSpawnPlacementsEvent event) {
        var replace = RegisterSpawnPlacementsEvent.Operation.REPLACE;
        var ground = Heightmap.Types.MOTION_BLOCKING_NO_LEAVES;
        // Satyrs and harpies roam by day as well; spartoi and shades need darkness.
        event.register(SATYR.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkAnyLightMonsterSpawnRules, replace);
        event.register(HARPY.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkAnyLightMonsterSpawnRules, replace);
        event.register(SPARTOI.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(SHADE.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(PEGASUS.get(), SpawnPlacementTypes.ON_GROUND, ground, Animal::checkAnimalSpawnRules, replace);
        event.register(GOLDEN_HIND.get(), SpawnPlacementTypes.ON_GROUND, ground, Animal::checkAnimalSpawnRules, replace);
        event.register(LION.get(), SpawnPlacementTypes.ON_GROUND, ground, Animal::checkAnimalSpawnRules, replace);
    }
}
