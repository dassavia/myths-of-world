package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.core.family.WarriorMaiden;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import net.minecraft.tags.ItemTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * Amazon, warrior woman of Themiscyra; courted, wed and raising daughters as every {@link WarriorMaiden}. Amazons like
 * flowers, gold and jewels, weapons and the trophies of the monsters of Hellas, and good food; give your wife a cake
 * for a daughter. The necklace of Harmonia wins any amazon's heart at once, and the horn of Themiscyra calls strays
 * back to their camp.
 */
public class Amazon extends WarriorMaiden {
    /** Looks 0 to {@code VARIANTS - 1}; {@link #ROYAL} among them is the look of Hippolyta's daughters only. */
    public static final int VARIANTS = 16;
    public static final int ROYAL = 4;

    private static final String[] NAMES = {"Antiope", "Melanippe", "Penthesilea", "Otrere", "Aella", "Areto", "Alcippe",
            "Hippothoe", "Lampedo", "Marpesia", "Orithyia", "Clonie", "Polemusa", "Derinoe", "Antibrote", "Bremusa",
            "Thermodosa", "Andromache", "Philippis", "Prothoe", "Myrina", "Thalestris", "Lysippe", "Ainia", "Antianeira",
            "Asteria", "Celaeno", "Eurybe", "Phoebe", "Deianira", "Tecmessa", "Alcibie", "Evandre", "Glauke", "Harmothoe",
            "Hippomache", "Iphito", "Molpadia", "Pantariste", "Toxaris", "Xanthippe", "Euryale", "Okyale", "Pisto",
            "Laomache", "Thraso", "Iodoke", "Kreousa", "Gortyessa", "Hippolyte", "Antandre", "Elaia", "Kleite"};

    public Amazon(EntityType<? extends AgeableMob> type, Level level) {
        super(type, level);
    }

    @Override
    protected String messages() {
        return "entity.mythsofworlds.amazon.";
    }

    @Override
    public String textureName() {
        return "amazon_" + Math.floorMod(getVariant(), VARIANTS);
    }

    @Override
    protected String randomName() {
        return NAMES[random.nextInt(NAMES.length)];
    }

    @Override
    protected int randomVariant() {
        return commonVariant(random);
    }

    @Override
    protected int childVariant() {
        return random.nextBoolean() && getVariant() != ROYAL ? getVariant() : commonVariant(random);
    }

    /** Any look but the royal one. */
    public static int commonVariant(RandomSource random) {
        int variant = random.nextInt(VARIANTS - 1);
        return variant >= ROYAL ? variant + 1 : variant;
    }

    @Nullable
    @Override
    protected WarriorMaiden newChild() {
        return GreekEntities.AMAZON.get().create(level());
    }

    @Nullable
    @Override
    protected Gift giftFor(ItemStack stack) {
        return gift(stack);
    }

    /** How much a gift is worth to amazons, or null if it is no gift. */
    @Nullable
    public static Gift gift(ItemStack stack) {
        if (stack.is(ItemTags.FLOWERS)) {
            return new Gift(0, 6);
        }
        if (stack.is(Items.GOLD_BLOCK)) {
            return new Gift(1, 40);
        }
        if (stack.is(Items.DIAMOND)) {
            return new Gift(1, 20);
        }
        if (stack.is(Items.GOLD_INGOT)) {
            return new Gift(1, 10);
        }
        if (stack.is(Items.EMERALD)) {
            return new Gift(1, 8);
        }
        if (stack.is(Items.AMETHYST_SHARD) || stack.is(Items.GOLD_NUGGET)) {
            return new Gift(1, 3);
        }
        if (stack.is(GreekContent.MINOTAUR_HORN.get()) || stack.is(GreekContent.HYDRA_SCALE.get())
                || stack.is(GreekContent.CERBERUS_FANG.get()) || stack.is(GreekContent.NEMEAN_PELT.get())
                || stack.is(GreekContent.CYCLOPS_EYE.get()) || stack.is(GreekContent.KARKINOS_CLAW.get())) {
            return new Gift(2, 20);
        }
        if (stack.is(ItemTags.SWORDS) || stack.is(ItemTags.AXES) || stack.is(Items.BOW) || stack.is(Items.CROSSBOW)
                || stack.is(Items.TRIDENT) || stack.is(Items.SHIELD)) {
            return new Gift(2, 12);
        }
        if (stack.is(GreekContent.HARPY_FEATHER.get())) {
            return new Gift(2, 4);
        }
        if (stack.is(GreekContent.AMBROSIA.get())) {
            return new Gift(3, 25);
        }
        if (stack.is(Items.GOLDEN_APPLE)) {
            return new Gift(3, 20);
        }
        if (stack.is(Items.HONEY_BOTTLE) || stack.is(GreekContent.POMEGRANATE.get())) {
            return new Gift(3, 8);
        }
        if (stack.is(GreekContent.OLIVES.get()) || stack.is(Items.BREAD) || stack.is(Items.COOKIE) || stack.is(Items.COOKED_MUTTON)
                || stack.is(Items.COOKED_BEEF) || stack.is(Items.SWEET_BERRIES)) {
            return new Gift(3, 4);
        }
        return null;
    }

    /** The horn of Themiscyra. */
    @Override
    public Item horn() {
        return GreekContent.HORN_OF_THEMISCYRA.get();
    }

    /** The necklace of Harmonia. */
    @Override
    protected boolean isLoveCharm(ItemStack stack) {
        return stack.is(GreekContent.NECKLACE_OF_HARMONIA.get());
    }
}
