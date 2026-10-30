package com.mythsofworlds.mythology.relic;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.registry.MetalSet;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Supplier;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageTypes;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.Item;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.ItemAttributeModifierEvent;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.registries.DeferredHolder;

/**
 * Which piece of gear gives which power of {@link MythAttributes}, and what the powers do in a fight:
 * <ul>
 *   <li>Reflection: that share of a melee blow you take strikes the attacker back (orichalcum, Titan's breastplate).</li>
 *   <li>Lifesteal: that share of the melee damage you deal heals you (bulat, kladenets, girdle of Hippolyta).</li>
 *   <li>Monster slaying: more damage to the creatures and gods of the myths (dark iron, Heimdall, Mjolnir, Surtr).</li>
 *   <li>Divine ward: less damage from the creatures and gods of the myths (bulat, dark iron, cap of invisibility).</li>
 *   <li>Evasion: a chance that a blow or a shot misses altogether (talaria, seven-league boots, cap).</li>
 *   <li>Fury: more damage at half health or less (the Nemean set, the girdle).</li>
 * </ul>
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class MythPowers {
    private record Bonus(DeferredHolder<Attribute, Attribute> attribute, double amount) {
    }

    private static Map<Item, List<Bonus>> table;

    private MythPowers() {
    }

    private static synchronized Map<Item, List<Bonus>> table() {
        if (table == null) {
            Map<Item, List<Bonus>> map = new HashMap<>();
            metal(map, GreekContent.ORICHALCUM, new Bonus(MythAttributes.REFLECTION, 0.05));
            metal(map, SlavicContent.BULAT, new Bonus(MythAttributes.LIFESTEAL, 0.025), new Bonus(MythAttributes.DIVINE_WARD, 0.03));
            metal(map, NorseContent.DARK_IRON, new Bonus(MythAttributes.MONSTER_SLAYING, 0.05),
                    new Bonus(MythAttributes.DIVINE_WARD, 0.05));
            for (Supplier<? extends Item> piece : List.of(GreekContent.NEMEAN_HELMET, GreekContent.NEMEAN_CHESTPLATE,
                    GreekContent.NEMEAN_LEGGINGS, GreekContent.NEMEAN_BOOTS)) {
                put(map, piece, new Bonus(MythAttributes.FURY, 0.05));
            }
            put(map, GreekContent.TITAN_BREASTPLATE, new Bonus(MythAttributes.REFLECTION, 0.15));
            put(map, GreekContent.TALARIA, new Bonus(MythAttributes.EVASION, 0.10));
            put(map, GreekContent.GIRDLE_OF_HIPPOLYTA, new Bonus(MythAttributes.FURY, 0.15), new Bonus(MythAttributes.LIFESTEAL, 0.05));
            put(map, NorseContent.HEIMDALL_HELMET, new Bonus(MythAttributes.MONSTER_SLAYING, 0.10));
            put(map, SlavicContent.SKOROKHODY, new Bonus(MythAttributes.EVASION, 0.08));
            put(map, SlavicContent.SHAPKA_NEVIDIMKA, new Bonus(MythAttributes.EVASION, 0.05), new Bonus(MythAttributes.DIVINE_WARD, 0.08));
            put(map, SlavicContent.KLADENETS, new Bonus(MythAttributes.LIFESTEAL, 0.10));
            put(map, NorseContent.MJOLNIR, new Bonus(MythAttributes.MONSTER_SLAYING, 0.15));
            put(map, NorseContent.SURTR_SWORD, new Bonus(MythAttributes.MONSTER_SLAYING, 0.15));
            put(map, GreekContent.HARPE, new Bonus(MythAttributes.MONSTER_SLAYING, 0.10));
            table = map;
        }
        return table;
    }

    private static void metal(Map<Item, List<Bonus>> map, MetalSet metal, Bonus... bonuses) {
        for (Supplier<? extends Item> piece : List.of(metal.helmet, metal.chestplate, metal.leggings, metal.boots)) {
            put(map, piece, bonuses);
        }
    }

    private static void put(Map<Item, List<Bonus>> map, Supplier<? extends Item> item, Bonus... bonuses) {
        map.computeIfAbsent(item.get(), k -> new ArrayList<>()).addAll(List.of(bonuses));
    }

    /** The powers of {@code item} (fractions: 0.05 is 5%), for the Codex and the tests. */
    public static Map<Attribute, Double> of(Item item) {
        Map<Attribute, Double> result = new HashMap<>();
        for (Bonus bonus : table().getOrDefault(item, List.of())) {
            result.merge(bonus.attribute().value(), bonus.amount(), Double::sum);
        }
        return result;
    }

    @SubscribeEvent
    public static void addModifiers(ItemAttributeModifierEvent event) {
        List<Bonus> bonuses = table().get(event.getItemStack().getItem());
        if (bonuses == null) {
            return;
        }
        EquipmentSlotGroup group = event.getItemStack().getItem() instanceof ArmorItem armour
                ? EquipmentSlotGroup.bySlot(armour.getEquipmentSlot()) : EquipmentSlotGroup.MAINHAND;
        for (Bonus bonus : bonuses) {
            event.addModifier(bonus.attribute(), new AttributeModifier(MythsOfWorlds.id(bonus.attribute().getId().getPath()
                    + "." + group.getSerializedName()), bonus.amount(), AttributeModifier.Operation.ADD_VALUE), group);
        }
    }

    @SubscribeEvent
    public static void onIncomingDamage(LivingIncomingDamageEvent event) {
        LivingEntity victim = event.getEntity();
        if (victim.level().isClientSide) {
            return;
        }
        DamageSource source = event.getSource();
        boolean byCreature = source.getEntity() instanceof LivingEntity && !source.is(DamageTypeTags.BYPASSES_INVULNERABILITY);
        // Evasion: the blow or the arrow misses.
        double evasion = MythAttributes.value(victim, MythAttributes.EVASION);
        if (byCreature && evasion > 0 && victim.getRandom().nextDouble() < evasion) {
            event.setCanceled(true);
            victim.level().playSound(null, victim.blockPosition(), SoundEvents.PLAYER_ATTACK_NODAMAGE, SoundSource.PLAYERS, 1.0F, 1.4F);
            if (victim.level() instanceof ServerLevel level) {
                level.sendParticles(ParticleTypes.CLOUD, victim.getX(), victim.getY(0.5), victim.getZ(), 6, 0.3, 0.4, 0.3, 0.02);
            }
            return;
        }
        float amount = event.getAmount();
        if (source.getEntity() instanceof LivingEntity attacker) {
            if (MythAttributes.fromTheMyths(attacker)) {
                amount *= (float) (1.0 - MythAttributes.value(victim, MythAttributes.DIVINE_WARD));
            }
            if (MythAttributes.fromTheMyths(victim)) {
                amount *= (float) (1.0 + MythAttributes.value(attacker, MythAttributes.MONSTER_SLAYING));
            }
            if (attacker.getHealth() <= attacker.getMaxHealth() / 2) {
                amount *= (float) (1.0 + MythAttributes.value(attacker, MythAttributes.FURY));
            }
            // Reflection: only blows struck by hand, and never a reflection of a reflection.
            double reflection = MythAttributes.value(victim, MythAttributes.REFLECTION);
            if (reflection > 0 && source.getDirectEntity() == attacker && attacker != victim && !source.is(DamageTypes.THORNS)) {
                attacker.hurt(victim.damageSources().thorns(victim), (float) (amount * reflection));
            }
        }
        event.setAmount(amount);
    }

    /** Lifesteal heals by what the blow really took, after armour. */
    @SubscribeEvent
    public static void onDamageDealt(LivingDamageEvent.Post event) {
        DamageSource source = event.getSource();
        if (source.getEntity() instanceof LivingEntity attacker && source.getDirectEntity() == attacker
                && !attacker.level().isClientSide) {
            double lifesteal = MythAttributes.value(attacker, MythAttributes.LIFESTEAL);
            if (lifesteal > 0 && event.getNewDamage() > 0) {
                attacker.heal((float) (event.getNewDamage() * lifesteal));
            }
        }
    }
}
