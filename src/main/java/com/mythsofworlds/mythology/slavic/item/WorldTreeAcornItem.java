package com.mythsofworlds.mythology.slavic.item;

import com.mythsofworlds.mythology.slavic.block.WorldTree;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;

/**
 * Acorn of the World Tree. Plant it on the top of a block of earth (grass, dirt, podzol, moss...) and the great oak
 * grows at once, its hollow towards you: the way to Nav (see {@link WorldTree}).
 */
public class WorldTreeAcornItem extends Item {
    public WorldTreeAcornItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos clicked = context.getClickedPos();
        if (context.getClickedFace() != Direction.UP || !level.getBlockState(clicked).is(BlockTags.DIRT)) {
            return InteractionResult.PASS;
        }
        Direction facing = context.getHorizontalDirection().getOpposite();
        BlockPos centre = clicked.above().relative(facing.getOpposite());
        Player player = context.getPlayer();
        if (!WorldTree.canGrow(level, centre, facing)) {
            if (!level.isClientSide && player != null) {
                player.displayClientMessage(Component.translatable(getDescriptionId() + ".no_room").withStyle(ChatFormatting.RED), true);
            }
            return InteractionResult.FAIL;
        }
        if (level instanceof ServerLevel server) {
            BlockPos hollow = WorldTree.grow(server, centre, facing, server.getRandom());
            server.playSound(null, hollow, SoundEvents.ROOTED_DIRT_PLACE, SoundSource.BLOCKS, 2.0F, 0.5F);
            server.playSound(null, hollow, SoundEvents.PORTAL_TRIGGER, SoundSource.BLOCKS, 0.6F, 1.4F);
            server.sendParticles(ParticleTypes.HAPPY_VILLAGER, hollow.getX() + 0.5, hollow.getY() + 1.0, hollow.getZ() + 0.5,
                    40, 2.0, 3.0, 2.0, 0.0);
            if (player != null) {
                player.displayClientMessage(Component.translatable(getDescriptionId() + ".grown").withStyle(ChatFormatting.GREEN), true);
                if (!player.getAbilities().instabuild) {
                    context.getItemInHand().shrink(1);
                }
            }
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
