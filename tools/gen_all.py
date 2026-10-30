"""
Runs every generator of the mod's data and assets in the order they depend on each other.

    python3 tools/gen_all.py            # rewrite the JSON, .nbt and the 32x32 art from the tables in tools/
    python3 tools/gen_all.py --textures # also redraw the placeholder PNGs of the first generators (overwrites them)
    python3 tools/gen_all.py --check    # regenerate, then fail if anything differs from what is committed (used by CI)

Each generator reads helpers from the ones before it, so the order below matters. The logo (gen_logo.py) and the
.ogg sounds (gen_greek_sounds.py --ogg) are left out: they are drawn once and kept as they are.
"""
import os
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)

# (script, takes --textures)
CHAIN = [
    ("gen_greek_assets.py", True),
    ("gen_greek_sounds.py", False),
    ("gen_norse_assets.py", True),
    ("gen_metals.py", True),
    ("gen_relics.py", True),
    ("gen_slavic_assets.py", True),
    ("gen_codex.py", False),
    ("gen_book.py", False),
    ("hd_textures.py", False),
    ("gen_art32_items.py", False),
    ("gen_art32_blocks.py", False),
    ("gen_gui.py", False),
    ("gen_3d_armour.py", False),
    ("gen_3d_gear.py", False),
    ("gen_geo_models.py", False),
]


def main(args):
    textures = "--textures" in args
    for script, accepts_textures in CHAIN:
        if not os.path.exists(os.path.join(TOOLS, script)):
            continue
        command = [sys.executable, os.path.join(TOOLS, script)]
        if textures and accepts_textures:
            command.append("--textures")
        print(f"== {script}", flush=True)
        subprocess.run(command, cwd=ROOT, check=True)
    if "--check" in args:
        changed = subprocess.run(["git", "status", "--porcelain", "--", "src/main/resources"], cwd=ROOT,
                                 check=True, capture_output=True, text=True).stdout
        if changed.strip():
            print("The generated resources differ from the tables in tools/. Run python3 tools/gen_all.py and commit:")
            print(changed)
            subprocess.run(["git", "--no-pager", "diff", "--stat", "--", "src/main/resources"], cwd=ROOT)
            sys.exit(1)
        print("Generated resources are up to date.")


if __name__ == "__main__":
    main(sys.argv[1:])
