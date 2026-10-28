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
 * Big four-legged predator with one or more heads: the Nemean Lion (one head with a mane)
 * and Cerberus (three heads). Texture 64x64; the UV layout is mirrored in tools/gen_greek_assets.py.
 */
public class BeastModel<T extends Entity> extends HierarchicalModel<T> {
    private final ModelPart root;
    private final ModelPart[] heads;
    private final float[] headYaw;
    private final ModelPart rightFront;
    private final ModelPart leftFront;
    private final ModelPart rightHind;
    private final ModelPart leftHind;
    private final ModelPart tail;

    public BeastModel(ModelPart root, int headCount) {
        this.root = root;
        this.heads = new ModelPart[headCount];
        this.headYaw = new float[headCount];
        for (int i = 0; i < headCount; i++) {
            heads[i] = root.getChild("head" + i);
            headYaw[i] = heads[i].yRot;
        }
        this.rightFront = root.getChild("right_front_leg");
        this.leftFront = root.getChild("left_front_leg");
        this.rightHind = root.getChild("right_hind_leg");
        this.leftHind = root.getChild("left_hind_leg");
        this.tail = root.getChild("tail");
    }

    /**
     * @param headCount 1 for the lion, 3 for Cerberus
     * @param mane      ring of fur around each head
     */
    public static LayerDefinition createBodyLayer(int headCount, boolean mane) {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create().texOffs(0, 0).addBox(-5.0F, -5.0F, -9.0F, 10.0F, 10.0F, 18.0F),
                PartPose.offset(0.0F, 11.0F, 0.0F));
        CubeListBuilder leg = CubeListBuilder.create().texOffs(0, 44).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 10.0F, 4.0F);
        CubeListBuilder mirroredLeg = CubeListBuilder.create().texOffs(0, 44).mirror().addBox(-2.0F, 0.0F, -2.0F, 4.0F, 10.0F, 4.0F);
        root.addOrReplaceChild("right_front_leg", leg, PartPose.offset(-3.0F, 14.0F, -6.0F));
        root.addOrReplaceChild("left_front_leg", mirroredLeg, PartPose.offset(3.0F, 14.0F, -6.0F));
        root.addOrReplaceChild("right_hind_leg", leg, PartPose.offset(-3.0F, 14.0F, 6.0F));
        root.addOrReplaceChild("left_hind_leg", mirroredLeg, PartPose.offset(3.0F, 14.0F, 6.0F));
        root.addOrReplaceChild("tail", CubeListBuilder.create().texOffs(16, 44).addBox(-1.0F, -1.0F, 0.0F, 2.0F, 2.0F, 10.0F),
                PartPose.offsetAndRotation(0.0F, 8.0F, 9.0F, -0.7F, 0.0F, 0.0F));
        for (int i = 0; i < headCount; i++) {
            float offset = i - (headCount - 1) / 2.0F;
            PartDefinition head = root.addOrReplaceChild("head" + i,
                    CubeListBuilder.create().texOffs(32, 28).addBox(-3.5F, -3.5F, -6.0F, 7.0F, 7.0F, 6.0F),
                    PartPose.offsetAndRotation(offset * 6.5F, 8.0F - (headCount > 1 && offset == 0 ? 1.5F : 0.0F), -9.0F,
                            0.0F, -offset * 0.3F, 0.0F));
            head.addOrReplaceChild("snout", CubeListBuilder.create().texOffs(40, 44).addBox(-2.0F, -0.5F, -9.0F, 4.0F, 3.0F, 3.0F),
                    PartPose.ZERO);
            if (mane) {
                head.addOrReplaceChild("mane", CubeListBuilder.create().texOffs(0, 28).addBox(-5.0F, -5.0F, -2.0F, 10.0F, 10.0F, 4.0F),
                        PartPose.ZERO);
            }
        }
        return LayerDefinition.create(mesh, 64, 64);
    }

    @Override
    public ModelPart root() {
        return root;
    }

    @Override
    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        for (int i = 0; i < heads.length; i++) {
            // Side heads look around on their own a little.
            float wander = heads.length > 1 ? Mth.sin(ageInTicks * 0.07F + i * 2.0F) * 0.15F : 0.0F;
            heads[i].yRot = headYaw[i] + netHeadYaw * Mth.DEG_TO_RAD + wander;
            heads[i].xRot = headPitch * Mth.DEG_TO_RAD;
        }
        float swing = Mth.cos(limbSwing * 0.6662F) * 1.4F * limbSwingAmount;
        rightFront.xRot = swing;
        leftHind.xRot = swing;
        leftFront.xRot = -swing;
        rightHind.xRot = -swing;
        tail.yRot = Mth.sin(ageInTicks * 0.1F) * 0.3F;
    }
}
