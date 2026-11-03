package com.mythsofworlds.mythology.egyptian.client;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.client.renderer.entity.CatRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.Cat;

/** The vanilla cat with the coat of the cats of Bastet: black, with golden eyes and a gold ring in one ear. */
public class BastetCatRenderer extends CatRenderer {
    private static final ResourceLocation TEXTURE = MythsOfWorlds.id("textures/entity/bastet_cat.png");

    public BastetCatRenderer(EntityRendererProvider.Context context) {
        super(context);
    }

    @Override
    public ResourceLocation getTextureLocation(Cat entity) {
        return TEXTURE;
    }
}
