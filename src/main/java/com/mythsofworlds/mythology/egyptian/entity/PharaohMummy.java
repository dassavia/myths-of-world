package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.egyptian.EgyptianContent;
import com.mythsofworlds.mythology.egyptian.EgyptianEntities;
import com.mythsofworlds.mythology.egyptian.EgyptianSounds;
import com.mythsofworlds.mythology.greek.entity.GreekBoss;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.SpawnGroupData;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import org.jetbrains.annotations.Nullable;

/**
 * The mummy of the pharaoh, who wakes in his tomb in the Valley of the Kings: a half-boss. The curse of the tomb falls
 * on everyone who comes near: every few seconds those within {@link #CURSE_RANGE} blocks are slowed in their work and
 * starved. Below half health he calls his servants, mummies, up out of the sand. Like every mummy he fears fire,
 * which wounds him twice as much. He carries the khopesh.
 */
public class PharaohMummy extends GreekBoss {
    public static final double CURSE_RANGE = 12.0;

    private int curseCooldown = 80;
    private int summonCooldown = 60;

    public PharaohMummy(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.YELLOW, true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 220.0)
                .add(Attributes.ATTACK_DAMAGE, 9.0)
                .add(Attributes.MOVEMENT_SPEED, 0.27)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.6)
                .add(Attributes.FOLLOW_RANGE, 32.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

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

    /** The khopesh in his hand; the loot table gives it, not his hand. */
    private void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(EgyptianContent.KHOPESH.get()));
        setDropChance(EquipmentSlot.MAINHAND, 0.0F);
    }

    @Override
    public void tick() {
        super.tick();
        if (!level().isClientSide && tickCount == 1 && getMainHandItem().isEmpty()) {
            arm();
        }
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (source.is(DamageTypeTags.IS_FIRE)) {
            amount *= 2.0F;
        }
        return super.hurt(source, amount);
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0), this);
        }
        return hit;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (!(level() instanceof ServerLevel server) || getTarget() == null) {
            return;
        }
        if (--curseCooldown <= 0) {
            curseCooldown = enraged() ? 140 : 220;
            curse(server);
        }
        if (enraged() && --summonCooldown <= 0) {
            summonCooldown = 300;
            raiseServants(server);
        }
    }

    /** The curse of the tomb: Mining Fatigue and Hunger on everyone around. Returns how many were cursed. */
    public int curse(ServerLevel server) {
        int cursed = 0;
        for (Player player : server.getEntitiesOfClass(Player.class, getBoundingBox().inflate(CURSE_RANGE),
                p -> p.isAlive() && !p.isSpectator() && !p.isCreative())) {
            curse(player);
            cursed++;
        }
        server.sendParticles(ParticleTypes.SCULK_SOUL, getX(), getY(1.0), getZ(), 20, 1.5, 0.8, 1.5, 0.02);
        playSound(EgyptianSounds.PHARAOH_CURSE.get(), 2.0F, 1.0F);
        return cursed;
    }

    /** The curse falls on one player. */
    public void curse(Player player) {
        player.addEffect(new MobEffectInstance(MobEffects.DIG_SLOWDOWN, 300, 1), this);
        player.addEffect(new MobEffectInstance(MobEffects.HUNGER, 200, 1), this);
        player.displayClientMessage(Component.translatable("entity.mythsofworlds.pharaoh_mummy.curse"), true);
    }

    /** Two mummies climb out of the sand around him. */
    public void raiseServants(ServerLevel server) {
        for (int i = 0; i < 2; i++) {
            Mummy mummy = EgyptianEntities.MUMMY.get().create(server);
            if (mummy == null) {
                continue;
            }
            double angle = random.nextDouble() * Math.PI * 2.0;
            mummy.moveTo(getX() + Math.cos(angle) * 3.0, getY(), getZ() + Math.sin(angle) * 3.0, random.nextFloat() * 360.0F, 0.0F);
            mummy.finalizeSpawn(server, server.getCurrentDifficultyAt(mummy.blockPosition()), MobSpawnType.MOB_SUMMONED, null);
            mummy.setTarget(getTarget());
            server.addFreshEntity(mummy);
            server.sendParticles(ParticleTypes.POOF, mummy.getX(), mummy.getY(), mummy.getZ(), 15, 0.4, 0.2, 0.4, 0.02);
        }
        playSound(SoundEvents.HUSK_CONVERTED_TO_ZOMBIE, 1.5F, 0.6F);
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return EgyptianSounds.MUMMY_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.HUSK_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.HUSK_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.6F;
    }
}
