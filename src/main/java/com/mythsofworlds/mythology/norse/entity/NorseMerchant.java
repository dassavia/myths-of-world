package com.mythsofworlds.mythology.norse.entity;

import com.mythsofworlds.mythology.norse.NorseTrades;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.goal.AvoidEntityGoal;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.InteractGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.LookAtTradingPlayerGoal;
import net.minecraft.world.entity.ai.goal.MoveTowardsRestrictionGoal;
import net.minecraft.world.entity.ai.goal.PanicGoal;
import net.minecraft.world.entity.ai.goal.TradeWithPlayerGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.npc.WanderingTrader;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.trading.MerchantOffers;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import org.jetbrains.annotations.Nullable;

/**
 * Trader of a Viking village. Never leaves its village and never despawns. Three kinds (saved as "Kind"):
 * 0 the jarl's steward who buys trophies, 1 a dwarf smith, 2 a volva (seeress); see {@link NorseTrades}.
 */
public class NorseMerchant extends WanderingTrader {
    public static final int KINDS = 3;
    public static final int DWARF = 1;
    private static final EntityDataAccessor<Integer> KIND = SynchedEntityData.defineId(NorseMerchant.class, EntityDataSerializers.INT);

    public NorseMerchant(EntityType<? extends WanderingTrader> type, Level level) {
        super(type, level);
    }

    /** The wandering trader's goals without its invisibility and milk potions and its wandering off. */
    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(1, new TradeWithPlayerGoal(this));
        goalSelector.addGoal(1, new AvoidEntityGoal<>(this, Monster.class, 8.0F, 0.5, 0.5));
        goalSelector.addGoal(1, new PanicGoal(this, 0.5));
        goalSelector.addGoal(1, new LookAtTradingPlayerGoal(this));
        goalSelector.addGoal(4, new MoveTowardsRestrictionGoal(this, 0.35));
        goalSelector.addGoal(8, new WaterAvoidingRandomStrollGoal(this, 0.35));
        goalSelector.addGoal(9, new InteractGoal(this, Player.class, 3.0F, 1.0F));
        goalSelector.addGoal(10, new LookAtPlayerGoal(this, Player.class, 8.0F));
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(KIND, 0);
    }

    public int getKind() {
        return entityData.get(KIND);
    }

    public void setKind(int kind) {
        entityData.set(KIND, Math.floorMod(kind, KINDS));
    }

    @Nullable
    @Override
    public SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, MobSpawnType spawnType,
                                        @Nullable SpawnGroupData spawnGroupData) {
        if (spawnType != MobSpawnType.STRUCTURE) {
            setKind(random.nextInt(KINDS));
        }
        return super.finalizeSpawn(level, difficulty, spawnType, spawnGroupData);
    }

    @Override
    protected void updateTrades() {
        MerchantOffers offers = getOffers();
        for (NorseTrades.Trade trade : NorseTrades.forKind(getKind())) {
            offers.add(trade.offer().get());
        }
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("Kind", getKind());
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        setKind(tag.getInt("Kind"));
    }

    @Override
    public void aiStep() {
        super.aiStep();
        // Stays near its longhouse.
        if (!level().isClientSide && !hasRestriction()) {
            restrictTo(blockPosition(), 10);
        }
    }

    @Override
    public void setTradingPlayer(@Nullable Player player) {
        if (player != null && getTradingPlayer() == null) {
            playSound(SoundEvents.VILLAGER_TRADE, 0.8F, getKind() == DWARF ? 0.7F : 1.0F);
        }
        super.setTradingPlayer(player);
    }

    @Override
    public boolean removeWhenFarAway(double distanceToClosestPlayer) {
        return false;
    }

    @Override
    public boolean requiresCustomPersistence() {
        return true;
    }
}
