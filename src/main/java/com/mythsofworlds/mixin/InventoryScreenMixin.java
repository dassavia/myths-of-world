package com.mythsofworlds.mixin;

import com.mythsofworlds.core.client.MythHud;
import net.minecraft.client.gui.components.WidgetSprites;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;

/**
 * While the HUD of the myths is on, the survival inventory is drawn on its parchment (see {@link MythHud#INVENTORY})
 * and the recipe book button sits in the gold niche of the parchment ({@link MythHud#RECIPE_BUTTON}).
 */
@Mixin(InventoryScreen.class)
public abstract class InventoryScreenMixin {
    @ModifyArg(method = "renderBg", at = @At(value = "INVOKE",
            target = "Lnet/minecraft/client/gui/GuiGraphics;blit(Lnet/minecraft/resources/ResourceLocation;IIIIII)V"), index = 0)
    private ResourceLocation mythsofworlds$background(ResourceLocation texture) {
        return MythHud.background(texture);
    }

    @ModifyArg(method = "init", at = @At(value = "INVOKE", target = "Lnet/minecraft/client/gui/components/ImageButton;<init>"
            + "(IIIILnet/minecraft/client/gui/components/WidgetSprites;Lnet/minecraft/client/gui/components/Button$OnPress;)V"),
            index = 4)
    private WidgetSprites mythsofworlds$recipeButton(WidgetSprites sprites) {
        return MythHud.recipeButton(sprites);
    }
}
