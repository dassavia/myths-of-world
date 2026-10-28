package com.mythsofworlds.registry;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModCreativeTabs {
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MythsOfWorlds.MODID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> MAIN = TABS.register("main",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup." + MythsOfWorlds.MODID))
                    .icon(() -> ModItems.BIFROST_RUNE.get().getDefaultInstance())
                    .displayItems((params, output) -> {
                        output.accept(ModItems.RUNESTONE.get());
                        output.accept(ModItems.BIFROST_RUNE.get());
                    })
                    .build());

    private ModCreativeTabs() {
    }
}
