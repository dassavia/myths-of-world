package com.mythsofworlds.mythology.relic;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.Mythology;
import java.util.EnumMap;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Supplier;
import net.minecraft.ChatFormatting;
import net.minecraft.core.Holder;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.crafting.Ingredient;
import net.neoforged.neoforge.registries.DeferredHolder;

import static com.mythsofworlds.registry.ModRegistries.ARMOR_MATERIALS;

/**
 * A piece of armour from the myths (the talaria of Hermes, the breastplate of a Titan, the helmet of Heimdall): it
 * belongs to one mythology, which counts towards the set bonuses of {@link ArmourSets}, and gives its own powers while
 * worn. The worn look is textures/models/armor/&lt;material&gt;_layer_1.png.
 */
public class RelicArmorItem extends ArmorItem {
    private final Mythology mythology;
    private final Consumer<Player> worn;

    public RelicArmorItem(Holder<ArmorMaterial> material, Type type, Mythology mythology, Consumer<Player> worn,
                          Properties properties) {
        super(material, type, properties);
        this.mythology = mythology;
        this.worn = worn;
    }

    public Mythology mythology() {
        return mythology;
    }

    /** Called every tick on the server while the piece is worn. */
    public void wornTick(Player player) {
        worn.accept(player);
    }

    /** An armour material with protection in one slot only, for a single relic. */
    public static DeferredHolder<ArmorMaterial, ArmorMaterial> material(String name, Type type, int defense, int enchantment,
                                                                        Holder<SoundEvent> sound, Supplier<Ingredient> repair,
                                                                        float toughness, float knockbackResistance) {
        return ARMOR_MATERIALS.register(name, () -> {
            EnumMap<Type, Integer> defenses = new EnumMap<>(Type.class);
            for (Type each : Type.values()) {
                defenses.put(each, each == type ? defense : 0);
            }
            return new ArmorMaterial(defenses, enchantment, sound, repair,
                    List.of(new ArmorMaterial.Layer(MythsOfWorlds.id(name))), toughness, knockbackResistance);
        });
    }

    /**
     * Keeps an effect going without flicker: renewed when it runs low, never over a stronger one. It fades within a
     * few seconds once the armour comes off.
     */
    public static void keep(Player player, Holder<MobEffect> effect, int amplifier) {
        MobEffectInstance current = player.getEffect(effect);
        if (current == null || current.getAmplifier() < amplifier
                || current.getAmplifier() == amplifier && !current.isInfiniteDuration() && current.getDuration() < 220) {
            player.addEffect(new MobEffectInstance(effect, 260, amplifier, true, false, true));
        }
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
        tooltip.add(Component.translatable("item.mythsofworlds.relic." + mythology.name().toLowerCase()).withStyle(ChatFormatting.GOLD));
    }
}
