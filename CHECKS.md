# What goes wrong, and what catches it

Every entry here is an error that actually shipped. None of them made the render fail or
look broken — that is why they need scripts rather than a careful eye.

| Check | Catches | Script |
|---|---|---|
| Goal-side | A defender behind their man instead of between him and the goal | `check_tactics.py` |
| Squad size | Wrong number of players for the format | `check_tactics.py` |
| Spacing | Players stacked into an unreadable blob | `check_tactics.py` |
| Badge occlusion | A shirt number hidden behind the player in front | `check_tactics.py --px-per-m` |
| Near vs far post | A "far post" run going to the near post | by hand, see below |
| Duplicate nets | Two goals drawn on one goal line | by hand, see below |
| Start spots | No cone, so nobody knows where to stand | by hand — every drill needs `zone` kind `start` |
| Distribution | Nobody named as the server, so the sides start apart | by hand — check `ballStart` and phase 1 |
| Glyph coverage | A character rendering as tofu | `check_glyphs.py` |
| Narration fit | A line overrunning its window | `make_narration.py` |
| Narration present | Voice-over silently missing from the render | correlation, see AUDIO.md |

## Goal-side

A defender marks from **between his man and the goal he is defending**. Home always attacks
towards y=0, so a defender's y must be *smaller* than his man's.

```
python3 scripts/check_tactics.py drill.json --marks 2:7,3:9,4:10
```

A deliberate beat is fine — that is often the whole point of the routine — but it has to be
declared, so it cannot hide among accidents:

```
python3 scripts/check_tactics.py drill.json --marks 3:9 --expect-beaten 3:9@4
```

In the futsal corner, two of three markers were behind their man, one of them for the
entire routine. Nothing about the render looked wrong.

## Squad size

Futsal is 5-a-side: a keeper **plus four** outfield. The first corner had three. The script
counts players per team and compares against the format.

An attacking keeper legitimately may not be in frame — during an attacking corner they are
usually in their own half. The script flags the count; judgement decides.

## Spacing

Markers hold a constant size on screen, so accurate positions can still read as one blob.
The script reports the closest pair in metres per phase.

Sub-metre is correct only when it *is* the point: a screen is near-contact, and the futsal
corner's 0.45 m at the screen phase is right. Anywhere else, separate them — the fix is
usually to move the marker, not to shrink the sprite.

`--min-gap` is **not** a fixed number. A sprite is 16 px wide whatever the pitch, so the
threshold in metres is `16 / S`: 2.3 m at S = 7, but 3.2 m at S = 5. A flat 1 m once let
two players merge into one blob on a large-S drill and passed the check.

## Badge occlusion

The spacing check is Euclidean, and that is not the shape of the problem. A sprite is
16 px wide, 22 tall, and its shirt number sits about 8 px above it — so the exclusion zone
is a tall ellipse, not a circle. Two players side by side at 3.2 m are fine; two players in
the same column at 4.8 m are not, because the upper one's number disappears behind the
lower one's head.

```
python3 scripts/check_tactics.py drill.json --px-per-m 5.0
```

The rule it enforces: if `|dx| < 16/S` then `|dy|` must exceed `30/S`. This shipped wrong
on a 2v2 transition drill where every defender/attacker pair passed the spacing check at
4.2 m and every attacker's number was invisible.

## Near vs far post

No script; it needs a moment's thought. **The far post is the one further from the ball.**
A shot from right of centre has its far post on the **left**.

This shipped wrong: narration said far post, the animation sent the runner to the near post,
and the keeper was already covering that side. Check the narration and the coordinates agree
whenever a routine names a post.

## Duplicate nets

The pitch drawing already includes goals. Adding a net marker on top renders two. In the
Pocket Tactic Board format that means leaving `nets` out when the field already draws them.

## Before every render

```bash
python3 scripts/check_tactics.py drill.json --marks <pairs> --min-gap <16/S> --px-per-m <S>
python3 scripts/check_glyphs.py src --font-dir node_modules/@fontsource/unifont/files
npm run lint        # eslint + tsc
```

All three exit non-zero on failure, so they chain with `&&`.

Then take one still per section — `npx remotion still <Composition> out.png --frame=N` —
before committing to a full render. Text screens and the drill card overflow silently, and
a sprite clipped by a panel edge looks deliberate. Compute the frames from
`sectionStarts(routine)` rather than guessing them.

After the render, correlate the narration against the mix (AUDIO.md) before saying it is done.
Compute each line's offset from `sectionStarts` too: a verification run against guessed
frames reported three failures that did not exist.
