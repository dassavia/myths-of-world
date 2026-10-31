package com.mythsofworlds.mythology.norse.item;

import com.mythsofworlds.mythology.norse.NorseContent;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/**
 * A rune of the Elder Futhark cut into a runestone, which Odin won hanging nine nights on the World Tree. Speak it
 * (right-click) and its power is yours for {@value #TICKS} ticks; the stone crumbles. One rune a minute: the runes
 * share their rest.
 */
public class RuneItem extends Item {
    public static final int TICKS = 20 * 60 * 3;
    public static final int COOLDOWN = 20 * 60;

    /** The six runes and what each one gives. */
    public enum Rune {
        /** Cattle, wealth: luck. */
        FEHU,
        /** The aurochs, wild strength: strength and health. */
        URUZ,
        /** The thorn of the giants (thurs): whoever strikes you is pricked in return. */
        THURISAZ,
        /** The god's word, Odin's rune: sight in the dark, and the creatures around are shown. */
        ANSUZ,
        /** The ride, the journey: speed and long leaps. */
        RAIDHO,
        /** The elk-sedge, protection: resistance and a shield of absorption. */
        ALGIZ;

        public String id() {
            return name().toLowerCase(java.util.Locale.ROOT);
        }
    }

    private final Rune rune;

    public RuneItem(Rune rune, Properties properties) {
        super(properties);
        this.rune = rune;
    }

    public Rune rune() {
        return rune;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!(level instanceof ServerLevel server)) {
            return InteractionResultHolder.success(stack);
        }
        speak(server, player, rune);
        for (var runeItem : NorseContent.RUNES.values()) {
            player.getCooldowns().addCooldown(runeItem.get(), COOLDOWN);
        }
        stack.consume(1, player);
        return InteractionResultHolder.consume(stack);
    }

    /** Gives the player the power of the rune. */
    public static void speak(ServerLevel level, Player player, Rune rune) {
        switch (rune) {
            case FEHU -> player.addEffect(new MobEffectInstance(MobEffects.LUCK, TICKS, 1));
            case URUZ -> {
                player.addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, TICKS, 0));
                player.addEffect(new MobEffectInstance(MobEffects.HEALTH_BOOST, TICKS, 1));
            }
            case THURISAZ -> player.addEffect(new MobEffectInstance(NorseContent.THURISAZ, TICKS, 0));
            case ANSUZ -> {
                player.addEffect(new MobEffectInstance(MobEffects.NIGHT_VISION, TICKS, 0));
                for (Mob mob : level.getEntitiesOfClass(Mob.class, player.getBoundingBox().inflate(32.0))) {
                    mob.addEffect(new MobEffectInstance(MobEffects.GLOWING, 20 * 30, 0, true, false));
                }
            }
            case RAIDHO -> {
                player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, TICKS, 1));
                player.addEffect(new MobEffectInstance(MobEffects.JUMP, TICKS, 1));
            }
            case ALGIZ -> {
                player.addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, TICKS, 1));
                player.addEffect(new MobEffectInstance(MobEffects.ABSORPTION, TICKS, 1));
            }
        }
        level.sendParticles(ParticleTypes.ENCHANT, player.getX(), player.getY(1.0), player.getZ(), 40, 0.5, 0.8, 0.5, 1.0);
        level.playSound(null, player.blockPosition(), SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.PLAYERS, 1.2F, 0.7F);
        player.displayClientMessage(Component.translatable("item.mythsofworlds.rune_" + rune.id() + ".spoken")
                .withStyle(ChatFormatting.AQUA), true);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
