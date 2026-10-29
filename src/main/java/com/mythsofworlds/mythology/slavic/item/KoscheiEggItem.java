package com.mythsofworlds.mythology.slavic.item;

import com.mythsofworlds.mythology.slavic.SlavicContent;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ItemParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/** The egg from the chest on the old oak. Break it (right-click) and the needle with the death of Koschei falls out. */
public class KoscheiEggItem extends Item {
    public KoscheiEggItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack egg = player.getItemInHand(hand);
        if (level instanceof ServerLevel server) {
            server.playSound(null, player.blockPosition(), SoundEvents.TURTLE_EGG_BREAK, SoundSource.PLAYERS, 1.0F, 0.8F);
            server.sendParticles(new ItemParticleOption(ParticleTypes.ITEM, egg), player.getX(), player.getEyeY() - 0.3,
                    player.getZ(), 12, 0.2, 0.2, 0.2, 0.05);
            player.displayClientMessage(Component.translatable(getDescriptionId() + ".broken").withStyle(ChatFormatting.DARK_PURPLE), false);
        }
        ItemStack needle = new ItemStack(SlavicContent.KOSCHEI_NEEDLE.get());
        if (egg.getCount() == 1 && !player.getAbilities().instabuild) {
            return InteractionResultHolder.sidedSuccess(needle, level.isClientSide);
        }
        if (!player.getAbilities().instabuild) {
            egg.shrink(1);
        }
        if (!player.getInventory().add(needle)) {
            player.drop(needle, false);
        }
        return InteractionResultHolder.sidedSuccess(egg, level.isClientSide);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
