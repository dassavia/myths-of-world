package com.mythsofworlds.mythology.egyptian.client;

import com.mojang.datafixers.util.Pair;
import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.client.model.BoatModel;
import net.minecraft.client.model.ListModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.BoatRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.vehicle.Boat;

/** The traveller's boat is drawn with the vanilla boat model and renderer, only with its own papyrus texture. */
public class TravelersBoatRenderer extends BoatRenderer {
    public static final ResourceLocation TEXTURE = MythsOfWorlds.id("textures/entity/boat/travelers_boat.png");
    private final Pair<ResourceLocation, ListModel<Boat>> look;

    public TravelersBoatRenderer(EntityRendererProvider.Context context) {
        super(context, false);
        this.look = Pair.of(TEXTURE, new BoatModel(context.bakeLayer(ModelLayers.createBoatModelName(Boat.Type.OAK))));
    }

    @Override
    public Pair<ResourceLocation, ListModel<Boat>> getModelWithLocation(Boat boat) {
        return look;
    }
}
