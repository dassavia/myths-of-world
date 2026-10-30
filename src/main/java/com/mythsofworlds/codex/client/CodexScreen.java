package com.mythsofworlds.codex.client;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.codex.Codex;
import com.mythsofworlds.codex.CodexState;
import com.mythsofworlds.codex.Progress;
import com.mythsofworlds.journal.Journal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.InventoryScreen;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.network.chat.Style;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.ItemStack;
import org.jetbrains.annotations.Nullable;

/**
 * The Codex of Myths, an open book of two pages. Three views:
 * <ul>
 *   <li>contents: the title page and the chapters, one per world; a locked chapter shows what opens it;</li>
 *   <li>a chapter: the map of the world's bosses in their order (or its introduction), then its entries, with a
 *       question mark for those not yet found;</li>
 *   <li>an entry: a portrait of the creature, if it is one, and the pages of the entry.</li>
 * </ul>
 * In creative mode every chapter and entry is open. The text is the journal text of the lang files, written to fit
 * pages of {@value #TEXT_WIDTH} pixels and {@value #LINES} lines.
 */
public class CodexScreen extends Screen {
    private static final ResourceLocation BOOK = MythsOfWorlds.id("textures/gui/codex.png");
    private static final ResourceLocation WIDGETS = MythsOfWorlds.id("textures/gui/codex_widgets.png");
    /** Old-style typeface of the titles (assets/mythsofworlds/font/myth.json). */
    public static final ResourceLocation MYTH_FONT = MythsOfWorlds.id("myth");
    private static final int BOOK_W = 292;
    private static final int BOOK_H = 186;
    static final int TEXT_WIDTH = 114;
    static final int LINES = 14;
    private static final int LEFT_PAGE_X = 20;
    private static final int RIGHT_PAGE_X = 158;
    private static final int PAGE_Y = 18;
    private static final int ROW = 12;
    private static final int ROWS = 11;
    private static final int INK = 0xFF3B2614;
    private static final int FADED = 0xFF8A7458;
    private static final int GOLD = 0xFF9A6A12;

    private enum View { CONTENTS, CHAPTER, ENTRY }

    /** Where the book was left, so it opens there again. */
    private static View lastView = View.CONTENTS;
    @Nullable
    private static String lastChapter;
    @Nullable
    private static String lastEntry;
    private static int lastSpread;

    private View view;
    @Nullable
    private Codex.Chapter chapter;
    @Nullable
    private Journal.Entry entry;
    private int spread;
    private int left;
    private int top;
    private final Map<String, Entity> portraits = new HashMap<>();
    /** What a click at the mouse would do this frame, found while drawing. */
    @Nullable
    private Runnable hoverAction;
    private final List<Component> hoverTooltip = new ArrayList<>();

    private CodexScreen(View view, @Nullable Codex.Chapter chapter, @Nullable Journal.Entry entry, int spread) {
        super(Component.translatable("item.mythsofworlds.codex"));
        this.view = view;
        this.chapter = chapter;
        this.entry = entry;
        this.spread = spread;
    }

    public static CodexScreen resume() {
        Codex.Chapter chapter = lastChapter == null ? null : Codex.chapter(lastChapter);
        if (lastView == View.CONTENTS || chapter == null || !isOpen(chapter)) {
            return new CodexScreen(View.CONTENTS, null, null, 0);
        }
        if (lastView == View.ENTRY && lastEntry != null) {
            for (Journal.Entry e : Journal.volume(chapter.volume())) {
                if (e.id().equals(lastEntry) && isFound(e)) {
                    return new CodexScreen(View.ENTRY, chapter, e, lastSpread);
                }
            }
        }
        return new CodexScreen(View.CHAPTER, chapter, null, lastView == View.CHAPTER ? lastSpread : 0);
    }

