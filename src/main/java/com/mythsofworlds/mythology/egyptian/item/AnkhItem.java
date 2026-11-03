package com.mythsofworlds.mythology.egyptian.item;

import com.mythsofworlds.mythology.egyptian.EgyptianSounds;
import com.mythsofworlds.mythology.egyptian.block.Pyramid;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;

/**
 * The ankh, the key of life. Touch a finished pyramid with it (any of its blocks or the doorway) and the gate of
 * shadow opens in the doorway: the way to the Duat (see {@link Pyramid}). Each opening costs one use.
 */
public class AnkhItem extends Item {
    public AnkhItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos clicked = context.getClickedPos();
        Player player = context.getPlayer();
        Pyramid.Gate gate = Pyramid.find(level, clicked);
        if (gate == null) {
            gate = Pyramid.find(level, clicked.relative(context.getClickedFace()));
        }
        if (gate == null) {
            if (!level.isClientSide && player != null) {
                player.displayClientMessage(Component.translatable(getDescriptionId() + ".no_pyramid").withStyle(ChatFormatting.RED), true);
            }
            return InteractionResult.FAIL;
        }
        if (level instanceof ServerLevel server) {
            Pyramid.open(server, gate);
            BlockPos door = gate.lower();
            server.playSound(null, door, EgyptianSounds.GATE_OPEN.get(), SoundSource.BLOCKS, 1.5F, 1.0F);
            server.playSound(null, door, SoundEvents.SAND_BREAK, SoundSource.BLOCKS, 1.0F, 0.6F);
            server.sendParticles(ParticleTypes.ENCHANT, door.getX() + 0.5, door.getY() + 1.0, door.getZ() + 0.5, 60, 1.5, 1.5, 1.5, 0.5);
            if (player != null) {
                player.displayClientMessage(Component.translatable(getDescriptionId() + ".opened").withStyle(ChatFormatting.GOLD), true);
                context.getItemInHand().hurtAndBreak(1, player, LivingEntity.getSlotForHand(context.getHand()));
            }
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
