---
name: soccer-drill-videos
description: The YouCoach pipeline — plan a training session, then build the drill video, thumbnail and YouTube description from it. Bird's-eye pixel-art pitch, Traditional Chinese on-screen text, Cantonese narration. Use whenever someone asks for a YouCoach video, a drill or training video, a session plan, a tactic or set-piece animation, a drill thumbnail or video description, or changes to any of them.
---

# YouCoach — session plans and drill videos

This is the whole pipeline for the YouCoach channel (@you_coach). A session plan first,
then a video of its main block, then the thumbnail and description. Designing the drill in
the editor instead of in the plan is how you get something that looks good and cannot be
run at training.

## The six steps

Follow them in order. **Read [WORKFLOW.md](WORKFLOW.md) before starting** — it carries the
detail each step needs.

| # | Step | Governed by |
|---|---|---|
| 1 | Take the topic, or pick one not already covered | [WORKFLOW.md](WORKFLOW.md) |
| 2 | Ask only for what changes the plan — age, squad size, level | [WORKFLOW.md](WORKFLOW.md) |
| 3 | Write the session plan to `out/sessions/<id>.md` | [SESSION-PLAN.md](SESSION-PLAN.md) |
| 4 | Build the video of the main block | [VIDEO.md](VIDEO.md) |
| 5 | Thumbnail and description | [THUMBNAIL.md](THUMBNAIL.md), [DESCRIPTION.md](DESCRIPTION.md) |
| 6 | Show the plan, mp4, thumbnail, description and duration | [WORKFLOW.md](WORKFLOW.md) |

## The reference shelf

| Document | Governs |
|---|---|
| [WORKFLOW.md](WORKFLOW.md) | The six steps, and when to ask versus assume |
| [SESSION-PLAN.md](SESSION-PLAN.md) | Session shape, length by age, load, the fourteen fields of a drill |
| [VIDEO.md](VIDEO.md) | The eleven sections, the build loop, the rules that matter most |
| [STYLE.md](STYLE.md) | Geometry, palette, fonts, layout, how a role change is drawn |
| [AUDIO.md](AUDIO.md) | The Cantonese voice, line budgets, verifying narration landed |
| [THUMBNAIL.md](THUMBNAIL.md) | What a thumbnail carries, and what it may not claim |
| [DESCRIPTION.md](DESCRIPTION.md) | The generated YouTube description |
| [CHECKS.md](CHECKS.md) | Every error that has shipped, and the script that catches it |

`BRAND.md` in the project root governs the mark, the palette tokens and the lockups.
The project is `~/Documents/projects/remotion-soccer-drills`.

## The three things that decide everything else

**It is for coaches.** A diagram that is pretty but misleading is worse than a plain one
that is right. Clarity beats style every time.

**It must be a game.** Repeatable, scored, with a winner. If you cannot say how each side
scores and who wins, it is a demonstration, and it does not get filmed.

**Check before you render.** Every tactical error that has shipped here looked fine in the
render and was caught by a person, not by the output looking wrong. Run the scripts.

## What is not in this skill

Nothing here uploads, posts or publishes — there is no YouTube connector, and publishing
needs the person's own Google sign-in. It makes the files; a person does the rest.
