"""An isorhythmic motet composer, pure standard library (no audio deps).

"Ars subtilior" (the later, more subtle art, ~14th century France) is famous
for rhythmic intricacy: isorhythm (a fixed rhythm pattern — the *talea* —
repeated against a slowly rotating pitch pattern — the *color*), hockets,
and highly syncopated upper voices.

This module composes a small three-voice motet — triplum and motetus
hocketing over a low tenor — with phrase lengths that never match, so the
rhythms and melodies sheer against each other the way the old masters did.
Output is a 16-bit PCM WAV in Dorian (the church mode). No dependencies
beyond the standard library.
"""

import array
import math
import random
import time
import wave

SR = 44100

DORIAN = [0, 2, 3, 5, 7, 9, 10]


def dorian_scale(root):
    """Degree 0..n over ~2 octaves from ``root`` (a midi int)."""
    notes = []
    for octave in range(3):
        for d in DORIAN:
            notes.append(root + 12 * octave + d)
    return notes


class Voice:
    def __init__(self, root, rhythm, color, register, volume, timbre):
        self.scale = dorian_scale(root)
        self.rhythm = rhythm
        self.color = color
        self.register = register
        self.volume = volume
        self.timbre = timbre

    @property
    def phrase(self):
        return sum(self.rhythm)


def build_events(voices, total_units):
    """Return [(start, dur, midi, volume, timbre)] for every voice.

    Hocket: when triplum and motetus would sound at once, keep the earlier
    note and drop the overlapping one so the two never clash in time (the
    medieval hocket).
    """
    events = []
    for voice in voices:
        phrase = voice.phrase
        phrase_index = 0
        cursor = 0
        while cursor < total_units:
            for slot, dur in enumerate(voice.rhythm):
                if cursor >= total_units:
                    break
                degree = voice.color[(phrase_index + slot) % len(voice.color)]
                midi = voice.scale[degree + voice.register]
                events.append((cursor, dur, midi, voice.volume, voice.timbre))
                cursor += dur
            phrase_index += 1
            if phrase == 0:
                break

    events_by_start = sorted(events, key=lambda e: e[0])
    kept = []
    last_upper_end = 0
    for start, dur, midi, vol, timbre in events_by_start:
        if timbre == "tenor":
            kept.append((start, dur, midi, vol, timbre))
            continue
        if start < last_upper_end:
            continue
        kept.append((start, dur, midi, vol, timbre))
        last_upper_end = start + dur
    return kept


def tone(midi, dur, vol, timbre, sr=SR):
    if midi <= 0 or dur <= 0:
        return None
    freq = 440.0 * (2.0 ** ((midi - 69) / 12.0))
    n = max(1, int(dur * sr))
    if timbre == "tenor":
        amps = [(1.0, 1.0), (2.0, 0.22), (3.0, 0.08)]
    else:
        amps = [(1.0, 1.0), (2.0, 0.42), (3.0, 0.16)]
    out = array.array("f")
    pi2 = 2.0 * math.pi
    attack = max(1, int(0.012 * sr)) if timbre != "tenor" else max(1, int(0.05 * sr))
    sustain = n - attack
    for i in range(n):
        if i < attack:
            env = i / attack
        elif timbre == "tenor":
            env = 1.0 - 0.25 * (i / n)
        else:
            env = math.exp(-2.6 * (i - attack) / max(1, attack))
        t = i / sr
        if timbre == "tenor":
            freq_now = freq * (1.0 + 0.005 * math.sin(pi2 * 5.0 * t))
        else:
            freq_now = freq
        s = 0.0
        for mult, amp in amps:
            s += amp * math.sin(pi2 * freq_now * mult * t)
        out.append(s * env * vol)
    return out


def synthesize(events, total_units, unit, sr=SR):
    total_samples = int(total_units * unit * sr) + int(1.5 * sr)
    mix = array.array("f", (0.0 for _ in range(total_samples)))
    for start, dur, midi, vol, timbre in events:
        tonebuf = tone(midi, dur, vol, timbre, sr)
        if tonebuf is None:
            continue
        offset = int(start * unit * sr)
        for i, sample in enumerate(tonebuf):
            j = offset + i
            if j < total_samples:
                mix[j] += sample
    peak = max(1e-6, max(abs(s) for s in mix))
    gain = 0.86 / peak
    return array.array("h", (int(max(-32767, min(32767, s * gain * 32767))) for s in mix))


def write_wav(path, samples, sr=SR):
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(samples.tobytes())


COMPOSERS = {
    "subtilior": dict(
        measure_units=12,
        voices=[
            Voice(
                root=38,
                rhythm=[12, 12, 12, 12],
                color=[d for d in range(4)],
                register=0,
                volume=0.5,
                timbre="tenor",
            ),
            Voice(
                root=50,
                rhythm=[3, 3, 6, 3, 3, 6],
                color=[8, 9, 10, 11, 10, 9],
                register=0,
                volume=0.34,
                timbre="bell",
            ),
            Voice(
                root=55,
                rhythm=[2, 4, 2, 4, 2, 4],
                color=[11, 12, 14, 12, 11, 10],
                register=0,
                volume=0.30,
                timbre="bell",
            ),
        ],
    ),
}


def compose(measures=16, bpm=88.0, seed=None):
    cfg = COMPOSERS["subtilior"]
    unit = 60.0 / (bpm * 4.0)
    total_units = int(measures * cfg["measure_units"])
    rng = random.Random(seed)
    rng.randrange(1)
    events = build_events(cfg["voices"], total_units)
    return events, total_units, unit


def main(bpm=88.0, measures=16, out=None, play=False, seed=None):
    if seed is None:
        seed = int(time.time()) % 100000
    events, total_units, unit = compose(measures=measures, bpm=bpm, seed=seed)
    samples = synthesize(events, total_units, unit)
    path = out or f"ars-subtilior-{seed}.wav"
    write_wav(path, samples)
    seconds = len(samples) / SR
    print(
        f"composed {measures} measures, {len(events)} notes, "
        f"{seconds:.1f}s -> {path}"
    )
    if play:
        _try_play(path)
    return 0


def _try_play(path):
    import shutil
    import subprocess

    commands = [
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path],
        ["paplay", path],
        ["pw-play", path],
        ["aplay", "-q", path],
    ]
    for cmd in commands:
        if shutil.which(cmd[0]):
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError:
                pass
            return
    print(f"no player found; open {path} in your music player")


if __name__ == "__main__":
    main()