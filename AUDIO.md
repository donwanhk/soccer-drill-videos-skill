# Narration, music and sound

## The voice

**macOS `say`, voice Sinji (zh_HK), rate 230.** Generate with
`scripts/make_narration.py`, which also does the post-processing and the budget check.

```
say -v Sinji -r 230 --data-format=LEI16@44100 -o out.wav "右路角球。五號開波。"
```

Sinji is the **only** Cantonese voice on a stock macOS install. Checked and ruled out:

- **Kokoro** — no Cantonese. Its `zf_*` / `zm_*` voices are Mandarin.
- **Piper** — no Cantonese. 54 language directories, `yue` is not among them.
- **espeak-ng** — has `yue`, but it is robotic.
- **`facebook/mms-tts-yue`** — does not exist.

**Do not pitch-shift Sinji.** It was tried at +10 / +15 / +20 / +25% to sound younger,
shipped at +15%, and rejected as unnatural. Pitch shifting buys a younger register at the
cost of sounding processed, which is the opposite of what was wanted.

If a different voice is genuinely needed, the real options are a neural Cantonese model
(`csukuangfj/vits-cantonese-hf-xiaomaiiwn`, 114 MB ONNX, runs locally through sherpa-onnx,
and sits around 235 Hz naturally) or a cloud voice such as Azure HiuMaan / HiuGaai. Note
that the VITS model's lexicon has **empty entries for some Traditional characters** — 傳 is
listed with no phonemes, so sherpa-onnx logs `OOV 傳. Ignore it!` and silently drops the
word. Feed it Simplified via OpenCC; the spoken Cantonese is identical.

## Post-processing

Every clip goes through the same chain before it reaches `public/audio/`:

1. **Despike.** `say` emits occasional single-sample full-scale clicks. Runs of 8 samples
   or fewer that tower over the local neighbourhood get replaced by interpolation.
2. **Normalise to RMS 0.145.** Every existing clip sits there. Matching it means a new line
   drops into an old video without re-balancing anything.
3. **Soft limit.** `tanh` above 0.8 rather than hard clipping, so transients round off
   instead of square off.

## Timing

Each line is placed at a frame and must fit the gap to the next one. `make_narration.py`
takes a budget per line and fails if any overruns.

```json
[ { "id": "f1", "text": "右路角球。五號開波，七號接應。", "budget": 95 } ]
```

A long-form video has **one line per section plus one per phase** — about fourteen, roughly
85 s of speech in a 115 s video. Budgets come from the section table, not from counting
frames by hand: a section line gets `LEN - 30`, a phase line `hold - 20`.

Then in the soundtrack, place every line from the section table itself rather than from
literal frame numbers, so the audio cannot drift when a section changes length:

```tsx
const starts = sectionStarts(routine);
const phases = phaseStarts(routine);
// section lines 12 frames in, phase lines 8 frames into their phase
narration.push({ ...line, from: starts[sec.id] + 12 });
const speaking = (f: number) =>
  narration.some((n) => f >= n.from - 4 && f <= n.from + n.len + 4);
```

Rules that have earned their place:

- **Leave the big moments clear.** A goal, a new record, a finish — keep a gap in the
  narration so the impact sound lands on its own. The futsal corner keeps frames 367-395
  free so the 新紀錄 hit at 389 is not spoken over.
- **Check nothing overruns the composition.** Lines are measured, not estimated; after any
  scene-length change, re-place every line and re-check.
- **Music ducks under speech**: 0.5 normally, 0.17 while `speaking(f)`. Set `loop` on the
  music when the video is longer than the bgm track.

## Verifying it actually landed

A render can succeed with the narration silently missing or misplaced. Correlate each
source clip against the rendered mix at its placed offset:

```python
ffmpeg -v error -y -i out.mp4 -vn -ac 1 -ar 44100 -f wav mix.wav
# then, per line, Pearson correlation of clip vs mix[offset : offset+len]
```

**0.75 and above means present and aligned.** Lower values are normal where a line sits
under a loud impact SFX. Anything near zero means it is not there — check the file name,
the `from` frame, and that `public/audio/` actually got written.

Get the offsets from the code, never from arithmetic in your head. Bundle a two-line entry
with esbuild and print `makeSoundtrack(...).narration`; a verification run against guessed
frames once reported three failures that did not exist.

## Sound effects

Shared one-shots in `public/audio/`: `kick`, `trap`, `impact`, `whoosh`, `pop`, `chime`,
`sparkle`, plus `bgm`.

Rough conventions: `kick` a frame before a pass is struck, `trap` as it arrives, `pop` for
each item appearing in a list, `whoosh` on a scene change, `impact` on a title card or a big
moment, `chime` when a result lands, `sparkle` for a flourish.

Derive SFX timings from the drill data rather than hand-placing them, so they stay correct
when the pacing changes:

```tsx
...DRILL.events.flatMap((e) => [
  { file: "kick", at: EXEC + e.t - 1, volume: 0.85 },
  { file: "trap", at: EXEC + e.arrive, volume: 0.6 },
]),
```
