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
 * Karkinos, the giant crab: a wide flat shell on six legs, two eyes on stalks and two big claws that snap.
 * Texture 64x64; the UV layout is mirrored in tools/textures.py (crab).
 */
public class CrabModel<T extends Entity> extends HierarchicalModel<T> {
    private static final float LEG_DROOP = 0.95F;
    private final ModelPart root;
    private final ModelPart[] legs = new ModelPart[6];
    private final ModelPart rightClaw;
    private final ModelPart leftClaw;

    public CrabModel(ModelPart root) {
        this.root = root;
        for (int i = 0; i < 6; i++) {
            legs[i] = root.getChild("leg" + i);
        }
        this.rightClaw = root.getChild("right_claw");
        this.leftClaw = root.getChild("left_claw");
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create().texOffs(0, 0).addBox(-8.0F, -3.0F, -6.0F, 16.0F, 6.0F, 12.0F),
                PartPose.offset(0.0F, 16.0F, 0.0F));
        for (int side = 0; side < 2; side++) {
            float x = side == 0 ? -3.0F : 3.0F;
            root.addOrReplaceChild("eye" + side, CubeListBuilder.create()
                            .texOffs(0, 18).addBox(-0.5F, -4.0F, -0.5F, 1.0F, 4.0F, 1.0F)
                            .texOffs(4, 18).addBox(-1.0F, -6.0F, -1.0F, 2.0F, 2.0F, 2.0F),
                    PartPose.offset(x, 13.0F, -5.0F));
        }
        for (int i = 0; i < 6; i++) {
            boolean right = i < 3;
            float z = -3.0F + (i % 3) * 3.0F;
            CubeListBuilder leg = CubeListBuilder.create().texOffs(0, 36);
            if (right) {
                leg.addBox(0.0F, -1.0F, -1.0F, 8.0F, 2.0F, 2.0F);
            } else {
                leg.mirror().addBox(-8.0F, -1.0F, -1.0F, 8.0F, 2.0F, 2.0F);
            }
            root.addOrReplaceChild("leg" + i, leg, PartPose.offsetAndRotation(right ? 7.0F : -7.0F, 17.0F, z,
                    0.0F, 0.0F, right ? LEG_DROOP : -LEG_DROOP));
        }
        for (int side = 0; side < 2; side++) {
            boolean right = side == 0;
            PartDefinition arm = root.addOrReplaceChild(right ? "right_claw" : "left_claw", CubeListBuilder.create()
                            .texOffs(0, 24).addBox(-1.5F, -1.5F, -6.0F, 3.0F, 3.0F, 6.0F),
                    PartPose.offsetAndRotation(right ? 6.0F : -6.0F, 15.0F, -5.0F, 0.0F, right ? -0.5F : 0.5F, 0.0F));
            arm.addOrReplaceChild("pincer", CubeListBuilder.create().texOffs(20, 24).addBox(-2.5F, -2.0F, -6.0F, 5.0F, 4.0F, 6.0F),
                    PartPose.offset(0.0F, 0.0F, -5.0F));
            arm.addOrReplaceChild("finger", CubeListBuilder.create().texOffs(20, 36).addBox(-1.0F, 0.0F, -5.0F, 2.0F, 1.0F, 5.0F),
                    PartPose.offset(0.0F, 2.0F, -6.0F));
        }
        return LayerDefinition.create(mesh, 64, 64);
    }

    @Override
    public ModelPart root() {
        return root;
    }

    @Override
    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        for (int i = 0; i < 6; i++) {
            boolean right = i < 3;
            float phase = Mth.cos(limbSwing * 1.2F + i * 1.7F) * 0.4F * limbSwingAmount;
            legs[i].zRot = (right ? LEG_DROOP : -LEG_DROOP) + phase;
            legs[i].yRot = Mth.sin(limbSwing * 1.2F + i * 1.7F) * 0.25F * limbSwingAmount;
        }
        float snap = Mth.sin(ageInTicks * 0.25F) * 0.12F;
        rightClaw.xRot = snap;
        leftClaw.xRot = -snap;
        rightClaw.yRot = -0.5F + netHeadYaw * Mth.DEG_TO_RAD * 0.3F;
        leftClaw.yRot = 0.5F + netHeadYaw * Mth.DEG_TO_RAD * 0.3F;
    }
}
