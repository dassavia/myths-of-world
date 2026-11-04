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
 * The scorpion of Serket: a flat carapace and three body segments low over the sand, eight jointed legs that bend at
 * the knee, two pedipalps ending in heavy pincers that snap, and a tail of five segments raised in a curve over the
 * back with the bulb of venom and the stinger pointing forward. The tail sways while it waits and strikes forward
 * when it attacks. Texture 64x64; the UV layout is mirrored in tools/textures_egyptian.py (scorpion).
 */
public class ScorpionModel<T extends Mob> extends HierarchicalModel<T> {
    private static final int TAIL_SEGMENTS = 5;
    /** How far each tail segment bends up from the one before, in radians: five of them curl the tail over the back. */
    private static final float TAIL_CURL = 0.5F;
    private static final float LEG_LIFT = 0.4F;
    private static final float KNEE = 1.5F;
    private static final float[] LEG_SPREAD = {0.6F, 0.2F, -0.2F, -0.6F};
    private static final float[] LEG_Z = {-6.0F, -4.0F, -2.0F, 0.0F};

    private final ModelPart root;
    private final ModelPart[] legs = new ModelPart[8];
    private final ModelPart[] tail = new ModelPart[TAIL_SEGMENTS];
    private final ModelPart[] arms = new ModelPart[2];
    private final ModelPart[] fingers = new ModelPart[2];

    public ScorpionModel(ModelPart root) {
        this.root = root;
        for (int i = 0; i < 8; i++) {
            legs[i] = root.getChild("leg" + i);
        }
        ModelPart segment = root;
        for (int i = 0; i < TAIL_SEGMENTS; i++) {
            segment = segment.getChild("tail" + i);
            tail[i] = segment;
        }
        for (int side = 0; side < 2; side++) {
            arms[side] = root.getChild("arm" + side);
            fingers[side] = arms[side].getChild("forearm").getChild("hand").getChild("finger");
        }
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition mesh = new MeshDefinition();
        PartDefinition root = mesh.getRoot();
        // The flat body: the carapace over the head with the eyes, and three segments narrowing towards the tail.
        root.addOrReplaceChild("carapace", CubeListBuilder.create().texOffs(0, 0).addBox(-3.5F, -1.0F, -6.0F, 7.0F, 2.0F, 6.0F),
                PartPose.offset(0.0F, 20.0F, -1.5F));
        root.addOrReplaceChild("segment0", CubeListBuilder.create().texOffs(0, 8).addBox(-3.5F, -1.0F, 0.0F, 7.0F, 2.0F, 3.0F),
                PartPose.offset(0.0F, 20.2F, -1.5F));
        root.addOrReplaceChild("segment1", CubeListBuilder.create().texOffs(20, 8).addBox(-3.0F, -1.0F, 0.0F, 6.0F, 2.0F, 3.0F),
                PartPose.offset(0.0F, 20.2F, 1.5F));
        root.addOrReplaceChild("segment2", CubeListBuilder.create().texOffs(38, 8).addBox(-2.5F, -1.0F, 0.0F, 5.0F, 2.0F, 3.0F),
                PartPose.offset(0.0F, 20.2F, 4.5F));
        // The tail: five segments, each bent up from the last, then the bulb of venom and the stinger.
        PartDefinition parent = root;
        for (int i = 0; i < TAIL_SEGMENTS; i++) {
            parent = parent.addOrReplaceChild("tail" + i, CubeListBuilder.create().texOffs(0, 14)
                            .addBox(-1.0F, -1.0F, 0.0F, 2.0F, 2.0F, 3.0F),
                    PartPose.offsetAndRotation(0.0F, i == 0 ? 19.8F : 0.0F, i == 0 ? 7.5F : 3.0F, TAIL_CURL, 0.0F, 0.0F));
        }
        PartDefinition telson = parent.addOrReplaceChild("telson", CubeListBuilder.create().texOffs(10, 14)
                .addBox(-1.0F, -1.0F, 0.0F, 2.0F, 2.0F, 2.0F), PartPose.offset(0.0F, 0.0F, 3.0F));
        telson.addOrReplaceChild("stinger", CubeListBuilder.create().texOffs(18, 14)
                .addBox(-0.5F, -0.5F, 0.0F, 1.0F, 1.0F, 2.0F), PartPose.offsetAndRotation(0.0F, 0.5F, 2.0F, 0.6F, 0.0F, 0.0F));
        // Eight legs, four on each side, each in two parts bent at the knee.
        for (int i = 0; i < 8; i++) {
            boolean right = i < 4;
            float s = right ? 1.0F : -1.0F;
            CubeListBuilder upper = CubeListBuilder.create().texOffs(0, 20);
            CubeListBuilder lower = CubeListBuilder.create().texOffs(0, 22);
            if (right) {
                upper.addBox(0.0F, -0.5F, -0.5F, 4.0F, 1.0F, 1.0F);
                lower.addBox(0.0F, -0.5F, -0.5F, 5.0F, 1.0F, 1.0F);
            } else {
                upper.mirror().addBox(-4.0F, -0.5F, -0.5F, 4.0F, 1.0F, 1.0F);
                lower.mirror().addBox(-5.0F, -0.5F, -0.5F, 5.0F, 1.0F, 1.0F);
            }
            PartDefinition leg = root.addOrReplaceChild("leg" + i, upper, PartPose.offsetAndRotation(s * 2.8F, 20.5F,
                    LEG_Z[i % 4], 0.0F, s * LEG_SPREAD[i % 4], -s * LEG_LIFT));
            leg.addOrReplaceChild("knee", lower, PartPose.offsetAndRotation(s * 4.0F, 0.0F, 0.0F, 0.0F, 0.0F, s * KNEE));
        }
        // The pedipalps: an arm reaching forward and out, a forearm folding back in, and the pincer at the end.
        for (int side = 0; side < 2; side++) {
            float s = side == 0 ? 1.0F : -1.0F;
            PartDefinition arm = root.addOrReplaceChild("arm" + side, CubeListBuilder.create().texOffs(0, 25)
                            .addBox(-0.5F, -0.5F, -4.0F, 1.0F, 1.0F, 4.0F),
                    PartPose.offsetAndRotation(s * 2.5F, 20.0F, -7.0F, 0.0F, -s * 0.6F, 0.0F));
            PartDefinition forearm = arm.addOrReplaceChild("forearm", CubeListBuilder.create().texOffs(10, 25)
                            .addBox(-0.5F, -0.5F, -3.0F, 1.0F, 1.0F, 3.0F),
                    PartPose.offsetAndRotation(0.0F, 0.0F, -4.0F, 0.0F, s * 1.1F, 0.0F));
            CubeListBuilder hand = CubeListBuilder.create().texOffs(0, 31).addBox(-1.5F, -1.0F, -3.0F, 3.0F, 2.0F, 3.0F)
                    .texOffs(12, 31);
            if (side == 0) {
                hand.addBox(0.0F, -0.5F, -6.0F, 1.0F, 1.0F, 3.0F);
            } else {
                hand.mirror().addBox(-1.0F, -0.5F, -6.0F, 1.0F, 1.0F, 3.0F);
            }
            PartDefinition palm = forearm.addOrReplaceChild("hand", hand,
                    PartPose.offsetAndRotation(0.0F, 0.0F, -3.0F, 0.0F, -s * 0.5F, 0.0F));
            palm.addOrReplaceChild("finger", CubeListBuilder.create().texOffs(20, 31).mirror(side == 1)
                    .addBox(-0.5F, -0.5F, -3.0F, 1.0F, 1.0F, 3.0F), PartPose.offset(-s * 0.5F, 0.0F, -3.0F));
        }
        return LayerDefinition.create(mesh, 64, 64);
    }

