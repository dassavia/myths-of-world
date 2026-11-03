package com.mythsofworlds.mythology.egyptian.entity;

import com.mythsofworlds.mythology.norse.entity.Warg;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.Level;

/**
 * Jackal of Anubis, a black desert dog with golden eyes that guards the ways of the dead. Lean and fast, it hunts in
 * packs like the wargs of the North: hurt one and the whole pack turns on you.
 */
public class Jackal extends Warg {
    public Jackal(EntityType<? extends Monster> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Warg.createAttributes()
                .add(Attributes.MAX_HEALTH, 22.0)
                .add(Attributes.ATTACK_DAMAGE, 5.0)
                .add(Attributes.MOVEMENT_SPEED, 0.4);
    }

    @Override
    public float getVoicePitch() {
        return super.getVoicePitch() * 1.5F;
    }
}
