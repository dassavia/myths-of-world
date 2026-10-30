package com.mythsofworlds.mythology.norse.client;

import com.mythsofworlds.core.client.MythGeoRenderer;
import com.mythsofworlds.core.client.MythMerchantRenderer;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.client.AmazonRenderer;
import com.mythsofworlds.core.client.BeastModel;
import com.mythsofworlds.core.client.MythHumanoidRenderer;
import com.mythsofworlds.core.client.MythMobRenderer;
import com.mythsofworlds.core.client.MythModels;
import com.mythsofworlds.core.client.ZombieArmsModel;
import com.mythsofworlds.mythology.norse.NorseEntities;
import com.mythsofworlds.mythology.norse.entity.Warg;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.world.entity.animal.Parrot;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Client side of the Norse mobs: which model and texture each one is drawn with. The bosses are GeckoLib models. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class NorseClient {
    private NorseClient() {
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        ModelLayerLocation humanoid = MythModels.HUMANOID;
        event.registerEntityRenderer(NorseEntities.DRAUGR.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "draugr", 1.0F, false));
        event.registerEntityRenderer(NorseEntities.DRAUGR_CHIEFTAIN.get(), ctx -> new MythGeoRenderer<>(ctx, "draugr_chieftain", 0.6F));
        event.registerEntityRenderer(NorseEntities.TROLL.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "troll", 1.6F, false));
        event.registerEntityRenderer(NorseEntities.FROST_GIANT.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "frost_giant", 2.0F, false));
        event.registerEntityRenderer(NorseEntities.FIRE_GIANT.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "fire_giant", 2.0F, false));
        event.registerEntityRenderer(NorseEntities.THRYM.get(), ctx -> new MythGeoRenderer<>(ctx, "thrym", 1.3F));
        event.registerEntityRenderer(NorseEntities.SURTR.get(), ctx -> new MythGeoRenderer<>(ctx, "surtr", 1.3F));
        event.registerEntityRenderer(NorseEntities.HEIMDALL.get(), ctx -> new MythGeoRenderer<>(ctx, "heimdall", 0.6F));
        event.registerEntityRenderer(NorseEntities.WARG.get(),
                ctx -> new MythMobRenderer<Warg, BeastModel<Warg>>(ctx, new BeastModel<>(ctx.bakeLayer(MythModels.WOLF), 1), "warg", 1.0F));
        event.registerEntityRenderer(NorseEntities.FENRIR.get(), ctx -> new MythGeoRenderer<>(ctx, "fenrir", 1.4F));
        event.registerEntityRenderer(NorseEntities.GARM.get(), ctx -> new MythGeoRenderer<>(ctx, "garm", 1.0F));
        event.<Parrot>registerEntityRenderer(NorseEntities.RAVEN.get(), RavenRenderer::new);
        event.registerEntityRenderer(NorseEntities.NORSE_MERCHANT.get(), ctx -> new MythMerchantRenderer<>(ctx, "norse_merchant"));
        event.registerEntityRenderer(NorseEntities.VALKYRIE.get(), AmazonRenderer::new);
    }
}
