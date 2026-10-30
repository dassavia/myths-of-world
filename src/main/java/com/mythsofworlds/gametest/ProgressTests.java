package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.codex.Codex;
import com.mythsofworlds.codex.Progress;
import com.mythsofworlds.core.PlayerData;
import com.mythsofworlds.journal.Journal;
import com.mythsofworlds.mythology.greek.GreekContent;
import com.mythsofworlds.mythology.norse.NorseContent;
import com.mythsofworlds.mythology.relic.MythAttributes;
import com.mythsofworlds.mythology.relic.MythPowers;
import com.mythsofworlds.mythology.slavic.SlavicContent;
import com.mythsofworlds.registry.MetalSet;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.GameType;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** The hero's path: the chapters of the Codex, the keys of the portals, the tiers of gear and the armour powers. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class ProgressTests {
    /** Every chapter shows a volume that loads, its icons are items, and what opens it is a step of another chapter. */
    @GameTest(template = "empty")
    public static void codexChaptersAreSound(GameTestHelper helper) {
        Set<String> steps = new HashSet<>();
        for (Codex.Chapter chapter : Codex.chapters()) {
            helper.assertTrue(!Journal.volume(chapter.volume()).isEmpty(), "volume " + chapter.volume() + " is empty");
            helper.assertTrue(BuiltInRegistries.ITEM.containsKey(chapter.icon()), "unknown icon " + chapter.icon());
            for (Codex.Step step : chapter.steps()) {
                helper.assertTrue(BuiltInRegistries.ITEM.containsKey(step.icon()), "unknown icon " + step.icon());
                steps.add(step.milestone());
                if (step.milestone().startsWith("kill.")) {
                    helper.assertTrue(Progress.BOSSES.contains(step.milestone().substring(5))
                            || step.milestone().equals("kill.hippolyta"), step.milestone() + " is never earned");
                }
            }
        }
        for (Codex.Chapter chapter : Codex.chapters()) {
            for (String need : chapter.requires()) {
                helper.assertTrue(steps.contains(need), chapter.id() + " needs " + need + ", which no chapter shows");
            }
        }
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        Set<String> none = Set.of();
        helper.assertTrue(Progress.has(player, none, Codex.chapter("hellas").requires()), "Hellas is open from the start");
        helper.assertTrue(!Progress.has(player, none, Codex.chapter("nav").requires()), "Nav waits for the Minotaur");
        helper.assertTrue(!Progress.has(player, Set.of("kill.cerberus"), Codex.chapter("jotunheim").requires()),
                "Jotunheim needs Zmey Gorynych too");
        helper.assertTrue(Progress.has(player, Set.of("kill.cerberus", "kill.zmey_gorynych"), Codex.chapter("jotunheim").requires()),
                "Cerberus and Zmey Gorynych open Jotunheim");
        helper.assertTrue(PlayerData.addMilestone(player, "kill.minotaur") && !PlayerData.addMilestone(player, "kill.minotaur"),
                "a milestone is earned once");
        helper.succeed();
    }

    /** The acorn of the World Tree needs the Minotaur's horn, the rune igniter a fang of Cerberus and a scale of Zmey. */
    @GameTest(template = "empty")
    public static void portalsNeedTrophies(GameTestHelper helper) {
        var recipes = helper.getLevel().getRecipeManager();
        assertNeeds(helper, recipes, "world_tree_acorn", List.of(GreekContent.MINOTAUR_HORN.get()));
        assertNeeds(helper, recipes, "rune_igniter", List.of(GreekContent.CERBERUS_FANG.get(), SlavicContent.ZMEY_SCALE.get()));
        helper.succeed();
    }

    private static void assertNeeds(GameTestHelper helper, net.minecraft.world.item.crafting.RecipeManager recipes, String name,
                                    List<Item> trophies) {
        var recipe = recipes.byKey(MythsOfWorlds.id(name)).orElseThrow();
        for (Item trophy : trophies) {
            boolean found = false;
            for (Ingredient ingredient : recipe.value().getIngredients()) {
                found |= ingredient.test(new ItemStack(trophy));
            }
            helper.assertTrue(found, name + " should need " + trophy);
        }
    }

    /** Each metal of the path is stronger than the one before: orichalcum, bulat, dark iron. */
    @GameTest(template = "empty")
    public static void gearTiersRise(GameTestHelper helper) {
        List<MetalSet> path = List.of(GreekContent.ORICHALCUM, SlavicContent.BULAT, NorseContent.DARK_IRON);
        for (int i = 1; i < path.size(); i++) {
            MetalSet before = path.get(i - 1);
            MetalSet after = path.get(i);
            helper.assertTrue(after.tier.getUses() > before.tier.getUses(), after.name + " should last longer than " + before.name);
            helper.assertTrue(after.tier.getAttackDamageBonus() > before.tier.getAttackDamageBonus(),
                    after.name + " should hit harder than " + before.name);
            helper.assertTrue(after.material.value().toughness() > before.material.value().toughness(),
                    after.name + " armour should be tougher than " + before.name);
            helper.assertTrue(after.material.value().getDefense(ArmorItem.Type.CHESTPLATE)
                    >= before.material.value().getDefense(ArmorItem.Type.CHESTPLATE), after.name + " chestplate is weaker");
        }
        helper.assertTrue(MythPowers.of(GreekContent.ORICHALCUM.chestplate.get()).get(MythAttributes.REFLECTION.value()) > 0,
                "orichalcum armour reflects");
        helper.succeed();
    }

    /** Reflection strikes the attacker back; lifesteal heals the one who strikes. */
    @GameTest(template = "empty")
    public static void armourPowersWork(GameTestHelper helper) {
        Player player = helper.makeMockPlayer(GameType.SURVIVAL);
        Player rival = helper.makeMockPlayer(GameType.SURVIVAL);
        Zombie zombie = helper.spawnWithNoFreeWill(EntityType.ZOMBIE, 1, 2, 1);
        player.getAttribute(MythAttributes.REFLECTION).addTransientModifier(new AttributeModifier(
                MythsOfWorlds.id("test_reflection"), 0.5, AttributeModifier.Operation.ADD_VALUE));
        float rivalHealth = rival.getHealth();
        player.hurt(helper.getLevel().damageSources().playerAttack(rival), 8.0F);
        helper.assertTrue(rival.getHealth() < rivalHealth, "reflection should wound the one who struck");

        player.getAttribute(MythAttributes.LIFESTEAL).addTransientModifier(new AttributeModifier(
                MythsOfWorlds.id("test_lifesteal"), 0.5, AttributeModifier.Operation.ADD_VALUE));
        player.setHealth(6.0F);
        zombie.invulnerableTime = 0;
        zombie.hurt(helper.getLevel().damageSources().playerAttack(player), 6.0F);
        helper.assertTrue(player.getHealth() > 6.0F, "lifesteal should heal the player, health " + player.getHealth());
        helper.succeed();
    }
}
