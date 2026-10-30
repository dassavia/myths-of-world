package com.mythsofworlds.registry;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.attachment.AttachmentType;
import net.neoforged.neoforge.registries.DeferredRegister;
import net.neoforged.neoforge.registries.NeoForgeRegistries;

/**
 * Shared registers. Each mythology (see the {@code mythology} package) adds its own blocks, items and mobs here.
 * Everything registered in {@link #ITEMS} shows up in the creative tab automatically.
 */
public final class ModRegistries {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(MythsOfWorlds.MODID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MythsOfWorlds.MODID);
    public static final DeferredRegister<EntityType<?>> ENTITY_TYPES =
            DeferredRegister.create(Registries.ENTITY_TYPE, MythsOfWorlds.MODID);
    public static final DeferredRegister<SoundEvent> SOUNDS =
            DeferredRegister.create(Registries.SOUND_EVENT, MythsOfWorlds.MODID);
    public static final DeferredRegister<Feature<?>> FEATURES =
            DeferredRegister.create(Registries.FEATURE, MythsOfWorlds.MODID);
    /** Data the mod keeps on players (journal entries, spouse); see {@link com.mythsofworlds.core.PlayerData}. */
    public static final DeferredRegister<AttachmentType<?>> ATTACHMENT_TYPES =
            DeferredRegister.create(NeoForgeRegistries.Keys.ATTACHMENT_TYPES, MythsOfWorlds.MODID);
    public static final DeferredRegister<ArmorMaterial> ARMOR_MATERIALS =
            DeferredRegister.create(Registries.ARMOR_MATERIAL, MythsOfWorlds.MODID);
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MythsOfWorlds.MODID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> MAIN_TAB = TABS.register("main",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup." + MythsOfWorlds.MODID))
                    // The flaming sword of Surtr, as on the mod's logo.
                    .icon(() -> BuiltInRegistries.ITEM.getOptional(MythsOfWorlds.id("surtr_sword"))
                            .map(Item::getDefaultInstance)
                            .orElse(Items.BOOK.getDefaultInstance()))
                    // The old journals of each world are replaced by the Codex of Myths: kept registered, not listed.
                    .displayItems((params, output) -> ITEMS.getEntries().stream()
                            .filter(item -> !(item.get() instanceof com.mythsofworlds.journal.JournalItem))
                            .forEach(item -> output.accept(item.get())))
                    .build());

    private ModRegistries() {
    }

    public static void register(IEventBus modBus) {
        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        ENTITY_TYPES.register(modBus);
        SOUNDS.register(modBus);
        FEATURES.register(modBus);
        ATTACHMENT_TYPES.register(modBus);
        ARMOR_MATERIALS.register(modBus);
        com.mythsofworlds.mythology.relic.MythAttributes.ATTRIBUTES.register(modBus);
        TABS.register(modBus);
    }
}
