package com.mythsofworlds.mythology.norse.client;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.client.model.ParrotModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.animal.Parrot;

/**
 * The parrot's body and wing flapping with one texture in the parrot layout: the black raven (textures/entity/raven.png)
 * or another bird, such as the Firebird of Nav.
 */
public class RavenRenderer extends MobRenderer<Parrot, ParrotModel> {
    private final ResourceLocation texture;

    public RavenRenderer(EntityRendererProvider.Context context) {
        this(context, "raven");
    }

    public RavenRenderer(EntityRendererProvider.Context context, String name) {
        super(context, new ParrotModel(context.bakeLayer(ModelLayers.PARROT)), 0.3F);
        this.texture = MythsOfWorlds.id("textures/entity/" + name + ".png");
    }

    @Override
    public ResourceLocation getTextureLocation(Parrot entity) {
        return texture;
    }

    @Override
    protected float getBob(Parrot entity, float partialTick) {
        float flap = Mth.lerp(partialTick, entity.oFlap, entity.flap);
        float speed = Mth.lerp(partialTick, entity.oFlapSpeed, entity.flapSpeed);
        return (Mth.sin(flap) + 1.0F) * speed;
    }
}
