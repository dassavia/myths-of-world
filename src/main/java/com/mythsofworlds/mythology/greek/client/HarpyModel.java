package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.mythology.greek.entity.Harpy;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.util.Mth;

/** Humanoid with two feathered wings on the back that beat while it flies. Texture 64x64. */
public class HarpyModel extends HumanoidModel<Harpy> {
    private final ModelPart rightWing;
    private final ModelPart leftWing;

    public HarpyModel(ModelPart root) {
        super(root);
        this.rightWing = body.getChild("right_wing");
        this.leftWing = body.getChild("left_wing");
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition body = mesh.getRoot().getChild("body");
        body.addOrReplaceChild("right_wing", CubeListBuilder.create().texOffs(0, 32).addBox(-0.5F, 0.0F, 0.0F, 1.0F, 12.0F, 8.0F),
                PartPose.offset(-1.5F, 1.0F, 2.0F));
        body.addOrReplaceChild("left_wing", CubeListBuilder.create().texOffs(24, 32).mirror().addBox(-0.5F, 0.0F, 0.0F, 1.0F, 12.0F, 8.0F),
                PartPose.offset(1.5F, 1.0F, 2.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }

    @Override
    public void setupAnim(Harpy entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);
        float spread = entity.isFlying() ? 0.9F + Mth.sin(ageInTicks * 0.9F) * 0.6F : 0.35F;
        rightWing.yRot = -spread;
        leftWing.yRot = spread;
        rightWing.xRot = 0.25F;
        leftWing.xRot = 0.25F;
        if (entity.isFlying()) {
            // Legs trail behind in flight.
            rightLeg.xRot = 0.6F;
            leftLeg.xRot = 0.6F;
        }
    }
}
