package com.mythsofworlds.compat.mca;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.CommonConfig;
import java.lang.reflect.Field;
import java.util.LinkedHashMap;
import java.util.Map;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.TagKey;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModList;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;

/**
 * The one place that knows about Minecraft Comes Alive Reborn (mod id {@value #MODID}, 7.7.32+ for 1.21.1). It is only
 * loaded when MCA is installed ({@link #isLoaded()} is checked before anything here is touched) and never links
 * against MCA's classes, so the mod builds and runs the same without it. Most of the integration is data that MCA
 * reads by itself and that is ignored when it is absent:
 * <ul>
 *   <li>{@code data/minecraft/tags/worldgen/structure/village.json}: the Egyptian village is a village, so MCA counts
 *   it among the villages (rumours, destinies, locating);</li>
 *   <li>{@code data/mca/tags/block/villager_pathfinding_collision_checks.json}: blocks of an odd shape (the brazier)
 *   get MCA's exact clearance check, so its villagers do not get stuck on them.</li>
 * </ul>
 * In code there are two things. MCA's guards choose whom to fight from the {@code guardsTargetEntities} map of its
 * config ({@code config/mca.json}), which accepts entity tags as {@code "#namespace:path"}; on start-up two keys are
 * added for our tags {@link #GUARD_IGNORED} (priority -1: gods, traders, friendly creatures) and {@link #GUARD_TARGETS}
 * (priority {@value #TARGET_PRIORITY}: our monsters). Keys the player wrote in mca.json win: nothing already there is
 * changed, and the ignored tag is checked before every other tag, so a god is never attacked even if a tag of the
 * player's lists it. And, if {@link CommonConfig#MCA_NO_DOUBLE_RESIDENTS} is on, a villager is not added inside one of
 * our structures right next to the trader or priestess who already lives there. No mixins into MCA, nothing of its
 * registries, entities or of the vanilla villager is replaced.
 */
public final class McaCompat {
    public static final String MODID = "mca";
    public static final TagKey<EntityType<?>> GUARD_TARGETS = TagKey.create(Registries.ENTITY_TYPE, MythsOfWorlds.id("mca/guard_targets"));
    public static final TagKey<EntityType<?>> GUARD_IGNORED = TagKey.create(Registries.ENTITY_TYPE, MythsOfWorlds.id("mca/guard_ignored"));
    /** Our residents: a villager is not added next to one of them inside our structures. */
    public static final TagKey<EntityType<?>> RESIDENTS = TagKey.create(Registries.ENTITY_TYPE, MythsOfWorlds.id("mca/residents"));
    /** As high as MCA's own priority for zombies and vindicators. */
    public static final int TARGET_PRIORITY = 4;
    /** How close to one of our residents a villager may not be added, in blocks. */
    public static final double RESIDENT_RADIUS = 6.0;
    private static final String CONFIG_CLASS = "net.conczin.mca.Config";
    private static final String GUARD_FIELD = "guardsTargetEntities";

    private static boolean guardsConfigured;

    private McaCompat() {
    }

    public static boolean isLoaded() {
        return ModList.get().isLoaded(MODID);
    }

    /** True if MCA is installed and the integration is switched on. */
    public static boolean active() {
        return isLoaded() && CommonConfig.MCA_COMPAT.get();
    }

    /** Whether the guard priorities were added to MCA's config (for the tests). */
    public static boolean guardsConfigured() {
        return guardsConfigured;
    }

    /** Called from the mod constructor, only when MCA is installed. */
    public static void init(IEventBus modBus) {
        modBus.addListener(McaCompat::setup);
        NeoForge.EVENT_BUS.addListener(McaCompat::onJoin);
    }

    private static void setup(FMLCommonSetupEvent event) {
        event.enqueueWork(() -> {
            if (CommonConfig.MCA_COMPAT.get()) {
                configureGuards();
            }
        });
    }

    /** Adds our two tags to MCA's guard priorities; leaves everything the player configured untouched. */
    @SuppressWarnings("unchecked")
    static void configureGuards() {
        try {
            Class<?> configClass = Class.forName(CONFIG_CLASS);
            Object config = configClass.getMethod("getInstance").invoke(null);
            Field field = configClass.getField(GUARD_FIELD);
            Map<String, Integer> current = (Map<String, Integer>) field.get(config);
            Map<String, Integer> merged = new LinkedHashMap<>();
            String ignored = "#" + GUARD_IGNORED.location();
            String targets = "#" + GUARD_TARGETS.location();
            merged.put(ignored, current.getOrDefault(ignored, -1));
            merged.putAll(current);
            merged.putIfAbsent(targets, TARGET_PRIORITY);
            field.set(config, merged);
            guardsConfigured = true;
            MythsOfWorlds.LOGGER.info("MCA Reborn found: its guards now fight {} and leave {} alone", targets, ignored);
        } catch (ReflectiveOperationException | ClassCastException | LinkageError e) {
            MythsOfWorlds.LOGGER.warn("MCA Reborn found, but its guard settings could not be read; its guards keep their own rules", e);
        }
    }

    /**
     * MCA's villagers (and vanilla ones, which MCA turns into its own) are not added inside one of our structures next
     * to one of our residents, so a house never gets two.
     */
    private static void onJoin(EntityJoinLevelEvent event) {
        if (event.loadedFromDisk() || !(event.getLevel() instanceof ServerLevel level) || !CommonConfig.MCA_COMPAT.get()
                || !CommonConfig.MCA_NO_DOUBLE_RESIDENTS.get()) {
            return;
        }
        Entity entity = event.getEntity();
        // Babies are born, not added: MCA's families grow as they like.
        if (!isVillager(entity.getType()) || entity instanceof AgeableMob mob && mob.isBaby()) {
            return;
        }
        BlockPos pos = entity.blockPosition();
        if (!level.isLoaded(pos) || !level.structureManager().getStructureWithPieceAt(pos,
                structure -> structure.unwrapKey().map(key -> key.location().getNamespace().equals(MythsOfWorlds.MODID)).orElse(false))
                .isValid()) {
            return;
        }
        boolean occupied = !level.getEntities(entity, entity.getBoundingBox().inflate(RESIDENT_RADIUS),
                other -> other.getType().is(RESIDENTS)).isEmpty();
        if (occupied) {
            event.setCanceled(true);
        }
    }

    /** The vanilla villager and MCA's villagers ({@code mca:male_villager}, {@code mca:female_villager}). */
    static boolean isVillager(EntityType<?> type) {
        if (type == EntityType.VILLAGER) {
            return true;
        }
        ResourceLocation id = BuiltInRegistries.ENTITY_TYPE.getKey(type);
        return id.getNamespace().equals(MODID) && id.getPath().endsWith("_villager") && !id.getPath().contains("zombie");
    }
}
