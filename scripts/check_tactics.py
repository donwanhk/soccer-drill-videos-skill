#!/usr/bin/env python3
"""Tactical sanity checks for a drill, run before rendering anything.

Two tables, phase by phase:

  goal-side  each defender against the attacker they mark. A defender belongs
             BETWEEN his man and the goal he is defending. Anything else is an
             error unless it is a deliberate beat.
  spacing    the closest pair of players in metres. Sub-metre is only right
             when it IS the point (a screen is near-contact); otherwise the
             markers merge into one blob on screen.

Input is a Pocket Tactic Board drill JSON (ptb.drill/1). Phases carry forward:
a player keeps its position until a later phase moves it.

    python3 check_tactics.py drill.json --marks 2:7,3:9,4:10
    python3 check_tactics.py drill.json --marks 2:7 --expect-beaten 3:9@4

Exit status is 1 if any unexpected problem is found, so it can gate a render.
"""

import argparse
import json
import sys

# Nominal pitch sizes in metres (width x length).
FIELDS = {
    "futsal": (20.0, 40.0),
    "7-a-side": (45.0, 60.0),
    "9-a-side": (55.0, 75.0),
    "11-a-side": (68.0, 105.0),
}

# Normalised coordinates: x 0 = left touchline, 1 = right.
# y 0 = the attacking goal line, 1 = your own. Home always attacks towards y=0.
LANES = {"left": 0.10, "left-centre": 0.30, "centre": 0.50,
         "right-centre": 0.70, "right": 0.90}
BANDS = {"attacking-third": 0.17, "middle-third": 0.50, "defensive-third": 0.83}

LANDMARKS = {
    "attacking-goal": (0.50, 0.00), "attacking-goal-line": (0.50, 0.00),
    "attacking-six": (0.50, 0.04), "attacking-box": (0.50, 0.09),
    "attacking-penalty-spot": (0.50, 0.11), "attacking-top-of-d": (0.50, 0.22),
    "attacking-corner-left": (0.02, 0.02), "attacking-corner-right": (0.98, 0.02),
    "centre-spot": (0.50, 0.50), "centre-circle": (0.50, 0.50),
    "halfway-line": (0.50, 0.50), "halfway-left": (0.10, 0.50),
    "halfway-right": (0.90, 0.50),
    "left-touchline": (0.02, 0.50), "right-touchline": (0.98, 0.50),
    "left-wing": (0.10, 0.30), "right-wing": (0.90, 0.30),
    "own-goal": (0.50, 1.00), "own-goal-line": (0.50, 1.00),
    "own-six": (0.50, 0.96), "own-box": (0.50, 0.91),
    "own-penalty-spot": (0.50, 0.89), "top-of-d": (0.50, 0.78),
    "own-corner-left": (0.02, 0.98), "own-corner-right": (0.98, 0.98),
}


def resolve(at):
    """A place name or an explicit [x, y] -> normalised (x, y)."""
    if isinstance(at, (list, tuple)):
        return float(at[0]), float(at[1])
    if at in LANDMARKS:
        return LANDMARKS[at]
    # lane + band, in either order, e.g. "left-centre-attacking-third"
    for band, y in BANDS.items():
        if at.endswith(band):
            lane = at[: -len(band)].rstrip("-")
            if lane == "":
                return 0.50, y
            if lane in LANES:
                return LANES[lane], y
    if at in LANES:
        return LANES[at], 0.50
    if at in BANDS:
        return 0.50, BANDS[at]
    raise KeyError(f"unknown place: {at!r}")


