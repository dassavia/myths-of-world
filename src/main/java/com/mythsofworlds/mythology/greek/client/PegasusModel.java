package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.mythology.greek.entity.Pegasus;
import net.minecraft.client.model.HorseModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.util.Mth;

/** The vanilla horse with a pair of wings: folded on the ground, beating in the air. Texture 64x64. */
public class PegasusModel extends HorseModel<Pegasus> {
    private final ModelPart rightWing;
    private final ModelPart leftWing;

    public PegasusModel(ModelPart root) {
        super(root);
        ModelPart bodyPart = root.getChild("body");
        this.rightWing = bodyPart.getChild("right_wing");
        this.leftWing = bodyPart.getChild("left_wing");
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = HorseModel.createBodyMesh(CubeDeformation.NONE);
        PartDefinition body = mesh.getRoot().getChild("body");
        body.addOrReplaceChild("right_wing", CubeListBuilder.create().texOffs(0, 0).addBox(-14.0F, -0.5F, 0.0F, 14.0F, 1.0F, 10.0F),
                PartPose.offset(-4.5F, -7.5F, -13.0F));
        body.addOrReplaceChild("left_wing", CubeListBuilder.create().texOffs(0, 0).mirror().addBox(0.0F, -0.5F, 0.0F, 14.0F, 1.0F, 10.0F),
                PartPose.offset(4.5F, -7.5F, -13.0F));
        return LayerDefinition.create(mesh, 64, 64);
    }

    @Override
    public void setupAnim(Pegasus entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);
        float angle = entity.isFlying() ? 0.3F + Mth.sin(ageInTicks * 0.6F) * 0.7F : -1.1F;
        rightWing.zRot = angle;
        leftWing.zRot = -angle;
    }
}
