package com.mythsofworlds.mythology.slavic.entity;

import com.mythsofworlds.mythology.norse.entity.Warg;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;

/** Volkolak, the werewolf: a sorcerer in the skin of a huge wolf. In the dusk of Nav he is stronger still. */
public class Volkolak extends Warg {
    public Volkolak(EntityType<? extends Monster> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Warg.createAttributes()
                .add(Attributes.MAX_HEALTH, 36.0)
                .add(Attributes.ATTACK_DAMAGE, 7.0)
                .add(Attributes.MOVEMENT_SPEED, 0.38)
                .add(Attributes.ARMOR, 2.0);
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (!level().isClientSide && tickCount % 100 == 0 && getTarget() != null) {
            addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, 120, 0, false, false));
        }
    }
}
