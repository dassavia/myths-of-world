package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.mythology.greek.GreekContent;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.NbtUtils;
import net.minecraft.nbt.StringTag;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;

/**
 * Hippolyta, queen of the Amazons, boss of Themiscyra. She attacks any stranger who enters her hall; her sisters join
 * in. Bring her down to a sixth of her health and she yields: she stops fighting and hands over her war girdle
 * (only once, to the first hero who defeats her).
 * <p>
 * She can be married too, but she is very particular. She listens only to someone who has defeated her, wants only
 * gifts worthy of a queen (trophies of the great monsters, ambrosia, enchanted golden apples, netherite, the heart
 * of the sea, the necklace of Harmonia), values a new kind of treasure twice as much as one she already has, and
 * scorns anything else. The duel itself is forgiven once she yields. She will not share her husband: a man
 * who is already married is turned away. A child with her asks for ambrosia, not every night is right, and she
 * rests three days between children; her daughters are princesses.
 */
public class Hippolyta extends Amazon {
    private static final int GIFT_POINTS = 20;
    private static final int REPEAT_POINTS = 10;

    private final ServerBossEvent bossEvent = new ServerBossEvent(getDisplayName(), BossEvent.BossBarColor.PURPLE,
            BossEvent.BossBarOverlay.PROGRESS);
    private final Set<UUID> worthy = new HashSet<>();
    private final Set<String> treasures = new HashSet<>();
    private boolean yielded;
    private boolean girdleGiven;

