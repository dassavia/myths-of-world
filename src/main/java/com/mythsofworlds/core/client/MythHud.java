package com.mythsofworlds.core.client;

import com.mojang.blaze3d.platform.InputConstants;
import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.codex.client.CodexScreen;
import com.mythsofworlds.core.ClientConfig;
import java.util.Set;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.screens.PauseScreen;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.Style;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.food.FoodData;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.ModList;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterGuiLayersEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.client.event.RenderGuiLayerEvent;
import net.neoforged.neoforge.client.event.ScreenEvent;
import net.neoforged.neoforge.client.gui.ConfigurationScreen;
import net.neoforged.neoforge.client.gui.IConfigScreenFactory;
import net.neoforged.neoforge.client.gui.VanillaGuiLayers;
import org.lwjgl.glfw.GLFW;

/**
 * The HUD of the myths: health, armour, hunger, air and experience as carved bars in gold frames, the numbers in the
 * old-style typeface of the Codex, and in the worlds of the myths a scroll with the world's name. It replaces the
 * vanilla hearts, armour, food, air and experience while it is on; the H key or the button in the pause menu
 * switches it at any time ({@link ClientConfig}).
 */
public final class MythHud {
    private static final ResourceLocation TEXTURE = MythsOfWorlds.id("textures/gui/hud.png");
    private static final int TEX_W = 256;
    private static final int TEX_H = 96;
    /** The vanilla layers the HUD takes over. */
    private static final Set<ResourceLocation> REPLACED = Set.of(VanillaGuiLayers.PLAYER_HEALTH, VanillaGuiLayers.ARMOR_LEVEL,
            VanillaGuiLayers.FOOD_LEVEL, VanillaGuiLayers.AIR_LEVEL, VanillaGuiLayers.EXPERIENCE_BAR,
            VanillaGuiLayers.EXPERIENCE_LEVEL);
    public static final KeyMapping TOGGLE = new KeyMapping("key.mythsofworlds.toggle_hud", InputConstants.Type.KEYSYM,
            GLFW.GLFW_KEY_H, "key.categories.mythsofworlds");
    /** Health shown on the bar, easing towards the real value so that a blow drains it visibly. */
    private static float shownHealth = -1;
    private static float lastHealth = -1;
    private static int hurtFlash;

    private MythHud() {
    }

    public static boolean enabled() {
        return ClientConfig.HUD_ENABLED.get();
    }

