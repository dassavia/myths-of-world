package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.core.client.ZombieArmsModel;
import com.mythsofworlds.mythology.greek.entity.Minotaur;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/** Humanoid body with a bull's horns and snout; lowers its head while charging. Texture 64x64. */
public class MinotaurModel extends ZombieArmsModel<Minotaur> {
    public MinotaurModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition head = mesh.getRoot().getChild("head");
        head.addOrReplaceChild("right_horn", CubeListBuilder.create().texOffs(0, 32).addBox(-6.0F, -1.0F, -1.0F, 6.0F, 2.0F, 2.0F),
                PartPose.offsetAndRotation(-4.0F, -7.0F, 0.0F, 0.0F, 0.0F, 0.45F));
        head.addOrReplaceChild("left_horn", CubeListBuilder.create().texOffs(0, 36).addBox(0.0F, -1.0F, -1.0F, 6.0F, 2.0F, 2.0F),
                PartPose.offsetAndRotation(4.0F, -7.0F, 0.0F, 0.0F, 0.0F, -0.45F));
        head.addOrReplaceChild("snout", CubeListBuilder.create().texOffs(16, 32).addBox(-2.5F, -3.0F, -6.0F, 5.0F, 3.0F, 2.0F),
                PartPose.ZERO);
        return LayerDefinition.create(mesh, 64, 64);
    }

    @Override
    public void setupAnim(Minotaur entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);
        if (entity.isAggressive() && entity.getDeltaMovement().horizontalDistanceSqr() > 0.2) {
            head.xRot = 0.6F;
        }
    }
}
