package com.mythsofworlds.mythology.slavic.entity;

import com.mythsofworlds.core.entity.MythBoss;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.mythology.slavic.SlavicEntities;
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
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.ServerLevelAccessor;
import org.jetbrains.annotations.Nullable;

/**
 * Koschei the Deathless, the bony sorcerer-king in his black castle. He cannot die: struck down, he rises again with
 * all his strength, unless his killer carries the needle with his death (from the egg on the old oak). Then he dies,
 * and the needle breaks. His touch withers; below half health he raises upyri from the earth to fight for him.
 */
public class Koschei extends MythBoss {
    public static final int SUMMON_COOLDOWN = 300;

    private int summonCooldown = 100;

    public Koschei(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.PURPLE, false);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 550.0)
                .add(Attributes.ATTACK_DAMAGE, 13.0)
                .add(Attributes.MOVEMENT_SPEED, 0.3)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.8)
                .add(Attributes.FOLLOW_RANGE, 40.0)
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

    /** A black sword and a golden crown, neither of them dropped. */
    private void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.NETHERITE_SWORD));
        setItemSlot(EquipmentSlot.HEAD, new ItemStack(Items.GOLDEN_HELMET));
        for (EquipmentSlot slot : EquipmentSlot.values()) {
            setDropChance(slot, 0.0F);
        }
    }

    @Override
    public void tick() {
        super.tick();
        if (!level().isClientSide && tickCount == 1 && getMainHandItem().isEmpty()) {
            arm();
        }
        if (level().isClientSide && random.nextInt(4) == 0) {
            level().addParticle(ParticleTypes.SOUL, getRandomX(0.6), getRandomY(), getRandomZ(0.6), 0.0, 0.03, 0.0);
        }
    }

    /** The needle with his death, if the one who struck him carries it. */
    public static ItemStack needleOf(DamageSource source) {
        if (source.getEntity() instanceof Player player) {
            for (ItemStack stack : player.getInventory().items) {
                if (stack.is(SlavicContent.KOSCHEI_NEEDLE.get())) {
                    return stack;
                }
            }
            for (ItemStack stack : player.getInventory().offhand) {
                if (stack.is(SlavicContent.KOSCHEI_NEEDLE.get())) {
                    return stack;
                }
            }
        }
        return ItemStack.EMPTY;
    }

    @Override
    protected void actuallyHurt(DamageSource source, float amount) {
        super.actuallyHurt(source, amount);
        if (!isDeadOrDying() || source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) {
            return;
        }
        ItemStack needle = needleOf(source);
        if (!needle.isEmpty()) {
            needle.shrink(1);
            playSound(SoundEvents.GLASS_BREAK, 1.5F, 0.6F);
            if (source.getEntity() instanceof Player player) {
                player.displayClientMessage(Component.translatable("entity.mythsofworlds.koschei.needle_broken"), false);
            }
            return;
        }
        rise(source);
    }

    /** Back on his feet with full health: there is no death for Koschei. */
    public void rise(DamageSource source) {
        setHealth(getMaxHealth());
        playSound(SoundEvents.WITHER_SPAWN, 1.5F, 1.2F);
        if (level() instanceof ServerLevel server) {
            server.sendParticles(ParticleTypes.SOUL_FIRE_FLAME, getX(), getY(1.0), getZ(), 40, 0.5, 1.0, 0.5, 0.05);
        }
        if (source.getEntity() instanceof Player player) {
            player.displayClientMessage(Component.translatable("entity.mythsofworlds.koschei.deathless"), false);
        }
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.WITHER, 100, 1), this);
        }
        return hit;
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (getTarget() != null && enraged() && --summonCooldown <= 0 && level() instanceof ServerLevel server) {
            summonCooldown = SUMMON_COOLDOWN;
            raiseUpyri(server);
        }
    }

    /** Two upyri climb out of the ground around him. */
    public void raiseUpyri(ServerLevel server) {
        for (int i = 0; i < 2; i++) {
            Upyr upyr = SlavicEntities.UPYR.get().create(server);
            if (upyr == null) {
                continue;
            }
            double angle = random.nextDouble() * Math.PI * 2.0;
            upyr.moveTo(getX() + Math.cos(angle) * 3.0, getY(), getZ() + Math.sin(angle) * 3.0, random.nextFloat() * 360.0F, 0.0F);
            upyr.finalizeSpawn(server, server.getCurrentDifficultyAt(upyr.blockPosition()), MobSpawnType.MOB_SUMMONED, null);
            upyr.setTarget(getTarget());
            server.addFreshEntity(upyr);
            server.sendParticles(ParticleTypes.SOUL, upyr.getX(), upyr.getY(), upyr.getZ(), 15, 0.4, 0.2, 0.4, 0.02);
        }
        playSound(SoundEvents.EVOKER_PREPARE_SUMMON, 1.5F, 0.8F);
        playSpecial();
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.WITHER_SKELETON_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.WITHER_SKELETON_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.WITHER_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return 0.7F;
    }
}
