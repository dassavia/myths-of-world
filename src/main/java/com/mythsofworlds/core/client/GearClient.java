package com.mythsofworlds.core.client;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.Strikes;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import net.minecraft.client.Minecraft;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.HumanoidArm;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.EntityRenderersEvent;
import net.neoforged.neoforge.client.extensions.common.IClientItemExtensions;
import net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent;

/**
 * The gear of the myths on the client: armour with a shape of its own (crests, pauldrons, horns, wings, fur, built by
 * tools/gen_3d_armour.py into armor_models/*.json) and the motion of the hand when a weapon or tool of the myths is
 * swung in first person (see {@link Strikes}).
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class GearClient {
    private static final String MODELS = "/assets/mythsofworlds/armor_models/";

    /** One armour texture with its extra boxes and the items wearing it. */
    private record ArmourSpec(String name, ModelLayerLocation layer, List<String> items, JsonObject json) {
    }

    private static List<ArmourSpec> specs;

    private GearClient() {
    }

    private static JsonElement read(String file) {
        try (InputStream in = GearClient.class.getResourceAsStream(MODELS + file)) {
            if (in == null) {
                throw new IllegalStateException("missing " + MODELS + file);
            }
            return JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8));
        } catch (java.io.IOException e) {
            throw new IllegalStateException("cannot read " + MODELS + file, e);
        }
    }

    private static List<ArmourSpec> specs() {
        if (specs == null) {
            List<ArmourSpec> list = new ArrayList<>();
            for (JsonElement name : read("index.json").getAsJsonArray()) {
                JsonObject json = read(name.getAsString() + ".json").getAsJsonObject();
                List<String> items = new ArrayList<>();
                json.getAsJsonArray("items").forEach(item -> items.add(item.getAsString()));
                list.add(new ArmourSpec(name.getAsString(),
                        new ModelLayerLocation(MythsOfWorlds.id("armor/" + name.getAsString()), "main"), items, json));
            }
            specs = list;
        }
        return specs;
    }

    private static float[] floats(JsonObject json, String key) {
        JsonArray array = json.getAsJsonArray(key);
        float[] values = new float[array.size()];
        for (int i = 0; i < values.length; i++) {
            values[i] = array.get(i).getAsFloat();
        }
        return values;
    }

    /** The outer vanilla armour model (1 pixel larger than the body) with the extra boxes of one armour. */
    static LayerDefinition armourLayer(JsonObject json) {
        MeshDefinition mesh = HumanoidModel.createMesh(new CubeDeformation(1.0F), 0.0F);
        PartDefinition root = mesh.getRoot();
        for (JsonElement element : json.getAsJsonArray("parts")) {
            JsonObject part = element.getAsJsonObject();
            float[] uv = floats(part, "uv");
            float[] origin = floats(part, "origin");
            float[] size = floats(part, "size");
            float[] pivot = floats(part, "pivot");
            float[] rotation = floats(part, "rotation");
            root.getChild(part.get("bone").getAsString()).addOrReplaceChild(part.get("name").getAsString(),
                    CubeListBuilder.create().texOffs((int) uv[0], (int) uv[1]).addBox(origin[0], origin[1], origin[2],
                            size[0], size[1], size[2], new CubeDeformation(part.get("inflate").getAsFloat())),
                    PartPose.offsetAndRotation(pivot[0], pivot[1], pivot[2], rotation[0], rotation[1], rotation[2]));
        }
        return LayerDefinition.create(mesh, 64, json.get("texture_height").getAsInt());
    }

    @SubscribeEvent
    public static void registerLayers(EntityRenderersEvent.RegisterLayerDefinitions event) {
        for (ArmourSpec spec : specs()) {
            event.registerLayerDefinition(spec.layer(), () -> armourLayer(spec.json()));
        }
    }

    /** Armour drawn with its own model; the leggings keep the vanilla inner model and texture. */
    private static final class ArmourExtensions implements IClientItemExtensions {
        private final ModelLayerLocation layer;
        private HumanoidModel<LivingEntity> model;

        ArmourExtensions(ModelLayerLocation layer) {
            this.layer = layer;
        }

        @Override
        public HumanoidModel<?> getHumanoidArmorModel(LivingEntity entity, ItemStack stack, EquipmentSlot slot,
                                                      HumanoidModel<?> original) {
            if (slot == EquipmentSlot.LEGS) {
                return original;
            }
            if (model == null) {
                model = new HumanoidModel<>(Minecraft.getInstance().getEntityModels().bakeLayer(layer));
            }
            return model;
        }
    }

    /** The first-person motion of a swing, in place of the vanilla one. */
    private record SwingExtensions(Strikes.Style style) implements IClientItemExtensions {
        @Override
        public boolean applyForgeHandTransform(PoseStack pose, LocalPlayer player, HumanoidArm arm, ItemStack stack,
                                               float partialTick, float equipProcess, float swingProcess) {
            swing(pose, arm == HumanoidArm.RIGHT ? 1 : -1, equipProcess, swingProcess, style);
            return true;
        }
    }

    /**
     * Places the hand like vanilla (the same resting place and equip motion) and then swings it: a sweep across for
     * a sword, a raise and a blow from above for an axe or a hammer, a thrust for a dagger or the bident, a sharp
     * strike down for the digging tools. Every motion starts and ends at rest, so nothing jumps between swings.
     */
    static void swing(PoseStack pose, int side, float equip, float s, Strikes.Style style) {
        pose.translate(side * 0.56F, -0.52F + equip * -0.6F, -0.72F);
        if (s <= 0.0F) {
            return;
        }
        float lift = Mth.sin(Mth.sqrt(s) * Mth.PI);
        float eased = 1.0F - (1.0F - s) * (1.0F - s) * (1.0F - s);
        switch (style) {
            case SLASH -> {
                pose.translate(side * (0.3F - 0.75F * eased) * lift, (0.2F - 0.4F * eased) * lift, -0.2F * lift);
                pose.mulPose(Axis.YP.rotationDegrees(side * 70.0F * (1.0F - 2.0F * eased) * lift));
                pose.mulPose(Axis.ZP.rotationDegrees(side * -50.0F * eased * lift));
                pose.mulPose(Axis.XP.rotationDegrees(-60.0F * eased * lift));
            }
            case CHOP, HEAVY -> {
                float power = style == Strikes.Style.HEAVY ? 1.3F : 1.0F;
                // The first third raises the blade over the shoulder, the rest brings it down.
                float raise = s < 0.3F ? s / 0.3F : 1.0F - (s - 0.3F) / 0.7F;
                float fall = s < 0.3F ? 0.0F : (s - 0.3F) / 0.7F;
                pose.translate(side * -0.1F * lift, (0.25F * raise - 0.35F * fall * fall) * power, -0.25F * lift);
                pose.mulPose(Axis.XP.rotationDegrees((40.0F * raise - 110.0F * Mth.sin(fall * Mth.HALF_PI)) * power));
                pose.mulPose(Axis.ZP.rotationDegrees(side * -15.0F * lift));
            }
            case STAB -> {
                pose.translate(side * -0.18F * lift, 0.05F * lift, -0.55F * lift);
                pose.mulPose(Axis.YP.rotationDegrees(side * 25.0F * lift));
                pose.mulPose(Axis.XP.rotationDegrees(-35.0F * lift));
            }
            case DIG -> {
                pose.translate(0.0F, 0.08F * lift, -0.1F * lift);
                pose.mulPose(Axis.ZP.rotationDegrees(side * -18.0F * lift));
                pose.mulPose(Axis.XP.rotationDegrees(-85.0F * lift));
            }
        }
    }

    @SubscribeEvent
    public static void registerExtensions(RegisterClientExtensionsEvent event) {
        for (ArmourSpec spec : specs()) {
            ArmourExtensions extensions = new ArmourExtensions(spec.layer());
            for (String name : spec.items()) {
                Item item = BuiltInRegistries.ITEM.get(MythsOfWorlds.id(name));
                if (item == Items.AIR) {
                    throw new IllegalStateException("armor_models/" + spec.name() + ".json names unknown item " + name);
                }
                event.registerItem(extensions, item);
            }
        }
        for (Map.Entry<Item, Strikes.Strike> entry : Strikes.all().entrySet()) {
            event.registerItem(new SwingExtensions(entry.getValue().style()), entry.getKey());
        }
    }
}
