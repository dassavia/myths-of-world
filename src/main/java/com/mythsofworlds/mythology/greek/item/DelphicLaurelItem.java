package com.mythsofworlds.mythology.greek.item;

import com.mythsofworlds.core.Prophecy;
import java.util.List;
import java.util.Optional;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * A sprig of Apollo's laurel from Delphi, which the Pythia chewed before she prophesied. Burn it (right-click) in a
 * world of the myths and the oracle names the nearest monster you have not yet beaten, how far it waits and which way.
 * The leaf is spent.
 */
public class DelphicLaurelItem extends Item {
    public static final int COOLDOWN = 200;

    public DelphicLaurelItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level.isClientSide || !(player instanceof ServerPlayer serverPlayer)) {
            return InteractionResultHolder.sidedSuccess(stack, level.isClientSide);
        }
        player.getCooldowns().addCooldown(this, COOLDOWN);
        Optional<Component> prophecy = prophesy(serverPlayer);
        if (prophecy.isEmpty()) {
            return InteractionResultHolder.fail(stack);
        }
        player.displayClientMessage(prophecy.get(), false);
        serverPlayer.serverLevel().sendParticles(ParticleTypes.SMOKE, player.getX(), player.getY(1.2), player.getZ(), 20, 0.3, 0.3, 0.3, 0.02);
        level.playSound(null, player.blockPosition(), SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.PLAYERS, 1.0F, 0.6F);
        stack.consume(1, player);
        return InteractionResultHolder.success(stack);
    }

    /** What the Pythia says, or empty (after telling the player why) if there is nothing to foretell here. */
    public static Optional<Component> prophesy(ServerPlayer player) {
        var lair = Prophecy.nextLair(player);
        if (lair.isEmpty()) {
            player.displayClientMessage(Component.translatable("item.mythsofworlds.delphic_laurel.silent"), true);
            return Optional.empty();
        }
        var pos = player.blockPosition();
        return Optional.of(Component.translatable("item.mythsofworlds.delphic_laurel.prophecy", lair.get().bossName(),
                        Prophecy.distance(pos, lair.get().pos()),
                        Component.translatable("direction.mythsofworlds." + Prophecy.direction(pos, lair.get().pos())))
                .withStyle(ChatFormatting.LIGHT_PURPLE));
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
