#!/usr/bin/env python3
"""Print the YouTube description for a drill, straight from the drill JSON.

The description and the video are generated from the same file, so they cannot
disagree. Nothing here is written by hand: if a line reads badly, fix the drill
JSON and the video picks up the same change.

    python3 make_description.py src/drills/rondo-scored.json
    python3 make_description.py src/drills/*.json --out out/descriptions

The title line is the drill title plus its subtitle, which is what the channel
uses as the video title too.
"""

import argparse
import json
import sys
from pathlib import Path

DIFFICULTY = {1: "初級", 2: "中級", 3: "高級"}

# Channel-wide. Tags go last so the readable part stays above the fold.
TAGS = ["#足球訓練", "#足球戰術", "#粵語", "#青訓", "#教練"]


def block(heading, lines):
    """A heading and its lines, or nothing at all when there is no content."""
    rows = [ln for ln in lines if ln]
    return [heading, *rows, ""] if rows else []


def describe(drill):
    spec = drill.get("spec", {})
    problem = drill.get("problem", {})
    winning = drill.get("winning", {})
    rotation = drill.get("rotation", {})
    out = []

    # the hook: the problem a coach already recognises, before any detail
    if problem.get("pain"):
        out += [problem["pain"], ""]

    out += [f'{drill["title"]}｜{drill.get("subtitle", "")}'.rstrip("｜ "), ""]

    if spec:
        out += [
            f'主題：{spec.get("theme", "")}｜類別：{spec.get("category", "")}',
            f'人數：{spec.get("players", "")}'
            f'｜難度：{DIFFICULTY.get(spec.get("difficulty"), "")}'
            f'｜年齡：{spec.get("ages", "")}',
            f'場地：{spec.get("area", "")}｜時間：{spec.get("duration", "")}',
            "",
        ]

    out += block("【練習目標】", [problem.get("aim")])
    # the video shows the start cones and the serve; a coach reading before
    # watching needs them in writing too
    start = drill.get("start", {})
    out += block("【開始】", [start.get("positions"), start.get("server")])
    out += block(
        "【點樣分勝負】",
        [
            f'進攻：{winning["home"]}' if winning.get("home") else None,
            f'防守：{winning["away"]}' if winning.get("away") else None,
            winning.get("decides"),
        ],
    )
    out += block("【輪轉】", [rotation.get("note")])
    out += block(
        "【重點】",
        [f'{i}. {p["title"]} — {p["d"]}' for i, p in enumerate(drill.get("points", []), 1)],
    )
    out += block("【變化】", [f"· {v}" for v in drill.get("variations", [])])
    out += block(
        "【進階】",
        [f'· {p["level"]}：{p["detail"]}' for p in drill.get("progression", [])],
    )

    if drill.get("question"):
        out += [drill["question"], ""]

    out += [" ".join(TAGS)]
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("drills", nargs="+")
    ap.add_argument("--out", default=None,
                    help="directory to write <id>.txt into; prints to stdout otherwise")
    args = ap.parse_args()

    out_dir = Path(args.out) if args.out else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    for path in args.drills:
        drill = json.loads(Path(path).read_text(encoding="utf-8"))
        text = describe(drill)
        if out_dir:
            dest = out_dir / f'{drill["id"]}.txt'
            dest.write_text(text, encoding="utf-8")
            print(f'{dest}  ({len(text)} chars)', file=sys.stderr)
        else:
            print(text)


if __name__ == "__main__":
    main()
