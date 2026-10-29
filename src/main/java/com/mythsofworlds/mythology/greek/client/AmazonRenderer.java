package com.mythsofworlds.mythology.greek.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.greek.entity.Hippolyta;
import java.util.HashMap;
import java.util.Map;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.resources.ResourceLocation;

/**
 * Amazons, Hippolyta and the valkyries of Jotunheim: the classic wide player model (with its hair and dress overlay
 * layers) and the texture {@link Amazon#textureName()} names: amazon_0 to amazon_15 (4 is the royal look of
 * Hippolyta's daughters), hippolyta, valkyrie_0 to valkyrie_7. Every one is a little taller or shorter than the next.
 */
public class AmazonRenderer extends HumanoidMobRenderer<Amazon, PlayerModel<Amazon>> {
    private static final Map<String, ResourceLocation> TEXTURES = new HashMap<>();

    public AmazonRenderer(EntityRendererProvider.Context context) {
        super(context, new PlayerModel<>(context.bakeLayer(ModelLayers.PLAYER), false), 0.5F);
    }

    @Override
    public ResourceLocation getTextureLocation(Amazon entity) {
        return TEXTURES.computeIfAbsent(entity.textureName(), name -> MythsOfWorlds.id("textures/entity/" + name + ".png"));
    }

    @Override
    protected void scale(Amazon entity, PoseStack poseStack, float partialTick) {
        float scale = entity instanceof Hippolyta ? 1.0F : 0.92F + Math.floorMod(entity.getUUID().hashCode(), 5) * 0.02F;
        poseStack.scale(scale, scale, scale);
    }
}
