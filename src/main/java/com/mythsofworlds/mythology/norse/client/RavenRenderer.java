package com.mythsofworlds.mythology.norse.client;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.client.model.ParrotModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.animal.Parrot;

/** The parrot's body and wing flapping, with the black raven texture (textures/entity/raven.png, parrot layout). */
public class RavenRenderer extends MobRenderer<Parrot, ParrotModel> {
    private static final ResourceLocation TEXTURE = MythsOfWorlds.id("textures/entity/raven.png");

    public RavenRenderer(EntityRendererProvider.Context context) {
        super(context, new ParrotModel(context.bakeLayer(ModelLayers.PARROT)), 0.3F);
    }

    @Override
    public ResourceLocation getTextureLocation(Parrot entity) {
        return TEXTURE;
    }

    @Override
    protected float getBob(Parrot entity, float partialTick) {
        float flap = Mth.lerp(partialTick, entity.oFlap, entity.flap);
        float speed = Mth.lerp(partialTick, entity.oFlapSpeed, entity.flapSpeed);
        return (Mth.sin(flap) + 1.0F) * speed;
    }
}
