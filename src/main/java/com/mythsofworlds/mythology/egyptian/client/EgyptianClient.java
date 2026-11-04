package com.mythsofworlds.mythology.egyptian.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import com.mythsofworlds.mythology.egyptian.entity.Apep;
import com.mythsofworlds.mythology.egyptian.entity.Crocodile;
import com.mythsofworlds.mythology.egyptian.entity.Jackal;
import com.mythsofworlds.mythology.egyptian.entity.Scarab;
import com.mythsofworlds.mythology.egyptian.entity.Scorpion;
import com.mythsofworlds.mythology.egyptian.entity.Sphinx;
import com.mythsofworlds.mythology.greek.client.AmazonRenderer;
import com.mythsofworlds.mythology.greek.client.BeastModel;
import com.mythsofworlds.mythology.greek.client.CrayfishModel;
import com.mythsofworlds.mythology.greek.client.GreekClient;
import com.mythsofworlds.mythology.greek.client.GreekHumanoidRenderer;
import com.mythsofworlds.mythology.greek.client.GreekMobRenderer;
import com.mythsofworlds.mythology.greek.client.HydraModel;
import com.mythsofworlds.mythology.greek.client.ZombieArmsModel;
import com.mythsofworlds.mythology.norse.client.NorseClient;
import com.mythsofworlds.mythology.norse.client.NorseMerchantRenderer;
import com.mythsofworlds.mythology.norse.entity.NorseMerchant;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.SpiderModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.Cat;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;

