package com.mythsofworlds.mixin;

import com.mythsofworlds.core.back.BackSlot;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** The client asks to glide when jumping in the air with an elytra on the back (see {@link BackSlot#flyingStack}). */
@Mixin(LocalPlayer.class)
public abstract class LocalPlayerMixin {
    @Redirect(method = "aiStep", at = @At(value = "INVOKE",
            target = "Lnet/minecraft/client/player/LocalPlayer;getItemBySlot(Lnet/minecraft/world/entity/EquipmentSlot;)Lnet/minecraft/world/item/ItemStack;"))
    private ItemStack mythsofworlds$backElytra(LocalPlayer player, EquipmentSlot slot) {
        ItemStack stack = player.getItemBySlot(slot);
        return slot == EquipmentSlot.CHEST ? BackSlot.flyingStack(player, stack) : stack;
    }
}
