package com.mythsofworlds.mythology.greek.item;

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
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/** Right-click: every creature in a cone in front of the player is turned to stone (frozen) for a few seconds. */
public class MedusaHeadItem extends Item {
    public static final double RANGE = 12.0;
    public static final int PETRIFY_TICKS = 100;
    public static final int COOLDOWN_TICKS = 200;

    public MedusaHeadItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel server) {
            Vec3 look = player.getViewVector(1.0F).normalize();
            Vec3 eye = player.getEyePosition();
            List<LivingEntity> targets = level.getEntitiesOfClass(LivingEntity.class, player.getBoundingBox().inflate(RANGE),
                    e -> e != player && e.isAlive() && player.hasLineOfSight(e)
                            && e.position().subtract(eye).normalize().dot(look) > 0.75);
            for (LivingEntity target : targets) {
                petrify(target);
                server.sendParticles(ParticleTypes.ASH, target.getX(), target.getY(0.5), target.getZ(), 20,
                        0.3, 0.6, 0.3, 0.0);
            }
            level.playSound(null, player.blockPosition(), SoundEvents.STONE_PLACE, SoundSource.PLAYERS, 1.0F, 0.6F);
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
            stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    /** "Stone" = cannot move, cannot hit, takes less damage. */
    public static void petrify(LivingEntity target) {
        target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, PETRIFY_TICKS, 9));
        target.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, PETRIFY_TICKS, 9));
        target.addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, PETRIFY_TICKS, 1));
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
