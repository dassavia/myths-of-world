"""Sounds of Nav and Jotunheim, merged into sounds.json by gen_greek_sounds.py (which also encodes them with --ogg).

Like the Greek ones: voices no vanilla sound fits are synthesized here (the robber's whistle, the three throats of
the Zmey, the Gjallarhorn, the rusalka's song, the music of both worlds); the rest re-voice vanilla sounds.
"""
import numpy as np

from gen_greek_sounds import NS, RATE, bell, envelope, event, hiss, lowpass, own, pluck, t

# event id -> (sounds, Russian subtitle, English subtitle)
SOUNDS = {
    # ---- Nav
    "entity.solovei.whistle": (own("solovei/whistle", 2), "Соловей-разбойник свистит", "Solovei the Robber whistles"),
    "entity.zmey_gorynych.roar": (own("zmey/roar", 2) + [event("minecraft:entity.ender_dragon.growl", 0.8)],
                                  "Змей Горыныч ревёт", "Zmey Gorynych roars"),
    "entity.zmey_gorynych.breath": (own("zmey/breath"), "Змей Горыныч дышит огнём", "Zmey Gorynych breathes fire"),
    "entity.koschei.laugh": (own("koschei/laugh", 2), "Кощей смеётся", "Koschei laughs"),
    "entity.koschei.summon": (own("koschei/summon"), "Кощей поднимает мёртвых", "Koschei raises the dead"),
    "entity.rusalka.song": (own("rusalka/song", 2), "Русалка поёт", "Rusalka sings"),
    "entity.leshy.ambient": (own("leshy/creak", 2), "Леший скрипит", "Leshy creaks"),
    "music.nav.forest": ([{"name": f"{NS}:music/nav_forest", "stream": True}], None, None),
    "music.nav.dark": ([{"name": f"{NS}:music/nav_dark", "stream": True}], None, None),
    # ---- Jotunheim
    "entity.heimdall.gjallarhorn": (own("heimdall/gjallarhorn"), "Хеймдалль трубит в Гьяллархорн", "Heimdall blows the Gjallarhorn"),
    "entity.thrym.stomp": (own("thrym/stomp", 2), "Трим топает", "Thrym stomps"),
    "entity.surtr.flames": (own("surtr/flames"), "Пламя Сурта", "Surtr's flames"),
    "entity.draugr_chieftain.call": (own("draugr/call"), "Вождь драугров зовёт мёртвых", "Draugr chieftain calls the dead"),
    "entity.fenrir.howl": (own("fenrir/howl") + [event("minecraft:entity.wolf.howl", 0.45)], "Фенрир воет", "Fenrir howls"),
    "entity.garm.howl": ([event("minecraft:entity.wolf.howl", 0.4), event("minecraft:entity.wolf.growl", 0.5)],
                         "Гарм воет", "Garm howls"),
    "music.jotunheim.north": ([{"name": f"{NS}:music/jotunheim_north", "stream": True}], None, None),
    "music.jotunheim.niflheim": ([{"name": f"{NS}:music/jotunheim_niflheim", "stream": True}], None, None),
}


def place(out, sound, at):
    start = int(RATE * at)
    if start >= len(out):
        return
    part = sound[:len(out) - start]
    out[start:start + len(part)] += part


def saw(freq, x):
    """A band-limited-ish sawtooth: the first harmonics only."""
    return sum(np.sin(2 * np.pi * freq * k * x) / k for k in range(1, 9))


def whistle(rng, seed):
    """Two fingers in the mouth: a piercing rising whistle that warbles, then a long shriek."""
    x = t(1.5)
    f = 2200 + 900 * np.minimum(x / 0.25, 1.0) + 120 * np.sin(2 * np.pi * (7 + 2 * seed) * x)
    phase = 2 * np.pi * np.cumsum(f) / RATE
    tone = np.sin(phase) + 0.2 * np.sin(2 * phase)
    breath = hiss(1.5, rng, 0.8, 9.0) * 0.25
    return (tone * envelope(len(x), 0.03, 0.4) + breath) * (1.0 - 0.3 * seed * (x > 0.7))


