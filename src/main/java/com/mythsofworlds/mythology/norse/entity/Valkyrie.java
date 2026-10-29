package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.mythology.greek.entity.Amazon;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.norse.NorseEntities;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * Valkyrie, shield-maiden of Odin, in the halls of the valkyries in Jotunheim. In the sagas valkyries wed heroes:
 * Brynhild and Sigurd, Svanhvit and Volund's brother, Sigrun and Helgi. Courted and married like an amazon (see
 * {@link Amazon}), with the wedding ring: she likes gold and jewels, weapons, trophies of the monsters of the North
 * and a good feast, flowers leave her cold. Give your wife mead and a daughter is born, once a day; she grows up a
 * valkyrie loyal to your family.
 */
public class Valkyrie extends Amazon {
    public static final int LOOKS = 8;

    private static final String[] NAMES = {"Brynhild", "Sigrun", "Svanhvit", "Hildr", "Gondul", "Skogul", "Hrist",
            "Mist", "Skuld", "Kara", "Eir", "Geirskogul", "Randgrid", "Reginleif", "Sigrdrifa", "Thrud", "Alvitr",
            "Olrun", "Gunnr", "Herfjotur", "Goll", "Geironul", "Hlokk", "Herja", "Hrund", "Sanngrid", "Skeggjold",
            "Svipul", "Thogn", "Hervor", "Svava", "Brynja", "Astrid", "Ingrid", "Sigrid", "Freydis", "Ragnhild",
            "Gunnhild", "Solveig", "Thora", "Ylva", "Alfhild", "Dagny", "Eydis", "Halla", "Runa", "Sigyn", "Tove"};

    public Valkyrie(EntityType<? extends AgeableMob> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Amazon.createAttributes()
                .add(Attributes.MAX_HEALTH, 34.0)
                .add(Attributes.ATTACK_DAMAGE, 6.0)
                .add(Attributes.ARMOR, 6.0);
    }

    @Override
    protected String messages() {
        return "entity.mythsofworlds.valkyrie.";
    }

    @Override
    public String textureName() {
        return "valkyrie_" + Math.floorMod(getVariant(), LOOKS);
    }

    @Override
    protected String randomName() {
        return NAMES[random.nextInt(NAMES.length)];
    }

    @Override
    protected int randomVariant() {
        return random.nextInt(LOOKS);
    }

    @Override
    protected int childVariant() {
        return random.nextBoolean() ? getVariant() : randomVariant();
    }

    @Nullable
    @Override
    protected Amazon newChild() {
        return NorseEntities.VALKYRIE.get().create(level());
    }

    @Override
    protected ItemStack childGift() {
        return new ItemStack(NorseContent.MEAD.get());
    }

    @Override
    protected void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(random.nextInt(10) < 6 ? Items.IRON_SWORD : Items.IRON_AXE));
        if (random.nextInt(10) < 7) {
            setItemSlot(EquipmentSlot.OFFHAND, new ItemStack(Items.SHIELD));
        }
        setDropChance(EquipmentSlot.MAINHAND, 0.0F);
        setDropChance(EquipmentSlot.OFFHAND, 0.0F);
    }

    /** Gifts for a valkyrie: 0 gold and jewels, 1 weapons and shields, 2 trophies of the North, 3 a feast. */
    @Nullable
    @Override
    protected Gift giftFor(ItemStack stack) {
        if (stack.is(Items.GOLD_BLOCK)) {
            return new Gift(0, 40);
        }
        if (stack.is(Items.DIAMOND)) {
            return new Gift(0, 20);
        }
        if (stack.is(Items.GOLD_INGOT) || stack.is(NorseContent.DARK_IRON.ingot.get())) {
            return new Gift(0, 10);
        }
        if (stack.is(Items.EMERALD) || stack.is(Items.AMETHYST_SHARD)) {
            return new Gift(0, 6);
        }
        if (stack.is(Items.GOLD_NUGGET)) {
            return new Gift(0, 2);
        }
        if (stack.is(NorseContent.DARK_IRON.sword.get()) || stack.is(NorseContent.DARK_IRON.axe.get())) {
            return new Gift(1, 25);
        }
        if (stack.is(ItemTags.SWORDS) || stack.is(ItemTags.AXES) || stack.is(Items.BOW) || stack.is(Items.CROSSBOW)
                || stack.is(Items.TRIDENT) || stack.is(Items.SHIELD)) {
            return new Gift(1, 12);
        }
        if (stack.is(NorseContent.FENRIR_FANG.get()) || stack.is(NorseContent.GARM_FANG.get())
                || stack.is(NorseContent.BARROW_CROWN.get())) {
            return new Gift(2, 25);
        }
        if (stack.is(NorseContent.TROLL_TUSK.get()) || stack.is(NorseContent.FROST_HEART.get())
                || stack.is(NorseContent.MUSPEL_EMBER.get())) {
            return new Gift(2, 12);
        }
        if (stack.is(NorseContent.RAVEN_FEATHER.get())) {
            return new Gift(2, 4);
        }
        if (stack.is(NorseContent.IDUNN_APPLE.get())) {
            return new Gift(3, 25);
        }
        if (stack.is(Items.GOLDEN_APPLE)) {
            return new Gift(3, 20);
        }
        if (stack.is(NorseContent.MEAD.get())) {
            return new Gift(3, 10);
        }
        if (stack.is(Items.COOKED_BEEF) || stack.is(Items.COOKED_MUTTON) || stack.is(Items.COOKED_PORKCHOP)
                || stack.is(Items.COOKED_SALMON) || stack.is(Items.BREAD) || stack.is(Items.SWEET_BERRIES)) {
            return new Gift(3, 4);
        }
        return null;
    }
}
