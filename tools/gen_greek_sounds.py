"""Sounds of Hellas: writes assets/mythsofworlds/sounds.json and synthesizes the custom .ogg files.

Most creatures are voiced by vanilla sounds re-pitched through "event" references; the sounds no vanilla
sound fits (pan flute, lyre, Medusa's hiss, the brazier flaring up...) are synthesized here with numpy and
encoded with ffmpeg. Run from the repository root: python3 tools/gen_greek_sounds.py [--ogg]
"""
import json
import os
import subprocess
import sys
import tempfile
import wave

import numpy as np

NS = "mythsofworlds"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources", "assets", NS)
RATE = 44100


def event(name, pitch=1.0, volume=1.0, weight=1):
    entry = {"name": name, "type": "event"}
    if pitch != 1.0:
        entry["pitch"] = pitch
    if volume != 1.0:
        entry["volume"] = volume
    if weight != 1:
        entry["weight"] = weight
    return entry


def own(name, count=1, volume=1.0):
    files = [f"{NS}:{name}{i + 1 if count > 1 else ''}" for i in range(count)]
    return [{"name": f, "volume": volume} if volume != 1.0 else f for f in files]


# event id -> (sounds, Russian subtitle, English subtitle)
SOUNDS = {
    "entity.satyr.pan_flute": (own("satyr/pan_flute", 3), "Сатир играет на свирели", "Satyr plays the pan flute"),
    "entity.satyr.ambient": ([event("minecraft:entity.goat.ambient", 1.3), event("minecraft:entity.goat.screaming.ambient", 1.4)],
                             "Сатир хохочет", "Satyr laughs"),
    "entity.harpy.ambient": ([event("minecraft:entity.parrot.ambient", 0.55), event("minecraft:entity.phantom.ambient", 1.4)],
                             "Гарпия кричит", "Harpy screeches"),
    "entity.harpy.hurt": ([event("minecraft:entity.parrot.hurt", 0.6)], "Гарпия ранена", "Harpy hurts"),
    "entity.harpy.death": ([event("minecraft:entity.phantom.death", 1.3)], "Гарпия погибает", "Harpy dies"),
    "entity.shade.ambient": ([event("minecraft:entity.vex.ambient", 0.55), event("minecraft:particle.soul_escape", 0.8, 2.0)],
                             "Тень стонет", "Shade moans"),
    "entity.shade.hurt": ([event("minecraft:entity.vex.hurt", 0.6)], "Тень ранена", "Shade hurts"),
    "entity.shade.death": ([event("minecraft:entity.vex.death", 0.5)], "Тень рассеивается", "Shade fades"),
    "entity.shade.teleport": (own("shade/blink"), "Тень переносится", "Shade blinks"),
    "entity.minotaur.ambient": ([event("minecraft:entity.ravager.ambient", 0.75), event("minecraft:entity.cow.ambient", 0.45)],
                                "Минотавр фыркает", "Minotaur snorts"),
    "entity.minotaur.roar": ([event("minecraft:entity.ravager.roar", 0.7)], "Минотавр ревёт", "Minotaur roars"),
    "entity.minotaur.hurt": ([event("minecraft:entity.ravager.hurt", 0.8)], "Минотавр ранен", "Minotaur hurts"),
    "entity.minotaur.death": ([event("minecraft:entity.ravager.death", 0.7)], "Минотавр погибает", "Minotaur dies"),
    "entity.hydra.ambient": ([event("minecraft:entity.hoglin.ambient", 0.6)] + own("hydra/hiss", 2),
                             "Гидра шипит", "Hydra hisses"),
    "entity.hydra.spit": (own("hydra/spit", 2), "Гидра плюёт ядом", "Hydra spits venom"),
    "entity.hydra.hurt": ([event("minecraft:entity.hoglin.hurt", 0.7)], "Гидра ранена", "Hydra hurts"),
    "entity.hydra.death": ([event("minecraft:entity.ender_dragon.growl", 1.2)], "Гидра погибает", "Hydra dies"),
    "entity.cerberus.ambient": ([event("minecraft:entity.wolf.growl", 0.5)], "Цербер рычит", "Cerberus growls"),
    "entity.cerberus.breath": ([event("minecraft:entity.blaze.shoot", 0.7), event("minecraft:item.firecharge.use", 0.6)],
                               "Цербер изрыгает пламя", "Cerberus breathes fire"),
    "entity.cerberus.hurt": ([event("minecraft:entity.wolf.hurt", 0.5)], "Цербер ранен", "Cerberus hurts"),
    "entity.cerberus.death": ([event("minecraft:entity.wolf.death", 0.5)], "Цербер погибает", "Cerberus dies"),
    "entity.cyclops.ambient": ([event("minecraft:entity.ravager.ambient", 0.55)], "Циклоп ворчит", "Cyclops grumbles"),
    "entity.cyclops.stomp": (own("cyclops/stomp", 2), "Циклоп топает", "Cyclops stomps"),
    "entity.cyclops.hurt": ([event("minecraft:entity.iron_golem.hurt", 0.6)], "Циклоп ранен", "Cyclops hurts"),
    "entity.cyclops.death": ([event("minecraft:entity.iron_golem.death", 0.6)], "Циклоп погибает", "Cyclops dies"),
    "entity.medusa.ambient": (own("medusa/hiss", 2) + [event("minecraft:entity.cat.hiss", 0.7)],
                              "Змеи Медузы шипят", "Medusa's snakes hiss"),
    "entity.medusa.gaze": (own("medusa/gaze"), "Взгляд Медузы", "Medusa's gaze"),
    "entity.medusa.hurt": ([event("minecraft:entity.witch.hurt", 0.8)], "Медуза ранена", "Medusa hurts"),
    "entity.medusa.death": ([event("minecraft:entity.witch.death", 0.8)], "Медуза погибает", "Medusa dies"),
    "entity.nemean_lion.ambient": ([event("minecraft:entity.polar_bear.warning", 0.6)], "Лев рычит", "Lion growls"),
    "entity.nemean_lion.hurt": ([event("minecraft:entity.polar_bear.hurt", 0.7)], "Лев ранен", "Lion hurts"),
    "entity.nemean_lion.death": ([event("minecraft:entity.polar_bear.death", 0.6)], "Лев погибает", "Lion dies"),
    "entity.greek_merchant.greet": (own("greek_merchant/lyre", 2), "Торговец приветствует вас", "Merchant greets you"),
    "block.brazier.ignite": (own("block/brazier_ignite"), "Священный огонь вспыхивает", "Sacred fire flares up"),
}


