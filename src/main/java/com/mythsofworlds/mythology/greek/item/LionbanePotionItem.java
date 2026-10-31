package com.mythsofworlds.mythology.greek.item;

import com.mythsofworlds.mythology.greek.entity.ThrownLionbanePotion;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.ThrowableItemProjectile;
import net.minecraft.world.level.Level;

/**
 * A splash potion brewed against the Nemean Lion: its golden hide drinks the potion in and burns. Six bottles are
 * enough to kill the lion (see {@link ThrownLionbanePotion#BOTTLES_TO_KILL}); every other creature only gets a splash.
 */
public class LionbanePotionItem extends GrowthPotionItem {
    public LionbanePotionItem(Properties properties) {
        super(properties);
    }

    @Override
    protected ThrowableItemProjectile createProjectile(Level level, Player player) {
        return new ThrownLionbanePotion(level, player);
    }
}