    public Hippolyta(EntityType<? extends AgeableMob> type, Level level) {
        super(type, level);
        this.xpReward = 80;
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Amazon.createAttributes()
                .add(Attributes.MAX_HEALTH, 220.0)
                .add(Attributes.ATTACK_DAMAGE, 11.0)
                .add(Attributes.MOVEMENT_SPEED, 0.34)
                .add(Attributes.ARMOR, 10.0)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.6)
                .add(Attributes.FOLLOW_RANGE, 32.0);
    }

    @Override
    public String textureName() {
        return "hippolyta";
    }

    /** The queen's name hangs over her head, always in English. */
    @Override
    protected Component getTypeName() {
        return Component.literal("Hippolyta");
    }

    @Override
    public boolean shouldShowName() {
        return true;
    }

    @Override
    protected void registerGoals() {
        super.registerGoals();
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, 10, true, false,
                target -> !yielded && !(target instanceof Player p && (p.isCreative() || isFamily(p)))));
    }

    @Override
    protected void initialize() {
        setVariant(ROYAL);
        arm();
    }

    @Override
    protected void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.GOLDEN_SWORD));
        setItemSlot(EquipmentSlot.OFFHAND, new ItemStack(Items.SHIELD));
        setDropChance(EquipmentSlot.MAINHAND, 0.0F);
        setDropChance(EquipmentSlot.OFFHAND, 0.0F);
    }

    @Override
    protected String messages() {
        return "entity.mythsofworlds.hippolyta.";
    }

    public boolean hasYielded() {
        return yielded;
    }

    public boolean isWorthy(Player player) {
        return worthy.contains(player.getUUID());
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (!level().isClientSide && !yielded && source.getEntity() instanceof Player player
                && getHealth() - amount < getMaxHealth() / 6.0F) {
            yieldTo(player);
            return false;
        }
        return super.hurt(source, amount);
    }

    /** The fight is over: she kneels, gives up her girdle and respects the victor. */
    public void yieldTo(Player player) {
        com.mythsofworlds.codex.Progress.awardAround(this, "kill.hippolyta");
        yielded = true;
        worthy.add(player.getUUID());
        // The blows of an honest duel are forgiven: courtship starts afresh.
        setAffection(player, Math.max(0, affection(player)));
        setHealth(getMaxHealth() / 2.0F);
        setTarget(null);
        setLastHurtByMob(null);
        for (Amazon sister : level().getEntitiesOfClass(Amazon.class, getBoundingBox().inflate(32.0))) {
            if (sister.getTarget() == player) {
                sister.setTarget(null);
                sister.setLastHurtByMob(null);
            }
        }
        if (!girdleGiven) {
            girdleGiven = true;
            spawnAtLocation(new ItemStack(GreekContent.GIRDLE_OF_HIPPOLYTA.get()));
        }
        particles(ParticleTypes.HAPPY_VILLAGER, 15);
        playSound(SoundEvents.PLAYER_LEVELUP, 1.0F, 0.7F);
        say(player, "yield");
        bossEvent.removeAllPlayers();
    }

    private static boolean worthyGift(ItemStack stack) {
        return stack.is(GreekContent.MINOTAUR_HORN.get()) || stack.is(GreekContent.HYDRA_SCALE.get())
                || stack.is(GreekContent.CERBERUS_FANG.get()) || stack.is(GreekContent.NEMEAN_PELT.get())
                || stack.is(GreekContent.CYCLOPS_EYE.get()) || stack.is(GreekContent.MEDUSA_HEAD.get())
                || stack.is(GreekContent.KARKINOS_CLAW.get()) || stack.is(GreekContent.AMBROSIA.get())
                || stack.is(Items.ENCHANTED_GOLDEN_APPLE) || stack.is(Items.NETHERITE_INGOT) || stack.is(Items.HEART_OF_THE_SEA);
    }

    @Override
    protected int giftPoints(Player player, ItemStack stack, Gift gift) {
        if (!isWorthy(player)) {
            say(player, "unworthy");
            return 0;
        }
        String key = BuiltInRegistries.ITEM.getKey(stack.getItem()).toString();
        if (!worthyGift(stack)) {
            setAffection(player, affection(player) - 5);
            particles(ParticleTypes.ANGRY_VILLAGER, 2);
            say(player, "scorn", affection(player), LOVE);
            return 0;
        }
        // A new kind of treasure delights her; another of a kind she already has still pleases her, a little less.
        int points = treasures.add(key) ? GIFT_POINTS : REPEAT_POINTS;
        say(player, points == GIFT_POINTS ? "gift" : "gift_again", affection(player) + points, LOVE);
        return points;
    }

    /** Worthy gifts are welcome even if they are not on the amazons' list (the Medusa head, netherite...). */
    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!level().isClientSide && gift(stack) == null && worthyGift(stack)) {
            Gift gift = new Gift(2, GIFT_POINTS);
            int before = affection(player);
            int points = giftPoints(player, stack, gift);
            if (points > 0) {
                setAffection(player, before + points);
                stack.consume(1, player);
                particles(ParticleTypes.HEART, 4);
                if (before < LOVE && affection(player) >= LOVE) {
                    say(player, "in_love");
                }
            }
            return InteractionResult.SUCCESS;
        }
        return super.mobInteract(player, hand);
    }

    @Override
    protected boolean acceptsNecklace(Player player) {
        return isWorthy(player);
    }

    @Override
    protected boolean canMarry(Player player) {
        return isWorthy(player);
    }

    @Override
    protected ItemStack childGift() {
        return new ItemStack(GreekContent.AMBROSIA.get());
    }

    @Override
    protected int childCooldownTicks() {
        return 3 * 24000;
    }

    @Override
    protected boolean wantsChild(Player player) {
        return random.nextBoolean();
    }

    @Override
    protected int childVariant() {
        return ROYAL;
    }

    @Override
    protected void talk(Player player) {
        if (!yielded) {
            say(player, "challenge");
        } else if (!isWorthy(player)) {
            say(player, "unworthy");
        } else if (bond() != Bond.WIFE) {
            say(player, "talk", affection(player), LOVE);
        } else {
            super.talk(player);
        }
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        bossEvent.setProgress(getHealth() / getMaxHealth());
    }

    @Override
    public void startSeenByPlayer(ServerPlayer player) {
        super.startSeenByPlayer(player);
        if (!yielded) {
            bossEvent.addPlayer(player);
        }
    }

    @Override
    public void stopSeenByPlayer(ServerPlayer player) {
        super.stopSeenByPlayer(player);
        bossEvent.removePlayer(player);
    }

    @Override
    public void setCustomName(Component name) {
        super.setCustomName(name);
        bossEvent.setName(getDisplayName());
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putBoolean("Yielded", yielded);
        tag.putBoolean("GirdleGiven", girdleGiven);
        ListTag worthyList = new ListTag();
        worthy.forEach(uuid -> worthyList.add(NbtUtils.createUUID(uuid)));
        tag.put("Worthy", worthyList);
        ListTag treasureList = new ListTag();
        treasures.forEach(item -> treasureList.add(StringTag.valueOf(item)));
        tag.put("Treasures", treasureList);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        yielded = tag.getBoolean("Yielded");
        girdleGiven = tag.getBoolean("GirdleGiven");
        worthy.clear();
        for (Tag element : tag.getList("Worthy", Tag.TAG_INT_ARRAY)) {
            worthy.add(NbtUtils.loadUUID(element));
        }
        treasures.clear();
        for (Tag element : tag.getList("Treasures", Tag.TAG_STRING)) {
            treasures.add(element.getAsString());
        }
    }

    /** Never despawns, and a queen is never a child. */
    @Override
    public boolean isBaby() {
        return false;
    }
}
