package com.mythsofworlds.mixin;

import com.mythsofworlds.core.back.BackSlot;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** Keeps an elytra on the back gliding (see {@link BackSlot#flyingStack}). */
@Mixin(LivingEntity.class)
public abstract class LivingEntityMixin {
    @Redirect(method = "updateFallFlying", at = @At(value = "INVOKE",
            target = "Lnet/minecraft/world/entity/LivingEntity;getItemBySlot(Lnet/minecraft/world/entity/EquipmentSlot;)Lnet/minecraft/world/item/ItemStack;"))
    private ItemStack mythsofworlds$backElytra(LivingEntity entity, EquipmentSlot slot) {
        ItemStack stack = entity.getItemBySlot(slot);
        return slot == EquipmentSlot.CHEST ? BackSlot.flyingStack(entity, stack) : stack;
    }
}
