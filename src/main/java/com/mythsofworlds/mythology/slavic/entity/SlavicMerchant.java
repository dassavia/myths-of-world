package com.mythsofworlds.mythology.slavic.entity;

import com.mythsofworlds.core.entity.MythMerchant;
import com.mythsofworlds.mythology.slavic.SlavicTrades;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.npc.WanderingTrader;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.Level;

/**
 * Trader of a village of Nav. Three kinds: 0 a merchant (купец) who buys trophies, 1 Baba Yaga, who sells living and
 * dead water and the acorns of the World Tree, 2 a smith; see {@link SlavicTrades}.
 */
public class SlavicMerchant extends MythMerchant {
    public static final int BABA_YAGA = 1;

    public SlavicMerchant(EntityType<? extends WanderingTrader> type, Level level) {
        super(type, level);
    }

    /** Baba Yaga is small and bent. */
    @Override
    public boolean isShort() {
        return getKind() == BABA_YAGA;
    }

    @Override
    protected void updateTrades() {
        MerchantOffers offers = getOffers();
        for (SlavicTrades.Trade trade : SlavicTrades.forKind(getKind())) {
            offers.add(trade.offer().get());
        }
    }
}
