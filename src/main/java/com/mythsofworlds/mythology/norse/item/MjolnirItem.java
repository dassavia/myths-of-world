package com.mythsofworlds.mythology.norse.item;

import com.mythsofworlds.mythology.norse.NorseContent;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;
import org.jetbrains.annotations.Nullable;

/**
 * Thor's hammer: a heavy weapon, and right-click calls lightning down on the creature or block you point at
 * (up to {@link #RANGE} blocks away). Thrym, king of the frost giants, keeps it in Utgard. Thor was the bane of the
 * giants: the hammer strikes every giant and troll twice as hard, and Thrym, who stole it, three times.
 */
public class MjolnirItem extends SwordItem {
    public static final double RANGE = 40.0;
    public static final int COOLDOWN_TICKS = 50;

    public MjolnirItem(Properties properties) {
        super(com.mythsofworlds.mythology.norse.NorseContent.DARK_IRON.tier, properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel server) {
            Vec3 target = aim(player);
            strike(server, BlockPos.containing(target), player instanceof ServerPlayer sp ? sp : null);
            level.playSound(null, player.blockPosition(), SoundEvents.LIGHTNING_BOLT_THUNDER, SoundSource.PLAYERS, 0.8F, 1.4F);
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
            stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    /** The creature in the line of sight, else the block, else the farthest point of the range. */
    public static Vec3 aim(Player player) {
        Vec3 eye = player.getEyePosition();
        Vec3 end = eye.add(player.getViewVector(1.0F).scale(RANGE));
        HitResult block = player.level().clip(new ClipContext(eye, end, ClipContext.Block.OUTLINE, ClipContext.Fluid.NONE, player));
        Vec3 reach = block.getType() == HitResult.Type.MISS ? end : block.getLocation();
        EntityHitResult entity = ProjectileUtil.getEntityHitResult(player.level(), player, eye, reach,
                new AABB(eye, reach).inflate(1.0), e -> e instanceof LivingEntity && e.isAlive() && !e.isSpectator());
        return entity != null ? entity.getEntity().position() : reach;
    }

    /** A blow struck with Mjolnir in hand. */
    public static boolean struckWith(DamageSource source) {
        ItemStack weapon = source.isDirect() ? source.getWeaponItem() : null;
        return weapon != null && weapon.is(NorseContent.MJOLNIR.get());
    }

    public static void strike(ServerLevel level, BlockPos pos, ServerPlayer cause) {
        LightningBolt bolt = EntityType.LIGHTNING_BOLT.create(level);
        if (bolt != null) {
            bolt.moveTo(Vec3.atBottomCenterOf(pos));
            bolt.setCause(cause);
            level.addFreshEntity(bolt);
        }
        scorch(level, pos);
    }

    /** Where the hammer's lightning lands, sand melts into glass and grass and soil are charred black. */
    public static void scorch(ServerLevel level, BlockPos centre) {
        RandomSource random = level.getRandom();
        for (BlockPos pos : BlockPos.betweenClosed(centre.offset(-2, -2, -2), centre.offset(2, 1, 2))) {
            int dx = pos.getX() - centre.getX();
            int dz = pos.getZ() - centre.getZ();
            int distance = dx * dx + dz * dz;
            if (distance > 5 || distance > 2 && random.nextInt(3) == 0) {
                continue;
            }
            BlockState above = level.getBlockState(pos.above());
            if (!above.isAir() && !above.canBeReplaced()) {
                continue;
            }
            BlockState charred = charred(level.getBlockState(pos));
            if (charred != null) {
                level.setBlockAndUpdate(pos, charred);
            }
        }
    }

    @Nullable
    private static BlockState charred(BlockState state) {
        if (state.is(Blocks.SAND) || state.is(Blocks.SUSPICIOUS_SAND)) {
            return Blocks.GLASS.defaultBlockState();
        }
        if (state.is(Blocks.RED_SAND)) {
            return Blocks.ORANGE_STAINED_GLASS.defaultBlockState();
        }
        if (state.is(BlockTags.DIRT) || state.is(Blocks.DIRT_PATH) || state.is(Blocks.FARMLAND)) {
            return state.is(NorseContent.SCORCHED_EARTH.get()) ? null : NorseContent.SCORCHED_EARTH.get().defaultBlockState();
        }
        return null;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable(getDescriptionId() + ".desc").withStyle(ChatFormatting.GRAY));
    }
}
