package com.mythsofworlds.mixin;

import com.mythsofworlds.core.client.MythHud;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;

/** While the HUD of the myths is on, the survival inventory is drawn on its parchment (see {@link MythHud#INVENTORY}). */
@Mixin(InventoryScreen.class)
public abstract class InventoryScreenMixin {
    @ModifyArg(method = "renderBg", at = @At(value = "INVOKE",
            target = "Lnet/minecraft/client/gui/GuiGraphics;blit(Lnet/minecraft/resources/ResourceLocation;IIIIII)V"), index = 0)
    private ResourceLocation mythsofworlds$background(ResourceLocation texture) {
        return MythHud.enabled() ? MythHud.INVENTORY : texture;
    }
}
