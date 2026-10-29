package com.mythsofworlds.mythology.greek.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.greek.entity.Hippolyta;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.resources.ResourceLocation;

/**
 * Amazons and Hippolyta: the slim player model (with its hair and armour overlay layers) and a texture per look,
 * textures/entity/amazon_&lt;variant&gt;.png, 0 to 9 (4 is the royal look of Hippolyta's daughters) and hippolyta.png.
 */
public class AmazonRenderer extends HumanoidMobRenderer<Amazon, PlayerModel<Amazon>> {
    private static final ResourceLocation[] TEXTURES = new ResourceLocation[Amazon.VARIANTS];
    private static final ResourceLocation HIPPOLYTA = MythsOfWorlds.id("textures/entity/hippolyta.png");

    static {
        for (int variant = 0; variant < Amazon.VARIANTS; variant++) {
            TEXTURES[variant] = MythsOfWorlds.id("textures/entity/amazon_" + variant + ".png");
        }
    }

    public AmazonRenderer(EntityRendererProvider.Context context) {
        super(context, new PlayerModel<>(context.bakeLayer(ModelLayers.PLAYER_SLIM), true), 0.5F);
    }

    @Override
    public ResourceLocation getTextureLocation(Amazon entity) {
        if (entity instanceof Hippolyta) {
            return HIPPOLYTA;
        }
        return TEXTURES[Math.floorMod(entity.getVariant(), TEXTURES.length)];
    }

    @Override
    protected void scale(Amazon entity, PoseStack poseStack, float partialTick) {
        float scale = entity instanceof Hippolyta ? 1.0F : 0.95F;
        poseStack.scale(scale, scale, scale);
    }
}
