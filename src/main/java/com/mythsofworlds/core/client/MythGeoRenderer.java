package com.mythsofworlds.core.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.entity.MythBoss;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import software.bernie.geckolib.model.DefaultedEntityGeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;
import software.bernie.geckolib.renderer.layer.AutoGlowingGeoLayer;

/**
 * A boss drawn with GeckoLib from the files tools/gen_geo_models.py writes: geo/entity/boss/&lt;name&gt;.geo.json,
 * animations/entity/boss/&lt;name&gt;.animation.json and textures/entity/boss/&lt;name&gt;.png. The parts painted in the
 * &lt;name&gt;_glowmask.png texture (eyes, fire, lava, ice) glow in the dark; the script writes that texture only for
 * models with glowing parts, and the glow layer is added only where it exists (an empty mask crashes GeckoLib).
 * The head bone turns to look. Renderers are made again on every resource reload, so a resource pack may add a mask.
 */
public class MythGeoRenderer<T extends MythBoss> extends GeoEntityRenderer<T> {
    public MythGeoRenderer(EntityRendererProvider.Context context, String name, float shadow) {
        super(context, new DefaultedEntityGeoModel<>(MythsOfWorlds.id("boss/" + name), true));
        if (context.getResourceManager().getResource(MythsOfWorlds.id("textures/entity/boss/" + name + "_glowmask.png")).isPresent()) {
            addRenderLayer(new AutoGlowingGeoLayer<>(this));
        }
        this.shadowRadius = shadow;
    }
}
