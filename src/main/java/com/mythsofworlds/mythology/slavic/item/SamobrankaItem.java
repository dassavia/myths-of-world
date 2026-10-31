package com.mythsofworlds.mythology.slavic.item;

import com.mythsofworlds.core.StackData;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * The self-laying tablecloth of the tales: unfold it (right-click) and it covers itself with a feast. It does so once a
 * day ({@value #DAY} ticks); then it must rest.
 */
public class SamobrankaItem extends Item {
    public static final long DAY = 24000L;
    public static final String LAST_FEAST = "last_feast";

    public SamobrankaItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide) {
            return InteractionResultHolder.success(stack);
        }
        if (!feast(level, player, stack)) {
            player.displayClientMessage(Component.translatable("item.mythsofworlds.samobranka.resting"), true);
            return InteractionResultHolder.fail(stack);
        }
        player.displayClientMessage(Component.translatable("item.mythsofworlds.samobranka.feast").withStyle(ChatFormatting.GOLD), true);
        level.playSound(null, player.blockPosition(), SoundEvents.WOOL_PLACE, SoundSource.PLAYERS, 1.0F, 1.0F);
        level.playSound(null, player.blockPosition(), SoundEvents.PLAYER_LEVELUP, SoundSource.PLAYERS, 0.5F, 1.6F);
        return InteractionResultHolder.success(stack);
    }

    /** Lays the feast before the player if a day has passed since the last one; false if the cloth still rests. */
    public static boolean feast(Level level, Player player, ItemStack stack) {
        long now = level.getGameTime();
        long last = StackData.getLong(stack, LAST_FEAST, -DAY);
        if (now - last < DAY) {
            return false;
        }
        StackData.putLong(stack, LAST_FEAST, now);
        RandomSource random = level.random;
        give(player, new ItemStack(SlavicContent.KARAVAI.get(), 2));
        give(player, new ItemStack(random.nextBoolean() ? Items.COOKED_BEEF : Items.COOKED_CHICKEN, 3));
        give(player, new ItemStack(Items.BAKED_POTATO, 3));
        give(player, new ItemStack(random.nextBoolean() ? Items.PUMPKIN_PIE : Items.MUSHROOM_STEW, 1));
        give(player, new ItemStack(Items.HONEY_BOTTLE, 2));
        return true;
    }

    private static void give(Player player, ItemStack stack) {
        if (!player.getInventory().add(stack)) {
            player.drop(stack, false);
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
