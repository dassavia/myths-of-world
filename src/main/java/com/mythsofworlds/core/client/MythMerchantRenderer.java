package com.mythsofworlds.core.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.entity.MythMerchant;
import net.minecraft.client.model.VillagerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.layers.CrossedArmsItemLayer;
import net.minecraft.resources.ResourceLocation;

/**
 * Villager body; each kind of trader has its own texture (textures/entity/&lt;name&gt;_&lt;kind&gt;.png). The short kinds
 * ({@link MythMerchant#isShort()}: the dwarf smith of Jotunheim, Baba Yaga in Nav) are drawn small and stocky.
 */
public class MythMerchantRenderer<T extends MythMerchant> extends MobRenderer<T, VillagerModel<T>> {
    private final ResourceLocation[] textures = new ResourceLocation[MythMerchant.KINDS];

    public MythMerchantRenderer(EntityRendererProvider.Context context, String name) {
        super(context, new VillagerModel<>(context.bakeLayer(ModelLayers.WANDERING_TRADER)), 0.5F);
        addLayer(new CrossedArmsItemLayer<>(this, context.getItemInHandRenderer()));
        for (int kind = 0; kind < MythMerchant.KINDS; kind++) {
            textures[kind] = MythsOfWorlds.id("textures/entity/" + name + "_" + kind + ".png");
        }
    }

    @Override
    public ResourceLocation getTextureLocation(T entity) {
        return textures[entity.getKind()];
    }

    @Override
    protected void scale(T entity, PoseStack poseStack, float partialTick) {
        if (entity.isShort()) {
            poseStack.scale(0.8F, 0.7F, 0.8F);
        } else {
            poseStack.scale(0.9375F, 0.9375F, 0.9375F);
        }
    }
}
