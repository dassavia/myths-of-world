package com.mythsofworlds.journal;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.game.ClientboundOpenBookPacket;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.stats.Stats;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * A journal of one mythology. Right-click to read it: the pages are written afresh each time from what the player
 * has found (or, for the complete creative copy, from every entry), and shown in the vanilla book screen.
 */
public class JournalItem extends Item {
    private final String volume;
    private final boolean complete;

    public JournalItem(String volume, boolean complete, Properties properties) {
        super(properties);
        this.volume = volume;
        this.complete = complete;
    }

    public String volume() {
        return volume;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player instanceof ServerPlayer serverPlayer) {
            stack.set(DataComponents.WRITTEN_BOOK_CONTENT, Journal.book(volume, player, complete));
            // Send the freshly written pages before the packet that opens the book. ServerPlayer.openItemGui only
            // sends that packet for vanilla written books, so send it ourselves.
            serverPlayer.containerMenu.broadcastChanges();
            serverPlayer.connection.send(new ClientboundOpenBookPacket(hand));
            player.awardStat(Stats.ITEM_USED.get(this));
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return complete;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(complete ? "item.mythsofworlds.journal.complete" : "item.mythsofworlds.journal.desc")
                .withStyle(ChatFormatting.GRAY));
    }
}
