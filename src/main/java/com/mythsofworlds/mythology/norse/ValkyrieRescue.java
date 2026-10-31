package com.mythsofworlds.mythology.norse;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.mythology.norse.entity.Valkyrie;
import java.util.Optional;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingDeathEvent;

/**
 * The valkyries choose who falls in battle and who lives. A man wed to a valkyrie does not die while she is within
 * {@link Valkyrie#RESCUE_RANGE} blocks: at the deadly blow she swoops to his side and carries him out of the fight,
 * wounded but alive. Once a day.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class ValkyrieRescue {
    private ValkyrieRescue() {
    }

    @SubscribeEvent(priority = EventPriority.HIGH)
    public static void onDeath(LivingDeathEvent event) {
        if (event.isCanceled() || !(event.getEntity() instanceof ServerPlayer player)) {
            return;
        }
        Optional<UUID> wife = PlayerData.spouse(player);
        if (wife.isPresent() && player.serverLevel().getEntity(wife.get()) instanceof Valkyrie valkyrie && rescue(player, valkyrie)) {
            event.setCanceled(true);
        }
    }

    /** Carries the player out of battle if his valkyrie wife can; true if she did. */
    public static boolean rescue(ServerPlayer player, Valkyrie valkyrie) {
        ServerLevel level = player.serverLevel();
        long now = level.getGameTime();
        if (valkyrie.level() != level || valkyrie.distanceToSqr(player) > Valkyrie.RESCUE_RANGE * Valkyrie.RESCUE_RANGE
                || !valkyrie.canRescue(now) || !valkyrie.isFamily(player)) {
            return false;
        }
        valkyrie.markRescue(now);
        player.setHealth(6.0F);
        player.clearFire();
        player.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 200, 1));
        player.addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 100, 2));
        player.addEffect(new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 200, 0));
        valkyrie.teleportTo(player.getX() + 1.0, player.getY(), player.getZ());
        valkyrie.getNavigation().stop();
        level.sendParticles(ParticleTypes.END_ROD, player.getX(), player.getY(1.0), player.getZ(), 40, 0.6, 1.0, 0.6, 0.08);
        level.sendParticles(ParticleTypes.CLOUD, valkyrie.getX(), valkyrie.getY(0.5), valkyrie.getZ(), 20, 0.5, 0.5, 0.5, 0.05);
        level.playSound(null, player.blockPosition(), SoundEvents.TOTEM_USE, SoundSource.PLAYERS, 0.8F, 1.2F);
        player.displayClientMessage(Component.translatable("entity.mythsofworlds.valkyrie.rescue", valkyrie.getDisplayName())
                .withStyle(ChatFormatting.GOLD), false);
        return true;
    }
}