    public static CodexScreen atChapter(String id) {
        Codex.Chapter chapter = Codex.chapter(id);
        return chapter != null && isOpen(chapter) ? new CodexScreen(View.CHAPTER, chapter, null, 0)
                : new CodexScreen(View.CONTENTS, null, null, 0);
    }

    // ------------------------------------------------------------------ state of the player

    private static boolean creative() {
        return Minecraft.getInstance().player != null && Minecraft.getInstance().player.isCreative();
    }

    static boolean isOpen(Codex.Chapter chapter) {
        var player = Minecraft.getInstance().player;
        return player != null && Progress.has(player, CodexState.milestones(), chapter.requires());
    }

    static boolean isFound(Journal.Entry entry) {
        return creative() || entry.category() == Journal.Category.INTRO || CodexState.entries().contains(entry.id());
    }

    private static boolean reached(String milestone) {
        return creative() || CodexState.milestones().contains(milestone);
    }

    // ------------------------------------------------------------------ screen

    @Override
    protected void init() {
        left = (width - BOOK_W) / 2;
        top = (height - BOOK_H) / 2;
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }

    @Override
    public void onClose() {
        lastView = view;
        lastChapter = chapter == null ? null : chapter.id();
        lastEntry = entry == null ? null : entry.id();
        lastSpread = spread;
        super.onClose();
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        super.render(graphics, mouseX, mouseY, partialTick);
        hoverAction = null;
        hoverTooltip.clear();
        graphics.blit(BOOK, left, top, BOOK_W, BOOK_H, 0, 0, BOOK_W * 2, BOOK_H * 2, BOOK_W * 2, BOOK_H * 2);
        switch (view) {
            case CONTENTS -> renderContents(graphics, mouseX, mouseY);
            case CHAPTER -> renderChapter(graphics, mouseX, mouseY);
            case ENTRY -> renderEntry(graphics, mouseX, mouseY, partialTick);
        }
        if (!hoverTooltip.isEmpty()) {
            graphics.renderComponentTooltip(font, hoverTooltip, mouseX, mouseY);
        }
    }

