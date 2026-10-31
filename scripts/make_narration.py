#!/usr/bin/env python3
"""Generate Cantonese narration with the macOS voice, and report whether each
line fits the window it has to sit in.

The voice is Sinji (zh_HK) at rate 230. Do not pitch-shift it: that was tried
at +10/15/20/25% to sound younger and it reads as processed. If a younger or
more natural voice is wanted, it needs a different engine, not this one.

Each clip is then:
  despiked      `say` emits occasional single-sample full-scale clicks
  normalised    to RMS 0.145, which is what every existing clip sits at
  soft-limited  tanh above 0.8 instead of clipping the transients

Lines come from a JSON file:

    [ { "id": "f1", "text": "右路角球。五號開波。", "budget": 95 }, ... ]

`budget` is the number of frames at 30 fps the line must fit inside — normally
the gap to the next line's start, minus a few frames of air.

    python3 make_narration.py lines.json --out public/audio
    python3 make_narration.py lines.json --out public/audio --dry-run

Exit status is 1 if any line overruns its budget, so it can gate a render.
Colloquial Cantonese runs wordier than English: when a line is over, shorten
the wording rather than raising the rate.
"""

import argparse
import json
import math
import struct
import subprocess
import sys
import wave
from pathlib import Path

VOICE = "Sinji"
RATE = 230
FPS = 30
TARGET_RMS = 0.145
LIMIT_KNEE = 0.8


def say(text, path, voice=VOICE, rate=RATE):
    subprocess.run(
        ["say", "-v", voice, "-r", str(rate),
         "--data-format=LEI16@44100", "-o", str(path), text],
        check=True,
    )


def load(path):
    with wave.open(str(path)) as w:
        n, sr = w.getnframes(), w.getframerate()
        raw = w.readframes(n)
    return [x / 32768 for x in struct.unpack(f"<{n}h", raw)], sr


def save(path, samples, sr):
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(struct.pack(
            f"<{len(samples)}h",
            *[max(-32768, min(32767, int(round(x * 32768)))) for x in samples],
        ))


def despike(a):
    """Flatten short full-scale bursts; they are synthesis clicks, not speech."""
    ordered = sorted(abs(x) for x in a)
    thr = max(ordered[int(0.9999 * len(ordered))] * 1.8, 0.2)
    i = fixed = 0
    while i < len(a):
        if abs(a[i]) > thr:
            j = i
            while j < len(a) and abs(a[j]) > thr:
                j += 1
            if j - i <= 8:  # a real sustained vowel is far longer than this
                lo = a[i - 1] if i else 0.0
                hi = a[j] if j < len(a) else 0.0
                for t in range(i, j):
                    a[t] = lo + (hi - lo) * ((t - i + 1) / (j - i + 1))
                fixed += j - i
            i = j
        else:
            i += 1
    return fixed


def soft_limit(x, knee=LIMIT_KNEE):
    ax = abs(x)
    if ax <= knee:
        return x
    return math.copysign(knee + (1 - knee) * math.tanh((ax - knee) / (1 - knee)), x)


def rms(a):
    return math.sqrt(sum(x * x for x in a) / len(a))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lines", help="JSON list of {id, text, budget}")
    ap.add_argument("--out", default="public/audio")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--rate", type=int, default=RATE)
    ap.add_argument("--dry-run", action="store_true",
                    help="measure lengths without writing into --out")
    args = ap.parse_args()

    items = json.load(open(args.lines, encoding="utf-8"))
    out = Path(args.out)
    tmp = Path(".narration-tmp")
    tmp.mkdir(exist_ok=True)
    if not args.dry_run:
        out.mkdir(parents=True, exist_ok=True)

    print(f"voice {args.voice} (zh_HK)  rate {args.rate}  target RMS {TARGET_RMS}\n")
    print(f"{'id':6s} {'frames':>7s} {'budget':>7s} {'peak':>6s}  text")
    over = []
    lengths = {}

    for item in items:
        ident, text = item["id"], item["text"]
        budget = item.get("budget")
        raw = tmp / f"{ident}.wav"
        say(text, raw, args.voice, args.rate)

        a, sr = load(raw)
        despike(a)
        gain = TARGET_RMS / rms(a)
        a = [soft_limit(x * gain) for x in a]

        frames = math.ceil(len(a) / sr * FPS)
        lengths[ident] = frames
        peak = max(abs(x) for x in a)
        fits = budget is None or frames <= budget
        if not fits:
            over.append(ident)

        if not args.dry_run:
            save(out / f"{ident}.wav", a, sr)

        flag = "" if fits else "  ** OVER **"
        shown = text if len(text) <= 30 else text[:29] + "…"
        print(f"{ident:6s} {frames:7d} {str(budget or '-'):>7s} {peak:6.3f}  {shown}{flag}")

    print()
    print("lengths for the NARRATION table:")
    print("  " + ", ".join(f'{{ file: "{k}", len: {v} }}' for k, v in lengths.items()))
    print()

    if over:
        print(f"Over budget: {', '.join(over)}. Shorten the wording, "
              f"do not raise the rate — a faster read is audible.")
        return 1
    print("Every line fits its window." if not args.dry_run
          else "Every line fits (dry run — nothing written).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
