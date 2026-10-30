package com.mythsofworlds.codex.client;

import com.mythsofworlds.codex.Codex;
import net.minecraft.client.Minecraft;
import org.jetbrains.annotations.Nullable;

/** Client side of the Codex: opening the book screen. Only ever called on the client. */
public final class CodexClient {
    private CodexClient() {
    }

    /** Opens the Codex where the player left it, or at the chapter of a journal volume. */
    public static void open(@Nullable String volume) {
        Codex.Chapter chapter = volume == null ? null : Codex.forVolume(volume);
        Minecraft.getInstance().setScreen(chapter == null ? CodexScreen.resume() : CodexScreen.atChapter(chapter.id()));
    }
}
