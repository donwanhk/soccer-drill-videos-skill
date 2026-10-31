# The workflow

Six steps, in order. The session plan comes **before** the video, always — the video is a
recording of a plan, not a thing designed in the editor. Writing the plan first is what
stops a drill being chosen because it looks good on screen.

```
topic → questions → session plan → ⏸ REVIEW → video → thumbnail + description → show
```

**There is a stop between the plan and the video.** Show the plan and wait. A mistake
caught in the plan costs a sentence; the same mistake caught after the render costs the
narration, the render and the verification pass. Never start building because the plan
looks finished to you.

## 1. Get a topic

Either the person gives one, or pick one. When picking, read `src/drills/*.json` first and
read each `title` and `spec.theme`, so the new one is not a repeat. Vary the category, the
age band and the difficulty against the last two or three — a run of videos should not be
three shades of the same idea.

## 2. Ask what is missing — but only what changes the plan

| Ask about | Why it changes the plan |
|---|---|
| Age group | Decides session length, block length, and how complex the rules can be |
| Number of players | Decides the format; 7 players cannot run a 4v4 |
| Level | Decides the constraints — two-touch, time limits, weak foot |

Space and equipment are worth asking only when the topic needs something unusual (a full
goal, a keeper, many cones). Otherwise assume a normal training patch and say so.

**Ask once, in one message, and only for what is genuinely missing.** If the person says
"a passing drill for U10", that is enough — the level and the squad size can be assumed
and stated. Do not interrogate. A plan built on a stated assumption is more useful than a
question that stalls the work.

## 3. Write the session plan

[SESSION-PLAN.md](SESSION-PLAN.md) governs this. The plan is the deliverable a coach takes
to training; the filmed drill is its main block. Written to `out/sessions/<id>.md`.

## 3a. Stop. Let them read the plan.

Hand over `out/sessions/<id>.md` and **wait for a yes.** Do not render, do not synthesise
narration, do not write the drill JSON. If they are not around, the work ends here with the
plan delivered — that is a complete, useful deliverable on its own.

## 4. Build the video

[VIDEO.md](VIDEO.md) governs this, with [STYLE.md](STYLE.md) for the drawing,
[AUDIO.md](AUDIO.md) for the narration and [CHECKS.md](CHECKS.md) for what to verify.

The drill JSON at `src/drills/<id>.json` is the machine-readable subset of the plan.
**Fill it from the plan, do not invent it a second time** — if the two disagree, the video
teaches something the coach is not running.

## 5. Thumbnail and description

[THUMBNAIL.md](THUMBNAIL.md) and [DESCRIPTION.md](DESCRIPTION.md).

## 6. Show the results

**Never re-render unprompted.** Editing text that feeds a video does not entitle you to
rebuild it. Change the source, say plainly which videos on disk are now stale, and wait to
be told. A batch of re-renders is twenty-five minutes of someone's machine, and they may
want several corrections to land in one pass.


The session plan, the mp4, the thumbnail and the description — with the video's duration,
and anything a check flagged that could not be fixed. If a drill fails its checks and
cannot be fixed, say so and ship nothing: a diagram that is wrong is worse than one that
is missing, because these are passed between coaches.

## What this never includes

Uploading. There is no YouTube connector here, and publishing needs the person's own
Google sign-in. The files are the deliverable.