def expand(player):
    """A player row -> list of (team, number, at).

    Accepts either the Pocket Tactic Board shape ({team, number, count}) or the
    routine shape used by the video pipeline ({key: "home7"}), so one script
    covers both.
    """
    if "key" in player:
        key = player["key"]
        team = "home" if key.startswith("home") else "away"
        return [(team, int(key[len(team):]), player["at"])]
    out = []
    n = int(player.get("count", 1))
    for i in range(n):
        out.append((player["team"], int(player["number"]) + i, player["at"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("drill")
    ap.add_argument("--marks", default="",
                    help="defender:attacker pairs, e.g. 2:7,3:9,4:10 "
                         "(away shirt marks home shirt)")
    ap.add_argument("--expect-beaten", default="",
                    help="pairs allowed to be non-goal-side in a given phase, "
                         "e.g. 3:9@4 (phase index from 0)")
    ap.add_argument("--min-gap", type=float, default=1.0,
                    help="metres; closest pair below this is reported")
    ap.add_argument("--px-per-m", type=float, default=None,
                    help="the drill's S; turns on the badge-occlusion check, "
                         "which is the one that actually bites on a small pitch")
    ap.add_argument("--dims", default=None,
                    help="WxL in metres, when coordinates are normalised against "
                         "a cropped window rather than a whole pitch, e.g. 20x20")
    args = ap.parse_args()

    drill = json.load(open(args.drill, encoding="utf-8"))

    # The window the coordinates are normalised against: --dims wins, then an
    # explicit `window`, then the named field.
    if args.dims:
        w_s, _, l_s = args.dims.lower().partition("x")
        w_m, l_m = float(w_s), float(l_s)
        field = f"{w_m:g} x {l_m:g} m window"
    elif "window" in drill:
        w_m = float(drill["window"]["widthM"])
        l_m = float(drill["window"]["lengthM"])
        field = f"{w_m:g} x {l_m:g} m window"
    else:
        field = drill.get("field", "11-a-side")
        if field not in FIELDS:
            sys.exit(f"unknown field {field!r}; expected one of {', '.join(FIELDS)}")
        w_m, l_m = FIELDS[field]

    marks = {}
    for pair in filter(None, args.marks.split(",")):
        d, a = pair.split(":")
        marks[int(d)] = int(a)

    allowed = set()
    for item in filter(None, args.expect_beaten.split(",")):
        pair, _, phase = item.partition("@")
        d, a = pair.split(":")
        allowed.add((int(d), int(a), int(phase)))

    pos = {}          # (team, number) -> (x, y)
    problems = 0

    print(f"{drill.get('title', args.drill)}  [{field}, {w_m:g} x {l_m:g} m]\n")

    for i, phase in enumerate(drill.get("phases", [])):
        for row in phase.get("players", []):
            for team, number, at in expand(row):
                try:
                    pos[(team, number)] = resolve(at)
                except KeyError as e:
                    sys.exit(f"phase {i}: {e}")

        caption = (phase.get("caption") or phase.get("role") or "").strip()
        print(f"  phase {i}  {caption[:44]}")

        # --- goal-side -------------------------------------------------
        for d_num, a_num in sorted(marks.items()):
            d, a = ("away", d_num), ("home", a_num)
            if d not in pos or a not in pos:
                continue
            dy, ay = pos[d][1], pos[a][1]
            ok = dy < ay
            if ok:
                verdict = "goal-side"
            elif (d_num, a_num, i) in allowed:
                verdict = "beaten (expected)"
            else:
                verdict = "** WRONG SIDE **"
                problems += 1
            print(f"      {d_num} vs {a_num}:  def y {dy:.2f}   att y {ay:.2f}   {verdict}")

        # --- spacing ---------------------------------------------------
        keys = list(pos)
        worst = None
        for x, k1 in enumerate(keys):
            for k2 in keys[x + 1:]:
                dx = (pos[k1][0] - pos[k2][0]) * w_m
                dy = (pos[k1][1] - pos[k2][1]) * l_m
                gap = (dx * dx + dy * dy) ** 0.5
                if worst is None or gap < worst[0]:
                    worst = (gap, k1, k2)
        if worst:
            gap, k1, k2 = worst
            tag = "  <- check this is deliberate" if gap < args.min_gap else ""
            print(f"      closest: {k1[0]} {k1[1]} / {k2[0]} {k2[1]}"
                  f"  {gap:.2f} m{tag}")

        # --- badge occlusion -------------------------------------------
        # A sprite is 16 px wide and 22 tall, and its shirt number sits about
        # 8 px above it. So two players within a sprite width of each other
        # horizontally must be a sprite-plus-badge apart vertically, or the
        # upper one's number vanishes behind the lower one's body. Euclidean
        # distance does not catch this: the exclusion zone is a tall ellipse.
        if args.px_per_m:
            min_dx, min_dy = 16 / args.px_per_m, 30 / args.px_per_m
            for x, k1 in enumerate(keys):
                for k2 in keys[x + 1:]:
                    dx = abs(pos[k1][0] - pos[k2][0]) * w_m
                    dy = abs(pos[k1][1] - pos[k2][1]) * l_m
                    if dx < min_dx and dy < min_dy:
                        problems += 1
                        print(f"      ** BADGE HIDDEN ** {k1[0]} {k1[1]} / "
                              f"{k2[0]} {k2[1]}: dx {dx:.2f} dy {dy:.2f} "
                              f"(need dx > {min_dx:.2f} or dy > {min_dy:.2f})")
        print()

    # --- squad size ----------------------------------------------------
    sizes = {"futsal": 5, "7-a-side": 7, "9-a-side": 9, "11-a-side": 11}
    if field in sizes:
        expected = sizes[field]
        for team in ("home", "away"):
            n = sum(1 for (t, _) in pos if t == team)
            if n and n != expected:
                print(f"  note: {team} has {n} player(s); {field} is {expected} a side "
                      f"(keeper included)")
    else:
        for team in ("home", "away"):
            n = sum(1 for (t, _) in pos if t == team)
            if n:
                print(f"  note: {team} has {n} player(s) on screen")
    print()

    if problems:
        print(f"{problems} positioning problem(s). Fix before rendering.")
        return 1
    print("No unexpected positioning problems.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
