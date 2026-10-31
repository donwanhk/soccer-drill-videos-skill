# soccer-drill-videos

A Claude Code skill: the **YouCoach** pipeline for turning a coaching topic into a training
session plan, an animated drill video, a thumbnail and a YouTube description.

Bird's-eye pixel-art pitch, Traditional Chinese on-screen text, Cantonese narration.
Rendered with [Remotion](https://remotion.dev).

Start at **[SKILL.md](SKILL.md)**, then **[WORKFLOW.md](WORKFLOW.md)**.

## Layout

| File | Governs |
|---|---|
| [SKILL.md](SKILL.md) | Entry point — the six steps and the reference shelf |
| [WORKFLOW.md](WORKFLOW.md) | The six steps, and when to ask versus assume |
| [SESSION-PLAN.md](SESSION-PLAN.md) | Session shape, length by age, load, the fourteen fields of a drill |
| [VIDEO.md](VIDEO.md) | The eleven video sections, the build loop, the rules that matter most |
| [STYLE.md](STYLE.md) | Geometry, palette, fonts, layout, how a role change is drawn |
| [AUDIO.md](AUDIO.md) | The Cantonese voice, line budgets, verifying narration landed |
| [THUMBNAIL.md](THUMBNAIL.md) | What a thumbnail carries, and what it may not claim |
| [DESCRIPTION.md](DESCRIPTION.md) | The generated YouTube description |
| [CHECKS.md](CHECKS.md) | Every error that has shipped, and the script that catches it |

`scripts/` holds the checks and generators the workflow calls; `examples/` holds reference
drill data.

## Why the documents read the way they do

Most rules here exist because something shipped wrong. The geometry rule is in STYLE.md
because a 15×15 m box once rendered as a 2.4:1 rectangle. The spacing thresholds are in
pixels-converted-to-metres because a flat 1 m let two players merge into one blob. The
tactical checks are scripted because four separate errors in one set piece were caught by a
human and never by the render, which looked fine either way.

## Installing

Clone into `~/.claude/skills/` and Claude Code picks it up:

```bash
git clone https://github.com/donwanhk/soccer-drill-videos-skill.git \
  ~/.claude/skills/soccer-drill-videos
```

The video project it drives lives separately.
