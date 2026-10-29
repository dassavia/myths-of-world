package com.mythsofworlds.mythology.greek.entity;

import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.greek.GreekEntities;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.NbtUtils;
import net.minecraft.nbt.Tag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.AgeableMob;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.MoveTowardsRestrictionGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Creeper;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

/**
 * Amazon, warrior woman of Themiscyra. Neutral: fights monsters, and fights back (with her sisters) when attacked.
 * <p>
 * She can be courted. Gifts (flowers, gold and jewels, weapons and trophies, good food) raise her affection for the
 * giver, twice as much if it is what she likes best (ask her by right-clicking with an empty hand); one gift every
 * 20 seconds. Hurting her or her sisters costs a lot of it. At {@value #LOVE} affection, give her a wedding ring to
 * marry her: your wife follows you and fights at your side; shift + right-click switches her between following,
 * waiting on the spot and walking freely around where she is. Give your wife a cake and a daughter is born (once a
 * day); she grows up into an amazon loyal to your family. The necklace of Harmonia wins any amazon's heart at once.
 * <p>
 * Amazons keep near the camp or city they were found in ({@link #HOME_RADIUS} blocks); the horn of Themiscyra calls
 * strays back home.
 */
public class Amazon extends AgeableMob {
    /** Looks 0 to {@code VARIANTS - 1}; {@link #ROYAL} among them is the look of Hippolyta's daughters only. */
    public static final int VARIANTS = 16;
    public static final int ROYAL = 4;
    public static final int HOME_RADIUS = 32;
    private static final int WANDER_RADIUS = 16;
    public static final int LOVE = 100;
    private static final int MAX_AFFECTION = 150;
    private static final int GIFT_COOLDOWN = 400;
    private static final int GROW_UP_TICKS = 24000;

    public enum Bond { NONE, WIFE, DAUGHTER }

    /** What a wife or daughter does when not fighting: shift + right-click goes to the next one. */
    public enum Mode { FOLLOW, STAY, WANDER }

    /** What a gift is: 0 flowers, 1 gold and jewels, 2 weapons and trophies, 3 food. */
    public record Gift(int kind, int points) {
    }

    public static final int KINDS = 4;

    private static final String[] NAMES = {"Antiope", "Melanippe", "Penthesilea", "Otrere", "Aella", "Areto", "Alcippe",
            "Hippothoe", "Lampedo", "Marpesia", "Orithyia", "Clonie", "Polemusa", "Derinoe", "Antibrote", "Bremusa",
            "Thermodosa", "Andromache", "Philippis", "Prothoe", "Myrina", "Thalestris", "Lysippe", "Ainia", "Antianeira",
            "Asteria", "Celaeno", "Eurybe", "Phoebe", "Deianira", "Tecmessa", "Alcibie", "Evandre", "Glauke", "Harmothoe",
            "Hippomache", "Iphito", "Molpadia", "Pantariste", "Toxaris", "Xanthippe", "Euryale", "Okyale", "Pisto",
            "Laomache", "Thraso", "Iodoke", "Kreousa", "Gortyessa", "Hippolyte", "Antandre", "Elaia", "Kleite"};
    private static final EntityDataAccessor<Integer> DATA_VARIANT = SynchedEntityData.defineId(Amazon.class, EntityDataSerializers.INT);

    private final Map<UUID, Integer> affection = new HashMap<>();
    private Bond bond = Bond.NONE;
    @Nullable
    private UUID family;
    private int favourite;
    private int giftCooldown;
    private int childCooldown;
    private Mode mode = Mode.FOLLOW;
    @Nullable
    private BlockPos home;
    private boolean initialized;
    // A duel with another amazon over a husband: not saved, the fight simply ends if the world unloads.
    @Nullable
    private Amazon rival;
    @Nullable
    private Player duelFor;
    private int duelTicks;
    private static final int DUEL_TICKS = 1200;
    private static final double DUEL_RANGE = 48.0;

    public Amazon(EntityType<? extends AgeableMob> type, Level level) {
        super(type, level);
        setPersistenceRequired();
    }

