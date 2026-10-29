package com.mythsofworlds.mythology.greek.item;

import com.mythsofworlds.mythology.greek.entity.Cerberus;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/**
 * The bident of Hades, lord of the dead and master of Cerberus. Lost in the fortresses and bastions of the Nether.
 * Point it at Cerberus (right-click) or strike him with it, and the hound is called back to the underworld at once:
 * he falls with all his loot. The bident goes back to its master too, so it works only once.
 */
public class BidentOfHadesItem extends Item {
    public BidentOfHadesItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResult interactLivingEntity(ItemStack stack, Player player, LivingEntity target, InteractionHand hand) {
        if (!(target instanceof Cerberus cerberus) || !cerberus.isAlive()) {
            return InteractionResult.PASS;
        }
        if (!player.level().isClientSide) {
            banish(player.getItemInHand(hand), player, cerberus);
        }
        return InteractionResult.sidedSuccess(player.level().isClientSide);
    }

    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        if (target instanceof Cerberus cerberus && cerberus.isAlive() && attacker instanceof Player player) {
            banish(stack, player, cerberus);
        }
        return true;
    }

    /** Cerberus dies as if slain by the player (so he drops his loot), and the bident is gone. */
    public static void banish(ItemStack stack, Player player, Cerberus cerberus) {
        if (cerberus.level() instanceof ServerLevel server) {
            server.sendParticles(ParticleTypes.SOUL_FIRE_FLAME, cerberus.getX(), cerberus.getY(1.0), cerberus.getZ(), 60, 1.0, 1.0, 1.0, 0.05);
            server.sendParticles(ParticleTypes.SOUL, cerberus.getX(), cerberus.getY(0.5), cerberus.getZ(), 40, 1.2, 0.8, 1.2, 0.02);
        }
        cerberus.playSound(SoundEvents.WITHER_DEATH, 1.5F, 0.6F);
        cerberus.setLastHurtByPlayer(player);
        cerberus.setHealth(1.0F);
        cerberus.hurt(player.damageSources().playerAttack(player), Float.MAX_VALUE);
        if (cerberus.isAlive()) {
            cerberus.kill();
        }
        player.displayClientMessage(Component.translatable("item.mythsofworlds.bident_of_hades.banished")
                .withStyle(ChatFormatting.DARK_PURPLE), true);
        stack.consume(1, player);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
