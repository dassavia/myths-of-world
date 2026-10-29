package com.mythsofworlds.mixin;

import com.mythsofworlds.core.back.BackSlot;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Redirect;

/** Lets a player start gliding with an elytra on the back (see {@link BackSlot#flyingStack}). */
@Mixin(Player.class)
public abstract class PlayerMixin {
    @Redirect(method = "tryToStartFallFlying", at = @At(value = "INVOKE",
            target = "Lnet/minecraft/world/entity/player/Player;getItemBySlot(Lnet/minecraft/world/entity/EquipmentSlot;)Lnet/minecraft/world/item/ItemStack;"))
    private ItemStack mythsofworlds$backElytra(Player player, EquipmentSlot slot) {
        ItemStack stack = player.getItemBySlot(slot);
        return slot == EquipmentSlot.CHEST ? BackSlot.flyingStack(player, stack) : stack;
    }
}