    @Override
    public boolean mouseClicked(double mouseX, double mouseY, int button) {
        if (button == 0 && hoverAction != null) {
            Runnable action = hoverAction;
            hoverAction = null;
            action.run();
            Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(SoundEvents.BOOK_PAGE_TURN, 1.0F));
            return true;
        }
        if (button == 1 && view != View.CONTENTS) {
            back();
            return true;
        }
        return super.mouseClicked(mouseX, mouseY, button);
    }

    @Override
    public boolean mouseScrolled(double mouseX, double mouseY, double scrollX, double scrollY) {
        int spreads = spreads();
        if (scrollY < 0 && spread + 1 < spreads) {
            spread++;
        } else if (scrollY > 0 && spread > 0) {
            spread--;
        }
        return true;
    }

    private void back() {
        if (view == View.ENTRY) {
            view = View.CHAPTER;
            entry = null;
            spread = 0;
        } else {
            view = View.CONTENTS;
            chapter = null;
            spread = 0;
        }
    }

    private int spreads() {
        return switch (view) {
            case CONTENTS -> 1;
            case CHAPTER -> (chapterPages().size() + 2) / 2;
            case ENTRY -> (entryPages() + 1) / 2;
        };
    }

    // ------------------------------------------------------------------ drawing helpers

    private static Component mythTitle(Component text) {
        return text.copy().withStyle(Style.EMPTY.withFont(MYTH_FONT).withColor(0x5A2A0C));
    }

    private int drawLines(GuiGraphics graphics, Component text, int x, int y, int colour) {
        for (FormattedCharSequence line : font.split(text, TEXT_WIDTH)) {
            graphics.drawString(font, line, x, y, colour, false);
            y += 9;
        }
        return y;
    }

    private void widget(GuiGraphics graphics, String name, int x, int y, boolean hover) {
        int[] r = switch (name + (hover ? "_hover" : "")) {
            case "next" -> new int[]{0, 0, 18, 10};
            case "next_hover" -> new int[]{0, 10, 18, 10};
            case "prev" -> new int[]{18, 0, 18, 10};
            case "prev_hover" -> new int[]{18, 10, 18, 10};
            case "back" -> new int[]{36, 0, 14, 12};
            case "back_hover" -> new int[]{36, 12, 14, 12};
            case "lock", "lock_hover" -> new int[]{50, 0, 9, 11};
            case "step_done", "step_done_hover" -> new int[]{60, 0, 22, 22};
            case "step_todo", "step_todo_hover" -> new int[]{82, 0, 22, 22};
            case "step_locked", "step_locked_hover" -> new int[]{104, 0, 22, 22};
            case "ornament", "ornament_hover" -> new int[]{0, 24, 110, 7};
            default -> new int[]{0, 32, 114, 12};
        };
        graphics.blit(WIDGETS, x, y, r[2], r[3], r[0] * 2, r[1] * 2, r[2] * 2, r[3] * 2, 256, 128);
    }

    private static boolean inside(int mouseX, int mouseY, int x, int y, int w, int h) {
        return mouseX >= x && mouseX < x + w && mouseY >= y && mouseY < y + h;
    }

    /** Arrows at the foot of the pages and the back arrow. */
    private void renderNavigation(GuiGraphics graphics, int mouseX, int mouseY) {
        int y = top + BOOK_H - 24;
        if (spread > 0) {
            int x = left + 24;
            boolean hover = inside(mouseX, mouseY, x, y, 18, 10);
            widget(graphics, "prev", x, y, hover);
            if (hover) {
                hoverAction = () -> spread--;
            }
        }
        if (spread + 1 < spreads()) {
            int x = left + BOOK_W - 42;
            boolean hover = inside(mouseX, mouseY, x, y, 18, 10);
            widget(graphics, "next", x, y, hover);
            if (hover) {
                hoverAction = () -> spread++;
            }
        }
        if (view != View.CONTENTS) {
            int x = left + BOOK_W / 2 - 22;
            boolean hover = inside(mouseX, mouseY, x, y - 1, 14, 12);
            widget(graphics, "back", x, y - 1, hover);
            if (hover) {
                hoverAction = this::back;
                hoverTooltip.add(Component.translatable("codex.mythsofworlds.back"));
            }
        }
        if (spreads() > 1) {
            String number = (spread + 1) + " / " + spreads();
            graphics.drawString(font, number, left + BOOK_W / 2 + 8, y + 1, FADED, false);
        }
    }

    // ------------------------------------------------------------------ contents

    private void renderContents(GuiGraphics graphics, int mouseX, int mouseY) {
        int x = left + LEFT_PAGE_X;
        int y = top + PAGE_Y + 4;
        Component title = mythTitle(Component.translatable("journal.mythsofworlds.path.title"));
        graphics.drawString(font, title, x + (TEXT_WIDTH - font.width(title)) / 2, y, 0xFF5A2A0C, false);
        widget(graphics, "ornament", x + 2, y + 12, false);
        y = drawLines(graphics, Component.translatable("journal.mythsofworlds.path.intro"), x, y + 24, INK);
        int found = 0;
        int total = 0;
        for (Codex.Chapter c : Codex.chapters()) {
            for (Journal.Entry e : Journal.volume(c.volume())) {
                if (e.category() != Journal.Category.INTRO) {
                    total++;
                    found += isFound(e) ? 1 : 0;
                }
            }
        }
        y += 6;
        drawLines(graphics, Component.translatable("codex.mythsofworlds.progress", found, total), x, y, FADED);
        if (creative()) {
            drawLines(graphics, Component.translatable("codex.mythsofworlds.creative"), x, y + 20, GOLD);
        }

        int rx = left + RIGHT_PAGE_X;
        int ry = top + PAGE_Y + 4;
        Component contents = mythTitle(Component.translatable("codex.mythsofworlds.contents"));
        graphics.drawString(font, contents, rx + (TEXT_WIDTH - font.width(contents)) / 2, ry, 0xFF5A2A0C, false);
        widget(graphics, "ornament", rx + 2, ry + 12, false);
        ry += 26;
        for (Codex.Chapter c : Codex.chapters()) {
            boolean open = isOpen(c);
            boolean hover = inside(mouseX, mouseY, rx - 2, ry - 2, TEXT_WIDTH + 4, 22);
            if (hover) {
                widget(graphics, "row_hover", rx, ry + 3, false);
            }
            ItemStack icon = icon(c.icon());
            graphics.renderItem(icon, rx, ry + 1);
            Component name = Component.translatable("codex.mythsofworlds.chapter." + c.id());
            if (open) {
                graphics.drawString(font, mythTitle(name), rx + 22, ry + 5, 0xFF5A2A0C, false);
            } else {
                graphics.fill(rx, ry + 1, rx + 16, ry + 17, 0x88EADBB8);
                widget(graphics, "lock", rx + 4, ry + 4, false);
                graphics.drawString(font, name.copy().withStyle(ChatFormatting.ITALIC), rx + 22, ry + 5, FADED, false);
            }
            if (hover) {
                if (open) {
                    Codex.Chapter target = c;
                    hoverAction = () -> {
                        chapter = target;
                        view = View.CHAPTER;
                        spread = 0;
                    };
                } else {
                    hoverTooltip.add(Component.translatable("codex.mythsofworlds.locked").withStyle(ChatFormatting.GOLD));
                    MutableComponent needs = Component.empty();
                    for (int i = 0; i < c.requires().size(); i++) {
                        if (i > 0) {
                            needs.append(", ");
                        }
                        String milestone = c.requires().get(i);
                        needs.append(Component.translatable("codex.mythsofworlds.milestone." + milestone)
                                .withStyle(reached(milestone) ? ChatFormatting.GREEN : ChatFormatting.GRAY));
                    }
                    hoverTooltip.add(Component.translatable("codex.mythsofworlds.requires", needs));
                }
            }
            ry += 24;
        }
    }

    private static ItemStack icon(ResourceLocation id) {
        return new ItemStack(BuiltInRegistries.ITEM.get(id));
    }

    // ------------------------------------------------------------------ chapter

    /** One row of the list of entries: a heading (entry null) or an entry. */
    private record Row(@Nullable Journal.Category heading, @Nullable Journal.Entry entry) {
    }

    /** Pages of the chapter after its first page (the map): rows of entries under their headings. */
    private List<List<Row>> chapterPages() {
        List<Row> rows = new ArrayList<>();
        List<Journal.Entry> entries = Journal.volume(chapter.volume());
        for (Journal.Category category : Journal.Category.values()) {
            boolean any = false;
            for (Journal.Entry e : entries) {
                if (e.category() == category) {
                    if (!any) {
                        rows.add(new Row(category, null));
                        any = true;
                    }
                    rows.add(new Row(null, e));
                }
            }
        }
        List<List<Row>> pages = new ArrayList<>();
        for (int i = 0; i < rows.size(); i += ROWS) {
            pages.add(rows.subList(i, Math.min(rows.size(), i + ROWS)));
        }
        return pages;
    }

    private void renderChapter(GuiGraphics graphics, int mouseX, int mouseY) {
        List<List<Row>> pages = chapterPages();
        // Page 0 is the map (or the introduction); pages 1.. are the lists.
        int first = spread * 2;
        for (int side = 0; side < 2; side++) {
            int page = first + side;
            int x = left + (side == 0 ? LEFT_PAGE_X : RIGHT_PAGE_X);
            if (page == 0) {
                renderChapterTitlePage(graphics, x, mouseX, mouseY);
            } else if (page - 1 < pages.size()) {
                renderRows(graphics, pages.get(page - 1), x, top + PAGE_Y + 2, mouseX, mouseY);
            }
        }
        renderNavigation(graphics, mouseX, mouseY);
    }

    private void renderChapterTitlePage(GuiGraphics graphics, int x, int mouseX, int mouseY) {
        int y = top + PAGE_Y + 2;
        Component title = mythTitle(Component.translatable("codex.mythsofworlds.chapter." + chapter.id()));
        graphics.drawString(font, title, x + (TEXT_WIDTH - font.width(title)) / 2, y, 0xFF5A2A0C, false);
        widget(graphics, "ornament", x + 2, y + 12, false);
        y += 24;
        if (chapter.steps().isEmpty()) {
            drawLines(graphics, Component.translatable("journal.mythsofworlds." + chapter.volume() + ".intro"), x, y, INK);
            return;
        }
        Component map = Component.translatable("codex.mythsofworlds.map");
        graphics.drawString(font, map, x + (TEXT_WIDTH - font.width(map)) / 2, y, FADED, false);
        y += 12;
        // The steps wind down the page four to a row, left to right, then right to left.
        List<Codex.Step> steps = chapter.steps();
        int[][] at = new int[steps.size()][];
        for (int i = 0; i < steps.size(); i++) {
            int row = i / 4;
            int col = i % 4;
            if (row % 2 == 1) {
                col = 3 - col;
            }
            at[i] = new int[]{x + 3 + col * 28, y + row * 30};
        }
        for (int i = 0; i + 1 < steps.size(); i++) {
            int colour = reached(steps.get(i + 1).milestone()) ? 0xFFC8962A : 0xFFB8A27E;
            int ax = at[i][0] + 11;
            int ay = at[i][1] + 11;
            int bx = at[i + 1][0] + 11;
            int by = at[i + 1][1] + 11;
            if (ay == by) {
                graphics.fill(Math.min(ax, bx), ay - 1, Math.max(ax, bx), ay + 1, colour);
            } else {
                graphics.fill(ax - 1, Math.min(ay, by), ax + 1, Math.max(ay, by), colour);
            }
        }
        boolean previousDone = true;
        for (int i = 0; i < steps.size(); i++) {
            Codex.Step step = steps.get(i);
            boolean done = reached(step.milestone());
            String frame = done ? "step_done" : previousDone ? "step_todo" : "step_locked";
            widget(graphics, frame, at[i][0], at[i][1], false);
            graphics.renderItem(icon(step.icon()), at[i][0] + 3, at[i][1] + 3);
            if (!done && !previousDone) {
                graphics.fill(at[i][0] + 3, at[i][1] + 3, at[i][0] + 19, at[i][1] + 19, 0x99D8C8A4);
            }
            if (inside(mouseX, mouseY, at[i][0], at[i][1], 22, 22)) {
                hoverTooltip.add(Component.translatable("codex.mythsofworlds.milestone." + step.milestone())
                        .withStyle(done ? ChatFormatting.GOLD : ChatFormatting.GRAY));
            }
            previousDone = done;
        }
    }

    private void renderRows(GuiGraphics graphics, List<Row> rows, int x, int y, int mouseX, int mouseY) {
        for (Row row : rows) {
            if (row.heading() != null) {
                Component heading = mythTitle(Component.translatable("journal.mythsofworlds.category."
                        + row.heading().name().toLowerCase()));
                graphics.drawString(font, heading, x, y + 2, 0xFF5A2A0C, false);
                graphics.fill(x, y + 11, x + TEXT_WIDTH, y + 12, 0x66A07840);
            } else {
                Journal.Entry e = row.entry();
                boolean found = isFound(e);
                boolean hover = inside(mouseX, mouseY, x - 2, y, TEXT_WIDTH + 4, ROW);
                if (hover && found) {
                    widget(graphics, "row_hover", x, y, false);
                    hoverAction = () -> {
                        entry = e;
                        view = View.ENTRY;
                        spread = 0;
                    };
                }
                Component name = found ? e.title() : Component.translatable("codex.mythsofworlds.unknown");
                // A name too long for the row ends in an ellipsis, and the whole name shows on hover.
                String full = name.getString();
                int room = TEXT_WIDTH - 2 - font.width("• ");
                String text = full;
                if (font.width(full) > room) {
                    text = font.plainSubstrByWidth(full, room - font.width("…")).stripTrailing() + "…";
                    if (hover && found) {
                        hoverTooltip.add(name);
                    }
                }
                graphics.drawString(font, "• " + text, x + 2, y + 2, found ? INK : FADED, false);
                if (hover && !found) {
                    hoverTooltip.add(Component.translatable("codex.mythsofworlds.unknown_hint").withStyle(ChatFormatting.GRAY));
                }
            }
            y += ROW;
        }
    }

    // ------------------------------------------------------------------ entry

    private boolean hasPortrait() {
        return entry != null && entry.entity().isPresent();
    }

    /** Pages of the entry: the portrait (for creatures and bosses), then the text pages. */
    private int entryPages() {
        return entry.pages() + (hasPortrait() ? 1 : 0);
    }

    private void renderEntry(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        int first = spread * 2;
        for (int side = 0; side < 2; side++) {
            int page = first + side;
            int x = left + (side == 0 ? LEFT_PAGE_X : RIGHT_PAGE_X);
            if (page >= entryPages()) {
                continue;
            }
            if (hasPortrait() && page == 0) {
                renderPortrait(graphics, x, mouseX, mouseY);
            } else {
                int textPage = page + (hasPortrait() ? 0 : 1);
                renderTextPage(graphics, x, textPage);
            }
        }
        renderNavigation(graphics, mouseX, mouseY);
    }

    private void renderTextPage(GuiGraphics graphics, int x, int textPage) {
        int y = top + PAGE_Y;
        if (textPage == 1) {
            graphics.drawString(font, Component.translatable("journal.mythsofworlds.category."
                    + entry.category().name().toLowerCase()), x, y, FADED, false);
            y = drawLines(graphics, mythTitle(entry.title()), x, y + 9, 0xFF5A2A0C);
            y += 9;
        }
        drawLines(graphics, Component.translatable("journal.mythsofworlds." + entry.id() + ".page" + textPage), x, y, INK);
    }

    private void renderPortrait(GuiGraphics graphics, int x, int mouseX, int mouseY) {
        int y = top + PAGE_Y;
        graphics.drawString(font, Component.translatable("journal.mythsofworlds.category."
                + entry.category().name().toLowerCase()), x, y, FADED, false);
        y = drawLines(graphics, mythTitle(entry.title()), x, y + 9, 0xFF5A2A0C);
        widget(graphics, "ornament", x + 2, y + 2, false);
        Entity creature = portrait(entry.entity().get());
        if (creature instanceof LivingEntity living) {
            int boxTop = y + 12;
            int boxBottom = top + BOOK_H - 30;
            float size = Math.max(living.getBbHeight(), living.getBbWidth() * 1.3F);
            int scale = (int) Math.max(8, Math.min(40, (boxBottom - boxTop - 8) / Math.max(0.5F, size)));
            try {
                InventoryScreen.renderEntityInInventoryFollowsMouse(graphics, x, boxTop, x + TEXT_WIDTH, boxBottom, scale,
                        0.0625F, mouseX, mouseY, living);
            } catch (RuntimeException e) {
                MythsOfWorlds.LOGGER.debug("cannot draw {} in the Codex", entry.entity().get(), e);
            }
        }
    }

    @Nullable
    private Entity portrait(ResourceLocation type) {
        var level = Minecraft.getInstance().level;
        if (level == null) {
            return null;
        }
        return portraits.computeIfAbsent(type.toString(), key -> {
            try {
                return BuiltInRegistries.ENTITY_TYPE.get(type).create(level);
            } catch (RuntimeException e) {
                return null;
            }
        });
    }
}
