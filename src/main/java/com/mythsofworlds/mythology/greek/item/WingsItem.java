package com.mythsofworlds.mythology.greek.item;

import com.mythsofworlds.mythology.greek.GreekContent;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Equipable;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Wings of Daedalus and Icarus, harpy feathers held together with wax. Worn in the chest slot. Weaker than an
 * elytra: they cannot fly, but give a very high jump and a gentle glide down instead of a fall. Like Icarus, do not
 * fly too close to the sun: above y = {@value #SUN_HEIGHT} in daylight the wax melts quickly. Mend them with honeycomb.
 */
public class WingsItem extends Item implements Equipable {
    public static final int SUN_HEIGHT = 200;

    public WingsItem(Properties properties) {
        super(properties);
    }

    @Override
    public EquipmentSlot getEquipmentSlot() {
        return EquipmentSlot.CHEST;
    }

    @Override
    public Holder<SoundEvent> getEquipSound() {
        return SoundEvents.ARMOR_EQUIP_ELYTRA;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        return swapWithEquipmentSlot(this, level, player, hand);
    }

    public static boolean isWorking(ItemStack stack) {
        return stack.is(GreekContent.WINGS_OF_DAEDALUS.get()) && stack.getDamageValue() < stack.getMaxDamage() - 1;
    }

    /** Called every tick on the server for a player wearing the wings (see GreekEvents). */
    public static void wornTick(Player player, ItemStack stack) {
        Level level = player.level();
        if (!isWorking(stack)) {
            return;
        }
        if (player.tickCount % 10 == 0) {
            player.addEffect(new MobEffectInstance(MobEffects.JUMP, 30, 2, true, false, true));
        }
        boolean gliding = !player.onGround() && !player.isInWater() && !player.isShiftKeyDown()
                && player.getDeltaMovement().y < -0.15 && !player.getAbilities().flying;
        if (gliding) {
            player.addEffect(new MobEffectInstance(MobEffects.SLOW_FALLING, 10, 0, true, false, true));
            // A little lift forward, so the fall becomes a glide.
            Vec3 look = player.getLookAngle();
            player.push(look.x * 0.02, 0.0, look.z * 0.02);
            player.hurtMarked = true;
            if (player.tickCount % 40 == 0) {
                stack.hurtAndBreak(1, player, EquipmentSlot.CHEST);
            }
        }
        if (player.getY() > SUN_HEIGHT && level.isDay() && level.canSeeSky(player.blockPosition()) && player.tickCount % 10 == 0) {
            stack.hurtAndBreak(4, player, EquipmentSlot.CHEST);
            if (player.tickCount % 60 == 0) {
                player.displayClientMessage(Component.translatable("item.mythsofworlds.wings_of_daedalus.melting")
                        .withStyle(ChatFormatting.GOLD), true);
            }
        }
    }

    @Override
    public boolean isValidRepairItem(ItemStack stack, ItemStack repairCandidate) {
        return repairCandidate.is(Items.HONEYCOMB);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.mythsofworlds.wings_of_daedalus.desc").withStyle(ChatFormatting.GRAY));
    }
}
