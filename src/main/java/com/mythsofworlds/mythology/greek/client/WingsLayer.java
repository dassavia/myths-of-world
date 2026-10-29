package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.GreekContent;
import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.EntityModelSet;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.ElytraLayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;

/** Draws the wings of Daedalus on the back of whoever wears them, with the elytra model and a feather texture. */
public class WingsLayer<T extends LivingEntity, M extends EntityModel<T>> extends ElytraLayer<T, M> {
    public static final ResourceLocation TEXTURE = MythsOfWorlds.id("textures/entity/wings_of_daedalus.png");

    public WingsLayer(RenderLayerParent<T, M> renderer, EntityModelSet models) {
        super(renderer, models);
    }

    @Override
    public boolean shouldRender(ItemStack stack, T entity) {
        return stack.is(GreekContent.WINGS_OF_DAEDALUS.get());
    }

    @Override
    public ResourceLocation getElytraTexture(ItemStack stack, T entity) {
        return TEXTURE;
    }
}
