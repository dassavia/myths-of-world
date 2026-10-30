package com.mythsofworlds.mythology.slavic.item;

import com.mythsofworlds.core.family.WarriorMaiden;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.OwnableEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;

/**
 * Kladenets, the sword-of-itself (меч-кладенец) of the bogatyrs. Every blow also strikes every foe around the one hit,
 * within {@link #REACH} blocks, for {@link #SPLASH} damage; it never touches players, pets or the wielder's family.
 */
public class KladenetsItem extends SwordItem {
    public static final double REACH = 3.0;
    public static final float SPLASH = 6.0F;

    public KladenetsItem(Tier tier, Properties properties) {
        super(tier, properties);
    }

    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        if (attacker.level() instanceof ServerLevel server) {
            DamageSource source = attacker instanceof Player player ? attacker.damageSources().playerAttack(player)
                    : attacker.damageSources().mobAttack(attacker);
            for (LivingEntity other : server.getEntitiesOfClass(LivingEntity.class, target.getBoundingBox().inflate(REACH),
                    e -> e != target && e != attacker && e.isAlive() && !(e instanceof Player)
                            && !(e instanceof OwnableEntity pet && pet.getOwnerUUID() != null)
                            && !(e instanceof WarriorMaiden && attacker instanceof Player player && ((WarriorMaiden) e).isFamily(player)))) {
                other.hurt(source, SPLASH);
            }
            server.sendParticles(ParticleTypes.SWEEP_ATTACK, target.getX(), target.getY(0.5), target.getZ(), 3, 1.0, 0.2, 1.0, 0.0);
        }
        return super.hurtEnemy(stack, target, attacker);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
