package com.mythsofworlds.mythology.norse.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.norse.entity.NorseMerchant;
import net.minecraft.client.model.VillagerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.layers.CrossedArmsItemLayer;
import net.minecraft.resources.ResourceLocation;

/**
 * Villager body; each kind of trader has its own texture (textures/entity/&lt;name&gt;_&lt;kind&gt;.png). Kind 1 (the dwarf
 * smith of Jotunheim, Baba Yaga in Nav) is short.
 */
public class NorseMerchantRenderer extends MobRenderer<NorseMerchant, VillagerModel<NorseMerchant>> {
    private final ResourceLocation[] textures = new ResourceLocation[NorseMerchant.KINDS];

    public NorseMerchantRenderer(EntityRendererProvider.Context context) {
        this(context, "norse_merchant");
    }

    public NorseMerchantRenderer(EntityRendererProvider.Context context, String name) {
        super(context, new VillagerModel<>(context.bakeLayer(ModelLayers.WANDERING_TRADER)), 0.5F);
        addLayer(new CrossedArmsItemLayer<>(this, context.getItemInHandRenderer()));
        for (int kind = 0; kind < NorseMerchant.KINDS; kind++) {
            textures[kind] = MythsOfWorlds.id("textures/entity/" + name + "_" + kind + ".png");
        }
    }

    @Override
    public ResourceLocation getTextureLocation(NorseMerchant entity) {
        return textures[entity.getKind()];
    }

    @Override
    protected void scale(NorseMerchant entity, PoseStack poseStack, float partialTick) {
        if (entity.getKind() == NorseMerchant.DWARF) {
            poseStack.scale(0.8F, 0.7F, 0.8F);
        } else {
            poseStack.scale(0.9375F, 0.9375F, 0.9375F);
        }
    }
}
