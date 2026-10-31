package com.mythsofworlds.mythology.norse;

import com.mythsofworlds.mythology.norse.item.RuneItem;
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

/** What the traders of the Viking villages buy and sell. Each kind of trader has its own list. */
public final class NorseTrades {
    /** A trade that can be offered again (offers are created fresh for every trader). */
    public record Trade(Supplier<MerchantOffer> offer) {
    }

    private NorseTrades() {
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

    /** Kind 0, the jarl's steward: pays emeralds for the spoils of giants and monsters. */
    public static final List<Trade> STEWARD = List.of(
            sell(NorseContent.FENRIR_FANG.get(), 1, 36),
            sell(NorseContent.GARM_FANG.get(), 1, 24),
            sell(NorseContent.BARROW_CROWN.get(), 1, 30),
            sell(NorseContent.FROST_HEART.get(), 1, 10),
            sell(NorseContent.MUSPEL_EMBER.get(), 1, 10),
            sell(NorseContent.TROLL_TUSK.get(), 1, 8),
            sell(NorseContent.RAVEN_FEATHER.get(), 6, 2),
            sell(Items.ROTTEN_FLESH, 24, 1),
            buy(3, () -> new ItemStack(NorseContent.MEAD.get(), 2), 12));

    /** Kind 1, the dwarf smith, a kinsman of Brokkr and Sindri: forges trophies into weapons, makes Gleipnir, and for
     *  the fangs of the great wolves the treasures of Odin, Draupnir and Gungnir. */
    public static final List<Trade> DWARF_SMITH = List.of(
            swap(NorseContent.FENRIR_FANG.get(), 16, () -> new ItemStack(Items.DIAMOND_SWORD)),
            swap(NorseContent.TROLL_TUSK.get(), 8, () -> new ItemStack(Items.DIAMOND_PICKAXE)),
            swap(NorseContent.FROST_HEART.get(), 6, () -> new ItemStack(Items.DIAMOND_HELMET)),
            swap(NorseContent.MUSPEL_EMBER.get(), 6, () -> new ItemStack(Items.DIAMOND_CHESTPLATE)),
            swap(NorseContent.BARROW_CROWN.get(), 12, () -> new ItemStack(Items.NETHERITE_SCRAP, 2)),
            buy(24, () -> new ItemStack(NorseContent.GLEIPNIR.get()), 1),
            swap(NorseContent.GARM_FANG.get(), 32, () -> new ItemStack(NorseContent.DRAUPNIR.get())),
            swap(NorseContent.FENRIR_FANG.get(), 48, () -> new ItemStack(NorseContent.GUNGNIR.get())),
            buy(5, () -> new ItemStack(Items.IRON_AXE), 6),
            buy(6, () -> new ItemStack(Items.SHIELD), 6),
            buy(2, () -> new ItemStack(NorseContent.RUNESTONE_ITEM.get(), 8), 16));

    /** Kind 2, the volva: seeress and healer, who sells runes, apples of Idunn and potions. */
    public static final List<Trade> VOLVA = List.of(
            buy(8, () -> new ItemStack(NorseContent.IDUNN_APPLE.get()), 6),
            buy(10, () -> new ItemStack(NorseContent.RUNE_IGNITER.get()), 3),
            buy(3, () -> new ItemStack(NorseContent.CARVED_RUNESTONE_ITEM.get(), 4), 16),
            buy(4, () -> new ItemStack(NorseContent.RUNES.get(RuneItem.Rune.ANSUZ).get(), 2), 8),
            buy(4, () -> new ItemStack(NorseContent.RUNES.get(RuneItem.Rune.ALGIZ).get(), 2), 8),
            buy(4, () -> PotionContents.createItemStack(Items.POTION, Potions.FIRE_RESISTANCE), 8),
            buy(4, () -> PotionContents.createItemStack(Items.POTION, Potions.STRONG_HEALING), 8),
            buy(5, () -> PotionContents.createItemStack(Items.POTION, Potions.NIGHT_VISION), 8),
            buy(2, () -> new ItemStack(Items.SNOWBALL, 16), 16),
            buy(3, () -> new ItemStack(Items.WHEAT_SEEDS, 8), 8));

    public static List<Trade> forKind(int kind) {
        return switch (kind) {
            case 1 -> DWARF_SMITH;
            case 2 -> VOLVA;
            default -> STEWARD;
        };
    }
}
