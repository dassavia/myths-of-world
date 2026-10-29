package com.mythsofworlds.mythology.greek.item;

import com.mythsofworlds.mythology.greek.GreekContent;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.network.chat.Component;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/**
 * The war girdle Ares gave Hippolyta, queen of the Amazons, which Heracles was sent to bring back. Worn in the legs
 * slot it gives Strength II, Resistance II, Speed and Regeneration, and others see a golden belt on the wearer
 * (textures/models/armor/girdle_of_hippolyta_layer_2.png). Hippolyta hands it over when she is defeated.
 */
public class GirdleItem extends ArmorItem {
    public GirdleItem(Holder<ArmorMaterial> material, Properties properties) {
        super(material, Type.LEGGINGS, properties);
    }

    public static boolean isWorn(Player player) {
        return player.getItemBySlot(EquipmentSlot.LEGS).is(GreekContent.GIRDLE_OF_HIPPOLYTA.get());
    }

    /** Called every tick on the server for a player wearing the girdle (see GreekEvents). */
    public static void wornTick(Player player) {
        if (player.tickCount % 20 == 0) {
            player.addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, 60, 1, true, false, true));
            player.addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 60, 1, true, false, true));
            player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 60, 0, true, false, true));
            player.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 60, 0, true, false, true));
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.mythsofworlds.girdle_of_hippolyta.desc").withStyle(ChatFormatting.GRAY));
    }
}
