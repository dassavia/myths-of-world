package com.mythsofworlds.mythology.slavic.item;

import com.mythsofworlds.core.Prophecy;
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
import net.minecraft.world.phys.Vec3;

/**
 * The yarn ball Baba Yaga gives the hero: "where it rolls, there you go." Drop it (right-click) and it rolls ahead
 * along the ground, leaving a golden trail toward the lair of the nearest foe you have not beaten.
 */
public class KlubokItem extends Item {
    public static final int TRAIL = 32;

    public KlubokItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!(player instanceof ServerPlayer serverPlayer)) {
            return InteractionResultHolder.success(stack);
        }
        var lair = Prophecy.nextLair(serverPlayer);
        if (lair.isEmpty()) {
            player.displayClientMessage(Component.translatable("item.mythsofworlds.klubok.still"), true);
            return InteractionResultHolder.fail(stack);
        }
        roll(serverPlayer.serverLevel(), player.position(), lair.get().pos());
        player.displayClientMessage(Component.translatable("item.mythsofworlds.klubok.rolls", lair.get().bossName())
                .withStyle(ChatFormatting.GOLD), true);
        level.playSound(null, player.blockPosition(), SoundEvents.WOOL_STEP, SoundSource.PLAYERS, 1.0F, 1.2F);
        player.getCooldowns().addCooldown(this, 100);
        stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
        return InteractionResultHolder.success(stack);
    }

    /** A trail of sparks along the ground from {@code from} toward {@code to}, {@value #TRAIL} blocks long. */
    public static void roll(ServerLevel level, Vec3 from, BlockPos to) {
        Vec3 dir = new Vec3(to.getX() + 0.5 - from.x, 0.0, to.getZ() + 0.5 - from.z);
        if (dir.lengthSqr() < 1.0E-4) {
            return;
        }
        dir = dir.normalize();
        for (int i = 1; i <= TRAIL; i++) {
            double x = from.x + dir.x * i;
            double z = from.z + dir.z * i;
            int y = level.getHeight(net.minecraft.world.level.levelgen.Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, (int) Math.floor(x),
                    (int) Math.floor(z));
            level.sendParticles(ParticleTypes.WAX_ON, x, y + 0.2, z, 3, 0.15, 0.05, 0.15, 0.0);
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