# ---------------------------------------------------------------- synthesis

def t(seconds):
    return np.arange(int(RATE * seconds)) / RATE


def envelope(n, attack=0.01, release=0.2):
    env = np.ones(n)
    a, r = int(RATE * attack), int(RATE * release)
    env[:a] = np.linspace(0, 1, a)
    if r:
        env[-r:] *= np.linspace(1, 0, r)
    return env


def lowpass(x, alpha):
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += alpha * (v - acc)
        y[i] = acc
    return y


def flute_note(freq, seconds, rng):
    x = t(seconds)
    vibrato = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * x)
    tone = np.sin(2 * np.pi * freq * vibrato * x) + 0.25 * np.sin(4 * np.pi * freq * x) + 0.08 * np.sin(6 * np.pi * freq * x)
    breath = lowpass(rng.normal(0, 1, len(x)), 0.15) * 0.35
    return (tone + breath * (0.6 + 0.4 * np.sin(2 * np.pi * freq * x))) * envelope(len(x), 0.06, seconds * 0.5)


def pan_flute(rng, seed):
    scale = [392.0, 440.0, 523.3, 587.3, 659.3, 784.0]  # G major pentatonic
    notes = []
    for _ in range(rng.integers(3, 6)):
        notes.append(flute_note(scale[rng.integers(len(scale))], float(rng.choice([0.18, 0.25, 0.4])), rng))
    return np.concatenate(notes)


def pluck(freq, seconds, rng, decay=0.996):
    """Karplus-Strong plucked string: a lyre."""
    n = int(RATE * seconds)
    period = int(RATE / freq)
    buf = rng.uniform(-1, 1, period)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % period]
        buf[i % period] = decay * 0.5 * (buf[i % period] + buf[(i + 1) % period])
    return out


def lyre(rng, seed):
    chord = [293.7, 370.0, 440.0, 587.3] if seed == 0 else [261.6, 329.6, 392.0, 523.3]
    total = np.zeros(int(RATE * 1.4))
    for k, f in enumerate(chord):
        start = int(RATE * 0.09 * k)
        note = pluck(f, 1.4 - 0.09 * k, rng)[:len(total) - start]
        total[start:start + len(note)] += note
    return total * envelope(len(total), 0.002, 0.4)


def hiss(seconds, rng, bright=0.6, wobble=6.0):
    x = t(seconds)
    noise = rng.normal(0, 1, len(x))
    noise = noise - lowpass(noise, 1 - bright)  # high-pass
    return noise * (0.6 + 0.4 * np.sin(2 * np.pi * wobble * x)) * envelope(len(x), 0.08, seconds * 0.6)


