package com.mythsofworlds.mythology.slavic.client;

import com.mythsofworlds.core.client.MythGeoRenderer;
import com.mythsofworlds.core.client.MythMerchantRenderer;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.client.BeastModel;
import com.mythsofworlds.core.client.MythHumanoidRenderer;
import com.mythsofworlds.core.client.MythMobRenderer;
import com.mythsofworlds.core.client.MythModels;
import com.mythsofworlds.core.client.ZombieArmsModel;
import com.mythsofworlds.mythology.norse.client.RavenRenderer;
import com.mythsofworlds.mythology.slavic.SlavicEntities;
import com.mythsofworlds.mythology.slavic.entity.Volkolak;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.world.entity.animal.Parrot;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/** Client side of the mobs of Nav: which model and texture each one is drawn with. The bosses are GeckoLib models. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class SlavicClient {
    private SlavicClient() {
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        ModelLayerLocation humanoid = MythModels.HUMANOID;
        event.registerEntityRenderer(SlavicEntities.LESHY.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "leshy", 1.35F, false));
        event.registerEntityRenderer(SlavicEntities.KIKIMORA.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "kikimora", 0.8F, false));
        event.registerEntityRenderer(SlavicEntities.UPYR.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "upyr", 1.0F, false));
        event.registerEntityRenderer(SlavicEntities.RUSALKA.get(),
                ctx -> new MythHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "rusalka", 1.0F, true));
        event.registerEntityRenderer(SlavicEntities.SOLOVEI.get(), ctx -> new MythGeoRenderer<>(ctx, "solovei", 0.6F));
        event.registerEntityRenderer(SlavicEntities.KOSCHEI.get(), ctx -> new MythGeoRenderer<>(ctx, "koschei", 0.5F));
        event.registerEntityRenderer(SlavicEntities.VOLKOLAK.get(),
                ctx -> new MythMobRenderer<Volkolak, BeastModel<Volkolak>>(ctx, new BeastModel<>(ctx.bakeLayer(MythModels.WOLF), 1),
                        "volkolak", 1.1F));
        event.registerEntityRenderer(SlavicEntities.ZMEY_GORYNYCH.get(), ctx -> new MythGeoRenderer<>(ctx, "zmey_gorynych", 1.6F));
        event.<Parrot>registerEntityRenderer(SlavicEntities.FIREBIRD.get(), ctx -> new RavenRenderer(ctx, "firebird"));
        event.registerEntityRenderer(SlavicEntities.SLAVIC_MERCHANT.get(), ctx -> new MythMerchantRenderer<>(ctx, "slavic_merchant"));
    }
}
