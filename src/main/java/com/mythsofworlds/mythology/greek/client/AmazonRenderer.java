package com.mythsofworlds.mythology.greek.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.egyptian.entity.Priestess;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.greek.entity.Hippolyta;
import com.mythsofworlds.mythology.norse.entity.Valkyrie;
import java.util.HashMap;
import java.util.Map;
import net.minecraft.client.model.PlayerModel;
import net.minecraft.client.model.geom.ModelLayers;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.HumanoidMobRenderer;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.fml.ModList;

/**
 * Amazons, Hippolyta and the valkyries of Jotunheim: the classic wide player model (with its hair and dress overlay
 * layers) and the texture {@link Amazon#textureName()} names: amazon_0 to amazon_15 (4 is the royal look of
 * Hippolyta's daughters), hippolyta, valkyrie_0 to valkyrie_7, priestess_0 to priestess_7. Every one is a little taller or
 * shorter than the next. With MCA Reborn installed, all but Hippolyta may wear its women's looks instead
 * (compat/mca/McaSkins), the mod's texture staying the fallback.
 */
public class AmazonRenderer extends HumanoidMobRenderer<Amazon, PlayerModel<Amazon>> {
    private static final Map<String, ResourceLocation> TEXTURES = new HashMap<>();

    public AmazonRenderer(EntityRendererProvider.Context context) {
        super(context, new PlayerModel<>(context.bakeLayer(ModelLayers.PLAYER), false), 0.5F);
        // With MCA Reborn the women may wear its looks; the compat classes are only touched when it is installed.
        if (ModList.get().isLoaded("mca")) {
            addLayer(new com.mythsofworlds.compat.mca.McaLookLayer(this, AmazonRenderer::mcaLook, AmazonRenderer::ownTexture));
        }
    }

    @Override
    public ResourceLocation getTextureLocation(Amazon entity) {
        if (ModList.get().isLoaded("mca")) {
            com.mythsofworlds.compat.mca.McaSkins.Look look = mcaLook(entity);
            if (look != null) {
                return look.skin();
            }
        }
        return ownTexture(entity);
    }

    /** The mod's own texture of this woman, the default and the fallback. */
    public static ResourceLocation ownTexture(Amazon entity) {
        return TEXTURES.computeIfAbsent(entity.textureName(), name -> MythsOfWorlds.id("textures/entity/" + name + ".png"));
    }

    /** Her MCA look (priestesses, amazons and valkyries; never Hippolyta), or null. Only called when MCA is installed. */
    private static com.mythsofworlds.compat.mca.McaSkins.Look mcaLook(Amazon entity) {
        if (entity instanceof Hippolyta) {
            return null;
        }
        var role = entity instanceof Priestess ? com.mythsofworlds.compat.mca.McaSkins.Role.PRIESTESS
                : entity instanceof Valkyrie ? com.mythsofworlds.compat.mca.McaSkins.Role.VALKYRIE
                : com.mythsofworlds.compat.mca.McaSkins.Role.AMAZON;
        return com.mythsofworlds.compat.mca.McaSkins.INSTANCE.look(entity.getUUID(), role);
    }

    @Override
    protected void scale(Amazon entity, PoseStack poseStack, float partialTick) {
        float scale = entity instanceof Hippolyta ? 1.0F : 0.92F + Math.floorMod(entity.getUUID().hashCode(), 5) * 0.02F;
        poseStack.scale(scale, scale, scale);
    }
}
