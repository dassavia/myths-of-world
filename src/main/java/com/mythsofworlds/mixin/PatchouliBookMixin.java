package com.mythsofworlds.mixin;

import com.mythsofworlds.codex.CodexBook;
import com.mythsofworlds.core.ClientConfig;
import net.minecraft.network.chat.Style;
import net.minecraft.resources.ResourceLocation;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;
import vazkii.patchouli.common.book.Book;

/**
 * Patchouli draws every book in the Unifont (or the vanilla font) and has no setting for another one. Only the Codex
 * of Myths gets the clean font of the mod with full Cyrillic ({@link CodexBook#FONT}, assets/mythsofworlds/font/codex.json,
 * which falls back to the vanilla font for anything it lacks); every other book stays as it is.
 */
@Mixin(value = Book.class, remap = false)
public abstract class PatchouliBookMixin {
    @Shadow
    @Final
    public ResourceLocation id;

    @Inject(method = "getFontStyle", at = @At("HEAD"), cancellable = true)
    private void mythsofworlds$codexFont(CallbackInfoReturnable<Style> cir) {
        if (CodexBook.ID.equals(id) && ClientConfig.CODEX_FONT.get()) {
            cir.setReturnValue(Style.EMPTY.withFont(CodexBook.FONT));
        }
    }
}
