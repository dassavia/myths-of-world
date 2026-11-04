package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import java.util.List;
import java.util.function.Supplier;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.RandomSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * Shared behaviour of the gods of Egypt who walk the Duat: Ra, Osiris, Isis, Horus, Anubis, Thoth, Bastet, Sobek,
 * Hathor, Ptah and Sekhmet (Set is a boss of his own, {@link SetGod}). Each waits in their shrine with the weapon of
 * their myth in hand (not dropped: the loot table gives the god's relic, from which the weapon is forged). Most are
 * neutral and only fight a hero who dares to challenge them; every few seconds in a fight they use the power of their
 * myth ({@link #power}), more often below half health.
 */
public abstract class EgyptianGod extends GreekBoss {
    private final Supplier<? extends Item> weapon;
    private int powerCooldown = 60;

    protected EgyptianGod(EntityType<? extends Monster> type, Level level, BossEvent.BossBarColor color,
                          Supplier<? extends Item> weapon) {
        super(type, level, color, false);
        this.weapon = weapon;
    }

    /** Gods are neutral unless they say otherwise. */
    @Override
    protected boolean hostile() {
        return false;
    }

    /** Ticks between two uses of the power; a third shorter below half health. */
    protected abstract int powerInterval();

    /** How close the foe must be for the power to be used. */
    protected double powerRange() {
        return 16.0;
    }

    /** The power of the god's myth, used on its current foe. */
    public abstract void power(ServerLevel server, LivingEntity target);

    @Nullable
    @Override
    public SpawnGroupData finalizeSpawn(ServerLevelAccessor level, DifficultyInstance difficulty, MobSpawnType spawnType,
                                        @Nullable SpawnGroupData data) {
        arm();
        return super.finalizeSpawn(level, difficulty, spawnType, data);
    }

    @Override
    protected void populateDefaultEquipmentSlots(RandomSource random, DifficultyInstance difficulty) {
        arm();
    }

    /** The weapon of the myth in the god's hand; it is not dropped. */
    private void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(weapon.get()));
        setDropChance(EquipmentSlot.MAINHAND, 0.0F);
    }

    @Override
    public void tick() {
        super.tick();
        if (!level().isClientSide && tickCount < 40 && getMainHandItem().isEmpty()) {
            arm();
        }
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        LivingEntity target = getTarget();
        if (target == null || !target.isAlive() || !(level() instanceof ServerLevel server)) {
            return;
        }
        if (--powerCooldown <= 0 && distanceToSqr(target) < powerRange() * powerRange()) {
            powerCooldown = enraged() ? powerInterval() * 2 / 3 : powerInterval();
            power(server, target);
        }
    }

    /** The players around the god within {@code radius} blocks who can be struck (not in creative or spectating). */
    protected List<Player> foesAround(ServerLevel server, double radius) {
        return server.getEntitiesOfClass(Player.class, getBoundingBox().inflate(radius),
                p -> p.isAlive() && !p.isSpectator() && !p.isCreative());
    }

    /** Throws {@code entity} away from the god, {@code strength} blocks a tick. */
    protected void throwBack(LivingEntity entity, double strength, double up) {
        Vec3 away = entity.position().subtract(position()).multiply(1.0, 0.0, 1.0);
        if (away.lengthSqr() < 1.0E-4) {
            away = new Vec3(1.0, 0.0, 0.0);
        }
        away = away.normalize().scale(strength);
        entity.push(away.x, up, away.z);
        entity.hurtMarked = true;
    }

    /** {@code count} servants of the god appear around it and turn on its foe. */
    protected <T extends Mob> void summon(ServerLevel server, EntityType<T> type, int count, @Nullable LivingEntity target) {
        for (int i = 0; i < count; i++) {
            T servant = type.create(server);
            if (servant == null) {
                continue;
            }
            double angle = i * Math.PI * 2.0 / count;
            servant.moveTo(getX() + Math.cos(angle) * 3.0, getY(), getZ() + Math.sin(angle) * 3.0, getYRot(), 0.0F);
            servant.finalizeSpawn(server, server.getCurrentDifficultyAt(servant.blockPosition()), MobSpawnType.MOB_SUMMONED, null);
            if (target != null) {
                servant.setTarget(target);
            }
            server.addFreshEntity(servant);
        }
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.EVOKER_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.EVOKER_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.EVOKER_DEATH;
    }
}
