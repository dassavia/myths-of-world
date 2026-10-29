package com.mythsofworlds.mythology;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.indian.IndianContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.oceanic.OceanicContent;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.Level;

/**
 * The six mythologies of the mod and the world (dimension) each one leads to.
 * Greek, Norse and Slavic have portals; the others are stubs: their dimension exists (reach it with
 * {@code /execute in mythsofworlds:<id> run tp @s ~ 120 ~}) but has no portal or own content yet.
 */
public enum Mythology {
    GREEK(GreekContent.HELLAS, true),
    NORSE(NorseContent.JOTUNHEIM, true),
    SLAVIC(SlavicContent.NAV, true),
    OCEANIC(OceanicContent.HAWAIKI, false),
    EGYPTIAN(EgyptianContent.DUAT, false),
    INDIAN(IndianContent.SVARGA, false);

    private final ResourceKey<Level> dimension;
    private final boolean hasPortal;

    Mythology(ResourceKey<Level> dimension, boolean hasPortal) {
        this.dimension = dimension;
        this.hasPortal = hasPortal;
    }

    public ResourceKey<Level> dimension() {
        return dimension;
    }

    public boolean hasPortal() {
        return hasPortal;
    }
}
