package com.mythsofworlds.core.entity;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.BossEvent;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * Shared behaviour of the bosses and mini-bosses of every world of the myths: a boss bar, no despawning, and a plain
 * "walk to the player and hit them" AI that each boss extends with its own ability in {@link #customServerAiStep()}.
 */
public abstract class MythBoss extends Monster {
    private final ServerBossEvent bossEvent;

    /**
     * @param miniBoss mini-bosses get a yellow, notched bar; bosses a red or purple one
     */
    protected MythBoss(EntityType<? extends Monster> type, Level level, BossEvent.BossBarColor color, boolean miniBoss) {
        super(type, level);
        this.bossEvent = new ServerBossEvent(getDisplayName(), color,
                miniBoss ? BossEvent.BossBarOverlay.NOTCHED_6 : BossEvent.BossBarOverlay.PROGRESS);
        this.xpReward = miniBoss ? 30 : 80;
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.0, true));
        goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 0.7));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 16.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this));
        if (hostile()) {
            targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
        }
    }

    /** False for neutral bosses, which only fight back once attacked. */
    protected boolean hostile() {
        return true;
    }

    /** Below half health most bosses fight harder. */
    protected boolean enraged() {
        return getHealth() < getMaxHealth() / 2.0F;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        bossEvent.setProgress(getHealth() / getMaxHealth());
    }

    /** False for the small guardians that fight without a health bar on the screen. */
    protected boolean hasBossBar() {
        return true;
    }

    @Override
    public void startSeenByPlayer(ServerPlayer player) {
        super.startSeenByPlayer(player);
        if (hasBossBar()) {
            bossEvent.addPlayer(player);
        }
    }

    @Override
    public void stopSeenByPlayer(ServerPlayer player) {
        super.stopSeenByPlayer(player);
        bossEvent.removePlayer(player);
    }

    @Override
    public void setCustomName(@Nullable Component name) {
        super.setCustomName(name);
        bossEvent.setName(getDisplayName());
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        if (hasCustomName()) {
            bossEvent.setName(getDisplayName());
        }
    }

    /** Bosses guard their lair forever. */
    @Override
    public boolean removeWhenFarAway(double distanceToClosestPlayer) {
        return false;
    }

    @Override
    public boolean requiresCustomPersistence() {
        return true;
    }
}
