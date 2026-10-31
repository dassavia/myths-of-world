package com.mythsofworlds.mythology.norse.item;

import com.mythsofworlds.core.family.WarriorMaiden;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.ItemAttributeModifiers;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * Gungnir, Odin's spear forged by the sons of Ivaldi: it never misses its mark. A spear in the hand; cast (right-click),
 * it strikes the creature nearest to where you look, up to {@value #RANGE} blocks away, for {@value #DAMAGE} damage, and
 * is back in your hand at once. It never strikes your family or your tamed beasts.
 */
public class GungnirItem extends Item {
    public static final double RANGE = 48.0;
    public static final float DAMAGE = 14.0F;
    /** How far from the line of sight (degrees) a creature may stand and still be the mark. */
    public static final double CONE = 20.0;
    public static final int COOLDOWN = 30;

    public GungnirItem(Properties properties) {
        super(properties);
    }

    /** A spear in melee: 9 damage, a little slower than a sword. */
    public static ItemAttributeModifiers attributes() {
        return ItemAttributeModifiers.builder()
                .add(Attributes.ATTACK_DAMAGE, new AttributeModifier(BASE_ATTACK_DAMAGE_ID, 8.0, AttributeModifier.Operation.ADD_VALUE),
                        EquipmentSlotGroup.MAINHAND)
                .add(Attributes.ATTACK_SPEED, new AttributeModifier(BASE_ATTACK_SPEED_ID, -2.8, AttributeModifier.Operation.ADD_VALUE),
                        EquipmentSlotGroup.MAINHAND)
                .build();
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!(level instanceof ServerLevel server)) {
            return InteractionResultHolder.success(stack);
        }
        LivingEntity mark = findMark(server, player);
        if (mark == null) {
            player.displayClientMessage(Component.translatable("item.mythsofworlds.gungnir.no_mark"), true);
            return InteractionResultHolder.fail(stack);
        }
        strike(server, player, mark);
        player.getCooldowns().addCooldown(this, COOLDOWN);
        stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
        return InteractionResultHolder.success(stack);
    }

    /** The creature nearest to the player's line of sight, in range and in view; null if there is none. */
    @Nullable
    public static LivingEntity findMark(ServerLevel level, Player player) {
        Vec3 eye = player.getEyePosition();
        Vec3 look = player.getLookAngle();
        double cos = Math.cos(Math.toRadians(CONE));
        LivingEntity best = null;
        double bestDot = cos;
        for (LivingEntity entity : level.getEntitiesOfClass(LivingEntity.class, player.getBoundingBox().inflate(RANGE),
                e -> e != player && e.isAlive() && !e.isSpectator() && !isFriend(player, e))) {
            Vec3 to = entity.getBoundingBox().getCenter().subtract(eye);
            double dist = to.length();
            if (dist > RANGE || dist < 1.0E-3) {
                continue;
            }
            double dot = to.scale(1.0 / dist).dot(look);
            if (dot > bestDot && player.hasLineOfSight(entity)) {
                best = entity;
                bestDot = dot;
            }
        }
        return best;
    }

    private static boolean isFriend(Player player, LivingEntity entity) {
        return entity instanceof Player
                || entity instanceof WarriorMaiden maiden && maiden.isFamily(player)
                || entity instanceof TamableAnimal pet && pet.isOwnedBy(player);
    }

    /** The spear flies, strikes and returns. */
    public static void strike(ServerLevel level, Player player, LivingEntity mark) {
        Vec3 from = player.getEyePosition();
        Vec3 to = mark.getBoundingBox().getCenter();
        for (int i = 0; i <= 24; i++) {
            Vec3 p = from.lerp(to, i / 24.0);
            level.sendParticles(ParticleTypes.ELECTRIC_SPARK, p.x, p.y, p.z, 1, 0.0, 0.0, 0.0, 0.0);
        }
        mark.hurt(level.damageSources().playerAttack(player), DAMAGE);
        Vec3 push = to.subtract(from).normalize();
        mark.knockback(0.8, -push.x, -push.z);
        level.playSound(null, player.blockPosition(), SoundEvents.TRIDENT_THROW.value(), SoundSource.PLAYERS, 1.0F, 0.8F);
        level.playSound(null, mark.blockPosition(), SoundEvents.TRIDENT_HIT, SoundSource.PLAYERS, 1.0F, 0.8F);
        level.playSound(null, player.blockPosition(), SoundEvents.TRIDENT_RETURN, SoundSource.PLAYERS, 0.8F, 1.0F);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