def medusa_hiss(rng, seed):
    return hiss(0.7 + 0.3 * seed, rng, wobble=9.0 + seed * 4)


def medusa_gaze(rng, seed):
    x = t(1.6)
    drone = np.sin(2 * np.pi * 110 * x + 3 * np.sin(2 * np.pi * 0.7 * x)) * 0.5 + np.sin(2 * np.pi * 116.5 * x) * 0.4
    return drone * envelope(len(x), 0.3, 0.8) + hiss(1.6, rng, 0.7, 3.0) * 0.6


def hydra_hiss(rng, seed):
    x = t(0.9)
    return hiss(0.9, rng, 0.45, 4.0 + seed * 3) + 0.3 * np.sin(2 * np.pi * (70 + 10 * seed) * x) * envelope(len(x), 0.1, 0.5)


def hydra_spit(rng, seed):
    x = t(0.35)
    wet = rng.normal(0, 1, len(x)) * np.exp(-x * 14)
    blob = np.sin(2 * np.pi * (300 - 500 * x) * x) * np.exp(-x * 10)
    return lowpass(wet, 0.35 + 0.1 * seed) + blob * 0.6


def stomp(rng, seed):
    x = t(0.9)
    boom = np.sin(2 * np.pi * (55 - 20 * x) * x) * np.exp(-x * 5)
    crack = lowpass(rng.normal(0, 1, len(x)), 0.2) * np.exp(-x * 18)
    rubble = lowpass(rng.normal(0, 1, len(x)), 0.05) * np.exp(-x * 4) * (0.5 + 0.2 * seed)
    return boom * 1.2 + crack * 0.8 + rubble


def blink(rng, seed):
    x = t(0.6)
    sweep = np.sin(2 * np.pi * (1800 * x * x + 400 * x)) * envelope(len(x), 0.2, 0.25)
    return (sweep * 0.5 + hiss(0.6, rng, 0.8, 12.0) * 0.4)[::-1].copy()


def brazier_ignite(rng, seed):
    x = t(1.6)
    whoosh = lowpass(rng.normal(0, 1, len(x)), 0.08) * np.exp(-((x - 0.25) ** 2) / 0.03) * 3
    crackle = (rng.random(len(x)) < 0.002) * rng.normal(0, 1, len(x)) * np.exp(-x * 1.5) * 4
    chime = sum(np.sin(2 * np.pi * f * x) * np.exp(-x * 2.5) for f in (880.0, 1318.5, 1760.0)) / 3
    return whoosh + crackle + chime * 0.5 * (x > 0.2)


SYNTHS = {
    "satyr/pan_flute": pan_flute,
    "greek_merchant/lyre": lyre,
    "medusa/hiss": medusa_hiss,
    "medusa/gaze": medusa_gaze,
    "hydra/hiss": hydra_hiss,
    "hydra/spit": hydra_spit,
    "cyclops/stomp": stomp,
    "shade/blink": blink,
    "block/brazier_ignite": brazier_ignite,
}


def write_ogg(samples, path):
    samples = samples / max(1e-6, np.max(np.abs(samples))) * 0.85
    pcm = (samples * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path, "-c:a", "libvorbis", "-q:a", "4", "-ac", "1", path],
                   check=True)
    os.remove(wav_path)


def main():
    sounds = {}
    for key, (entries, ru, en) in SOUNDS.items():
        sounds[key] = {"subtitle": f"subtitles.{NS}.{key}", "sounds": entries}
    with open(os.path.join(ROOT, "sounds.json"), "w", encoding="utf-8") as f:
        json.dump(sounds, f, indent=2, ensure_ascii=False)
        f.write("\n")
    for index, code in ((0, "ru_ru"), (1, "en_us")):
        path = os.path.join(ROOT, "lang", f"{code}.json")
        with open(path, encoding="utf-8") as f:
            lang = json.load(f)
        for key, (_, ru, en) in SOUNDS.items():
            lang[f"subtitles.{NS}.{key}"] = (ru, en)[index]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(lang, f, indent=2, ensure_ascii=False)
            f.write("\n")
    if "--ogg" in sys.argv:
        for key, (entries, _, _) in SOUNDS.items():
            for entry in entries:
                name = entry if isinstance(entry, str) else entry["name"]
                if isinstance(entry, dict) and entry.get("type") == "event":
                    continue
                file = name.split(":", 1)[1]
                base = file.rstrip("0123456789")
                seed = int(file[len(base):] or 1) - 1
                rng = np.random.default_rng(seed * 7919 + len(file))
                write_ogg(SYNTHS[base](rng, seed), os.path.join(ROOT, "sounds", f"{file}.ogg"))


if __name__ == "__main__":
    main()
