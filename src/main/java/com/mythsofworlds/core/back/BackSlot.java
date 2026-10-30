package com.mythsofworlds.core.back;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.item.WingsItem;
import java.util.function.Supplier;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ElytraItem;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.attachment.AttachmentType;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.items.ItemStackHandler;
import top.theillusivec4.curios.api.CuriosApi;

import static com.mythsofworlds.registry.ModRegistries.ATTACHMENT_TYPES;

/**
 * The back slot for an elytra or the wings of Daedalus, worn over a chestplate. The slot itself is the "back" slot of
 * the Curios API (data/mythsofworlds/curios: the slot, the player having it, and the items allowed in it through the
 * curios:back tag), so it shows in the Curios inventory with the other accessories, is kept or dropped on death the
 * way Curios does it and is seen by every player nearby. An elytra on the back flies whenever the chest slot holds
 * nothing that can fly (see the mixins in com.mythsofworlds.mixin); the wings work from the back as from the chest.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class BackSlot {
    public static final String CURIOS_SLOT = "back";
    /**
     * The slot of the mod before 0.12, kept only to hand back what a player had in it: on login it moves into the
     * Curios slot, or into the inventory if that is taken.
     */
    public static final Supplier<AttachmentType<ItemStackHandler>> OLD_BACK = ATTACHMENT_TYPES.register("back",
            () -> AttachmentType.serializable(() -> new ItemStackHandler(1)).copyOnDeath().build());

    private BackSlot() {
    }

    public static void init() {
    }

    /** What {@code entity} carries on the back, or an empty stack. */
    public static ItemStack get(LivingEntity entity) {
        return CuriosApi.getCuriosInventory(entity)
                .flatMap(inventory -> inventory.getStacksHandler(CURIOS_SLOT))
                .filter(handler -> handler.getSlots() > 0)
                .map(handler -> handler.getStacks().getStackInSlot(0))
                .filter(BackSlot::canWear)
                .orElse(ItemStack.EMPTY);
    }

    /** Puts {@code stack} on the back of {@code entity}, if it has a back slot. */
    public static void set(LivingEntity entity, ItemStack stack) {
        CuriosApi.getCuriosInventory(entity).ifPresent(inventory -> inventory.setEquippedCurio(CURIOS_SLOT, 0, stack));
    }

    /** Whether {@code stack} can be worn on the back: an elytra or the wings of Daedalus. */
    public static boolean canWear(ItemStack stack) {
        return stack.getItem() instanceof ElytraItem || stack.getItem() instanceof WingsItem;
    }

    /**
     * The stack that decides whether {@code entity} can glide: the chest slot, or an elytra on the back when the chest
     * holds nothing that flies. Used by the mixins in place of the chest slot.
     */
    public static ItemStack flyingStack(LivingEntity entity, ItemStack chest) {
        if (entity instanceof Player player && !chest.canElytraFly(player)) {
            ItemStack back = get(player);
            if (!back.isEmpty() && back.canElytraFly(player)) {
                return back;
            }
        }
        return chest;
    }

    @SubscribeEvent
    public static void onLogin(PlayerEvent.PlayerLoggedInEvent event) {
        Player player = event.getEntity();
        if (!player.hasData(OLD_BACK)) {
            return;
        }
        ItemStack old = player.getData(OLD_BACK).getStackInSlot(0).copy();
        player.removeData(OLD_BACK);
        if (old.isEmpty()) {
            return;
        }
        if (get(player).isEmpty() && CuriosApi.getCuriosInventory(player).isPresent()) {
            set(player, old);
        } else if (!player.getInventory().add(old)) {
            player.drop(old, false);
        }
    }
}
