package com.mythsofworlds.mythology.slavic.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.client.BeastModel;
import com.mythsofworlds.mythology.greek.client.GreekClient;
import com.mythsofworlds.mythology.greek.client.GreekHumanoidRenderer;
import com.mythsofworlds.mythology.greek.client.GreekMobRenderer;
import com.mythsofworlds.mythology.greek.client.HydraModel;
import com.mythsofworlds.mythology.greek.client.ZombieArmsModel;
import com.mythsofworlds.mythology.norse.client.NorseClient;
import com.mythsofworlds.mythology.norse.client.NorseMerchantRenderer;
import com.mythsofworlds.mythology.norse.client.RavenRenderer;
import com.mythsofworlds.mythology.norse.entity.NorseMerchant;
import com.mythsofworlds.mythology.slavic.SlavicEntities;
import com.mythsofworlds.mythology.slavic.entity.Volkolak;
import com.mythsofworlds.mythology.slavic.entity.ZmeyGorynych;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.world.entity.animal.Parrot;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Client side of the mobs of Nav: which model and texture each one is drawn with. Reuses the Greek and Norse models. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class SlavicClient {
    /** The Hydra's body with three necks. */
    public static final ModelLayerLocation ZMEY = new ModelLayerLocation(MythsOfWorlds.id("zmey_gorynych"), "main");

    private SlavicClient() {
    }

    @SubscribeEvent
    public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.registerLayerDefinition(ZMEY, () -> HydraModel.createBodyLayer(ZmeyGorynych.HEADS));
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        ModelLayerLocation humanoid = GreekClient.HUMANOID;
        event.registerEntityRenderer(SlavicEntities.LESHY.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "leshy", 1.35F, false));
        event.registerEntityRenderer(SlavicEntities.KIKIMORA.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "kikimora", 0.8F, false));
        event.registerEntityRenderer(SlavicEntities.UPYR.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "upyr", 1.0F, false));
        event.registerEntityRenderer(SlavicEntities.RUSALKA.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "rusalka", 1.0F, true));
        event.registerEntityRenderer(SlavicEntities.SOLOVEI.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "solovei", 1.1F, false));
        event.registerEntityRenderer(SlavicEntities.KOSCHEI.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "koschei", 1.25F, false));
        event.registerEntityRenderer(SlavicEntities.VOLKOLAK.get(),
                ctx -> new GreekMobRenderer<Volkolak, BeastModel<Volkolak>>(ctx, new BeastModel<>(ctx.bakeLayer(NorseClient.WOLF), 1),
                        "volkolak", 1.1F));
        event.registerEntityRenderer(SlavicEntities.ZMEY_GORYNYCH.get(),
                ctx -> new GreekMobRenderer<ZmeyGorynych, HydraModel<ZmeyGorynych>>(ctx,
                        new HydraModel<>(ctx.bakeLayer(ZMEY), ZmeyGorynych.HEADS), "zmey_gorynych", 2.0F));
        event.<Parrot>registerEntityRenderer(SlavicEntities.FIREBIRD.get(), ctx -> new RavenRenderer(ctx, "firebird"));
        event.<NorseMerchant>registerEntityRenderer(SlavicEntities.SLAVIC_MERCHANT.get(),
                ctx -> new NorseMerchantRenderer(ctx, "slavic_merchant"));
    }
}
