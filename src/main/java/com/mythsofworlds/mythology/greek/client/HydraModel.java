package com.mythsofworlds.mythology.greek.client;

import net.minecraft.client.model.HierarchicalModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.TamableAnimal;

/**
 * Squat reptile body with long swaying necks: five for the Hydra and its hatchlings, three for Zmey Gorynych.
 * Texture 128x64; layout mirrored in tools/gen_greek_assets.py.
 */
public class HydraModel<T extends Entity> extends HierarchicalModel<T> {
    public static final int HEADS = 5;

    private final ModelPart root;
    private final int count;
    private final ModelPart[] necks;
    private final ModelPart[] heads;
    private final ModelPart body;
    private final ModelPart rightFront;
    private final ModelPart leftFront;
    private final ModelPart rightHind;
    private final ModelPart leftHind;
    private final ModelPart tail;

    public HydraModel(ModelPart root) {
        this(root, HEADS);
    }

    public HydraModel(ModelPart root, int count) {
        this.root = root;
        this.count = count;
        this.necks = new ModelPart[count];
        this.heads = new ModelPart[count];
        for (int i = 0; i < count; i++) {
            necks[i] = root.getChild("neck" + i);
            heads[i] = necks[i].getChild("head");
        }
        this.body = root.getChild("body");
        this.rightFront = root.getChild("right_front_leg");
        this.leftFront = root.getChild("left_front_leg");
        this.rightHind = root.getChild("right_hind_leg");
        this.leftHind = root.getChild("left_hind_leg");
        this.tail = root.getChild("tail");
    }

    public static LayerDefinition createBodyLayer() {
        return createBodyLayer(HEADS);
    }

    public static LayerDefinition createBodyLayer(int count) {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create().texOffs(0, 0).addBox(-8.0F, -6.0F, -10.0F, 16.0F, 12.0F, 20.0F),
                PartPose.offset(0.0F, 12.0F, 0.0F));
        CubeListBuilder leg = CubeListBuilder.create().texOffs(0, 32).addBox(-3.0F, 0.0F, -3.0F, 6.0F, 8.0F, 6.0F);
        root.addOrReplaceChild("right_front_leg", leg, PartPose.offset(-6.0F, 16.0F, -6.0F));
        root.addOrReplaceChild("left_front_leg", leg, PartPose.offset(6.0F, 16.0F, -6.0F));
        root.addOrReplaceChild("right_hind_leg", leg, PartPose.offset(-6.0F, 16.0F, 6.0F));
        root.addOrReplaceChild("left_hind_leg", leg, PartPose.offset(6.0F, 16.0F, 6.0F));
        root.addOrReplaceChild("tail", CubeListBuilder.create().texOffs(0, 46).addBox(-2.0F, -2.0F, 0.0F, 4.0F, 4.0F, 14.0F),
                PartPose.offsetAndRotation(0.0F, 12.0F, 10.0F, -0.3F, 0.0F, 0.0F));
        for (int i = 0; i < count; i++) {
            PartDefinition neck = root.addOrReplaceChild("neck" + i,
                    CubeListBuilder.create().texOffs(72, 0).addBox(-1.5F, -14.0F, -1.5F, 3.0F, 14.0F, 3.0F),
                    PartPose.offset((i - (count - 1) / 2.0F) * 3.0F, 8.0F, -8.0F));
            neck.addOrReplaceChild("head", CubeListBuilder.create().texOffs(72, 20).addBox(-2.5F, -3.0F, -7.0F, 5.0F, 5.0F, 7.0F),
                    PartPose.offset(0.0F, -14.0F, 0.0F));
        }
        return LayerDefinition.create(mesh, 128, 64);
    }

    @Override
    public ModelPart root() {
        return root;
    }

    @Override
    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        root.getAllParts().forEach(ModelPart::resetPose);
        boolean sitting = entity instanceof TamableAnimal pet && pet.isInSittingPose();
        for (int i = 0; i < count; i++) {
            float sway = sitting ? 0.04F : 0.08F;
            necks[i].zRot = (i - (count - 1) / 2.0F) * 0.28F + Mth.sin(ageInTicks * 0.08F + i * 1.3F) * sway;
            necks[i].xRot = -0.35F + Mth.cos(ageInTicks * 0.06F + i) * 0.1F;
            heads[i].yRot = netHeadYaw * Mth.DEG_TO_RAD * 0.6F - necks[i].zRot * 0.5F;
            heads[i].xRot = 0.35F + headPitch * Mth.DEG_TO_RAD * 0.5F;
        }
        if (sitting) {
            sit(ageInTicks);
            return;
        }
        float swing = Mth.cos(limbSwing * 0.6662F) * 1.2F * limbSwingAmount;
        rightFront.xRot = swing;
        leftHind.xRot = swing;
        leftFront.xRot = -swing;
        rightHind.xRot = -swing;
        tail.yRot = Mth.sin(ageInTicks * 0.08F) * 0.25F;
    }

    /**
     * Sitting on command: the belly lies on the ground, the forelegs stretch out in front and the hind legs behind like
     * a resting lizard, the tail curls along the ground and the necks stand up, swaying slowly.
     */
    private void sit(float ageInTicks) {
        float drop = 5.0F;
        body.y += drop;
        tail.y += drop;
        for (ModelPart neck : necks) {
            neck.y += drop;
        }
        for (ModelPart leg : new ModelPart[]{rightFront, leftFront, rightHind, leftHind}) {
            leg.y = 21.0F;
        }
        rightFront.xRot = -Mth.HALF_PI;
        leftFront.xRot = -Mth.HALF_PI;
        rightFront.yRot = 0.25F;
        leftFront.yRot = -0.25F;
        rightHind.xRot = Mth.HALF_PI;
        leftHind.xRot = Mth.HALF_PI;
        rightHind.yRot = -0.3F;
        leftHind.yRot = 0.3F;
        tail.xRot = -0.38F;
        tail.yRot = 0.5F + Mth.sin(ageInTicks * 0.05F) * 0.08F;
        for (ModelPart neck : necks) {
            neck.xRot = -0.15F + (neck.xRot + 0.35F) * 0.5F;
        }
    }
}
