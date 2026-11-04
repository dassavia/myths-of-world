package com.mythsofworlds.mythology.egyptian.item;

import com.mythsofworlds.mythology.greek.entity.Amazon;
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
import net.minecraft.world.entity.OwnableEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * The sceptre of Isis, with the wing of the goddess whose magic brought Osiris back to life. Raise it (right-click)
 * and you, the other players, your pets and your family within {@link #RADIUS} blocks are healed by {@link #HEAL}
 * health and regenerate. Once every {@link #COOLDOWN_TICKS} ticks.
 */
public class IsisSceptreItem extends Item {
    public static final double RADIUS = 8.0;
    public static final float HEAL = 6.0F;
    public static final int COOLDOWN_TICKS = 400;

    public IsisSceptreItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel server) {
            bless(server, player);
            server.playSound(null, player.blockPosition(), SoundEvents.BEACON_ACTIVATE, SoundSource.PLAYERS, 1.0F, 1.4F);
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
            stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    /** Heals {@code player} and their friends around; returns how many were healed. */
    public static int bless(ServerLevel level, Player player) {
        int healed = 0;
        for (LivingEntity friend : level.getEntitiesOfClass(LivingEntity.class, player.getBoundingBox().inflate(RADIUS),
                e -> e.isAlive() && (e instanceof Player
                        || e instanceof OwnableEntity pet && player.getUUID().equals(pet.getOwnerUUID())
                        || e instanceof Amazon amazon && amazon.isFamily(player)))) {
            friend.heal(HEAL);
            friend.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 100, 1), player);
            level.sendParticles(ParticleTypes.HEART, friend.getX(), friend.getY(1.1), friend.getZ(), 3, 0.3, 0.2, 0.3, 0.1);
            healed++;
        }
        level.sendParticles(ParticleTypes.END_ROD, player.getX(), player.getY(0.5), player.getZ(), 40, RADIUS * 0.4, 0.6,
                RADIUS * 0.4, 0.02);
        return healed;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
