# Writing the session plan

The plan is what a coach prints and carries to training. The video is a recording of its
main block. Write the plan first: a drill chosen to look good on screen is a different
drill from one chosen to fill a slot in a session, and the second one is the useful one.

The numbers here are conventional practice, not regulation. Check them against whatever
your federation or club publishes before treating any of them as fixed.

## What you need before planning

| Input | Default when not given |
|---|---|
| Age group | State one and say so — it drives everything else |
| Players | 8–12, the usual youth turnout |
| Level | Mixed ability within the age group |
| Session length | From the age table below |
| Space | A third of a pitch, normal cones, bibs, one ball each |

Ask only for what genuinely changes the plan — see [WORKFLOW.md](WORKFLOW.md). Anything
assumed goes in the plan in writing, so the coach can see what it was built on.

## The shape of a session

Four blocks. The main block is the one that gets filmed.

| Block | Share | What it is |
|---|---|---|
| 熱身 Warm-up | ~20% | Ball work, joints and heart rate up, no queues |
| 主練習 Main | ~20–35% | The theme, in a game: this is the filmed block |
| 進階 Progression | ~25% | The same theme, harder or bigger |
| 比賽 Game | ~20–25% | Free play where the theme can appear on its own |

**The age cap below beats the share.** They disagree: 35% of a 70-minute U9–U12 session is
24 minutes, and the age table caps the main block at 15. The cap wins — a share is a rough
target, the cap is a limit on how long one rule set holds attention. Put the spare minutes
into the progression and the game, which are the same theme anyway.

**One theme per session.** A session that teaches pressing and switching play teaches
neither. The warm-up and the game should both touch the main block's theme, so the night
reads as one idea three times, not four unrelated activities.

### Length by age

| Age | Session | Main block | Why |
|---|---|---|---|
| U6–U8 | 45–60 min | 8–10 min | Attention goes before the legs do |
| U9–U12 | 60–75 min | 10–15 min | Can hold one rule set, not three |
| U13+ | 75–90 min | 15–20 min | Can hold constraints and tactical detail |

When the main block is longer than the table allows, the drill is too complicated, not the
age group too slow. Cut a rule.

### Load

Work to rest between **1:2 and 1:4** for anything at full speed — a 20-second duel wants
40 to 80 seconds before that player goes again. That ratio is what sets queue length: two
waiting per working pair gives roughly 1:2, which is why the formats in these videos run
queues of two and no more.

A queue longer than three is a planning failure, not a detail. Split into two grids and
run them side by side instead.

## The main block — the fields the plan must carry

Everything here is what a coach asks, in the order they ask it. These are also the fields
the drill JSON carries, so the video cannot teach something the plan does not say.

1. **主題 Theme** — one thing. 壓迫下控球, not 控球同埋壓迫.
2. **問題 Problem** — what goes wrong in a match that this fixes. Written as the coach
   would describe it, not as a textbook objective.
3. **目標 Aim** — what the players should be able to do by the end.
4. **場地 Area** — real metres. Two numbers, and they must be the numbers drawn.
5. **器材 Equipment** — cones, bibs, balls, goals, gates. Count them.
6. **起點 Starting positions** — where every player stands before anything moves, marked
   with a cone where the shape does not make it obvious. The queue stands at the end its
   players start from, so a player comes off and rejoins in the same place.
7. **開始 Distribution** — who serves and what starts the play. "The attacker begins with
   it" starts the two sides at different moments; prefer a serve that starts both together
   (in a 1v1, the defender passes to the attacker).
8. **玩法 Steps** — the sequence, one beat at a time, about two seconds each.
9. **點樣分勝負 Scoring** — how each side scores and who wins. **If you cannot write this,
   it is a demonstration, not a drill, and it does not get filmed.**
10. **輪轉 Rotation** — who swaps with whom and when. Name the role change explicitly:
    "the attacking pair becomes the next defending pair".
    **Count the two sides before writing "the teams swap".** A whole-team swap only works
    when the sides are the same size. Four attackers and two defenders cannot trade
    wholesale; swap a pair instead — the pair that just attacked takes over defending and
    the two defenders rejoin the attacking pool, which keeps 4 and 2 as 4 and 2.
11. **重點 Coaching points** — four, no more. Each one a thing to say on the grass, short
    enough to shout.
12. **變化 Variations** — two or three ways to change it without rebuilding it.
13. **進階 Progression** — three levels, easiest first.
14. **問題 Closing question** — one, for the coach to ask the players, and for the video
    to ask the audience.

## Writing it down

`out/sessions/<id>.md`, in Traditional Chinese, with the four blocks and the main block
carrying all fourteen fields above. Head it with the age group, player count, session
length and every assumption made.

Then fill `src/drills/<id>.json` **from the plan**. The JSON is the machine-readable
subset — spec, problem, winning, rotation, zones, variations, progression, question, plus
the positions and phases. Fill it by copying, never by inventing a second time.

## Where the plan lands in the video

| Plan field | Video section |
|---|---|
| Theme, players, difficulty, age, time, area | 練習資料 drill card |
| Problem, aim | 問題 |
| Area, equipment, starting positions, distribution | 設置 |
| Scoring | 點樣分勝負 |
| Steps | 玩法 |
| Rotation | 輪轉 |
| Coaching points | 重點 |
| Variations, progression, closing question | the last three screens |

The warm-up, the progression block and the game are in the plan but **not** in the video.
The video is the main block only, which is why it runs under two minutes.
