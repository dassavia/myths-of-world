package com.mythsofworlds.mythology.greek.client;

import com.mythsofworlds.mythology.greek.entity.GoldenHind;
import net.minecraft.client.model.HorseModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/** The vanilla horse body with branching golden antlers. Texture 64x64; the antlers use the 4x8 corner at 0,0. */
public class HindModel extends HorseModel<GoldenHind> {
    public HindModel(ModelPart root) {
        super(root);
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = HorseModel.createBodyMesh(CubeDeformation.NONE);
        PartDefinition head = mesh.getRoot().getChild("head_parts");
        CubeListBuilder beam = CubeListBuilder.create().texOffs(0, 0).addBox(-0.5F, -7.0F, -0.5F, 1.0F, 7.0F, 1.0F);
        CubeListBuilder tine = CubeListBuilder.create().texOffs(0, 0).addBox(-0.5F, -3.0F, -0.5F, 1.0F, 3.0F, 1.0F);
        for (int side = -1; side <= 1; side += 2) {
            PartDefinition antler = head.addOrReplaceChild(side < 0 ? "right_antler" : "left_antler", beam,
                    PartPose.offsetAndRotation(side * 1.6F, -11.5F, 4.5F, 0.35F, 0.0F, side * 0.45F));
            antler.addOrReplaceChild("front_tine", tine, PartPose.offsetAndRotation(0.0F, -3.0F, 0.0F, -0.9F, 0.0F, 0.0F));
            antler.addOrReplaceChild("top_tine", tine, PartPose.offsetAndRotation(0.0F, -6.5F, 0.0F, 0.0F, 0.0F, side * 0.7F));
        }
        return LayerDefinition.create(mesh, 64, 64);
    }
}
