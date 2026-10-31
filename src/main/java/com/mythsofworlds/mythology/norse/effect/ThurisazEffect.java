package com.mythsofworlds.mythology.norse.effect;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.norse.NorseContent;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;

/** Thurisaz, the thorn of the giants: whoever wounds you in close combat is pricked for {@value #THORNS} damage. */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public class ThurisazEffect extends MobEffect {
    public static final float THORNS = 3.0F;

    public ThurisazEffect() {
        super(MobEffectCategory.BENEFICIAL, 0x6EC8FF);
    }

    @SubscribeEvent
    public static void onDamaged(LivingDamageEvent.Post event) {
        LivingEntity victim = event.getEntity();
        if (victim.level().isClientSide || !victim.hasEffect(NorseContent.THURISAZ) || !event.getSource().isDirect()) {
            return;
        }
        if (event.getSource().getEntity() instanceof LivingEntity attacker && attacker != victim) {
            attacker.hurt(victim.damageSources().thorns(victim), THORNS);
        }
    }
}
