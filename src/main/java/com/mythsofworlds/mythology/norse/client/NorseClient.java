package com.mythsofworlds.mythology.norse.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.client.AmazonRenderer;
import com.mythsofworlds.mythology.greek.client.BeastModel;
import com.mythsofworlds.mythology.greek.client.GreekClient;
import com.mythsofworlds.mythology.greek.client.GreekHumanoidRenderer;
import com.mythsofworlds.mythology.greek.client.GreekMobRenderer;
import com.mythsofworlds.mythology.greek.client.ZombieArmsModel;
import com.mythsofworlds.mythology.norse.NorseEntities;
import com.mythsofworlds.mythology.norse.entity.Fenrir;
import com.mythsofworlds.mythology.norse.entity.Garm;
import com.mythsofworlds.mythology.norse.entity.Warg;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Client side of the Norse mobs: which model and texture each one is drawn with. Reuses the Greek models. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class NorseClient {
    public static final ModelLayerLocation WOLF = new ModelLayerLocation(MythsOfWorlds.id("norse_wolf"), "main");

    private NorseClient() {
    }

    @SubscribeEvent
    public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.registerLayerDefinition(WOLF, () -> BeastModel.createBodyLayer(1, false));
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        ModelLayerLocation humanoid = GreekClient.HUMANOID;
        event.registerEntityRenderer(NorseEntities.DRAUGR.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "draugr", 1.0F, false));
        event.registerEntityRenderer(NorseEntities.DRAUGR_CHIEFTAIN.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "draugr_chieftain", 1.2F, false));
        event.registerEntityRenderer(NorseEntities.TROLL.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "troll", 1.6F, false));
        event.registerEntityRenderer(NorseEntities.FROST_GIANT.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "frost_giant", 2.0F, false));
        event.registerEntityRenderer(NorseEntities.FIRE_GIANT.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "fire_giant", 2.0F, false));
        event.registerEntityRenderer(NorseEntities.THRYM.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "thrym", 2.6F, false));
        event.registerEntityRenderer(NorseEntities.SURTR.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "surtr", 2.6F, false));
        event.registerEntityRenderer(NorseEntities.WARG.get(),
                ctx -> new GreekMobRenderer<Warg, BeastModel<Warg>>(ctx, new BeastModel<>(ctx.bakeLayer(WOLF), 1), "warg", 1.0F));
        event.registerEntityRenderer(NorseEntities.FENRIR.get(),
                ctx -> new GreekMobRenderer<Fenrir, BeastModel<Fenrir>>(ctx, new BeastModel<>(ctx.bakeLayer(WOLF), 1), "fenrir", 2.4F));
        event.registerEntityRenderer(NorseEntities.GARM.get(),
                ctx -> new GreekMobRenderer<Garm, BeastModel<Garm>>(ctx, new BeastModel<>(ctx.bakeLayer(GreekClient.NEMEAN_LION), 1),
                        "garm", 1.6F));
        event.registerEntityRenderer(NorseEntities.RAVEN.get(), RavenRenderer::new);
        event.registerEntityRenderer(NorseEntities.NORSE_MERCHANT.get(), NorseMerchantRenderer::new);
        event.registerEntityRenderer(NorseEntities.VALKYRIE.get(), AmazonRenderer::new);
    }
}
