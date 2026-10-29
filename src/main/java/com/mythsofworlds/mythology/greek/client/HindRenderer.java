package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.entity.GoldenHind;
import net.minecraft.client.renderer.entity.AbstractHorseRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;

public class HindRenderer extends AbstractHorseRenderer<GoldenHind, HindModel> {
    private static final ResourceLocation TEXTURE = MythsOfWorlds.id("textures/entity/golden_hind.png");

    public HindRenderer(EntityRendererProvider.Context context) {
        super(context, new HindModel(context.bakeLayer(GreekClient.GOLDEN_HIND)), 0.9F);
    }

    @Override
    public ResourceLocation getTextureLocation(GoldenHind entity) {
        return TEXTURE;
    }
}