    @Override
    public ModelPart root() {
        return root;
    }

    @Override
    public void setupAnim(T entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        // The legs step in waves, alternate legs together, each lifting a little as it swings forward.
        for (int i = 0; i < 8; i++) {
            float s = i < 4 ? 1.0F : -1.0F;
            float phase = limbSwing * 1.4F + i * 1.3F + (i < 4 ? 0.0F : Mth.PI);
            legs[i].yRot = s * LEG_SPREAD[i % 4] + Mth.sin(phase) * 0.3F * limbSwingAmount;
            legs[i].zRot = -s * (LEG_LIFT + Math.max(0.0F, Mth.cos(phase)) * 0.3F * limbSwingAmount);
        }
        // The tail sways while it waits, curls tighter when angry and lashes forward with the sting when it attacks.
        float strike = Mth.sin(attackTime * Mth.PI);
        float tense = entity.isAggressive() ? 0.06F : 0.0F;
        for (int i = 0; i < TAIL_SEGMENTS; i++) {
            tail[i].xRot = TAIL_CURL + tense + Mth.sin(ageInTicks * 0.08F - i * 0.5F) * 0.04F + strike * 0.22F;
            tail[i].yRot = i == 0 ? Mth.sin(ageInTicks * 0.05F) * 0.12F : 0.0F;
        }
        // The pincers follow the head and snap, faster when it hunts.
        float snapSpeed = entity.isAggressive() ? 0.6F : 0.25F;
        float snap = Math.max(0.0F, Mth.sin(ageInTicks * snapSpeed)) * 0.5F;
        for (int side = 0; side < 2; side++) {
            float s = side == 0 ? 1.0F : -1.0F;
            arms[side].yRot = -s * 0.6F + netHeadYaw * Mth.DEG_TO_RAD * 0.3F;
            arms[side].xRot = Mth.sin(ageInTicks * 0.1F) * 0.08F * s - strike * 0.3F;
            fingers[side].yRot = s * snap;
        }
    }
}
