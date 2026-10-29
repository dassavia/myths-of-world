package com.mythsofworlds.core.family;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.mythology.greek.entity.Amazon;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.ChunkPos;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.portal.DimensionTransition;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

/**
 * The family whistle: blow it and your wives and daughters come to you at once, from anywhere in any world (an amazon
 * or valkyrie the registry of {@link FamilyRegistry} knows). A member whose chunk is not loaded is fetched by loading
 * it for a few seconds.
 */
@EventBusSubscriber(modid = MythsOfWorlds.MODID)
public class FamilyWhistleItem extends Item {
    private static final int COOLDOWN_TICKS = 100;
    private static final int SEARCH_TICKS = 200;

    /** A member being fetched from a chunk that had to be loaded. */
    private record Search(UUID member, UUID player, ServerLevel level, ChunkPos chunk, boolean forcedByUs, int[] ticks) {
    }

    private static final List<Search> SEARCHES = new ArrayList<>();

    public FamilyWhistleItem(Properties properties) {
        super(properties);
    }

    /** Calls the family of {@code player}; returns how many came at once (more may follow from far worlds). */
    public static int call(Player player) {
        MinecraftServer server = player.level().getServer();
        if (server == null) {
            return 0;
        }
        FamilyRegistry registry = FamilyRegistry.get(server);
        int came = 0;
        for (FamilyRegistry.Member member : registry.familyOf(player.getUUID())) {
            ServerLevel level = server.getLevel(member.dimension());
            if (level == null) {
                registry.remove(member.id());
                continue;
            }
            Entity entity = level.getEntity(member.id());
            if (entity != null) {
                if (bring(entity, player)) {
                    came++;
                }
                continue;
            }
            ChunkPos chunk = new ChunkPos(member.pos());
            boolean forced = !level.getForcedChunks().contains(chunk.toLong());
            if (forced) {
                level.setChunkForced(chunk.x, chunk.z, true);
            }
            SEARCHES.add(new Search(member.id(), player.getUUID(), level, chunk, forced, new int[] {0}));
        }
        return came;
    }

    /** Brings {@code entity} to {@code player} if it is still one of the family. */
    private static boolean bring(Entity entity, Player player) {
        ServerLevel here = (ServerLevel) player.level();
        if (!(entity instanceof Amazon amazon) || !amazon.isAlive() || !amazon.isFamily(player)) {
            FamilyRegistry.get(here.getServer()).remove(entity.getUUID());
            return false;
        }
        Entity arrived = amazon;
        if (amazon.level() == player.level()) {
            amazon.teleportTo(player.getX(), player.getY(), player.getZ());
        } else {
            arrived = amazon.changeDimension(new DimensionTransition(here, player.position(), Vec3.ZERO,
                    amazon.getYRot(), amazon.getXRot(), DimensionTransition.DO_NOTHING));
        }
        if (arrived instanceof Amazon wife) {
            wife.answerWhistle();
            FamilyRegistry.get(here.getServer()).update(wife, player.getUUID());
            here.sendParticles(ParticleTypes.PORTAL, wife.getX(), wife.getY() + 1.0, wife.getZ(), 30, 0.4, 0.8, 0.4, 0.2);
            return true;
        }
        return false;
    }

    @SubscribeEvent
    public static void onServerTick(ServerTickEvent.Post event) {
        Iterator<Search> searches = SEARCHES.iterator();
        while (searches.hasNext()) {
            Search search = searches.next();
            Entity entity = search.level().getEntity(search.member());
            ServerPlayer player = event.getServer().getPlayerList().getPlayer(search.player());
            boolean done = entity != null || player == null || ++search.ticks()[0] > SEARCH_TICKS;
            if (entity != null && player != null && bring(entity, player)) {
                player.displayClientMessage(Component.translatable("item.mythsofworlds.family_whistle.arrived",
                        entity.getDisplayName()).withStyle(ChatFormatting.LIGHT_PURPLE), false);
            }
            if (done) {
                if (search.forcedByUs()) {
                    search.level().setChunkForced(search.chunk().x, search.chunk().z, false);
                }
                searches.remove();
            }
        }
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        level.playSound(null, player.getX(), player.getY(), player.getZ(), SoundEvents.NOTE_BLOCK_FLUTE.value(), SoundSource.PLAYERS,
                2.0F, 1.8F);
        if (!level.isClientSide && level.getServer() != null) {
            int members = FamilyRegistry.get(level.getServer()).familyOf(player.getUUID()).size();
            call(player);
            player.displayClientMessage(Component.translatable(members == 0 ? "item.mythsofworlds.family_whistle.nobody"
                    : "item.mythsofworlds.family_whistle.called", members).withStyle(ChatFormatting.LIGHT_PURPLE), true);
            player.getCooldowns().addCooldown(this, COOLDOWN_TICKS);
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.mythsofworlds.family_whistle.desc").withStyle(ChatFormatting.GRAY));
    }
}
