# Art direction and geometry

The look is the NES football games of around 1990 — 熱血足球 (Technōs, 1990) specifically:
a top-down pitch on a low-resolution grid, hard flat colour, black outlines, no gradients
and no anti-aliasing.

That style is not nostalgia for its own sake. Flat colour and heavy outlines survive being
watched on a phone at the side of a pitch, and a bird's-eye view is how coaches already
draw on a whiteboard.

## The framebuffer

Everything is drawn in a **320 x 180 virtual framebuffer, scaled 6x to 1920 x 1080**.

```tsx
<svg width={1920} height={1080} viewBox="0 0 320 180" shapeRendering="crispEdges">
```

`crispEdges` turns off anti-aliasing. Every sprite coordinate is rounded to a whole virtual
pixel before use (`snap()`), or edges blur between cells and the pixel look collapses.

Keep shapes to axis-aligned `<rect>`s wherever possible. Curves get drawn by sampling into
1 px rects, which is how the futsal D is built.

## The geometry rule

**One px-per-metre constant, shared by both axes.** This is the rule the whole style stands on.

```ts
export const S = 6.6;   // pixels per metre — the SAME for x and y
export const X0 = 104;  // centre of the pitch region
export const Y0 = 152;  // screen y of the near edge

export const toScreen = (p: P) => ({ x: X0 + p.u * S, y: Y0 - p.v * S });
```

If x and y use different scales, a square draws as a rectangle and every distance in the
video is a lie. There is no perspective, no vertical squash, no "it looks better this way".
A coach reads positions off these frames.

### Choosing S and the origin

Solve for the extremes, not the pitch edges. Sprites are 16 x 22 with a number badge above,
so an actor's drawn extent runs from `y_feet - 30` to `y_feet`.

```
deepest actor:    Y0 + v_min * S  <=  VH - 2        (v_min is negative, behind the near edge)
furthest actor:   Y0 - v_max * S  -  30  >=  2
widest actor:     X0 +/- u_max * S        within the pitch region
```

Worked examples that ship:

| | field | S | origin | notes |
|---|---|---|---|---|
| `src/nes.tsx` | 15 x 15 m square grid | 6.6 | `X0 104, Y0 152` | queues stand up to 4.5 m outside the cones |
| `src/futsal.ts` | 20 x 40 m futsal court | 9.5 | `CX 104, TOP 34` | only the attacking third is in frame; `TOP` leaves room for the corner taker's sprite above the goal line |

For a format not covered, pick the region that actually matters — a corner routine does not
need the far half — and solve S against that region, not the whole pitch.

## Layout

A square pitch does not fit a 16:9 frame with a bottom bar, so the information goes down
the side:

```
x 0 .......... 208 ......... 320
  [   pitch    ][  info panel ]
```

`PANEL_X = 208`. The panel carries the scene title, the numbered phase list with the
current one highlighted, and a footer naming the pitch size. The pitch region gets the
full 180 px of height.

Earlier versions used a bottom HUD bar with portraits and a mini-map. Both were dropped: in
a bird's-eye view a mini-map duplicates the main picture, and the bar stole the height the
square needed.

The panel is about 96 px wide, which is **eleven CJK characters at 9 px** — and SVG text
does not wrap, so it has to be split by count before it is drawn. A full stop that lands at
the start of a line hangs off the end of the previous one instead; a lone 。 on its own line
reads as a bug.

### Text screens

Sections with no pitch (problem, how you win, variation, progression, the closing question)
use the full width, a heading in a `Window` and numbered rows. Everything there wraps at a
wider count, but it still wraps — a long line runs off the frame silently and the render
looks fine.

### The drill card

Label above value, seven rows: 主題, 類別, 人數, 難度, 年齡, 時間, 場地. Difficulty draws
as **filled and empty pixel squares**, never a ★: a star glyph needs font coverage, and the
glyph checker's CJK range would not even flag it as missing — it would simply render as
tofu. Drawn squares also match the pixel style. Keep values short; 人數 is the one that
overflows, so `7人（2打2＋2換）`, not the full sentence.

### Zones

A queue or a target gate draws as a bracket with a Chinese label below it — `等緊` for a
queue in `blueLight`, a named gate in `gold`. They sit outside the playing area, below the
bottom line, where no sprite can ever cover them.

### Mini goals

