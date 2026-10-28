package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.entity.Spartoi;
import net.minecraft.client.model.SkeletonModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.client.renderer.entity.layers.HumanoidArmorLayer;
import net.minecraft.resources.ResourceLocation;

/** Vanilla skeleton model with its own bones texture and the golden helmet drawn by the armor layer. */
public class SpartoiRenderer extends HumanoidMobRenderer<Spartoi, SkeletonModel<Spartoi>> {
    private static final ResourceLocation TEXTURE = MythsOfWorlds.id("textures/entity/spartoi.png");

    public SpartoiRenderer(EntityRendererProvider.Context context) {
        super(context, new SkeletonModel<>(context.bakeLayer(ModelLayers.SKELETON)), 0.5F);
        addLayer(new HumanoidArmorLayer<>(this,
                new SkeletonModel<>(context.bakeLayer(ModelLayers.SKELETON_INNER_ARMOR)),
                new SkeletonModel<>(context.bakeLayer(ModelLayers.SKELETON_OUTER_ARMOR)),
                context.getModelManager()));
    }

    @Override
    public ResourceLocation getTextureLocation(Spartoi entity) {
        return TEXTURE;
    }
}
