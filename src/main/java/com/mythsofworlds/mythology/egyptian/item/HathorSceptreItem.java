package com.mythsofworlds.mythology.egyptian.item;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * The sceptre of Hathor, a sistrum on a staff with the horn of the goddess of joy and music. Shake it (right-click)
 * and its song calms the monsters within {@link #RADIUS} blocks: they forget whom they were hunting and dance slowly
 * on the spot. Once every {@link #COOLDOWN_TICKS} ticks.
 */
public class HathorSceptreItem extends Item {
    public static final double RADIUS = 10.0;
    public static final int COOLDOWN_TICKS = 300;

    public HathorSceptreItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel server) {
            int calmed = song(server, player);
            server.playSound(null, player.blockPosition(), SoundEvents.NOTE_BLOCK_CHIME.value(), SoundSource.PLAYERS, 1.5F, 1.2F);
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
            if (calmed > 0) {
                stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
            }
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    /** Calms the monsters around {@code player}; returns how many heard the song. */
    public static int song(ServerLevel level, Player player) {
        int calmed = 0;
        for (Mob mob : level.getEntitiesOfClass(Mob.class, player.getBoundingBox().inflate(RADIUS),
                m -> m.isAlive() && m instanceof Enemy)) {
            mob.setTarget(null);
            mob.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 120, 3), player);
            mob.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 120, 1), player);
            level.sendParticles(ParticleTypes.NOTE, mob.getX(), mob.getY(1.1), mob.getZ(), 2, 0.3, 0.2, 0.3, 1.0);
            calmed++;
        }
        return calmed;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
