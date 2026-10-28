package com.mythsofworlds.mythology.greek.item;

import com.mythsofworlds.mythology.greek.GreekEntities;
import com.mythsofworlds.mythology.greek.entity.HydraHatchling;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;

/** Right-click the ground: a little hydra hatches and becomes the pet of whoever hatched it. */
public class HydraEggItem extends Item {
    public HydraEggItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        if (!(context.getLevel() instanceof ServerLevel level)) {
            return InteractionResult.SUCCESS;
        }
        Player player = context.getPlayer();
        BlockPos pos = context.getClickedPos().relative(context.getClickedFace());
        HydraHatchling hatchling = GreekEntities.HYDRA_HATCHLING.get().create(level);
        if (hatchling == null) {
            return InteractionResult.FAIL;
        }
        hatchling.moveTo(pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5, player != null ? player.getYRot() + 180.0F : 0.0F, 0.0F);
        if (player != null) {
            hatchling.tame(player);
        }
        level.addFreshEntity(hatchling);
        level.playSound(null, pos, SoundEvents.TURTLE_EGG_HATCH, SoundSource.NEUTRAL, 1.0F, 0.8F);
        level.sendParticles(ParticleTypes.HAPPY_VILLAGER, pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5, 12, 0.4, 0.4, 0.4, 0.0);
        if (player == null || !player.getAbilities().instabuild) {
            context.getItemInHand().shrink(1);
        }
        return InteractionResult.CONSUME;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
