package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.entity.Pegasus;
import net.minecraft.client.renderer.entity.AbstractHorseRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;

public class PegasusRenderer extends AbstractHorseRenderer<Pegasus, PegasusModel> {
    private static final ResourceLocation TEXTURE = MythsOfWorlds.id("textures/entity/pegasus.png");

    public PegasusRenderer(EntityRendererProvider.Context context) {
        super(context, new PegasusModel(context.bakeLayer(GreekClient.PEGASUS)), 1.1F);
    }

    @Override
    public ResourceLocation getTextureLocation(Pegasus entity) {
        return TEXTURE;
    }
}
