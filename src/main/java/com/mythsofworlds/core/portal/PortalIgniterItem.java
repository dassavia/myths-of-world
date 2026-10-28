package com.mythsofworlds.core.portal;

import java.util.List;
import java.util.function.Supplier;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;

/**
 * A "flint and steel" for mythology portals: right-click the inside of a closed frame to open the portal.
 * One igniter can open several portal types; it tries them in order.
 * The tooltip comes from the lang key {@code <item description id>.desc}.
 */
public class PortalIgniterItem extends Item {
    private final List<Supplier<? extends MythPortalBlock>> portals;
    private final Supplier<SoundEvent> igniteSound;

    public PortalIgniterItem(Properties properties, Supplier<SoundEvent> igniteSound,
                             List<Supplier<? extends MythPortalBlock>> portals) {
        super(properties);
        this.igniteSound = igniteSound;
        this.portals = portals;
    }

    @Override
    public InteractionResult useOn(UseOnContext context) {
        Level level = context.getLevel();
        BlockPos target = context.getClickedPos().relative(context.getClickedFace());
        if (level.isClientSide) {
            // The server does the real work; the client only swings the arm.
            return InteractionResult.SUCCESS;
        }
        for (Supplier<? extends MythPortalBlock> portal : portals) {
            if (PortalShape.tryLight(level, target, portal.get())) {
                level.playSound(null, target, igniteSound.get(), SoundSource.BLOCKS, 1.0F, 0.8F);
                if (context.getPlayer() != null) {
                    context.getItemInHand().hurtAndBreak(1, context.getPlayer(),
                            LivingEntity.getSlotForHand(context.getHand()));
                }
                return InteractionResult.CONSUME;
            }
        }
        return InteractionResult.PASS;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
