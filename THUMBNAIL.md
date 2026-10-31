# Thumbnail

1280 x 720, which is the video's own 320 x 180 grid at 4x — so the stripes land on exactly
the same pixel pitch as the film. Rendered from a `Thumb<Id>` composition, never drawn by
hand. Branding is governed by `BRAND.md` in the project root.

## Three things, and no more

A thumbnail is read at about 200 px wide in a feed. It carries:

1. **The title** — large, left, two lines of four characters.
2. **Who it is for** — one gold chip: `人數 · 年齡`.
3. **A glimpse of the drill** — right side.

Plus the channel lockup bottom-left at a size that stays out of the way. Anything else is
noise at feed size.

## The glimpse is the real position

The right side draws the drill's **actual opening position at the video's own scale**,
re-centred in its window. Not a mock-up, not a simplified diagram. A thumbnail must not be
able to advertise a shape the video does not contain.

Two things that follow from that:

- **A position is the sprite's feet.** The body plus its shirt number stand 30 px above it,
  so centre on the visual box, not the raw points, or the back row loses its heads.
- **Clip the pitch window** so a wide pitch cannot spill into the title.
- **Scale the group down when it does not fit.** A drill with queues behind both end lines
  is taller than the 134 x 146 window, and cropping it cuts players off at the shins, which
  reads as a broken image rather than a crop. A *uniform* scale is not a violation of the
  true-scale rule: every distance stays proportional, which is what that rule protects. A
  non-uniform one would be.

## Titles

Chinese does not break by meaning on its own. The automatic wrap splits at four characters,
which is right for `圍圈搶球積分賽` (圍圈搶球 / 積分賽) and wrong for `三門小型賽`
(三門小型 / 賽). When the automatic wrap breaks a title badly, set `thumbTitle` in the drill
JSON with an explicit `\n`.

**Every line of `thumbTitle` must itself be four characters or fewer.** The wrap still runs
over what you wrote, so `邊路二過一\n挑戰` comes out as three lines — 邊路二過 / 一 / 挑戰.
Drop a word rather than overflow: `邊路\n二過一` reads fine and the full title is on the
title card anyway.

Outline every text item: `stroke` plus `paintOrder="stroke fill"` at about a third of the
font size. White on grass vibrates without it.

## Checking it

Look at the rendered PNG before shipping it, at full size **and** scaled to about 320 px
wide. Things that only show up small: the title turning to mush, the chip becoming a grey
bar, the lockup disappearing. Things that only show up large: a clipped sprite, a badge
behind a head, text touching the frame edge.
