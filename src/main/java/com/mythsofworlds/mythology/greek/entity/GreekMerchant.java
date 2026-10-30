package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.core.entity.MythMerchant;
import com.mythsofworlds.mythology.greek.GreekSounds;
import com.mythsofworlds.mythology.greek.GreekTrades;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.npc.WanderingTrader;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.Level;

/** Merchant of the agora. Three kinds: 0 trophy dealer, 1 smith of Hephaestus, 2 priestess; see {@link GreekTrades}. */
public class GreekMerchant extends MythMerchant {
    public GreekMerchant(EntityType<? extends WanderingTrader> type, Level level) {
        super(type, level);
    }

    @Override
    protected void updateTrades() {
        MerchantOffers offers = getOffers();
        for (GreekTrades.Trade trade : GreekTrades.forKind(getKind())) {
            offers.add(trade.offer().get());
        }
    }

    /** A few notes of the lyre. */
    @Override
    protected void greet() {
        playSound(GreekSounds.MERCHANT_GREET.get(), 0.8F, 1.0F);
    }
}
