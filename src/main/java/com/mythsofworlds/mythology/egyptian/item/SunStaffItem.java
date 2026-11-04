package com.mythsofworlds.mythology.egyptian.item;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.SmallFireball;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * The staff of Ra, crowned with the sun disc taken from the sun god: raise it (right-click) and it hurls
 * {@link #FIREBALLS} fireballs of the sun fanned out where you look. Once every {@link #COOLDOWN_TICKS} ticks.
 */
public class SunStaffItem extends Item {
    public static final int FIREBALLS = 3;
    public static final int COOLDOWN_TICKS = 40;

    public SunStaffItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel server) {
            shoot(server, player);
            server.playSound(null, player.blockPosition(), SoundEvents.BLAZE_SHOOT, SoundSource.PLAYERS, 1.0F, 0.8F);
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
            stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    /** Hurls the fireballs from {@code player}'s eyes; returns how many flew. */
    public static int shoot(ServerLevel level, Player player) {
        Vec3 look = player.getViewVector(1.0F);
        Vec3 side = new Vec3(-look.z, 0.0, look.x).normalize().scale(0.12);
        Vec3 start = player.getEyePosition().add(look.scale(1.0));
        for (int i = 0; i < FIREBALLS; i++) {
            Vec3 direction = look.add(side.scale(i - (FIREBALLS - 1) / 2.0)).normalize();
            SmallFireball fireball = new SmallFireball(level, player, direction);
            fireball.setPos(start);
            level.addFreshEntity(fireball);
        }
        return FIREBALLS;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
