package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.MythsOfWorlds;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.TagKey;
import net.minecraft.util.RandomSource;
import net.minecraft.world.Difficulty;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
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
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;

/**
 * Giant scorpion of the desert, sacred to the goddess Serket. Its sting is a strong poison and leaves you weak; its
 * armoured shell turns light blows.
 */
public class Scorpion extends Monster {
    public Scorpion(EntityType<? extends Monster> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 26.0)
                .add(Attributes.ATTACK_DAMAGE, 4.0)
                .add(Attributes.ARMOR, 6.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.FOLLOW_RANGE, 24.0)
                .add(Attributes.STEP_HEIGHT, 1.0);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.15, false));
        goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 0.7));
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this));
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.POISON, 100, 1), this);
            living.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0), this);
        }
        return hit;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.SPIDER_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.SPIDER_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.SPIDER_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return super.getVoicePitch() * 0.7F;
    }

    /** Desert-type biomes, the only ones scorpions spawn in (data/mythsofworlds/tags/worldgen/biome/spawns/scorpion.json). */
    public static final TagKey<Biome> SPAWN_BIOMES = TagKey.create(Registries.BIOME, MythsOfWorlds.id("spawns/scorpion"));
    /** What scorpions spawn on: sand and terracotta (data/mythsofworlds/tags/block/scorpion_spawnable_on.json). */
    public static final TagKey<Block> SPAWNS_ON = TagKey.create(Registries.BLOCK, MythsOfWorlds.id("scorpion_spawnable_on"));
    /** In daylight only one spot in this many lets a scorpion out: they come mostly at night and in the dark. */
    public static final int DAYLIGHT_CHANCE = 10;

    /**
     * Natural spawning: never in peaceful, only in a desert-type biome on sand or terracotta, and mostly at night or in
     * the dark. Spawners, eggs and commands only need solid ground.
     */
    public static boolean checkScorpionSpawnRules(EntityType<Scorpion> type, ServerLevelAccessor level, MobSpawnType spawnType,
                                                  BlockPos pos, RandomSource random) {
        if (level.getDifficulty() == Difficulty.PEACEFUL) {
            return false;
        }
        if (!(spawnType == MobSpawnType.NATURAL || spawnType == MobSpawnType.CHUNK_GENERATION)) {
            return checkMobSpawnRules(type, level, spawnType, pos, random);
        }
        return canSpawnAt(level.getBiome(pos), level.getBlockState(pos.below()))
                && (Monster.isDarkEnoughToSpawn(level, pos, random) || random.nextInt(DAYLIGHT_CHANCE) == 0);
    }

    /** The biome and the ground a scorpion needs, whatever the light. */
    public static boolean canSpawnAt(Holder<Biome> biome, BlockState ground) {
        return biome.is(SPAWN_BIOMES) && ground.is(SPAWNS_ON);
    }
}
