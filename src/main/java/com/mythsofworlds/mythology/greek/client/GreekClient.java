package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.core.client.MythGeoRenderer;
import com.mythsofworlds.core.client.MythMerchantRenderer;
import com.mythsofworlds.core.client.BeastModel;
import com.mythsofworlds.core.client.MythHumanoidRenderer;
import com.mythsofworlds.core.client.MythMobRenderer;
import com.mythsofworlds.core.client.MythModels;
import com.mythsofworlds.core.client.ZombieArmsModel;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.entity.Karkinos;
import com.mythsofworlds.mythology.greek.entity.Lion;
import com.mythsofworlds.mythology.greek.entity.HydraHatchling;
import net.minecraft.client.renderer.entity.ThrownItemRenderer;
import net.minecraft.client.renderer.entity.player.PlayerRenderer;
import net.minecraft.client.resources.PlayerSkin;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Client side of the Greek mobs: which model and texture each one is drawn with. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class GreekClient {
    public static final ModelLayerLocation HARPY = layer("harpy");
    public static final ModelLayerLocation PEGASUS = layer("pegasus");
    public static final ModelLayerLocation NEMEAN_LION = layer("nemean_lion");
    public static final ModelLayerLocation HYDRA = layer("hydra");
    public static final ModelLayerLocation GOLDEN_HIND = layer("golden_hind");
    public static final ModelLayerLocation KARKINOS = layer("karkinos");

    private GreekClient() {
    }

    private static ModelLayerLocation layer(String name) {
        return new ModelLayerLocation(MythsOfWorlds.id(name), "main");
    }

    @SubscribeEvent
    public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.registerLayerDefinition(HARPY, HarpyModel::createBodyLayer);
        event.registerLayerDefinition(PEGASUS, PegasusModel::createBodyLayer);
        event.registerLayerDefinition(NEMEAN_LION, () -> BeastModel.createBodyLayer(1, true));
        event.registerLayerDefinition(HYDRA, HydraModel::createBodyLayer);
        event.registerLayerDefinition(GOLDEN_HIND, HindModel::createBodyLayer);
        event.registerLayerDefinition(KARKINOS, CrayfishModel::createBodyLayer);
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(GreekEntities.SATYR.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(MythModels.HUMANOID)), "satyr", 0.95F, false));
        event.registerEntityRenderer(GreekEntities.HARPY.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new HarpyModel(ctx.bakeLayer(HARPY)), "harpy", 0.9F, false));
        event.registerEntityRenderer(GreekEntities.SPARTOI.get(), SpartoiRenderer::new);
        event.registerEntityRenderer(GreekEntities.GROWTH_POTION.get(), ThrownItemRenderer::new);
        event.registerEntityRenderer(GreekEntities.SHADE.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(MythModels.HUMANOID)), "shade", 1.0F, true));
        event.registerEntityRenderer(GreekEntities.PEGASUS.get(), PegasusRenderer::new);
        event.registerEntityRenderer(GreekEntities.CYCLOPS.get(), ctx -> new MythGeoRenderer<>(ctx, "cyclops", 1.2F));
        event.registerEntityRenderer(GreekEntities.MEDUSA.get(), ctx -> new MythGeoRenderer<>(ctx, "medusa", 0.5F));
        event.registerEntityRenderer(GreekEntities.NEMEAN_LION.get(), ctx -> new MythGeoRenderer<>(ctx, "nemean_lion", 0.9F));
        event.registerEntityRenderer(GreekEntities.MINOTAUR.get(), ctx -> new MythGeoRenderer<>(ctx, "minotaur", 0.8F));
        event.registerEntityRenderer(GreekEntities.HYDRA.get(), ctx -> new MythGeoRenderer<>(ctx, "hydra", 1.5F));
        event.registerEntityRenderer(GreekEntities.HYDRA_HATCHLING.get(),
                ctx -> new MythMobRenderer<HydraHatchling, HydraModel<HydraHatchling>>(ctx, new HydraModel<>(ctx.bakeLayer(HYDRA)),
                        "hydra_hatchling", 0.45F));
        event.registerEntityRenderer(GreekEntities.GOLDEN_HIND.get(), HindRenderer::new);
        event.registerEntityRenderer(GreekEntities.GREEK_MERCHANT.get(), ctx -> new MythMerchantRenderer<>(ctx, "greek_merchant"));
        event.registerEntityRenderer(GreekEntities.LION.get(),
                ctx -> new MythMobRenderer<Lion, BeastModel<Lion>>(ctx, new BeastModel<>(ctx.bakeLayer(NEMEAN_LION), 1), "lion", 0.85F));
        event.registerEntityRenderer(GreekEntities.KARKINOS.get(),
                ctx -> new MythMobRenderer<Karkinos, CrayfishModel<Karkinos>>(ctx, new CrayfishModel<>(ctx.bakeLayer(KARKINOS)), "karkinos", 0.65F));
        event.registerEntityRenderer(GreekEntities.AMAZON.get(), AmazonRenderer::new);
        event.registerEntityRenderer(GreekEntities.HIPPOLYTA.get(), AmazonRenderer::new);
        event.registerEntityRenderer(GreekEntities.CERBERUS.get(), ctx -> new MythGeoRenderer<>(ctx, "cerberus", 1.1F));
    }

    /** Players wearing the wings of Daedalus show them on their back. */
    @SubscribeEvent
    public static void addLayers(EntityRenderersEvent.AddLayers event) {
        for (PlayerSkin.Model skin : event.getSkins()) {
            if (event.getSkin(skin) instanceof PlayerRenderer renderer) {
                renderer.addLayer(new WingsLayer<>(renderer, event.getEntityModels()));
            }
        }
    }
}