    @EventBusSubscriber(modid = MythsOfWorlds.MODID, bus = EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
    public static final class ModBus {
        private ModBus() {
        }

        @SubscribeEvent
        public static void registerLayers(RegisterGuiLayersEvent event) {
            event.registerAbove(VanillaGuiLayers.FOOD_LEVEL, MythsOfWorlds.id("myth_bars"), (graphics, delta) -> renderBars(graphics));
            event.registerAbove(VanillaGuiLayers.CAMERA_OVERLAYS, MythsOfWorlds.id("myth_world_scroll"),
                    (graphics, delta) -> renderWorldScroll(graphics));
        }

        @SubscribeEvent
        public static void registerKeys(RegisterKeyMappingsEvent event) {
            event.register(TOGGLE);
        }

        /** The settings screen in the mod list (Mods, Myths of Worlds, Config). */
        @SubscribeEvent
        public static void setup(FMLClientSetupEvent event) {
            ModList.get().getModContainerById(MythsOfWorlds.MODID).ifPresent(container ->
                    container.registerExtensionPoint(IConfigScreenFactory.class, ConfigurationScreen::new));
        }
    }

    @EventBusSubscriber(modid = MythsOfWorlds.MODID, value = Dist.CLIENT)
    public static final class GameBus {
        private GameBus() {
        }

        @SubscribeEvent
        public static void hideVanilla(RenderGuiLayerEvent.Pre event) {
            if (enabled() && REPLACED.contains(event.getName())) {
                event.setCanceled(true);
            }
        }

        @SubscribeEvent
        public static void onTick(ClientTickEvent.Post event) {
            while (TOGGLE.consumeClick()) {
                boolean on = ClientConfig.toggleHud();
                LocalPlayer player = Minecraft.getInstance().player;
                if (player != null) {
                    player.displayClientMessage(Component.translatable(on ? "hud.mythsofworlds.on" : "hud.mythsofworlds.off"), true);
                }
            }
        }

        /** A button in the pause menu switches the HUD without leaving the game. */
        @SubscribeEvent
        public static void addPauseButton(ScreenEvent.Init.Post event) {
            if (event.getScreen() instanceof PauseScreen pause && pause.showsPauseMenu()) {
                event.addListener(Button.builder(buttonLabel(), button -> {
                    ClientConfig.toggleHud();
                    button.setMessage(buttonLabel());
                }).bounds(4, 4, 110, 20).build());
            }
        }

        private static Component buttonLabel() {
            return Component.translatable("hud.mythsofworlds.button",
                    Component.translatable(enabled() ? "hud.mythsofworlds.button.on" : "hud.mythsofworlds.button.off"));
        }
    }

    // ------------------------------------------------------------------ drawing

    private static void sprite(GuiGraphics graphics, int x, int y, int u, int v, int w, int h) {
        graphics.blit(TEXTURE, x, y, w, h, u * 2, v * 2, w * 2, h * 2, TEX_W, TEX_H);
    }

    private static Component myth(String text) {
        return Component.literal(text).withStyle(Style.EMPTY.withFont(CodexScreen.MYTH_FONT));
    }

    /** Text centred on (cx, y), small, with a dark outline so it reads over any fill. */
    private static void label(GuiGraphics graphics, Font font, Component text, int cx, int y, int colour, float scale) {
        graphics.pose().pushPose();
        graphics.pose().translate(cx, y, 0);
        graphics.pose().scale(scale, scale, 1);
        int x = -font.width(text) / 2;
        for (int[] o : new int[][]{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}) {
            graphics.drawString(font, text, x + o[0], o[1], 0xFF1A0E06, false);
        }
        graphics.drawString(font, text, x, 0, colour, false);
        graphics.pose().popPose();
    }

    /**
     * One bar: the frame, the fill from {@code from} to {@code to} colours over {@code fraction} of the width, an
     * optional thin second fill along the bottom (saturation) and the number.
     */
    private static void bar(GuiGraphics graphics, Font font, int x, int y, float fraction, int from, int to,
                            float extra, int extraColour, int iconU, String text, boolean flash) {
        sprite(graphics, x - 2, y - 2, 0, 0, 85, 13);
        int fill = Math.round(81 * Mth.clamp(fraction, 0, 1));
        if (fill > 0) {
            graphics.fillGradient(x, y, x + fill, y + 9, from, to);
            graphics.fill(x, y, x + fill, y + 1, 0x40FFFFFF);
        }
        if (extra > 0) {
            graphics.fill(x, y + 7, x + Math.round(81 * Mth.clamp(extra, 0, 1)), y + 9, extraColour);
        }
        if (flash) {
            graphics.fill(x, y, x + 81, y + 9, 0x70FFFFFF);
        }
        sprite(graphics, x - 6, y, iconU, 0, 9, 9);
        if (ClientConfig.SHOW_NUMBERS.get() && text != null) {
            label(graphics, font, myth(text), x + 43, y + 1, 0xFFF6E7C1, 0.8F);
        }
    }

    private static String number(float value) {
        return value == Math.floor(value) ? Integer.toString((int) value) : String.format("%.1f", value);
    }

    static void renderBars(GuiGraphics graphics) {
        Minecraft minecraft = Minecraft.getInstance();
        LocalPlayer player = minecraft.player;
        if (!enabled() || player == null || minecraft.options.hideGui || minecraft.gameMode == null) {
            return;
        }
        Font font = minecraft.font;
        int w = graphics.guiWidth();
        int h = graphics.guiHeight();
        int leftX = w / 2 - 91;
        int rightX = w / 2 + 10;
        if (minecraft.gameMode.canHurtPlayer()) {
            // Health, with poison, wither and frost in their colours, gold for absorption.
            float max = Math.max(player.getMaxHealth(), 1);
            float health = player.getHealth();
            if (shownHealth < 0 || Math.abs(shownHealth - health) > max) {
                shownHealth = health;
            }
            if (health < lastHealth) {
                hurtFlash = 6;
            }
            lastHealth = health;
            shownHealth += (health - shownHealth) * 0.15F;
            int from = 0xFFE0303A;
            int to = 0xFF7A0E16;
            if (player.hasEffect(MobEffects.POISON)) {
                from = 0xFF8FBF30;
                to = 0xFF3E6A12;
            } else if (player.hasEffect(MobEffects.WITHER)) {
                from = 0xFF5A4A52;
                to = 0xFF201A1E;
            } else if (player.isFullyFrozen()) {
                from = 0xFFAEE2FF;
                to = 0xFF4A86B8;
            }
            int y = h - 39;
            // A pale trail shows the health just lost.
            if (shownHealth > health) {
                graphics.fill(leftX + Math.round(81 * health / max), y, leftX + Math.round(81 * Math.min(shownHealth, max) / max), y + 9,
                        0xFFF0C8A0);
            }
            float absorption = player.getAbsorptionAmount();
            String text = number(Mth.ceil(health)) + "/" + number(max) + (absorption > 0 ? " +" + Mth.ceil(absorption) : "");
            boolean lowPulse = health <= max * 0.25F && (player.tickCount / 5) % 2 == 0;
            bar(graphics, font, leftX, y, health / max, from, to, absorption / max, 0xFFFFD84A, 86, text,
                    hurtFlash-- > 0 || lowPulse);
            // Armour above health, if any.
            int armour = player.getArmorValue();
            if (armour > 0) {
                // Toughness is the thin steel-blue line along the bottom of the armour bar.
                double toughness = player.getAttributeValue(Attributes.ARMOR_TOUGHNESS);
                bar(graphics, font, leftX, y - 12, armour / 20.0F, 0xFFD8DEE8, 0xFF6E7684, (float) toughness / 20.0F,
                        0xFF5A9AD8, 95, Integer.toString(armour), false);
            }
            // The bars stand taller than the vanilla icons: lift the held item's name above them.
            minecraft.gui.leftHeight = Math.max(minecraft.gui.leftHeight, armour > 0 ? 64 : 52);
            // Food, unless a living mount shows its own health there.
            boolean mounted = player.getVehicle() instanceof LivingEntity mount && mount.showVehicleHealth();
            if (!mounted) {
                FoodData food = player.getFoodData();
                boolean hungry = player.hasEffect(MobEffects.HUNGER);
                bar(graphics, font, rightX, y, food.getFoodLevel() / 20.0F, hungry ? 0xFF9CB04A : 0xFFE6A24A,
                        hungry ? 0xFF4E5C1A : 0xFF8A4A16, food.getSaturationLevel() / 20.0F, 0xFFFFE680, 104,
                        food.getFoodLevel() + "/20", false);
            }
            // Air while it runs out.
            int maxAir = player.getMaxAirSupply();
            int air = Math.max(0, player.getAirSupply());
            if (player.isUnderWater() || air < maxAir) {
                bar(graphics, font, rightX, y - 12, air / (float) maxAir, 0xFF9AD8FF, 0xFF2A64B0, 0, 0, 113,
                        Mth.ceil(air / 20.0F) + "s", false);
                minecraft.gui.rightHeight = Math.max(minecraft.gui.rightHeight, 64);
            }
        }
        if (minecraft.gameMode.hasExperience() && player.jumpableVehicle() == null) {
            int x = w / 2 - 91;
            int y = h - 29;
            sprite(graphics, x - 2, y - 2, 0, 13, 186, 9);
            int fill = Math.round(182 * player.experienceProgress);
            if (fill > 0) {
                graphics.fillGradient(x, y, x + fill, y + 5, 0xFFC8F060, 0xFF4E8A1E);
                graphics.fill(x, y, x + fill, y + 1, 0x50FFFFFF);
            }
            if (player.experienceLevel > 0) {
                sprite(graphics, w / 2 - 12, y - 13, 0, 22, 24, 16);
                label(graphics, font, myth(Integer.toString(player.experienceLevel)), w / 2, y - 9, 0xFFB8F070, 0.9F);
            }
        }
    }

    static void renderWorldScroll(GuiGraphics graphics) {
        Minecraft minecraft = Minecraft.getInstance();
        if (!enabled() || !ClientConfig.SHOW_WORLD_NAME.get() || minecraft.level == null || minecraft.options.hideGui
                || minecraft.getDebugOverlay().showDebugScreen()) {
            return;
        }
        ResourceLocation dimension = minecraft.level.dimension().location();
        if (!dimension.getNamespace().equals(MythsOfWorlds.MODID)) {
            return;
        }
        sprite(graphics, 4, 4, 24, 22, 104, 18);
        Component name = Component.translatable("hud.mythsofworlds.world." + dimension.getPath())
                .withStyle(Style.EMPTY.withFont(CodexScreen.MYTH_FONT));
        int x = 4 + 52 - minecraft.font.width(name) / 2;
        graphics.drawString(minecraft.font, name, x, 9, 0xFF4A2410, false);
    }
}
