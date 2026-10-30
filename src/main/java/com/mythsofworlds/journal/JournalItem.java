package com.mythsofworlds.journal;

import com.mythsofworlds.codex.CodexBook;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
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
 * A journal of one mythology, from before the Codex of Myths gathered them all: right-click opens the Codex. No longer
 * made or handed out, it stays so that old copies keep working.
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
        if (player instanceof ServerPlayer serverPlayer) {
            player.awardStat(Stats.ITEM_USED.get(this));
            CodexBook.open(serverPlayer);
        }
        return InteractionResultHolder.sidedSuccess(player.getItemInHand(hand), level.isClientSide());
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
