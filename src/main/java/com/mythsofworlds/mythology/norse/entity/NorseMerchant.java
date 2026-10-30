package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.core.entity.MythMerchant;
import com.mythsofworlds.mythology.norse.NorseTrades;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.npc.WanderingTrader;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.Level;

/**
 * Trader of a Viking village. Three kinds: 0 the jarl's steward who buys trophies, 1 a dwarf smith, 2 a volva
 * (seeress); see {@link NorseTrades}.
 */
public class NorseMerchant extends MythMerchant {
    public static final int DWARF = 1;

    public NorseMerchant(EntityType<? extends WanderingTrader> type, Level level) {
        super(type, level);
    }

    @Override
    public boolean isShort() {
        return getKind() == DWARF;
    }

    @Override
    protected void updateTrades() {
        MerchantOffers offers = getOffers();
        for (NorseTrades.Trade trade : NorseTrades.forKind(getKind())) {
            offers.add(trade.offer().get());
        }
    }
}
