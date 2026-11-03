package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * Priestess of Isis, keeper of the temples of the great goddess on the banks of the Nile of the Duat. Courted and
 * married like an amazon (see {@link Amazon}), with the wedding ring: she likes lotus and flowers, gold and lapis,
 * sweet things (honey and dates) and the trophies of the monsters of the Duat; the knot of Isis wins her heart at
 * once, and the sistrum of Hathor calls her back to her temple. Give your wife a honey cake and a daughter is born,
 * once a day; she grows up a priestess loyal to your family. She fights with a spear (a trident) and a staff of gold.
 */
public class Priestess extends Amazon {
    public static final int LOOKS = 8;

    private static final String[] NAMES = {"Nefertari", "Nefertiti", "Merit", "Tiye", "Ankhesenamun", "Hatshepsut",
            "Neferure", "Meritamun", "Isetnofret", "Nebet", "Sitamun", "Ahhotep", "Ahmose", "Henutmire", "Tawosret",
            "Nitocris", "Khentkaus", "Meresankh", "Hetepheres", "Satiah", "Baketaten", "Nebettawy", "Bintanath",
            "Takhat", "Mutnodjmet", "Kiya", "Iset", "Renenet", "Seshat", "Tamit", "Menna", "Nefru", "Henut",
            "Ipwet", "Tiaa", "Wadjet", "Amunet", "Meryet", "Khnumet", "Sobekneferu", "Nubkhaes", "Tetisheri"};

    public Priestess(EntityType<? extends AgeableMob> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Amazon.createAttributes()
                .add(Attributes.MAX_HEALTH, 40.0)
                .add(Attributes.ATTACK_DAMAGE, 8.0)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.ARMOR_TOUGHNESS, 4.0);
    }

    @Override
    public Item horn() {
        return EgyptianContent.SISTRUM.get();
    }

    /** The knot of Isis, the goddess's own amulet, wins a priestess's heart at once. */
    @Override
    protected boolean isLoveCharm(ItemStack stack) {
        return stack.is(EgyptianContent.KNOT_OF_ISIS.get());
    }

    @Override
    protected String messages() {
        return "entity.mythsofworlds.priestess.";
    }

    @Override
    public String textureName() {
        return "priestess_" + Math.floorMod(getVariant(), LOOKS);
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
        return EgyptianEntities.PRIESTESS.get().create(level());
    }

    @Override
    protected ItemStack childGift() {
        return new ItemStack(EgyptianContent.HONEY_CAKE.get());
    }

    @Override
    protected void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(random.nextInt(10) < 6 ? Items.TRIDENT : Items.GOLDEN_SWORD));
        setDropChance(EquipmentSlot.MAINHAND, 0.0F);
    }

    /** Gifts for a priestess: 0 lotus and flowers, 1 gold and lapis, 2 sweet things, 3 trophies of the Duat. */
    @Nullable
    @Override
    protected Gift giftFor(ItemStack stack) {
        if (stack.is(Items.LILY_PAD)) {
            return new Gift(0, 10);
        }
        if (stack.is(ItemTags.FLOWERS)) {
            return new Gift(0, 6);
        }
        if (stack.is(Items.GOLD_BLOCK) || stack.is(Items.LAPIS_BLOCK)) {
            return new Gift(1, 40);
        }
        if (stack.is(Items.DIAMOND)) {
            return new Gift(1, 20);
        }
        if (stack.is(Items.GOLD_INGOT) || stack.is(EgyptianContent.METEORIC_IRON.ingot.get())) {
            return new Gift(1, 10);
        }
        if (stack.is(Items.LAPIS_LAZULI) || stack.is(Items.EMERALD)) {
            return new Gift(1, 6);
        }
        if (stack.is(Items.GOLD_NUGGET)) {
            return new Gift(1, 2);
        }
        if (stack.is(EgyptianContent.HONEY_CAKE.get()) || stack.is(Items.GOLDEN_APPLE)) {
            return new Gift(2, 20);
        }
        if (stack.is(Items.HONEY_BOTTLE) || stack.is(Items.CAKE)) {
            return new Gift(2, 10);
        }
        if (stack.is(EgyptianContent.DATES.get()) || stack.is(Items.MELON_SLICE) || stack.is(Items.SWEET_BERRIES)
                || stack.is(Items.COOKIE) || stack.is(Items.BREAD)) {
            return new Gift(2, 4);
        }
        if (stack.is(EgyptianContent.APEP_SCALE.get()) || stack.is(EgyptianContent.SPHINX_CLAW.get())) {
            return new Gift(3, 25);
        }
        if (stack.is(EgyptianContent.SCARAB_SHELL.get()) || stack.is(EgyptianContent.SCORPION_STINGER.get())
                || stack.is(EgyptianContent.JACKAL_PELT.get())) {
            return new Gift(3, 10);
        }
        if (stack.is(EgyptianContent.MUMMY_WRAPPINGS.get())) {
            return new Gift(3, 3);
        }
        return null;
    }
}
