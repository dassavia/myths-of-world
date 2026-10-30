package com.mythsofworlds.gametest;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.BossBalance;
import com.mythsofworlds.core.ServerConfig;
import com.mythsofworlds.mythology.slavic.SlavicEntities;
import com.mythsofworlds.mythology.slavic.entity.Koschei;
import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.animal.Pig;
import net.neoforged.neoforge.gametest.GameTestHolder;
import net.neoforged.neoforge.gametest.PrefixGameTestTemplate;

/** The balance settings of the server config. */
@GameTestHolder(MythsOfWorlds.MODID)
@PrefixGameTestTemplate(false)
public class BalanceTests {
    /** The boss health setting scales the boss's maximum health and keeps the share of health it has left. */
    @GameTest(template = "empty")
    public static void bossHealthScales(GameTestHelper helper) {
        Koschei koschei = helper.spawn(SlavicEntities.KOSCHEI.get(), new BlockPos(1, 2, 1));
        float base = koschei.getMaxHealth();
        BossBalance.scaleHealth(koschei, 2.0);
        helper.assertTrue(koschei.getMaxHealth() == base * 2.0F && koschei.getHealth() == koschei.getMaxHealth(),
                "twice the health, at full: " + koschei.getHealth() + "/" + koschei.getMaxHealth());
        koschei.setHealth(base);
        BossBalance.scaleHealth(koschei, 1.0);
        helper.assertTrue(koschei.getMaxHealth() == base && Math.abs(koschei.getHealth() - base / 2.0F) < 0.01F,
                "back to the base, still half wounded: " + koschei.getHealth() + "/" + koschei.getMaxHealth());
        koschei.discard();
        helper.succeed();
    }

    /** The boss damage setting multiplies the blows of a boss. */
    @GameTest(template = "empty")
    public static void bossDamageScales(GameTestHelper helper) {
        Koschei koschei = helper.spawn(SlavicEntities.KOSCHEI.get(), new BlockPos(1, 2, 1));
        Pig plain = helper.spawn(EntityType.PIG, new BlockPos(3, 2, 1));
        Pig doubled = helper.spawn(EntityType.PIG, new BlockPos(3, 2, 3));
        var sources = helper.getLevel().damageSources();
        plain.hurt(sources.mobAttack(koschei), 2.0F);
        double before = ServerConfig.BOSS_DAMAGE.get();
        try {
            ServerConfig.BOSS_DAMAGE.set(2.0);
            doubled.hurt(sources.mobAttack(koschei), 2.0F);
        } finally {
            ServerConfig.BOSS_DAMAGE.set(before);
        }
        float lostPlain = plain.getMaxHealth() - plain.getHealth();
        float lostDoubled = doubled.getMaxHealth() - doubled.getHealth();
        helper.assertTrue(Math.abs(lostDoubled - lostPlain * 2.0F) < 0.01F, "lost " + lostPlain + " and " + lostDoubled);
        plain.discard();
        doubled.discard();
        koschei.discard();
        helper.succeed();
    }
}
