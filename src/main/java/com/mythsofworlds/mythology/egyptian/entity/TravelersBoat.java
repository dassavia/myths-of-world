package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.vehicle.Boat;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;

/**
 * The traveller's boat: a skiff of bound papyrus with a linen sail, like those that ply the Nile. It is a vanilla boat
 * in everything (it floats, paddles, carries two, breaks into its item), only built and drawn differently
 * (client/TravelersBoatRenderer, texture textures/entity/boat/travelers_boat.png).
 */
public class TravelersBoat extends Boat {
    public TravelersBoat(EntityType<? extends Boat> type, Level level) {
        super(type, level);
    }

    public TravelersBoat(Level level, double x, double y, double z) {
        this(EgyptianEntities.TRAVELERS_BOAT.get(), level);
        setPos(x, y, z);
        xo = x;
        yo = y;
        zo = z;
    }

    @Override
    public Item getDropItem() {
        return EgyptianContent.TRAVELERS_BOAT.get();
    }
}
