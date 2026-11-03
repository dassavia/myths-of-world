package com.mythsofworlds.mythology.egyptian.item;

import com.mythsofworlds.mythology.egyptian.EgyptianSounds;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.OwnableEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;

/**
 * The was-sceptre of Set, lord of the desert and of storms. Raise it (right-click) and a sandstorm bursts around you:
 * every foe within {@link #RADIUS} blocks is thrown back, blinded and slowed. Players, pets and your family are
 * spared. Once every {@link #COOLDOWN_TICKS} ticks.
 */
public class WasSceptreItem extends Item {
    public static final double RADIUS = 8.0;
    public static final int COOLDOWN_TICKS = 200;

    public WasSceptreItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel server) {
            int struck = sandstorm(server, player);
            server.playSound(null, player.blockPosition(), EgyptianSounds.SANDSTORM.get(), SoundSource.PLAYERS, 1.5F, 1.0F);
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
            if (struck > 0) {
                stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
            }
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    /** Throws back every foe around {@code player}; returns how many were caught. */
    public static int sandstorm(ServerLevel level, Player player) {
        int struck = 0;
        for (LivingEntity foe : level.getEntitiesOfClass(LivingEntity.class, player.getBoundingBox().inflate(RADIUS),
                e -> e != player && e.isAlive() && !(e instanceof Player)
                        && !(e instanceof OwnableEntity pet && pet.getOwnerUUID() != null)
                        && !(e instanceof Amazon amazon && amazon.isFamily(player)))) {
            Vec3 away = foe.position().subtract(player.position()).multiply(1.0, 0.0, 1.0);
            if (away.lengthSqr() < 1.0E-4) {
                away = new Vec3(1.0, 0.0, 0.0);
            }
            away = away.normalize().scale(1.8);
            foe.push(away.x, 0.5, away.z);
            foe.hurtMarked = true;
            foe.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 100, 0), player);
            foe.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 100, 1), player);
            struck++;
        }
        level.sendParticles(new BlockParticleOption(ParticleTypes.BLOCK, Blocks.SAND.defaultBlockState()),
                player.getX(), player.getY(0.5), player.getZ(), 120, RADIUS * 0.5, 1.0, RADIUS * 0.5, 0.2);
        level.sendParticles(ParticleTypes.CLOUD, player.getX(), player.getY(0.5), player.getZ(), 30, 3.0, 0.8, 3.0, 0.1);
        return struck;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
