package com.mythsofworlds.core;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.registry.MetalSet;
import java.util.IdentityHashMap;
import java.util.Map;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.AttackEntityEvent;
import org.joml.Vector3f;
import org.jetbrains.annotations.Nullable;

/**
 * How the weapons and tools of the myths are swung: the motion of the hand in first person (see GearClient) and the
 * trail a full-strength blow leaves in the air, coloured after the metal or the relic. The trail is sent from the
 * server, so every player nearby sees it. Neither changes damage, reach or speed.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public final class Strikes {
    /** The motion of a swing. */
    public enum Style { SLASH, STAB, CHOP, HEAVY, DIG }

    /** The motion and the colour of the trail of one item; extra is a particle mixed into the trail, if any. */
    public record Strike(Style style, int colour, @Nullable ParticleOptions extra) {
    }

    private static Map<Item, Strike> strikes;

    private Strikes() {
    }

    /** Every weapon and tool of the myths with its strike; built on first use, when the items exist. */
    public static Map<Item, Strike> all() {
        if (strikes == null) {
            Map<Item, Strike> map = new IdentityHashMap<>();
            metal(map, GreekContent.ORICHALCUM, 0xF0A848);
            metal(map, SlavicContent.BULAT, 0x9ED8FF);
            metal(map, NorseContent.DARK_IRON, 0x8C6CE0);
            map.put(GreekContent.HARPE.get(), new Strike(Style.SLASH, 0xF4D878, null));
            map.put(GreekContent.NEMEAN_CLAW_DAGGER.get(), new Strike(Style.STAB, 0xE0B060, null));
            map.put(GreekContent.BIDENT_OF_HADES.get(), new Strike(Style.STAB, 0x6A2CB0, ParticleTypes.SOUL));
            map.put(SlavicContent.KLADENETS.get(), new Strike(Style.SLASH, 0xC4F4FF, ParticleTypes.END_ROD));
            map.put(NorseContent.MJOLNIR.get(), new Strike(Style.HEAVY, 0x8CD0FF, ParticleTypes.ELECTRIC_SPARK));
            map.put(NorseContent.SURTR_SWORD.get(), new Strike(Style.SLASH, 0xFF6A20, ParticleTypes.FLAME));
            strikes = map;
        }
        return strikes;
    }

    private static void metal(Map<Item, Strike> map, MetalSet metal, int colour) {
        map.put(metal.sword.get(), new Strike(Style.SLASH, colour, null));
        map.put(metal.axe.get(), new Strike(Style.CHOP, colour, null));
        map.put(metal.pickaxe.get(), new Strike(Style.DIG, colour, null));
        map.put(metal.shovel.get(), new Strike(Style.DIG, colour, null));
        map.put(metal.hoe.get(), new Strike(Style.DIG, colour, null));
    }

    @Nullable
    public static Strike of(Item item) {
        return all().get(item);
    }

    @SubscribeEvent
    public static void onAttack(AttackEntityEvent event) {
        Player player = event.getEntity();
        Strike strike = of(player.getMainHandItem().getItem());
        if (strike == null || strike.style() == Style.DIG || !(player.level() instanceof ServerLevel level)
                || player.getAttackStrengthScale(0.5F) < 0.9F) {
            return;
        }
        trail(level, player, strike);
    }

    /** An arc of coloured dust in front of the attacker: across for a slash, down for a chop, straight for a thrust. */
    public static void trail(ServerLevel level, Player player, Strike strike) {
        int c = strike.colour();
        DustParticleOptions dust = new DustParticleOptions(new Vector3f((c >> 16 & 255) / 255F, (c >> 8 & 255) / 255F,
                (c & 255) / 255F), 1.1F);
        Vec3 eye = player.getEyePosition();
        float yaw = player.getYRot() * Mth.DEG_TO_RAD;
        Vec3 forward = Vec3.directionFromRotation(player.getXRot(), player.getYRot());
        Vec3 right = new Vec3(-Mth.cos(yaw), 0, -Mth.sin(yaw));
        Vec3 up = right.cross(forward).normalize();
        int steps = 11;
        for (int i = 0; i < steps; i++) {
            float t = i / (float) (steps - 1);
            Vec3 point = switch (strike.style()) {
                case SLASH -> {
                    float angle = (t - 0.5F) * 2.1F;
                    yield eye.add(forward.scale(1.6 * Mth.cos(angle))).add(right.scale(1.6 * Mth.sin(angle)))
                            .add(up.scale(0.45 - 0.9 * t));
                }
                case CHOP, HEAVY -> {
                    float angle = (0.5F - t) * 2.0F;
                    yield eye.add(forward.scale(1.5 * Mth.cos(angle))).add(up.scale(1.5 * Mth.sin(angle) - 0.2));
                }
                default -> eye.add(forward.scale(0.6 + 1.6 * t)).add(up.scale(-0.25));
            };
            level.sendParticles(dust, point.x, point.y, point.z, 1, 0.02, 0.02, 0.02, 0.0);
            if (strike.extra() != null && i % 3 == 1) {
                level.sendParticles(strike.extra(), point.x, point.y, point.z, 1, 0.05, 0.05, 0.05, 0.01);
            }
        }
        if (strike.style() == Style.HEAVY) {
            level.sendParticles(ParticleTypes.EXPLOSION, eye.x + forward.x * 1.8, eye.y + forward.y * 1.8 - 0.3,
                    eye.z + forward.z * 1.8, 1, 0, 0, 0, 0);
        }
    }
}
