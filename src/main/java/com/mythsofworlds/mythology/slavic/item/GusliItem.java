package com.mythsofworlds.mythology.slavic.item;

import com.mythsofworlds.core.entity.BalancedBoss;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.mythology.slavic.SlavicSounds;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * Gusli-samogudy, the self-playing harp of the tales (Sadko played the Sea King's court into a dance that shook the
 * waves). Pluck them (right-click) and every monster within {@value #RANGE} blocks breaks into a dance for
 * {@value #DANCE_TICKS} ticks: it forgets its prey and hops in place. The great monsters of the myths are deaf to them.
 */
public class GusliItem extends Item {
    public static final double RANGE = 12.0;
    public static final int DANCE_TICKS = 160;
    public static final int COOLDOWN = 600;

    public GusliItem(Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!(level instanceof ServerLevel server)) {
            return InteractionResultHolder.success(stack);
        }
        int dancers = play(server, player);
        player.displayClientMessage(Component.translatable("item.mythsofworlds.gusli.played", dancers), true);
        player.getCooldowns().addCooldown(this, COOLDOWN);
        stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
        return InteractionResultHolder.success(stack);
    }

    /** Sets every monster around the player dancing; returns how many. */
    public static int play(ServerLevel level, Player player) {
        level.playSound(null, player.blockPosition(), SlavicSounds.GUSLI.get(), SoundSource.PLAYERS, 1.5F, 1.0F);
        level.sendParticles(ParticleTypes.NOTE, player.getX(), player.getY(1.2), player.getZ(), 12, 1.5, 0.5, 1.5, 1.0);
        List<Mob> dancers = level.getEntitiesOfClass(Mob.class, player.getBoundingBox().inflate(RANGE),
                mob -> mob instanceof Enemy && !(mob instanceof BalancedBoss) && mob.isAlive());
        for (Mob mob : dancers) {
            mob.addEffect(new MobEffectInstance(SlavicContent.DANCE, DANCE_TICKS, 0), player);
            level.sendParticles(ParticleTypes.NOTE, mob.getX(), mob.getY(1.1), mob.getZ(), 3, 0.3, 0.2, 0.3, 1.0);
        }
        return dancers.size();
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
