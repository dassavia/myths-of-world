package com.mythsofworlds.mythology.relic;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.Mythology;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.item.GirdleItem;
import com.mythsofworlds.mythology.norse.NorseContent;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import org.jetbrains.annotations.Nullable;

/**
 * Set bonuses of the armour of the myths. Greek pieces: orichalcum armour, the armour of the Nemean lion, the girdle of
 * Hippolyta, the talaria and the Titan's breastplate. Norse pieces: dark iron armour and the helmet of Heimdall.
 * <ul>
 *   <li>Union of the pantheons (both mythologies worn): 2 pieces give Haste, 3 also Fire Resistance, 4 also
 *       Regeneration; two of each also give Resistance.</li>
 *   <li>Blessing of Olympus (4 Greek pieces): Speed and Jump Boost.</li>
 *   <li>Fury of the berserker (4 Norse pieces): Strength and Resistance.</li>
 *   <li>Hide of the Nemean lion (the whole Nemean set, Greek too): Strength, and no arrow or other projectile can
 *       wound you.</li>
 * </ul>
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class ArmourSets {
    private static final EquipmentSlot[] ARMOUR = {EquipmentSlot.HEAD, EquipmentSlot.CHEST, EquipmentSlot.LEGS, EquipmentSlot.FEET};

    private ArmourSets() {
    }

    /** Which mythology a worn piece belongs to, or null for ordinary armour. */
    @Nullable
    public static Mythology mythologyOf(ItemStack stack) {
        if (stack.getItem() instanceof RelicArmorItem relic) {
            return relic.mythology();
        }
        if (stack.getItem() instanceof GirdleItem) {
            return Mythology.GREEK;
        }
        if (stack.getItem() instanceof ArmorItem armour) {
            if (armour.getMaterial().value() == GreekContent.ORICHALCUM.material.value()) {
                return Mythology.GREEK;
            }
            if (armour.getMaterial().value() == NorseContent.DARK_IRON.material.value()) {
                return Mythology.NORSE;
            }
        }
        return null;
    }

    /** Pieces worn of each mythology: {Greek, Norse}. */
    public static int[] count(Player player) {
        int[] counts = new int[2];
        for (EquipmentSlot slot : ARMOUR) {
            Mythology mythology = mythologyOf(player.getItemBySlot(slot));
            if (mythology == Mythology.GREEK) {
                counts[0]++;
            } else if (mythology == Mythology.NORSE) {
                counts[1]++;
            }
        }
        return counts;
    }

    /** Whether {@code entity} wears the whole armour of the Nemean lion. */
    public static boolean wearsNemean(LivingEntity entity) {
        for (EquipmentSlot slot : ARMOUR) {
            if (!(entity.getItemBySlot(slot).getItem() instanceof ArmorItem armour)
                    || armour.getMaterial().value() != GreekContent.NEMEAN_MATERIAL.value()) {
                return false;
            }
        }
        return true;
    }

    /** Arrows, tridents and fireballs glance off the hide of the Nemean lion. */
    @SubscribeEvent
    public static void onIncomingDamage(LivingIncomingDamageEvent event) {
        if (event.getSource().is(DamageTypeTags.IS_PROJECTILE) && wearsNemean(event.getEntity())) {
            event.setCanceled(true);
        }
    }

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        Player player = event.getEntity();
        if (player.level().isClientSide) {
            return;
        }
        for (EquipmentSlot slot : ARMOUR) {
            if (player.getItemBySlot(slot).getItem() instanceof RelicArmorItem relic) {
                relic.wornTick(player);
            }
        }
        if (player.tickCount % 20 == 0) {
            apply(player);
        }
    }

    public static void apply(Player player) {
        int[] counts = count(player);
        int greek = counts[0];
        int norse = counts[1];
        int total = greek + norse;
        if (greek > 0 && norse > 0) {
            RelicArmorItem.keep(player, MobEffects.DIG_SPEED, 0);
            if (total >= 3) {
                RelicArmorItem.keep(player, MobEffects.FIRE_RESISTANCE, 0);
            }
            if (total == 4) {
                RelicArmorItem.keep(player, MobEffects.REGENERATION, 0);
            }
            if (greek == 2 && norse == 2) {
                RelicArmorItem.keep(player, MobEffects.DAMAGE_RESISTANCE, 0);
            }
        } else if (greek == 4) {
            RelicArmorItem.keep(player, MobEffects.MOVEMENT_SPEED, 0);
            RelicArmorItem.keep(player, MobEffects.JUMP, 0);
        } else if (norse == 4) {
            RelicArmorItem.keep(player, MobEffects.DAMAGE_BOOST, 0);
            RelicArmorItem.keep(player, MobEffects.DAMAGE_RESISTANCE, 0);
        }
        if (wearsNemean(player)) {
            RelicArmorItem.keep(player, MobEffects.DAMAGE_BOOST, 0);
        }
    }
}
