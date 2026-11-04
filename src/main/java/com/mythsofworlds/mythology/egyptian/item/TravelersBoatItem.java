package com.mythsofworlds.mythology.egyptian.item;

import com.mythsofworlds.mythology.egyptian.entity.TravelersBoat;
import java.util.List;
import java.util.function.Predicate;
import net.minecraft.stats.Stats;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySelector;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.gameevent.GameEvent;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/** Places the traveller's boat on water (or land) where the player looks, as a vanilla boat item does. */
public class TravelersBoatItem extends Item {
    private static final Predicate<Entity> ENTITY_PREDICATE = EntitySelector.NO_SPECTATORS.and(Entity::isPickable);

    public TravelersBoatItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        HitResult hit = getPlayerPOVHitResult(level, player, ClipContext.Fluid.ANY);
        if (hit.getType() != HitResult.Type.BLOCK) {
            return InteractionResultHolder.pass(stack);
        }
        Vec3 view = player.getViewVector(1.0F);
        List<Entity> near = level.getEntities(player, player.getBoundingBox().expandTowards(view.scale(5.0)).inflate(1.0), ENTITY_PREDICATE);
        Vec3 eye = player.getEyePosition();
        for (Entity entity : near) {
            AABB box = entity.getBoundingBox().inflate(entity.getPickRadius());
            if (box.contains(eye)) {
                return InteractionResultHolder.pass(stack);
            }
        }
        Vec3 at = hit.getLocation();
        TravelersBoat boat = new TravelersBoat(level, at.x, at.y, at.z);
        boat.setYRot(player.getYRot());
        if (!level.noCollision(boat, boat.getBoundingBox())) {
            return InteractionResultHolder.fail(stack);
        }
        if (!level.isClientSide) {
            level.addFreshEntity(boat);
            level.gameEvent(player, GameEvent.ENTITY_PLACE, at);
            stack.consume(1, player);
        }
        player.awardStat(Stats.ITEM_USED.get(this));
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }
}
