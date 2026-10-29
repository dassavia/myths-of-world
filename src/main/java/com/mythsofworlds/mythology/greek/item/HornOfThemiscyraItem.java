package com.mythsofworlds.mythology.greek.item;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.TagKey;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.Structure;

/**
 * The war horn of Themiscyra. Blow it and every amazon within {@value #RANGE} blocks who has no family goes back to
 * the camp or city she came from (she comes at once if she wandered far). Wives and daughters stay with you.
 */
public class HornOfThemiscyraItem extends Item {
    public static final double RANGE = 96.0;
    /** The amazon camps and Themiscyra. */
    public static final TagKey<Structure> HOMES = TagKey.create(Registries.STRUCTURE, MythsOfWorlds.id("amazon_homes"));
    private static final int COOLDOWN_TICKS = 100;

    public HornOfThemiscyraItem(Properties properties) {
        super(properties);
    }

    /** Sends the amazons around {@code player} home; returns how many obeyed. */
    public static int callAmazons(ServerLevel level, Player player) {
        int called = 0;
        BlockPos outpost = null;
        boolean searched = false;
        for (Amazon amazon : level.getEntitiesOfClass(Amazon.class, player.getBoundingBox().inflate(RANGE))) {
            if (amazon.home() == null && amazon.bond() == Amazon.Bond.NONE) {
                // Amazons from before 0.5 did not remember their camp: send them to the nearest one.
                if (!searched) {
                    searched = true;
                    BlockPos found = level.findNearestMapStructure(HOMES, player.blockPosition(), 64, false);
                    if (found != null) {
                        outpost = level.getHeightmapPos(Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, found.offset(8, 0, 8));
                    }
                }
                if (outpost != null) {
                    amazon.setHome(outpost, Amazon.HOME_RADIUS);
                }
            }
            if (amazon.callHome()) {
                called++;
            }
        }
        return called;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.RAID_HORN.value(), SoundSource.PLAYERS,
                4.0F, 1.2F);
        if (!level.isClientSide) {
            int called = callAmazons((ServerLevel) level, player);
            player.displayClientMessage(Component.translatable("item.mythsofworlds.horn_of_themiscyra.called", called)
                    .withStyle(ChatFormatting.LIGHT_PURPLE), true);
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.mythsofworlds.horn_of_themiscyra.desc").withStyle(ChatFormatting.GRAY));
    }
}
