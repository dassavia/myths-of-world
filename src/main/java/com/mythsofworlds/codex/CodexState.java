package com.mythsofworlds.codex;

import java.util.List;
import java.util.Set;

/** The client's copy of what its player has found and done (sent by {@link CodexSyncPayload}). */
public final class CodexState {
    private static volatile Set<String> entries = Set.of();
    private static volatile Set<String> milestones = Set.of();

    private CodexState() {
    }

    public static void set(List<String> newEntries, List<String> newMilestones) {
        entries = Set.copyOf(newEntries);
        milestones = Set.copyOf(newMilestones);
    }

    public static Set<String> entries() {
        return entries;
    }

    public static Set<String> milestones() {
        return milestones;
    }
}