    public static AttributeSupplier.Builder createAttributes() {
        return AgeableMob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 30.0)
                .add(Attributes.ATTACK_DAMAGE, 5.0)
                .add(Attributes.MOVEMENT_SPEED, 0.32)
                .add(Attributes.ARMOR, 4.0)
                .add(Attributes.FOLLOW_RANGE, 24.0);
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
        super.defineSynchedData(builder);
        builder.define(DATA_VARIANT, 0);
    }

    public int getVariant() {
        return entityData.get(DATA_VARIANT);
    }

    public void setVariant(int variant) {
        entityData.set(DATA_VARIANT, variant);
    }

    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.15, true));
        goalSelector.addGoal(4, new FollowFamilyGoal());
        goalSelector.addGoal(5, new MoveTowardsRestrictionGoal(this, 1.0));
        goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 0.7) {
            @Override
            public boolean canUse() {
                return mode != Mode.STAY && super.canUse();
            }
        });
        goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 8.0F));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this).setAlertOthers());
        targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(this, Monster.class, 10, true, false,
                target -> !(target instanceof Creeper) && !isBaby()));
    }

    // ---- Who she is ----

    /** Looks, name, taste and weapons, chosen the first time she ticks (also for amazons placed by structures). */
    protected void initialize() {
        if (getVariant() == 0) {
            setVariant(randomVariant());
        }
        setCustomName(Component.literal(randomName()));
        favourite = random.nextInt(KINDS);
        if (!isBaby()) {
            arm();
        }
    }

    protected void arm() {
        setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(random.nextInt(10) < 7 ? Items.IRON_SWORD : Items.IRON_AXE));
        if (random.nextInt(10) < 4) {
            setItemSlot(EquipmentSlot.OFFHAND, new ItemStack(Items.SHIELD));
        }
        setDropChance(EquipmentSlot.MAINHAND, 0.0F);
        setDropChance(EquipmentSlot.OFFHAND, 0.0F);
    }

    public Bond bond() {
        return bond;
    }

    public boolean isFamily(Player player) {
        return family != null && family.equals(player.getUUID());
    }

    public int affection(Player player) {
        return affection.getOrDefault(player.getUUID(), 0);
    }

    public void setAffection(Player player, int value) {
        affection.put(player.getUUID(), Math.max(-100, Math.min(MAX_AFFECTION, value)));
    }

    protected String messages() {
        return "entity.mythsofworlds.amazon.";
    }

    /** Her texture, textures/entity/&lt;name&gt;.png. */
    public String textureName() {
        return "amazon_" + Math.floorMod(getVariant(), VARIANTS);
    }

    protected String randomName() {
        return NAMES[random.nextInt(NAMES.length)];
    }

    protected int randomVariant() {
        return commonVariant(random);
    }

    /** A new daughter of her kind. */
    @Nullable
    protected Amazon newChild() {
        return GreekEntities.AMAZON.get().create(level());
    }

    /** What a gift is worth to her people, or null if it is no gift. */
    @Nullable
    protected Gift giftFor(ItemStack stack) {
        return gift(stack);
    }

    protected void say(Player player, String key, Object... args) {
        Object[] withName = new Object[args.length + 1];
        withName[0] = getDisplayName();
        System.arraycopy(args, 0, withName, 1, args.length);
        player.displayClientMessage(Component.translatable(messages() + key, withName).withStyle(ChatFormatting.LIGHT_PURPLE), false);
    }

    protected void particles(ParticleOptions particle, int count) {
        if (level() instanceof ServerLevel server) {
            server.sendParticles(particle, getX(), getEyeY() + 0.4, getZ(), count, 0.4, 0.3, 0.4, 0.0);
        }
    }

    // ---- Courtship ----

    /** How much a gift is worth to amazons, or null if it is no gift. */
    @Nullable
    public static Gift gift(ItemStack stack) {
        if (stack.is(ItemTags.FLOWERS)) {
            return new Gift(0, 6);
        }
        if (stack.is(Items.GOLD_BLOCK)) {
            return new Gift(1, 40);
        }
        if (stack.is(Items.DIAMOND)) {
            return new Gift(1, 20);
        }
        if (stack.is(Items.GOLD_INGOT)) {
            return new Gift(1, 10);
        }
        if (stack.is(Items.EMERALD)) {
            return new Gift(1, 8);
        }
        if (stack.is(Items.AMETHYST_SHARD) || stack.is(Items.GOLD_NUGGET)) {
            return new Gift(1, 3);
        }
        if (stack.is(GreekContent.MINOTAUR_HORN.get()) || stack.is(GreekContent.HYDRA_SCALE.get())
                || stack.is(GreekContent.CERBERUS_FANG.get()) || stack.is(GreekContent.NEMEAN_PELT.get())
                || stack.is(GreekContent.CYCLOPS_EYE.get()) || stack.is(GreekContent.KARKINOS_CLAW.get())) {
            return new Gift(2, 20);
        }
        if (stack.is(ItemTags.SWORDS) || stack.is(ItemTags.AXES) || stack.is(Items.BOW) || stack.is(Items.CROSSBOW)
                || stack.is(Items.TRIDENT) || stack.is(Items.SHIELD)) {
            return new Gift(2, 12);
        }
        if (stack.is(GreekContent.HARPY_FEATHER.get())) {
            return new Gift(2, 4);
        }
        if (stack.is(GreekContent.AMBROSIA.get())) {
            return new Gift(3, 25);
        }
        if (stack.is(Items.GOLDEN_APPLE)) {
            return new Gift(3, 20);
        }
        if (stack.is(Items.HONEY_BOTTLE) || stack.is(GreekContent.POMEGRANATE.get())) {
            return new Gift(3, 8);
        }
        if (stack.is(GreekContent.OLIVES.get()) || stack.is(Items.BREAD) || stack.is(Items.COOKIE) || stack.is(Items.COOKED_MUTTON)
                || stack.is(Items.COOKED_BEEF) || stack.is(Items.SWEET_BERRIES)) {
            return new Gift(3, 4);
        }
        return null;
    }

    /** Affection a gift earns from this amazon; 0 or less means she refuses it (and it is not used up). */
    protected int giftPoints(Player player, ItemStack stack, Gift gift) {
        if (gift.kind() == favourite) {
            say(player, "gift_favourite", affection(player) + gift.points() * 2, LOVE);
            return gift.points() * 2;
        }
        say(player, "gift", affection(player) + gift.points(), LOVE);
        return gift.points();
    }

    /** Whether this amazon would marry the player at all, once she loves them. */
    protected boolean canMarry(Player player) {
        return true;
    }

    protected ItemStack childGift() {
        return new ItemStack(Items.CAKE);
    }

    protected int childCooldownTicks() {
        return 24000;
    }

    /** Whether she agrees to a child today. */
    protected boolean wantsChild(Player player) {
        return true;
    }

    protected int childVariant() {
        return random.nextBoolean() && getVariant() != ROYAL ? getVariant() : commonVariant(random);
    }

    /** Any look but the royal one. */
    public static int commonVariant(net.minecraft.util.RandomSource random) {
        int variant = random.nextInt(VARIANTS - 1);
        return variant >= ROYAL ? variant + 1 : variant;
    }

    public Mode mode() {
        return mode;
    }

    @Nullable
    public BlockPos home() {
        return home;
    }

    /** Where she keeps to when she is free: her camp, or the spot her husband left her to wander. */
    public void setHome(@Nullable BlockPos pos, int radius) {
        home = pos;
        if (pos == null) {
            clearRestriction();
        } else {
            restrictTo(pos, radius);
        }
    }

    /** Called by the horn of Themiscyra: walk back home, or come at once if far away. */
    public boolean callHome() {
        if (home == null || family != null || isBaby()) {
            return false;
        }
        setTarget(null);
        if (distanceToSqr(home.getX() + 0.5, home.getY(), home.getZ() + 0.5) > 48 * 48) {
            particles(ParticleTypes.CLOUD, 10);
            teleportTo(home.getX() + 0.5, home.getY(), home.getZ() + 0.5);
            getNavigation().stop();
        } else {
            getNavigation().moveTo(home.getX() + 0.5, home.getY(), home.getZ() + 0.5, 1.2);
        }
        return true;
    }

    /** Whether the necklace of Harmonia wins her heart (Hippolyta listens only to her victor). */
    protected boolean acceptsNecklace(Player player) {
        return true;
    }

    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        if (level().isClientSide) {
            return InteractionResult.SUCCESS;
        }
        ItemStack stack = player.getItemInHand(hand);
        if (isBaby()) {
            say(player, isFamily(player) ? "daughter" : "child");
            return InteractionResult.SUCCESS;
        }
        if (getTarget() == player) {
            say(player, "angry");
            particles(ParticleTypes.ANGRY_VILLAGER, 3);
            return InteractionResult.SUCCESS;
        }
        if (isFamily(player) && player.isShiftKeyDown()) {
            setMode(Mode.values()[(mode.ordinal() + 1) % Mode.values().length]);
            getNavigation().stop();
            say(player, mode.name().toLowerCase(java.util.Locale.ROOT));
            return InteractionResult.SUCCESS;
        }
        if (stack.is(GreekContent.NECKLACE_OF_HARMONIA.get())) {
            if (!acceptsNecklace(player)) {
                say(player, "unworthy");
            } else if (affection(player) >= LOVE) {
                say(player, "necklace_already");
            } else {
                setAffection(player, Math.max(affection(player), 0) + LOVE);
                stack.consume(1, player);
                particles(ParticleTypes.HEART, 20);
                playSound(SoundEvents.AMETHYST_BLOCK_RESONATE, 1.0F, 1.2F);
                say(player, "necklace");
            }
            return InteractionResult.SUCCESS;
        }
        if (stack.is(GreekContent.WEDDING_RING.get())) {
            marry(player, stack);
            return InteractionResult.SUCCESS;
        }
        if (bond == Bond.WIFE && isFamily(player) && stack.is(childGift().getItem())) {
            haveChild(player, stack);
            return InteractionResult.SUCCESS;
        }
        Gift gift = giftFor(stack);
        if (gift != null) {
            if (giftCooldown > 0) {
                say(player, "busy");
                return InteractionResult.SUCCESS;
            }
            int before = affection(player);
            int points = giftPoints(player, stack, gift);
            if (points > 0) {
                setAffection(player, before + points);
                stack.consume(1, player);
                giftCooldown = GIFT_COOLDOWN;
                particles(ParticleTypes.HEART, Math.max(1, points / 5));
                playSound(SoundEvents.AMETHYST_BLOCK_CHIME, 1.0F, 1.2F);
                if (before < LOVE && affection(player) >= LOVE && bond == Bond.NONE) {
                    say(player, "in_love");
                }
            }
            return InteractionResult.SUCCESS;
        }
        talk(player);
        return InteractionResult.SUCCESS;
    }

    protected void talk(Player player) {
        if (bond == Bond.WIFE && isFamily(player)) {
            say(player, "wife");
        } else if (bond == Bond.DAUGHTER && isFamily(player)) {
            say(player, "grown_daughter");
        } else {
            say(player, "talk", Component.translatable(messages() + "likes." + favourite), affection(player), LOVE);
        }
    }

    private void marry(Player player, ItemStack ring) {
        if (bond == Bond.DAUGHTER && isFamily(player)) {
            say(player, "is_daughter");
        } else if (bond == Bond.WIFE) {
            say(player, isFamily(player) ? "already_yours" : "taken");
        } else if (!canMarry(player)) {
            say(player, "unworthy");
        } else if (affection(player) < LOVE) {
            say(player, "not_yet", affection(player), LOVE);
        } else if (PlayerData.spouse(player).isPresent()) {
            challenge(player);
        } else {
            ring.consume(1, player);
            wed(player);
            say(player, "married");
        }
    }

    private void wed(Player player) {
        bond = Bond.WIFE;
        family = player.getUUID();
        setMode(Mode.FOLLOW);
        PlayerData.setSpouse(player, Optional.of(getUUID()));
        particles(ParticleTypes.HEART, 20);
        playSound(SoundEvents.PLAYER_LEVELUP, 1.0F, 1.0F);
    }

    // ---- Rivals: a second proposal makes her fight the wife for the husband ----

    @Nullable
    public Amazon rival() {
        return rival;
    }

    private void challenge(Player player) {
        if (rival != null) {
            return;
        }
        UUID wifeId = PlayerData.spouse(player).orElseThrow();
        Amazon wife = null;
        if (level() instanceof ServerLevel server && server.getEntity(wifeId) instanceof Amazon found && found.isAlive()
                && found.distanceToSqr(this) < DUEL_RANGE * DUEL_RANGE) {
            wife = found;
        }
        if (wife == null || wife.rival != null) {
            say(player, "rival_far");
            return;
        }
        rival = wife;
        wife.rival = this;
        duelFor = player;
        wife.duelFor = player;
        duelTicks = DUEL_TICKS;
        wife.duelTicks = DUEL_TICKS;
        setTarget(wife);
        wife.setTarget(this);
        particles(ParticleTypes.ANGRY_VILLAGER, 6);
        wife.particles(ParticleTypes.ANGRY_VILLAGER, 6);
        say(player, "rivals", wife.getDisplayName());
    }

    private void endDuel() {
        rival = null;
        duelFor = null;
        duelTicks = 0;
        setTarget(null);
        setLastHurtByMob(null);
    }

    /** Beaten by her rival: she lowers her weapon, and the winner keeps (or takes) the husband. */
    private void loseDuel() {
        Amazon winner = rival;
        Player husband = duelFor;
        endDuel();
        if (winner != null) {
            winner.endDuel();
        }
        particles(ParticleTypes.SMOKE, 10);
        if (husband == null || winner == null) {
            return;
        }
        say(husband, "rival_yields", winner.getDisplayName());
        if (bond == Bond.WIFE && isFamily(husband)) {
            bond = Bond.NONE;
            family = null;
            mode = Mode.FOLLOW;
            setHome(blockPosition(), HOME_RADIUS);
            setAffection(husband, LOVE / 2);
            PlayerData.setSpouse(husband, Optional.empty());
            winner.wed(husband);
            winner.say(husband, "rival_won");
        } else {
            setAffection(husband, LOVE / 2);
            winner.say(husband, "rival_kept");
        }
    }

    private void haveChild(Player player, ItemStack gift) {
        if (childCooldown > 0) {
            say(player, "tired");
            return;
        }
        if (!wantsChild(player)) {
            childCooldown = 1200;
            say(player, "not_tonight");
            return;
        }
        Amazon child = newChild();
        if (child == null) {
            return;
        }
        child.moveTo(getX(), getY(), getZ(), getYRot(), 0.0F);
        child.setAge(-GROW_UP_TICKS);
        child.setVariant(childVariant());
        child.initialized = true;
        child.setCustomName(Component.literal(randomName()));
        child.favourite = random.nextInt(KINDS);
        child.bond = Bond.DAUGHTER;
        child.family = player.getUUID();
        level().addFreshEntity(child);
        gift.consume(1, player);
        childCooldown = childCooldownTicks();
        particles(ParticleTypes.HEART, 12);
        playSound(SoundEvents.PLAYER_LEVELUP, 1.0F, 1.5F);
        say(player, "daughter_born", child.getDisplayName());
    }

    private void setMode(Mode next) {
        mode = next;
        // Following ignores any home; waiting or wandering keeps her around the spot where she was told to.
        setHome(next == Mode.FOLLOW ? null : blockPosition(), next == Mode.STAY ? 2 : WANDER_RADIUS);
    }

    // ---- Life ----

    @Override
    public void tick() {
        super.tick();
        if (!level().isClientSide && !initialized) {
            initialized = true;
            initialize();
            if (family == null) {
                setHome(blockPosition(), HOME_RADIUS);
            }
        }
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        if (giftCooldown > 0) {
            giftCooldown--;
        }
        if (childCooldown > 0) {
            childCooldown--;
        }
        if (rival != null) {
            if (!rival.isAlive() || rival.rival != this || --duelTicks <= 0 || distanceToSqr(rival) > DUEL_RANGE * DUEL_RANGE) {
                if (rival.rival == this) {
                    rival.endDuel();
                }
                endDuel();
            } else if (getTarget() != rival) {
                setTarget(rival);
            }
            return;
        }
        // Defend the family: go for whatever hurts them or whatever they fight.
        if (family != null && tickCount % 10 == 0 && !isBaby()) {
            Player owner = level().getPlayerByUUID(family);
            if (owner != null && distanceToSqr(owner) < 32 * 32) {
                LivingEntity enemy = owner.getLastHurtByMob();
                if (enemy == null || !enemy.isAlive()) {
                    enemy = owner.getLastHurtMob();
                }
                if (enemy != null && enemy.isAlive() && enemy != this && !(enemy instanceof Player)
                        && !(enemy instanceof Amazon sister && sister.family != null && sister.family.equals(family))) {
                    setTarget(enemy);
                }
            }
        }
    }

    @Override
    protected void ageBoundaryReached() {
        super.ageBoundaryReached();
        if (!level().isClientSide && !isBaby() && getMainHandItem().isEmpty()) {
            arm();
        }
    }

    @Override
    public void setTarget(@Nullable LivingEntity target) {
        if (target instanceof Player player && isFamily(player)) {
            return;
        }
        // A duel is between the two of them: no one else joins in, and they fight nothing else meanwhile.
        if (rival != null ? target != null && target != rival : target instanceof Amazon other && other.rival != null) {
            return;
        }
        super.setTarget(target);
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (!level().isClientSide && rival != null && source.getEntity() == rival && getHealth() - amount < getMaxHealth() * 0.3F) {
            loseDuel();
            return false;
        }
        boolean hurt = super.hurt(source, amount);
        if (hurt && !level().isClientSide && source.getEntity() instanceof Player player && !isFamily(player)) {
            setAffection(player, affection(player) - 40);
        }
        return hurt;
    }

    @Override
    public void die(DamageSource source) {
        if (!level().isClientSide && bond == Bond.WIFE && family != null && level().getServer() != null) {
            Player husband = level().getServer().getPlayerList().getPlayer(family);
            if (husband != null) {
                PlayerData.setSpouse(husband, Optional.empty());
                husband.displayClientMessage(Component.translatable(messages() + "died", getDisplayName())
                        .withStyle(ChatFormatting.DARK_RED), false);
            }
        }
        super.die(source);
    }

    @Nullable
    @Override
    public AgeableMob getBreedOffspring(ServerLevel level, AgeableMob partner) {
        return null;
    }

    @Override
    public boolean removeWhenFarAway(double distanceToClosestPlayer) {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return null;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.PLAYER_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.PLAYER_DEATH;
    }

    @Override
    public float getVoicePitch() {
        return isBaby() ? 1.8F : 1.35F;
    }

    // ---- Saving ----

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("Variant", getVariant());
        tag.putString("Bond", bond.name());
        if (family != null) {
            tag.putUUID("Family", family);
        }
        tag.putInt("Favourite", favourite);
        tag.putInt("GiftCooldown", giftCooldown);
        tag.putInt("ChildCooldown", childCooldown);
        tag.putString("Mode", mode.name());
        if (home != null) {
            tag.put("Home", NbtUtils.writeBlockPos(home));
        }
        tag.putBoolean("Initialized", initialized);
        ListTag list = new ListTag();
        affection.forEach((uuid, value) -> {
            CompoundTag entry = new CompoundTag();
            entry.putUUID("Player", uuid);
            entry.putInt("Value", value);
            list.add(entry);
        });
        tag.put("Affection", list);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        setVariant(tag.getInt("Variant"));
        try {
            bond = Bond.valueOf(tag.getString("Bond"));
        } catch (IllegalArgumentException e) {
            bond = Bond.NONE;
        }
        family = tag.hasUUID("Family") ? tag.getUUID("Family") : null;
        favourite = tag.getInt("Favourite");
        giftCooldown = tag.getInt("GiftCooldown");
        childCooldown = tag.getInt("ChildCooldown");
        try {
            mode = tag.contains("Mode") ? Mode.valueOf(tag.getString("Mode")) : tag.getBoolean("Staying") ? Mode.STAY : Mode.FOLLOW;
        } catch (IllegalArgumentException e) {
            mode = Mode.FOLLOW;
        }
        BlockPos savedHome = NbtUtils.readBlockPos(tag, "Home").orElse(null);
        setHome(savedHome, family == null ? HOME_RADIUS : mode == Mode.STAY ? 2 : WANDER_RADIUS);
        initialized = tag.getBoolean("Initialized");
        affection.clear();
        for (Tag element : tag.getList("Affection", Tag.TAG_COMPOUND)) {
            CompoundTag entry = (CompoundTag) element;
            affection.put(entry.getUUID("Player"), entry.getInt("Value"));
        }
    }

    /** Walks after her husband (or father) unless told to stay; catches up by teleporting if left far behind. */
    private class FollowFamilyGoal extends Goal {
        @Nullable
        private Player owner;

        FollowFamilyGoal() {
            setFlags(EnumSet.of(Flag.MOVE, Flag.LOOK));
        }

        @Override
        public boolean canUse() {
            if (family == null || mode != Mode.FOLLOW || getTarget() != null) {
                return false;
            }
            owner = level().getPlayerByUUID(family);
            return owner != null && !owner.isSpectator() && distanceToSqr(owner) > 36.0;
        }

        @Override
        public boolean canContinueToUse() {
            return owner != null && owner.isAlive() && mode == Mode.FOLLOW && getTarget() == null && distanceToSqr(owner) > 9.0;
        }

        @Override
        public void tick() {
            if (owner == null) {
                return;
            }
            getLookControl().setLookAt(owner, 10.0F, getMaxHeadXRot());
            if (distanceToSqr(owner) > 24 * 24 && owner.onGround()) {
                teleportTo(owner.getX(), owner.getY(), owner.getZ());
                getNavigation().stop();
            } else {
                getNavigation().moveTo(owner, 1.1);
            }
        }

        @Override
        public void stop() {
            owner = null;
            getNavigation().stop();
        }
    }
}
