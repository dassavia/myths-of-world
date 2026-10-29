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

/**
 * Karkinos as a crayfish (the Russian "рак"): a long armoured body, a tail of three plates ending in a fan, two long
 * feelers, stalked eyes, eight walking legs and two big claws that snap. Texture 64x64; the UV layout is mirrored in
 * tools/textures.py (crayfish).
 */
public class CrayfishModel<T extends Entity> extends HierarchicalModel<T> {
    private static final float LEG_DROOP = 0.45F;
    private final ModelPart root;
    private final ModelPart[] legs = new ModelPart[8];
    private final ModelPart tail;
    private final ModelPart rightClaw;
    private final ModelPart leftClaw;
    private final ModelPart rightFinger;
    private final ModelPart leftFinger;

    public CrayfishModel(ModelPart root) {
        this.root = root;
        for (int i = 0; i < 8; i++) {
            legs[i] = root.getChild("leg" + i);
        }
        this.tail = root.getChild("tail");
        this.rightClaw = root.getChild("right_claw");
        this.leftClaw = root.getChild("left_claw");
        this.rightFinger = rightClaw.getChild("pincer").getChild("finger");
        this.leftFinger = leftClaw.getChild("pincer").getChild("finger");
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create().texOffs(0, 0).addBox(-4.0F, -2.5F, -6.0F, 8.0F, 5.0F, 12.0F),
                PartPose.offset(0.0F, 19.5F, 0.0F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create().texOffs(0, 17)
                .addBox(-3.0F, -1.5F, 0.0F, 6.0F, 3.0F, 5.0F), PartPose.offset(0.0F, 19.5F, 6.0F));
        PartDefinition tail2 = tail.addOrReplaceChild("tail2", CubeListBuilder.create().texOffs(22, 17)
                .addBox(-2.5F, -1.5F, 0.0F, 5.0F, 3.0F, 4.0F), PartPose.offset(0.0F, 0.3F, 5.0F));
        PartDefinition tail3 = tail2.addOrReplaceChild("tail3", CubeListBuilder.create().texOffs(40, 17)
                .addBox(-2.0F, -1.0F, 0.0F, 4.0F, 2.0F, 4.0F), PartPose.offset(0.0F, 0.3F, 4.0F));
        tail3.addOrReplaceChild("fan", CubeListBuilder.create().texOffs(40, 0)
                .addBox(-4.0F, -0.5F, 0.0F, 8.0F, 1.0F, 4.0F), PartPose.offset(0.0F, 0.3F, 4.0F));
        for (int side = 0; side < 2; side++) {
            float s = side == 0 ? 1.0F : -1.0F;
            root.addOrReplaceChild("feeler" + side, CubeListBuilder.create().texOffs(0, 26)
                            .addBox(-0.5F, -0.5F, -12.0F, 1.0F, 1.0F, 12.0F),
                    PartPose.offsetAndRotation(s * 1.5F, 18.0F, -6.0F, 0.35F, s * -0.3F, 0.0F));
            root.addOrReplaceChild("eye" + side, CubeListBuilder.create().texOffs(28, 26)
                    .addBox(-0.5F, -2.0F, -0.5F, 1.0F, 2.0F, 1.0F), PartPose.offset(s * 2.0F, 17.0F, -5.5F));
        }
        for (int i = 0; i < 8; i++) {
            boolean right = i < 4;
            float z = -3.0F + (i % 4) * 2.0F;
            CubeListBuilder leg = CubeListBuilder.create().texOffs(0, 50);
            if (right) {
                leg.addBox(0.0F, -0.5F, -0.5F, 6.0F, 1.0F, 1.0F);
            } else {
                leg.mirror().addBox(-6.0F, -0.5F, -0.5F, 6.0F, 1.0F, 1.0F);
            }
            root.addOrReplaceChild("leg" + i, leg, PartPose.offsetAndRotation(right ? 3.5F : -3.5F, 21.0F, z,
                    0.0F, 0.0F, right ? LEG_DROOP : -LEG_DROOP));
        }
        for (int side = 0; side < 2; side++) {
            boolean right = side == 0;
            PartDefinition arm = root.addOrReplaceChild(right ? "right_claw" : "left_claw", CubeListBuilder.create()
                            .texOffs(0, 40).addBox(-1.0F, -1.0F, -6.0F, 2.0F, 2.0F, 6.0F),
                    PartPose.offsetAndRotation(right ? 3.5F : -3.5F, 20.0F, -5.0F, 0.0F, right ? -0.35F : 0.35F, 0.0F));
            PartDefinition pincer = arm.addOrReplaceChild("pincer", CubeListBuilder.create().texOffs(16, 40)
                    .addBox(-2.0F, -1.5F, -6.0F, 4.0F, 3.0F, 6.0F), PartPose.offset(0.0F, 0.0F, -5.0F));
            pincer.addOrReplaceChild("finger", CubeListBuilder.create().texOffs(36, 40)
                    .addBox(-1.0F, 0.0F, -5.0F, 2.0F, 1.0F, 5.0F), PartPose.offset(0.0F, 1.5F, -1.0F));
        }
        return LayerDefinition.create(mesh, 64, 64);
    }

    @Override
    public ModelPart root() {
        return root;
    }

    @Override
    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        for (int i = 0; i < 8; i++) {
            boolean right = i < 4;
            float phase = Mth.cos(limbSwing * 1.4F + i * 1.3F) * 0.35F * limbSwingAmount;
            legs[i].zRot = (right ? LEG_DROOP : -LEG_DROOP) + phase;
            legs[i].yRot = Mth.sin(limbSwing * 1.4F + i * 1.3F) * 0.3F * limbSwingAmount;
        }
        tail.xRot = 0.1F + Mth.sin(ageInTicks * 0.08F) * 0.06F;
        float snap = Math.max(0.0F, Mth.sin(ageInTicks * 0.25F)) * 0.45F;
        rightFinger.xRot = snap;
        leftFinger.xRot = snap;
        rightClaw.yRot = -0.35F + netHeadYaw * Mth.DEG_TO_RAD * 0.3F;
        leftClaw.yRot = 0.35F + netHeadYaw * Mth.DEG_TO_RAD * 0.3F;
        rightClaw.xRot = Mth.sin(ageInTicks * 0.1F) * 0.08F;
        leftClaw.xRot = -rightClaw.xRot;
    }
}
