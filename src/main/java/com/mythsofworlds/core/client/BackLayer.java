package com.mythsofworlds.core.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mythsofworlds.core.back.BackSlot;
import com.mythsofworlds.mythology.greek.client.WingsLayer;
import com.mythsofworlds.mythology.greek.item.WingsItem;
import net.minecraft.client.model.ElytraModel;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.model.geom.EntityModelSet;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.ItemRenderer;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.client.resources.PlayerSkin;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.PlayerModelPart;
import net.minecraft.world.item.ItemStack;

/**
 * Draws what a player carries on the back ({@link BackSlot}): an elytra (with the player's cape or elytra skin) or the
 * wings of Daedalus, the way vanilla draws an elytra in the chest slot. Nothing is drawn while the chest slot itself
 * holds an elytra or wings, which their own layers draw.
 */
public class BackLayer extends RenderLayer<AbstractClientPlayer, PlayerModel<AbstractClientPlayer>> {
    private static final ResourceLocation ELYTRA = ResourceLocation.withDefaultNamespace("textures/entity/elytra.png");
    private final ElytraModel<AbstractClientPlayer> model;

    public BackLayer(RenderLayerParent<AbstractClientPlayer, PlayerModel<AbstractClientPlayer>> renderer, EntityModelSet models) {
        super(renderer);
        this.model = new ElytraModel<>(models.bakeLayer(ModelLayers.ELYTRA));
    }

    @Override
    public void render(PoseStack poseStack, MultiBufferSource buffer, int light, AbstractClientPlayer player, float limbSwing,
                       float limbSwingAmount, float partialTick, float ageInTicks, float netHeadYaw, float headPitch) {
        ItemStack back = BackSlot.get(player);
        if (back.isEmpty() || BackSlot.canWear(player.getItemBySlot(EquipmentSlot.CHEST))) {
            return;
        }
        ResourceLocation texture;
        if (back.getItem() instanceof WingsItem) {
            texture = WingsLayer.TEXTURE;
        } else {
            PlayerSkin skin = player.getSkin();
            if (skin.elytraTexture() != null) {
                texture = skin.elytraTexture();
            } else if (skin.capeTexture() != null && player.isModelPartShown(PlayerModelPart.CAPE)) {
                texture = skin.capeTexture();
            } else {
                texture = ELYTRA;
            }
        }
        poseStack.pushPose();
        poseStack.translate(0.0F, 0.0F, 0.125F);
        getParentModel().copyPropertiesTo(model);
        model.setupAnim(player, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);
        VertexConsumer consumer = ItemRenderer.getArmorFoilBuffer(buffer, RenderType.armorCutoutNoCull(texture), back.hasFoil());
        model.renderToBuffer(poseStack, consumer, light, OverlayTexture.NO_OVERLAY);
        poseStack.popPose();
    }
}
