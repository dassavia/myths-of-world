package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.entity.Cerberus;
import com.mythsofworlds.mythology.greek.entity.Karkinos;
import com.mythsofworlds.mythology.greek.entity.Lion;
import com.mythsofworlds.mythology.greek.entity.Hydra;
import com.mythsofworlds.mythology.greek.entity.HydraHatchling;
import com.mythsofworlds.mythology.greek.entity.NemeanLion;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.renderer.entity.player.PlayerRenderer;
import net.minecraft.client.resources.PlayerSkin;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Client side of the Greek mobs: which model and texture each one is drawn with. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class GreekClient {
    public static final ModelLayerLocation HUMANOID = layer("greek_humanoid");
    public static final ModelLayerLocation MINOTAUR = layer("minotaur");
    public static final ModelLayerLocation HARPY = layer("harpy");
    public static final ModelLayerLocation PEGASUS = layer("pegasus");
    public static final ModelLayerLocation NEMEAN_LION = layer("nemean_lion");
    public static final ModelLayerLocation CERBERUS = layer("cerberus");
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
        event.registerLayerDefinition(HUMANOID, () -> LayerDefinition.create(HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F), 64, 64));
        event.registerLayerDefinition(MINOTAUR, MinotaurModel::createBodyLayer);
        event.registerLayerDefinition(HARPY, HarpyModel::createBodyLayer);
        event.registerLayerDefinition(PEGASUS, PegasusModel::createBodyLayer);
        event.registerLayerDefinition(NEMEAN_LION, () -> BeastModel.createBodyLayer(1, true));
        event.registerLayerDefinition(CERBERUS, () -> BeastModel.createBodyLayer(3, false));
        event.registerLayerDefinition(HYDRA, HydraModel::createBodyLayer);
        event.registerLayerDefinition(GOLDEN_HIND, HindModel::createBodyLayer);
        event.registerLayerDefinition(KARKINOS, CrabModel::createBodyLayer);
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        event.registerEntityRenderer(GreekEntities.SATYR.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(HUMANOID)), "satyr", 0.95F, false));
        event.registerEntityRenderer(GreekEntities.HARPY.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HarpyModel(ctx.bakeLayer(HARPY)), "harpy", 0.9F, false));
        event.registerEntityRenderer(GreekEntities.SPARTOI.get(), SpartoiRenderer::new);
        event.registerEntityRenderer(GreekEntities.SHADE.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(HUMANOID)), "shade", 1.0F, true));
        event.registerEntityRenderer(GreekEntities.PEGASUS.get(), PegasusRenderer::new);
        event.registerEntityRenderer(GreekEntities.CYCLOPS.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(HUMANOID)), "cyclops", 2.2F, false));
        event.registerEntityRenderer(GreekEntities.MEDUSA.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(HUMANOID)), "medusa", 1.1F, false));
        event.registerEntityRenderer(GreekEntities.NEMEAN_LION.get(),
                ctx -> new GreekMobRenderer<NemeanLion, BeastModel<NemeanLion>>(ctx, new BeastModel<>(ctx.bakeLayer(NEMEAN_LION), 1),
                        "nemean_lion", 1.3F));
        event.registerEntityRenderer(GreekEntities.MINOTAUR.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new MinotaurModel(ctx.bakeLayer(MINOTAUR)), "minotaur", 1.5F, false));
        event.registerEntityRenderer(GreekEntities.HYDRA.get(),
                ctx -> new GreekMobRenderer<Hydra, HydraModel<Hydra>>(ctx, new HydraModel<>(ctx.bakeLayer(HYDRA)), "hydra", 1.8F));
        event.registerEntityRenderer(GreekEntities.HYDRA_HATCHLING.get(),
                ctx -> new GreekMobRenderer<HydraHatchling, HydraModel<HydraHatchling>>(ctx, new HydraModel<>(ctx.bakeLayer(HYDRA)),
                        "hydra_hatchling", 0.45F));
        event.registerEntityRenderer(GreekEntities.GOLDEN_HIND.get(), HindRenderer::new);
        event.registerEntityRenderer(GreekEntities.GREEK_MERCHANT.get(), GreekMerchantRenderer::new);
        event.registerEntityRenderer(GreekEntities.LION.get(),
                ctx -> new GreekMobRenderer<Lion, BeastModel<Lion>>(ctx, new BeastModel<>(ctx.bakeLayer(NEMEAN_LION), 1), "lion", 0.85F));
        event.registerEntityRenderer(GreekEntities.KARKINOS.get(),
                ctx -> new GreekMobRenderer<Karkinos, CrabModel<Karkinos>>(ctx, new CrabModel<>(ctx.bakeLayer(KARKINOS)), "karkinos", 1.3F));
        event.registerEntityRenderer(GreekEntities.AMAZON.get(), AmazonRenderer::new);
        event.registerEntityRenderer(GreekEntities.HIPPOLYTA.get(), AmazonRenderer::new);
        event.registerEntityRenderer(GreekEntities.CERBERUS.get(),
                ctx -> new GreekMobRenderer<Cerberus, BeastModel<Cerberus>>(ctx, new BeastModel<>(ctx.bakeLayer(CERBERUS), 3),
                        "cerberus", 1.8F));
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