When a format has several small goals, draw each as a gold gate **outside** the end line,
the way the full goal sits above its line — two posts and a bar, no net. A net reads as
"this is the goal" when all of them are live, and a gate drawn on the line gets stood on.

## Palette

The NES master palette, as `N` in `nesTheme.ts`. Flat fills only — no gradient anywhere.

| | | | |
|---|---|---|---|
| `black` `#000000` | `white` `#fcfcfc` | `grey` `#bcbcbc` | `darkGrey` `#7c7c7c` |
| `grassLight` `#00b800` | `grassDark` `#009400` | `grassShade` `#007800` | |
| `skin` `#fcbcb0` | `skinDark` `#d88070` | `hairBlack` `#1c1c1c` | `brown` `#a84400` |
| `red` `#f83800` | `redDark` `#a81000` | `salmon` `#fc7460` | `orange` `#fc9838` |
| `yellow` `#fcd8a8` | `gold` `#f8b800` | `purple` `#6844fc` | |
| `blue` `#0058f8` | `blueDark` `#0000bc` | `blueLight` `#3cbcfc` | |

Grass is two bands alternating `grassLight` / `grassDark`; `grassShade` does shadows and
the highlight behind an active panel row.

## Fonts

| role | face | why |
|---|---|---|
| Chinese | **GNU Unifont** (`@fontsource/unifont`) | a true 16x16 bitmap face, so Chinese stays 8-bit |
| Latin and digits | **Press Start 2P** (`@fontsource/press-start-2p`) | the chunky NES look for numbers and letters |

**Do not use DotGothic16 for Traditional Chinese.** It is a Japanese face and genuinely
lacks 每 內 腳 踢 擊 錄 — Japanese writes those 毎 内 脚 撃 録. It renders Japanese beautifully
and Traditional Chinese with holes. `check_glyphs.py --font-dir` catches this.

Fonts are bundled from npm so a render never depends on a network fetch, and the CJK subset
is loaded behind `delayRender` with an explicit character list.

## Sprites

16 wide x 22 tall, written as rows of single-character colour keys and plotted by merging
runs of the same colour into one `<rect>` — about 40 nodes per sprite instead of 352.

```
"......kkkk......",
"....kkhhhhkk....",
"..ksseesseessk..",
```

Poses: `idle`, `run1`, `run2`, `kick`. Alternate `run1`/`run2` every 4-5 frames while a
player is moving; use `kick` for a few frames either side of a pass or a strike.

`kit` overrides the colours per team. `badge` sets the shirt-number colour — **white for
attackers, blue for defenders, gold for the keeper.** At true scale a marker stands within
a metre of his man and the sprites overlap; without team-coloured numbers you cannot tell
whose badge is whose. That overlap is real proximity, not a layout bug.

Sprites spawn with a short blink (visible on alternating frames for ~6 frames), the way NES
games do, rather than fading in.

## Showing movement

The ball carries a short trail. A pass draws a **solid line with an arrow head** from passer
to receiver while the ball is live, and nothing once it has arrived. A follow-run draws as a
**static dashed path sampled from the runner's own track**, so it is accurate by
construction rather than an approximation of where they went.

Katakana-style hit markers (咻！on a strike, 咚 on a touch) pop for a few frames and blink
out. They are the one piece of pure decoration, and they are brief.

## Showing a role change

A player who changes team changes **kit and badge colour**, resolved through `sideAt` so it
carries forward from the phase that swapped them. In the rotation section the two players
of a pair ease past each other into one another's opening positions while a **two-headed
purple arrow** joins them. Purple is used for nothing else, so it cannot be mistaken for a
pass (gold) or a run (salmon).

The rotation section is schematic — it shows the pairs trading places from the opening
shape, not the real end-of-drill geometry. A three-way cycle (attackers to defenders,
defenders to the queue, queue on) cannot be drawn as pairs; the panel note carries the
third leg in words, and the last execution phase shows the real result.

## The other look

A second visual system exists in `theme.ts` / `field.tsx`: a Captain Tsubasa pastiche with a
perspective camera, cel shading and 7-head-tall anime players. It is for hype — a
competitive challenge, a progression video, a channel trailer.

Do not use it for instructional diagrams. It has a perspective camera, so distances on
screen are not proportional, which is exactly what makes it wrong for teaching a shape.
