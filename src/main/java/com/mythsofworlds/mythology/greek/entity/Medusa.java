package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekSounds;
import com.mythsofworlds.mythology.greek.item.MedusaHeadItem;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ShieldItem;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Medusa the Gorgon, mini-boss of the coast. Looking at her slows you down, and after 3 seconds of eye
 * contact you start turning to stone (heavy damage). Like Perseus with his mirrored shield, a player
 * holding a shield is safe from the gaze. Her snake hair poisons on every bite. The harpe, the sickle-sword
 * Perseus beheaded her with, deals her double damage.
 */
public class Medusa extends GreekBoss {
    private static final double GAZE_RANGE = 24.0;
    /** Ticks of eye contact before the gaze starts to hurt. */
    private static final int PETRIFY_AFTER = 60;

    private final Map<UUID, Integer> gazeTicks = new HashMap<>();

    public Medusa(EntityType<? extends Monster> type, Level level) {
        super(type, level, BossEvent.BossBarColor.YELLOW, true);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 150.0)
                .add(Attributes.ATTACK_DAMAGE, 7.0)
                .add(Attributes.MOVEMENT_SPEED, 0.27)
                .add(Attributes.ARMOR, 4.0)
                .add(Attributes.FOLLOW_RANGE, 32.0);
    }

    /** Same test the Enderman uses, a little more forgiving. */
    public boolean isLookedAtBy(Player player) {
        Vec3 view = player.getViewVector(1.0F).normalize();
        Vec3 toMe = new Vec3(getX() - player.getX(), getEyeY() - player.getEyeY(), getZ() - player.getZ());
        double distance = toMe.length();
        return view.dot(toMe.normalize()) > 1.0 - 0.08 / distance && player.hasLineOfSight(this);
    }

    public static boolean isShielded(Player player) {
        return player.getMainHandItem().getItem() instanceof ShieldItem
                || player.getOffhandItem().getItem() instanceof ShieldItem;
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (source.isDirect() && source.getEntity() instanceof LivingEntity attacker
                && attacker.getMainHandItem().is(GreekContent.HARPE.get())) {
            amount *= 2.0F;
        }
        return super.hurt(source, amount);
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (tickCount % 5 != 0) {
            return;
        }
        for (Player player : level().getEntitiesOfClass(Player.class, getBoundingBox().inflate(GAZE_RANGE),
                p -> !p.isCreative() && !p.isSpectator())) {
            if (isShielded(player) || !isLookedAtBy(player)) {
                gazeTicks.remove(player.getUUID());
                continue;
            }
            int ticks = gazeTicks.merge(player.getUUID(), 5, Integer::sum);
            player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 2));
            if (ticks == PETRIFY_AFTER) {
                playSound(GreekSounds.MEDUSA_GAZE.get(), 1.5F, 1.0F);
                player.displayClientMessage(Component.translatable("entity.mythsofworlds.medusa.petrify"), true);
            }
            if (ticks >= PETRIFY_AFTER) {
                MedusaHeadItem.petrify(player);
                player.hurt(damageSources().indirectMagic(this, this), 4.0F);
            }
        }
    }

    @Override
    public boolean doHurtTarget(Entity target) {
        boolean hit = super.doHurtTarget(target);
        if (hit && target instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.POISON, 100, 1), this);
        }
        return hit;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return GreekSounds.MEDUSA_AMBIENT.get();
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return GreekSounds.MEDUSA_HURT.get();
    }

    @Override
    protected SoundEvent getDeathSound() {
        return GreekSounds.MEDUSA_DEATH.get();
    }
}