def roar(rng, seed):
    """Three throats at once, a little apart: low saw growls through a rough throat."""
    out = np.zeros(int(RATE * 2.2))
    for head, base in enumerate((62.0, 74.0, 88.0)):
        x = t(1.9)
        f = base * (1 + 0.15 * np.sin(2 * np.pi * 0.6 * x)) * (1 + 0.1 * seed)
        voice = saw(1, np.cumsum(f) / RATE) * (0.6 + 0.4 * lowpass(rng.normal(0, 1, len(x)), 0.01) * 8)
        place(out, lowpass(voice, 0.08) * envelope(len(x), 0.15, 0.8), 0.12 * head)
    return out + lowpass(rng.normal(0, 1, len(out)), 0.05) * 0.6 * envelope(len(out), 0.2, 1.0)


def fire_breath(rng, seed):
    x = t(1.6)
    roar_ = lowpass(rng.normal(0, 1, len(x)), 0.12) * (1.0 + np.sin(2 * np.pi * 3 * x) * 0.3)
    crackle = (rng.random(len(x)) < 0.003) * rng.normal(0, 1, len(x)) * 3
    return (roar_ * 2 + crackle) * envelope(len(x), 0.08, 0.6)


def laugh(rng, seed):
    """A dry cackle: bursts of breath over a low voice falling in pitch."""
    out = np.zeros(int(RATE * 1.6))
    count = 5 + seed
    for k in range(count):
        x = t(0.16)
        f = (180 - 12 * k) * (1.1 if seed else 1.0)
        burst = (np.sin(2 * np.pi * f * x) + 0.5 * np.sin(4 * np.pi * f * x) + hiss(0.16, rng, 0.5, 30.0) * 0.6)
        place(out, burst * envelope(len(x), 0.01, 0.1), 0.05 + k * 0.2)
    return out


def koschei_summon(rng, seed):
    """Bones rattle out of the earth over a low rising drone."""
    x = t(2.2)
    drone = np.sin(2 * np.pi * (45 + 25 * x) * x) * envelope(len(x), 0.5, 0.6)
    clicks = (rng.random(len(x)) < 0.004 * (x / 2.2)) * 1.0
    rattle = lowpass(clicks * rng.normal(0, 3, len(x)), 0.6)
    return drone * 0.7 + rattle + hiss(2.2, rng, 0.5, 2.0) * 0.2


def song(rng, seed):
    """A wordless song in a minor key: a breathy voice with vibrato and a soft second harmonic."""
    melody = [[440.0, 523.3, 493.9, 440.0, 392.0, 440.0], [329.6, 392.0, 440.0, 392.0, 349.2, 329.6]][seed]
    out = np.zeros(int(RATE * 3.6))
    pos = 0.0
    for f in melody:
        x = t(0.6)
        vib = 1 + 0.008 * np.sin(2 * np.pi * 5.0 * x)
        phase = 2 * np.pi * np.cumsum(f * vib) / RATE
        voice = np.sin(phase) + 0.3 * np.sin(2 * phase) + 0.1 * np.sin(3 * phase)
        place(out, voice * envelope(len(x), 0.12, 0.25), pos)
        pos += 0.55
    return out + hiss(3.6, rng, 0.7, 1.0) * 0.05


def creak(rng, seed):
    """Wood bending: a stick-slip train of clicks that slows down, and leaves rustling."""
    x = t(1.4)
    rate = 40 + 30 * np.sin(2 * np.pi * (0.4 + 0.2 * seed) * x) + rng.normal(0, 3, len(x))
    phase = np.cumsum(rate) / RATE
    clicks = (np.diff(np.floor(phase), prepend=0) > 0) * 1.0
    wood = lowpass(clicks * 6, 0.3) - lowpass(clicks * 6, 0.05)
    rustle = hiss(1.4, rng, 0.75, 5.0) * 0.3
    return wood * envelope(len(x), 0.1, 0.4) + rustle


