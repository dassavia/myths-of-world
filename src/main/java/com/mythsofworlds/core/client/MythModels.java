package com.mythsofworlds.core.client;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Model layers shared by the mobs of every mythology: the plain humanoid body and the four-legged wolf. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class MythModels {
    /** Steve's body, for {@link MythHumanoidRenderer} with a {@code HumanoidModel} or {@link ZombieArmsModel}. */
    public static final ModelLayerLocation HUMANOID = new ModelLayerLocation(MythsOfWorlds.id("humanoid"), "main");
    /** A wolf with one head, for {@link BeastModel}: wargs and volkolaks. */
    public static final ModelLayerLocation WOLF = new ModelLayerLocation(MythsOfWorlds.id("wolf"), "main");

    private MythModels() {
    }

    @SubscribeEvent
    public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.registerLayerDefinition(HUMANOID, () -> LayerDefinition.create(HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F), 64, 64));
        event.registerLayerDefinition(WOLF, () -> BeastModel.createBodyLayer(1, false));
    }
}
