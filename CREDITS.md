# Credits and licences of third-party assets

Everything not listed here (code, textures, models, structures, synthesized sounds) is original work of the mod
and falls under the mod's licence.

## Fonts

| File | Font | Author | Licence |
|------|------|--------|---------|
| `assets/mythsofworlds/font/carlito_regular.ttf`, `carlito_bold.ttf` | Carlito | tyPoland Łukasz Dziedzic, The Carlito Project Authors (https://github.com/googlefonts/carlito) | SIL Open Font License 1.1, see `assets/mythsofworlds/font/OFL-carlito.txt` |

Carlito is used unmodified. It covers the full Cyrillic alphabet (А–Я, а–я, Ё, ё) and is the font of the mod's HUD
(`font/myth.json`) and of the Codex of Myths (`font/codex.json`); both fall back to the vanilla font for any glyph
it lacks.

## Sounds

All of the mod's own sounds (`assets/mythsofworlds/sounds/**/*.ogg`) are procedurally synthesized by
`tools/gen_greek_sounds.py` with numpy and encoded with ffmpeg (Vorbis, mono, 44.1 kHz). No recordings and no
third-party audio are used, so they are original work of the mod. The other creatures reuse vanilla Minecraft sounds
by reference through `sounds.json` (nothing of them is copied into the jar).

| Files | Sound | Source |
|-------|-------|--------|
| `sounds/isis/{ambient1-3,idle1-2,hurt1-2,death,yes,no}.ogg` | The voice of Isis: a small choir singing on vowel formants, a low choir pad, golden chimes and the rattle of her sistrum | synthesized, `isis_*` in `tools/gen_greek_sounds.py` (`python3 tools/gen_greek_sounds.py --ogg=isis/`) |
| all other `sounds/**/*.ogg` | pan flute, lyre, hisses, stomps, chimes, music of Hellas | synthesized in the same script |
