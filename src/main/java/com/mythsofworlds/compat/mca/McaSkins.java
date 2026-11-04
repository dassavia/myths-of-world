package com.mythsofworlds.compat.mca;

import com.mythsofworlds.MythsOfWorlds;
import com.mythsofworlds.core.ClientConfig;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import javax.annotation.Nullable;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManager;
import net.minecraft.server.packs.resources.ResourceManagerReloadListener;
import net.neoforged.fml.ModList;

/**
 * The client side of {@link McaCompat}: with MCA Reborn installed, the priestesses of Isis, the amazons and the
 * valkyries can wear MCA's women's looks (a skin, a face, a hairstyle and clothes that suit them), each her own and
 * always the same, chosen from her UUID. Isis and Hippolyta keep their own looks.
 * <p>
 * Nothing of MCA is copied into this mod: its textures ({@code mca:skins/...}) are found at run time in the resources
 * MCA itself loads, with the plain resource manager, and never linked against MCA's code. If MCA is absent, the
 * option {@link ClientConfig#MCA_SKINS} is off, or any kind of texture is missing from its resources (another version
 * laid them out differently), every woman keeps the mod's own texture.
 */
public final class McaSkins implements ResourceManagerReloadListener {
    public static final McaSkins INSTANCE = new McaSkins();
    private static final String ROOT = "skins/";

    /** Which of MCA's women's clothes suit each of ours. */
    public enum Role {
        PRIESTESS("cleric", "none"),
        AMAZON("archer", "guard"),
        VALKYRIE("guard", "armorer");

        private final String[] clothes;

        Role(String... clothes) {
            this.clothes = clothes;
        }
    }

    /** One woman's MCA look: drawn base first, then the face, the clothes and the hair (tinted). */
    public record Look(ResourceLocation skin, ResourceLocation face, ResourceLocation clothes, ResourceLocation hair,
                       int hairColour) {
    }

    /** Natural hair colours for the grey hair textures, darker for the women of the Nile. */
    private static final int[] HAIR = {0xFF1A1210, 0xFF2E1E14, 0xFF4A2E1C, 0xFF6A3E22, 0xFF8A4A26, 0xFFB07A3A, 0xFFD8B070, 0xFFE8D8B8};
    private static final int[] NILE_HAIR = {0xFF0E0A0A, 0xFF1A1210, 0xFF241812, 0xFF2E1E14};

    private List<ResourceLocation> skins = List.of();
    private List<ResourceLocation> faces = List.of();
    private List<ResourceLocation> hair = List.of();
    private final List<List<ResourceLocation>> clothes = new ArrayList<>();

    private McaSkins() {
    }

    /** True if the women should wear MCA's looks right now. */
    public boolean active() {
        return ModList.get().isLoaded(McaCompat.MODID) && ClientConfig.MCA_SKINS.get() && !skins.isEmpty() && !faces.isEmpty()
                && !hair.isEmpty() && clothes.size() == Role.values().length && clothes.stream().noneMatch(List::isEmpty);
    }

    @Override
    public void onResourceManagerReload(ResourceManager manager) {
        skins = find(manager, "skin/female", true);
        faces = find(manager, "face/normal", false);
        hair = find(manager, "hair/female", false);
        clothes.clear();
        for (Role role : Role.values()) {
            List<ResourceLocation> found = new ArrayList<>();
            for (String folder : role.clothes) {
                found.addAll(find(manager, "clothing/normal/female/" + folder, false));
            }
            clothes.add(found);
        }
        MythsOfWorlds.LOGGER.info("MCA Reborn looks: {} skins, {} faces, {} hairstyles, clothes {}", skins.size(), faces.size(),
                hair.size(), clothes.stream().map(List::size).toList());
    }

    /** MCA's textures in one folder; the grey "classic" skins (tinted by MCA's genetics) are skipped. */
    private static List<ResourceLocation> find(ResourceManager manager, String folder, boolean skipClassic) {
        List<ResourceLocation> found = new ArrayList<>(manager.listResources(ROOT + folder, id -> id.getNamespace().equals(McaCompat.MODID)
                && id.getPath().endsWith(".png") && !id.getPath().endsWith("_overlay.png")
                && !(skipClassic && id.getPath().endsWith("_classic.png"))).keySet());
        found.sort(ResourceLocation::compareTo);
        return List.copyOf(found);
    }

    /** The look of the woman with this UUID, or null to keep the mod's own texture. */
    @Nullable
    public Look look(UUID uuid, Role role) {
        if (!active()) {
            return null;
        }
        long seed = uuid.getMostSignificantBits() ^ (uuid.getLeastSignificantBits() * 31) ^ 0x5DEECE66DL;
        List<ResourceLocation> wear = clothes.get(role.ordinal());
        int[] palette = role == Role.PRIESTESS ? NILE_HAIR : HAIR;
        return new Look(pick(skins, seed, 1), pick(faces, seed, 2), pick(wear, seed, 3), pick(hair, seed, 4),
                palette[Math.floorMod(Long.hashCode(seed * 0x9E3779B97F4A7C15L + 5), palette.length)]);
    }

    private static <T> T pick(List<T> list, long seed, int salt) {
        return list.get(Math.floorMod(Long.hashCode(seed * 0x9E3779B97F4A7C15L + salt * 0x632BE59BD9B4E019L), list.size()));
    }
}