def horn_note(freq, seconds, rng):
    """A long brass horn: harmonics swelling in, a slight rise in pitch and vibrato."""
    x = t(seconds)
    f = freq * (1 + 0.02 * np.minimum(x / 0.4, 1.0)) * (1 + 0.004 * np.sin(2 * np.pi * 4.5 * x))
    phase = 2 * np.pi * np.cumsum(f) / RATE
    swell = np.minimum(x / 0.5, 1.0)
    tone = sum((swell ** (k * 0.5)) * np.sin(k * phase) / k for k in range(1, 10))
    return tone * envelope(len(x), 0.1, seconds * 0.35)


def echo(sound, delay=0.23, feedback=0.4, taps=4):
    out = np.concatenate([sound, np.zeros(int(RATE * delay * taps))])
    for k in range(1, taps + 1):
        place(out, sound * feedback ** k, delay * k)
    return out


def gjallarhorn(rng, seed):
    return echo(horn_note(98.0, 2.6, rng) + 0.5 * horn_note(147.0, 2.6, rng), 0.31, 0.45)


def ice_stomp(rng, seed):
    x = t(1.1)
    boom = np.sin(2 * np.pi * (42 - 15 * x) * x) * np.exp(-x * 4)
    crack = (rng.random(len(x)) < 0.01 * np.exp(-x * 6)) * rng.normal(0, 4, len(x))
    rubble = lowpass(rng.normal(0, 1, len(x)), 0.04) * np.exp(-x * 3) * (0.6 + 0.2 * seed)
    return boom * 1.4 + (crack - lowpass(crack, 0.3)) + rubble


def flames(rng, seed):
    x = t(2.0)
    body = lowpass(rng.normal(0, 1, len(x)), 0.06) * 3 * (0.7 + 0.3 * np.sin(2 * np.pi * 1.3 * x))
    crackle = (rng.random(len(x)) < 0.004) * rng.normal(0, 1, len(x)) * 4
    return (body + crackle) * envelope(len(x), 0.2, 0.7)


def draugr_call(rng, seed):
    x = t(2.0)
    f = 82 * (1 + 0.05 * np.sin(2 * np.pi * 0.8 * x))
    moan = saw(1, np.cumsum(f) / RATE)
    return lowpass(moan, 0.05) * envelope(len(x), 0.4, 0.8) * 2 + hiss(2.0, rng, 0.4, 1.5) * 0.3


def howl(rng, seed):
    x = t(2.6)
    f = 230 + 160 * np.sin(np.pi * np.minimum(x / 2.2, 1.0)) + 6 * np.sin(2 * np.pi * 5.5 * x)
    phase = 2 * np.pi * np.cumsum(f) / RATE
    voice = np.sin(phase) + 0.35 * np.sin(2 * phase) + 0.15 * np.sin(3 * phase)
    return echo(voice * envelope(len(x), 0.3, 0.9), 0.4, 0.3, 3)


def reed(freq, seconds, rng):
    """A zhaleika: a bright reed pipe."""
    x = t(seconds)
    phase = 2 * np.pi * freq * (1 + 0.005 * np.sin(2 * np.pi * 6 * x)) * x
    tone = np.tanh(2.5 * np.sin(phase)) * 0.6 + 0.2 * np.sin(2 * phase)
    return lowpass(tone, 0.3) * envelope(len(x), 0.04, seconds * 0.4)


def nav_forest(rng, seed):
    """About a minute of gusli and a reed pipe in D dorian over a soft fifth: the deep forests of Nav."""
    seconds = 62.0
    x = t(seconds)
    out = 0.07 * (np.sin(2 * np.pi * 73.4 * x) + 0.6 * np.sin(2 * np.pi * 110.0 * x)) * envelope(len(x), 4.0, 6.0)
    scale = [293.7, 329.6, 349.2, 392.0, 440.0, 493.9, 523.3, 587.3]
    pos, i = 1.5, 0
    while pos < seconds - 5:
        if i % 8 == 0:
            for k, f in enumerate((146.8, 220.0, 293.7)):
                place(out, pluck(f, 3.0, rng, 0.998) * 0.45, pos + 0.04 * k)
        if rng.random() < 0.7:
            place(out, pluck(scale[rng.integers(len(scale))], 1.8, rng, 0.997) * 0.6, pos)
        if i % 16 == 12:
            for k in range(4):
                place(out, reed(scale[rng.integers(3, len(scale))], 0.45, rng) * 0.35, pos + 0.45 * k)
        pos += 0.55 * (2 if rng.random() < 0.2 else 1)
        i += 1
    return out * envelope(len(out), 2.0, 4.0)


