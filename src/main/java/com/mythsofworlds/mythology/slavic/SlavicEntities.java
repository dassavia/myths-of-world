package com.mythsofworlds.mythology.slavic;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.slavic.entity.Firebird;
import com.mythsofworlds.mythology.slavic.entity.Kikimora;
import com.mythsofworlds.mythology.slavic.entity.Koschei;
import com.mythsofworlds.mythology.slavic.entity.Leshy;
import com.mythsofworlds.mythology.slavic.entity.Rusalka;
import com.mythsofworlds.mythology.slavic.entity.SlavicMerchant;
import com.mythsofworlds.mythology.slavic.entity.Solovei;
import com.mythsofworlds.mythology.slavic.entity.Upyr;
import com.mythsofworlds.mythology.slavic.entity.Volkolak;
import com.mythsofworlds.mythology.slavic.entity.ZmeyGorynych;
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
 * Creatures of Nav. Which biomes they spawn in is set in data/mythsofworlds/worldgen/biome/*.json ("spawners");
 * bosses wait in their structures (data/mythsofworlds/structure/slavic). Renderers are in the client package.
 */
public final class SlavicEntities {
    // ---- Creatures ----
    public static final DeferredHolder<EntityType<?>, EntityType<Leshy>> LESHY = register("leshy",
            EntityType.Builder.of(Leshy::new, MobCategory.MONSTER).sized(0.8F, 2.6F).eyeHeight(2.3F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Kikimora>> KIKIMORA = register("kikimora",
            EntityType.Builder.of(Kikimora::new, MobCategory.MONSTER).sized(0.5F, 1.5F).eyeHeight(1.3F));
    public static final DeferredHolder<EntityType<?>, EntityType<Upyr>> UPYR = register("upyr",
            EntityType.Builder.of(Upyr::new, MobCategory.MONSTER).sized(0.6F, 1.95F).eyeHeight(1.74F));
    public static final DeferredHolder<EntityType<?>, EntityType<Volkolak>> VOLKOLAK = register("volkolak",
            EntityType.Builder.of(Volkolak::new, MobCategory.MONSTER).sized(1.1F, 1.3F).eyeHeight(1.1F));
    public static final DeferredHolder<EntityType<?>, EntityType<Rusalka>> RUSALKA = register("rusalka",
            EntityType.Builder.of(Rusalka::new, MobCategory.MONSTER).sized(0.6F, 1.9F).eyeHeight(1.65F));
    /** Zhar-ptitsa: strokes give a glowing feather; tamed with seeds like the raven. */
    public static final DeferredHolder<EntityType<?>, EntityType<Firebird>> FIREBIRD = register("firebird",
            EntityType.Builder.of(Firebird::new, MobCategory.CREATURE).sized(0.5F, 0.9F).eyeHeight(0.54F).fireImmune()
                    .clientTrackingRange(8));
    /** Trader of the villages of Nav: a merchant, Baba Yaga or a smith. */
    public static final DeferredHolder<EntityType<?>, EntityType<SlavicMerchant>> SLAVIC_MERCHANT = register("slavic_merchant",
            EntityType.Builder.of(SlavicMerchant::new, MobCategory.CREATURE).sized(0.6F, 1.95F).eyeHeight(1.62F)
                    .clientTrackingRange(10));

    // ---- Mini-boss and bosses ----
    public static final DeferredHolder<EntityType<?>, EntityType<Solovei>> SOLOVEI = register("solovei",
            EntityType.Builder.of(Solovei::new, MobCategory.MONSTER).sized(0.7F, 2.2F).eyeHeight(1.95F).clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<ZmeyGorynych>> ZMEY_GORYNYCH = register("zmey_gorynych",
            EntityType.Builder.of(ZmeyGorynych::new, MobCategory.MONSTER).sized(2.8F, 3.4F).eyeHeight(3.0F).fireImmune()
                    .clientTrackingRange(10));
    public static final DeferredHolder<EntityType<?>, EntityType<Koschei>> KOSCHEI = register("koschei",
            EntityType.Builder.of(Koschei::new, MobCategory.MONSTER).sized(0.7F, 2.5F).eyeHeight(2.2F).clientTrackingRange(10));

    // ---- Spawn eggs (creative tab) ----
    public static final DeferredItem<DeferredSpawnEggItem> LESHY_SPAWN_EGG = egg("leshy", LESHY, 0x4A3A24, 0x5E8A3A);
    public static final DeferredItem<DeferredSpawnEggItem> KIKIMORA_SPAWN_EGG = egg("kikimora", KIKIMORA, 0x4E5A3A, 0x8A9A5A);
    public static final DeferredItem<DeferredSpawnEggItem> UPYR_SPAWN_EGG = egg("upyr", UPYR, 0xC8C4BC, 0x8A1414);
    public static final DeferredItem<DeferredSpawnEggItem> VOLKOLAK_SPAWN_EGG = egg("volkolak", VOLKOLAK, 0x5A4A3E, 0xA89A86);
    public static final DeferredItem<DeferredSpawnEggItem> RUSALKA_SPAWN_EGG = egg("rusalka", RUSALKA, 0xD8E0E0, 0x3E8A6A);
    public static final DeferredItem<DeferredSpawnEggItem> FIREBIRD_SPAWN_EGG = egg("firebird", FIREBIRD, 0xE5501F, 0xFFD040);
    public static final DeferredItem<DeferredSpawnEggItem> SLAVIC_MERCHANT_SPAWN_EGG = egg("slavic_merchant", SLAVIC_MERCHANT, 0xA8282E, 0xE2B33C);
    public static final DeferredItem<DeferredSpawnEggItem> SOLOVEI_SPAWN_EGG = egg("solovei", SOLOVEI, 0x6B4A2B, 0x2A2A2A);
    public static final DeferredItem<DeferredSpawnEggItem> ZMEY_GORYNYCH_SPAWN_EGG = egg("zmey_gorynych", ZMEY_GORYNYCH, 0x2E5A2A, 0xE5501F);
    public static final DeferredItem<DeferredSpawnEggItem> KOSCHEI_SPAWN_EGG = egg("koschei", KOSCHEI, 0x1E1A24, 0xC9962E);

    /** Every mob of Nav, used by the tests. */
    public static List<DeferredHolder<EntityType<?>, ? extends EntityType<? extends Mob>>> all() {
        return List.of(LESHY, KIKIMORA, UPYR, VOLKOLAK, RUSALKA, FIREBIRD, SLAVIC_MERCHANT, SOLOVEI, ZMEY_GORYNYCH, KOSCHEI);
    }

    private SlavicEntities() {
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
        modBus.addListener(SlavicEntities::registerAttributes);
        modBus.addListener(SlavicEntities::registerSpawnPlacements);
    }

    private static void registerAttributes(EntityAttributeCreationEvent event) {
        event.put(LESHY.get(), Leshy.createAttributes().build());
        event.put(KIKIMORA.get(), Kikimora.createAttributes().build());
        event.put(UPYR.get(), Upyr.createAttributes().build());
        event.put(VOLKOLAK.get(), Volkolak.createAttributes().build());
        event.put(RUSALKA.get(), Rusalka.createAttributes().build());
        event.put(FIREBIRD.get(), Parrot.createAttributes().build());
        event.put(SLAVIC_MERCHANT.get(), Mob.createMobAttributes().add(Attributes.MOVEMENT_SPEED, 0.5).build());
        event.put(SOLOVEI.get(), Solovei.createAttributes().build());
        event.put(ZMEY_GORYNYCH.get(), ZmeyGorynych.createAttributes().build());
        event.put(KOSCHEI.get(), Koschei.createAttributes().build());
    }

    /** Rules for natural spawning; the biomes decide where and how often. */
    private static void registerSpawnPlacements(RegisterSpawnPlacementsEvent event) {
        var replace = RegisterSpawnPlacementsEvent.Operation.REPLACE;
        var ground = Heightmap.Types.MOTION_BLOCKING_NO_LEAVES;
        // The dead and the bog hags want darkness; the master of the forest and the werewolves walk in the dusk.
        event.register(UPYR.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(KIKIMORA.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(RUSALKA.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkMonsterSpawnRules, replace);
        event.register(LESHY.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkAnyLightMonsterSpawnRules, replace);
        event.register(VOLKOLAK.get(), SpawnPlacementTypes.ON_GROUND, ground, Monster::checkAnyLightMonsterSpawnRules, replace);
        event.register(FIREBIRD.get(), SpawnPlacementTypes.ON_GROUND, ground, Mob::checkMobSpawnRules, replace);
    }
}
