package com.mythsofworlds.core.entity;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.Mythology;
import java.util.Optional;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.BossEvent;
import net.minecraft.world.entity.Entity;
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
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animation.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.PlayState;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Shared behaviour of the bosses and mini-bosses of every world of the myths: a boss bar, no despawning, and a plain
 * "walk to the player and hit them" AI that each boss extends with its own ability in {@link #customServerAiStep()}.
 * <p>
 * Two phases: below half health ({@link #enraged()}) most bosses fight harder. The bar names the boss and its world
 * ("Koschei the Deathless · Nav"); when the boss flies into a rage it roars, the bar turns red and says so, and when
 * it heals above half again (Koschei rising) the bar goes back.
 * <p>
 * The bosses drawn with GeckoLib (MythGeoRenderer) play the animations of their model: idle and walk, "attack" on
 * every blow and "special" when they use their power ({@link #playSpecial()}).
 */
public abstract class MythBoss extends Monster implements GeoEntity, BalancedBoss {
    private static final RawAnimation IDLE = RawAnimation.begin().thenLoop("idle");
    private static final RawAnimation WALK = RawAnimation.begin().thenLoop("walk");
    private static final RawAnimation ATTACK = RawAnimation.begin().thenPlay("attack");
    private static final RawAnimation SPECIAL = RawAnimation.begin().thenPlay("special");

    private final ServerBossEvent bossEvent;
    private final BossEvent.BossBarColor calmColour;
    private final AnimatableInstanceCache animations = GeckoLibUtil.createInstanceCache(this);
    /** The phase the bar shows, null until the first look at the boss's health. */
    @Nullable
    private Boolean ragingShown;

    /**
     * @param miniBoss mini-bosses get a yellow, notched bar; bosses a red or purple one
     */
    protected MythBoss(EntityType<? extends Monster> type, Level level, BossEvent.BossBarColor color, boolean miniBoss) {
        super(type, level);
        this.calmColour = color;
        this.bossEvent = new ServerBossEvent(barName(false), color,
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

    /** The mythology whose boss this is, from the lists in {@link Mythology}. */
    public Optional<Mythology> mythology() {
        ResourceLocation id = BuiltInRegistries.ENTITY_TYPE.getKey(getType());
        if (!id.getNamespace().equals(MythsOfWorlds.MODID)) {
            return Optional.empty();
        }
        for (Mythology mythology : Mythology.values()) {
            if (mythology.bosses().contains(id.getPath())) {
                return Optional.of(mythology);
            }
        }
        return Optional.empty();
    }

    /** "Name · World", and "in a rage" in the second phase. */
    private Component barName(boolean raging) {
        Optional<Mythology> mythology = mythology();
        if (mythology.isEmpty()) {
            return getDisplayName();
        }
        Component world = Component.translatable("hud.mythsofworlds.world." + mythology.get().world());
        return Component.translatable(raging ? "boss.mythsofworlds.bar.enraged" : "boss.mythsofworlds.bar", getDisplayName(), world);
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        bossEvent.setProgress(getHealth() / getMaxHealth());
        boolean raging = enraged();
        if (ragingShown == null || ragingShown != raging) {
            if (ragingShown != null && raging && level() instanceof ServerLevel server) {
                enterRage(server);
            }
            ragingShown = raging;
            bossEvent.setName(barName(raging));
            bossEvent.setColor(raging ? BossEvent.BossBarColor.RED : calmColour);
        }
    }

    /** The second phase begins: a roar, a burst of anger, a line over the hotbar of everyone fighting. */
    protected void enterRage(ServerLevel server) {
        playSound(SoundEvents.RAVAGER_ROAR, 2.0F, 0.7F);
        server.sendParticles(ParticleTypes.ANGRY_VILLAGER, getX(), getY(1.0), getZ(), 12, getBbWidth() * 0.5, 0.5, getBbWidth() * 0.5, 0.0);
        playSpecial();
        for (ServerPlayer player : bossEvent.getPlayers()) {
            player.displayClientMessage(Component.translatable("boss.mythsofworlds.enraged", getDisplayName()), true);
        }
    }

    /** Plays the "special" animation of the boss's model (on every client that sees it). */
    protected void playSpecial() {
        if (!level().isClientSide) {
            triggerAnim("action", "special");
        }
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && !level().isClientSide) {
            triggerAnim("action", "attack");
        }
        return hit;
    }

    @Override
    public void registerControllers(AnimatableManager.ControllerRegistrar controllers) {
        controllers.add(new AnimationController<>(this, "move", 5,
                state -> state.setAndContinue(state.isMoving() ? WALK : IDLE)));
        controllers.add(new AnimationController<>(this, "action", 2, state -> PlayState.STOP)
                .triggerableAnim("attack", ATTACK)
                .triggerableAnim("special", SPECIAL));
    }

    @Override
    public AnimatableInstanceCache getAnimatableInstanceCache() {
        return animations;
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
        bossEvent.setName(barName(Boolean.TRUE.equals(ragingShown)));
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        if (hasCustomName()) {
            bossEvent.setName(barName(Boolean.TRUE.equals(ragingShown)));
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
