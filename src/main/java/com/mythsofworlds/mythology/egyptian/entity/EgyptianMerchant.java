package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianTrades;
import com.mythsofworlds.mythology.norse.entity.NorseMerchant;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.npc.WanderingTrader;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.Level;

/**
 * Trader of a village on the Nile of the Duat. Kinds as for {@link NorseMerchant}: 0 a trader of the market who buys
 * trophies, 1 a priest of Anubis who sells ankhs, the eye of Horus and potions, 2 a smith who works meteoric iron;
 * see {@link EgyptianTrades}.
 */
public class EgyptianMerchant extends NorseMerchant {
    public static final int PRIEST = 1;

    public EgyptianMerchant(EntityType<? extends WanderingTrader> type, Level level) {
        super(type, level);
    }

    @Override
    protected void updateTrades() {
        MerchantOffers offers = getOffers();
        for (EgyptianTrades.Trade trade : EgyptianTrades.forKind(getKind())) {
            offers.add(trade.offer().get());
        }
    }
}
