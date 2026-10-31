package com.mythsofworlds.mythology.norse.item;

import com.mythsofworlds.core.StackData;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * Draupnir, the golden ring the dwarves Brokkr and Sindri forged for Odin: every ninth night eight rings as heavy as
 * itself drip from it. Carried, it drips {@value #DRIP} gold nuggets every {@value #PERIOD} ticks (one day), counted
 * from the moment it came to you.
 */
public class DraupnirItem extends Item {
    public static final long PERIOD = 24000L;
    public static final int DRIP = 8;
    public static final String LAST_DRIP = "last_drip";

    public DraupnirItem(Properties properties) {
        super(properties);
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slot, boolean selected) {
        if (!level.isClientSide && entity instanceof Player player && level.getGameTime() % 20 == 0) {
            drip(level, player, stack);
        }
    }

    /** Gives the player the rings of the past day, if one has passed; returns the nuggets given. */
    public static int drip(Level level, Player player, ItemStack stack) {
        long now = level.getGameTime();
        if (!StackData.has(stack, LAST_DRIP)) {
            StackData.putLong(stack, LAST_DRIP, now);
            return 0;
        }
        if (now - StackData.getLong(stack, LAST_DRIP, now) < PERIOD) {
            return 0;
        }
        StackData.putLong(stack, LAST_DRIP, now);
        ItemStack gold = new ItemStack(Items.GOLD_NUGGET, DRIP);
        if (!player.getInventory().add(gold)) {
            player.drop(gold, false);
        }
        level.playSound(null, player.blockPosition(), SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 1.0F, 1.6F);
        player.displayClientMessage(Component.translatable("item.mythsofworlds.draupnir.drip").withStyle(ChatFormatting.GOLD), true);
        return DRIP;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
