# Building the video

The video is the session plan's **main block**, and nothing else. It runs about two
minutes. [STYLE.md](STYLE.md) is the authority on how it is drawn, [AUDIO.md](AUDIO.md) on
the narration, [CHECKS.md](CHECKS.md) on what to verify.

These videos are made for coaches to watch and pass to other coaches. That one fact
decides nearly every call: a diagram that is pretty but misleading is worse than a plain
one that is right. Clarity wins over style every time.

Output is 1920x1080, 30 fps, MP4.

## The eleven sections

The order is fixed, because it is the order a coach needs.

| # | Section | Frames | Fed by |
|---|---|---|---|
| 1 | Title | 60 | title, subtitle |
| 2 | 練習資料 Drill card | 240 | spec |
| 3 | 問題 Problem + aim | 270 | problem |
| 4 | 設置 Setup | 330 | area, equipment, start positions, distribution |
| 5 | 點樣分勝負 How you win | 300 | winning |
| 6 | 玩法 Execution | per phase | phases |
| 7 | 輪轉 Rotation | 240 | rotation |
| 8 | 重點 Coaching points | 390 | points |
| 9 | 變化 Variation | 300 | variations |
| 10 | 進階 Progression | 300 | progression |
| 11 | 問題 Closing question | 240 | question |

Sections 3, 5, 9, 10 and 11 are one text-screen component with different content. An
optional section is skipped when the drill JSON has no content for it, so a drill with no
rotation simply has ten. The execution section is as long as the phases make it.

**Never hard-code section starts** — read them from `sectionStarts(routine)`. Narration
placement and still frames both depend on them, and a hand-computed offset once produced
three verification failures that did not exist.

## What the video must show, not say

- **The role change.** When the attackers become the next defenders, draw it. Kit and badge
  colour follow `sideAt`, so a player visibly changes team, and the rotation section draws a
  two-headed purple arrow between each pair. Purple is used nowhere else, so it can never be
  read as a pass (gold) or a run (salmon).
- **The queue.** Waiting players are real actors standing in it, with a `zone` labelling it.
- **The starting positions.** A `zone` of kind `start` draws a cone where a player stands
  before anything moves.
- **The serve.** The server is the `ballStart` actor and the first phase is the pass.

## The build loop

1. Fill `src/drills/<id>.json` from the session plan — positions, phases, and the teaching
   fields. Never invent the teaching content a second time.
2. Register the routine in `src/drills.ts` with its pitch spec and markings.
3. `python3 scripts/check_tactics.py drill.json --marks 2:7,… --min-gap <16/S> --px-per-m <S>`
   Fix what it reports. **Before rendering, not after.**
4. `python3 scripts/make_narration.py lines.json --out public/audio` — one line per section
   plus one per phase. Shorten anything over budget; never raise the rate.
5. Wire the soundtrack in `src/batch.tsx` with the **measured** lengths the script prints.
6. `python3 scripts/check_glyphs.py src --font-dir node_modules/@fontsource/unifont/files --write`
7. `npm run lint` — eslint and tsc.
8. One still per section, and **look at them**. Text overflows silently.
9. `npx remotion render <Composition> out/<id>.mp4 --port 4100`
10. Correlate every narration line against the mix (AUDIO.md).
11. Thumbnail and description — [THUMBNAIL.md](THUMBNAIL.md), [DESCRIPTION.md](DESCRIPTION.md).

Use a port other than 3000 if the studio is running.

## The rules that matter most

**One scale for both axes.** The worst bug shipped here drew a 15x15 m box at 10 px/m
across and 4.2 px/m down, so a square rendered as a 2.4:1 rectangle and every vertical
distance in the video lied. Share one px-per-metre constant between x and y. Always.

**Static lines.** No marching dashes, no animated outlines, no decoration that moves for
its own sake. A marching dashed box reads as noise and was removed for that reason.

**Check the tactics before you render.** Four tactical errors shipped in one futsal corner
— defenders behind their man, three outfield defenders in a 5-a-side format, a "far post"
run going to the near post, a duplicate net. Every one was caught by the person, not by the
render looking wrong. The render looks fine either way; that is the point.

**Positions are to scale, sprites are not.** A real player at 9.5 px/m would be 5 px wide
and invisible. Oversized figures on exact positions is the normal coaching-diagram
convention — say so when presenting, so nobody reads the body sizes as real. Because they
are oversized, spacing thresholds are pixels converted to metres, never a flat number:
`16/S` horizontally, `30/S` vertically for two players in the same column.

**Slow down.** About two seconds per beat. The first cut ran one pass every 1.33 s and read
as rushed. Build the setup in stages — box, cones, labels, players, ball.

## Writing the Cantonese

On-screen text is standard written Chinese (書面語). Narration is **colloquial spoken
Cantonese** — 傳波 not 傳球, 企 not 站, 咁 / 跟實 / 破咗 / 試吓. Sinji pronounces colloquial
characters correctly; that was verified by synthesising each one ten times against a
reference, so there is no reason to retreat to formal written Chinese.

**Write 球員, not 波仔.** 波仔 is affectionate but diminutive, and these are watched by
coaches talking about their own players.
