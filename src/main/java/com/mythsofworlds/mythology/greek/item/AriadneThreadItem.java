package com.mythsofworlds.mythology.greek.item;

import com.mythsofworlds.core.StackData;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * The thread Ariadne gave Theseus, so that he could find his way out of the Labyrinth. Crouch and right-click to tie
 * its end where you stand; right-click anywhere in the same world to follow it back there at once. Each return uses a
 * little of the thread.
 */
public class AriadneThreadItem extends Item {
    public static final String KNOT = "knot";
    public static final String WORLD = "knot_world";

    public AriadneThreadItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide || !(player instanceof ServerPlayer serverPlayer)) {
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
        }
        if (player.isShiftKeyDown()) {
            tie(stack, player.blockPosition(), level);
            player.displayClientMessage(Component.translatable("item.mythsofworlds.ariadne_thread.tied"), true);
            level.playSound(null, player.blockPosition(), SoundEvents.LEASH_KNOT_PLACE, SoundSource.PLAYERS, 1.0F, 1.0F);
            return InteractionResultHolder.success(stack);
        }
        if (!StackData.has(stack, KNOT)) {
            player.displayClientMessage(Component.translatable("item.mythsofworlds.ariadne_thread.untied"), true);
            return InteractionResultHolder.fail(stack);
        }
        if (!StackData.getString(stack, WORLD).equals(level.dimension().location().toString())) {
            player.displayClientMessage(Component.translatable("item.mythsofworlds.ariadne_thread.other_world"), true);
            return InteractionResultHolder.fail(stack);
        }
        follow(serverPlayer, stack, hand);
        return InteractionResultHolder.success(stack);
    }

    /** Ties the end of the thread at {@code pos}. */
    public static void tie(ItemStack stack, BlockPos pos, Level level) {
        StackData.putLong(stack, KNOT, pos.asLong());
        StackData.putString(stack, WORLD, level.dimension().location().toString());
    }

    /** Walks the player back along the thread to its knot. */
    public static void follow(ServerPlayer player, ItemStack stack, InteractionHand hand) {
        BlockPos knot = BlockPos.of(StackData.getLong(stack, KNOT, 0L));
        ServerLevel level = player.serverLevel();
        level.sendParticles(ParticleTypes.ENCHANT, player.getX(), player.getY(1.0), player.getZ(), 30, 0.4, 0.6, 0.4, 0.5);
        player.teleportTo(knot.getX() + 0.5, knot.getY(), knot.getZ() + 0.5);
        player.resetFallDistance();
        level.sendParticles(ParticleTypes.ENCHANT, player.getX(), player.getY(1.0), player.getZ(), 30, 0.4, 0.6, 0.4, 0.5);
        level.playSound(null, knot, SoundEvents.WOOL_PLACE, SoundSource.PLAYERS, 1.0F, 0.8F);
        player.getCooldowns().addCooldown(stack.getItem(), 40);
        stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
        if (StackData.has(stack, KNOT)) {
            BlockPos knot = BlockPos.of(StackData.getLong(stack, KNOT, 0L));
            tooltip.add(Component.translatable(getDescriptionId() + ".knot", knot.getX(), knot.getY(), knot.getZ())
                    .withStyle(ChatFormatting.GOLD));
        }
    }
}
