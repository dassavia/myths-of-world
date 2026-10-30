package com.mythsofworlds.core.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.Mob;
import org.jetbrains.annotations.Nullable;

/** Humanoid mob with held items, one texture, optional scale, optionally see-through (uses the texture's alpha). */
public class MythHumanoidRenderer<T extends Mob, M extends HumanoidModel<T>> extends HumanoidMobRenderer<T, M> {
    private final ResourceLocation texture;
    private final float scale;
    private final boolean translucent;

    public MythHumanoidRenderer(EntityRendererProvider.Context context, M model, String name, float scale, boolean translucent) {
        super(context, model, 0.5F * scale);
        this.texture = MythsOfWorlds.id("textures/entity/" + name + ".png");
        this.scale = scale;
        this.translucent = translucent;
    }

    @Override
    public ResourceLocation getTextureLocation(T entity) {
        return texture;
    }

    @Override
    protected void scale(T entity, PoseStack poseStack, float partialTick) {
        poseStack.scale(scale, scale, scale);
    }

    @Nullable
    @Override
    protected RenderType getRenderType(T entity, boolean bodyVisible, boolean translucentInvisible, boolean glowing) {
        if (translucent && bodyVisible) {
            return RenderType.entityTranslucent(texture);
        }
        return super.getRenderType(entity, bodyVisible, translucentInvisible, glowing);
    }
}
