package com.mythsofworlds.compat.mca;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.norse.entity.Valkyrie;
import java.util.function.Function;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.resources.ResourceLocation;

/**
 * Draws the rest of an MCA look ({@link McaSkins}) over the skin the renderer already drew: the face, the clothes and
 * the hair tinted to her colour, on the same model in the same pose. A valkyrie keeps her winged helmet: the hat layer
 * of her own texture is drawn last. Draws nothing when the woman has no MCA look.
 */
public class McaLookLayer extends RenderLayer<Amazon, PlayerModel<Amazon>> {
    private final Function<Amazon, McaSkins.Look> looks;
    private final Function<Amazon, ResourceLocation> ownTexture;

    public McaLookLayer(RenderLayerParent<Amazon, PlayerModel<Amazon>> parent, Function<Amazon, McaSkins.Look> looks,
                        Function<Amazon, ResourceLocation> ownTexture) {
        super(parent);
        this.looks = looks;
        this.ownTexture = ownTexture;
    }

    @Override
    public void render(PoseStack pose, MultiBufferSource buffers, int light, Amazon entity, float limbSwing, float limbSwingAmount,
                       float partialTick, float ageInTicks, float netHeadYaw, float headPitch) {
        McaSkins.Look look = looks.apply(entity);
        if (look == null || entity.isInvisible()) {
            return;
        }
        PlayerModel<Amazon> model = getParentModel();
        renderColoredCutoutModel(model, look.face(), pose, buffers, light, entity, -1);
        renderColoredCutoutModel(model, look.clothes(), pose, buffers, light, entity, -1);
        renderColoredCutoutModel(model, look.hair(), pose, buffers, light, entity, look.hairColour());
        if (entity instanceof Valkyrie) {
            onlyHat(model, true);
            renderColoredCutoutModel(model, ownTexture.apply(entity), pose, buffers, light, entity, -1);
            onlyHat(model, false);
        }
    }

    /** Shows only the hat layer of the model (true), or everything again (false). */
    private static void onlyHat(PlayerModel<?> model, boolean only) {
        model.setAllVisible(!only);
        model.hat.visible = true;
        if (only) {
            model.head.visible = false;
        }
    }
}
