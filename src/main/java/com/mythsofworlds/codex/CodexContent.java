package com.mythsofworlds.codex;

import net.minecraft.world.item.Item;
import net.minecraft.world.item.Rarity;
import net.neoforged.neoforge.registries.DeferredItem;

import static com.mythsofworlds.registry.ModRegistries.ITEMS;

/** The Codex of Myths, the one book of the mod. */
public final class CodexContent {
    public static final DeferredItem<CodexItem> CODEX = ITEMS.register("codex",
            () -> new CodexItem(new Item.Properties().stacksTo(1).rarity(Rarity.UNCOMMON)));

    private CodexContent() {
    }

    /** Called from the mod constructor so the fields above are registered. */
    public static void init() {
    }
}
