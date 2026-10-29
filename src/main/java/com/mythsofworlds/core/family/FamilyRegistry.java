package com.mythsofworlds.core.family;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.saveddata.SavedData;

/**
 * Where the wives and daughters of every player were last seen, in every world, so the family whistle can find them
 * even in a world nobody is in. Kept with the overworld's data.
 */
public class FamilyRegistry extends SavedData {
    public record Member(UUID id, UUID family, ResourceKey<Level> dimension, BlockPos pos) {
    }

    private static final String NAME = "mythsofworlds_family";
    private final Map<UUID, Member> members = new HashMap<>();

    public static FamilyRegistry get(MinecraftServer server) {
        return server.overworld().getDataStorage().computeIfAbsent(
                new SavedData.Factory<>(FamilyRegistry::new, FamilyRegistry::load, null), NAME);
    }

    /** Remembers where {@code entity}, a member of {@code family}'s family, is now. */
    public void update(Entity entity, UUID family) {
        Member old = members.get(entity.getUUID());
        Member now = new Member(entity.getUUID(), family, entity.level().dimension(), entity.blockPosition());
        if (!now.equals(old)) {
            members.put(now.id(), now);
            setDirty();
        }
    }

    public void remove(UUID id) {
        if (members.remove(id) != null) {
            setDirty();
        }
    }

    public List<Member> familyOf(UUID player) {
        List<Member> found = new ArrayList<>();
        for (Member member : members.values()) {
            if (member.family().equals(player)) {
                found.add(member);
            }
        }
        return found;
    }

    private static FamilyRegistry load(CompoundTag tag, HolderLookup.Provider registries) {
        FamilyRegistry registry = new FamilyRegistry();
        for (Tag each : tag.getList("Members", Tag.TAG_COMPOUND)) {
            CompoundTag entry = (CompoundTag) each;
            ResourceLocation dimension = ResourceLocation.tryParse(entry.getString("Dimension"));
            if (dimension == null || !entry.hasUUID("Id") || !entry.hasUUID("Family")) {
                continue;
            }
            Member member = new Member(entry.getUUID("Id"), entry.getUUID("Family"),
                    ResourceKey.create(Registries.DIMENSION, dimension), BlockPos.of(entry.getLong("Pos")));
            registry.members.put(member.id(), member);
        }
        return registry;
    }

    @Override
    public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
        ListTag list = new ListTag();
        for (Member member : members.values()) {
            CompoundTag entry = new CompoundTag();
            entry.putUUID("Id", member.id());
            entry.putUUID("Family", member.family());
            entry.putString("Dimension", member.dimension().location().toString());
            entry.putLong("Pos", member.pos().asLong());
            list.add(entry);
        }
        tag.put("Members", list);
        return tag;
    }
}
