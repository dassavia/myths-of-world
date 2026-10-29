package com.mythsofworlds.core.back;

import com.mojang.datafixers.util.Pair;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.item.WingsItem;
import java.util.Map;
import java.util.WeakHashMap;
import java.util.function.BooleanSupplier;
import java.util.function.Supplier;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.SimpleContainer;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.inventory.Slot;
import net.minecraft.world.item.ElytraItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.GameRules;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.attachment.AttachmentType;
import net.neoforged.neoforge.event.entity.living.LivingDropsEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.neoforge.items.ItemStackHandler;
import net.neoforged.neoforge.network.PacketDistributor;
import org.jetbrains.annotations.Nullable;

import static com.mythsofworlds.registry.ModRegistries.ATTACHMENT_TYPES;

/**
 * A slot on the back, next to the player in the inventory, for an elytra or the wings of Daedalus: wear them over a
 * chestplate. An elytra on the back flies whenever the chest slot holds nothing that can fly (see the mixins in
 * com.mythsofworlds.mixin); the wings work from the back as from the chest. The slot is kept on death with
 * keepInventory and dropped otherwise, and every player nearby sees what you carry on your back ({@link BackPayload}).
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class BackSlot {
    public static final Supplier<AttachmentType<ItemStackHandler>> BACK = ATTACHMENT_TYPES.register("back",
            () -> AttachmentType.serializable(() -> new ItemStackHandler(1)).copyOnDeath().build());
    /** Where the slot sits in the survival inventory, next to the offhand slot. */
    public static final int X = 77;
    public static final int Y = 44;
    public static final ResourceLocation EMPTY_ICON = MythsOfWorlds.id("item/empty_slot_back");
    /** True on the client while a screen is open that has no room for the slot (the creative inventory). */
    public static BooleanSupplier hidden = () -> false;

    private static final Map<Player, ItemStack> SENT = new WeakHashMap<>();

    private BackSlot() {
    }

    public static void init() {
    }

    /** What {@code player} carries on the back (the stack itself, not a copy). */
    public static ItemStack get(Player player) {
        return player.getData(BACK).getStackInSlot(0);
    }

    public static void set(Player player, ItemStack stack) {
        player.getData(BACK).setStackInSlot(0, stack);
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
    public static void onDrops(LivingDropsEvent event) {
        if (!(event.getEntity() instanceof Player player) || player.level().getGameRules().getBoolean(GameRules.RULE_KEEPINVENTORY)) {
            return;
        }
        ItemStack back = get(player);
        if (!back.isEmpty()) {
            ItemEntity drop = new ItemEntity(player.level(), player.getX(), player.getEyeY() - 0.3, player.getZ(), back.copy());
            drop.setPickUpDelay(40);
            event.getDrops().add(drop);
            set(player, ItemStack.EMPTY);
        }
    }

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        if (!(event.getEntity() instanceof ServerPlayer player)) {
            return;
        }
        ItemStack back = get(player);
        if (player.tickCount % 10 == 0) {
            ItemStack sent = SENT.get(player);
            if (sent == null || !ItemStack.matches(sent, back)) {
                SENT.put(player, back.copy());
                PacketDistributor.sendToPlayersTrackingEntityAndSelf(player, new BackPayload(player.getId(), back.copy()));
            }
        }
    }

    @SubscribeEvent
    public static void onStartTracking(PlayerEvent.StartTracking event) {
        if (event.getTarget() instanceof Player target && event.getEntity() instanceof ServerPlayer watcher) {
            PacketDistributor.sendToPlayer(watcher, new BackPayload(target.getId(), get(target).copy()));
        }
    }

    @SubscribeEvent
    public static void onRespawn(PlayerEvent.PlayerRespawnEvent event) {
        SENT.remove(event.getEntity());
    }

    @SubscribeEvent
    public static void onChangeDimension(PlayerEvent.PlayerChangedDimensionEvent event) {
        SENT.remove(event.getEntity());
    }

    /** The back slot in the player's inventory menu. It always reads the player's current attachment. */
    public static class BackSlotUI extends Slot {
        private final Player player;

        public BackSlotUI(Player player) {
            super(new SimpleContainer(1), 0, X, Y);
            this.player = player;
        }

        @Override
        public ItemStack getItem() {
            return get(player);
        }

        @Override
        public void set(ItemStack stack) {
            BackSlot.set(player, stack);
            setChanged();
        }

        @Override
        public void setByPlayer(ItemStack stack, ItemStack previous) {
            set(stack);
        }

        @Override
        public ItemStack remove(int amount) {
            return player.getData(BACK).extractItem(0, amount, false);
        }

        @Override
        public void setChanged() {
        }

        @Override
        public boolean mayPlace(ItemStack stack) {
            return canWear(stack);
        }

        @Override
        public int getMaxStackSize() {
            return 1;
        }

        @Override
        public int getMaxStackSize(ItemStack stack) {
            return 1;
        }

        @Override
        public boolean isActive() {
            return !hidden.getAsBoolean();
        }

        @Nullable
        @Override
        public Pair<ResourceLocation, ResourceLocation> getNoItemIcon() {
            return Pair.of(InventoryMenu.BLOCK_ATLAS, EMPTY_ICON);
        }
    }
}
