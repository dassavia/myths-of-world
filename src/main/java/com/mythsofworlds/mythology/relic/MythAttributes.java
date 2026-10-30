package com.mythsofworlds.mythology.relic;

import com.mythsofworlds.MythsOfWorlds;
import java.util.List;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.common.PercentageAttribute;
import net.neoforged.neoforge.event.entity.EntityAttributeModificationEvent;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

/**
 * Powers of the armour and weapons of the myths that vanilla Minecraft has no attribute for. They are real
 * attributes of the player, so the tooltip of every piece lists them ("+5% Reflection") and they add up over the
 * pieces worn. What they do is in {@link MythPowers}.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD)
public final class MythAttributes {
    public static final DeferredRegister<Attribute> ATTRIBUTES = DeferredRegister.create(Registries.ATTRIBUTE, MythsOfWorlds.MODID);

    /** Share of the melee damage you take that strikes back at the attacker. */
    public static final DeferredHolder<Attribute, Attribute> REFLECTION = percent("reflection", 0.9);
    /** Share of the melee damage you deal that heals you. */
    public static final DeferredHolder<Attribute, Attribute> LIFESTEAL = percent("lifesteal", 0.5);
    /** Extra damage against the creatures and gods of the myths. */
    public static final DeferredHolder<Attribute, Attribute> MONSTER_SLAYING = percent("monster_slaying", 2.0);
    /** Less damage from the creatures and gods of the myths. */
    public static final DeferredHolder<Attribute, Attribute> DIVINE_WARD = percent("divine_ward", 0.75);
    /** Chance that a blow or an arrow misses you altogether. */
    public static final DeferredHolder<Attribute, Attribute> EVASION = percent("evasion", 0.6);
    /** Extra damage while you are at half health or less. */
    public static final DeferredHolder<Attribute, Attribute> FURY = percent("fury", 2.0);

    public static final List<DeferredHolder<Attribute, Attribute>> ALL =
            List.of(REFLECTION, LIFESTEAL, MONSTER_SLAYING, DIVINE_WARD, EVASION, FURY);

    private MythAttributes() {
    }

    private static DeferredHolder<Attribute, Attribute> percent(String name, double max) {
        return ATTRIBUTES.register(name, () -> new PercentageAttribute("attribute.name." + MythsOfWorlds.MODID + "." + name,
                0.0, 0.0, max).setSyncable(true));
    }

    @SubscribeEvent
    public static void addToPlayers(EntityAttributeModificationEvent event) {
        for (DeferredHolder<Attribute, Attribute> attribute : ALL) {
            event.add(EntityType.PLAYER, attribute);
        }
    }

    /** Whether the attribute exists on this entity at all (only players carry them). */
    public static double value(net.minecraft.world.entity.LivingEntity entity, DeferredHolder<Attribute, Attribute> attribute) {
        var instance = entity.getAttributes().hasAttribute(attribute) ? entity.getAttribute(attribute) : null;
        return instance == null ? 0.0 : instance.getValue();
    }

    static boolean fromTheMyths(net.minecraft.world.entity.Entity entity) {
        return BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType()).getNamespace().equals(MythsOfWorlds.MODID);
    }
}
