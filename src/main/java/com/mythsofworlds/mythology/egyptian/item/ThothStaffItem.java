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
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * The staff of Thoth, set with his tablet of the words of power: right-click speaks a word at the creature you look
 * at (up to {@link #RANGE} blocks away). It takes {@link #DAMAGE} magic damage and is lifted into the air by the
 * moonlight. Once every {@link #COOLDOWN_TICKS} ticks.
 */
public class ThothStaffItem extends Item {
    public static final double RANGE = 24.0;
    public static final float DAMAGE = 7.0F;
    public static final int COOLDOWN_TICKS = 30;

    public ThothStaffItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel server) {
            LivingEntity target = aim(player);
            Vec3 from = player.getEyePosition();
            Vec3 to = target != null ? target.position().add(0.0, target.getBbHeight() * 0.5, 0.0)
                    : from.add(player.getViewVector(1.0F).scale(RANGE));
            for (int i = 1; i <= 16; i++) {
                Vec3 at = from.lerp(to, i / 16.0);
                server.sendParticles(ParticleTypes.ENCHANT, at.x, at.y, at.z, 3, 0.1, 0.1, 0.1, 0.2);
            }
            if (target != null) {
                speak(player, target);
                stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
            }
            server.playSound(null, player.blockPosition(), SoundEvents.EVOKER_CAST_SPELL, SoundSource.PLAYERS, 1.0F, 1.3F);
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    /** The living creature in {@code player}'s line of sight, if any. */
    @Nullable
    public static LivingEntity aim(Player player) {
        Vec3 eye = player.getEyePosition();
        Vec3 end = eye.add(player.getViewVector(1.0F).scale(RANGE));
        HitResult block = player.level().clip(new ClipContext(eye, end, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, player));
        Vec3 reach = block.getType() == HitResult.Type.MISS ? end : block.getLocation();
        EntityHitResult entity = ProjectileUtil.getEntityHitResult(player.level(), player, eye, reach,
                new AABB(eye, reach).inflate(1.0), e -> e instanceof LivingEntity && e.isAlive() && !e.isSpectator());
        return entity != null && entity.getEntity() instanceof LivingEntity living ? living : null;
    }

    /** The word of power falls on {@code target}. */
    public static void speak(Player player, LivingEntity target) {
        target.hurt(player.damageSources().indirectMagic(player, player), DAMAGE);
        target.addEffect(new MobEffectInstance(MobEffects.LEVITATION, 30, 0), player);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