/**
 * Client side of the mobs of the Duat: which model and texture each one is drawn with. Reuses the models of Hellas
 * and Jotunheim and some vanilla ones: the Sphinx is the Nemean lion's body with a king's head and nemes, Apep the
 * Hydra's body with a single long neck, the scorpion the body of Karkinos, the scarab a small spider's. The gods are
 * tall humanoids with the heads of their sacred animals drawn on; the crocodile has a model of its own.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class EgyptianClient {
    /** The Hydra's body with one neck. */
    public static final ModelLayerLocation APEP = new ModelLayerLocation(MythsOfWorlds.id("apep"), "main");
    public static final ModelLayerLocation CROCODILE = new ModelLayerLocation(MythsOfWorlds.id("crocodile"), "main");

    private EgyptianClient() {
    }

    @SubscribeEvent
    public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions event) {
        event.registerLayerDefinition(APEP, () -> HydraModel.createBodyLayer(1));
        event.registerLayerDefinition(CROCODILE, CrocodileModel::createBodyLayer);
    }

    /** The bow of Horus draws like a vanilla bow: the "pull" and "pulling" properties pick its model. */
    @SubscribeEvent
    public static void clientSetup(FMLClientSetupEvent event) {
        event.enqueueWork(() -> {
            ItemProperties.register(EgyptianContent.BOW_OF_HORUS.get(), ResourceLocation.withDefaultNamespace("pull"),
                    (stack, level, entity, seed) -> entity == null || entity.getUseItem() != stack ? 0.0F
                            : (stack.getUseDuration(entity) - entity.getUseItemRemainingTicks()) / 20.0F);
            ItemProperties.register(EgyptianContent.BOW_OF_HORUS.get(), ResourceLocation.withDefaultNamespace("pulling"),
                    (stack, level, entity, seed) -> entity != null && entity.isUsingItem() && entity.getUseItem() == stack ? 1.0F : 0.0F);
        });
    }

    @SubscribeEvent
    public static void registerRenderers(EntityRenderersEvent.RegisterRenderers event) {
        ModelLayerLocation humanoid = GreekClient.HUMANOID;
        event.registerEntityRenderer(EgyptianEntities.MUMMY.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "mummy", 1.0F, false));
        event.registerEntityRenderer(EgyptianEntities.USHABTI.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "ushabti", 1.0F, false));
        event.registerEntityRenderer(EgyptianEntities.PHARAOH_MUMMY.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new ZombieArmsModel<>(ctx.bakeLayer(humanoid)), "pharaoh_mummy", 1.2F, false));
        event.registerEntityRenderer(EgyptianEntities.SET.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "set", 1.45F, false));
        event.registerEntityRenderer(EgyptianEntities.SCARAB.get(),
                ctx -> new GreekMobRenderer<Scarab, SpiderModel<Scarab>>(ctx, new SpiderModel<>(ctx.bakeLayer(ModelLayers.SPIDER)),
                        "scarab", 0.45F));
        event.registerEntityRenderer(EgyptianEntities.JACKAL.get(),
                ctx -> new GreekMobRenderer<Jackal, BeastModel<Jackal>>(ctx, new BeastModel<>(ctx.bakeLayer(NorseClient.WOLF), 1),
                        "jackal", 0.8F));
        event.registerEntityRenderer(EgyptianEntities.SCORPION.get(),
                ctx -> new GreekMobRenderer<Scorpion, CrayfishModel<Scorpion>>(ctx, new CrayfishModel<>(ctx.bakeLayer(GreekClient.KARKINOS)),
                        "scorpion", 0.85F));
        event.registerEntityRenderer(EgyptianEntities.SPHINX.get(),
                ctx -> new GreekMobRenderer<Sphinx, BeastModel<Sphinx>>(ctx, new BeastModel<>(ctx.bakeLayer(GreekClient.NEMEAN_LION), 1),
                        "sphinx", 2.2F));
        event.registerEntityRenderer(EgyptianEntities.APEP.get(),
                ctx -> new GreekMobRenderer<Apep, HydraModel<Apep>>(ctx, new HydraModel<>(ctx.bakeLayer(APEP), 1), "apep", 2.2F));
        event.registerEntityRenderer(EgyptianEntities.RA.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "ra", 1.3F, false));
        event.registerEntityRenderer(EgyptianEntities.OSIRIS.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "osiris", 1.3F, false));
        event.registerEntityRenderer(EgyptianEntities.ISIS.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "isis", 1.25F, false));
        event.registerEntityRenderer(EgyptianEntities.HORUS.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "horus", 1.3F, false));
        event.registerEntityRenderer(EgyptianEntities.ANUBIS.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "anubis", 1.3F, false));
        event.registerEntityRenderer(EgyptianEntities.THOTH.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "thoth", 1.3F, false));
        event.registerEntityRenderer(EgyptianEntities.BASTET.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "bastet", 1.15F, false));
        event.registerEntityRenderer(EgyptianEntities.SOBEK.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "sobek", 1.4F, false));
        event.registerEntityRenderer(EgyptianEntities.HATHOR.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "hathor", 1.25F, false));
        event.registerEntityRenderer(EgyptianEntities.PTAH.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "ptah", 1.3F, false));
        event.registerEntityRenderer(EgyptianEntities.SEKHMET.get(),
                ctx -> new GreekHumanoidRenderer<>(ctx, new HumanoidModel<>(ctx.bakeLayer(humanoid)), "sekhmet", 1.3F, false));
        event.registerEntityRenderer(EgyptianEntities.CROCODILE.get(),
                ctx -> new GreekMobRenderer<Crocodile, CrocodileModel<Crocodile>>(ctx, new CrocodileModel<>(ctx.bakeLayer(CROCODILE)),
                        "crocodile", 1.0F));
        event.<Cat>registerEntityRenderer(EgyptianEntities.BASTET_CAT.get(), BastetCatRenderer::new);
        event.registerEntityRenderer(EgyptianEntities.PRIESTESS.get(), AmazonRenderer::new);
        event.<NorseMerchant>registerEntityRenderer(EgyptianEntities.EGYPTIAN_MERCHANT.get(),
                ctx -> new NorseMerchantRenderer(ctx, "egyptian_merchant"));
    }
}
