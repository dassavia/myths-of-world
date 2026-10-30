package com.mythsofworlds.registry;

import com.mythsofworlds.MythsOfWorlds;
import java.util.EnumMap;
import java.util.List;
import net.minecraft.core.Holder;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.tags.TagKey;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.DiggerItem;
import net.minecraft.world.item.HoeItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.PickaxeItem;
import net.minecraft.world.item.ShovelItem;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.DropExperienceBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.neoforge.common.SimpleTier;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;

import static com.mythsofworlds.registry.ModRegistries.ARMOR_MATERIALS;
import static com.mythsofworlds.registry.ModRegistries.BLOCKS;
import static com.mythsofworlds.registry.ModRegistries.ITEMS;

/**
 * A metal of the myths and everything made of it: the ore (found in stone), the raw metal, the ingot and its block,
 * a sword, pickaxe, axe, shovel and hoe, and a full suit of armour. Recipes, loot, tags, models and textures are made
 * by tools/gen_metals.py; the armour is drawn from textures/models/armor/&lt;name&gt;_layer_1/2.png.
 */
public final class MetalSet {
    /**
     * How strong a metal is, compared with iron (250 uses, speed 6, +2 damage) and diamond (1561, 8, +3).
     * {@code incorrect} is the tag of blocks its pickaxe cannot mine, as for the vanilla tiers.
     */
    public record Stats(int uses, float speed, float damage, int enchantment, int[] armour, int armourDurability,
                        float toughness, float knockbackResistance, Holder<SoundEvent> equipSound,
                        TagKey<Block> incorrect) {
    }

    public final String name;
    public final DeferredBlock<DropExperienceBlock> ore;
    public final DeferredItem<BlockItem> oreItem;
    public final DeferredItem<Item> raw;
    public final DeferredItem<Item> ingot;
    public final DeferredBlock<Block> block;
    public final DeferredItem<BlockItem> blockItem;
    public final Tier tier;
    public final DeferredHolder<ArmorMaterial, ArmorMaterial> material;
    public final DeferredItem<SwordItem> sword;
    public final DeferredItem<PickaxeItem> pickaxe;
    public final DeferredItem<AxeItem> axe;
    public final DeferredItem<ShovelItem> shovel;
    public final DeferredItem<HoeItem> hoe;
    public final DeferredItem<ArmorItem> helmet;
    public final DeferredItem<ArmorItem> chestplate;
    public final DeferredItem<ArmorItem> leggings;
    public final DeferredItem<ArmorItem> boots;

    public MetalSet(String name, MapColor color, Stats stats) {
        this.name = name;
        ore = BLOCKS.registerBlock(name + "_ore", props -> new DropExperienceBlock(UniformInt.of(0, 2), props),
                BlockBehaviour.Properties.of().mapColor(MapColor.STONE).strength(3.5F, 3.0F).requiresCorrectToolForDrops());
        oreItem = ITEMS.registerSimpleBlockItem(ore);
        raw = ITEMS.registerSimpleItem("raw_" + name);
        ingot = ITEMS.registerSimpleItem(name + "_ingot");
        block = BLOCKS.registerSimpleBlock(name + "_block", BlockBehaviour.Properties.of().mapColor(color)
                .strength(5.0F, 6.0F).requiresCorrectToolForDrops().sound(SoundType.METAL));
        blockItem = ITEMS.registerSimpleBlockItem(block);
        tier = new SimpleTier(stats.incorrect(), stats.uses(), stats.speed(), stats.damage(),
                stats.enchantment(), () -> Ingredient.of(ingot.get()));
        material = ARMOR_MATERIALS.register(name, () -> {
            EnumMap<ArmorItem.Type, Integer> defense = new EnumMap<>(ArmorItem.Type.class);
            defense.put(ArmorItem.Type.HELMET, stats.armour()[0]);
            defense.put(ArmorItem.Type.CHESTPLATE, stats.armour()[1]);
            defense.put(ArmorItem.Type.LEGGINGS, stats.armour()[2]);
            defense.put(ArmorItem.Type.BOOTS, stats.armour()[3]);
            defense.put(ArmorItem.Type.BODY, stats.armour()[1]);
            return new ArmorMaterial(defense, stats.enchantment(), stats.equipSound(), () -> Ingredient.of(ingot.get()),
                    List.of(new ArmorMaterial.Layer(MythsOfWorlds.id(name))), stats.toughness(), stats.knockbackResistance());
        });
        sword = ITEMS.register(name + "_sword", () -> new SwordItem(tier,
                new Item.Properties().attributes(SwordItem.createAttributes(tier, 3, -2.4F))));
        pickaxe = ITEMS.register(name + "_pickaxe", () -> new PickaxeItem(tier,
                new Item.Properties().attributes(DiggerItem.createAttributes(tier, 1.0F, -2.8F))));
        axe = ITEMS.register(name + "_axe", () -> new AxeItem(tier,
                new Item.Properties().attributes(DiggerItem.createAttributes(tier, 5.0F, -3.0F))));
        shovel = ITEMS.register(name + "_shovel", () -> new ShovelItem(tier,
                new Item.Properties().attributes(DiggerItem.createAttributes(tier, 1.5F, -3.0F))));
        hoe = ITEMS.register(name + "_hoe", () -> new HoeItem(tier,
                new Item.Properties().attributes(DiggerItem.createAttributes(tier, -3.0F, 0.0F))));
        helmet = armour(ArmorItem.Type.HELMET, stats.armourDurability());
        chestplate = armour(ArmorItem.Type.CHESTPLATE, stats.armourDurability());
        leggings = armour(ArmorItem.Type.LEGGINGS, stats.armourDurability());
        boots = armour(ArmorItem.Type.BOOTS, stats.armourDurability());
    }

    private DeferredItem<ArmorItem> armour(ArmorItem.Type type, int durability) {
        return ITEMS.register(name + "_" + type.getName(), () -> new ArmorItem(material, type,
                new Item.Properties().durability(type.getDurability(durability))));
    }
}
