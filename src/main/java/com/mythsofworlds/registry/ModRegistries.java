package com.mythsofworlds.registry;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Items;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Shared registers. Each mythology (see the {@code mythology} package) adds its own blocks, items and mobs here.
 * Everything registered in {@link #ITEMS} shows up in the creative tab automatically.
 */
public final class ModRegistries {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(MythsOfWorlds.MODID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MythsOfWorlds.MODID);
    public static final DeferredRegister<EntityType<?>> ENTITY_TYPES =
            DeferredRegister.create(Registries.ENTITY_TYPE, MythsOfWorlds.MODID);
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MythsOfWorlds.MODID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> MAIN_TAB = TABS.register("main",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup." + MythsOfWorlds.MODID))
                    .icon(() -> ITEMS.getEntries().stream().findFirst()
                            .map(item -> item.get().getDefaultInstance())
                            .orElse(Items.BOOK.getDefaultInstance()))
                    .displayItems((params, output) -> ITEMS.getEntries().forEach(item -> output.accept(item.get())))
                    .build());

    private ModRegistries() {
    }

    public static void register(IEventBus modBus) {
        BLOCKS.register(modBus);
        ITEMS.register(modBus);
        ENTITY_TYPES.register(modBus);
        TABS.register(modBus);
    }
}
