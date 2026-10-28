package com.mythsofworlds.core.portal;

import java.util.function.Supplier;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;

/**
 * Everything that makes one mythology's portal different from another.
 *
 * @param frame       block the frame must be built from (e.g. runestone)
 * @param destination dimension the portal leads to (e.g. Jotunheim)
 * @param home        dimension you return to when using the portal inside {@code destination}
 * @param particle    particle the portal surface emits
 * @param delayTicks  how long a survival player must stand inside before travelling (20 ticks = 1 s)
 */
public record PortalSettings(
        Supplier<? extends Block> frame,
        ResourceKey<Level> destination,
        ResourceKey<Level> home,
        ParticleOptions particle,
        int delayTicks) {

    /** Portal from the Overworld to {@code destination} with a 3 second delay. */
    public static PortalSettings toDimension(Supplier<? extends Block> frame, ResourceKey<Level> destination,
                                             ParticleOptions particle) {
        return new PortalSettings(frame, destination, Level.OVERWORLD, particle, 60);
    }
}
