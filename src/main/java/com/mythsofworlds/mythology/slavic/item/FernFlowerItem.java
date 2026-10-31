package com.mythsofworlds.mythology.slavic.item;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.Container;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.common.Tags;

/**
 * The flower of the fern, which blooms for a single moment on the night of Kupala and shows its finder where treasure
 * lies. Planted (right-click a block) it grows again; raised to the sky (right-click the air) it withers and lights up
 * every ore and chest within {@value #RADIUS} blocks, and grants luck.
 */
public class FernFlowerItem extends BlockItem {
    public static final int RADIUS = 16;
    private static final int MAX_SHOWN = 96;

    public FernFlowerItem(Block block, Properties properties) {
        super(block, properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!(level instanceof ServerLevel server)) {
            return InteractionResultHolder.success(stack);
        }
        int found = revealTreasure(server, player.blockPosition());
        player.addEffect(new MobEffectInstance(MobEffects.LUCK, 20 * 60 * 3, 1));
        player.displayClientMessage(Component.translatable("item.mythsofworlds.fern_flower.reveal", found)
                .withStyle(ChatFormatting.GOLD), true);
        level.playSound(null, player.blockPosition(), SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.PLAYERS, 1.0F, 1.4F);
        stack.consume(1, player);
        return InteractionResultHolder.consume(stack);
    }

    /** True for what the flower shows: ores of any kind and chests, barrels and other containers. */
    public static boolean isTreasure(ServerLevel level, BlockPos pos, BlockState state) {
        return state.is(Tags.Blocks.ORES) || level.getBlockEntity(pos) instanceof Container;
    }

    /** Sparks over every treasure around {@code centre}; returns how many there are. */
    public static int revealTreasure(ServerLevel level, BlockPos centre) {
        int found = 0;
        for (BlockPos pos : BlockPos.betweenClosed(centre.offset(-RADIUS, -RADIUS, -RADIUS), centre.offset(RADIUS, RADIUS, RADIUS))) {
            BlockState state = level.getBlockState(pos);
            if (state.isAir() || !isTreasure(level, pos, state)) {
                continue;
            }
            if (found++ < MAX_SHOWN) {
                level.sendParticles(ParticleTypes.WAX_ON, pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5, 8, 0.4, 0.4, 0.4, 0.0);
            }
        }
        return found;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
