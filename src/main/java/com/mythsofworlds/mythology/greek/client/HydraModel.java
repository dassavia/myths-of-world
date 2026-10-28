package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.mythology.greek.entity.Hydra;
import net.minecraft.client.model.HierarchicalModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.util.Mth;

/** Squat reptile body with five long swaying necks. Texture 128x64; layout mirrored in tools/gen_greek_assets.py. */
public class HydraModel extends HierarchicalModel<Hydra> {
    public static final int HEADS = 5;

    private final ModelPart root;
    private final ModelPart[] necks = new ModelPart[HEADS];
    private final ModelPart[] heads = new ModelPart[HEADS];
    private final ModelPart rightFront;
    private final ModelPart leftFront;
    private final ModelPart rightHind;
    private final ModelPart leftHind;
    private final ModelPart tail;

    public HydraModel(ModelPart root) {
        this.root = root;
        for (int i = 0; i < HEADS; i++) {
            necks[i] = root.getChild("neck" + i);
            heads[i] = necks[i].getChild("head");
        }
        this.rightFront = root.getChild("right_front_leg");
        this.leftFront = root.getChild("left_front_leg");
        this.rightHind = root.getChild("right_hind_leg");
        this.leftHind = root.getChild("left_hind_leg");
        this.tail = root.getChild("tail");
    }

    public static LayerDefinition createBodyLayer() {
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
        for (int i = 0; i < HEADS; i++) {
            PartDefinition neck = root.addOrReplaceChild("neck" + i,
                    CubeListBuilder.create().texOffs(72, 0).addBox(-1.5F, -14.0F, -1.5F, 3.0F, 14.0F, 3.0F),
                    PartPose.offset((i - 2) * 3.0F, 8.0F, -8.0F));
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
    public void setupAnim(Hydra entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        for (int i = 0; i < HEADS; i++) {
            necks[i].zRot = (i - 2) * 0.28F + Mth.sin(ageInTicks * 0.08F + i * 1.3F) * 0.08F;
            necks[i].xRot = -0.35F + Mth.cos(ageInTicks * 0.06F + i) * 0.1F;
            heads[i].yRot = netHeadYaw * Mth.DEG_TO_RAD * 0.6F - necks[i].zRot * 0.5F;
            heads[i].xRot = 0.35F + headPitch * Mth.DEG_TO_RAD * 0.5F;
        }
        float swing = Mth.cos(limbSwing * 0.6662F) * 1.2F * limbSwingAmount;
        rightFront.xRot = swing;
        leftHind.xRot = swing;
        leftFront.xRot = -swing;
        rightHind.xRot = -swing;
        tail.yRot = Mth.sin(ageInTicks * 0.08F) * 0.25F;
    }
}
