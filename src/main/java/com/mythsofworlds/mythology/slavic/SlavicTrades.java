package com.mythsofworlds.mythology.slavic;

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

/** What the traders of the villages of Nav buy and sell. Each kind of trader has its own list. */
public final class SlavicTrades {
    /** A trade that can be offered again (offers are created fresh for every trader). */
    public record Trade(Supplier<MerchantOffer> offer) {
    }

    private SlavicTrades() {
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

    /** Kind 0, the merchant (купец): pays for the spoils of the monsters of Nav, sells bread and honey. */
    public static final List<Trade> MERCHANT = List.of(
            sell(SlavicContent.ZMEY_SCALE.get(), 1, 12),
            sell(SlavicContent.VOLKOLAK_PELT.get(), 1, 6),
            sell(SlavicContent.UPYR_FANG.get(), 3, 2),
            sell(SlavicContent.FIREBIRD_FEATHER.get(), 1, 8),
            sell(Items.ROTTEN_FLESH, 24, 1),
            buy(2, () -> new ItemStack(SlavicContent.KARAVAI.get(), 2), 16),
            buy(2, () -> new ItemStack(Items.HONEY_BOTTLE, 3), 12),
            buy(1, () -> new ItemStack(Items.BREAD, 6), 16),
            buy(12, () -> new ItemStack(SlavicContent.WORLD_TREE_ACORN.get()), 2),
            buy(20, () -> new ItemStack(SlavicContent.GUSLI.get()), 1));

    /** Kind 1, Baba Yaga in her hut on chicken legs: the waters of life and death, acorns of the World Tree, brews. */
    public static final List<Trade> BABA_YAGA = List.of(
            buy(10, () -> new ItemStack(SlavicContent.LIVING_WATER.get()), 4),
            buy(8, () -> new ItemStack(SlavicContent.DEAD_WATER.get()), 4),
            buy(8, () -> new ItemStack(SlavicContent.WORLD_TREE_ACORN.get()), 4),
            buy(6, () -> new ItemStack(SlavicContent.KLUBOK.get()), 3),
            buy(4, () -> PotionContents.createItemStack(Items.POTION, Potions.STRONG_HEALING), 8),
            buy(4, () -> PotionContents.createItemStack(Items.POTION, Potions.NIGHT_VISION), 8),
            buy(5, () -> PotionContents.createItemStack(Items.POTION, Potions.INVISIBILITY), 6),
            buy(6, () -> PotionContents.createItemStack(Items.SPLASH_POTION, Potions.HARMING), 6),
            sell(SlavicContent.UPYR_FANG.get(), 2, 3),
            sell(Items.BONE, 16, 1));

    /** Kind 2, the smith: forges the trophies of Nav into weapons and armour. */
    public static final List<Trade> SMITH = List.of(
            swap(SlavicContent.ZMEY_SCALE.get(), 2, 12, () -> new ItemStack(Items.DIAMOND_CHESTPLATE)),
            swap(SlavicContent.VOLKOLAK_PELT.get(), 2, 6, () -> new ItemStack(Items.DIAMOND_HELMET)),
            swap(SlavicContent.UPYR_FANG.get(), 6, 8, () -> new ItemStack(Items.DIAMOND_SWORD)),
            buy(5, () -> new ItemStack(Items.IRON_AXE), 6),
            buy(6, () -> new ItemStack(Items.SHIELD), 6),
            buy(4, () -> new ItemStack(Items.CHAINMAIL_CHESTPLATE), 4),
            buy(3, () -> new ItemStack(Items.IRON_HORSE_ARMOR), 3),
            buy(2, () -> new ItemStack(Items.LANTERN, 4), 12));

    public static List<Trade> forKind(int kind) {
        return switch (kind) {
            case 1 -> BABA_YAGA;
            case 2 -> SMITH;
            default -> MERCHANT;
        };
    }
}
