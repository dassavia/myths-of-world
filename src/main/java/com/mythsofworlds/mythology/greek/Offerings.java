package com.mythsofworlds.mythology.greek;

import com.mythsofworlds.core.PlayerData;
import java.util.List;
import java.util.Optional;
import java.util.function.Predicate;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

/**
 * Offerings to the Olympians. Hold a gift over a lit brazier and right-click: the god it pleases burns it and blesses
 * you for {@value #BLESSING_TICKS} ticks. The gods hear one offering in {@value #COOLDOWN} ticks.
 * <ul>
 *   <li>Zeus, king of the gods: a gold ingot; strength and endurance.</li>
 *   <li>Athena, giver of the olive tree: olives; luck and knowledge (experience).</li>
 *   <li>Hermes, the winged messenger: a feather; speed and a light step.</li>
 *   <li>Poseidon, lord of the sea: a fish; breath under water and the grace of dolphins.</li>
 *   <li>Demeter, goddess of the harvest: wheat or bread; a full belly and healing.</li>
 *   <li>Hephaestus, the smith: coal of Hephaestus; fire cannot burn you, and your hands work fast.</li>
 * </ul>
 */
public final class Offerings {
    public static final int BLESSING_TICKS = 20 * 60 * 5;
    public static final int COOLDOWN = 20 * 60 * 3;

    /** A god, the gifts that please them and their blessing. */
    public record God(String id, Predicate<ItemStack> gift, List<Blessing> blessings, int experience) {
    }

    public record Blessing(Holder<MobEffect> effect, int amplifier) {
    }

    public static final List<God> GODS = List.of(
            new God("zeus", s -> s.is(Items.GOLD_INGOT),
                    List.of(new Blessing(MobEffects.DAMAGE_BOOST, 0), new Blessing(MobEffects.DAMAGE_RESISTANCE, 0)), 0),
            new God("athena", s -> s.is(GreekContent.OLIVES.get()), List.of(new Blessing(MobEffects.LUCK, 1)), 40),
            new God("hermes", s -> s.is(Items.FEATHER) || s.is(GreekContent.HARPY_FEATHER.get()),
                    List.of(new Blessing(MobEffects.MOVEMENT_SPEED, 1), new Blessing(MobEffects.JUMP, 1)), 0),
            new God("poseidon", s -> s.is(ItemTags.FISHES),
                    List.of(new Blessing(MobEffects.WATER_BREATHING, 0), new Blessing(MobEffects.DOLPHINS_GRACE, 0)), 0),
            new God("demeter", s -> s.is(Items.WHEAT) || s.is(Items.BREAD),
                    List.of(new Blessing(MobEffects.SATURATION, 0), new Blessing(MobEffects.REGENERATION, 0)), 0),
            new God("hephaestus", s -> s.is(GreekContent.HEPHAESTUS_COAL.get()),
                    List.of(new Blessing(MobEffects.FIRE_RESISTANCE, 0), new Blessing(MobEffects.DIG_SPEED, 1)), 0));

    private Offerings() {
    }

    /** The god this gift would please, if any. */
    public static Optional<God> godOf(ItemStack stack) {
        return GODS.stream().filter(god -> god.gift().test(stack)).findFirst();
    }

    /**
     * Burns the gift on the brazier at {@code pos} and blesses the player.
     *
     * @return false if the gods will not hear the player yet (nothing is used up)
     */
    public static boolean offer(ServerLevel level, BlockPos pos, Player player, ItemStack stack, God god) {
        long now = level.getGameTime();
        long last = player.getData(PlayerData.LAST_OFFERING);
        if (last > 0 && now - last < COOLDOWN && !player.isCreative()) {
            player.displayClientMessage(Component.translatable("offering.mythsofworlds.wait"), true);
            return false;
        }
        player.setData(PlayerData.LAST_OFFERING, now);
        stack.consume(1, player);
        for (Blessing blessing : god.blessings()) {
            // Saturation is instant: a whole feast at once, not five minutes of it.
            int ticks = blessing.effect() == MobEffects.SATURATION ? 10 : BLESSING_TICKS;
            player.addEffect(new MobEffectInstance(blessing.effect(), ticks, blessing.amplifier()));
        }
        if (god.experience() > 0) {
            player.giveExperiencePoints(god.experience());
        }
        level.sendParticles(ParticleTypes.FLAME, pos.getX() + 0.5, pos.getY() + 0.9, pos.getZ() + 0.5, 25, 0.2, 0.3, 0.2, 0.05);
        level.sendParticles(ParticleTypes.END_ROD, pos.getX() + 0.5, pos.getY() + 1.2, pos.getZ() + 0.5, 12, 0.3, 0.6, 0.3, 0.05);
        level.playSound(null, pos, GreekSounds.PORTAL_IGNITE.get(), SoundSource.BLOCKS, 1.0F, 1.2F);
        level.playSound(null, pos, SoundEvents.AMETHYST_BLOCK_CHIME, SoundSource.BLOCKS, 1.0F, 0.8F);
        player.displayClientMessage(Component.translatable("offering.mythsofworlds." + god.id()).withStyle(ChatFormatting.GOLD), false);
        return true;
    }
}
