package com.mythsofworlds.core;

import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.CustomData;

/** Small values a relic remembers about itself (the knot of Ariadne's thread, the last feast of the tablecloth...). */
public final class StackData {
    private StackData() {
    }

    public static CompoundTag read(ItemStack stack) {
        return stack.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag();
    }

    public static boolean has(ItemStack stack, String key) {
        return read(stack).contains(key);
    }

    public static long getLong(ItemStack stack, String key, long fallback) {
        CompoundTag tag = read(stack);
        return tag.contains(key) ? tag.getLong(key) : fallback;
    }

    public static void putLong(ItemStack stack, String key, long value) {
        CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> tag.putLong(key, value));
    }

    public static String getString(ItemStack stack, String key) {
        return read(stack).getString(key);
    }

    public static void putString(ItemStack stack, String key, String value) {
        CustomData.update(DataComponents.CUSTOM_DATA, stack, tag -> tag.putString(key, value));
    }
}
