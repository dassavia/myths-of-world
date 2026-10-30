package com.mythsofworlds.core.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.Mob;

/** Renders any mob with one texture (textures/entity/&lt;name&gt;.png), optionally scaled up; babies at half size. */
public class MythMobRenderer<T extends Mob, M extends EntityModel<T>> extends MobRenderer<T, M> {
    private final ResourceLocation texture;
    private final float scale;

    public MythMobRenderer(EntityRendererProvider.Context context, M model, String name, float scale) {
        super(context, model, 0.5F * scale);
        this.texture = MythsOfWorlds.id("textures/entity/" + name + ".png");
        this.scale = scale;
    }

    @Override
    public ResourceLocation getTextureLocation(T entity) {
        return texture;
    }

    @Override
    protected void scale(T entity, PoseStack poseStack, float partialTick) {
        float size = entity.isBaby() ? scale * 0.5F : scale;
        poseStack.scale(size, size, size);
    }
}
