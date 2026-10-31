package com.mythsofworlds.mythology.greek;

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

/**
 * What the merchants of the agora buy and sell. Each kind of merchant has its own list.
 * Trophies from bosses are the most valuable thing you can bring to Hellas.
 */
public final class GreekTrades {
    /** A trade that can be offered again (offers are created fresh for every merchant). */
    public record Trade(Supplier<MerchantOffer> offer) {
    }

    private GreekTrades() {
    }

    private static Trade sell(ItemLike item, int count, int emeralds) {
        return new Trade(() -> new MerchantOffer(new ItemCost(item, count), new ItemStack(Items.EMERALD, emeralds), 12, 20, 0.05F));
    }

    private static Trade buy(int emeralds, Supplier<ItemStack> result, int maxUses) {
        return new Trade(() -> new MerchantOffer(new ItemCost(Items.EMERALD, emeralds), result.get(), maxUses, 10, 0.05F));
    }

    private static Trade swap(ItemLike trophy, int emeralds, Supplier<ItemStack> result) {
        return new Trade(() -> new MerchantOffer(new ItemCost(trophy, 1), Optional.of(new ItemCost(Items.EMERALD, emeralds)),
                result.get(), 4, 30, 0.05F));
    }

    /** Kind 0, the trophy dealer: pays emeralds for the spoils of every monster of Hellas. */
    public static final List<Trade> TROPHY_DEALER = List.of(
            sell(GreekContent.MINOTAUR_HORN.get(), 1, 32),
            sell(GreekContent.HYDRA_SCALE.get(), 2, 12),
            sell(GreekContent.CERBERUS_FANG.get(), 1, 28),
            sell(GreekContent.MEDUSA_HEAD.get(), 1, 40),
            sell(GreekContent.NEMEAN_PELT.get(), 1, 24),
            sell(GreekContent.NEMEAN_CLAW.get(), 1, 10),
            sell(GreekContent.CYCLOPS_EYE.get(), 1, 18),
            sell(GreekContent.HARPY_FEATHER.get(), 6, 2),
            sell(Items.BONE, 16, 1));

    /** Kind 1, the smith of Hephaestus: turns trophies into weapons and armour. */
    public static final List<Trade> SMITH = List.of(
            swap(GreekContent.MINOTAUR_HORN.get(), 16, () -> new ItemStack(Items.DIAMOND_AXE)),
            swap(GreekContent.CERBERUS_FANG.get(), 12, () -> new ItemStack(Items.TRIDENT)),
            swap(GreekContent.CYCLOPS_EYE.get(), 8, () -> new ItemStack(Items.SPYGLASS)),
            swap(GreekContent.HYDRA_SCALE.get(), 10, () -> new ItemStack(Items.DIAMOND_CHESTPLATE)),
            swap(GreekContent.NEMEAN_CLAW.get(), 6, () -> new ItemStack(GreekContent.NEMEAN_CLAW_DAGGER.get())),
            buy(14, () -> new ItemStack(GreekContent.HARPE.get()), 2),
            buy(6, () -> new ItemStack(Items.SHIELD), 6),
            buy(2, () -> new ItemStack(GreekContent.BRAZIER_ITEM.get()), 12));

    /** Kind 2, the priestess: gifts of the gods. */
    public static final List<Trade> PRIESTESS = List.of(
            buy(6, () -> new ItemStack(GreekContent.AMBROSIA.get()), 8),
            buy(10, () -> new ItemStack(GreekContent.PROMETHEAN_TORCH.get()), 3),
            buy(3, () -> new ItemStack(GreekContent.OLYMPIAN_MARBLE_ITEM.get(), 8), 16),
            buy(4, () -> new ItemStack(GreekContent.DELPHIC_LAUREL.get(), 2), 12),
            buy(8, () -> new ItemStack(GreekContent.ARIADNE_THREAD.get()), 3),
            buy(4, () -> PotionContents.createItemStack(Items.POTION, Potions.STRONG_HEALING), 8),
            buy(4, () -> PotionContents.createItemStack(Items.SPLASH_POTION, Potions.STRONG_POISON), 8),
            buy(5, () -> PotionContents.createItemStack(Items.POTION, Potions.FIRE_RESISTANCE), 8),
            buy(8, () -> new ItemStack(Items.GOLDEN_APPLE), 6),
            buy(1, () -> new ItemStack(GreekContent.ASPHODEL_ITEM.get(), 4), 16));

    public static List<Trade> forKind(int kind) {
        return switch (kind) {
            case 1 -> SMITH;
            case 2 -> PRIESTESS;
            default -> TROPHY_DEALER;
        };
    }
}
