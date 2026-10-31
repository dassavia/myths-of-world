package com.mythsofworlds.mixin;

import com.mythsofworlds.core.client.MythHud;
import net.minecraft.client.gui.components.WidgetSprites;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyArg;
import top.theillusivec4.curios.client.gui.CuriosScreen;

/**
 * The Curios screen (opened by the back slot's button) on the same parchment as the survival inventory while the HUD
 * of the myths is on: the inventory, the accessory panel beside it (its slots are drawn in a lambda of renderBg) and
 * the recipe book button. Without this, opening the back slot fell back to the vanilla look.
 */
@Mixin(CuriosScreen.class)
public abstract class CuriosScreenMixin {
    @ModifyArg(method = {"renderBg", "lambda$renderBg$5"}, at = @At(value = "INVOKE",
            target = "Lnet/minecraft/client/gui/GuiGraphics;blit(Lnet/minecraft/resources/ResourceLocation;IIIIII)V"), index = 0,
            require = 1)
    private ResourceLocation mythsofworlds$background(ResourceLocation texture) {
        return MythHud.background(texture);
    }

    @ModifyArg(method = "init", at = @At(value = "INVOKE", target = "Lnet/minecraft/client/gui/components/ImageButton;<init>"
            + "(IIIILnet/minecraft/client/gui/components/WidgetSprites;Lnet/minecraft/client/gui/components/Button$OnPress;)V"),
            index = 4, require = 0)
    private WidgetSprites mythsofworlds$recipeButton(WidgetSprites sprites) {
        return MythHud.recipeButton(sprites);
    }
}
