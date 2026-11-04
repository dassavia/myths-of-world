package com.mythsofworlds.mythology.egyptian;

import java.util.List;
import java.util.Optional;
import java.util.function.Supplier;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.alchemy.PotionContents;
import net.minecraft.world.item.alchemy.Potions;
import net.minecraft.world.item.trading.ItemCost;
import net.minecraft.world.item.trading.MerchantOffer;
import net.minecraft.world.level.ItemLike;

/** What the traders of the villages on the Nile buy and sell. Each kind of trader has its own list. */
public final class EgyptianTrades {
    /** A trade that can be offered again (offers are created fresh for every trader). */
    public record Trade(Supplier<MerchantOffer> offer) {
    }

    private EgyptianTrades() {
    }

    private static Trade sell(ItemLike item, int count, int emeralds) {
        return new Trade(() -> new MerchantOffer(new ItemCost(item, count), new ItemStack(Items.EMERALD, emeralds), 12, 20, 0.05F));
    }

    private static Trade buy(int emeralds, Supplier<ItemStack> result, int maxUses) {
        return new Trade(() -> new MerchantOffer(new ItemCost(Items.EMERALD, emeralds), result.get(), maxUses, 10, 0.05F));
    }

    private static Trade swap(ItemLike trophy, int count, int emeralds, Supplier<ItemStack> result) {
        return new Trade(() -> new MerchantOffer(new ItemCost(trophy, count), Optional.of(new ItemCost(Items.EMERALD, emeralds)),
                result.get(), 4, 30, 0.05F));
    }

    /** Kind 0, the trader of the market: pays for the spoils of the monsters of the Duat, sells dates, cakes and linen. */
    public static final List<Trade> TRADER = List.of(
            sell(EgyptianContent.APEP_SCALE.get(), 1, 14),
            sell(EgyptianContent.SPHINX_CLAW.get(), 1, 12),
            sell(EgyptianContent.SCARAB_SHELL.get(), 2, 3),
            sell(EgyptianContent.SCORPION_STINGER.get(), 2, 3),
            sell(EgyptianContent.JACKAL_PELT.get(), 2, 2),
            sell(EgyptianContent.MUMMY_WRAPPINGS.get(), 8, 1),
            sell(EgyptianContent.CROCODILE_HIDE.get(), 3, 2),
            buy(1, () -> new ItemStack(EgyptianContent.DATES.get(), 6), 16),
            buy(2, () -> new ItemStack(EgyptianContent.NILE_SILT_ITEM.get(), 8), 12),
            buy(4, () -> new ItemStack(EgyptianContent.GIFT_OF_HAPI.get(), 4), 8),
            buy(3, () -> new ItemStack(EgyptianContent.HONEY_CAKE.get(), 2), 12),
            buy(2, () -> new ItemStack(Items.WHITE_WOOL, 6), 12),
            buy(4, () -> new ItemStack(Items.LAPIS_LAZULI, 8), 8));

    /** Kind 1, the priest of Anubis: ankhs, the eye of Horus, the sistrum and potions for the road through the night. */
    public static final List<Trade> PRIEST = List.of(
            buy(12, () -> new ItemStack(EgyptianContent.ANKH.get()), 3),
            buy(18, () -> new ItemStack(EgyptianContent.EYE_OF_HORUS.get()), 1),
            buy(6, () -> new ItemStack(EgyptianContent.SISTRUM.get()), 2),
            buy(4, () -> PotionContents.createItemStack(Items.POTION, Potions.LONG_NIGHT_VISION), 8),
            buy(5, () -> PotionContents.createItemStack(Items.POTION, Potions.LONG_FIRE_RESISTANCE), 8),
            buy(4, () -> PotionContents.createItemStack(Items.POTION, Potions.STRONG_HEALING), 8),
            buy(6, () -> PotionContents.createItemStack(Items.SPLASH_POTION, Potions.HARMING), 6),
            sell(EgyptianContent.MUMMY_WRAPPINGS.get(), 6, 2),
            sell(Items.BONE, 16, 1));

    /** Kind 2, the smith: forges the trophies of the Duat and its meteoric iron into weapons and armour. */
    public static final List<Trade> SMITH = List.of(
            swap(EgyptianContent.APEP_SCALE.get(), 2, 12, () -> new ItemStack(Items.DIAMOND_CHESTPLATE)),
            swap(EgyptianContent.SPHINX_CLAW.get(), 2, 10, () -> new ItemStack(Items.DIAMOND_SWORD)),
            swap(EgyptianContent.SCORPION_STINGER.get(), 6, 6, () -> new ItemStack(Items.DIAMOND_HELMET)),
            buy(14, () -> new ItemStack(EgyptianContent.METEORIC_IRON.ingot.get()), 4),
            buy(6, () -> new ItemStack(Items.SHIELD), 6),
            buy(5, () -> new ItemStack(Items.GOLDEN_HORSE_ARMOR), 3),
            buy(4, () -> new ItemStack(Items.GOLD_INGOT, 3), 8),
            buy(2, () -> new ItemStack(Items.LANTERN, 4), 12));

    public static List<Trade> forKind(int kind) {
        return switch (kind) {
            case 1 -> PRIEST;
            case 2 -> SMITH;
            default -> TRADER;
        };
    }
}
