package com.mythsofworlds.mythology.greek.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.entity.GreekMerchant;
import net.minecraft.client.model.VillagerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.layers.CrossedArmsItemLayer;
import net.minecraft.resources.ResourceLocation;

/** Villager body in a chiton; each kind of merchant has its own texture (textures/entity/greek_merchant_&lt;kind&gt;.png). */
public class GreekMerchantRenderer extends MobRenderer<GreekMerchant, VillagerModel<GreekMerchant>> {
    private static final ResourceLocation[] TEXTURES = new ResourceLocation[GreekMerchant.KINDS];

    static {
        for (int kind = 0; kind < GreekMerchant.KINDS; kind++) {
            TEXTURES[kind] = MythsOfWorlds.id("textures/entity/greek_merchant_" + kind + ".png");
        }
    }

    public GreekMerchantRenderer(EntityRendererProvider.Context context) {
        super(context, new VillagerModel<>(context.bakeLayer(ModelLayers.WANDERING_TRADER)), 0.5F);
        addLayer(new CrossedArmsItemLayer<>(this, context.getItemInHandRenderer()));
    }

    @Override
    public ResourceLocation getTextureLocation(GreekMerchant entity) {
        return TEXTURES[entity.getKind()];
    }

    @Override
    protected void scale(GreekMerchant entity, PoseStack poseStack, float partialTick) {
        poseStack.scale(0.9375F, 0.9375F, 0.9375F);
    }
}