def nav_dark(rng, seed):
    """About a minute of low drones, wind and a far-off bell: the bog and the deathless king's land."""
    seconds = 60.0
    x = t(seconds)
    drone = (np.sin(2 * np.pi * 49.0 * x + 2 * np.sin(2 * np.pi * 0.04 * x)) + 0.5 * np.sin(2 * np.pi * 73.4 * x)
             + 0.35 * np.sin(2 * np.pi * 103.8 * x)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.025 * x))
    wind = lowpass(rng.normal(0, 1, len(x)), 0.008) * 6 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.06 * x))
    out = drone * 0.5 + wind
    for k in range(6):
        place(out, bell(rng.choice([196.0, 207.7, 155.6]), 7.0) * 0.3, 5 + k * 9 + rng.uniform(0, 2))
    for k in range(10):
        place(out, pluck(rng.choice([73.4, 98.0, 110.0]), 3.0, rng, 0.999) * 0.4, 3 + k * 5.5)
    return out * envelope(len(out), 4.0, 6.0)


def drum(rng):
    x = t(0.6)
    return np.sin(2 * np.pi * (70 - 30 * x) * x) * np.exp(-x * 7) + lowpass(rng.normal(0, 1, len(x)), 0.1) * np.exp(-x * 25) * 0.5


def jotunheim_north(rng, seed):
    """About a minute of a low drone, a slow frame drum, kantele plucks and horn calls across the fjords."""
    seconds = 64.0
    x = t(seconds)
    out = 0.08 * (np.sin(2 * np.pi * 73.4 * x) + 0.7 * np.sin(2 * np.pi * 110.0 * x)) * envelope(len(x), 4.0, 6.0)
    beat = 1.1
    pos = 2.0
    k = 0
    scale = [293.7, 349.2, 392.0, 440.0, 523.3, 587.3]  # D minor pentatonic
    while pos < seconds - 5:
        place(out, drum(rng) * (0.6 if k % 4 else 0.9), pos)
        if rng.random() < 0.5:
            place(out, pluck(scale[rng.integers(len(scale))], 2.2, rng, 0.997) * 0.4, pos + beat / 2)
        if k % 12 == 6:
            place(out, horn_note(rng.choice([146.8, 110.0, 196.0]), 3.0, rng) * 0.25, pos)
        pos += beat
        k += 1
    return out * envelope(len(out), 2.0, 4.0)


def jotunheim_niflheim(rng, seed):
    """About a minute of cold wind, a hollow drone and high icy bells: the mists of Niflheim."""
    seconds = 60.0
    x = t(seconds)
    wind = lowpass(rng.normal(0, 1, len(x)), 0.015) * 7 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * x))
    drone = (np.sin(2 * np.pi * 55.0 * x) + 0.4 * np.sin(2 * np.pi * 82.4 * x)) * 0.35
    out = wind + drone
    for k in range(12):
        place(out, bell(rng.choice([1318.5, 1567.98, 1975.5, 2349.3]), 4.0) * 0.12, 3 + k * 4.5 + rng.uniform(0, 1.5))
    return out * envelope(len(out), 4.0, 6.0)


SYNTHS = {
    "solovei/whistle": whistle,
    "zmey/roar": roar,
    "zmey/breath": fire_breath,
    "koschei/laugh": laugh,
    "koschei/summon": koschei_summon,
    "rusalka/song": song,
    "leshy/creak": creak,
    "music/nav_forest": nav_forest,
    "music/nav_dark": nav_dark,
    "heimdall/gjallarhorn": gjallarhorn,
    "thrym/stomp": ice_stomp,
    "surtr/flames": flames,
    "draugr/call": draugr_call,
    "fenrir/howl": howl,
    "music/jotunheim_north": jotunheim_north,
    "music/jotunheim_niflheim": jotunheim_niflheim,
}
