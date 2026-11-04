package com.mythsofworlds.mythology.egyptian.client;

import net.minecraft.client.model.HierarchicalModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Mob;

/**
 * The crocodile of the Nile: a long low body with a ridge of bony scutes down the back, a flat skull with raised eyes,
 * a long narrow snout over a lower jaw that gapes when it hunts, four sprawling legs and a tail of three segments that
 * sweeps from side to side (harder when it swims, with the legs folded back). Texture 64x64; the UV layout is mirrored
 * in tools/textures_egyptian.py (crocodile).
 */
public class CrocodileModel<T extends Mob> extends HierarchicalModel<T> {
    private static final float SPLAY = 0.6F;
    private final ModelPart root;
    private final ModelPart head;
    private final ModelPart jaw;
    private final ModelPart tail;
    private final ModelPart tail2;
    private final ModelPart tail3;
    private final ModelPart[] legs = new ModelPart[4];

    public CrocodileModel(ModelPart root) {
        this.root = root;
        this.head = root.getChild("head");
        this.jaw = head.getChild("jaw");
        this.tail = root.getChild("tail");
        this.tail2 = tail.getChild("tail2");
        this.tail3 = tail2.getChild("tail3");
        for (int i = 0; i < 4; i++) {
            legs[i] = root.getChild("leg" + i);
        }
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("body", CubeListBuilder.create().texOffs(0, 0).addBox(-4.0F, -2.0F, -8.0F, 8.0F, 4.0F, 16.0F)
                .texOffs(0, 20).addBox(-2.0F, -3.0F, -7.0F, 4.0F, 1.0F, 14.0F), PartPose.offset(0.0F, 18.0F, 0.0F));
        PartDefinition head = root.addOrReplaceChild("head", CubeListBuilder.create()
                .texOffs(0, 35).addBox(-3.0F, -2.5F, -5.0F, 6.0F, 4.0F, 5.0F)
                .texOffs(22, 35).addBox(-2.0F, -1.5F, -13.0F, 4.0F, 2.0F, 8.0F)
                .texOffs(48, 8).addBox(-2.6F, -3.5F, -4.5F, 1.0F, 1.0F, 2.0F)
                .texOffs(48, 8).mirror().addBox(1.6F, -3.5F, -4.5F, 1.0F, 1.0F, 2.0F), PartPose.offset(0.0F, 18.0F, -8.0F));
        head.addOrReplaceChild("jaw", CubeListBuilder.create().texOffs(0, 45).addBox(-2.5F, 0.0F, -9.0F, 5.0F, 1.0F, 9.0F),
                PartPose.offset(0.0F, 0.5F, -4.0F));
        PartDefinition tail = root.addOrReplaceChild("tail", CubeListBuilder.create().texOffs(36, 20)
                .addBox(-3.0F, -2.0F, 0.0F, 6.0F, 4.0F, 8.0F), PartPose.offset(0.0F, 18.0F, 8.0F));
        PartDefinition tail2 = tail.addOrReplaceChild("tail2", CubeListBuilder.create().texOffs(42, 45)
                .addBox(-2.0F, -1.5F, 0.0F, 4.0F, 3.0F, 7.0F), PartPose.offset(0.0F, 0.3F, 8.0F));
        tail2.addOrReplaceChild("tail3", CubeListBuilder.create().texOffs(0, 55)
                .addBox(-1.0F, -1.0F, 0.0F, 2.0F, 2.0F, 7.0F), PartPose.offset(0.0F, 0.3F, 7.0F));
        for (int i = 0; i < 4; i++) {
            boolean right = i % 2 == 0;
            float z = i < 2 ? -5.0F : 5.0F;
            CubeListBuilder leg = CubeListBuilder.create().texOffs(48, 0);
            if (right) {
                leg.addBox(-1.5F, 0.0F, -1.5F, 3.0F, 4.0F, 3.0F);
            } else {
                leg.mirror().addBox(-1.5F, 0.0F, -1.5F, 3.0F, 4.0F, 3.0F);
            }
            root.addOrReplaceChild("leg" + i, leg, PartPose.offsetAndRotation(right ? -4.0F : 4.0F, 20.7F, z,
                    0.0F, 0.0F, right ? SPLAY : -SPLAY));
        }
        return LayerDefinition.create(mesh, 64, 64);
    }

    @Override
    public ModelPart root() {
        return root;
    }

    @Override
    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        boolean swimming = entity.isInWater();
        for (int i = 0; i < 4; i++) {
            boolean right = i % 2 == 0;
            // Diagonal pairs step together, as a lizard walks.
            float phase = (i == 0 || i == 3) ? 0.0F : Mth.PI;
            if (swimming) {
                legs[i].xRot = 1.2F;
                legs[i].zRot = right ? SPLAY * 0.4F : -SPLAY * 0.4F;
            } else {
                legs[i].xRot = Mth.cos(limbSwing * 0.9F + phase) * 0.9F * limbSwingAmount;
                legs[i].zRot = right ? SPLAY : -SPLAY;
            }
        }
        float sweep = swimming ? 0.35F : 0.12F + 0.25F * limbSwingAmount;
        float speed = swimming ? 0.35F : 0.08F + 0.5F * limbSwingAmount;
        tail.yRot = Mth.sin(ageInTicks * speed) * sweep;
        tail2.yRot = Mth.sin(ageInTicks * speed - 0.8F) * sweep * 1.2F;
        tail3.yRot = Mth.sin(ageInTicks * speed - 1.6F) * sweep * 1.4F;
        head.yRot = netHeadYaw * Mth.DEG_TO_RAD * 0.5F;
        head.xRot = headPitch * Mth.DEG_TO_RAD * 0.3F;
        float gape = entity.isAggressive() ? 0.35F + Math.abs(Mth.sin(ageInTicks * 0.3F)) * 0.35F
                : Math.max(0.0F, Mth.sin(ageInTicks * 0.02F)) * 0.25F;
        jaw.xRot = gape;
    }
}
