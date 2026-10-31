import React from "react";
import { Audio } from "@remotion/media";
import { Sequence, interpolate, staticFile } from "remotion";
import { PHASES, PHASE_START } from "./futsal";

// Scene start frames on the main timeline (the wipe overlaps by 15).
const TITLE = 60;
const COACH = 575;

// Spoken Cantonese narration (macOS Sinji, zh_HK, rate 230).
export const NARRATION = [
  { file: "f1", from: 70, len: 89 }, // 右路角球，五號開波
  { file: "f2", from: 175, len: 66 }, // 開短波，二號出嚟逼
  { file: "f3", from: 275, len: 84 }, // 九號擋人，十號繞出去
  { file: "f4", from: 375, len: 84 }, // 擺返，低波射遠柱
  { file: "f5", from: 475, len: 95 }, // 遠柱補射入網
  { file: "f6", from: 590, len: 205 }, // 教練要點
];

const speaking = (f: number) => NARRATION.some((n) => f >= n.from - 4 && f <= n.from + n.len + 4);

// Every phase that moves the ball gives a kick on the strike and a trap on arrival.
const passes = PHASES.map((p, i) => ({ p, i }))
  .filter(({ p }) => p.ballTo !== undefined)
  .map(({ i }) => TITLE + PHASE_START[i]);

const SFX: { file: string; at: number; volume: number }[] = [
  { file: "impact", at: 0, volume: 0.9 },
  { file: "sparkle", at: 20, volume: 0.45 },
  { file: "whoosh", at: TITLE - 2, volume: 0.8 },
  ...passes.flatMap((t) => [
    { file: "kick", at: t - 1, volume: 0.85 },
    { file: "trap", at: t + 16, volume: 0.6 },
  ]),
  { file: "chime", at: 505, volume: 0.5 }, // the finish
  { file: "whoosh", at: COACH - 2, volume: 0.8 },
  { file: "impact", at: COACH + 2, volume: 0.5 },
  ...[20, 55, 90, 125].map((d) => ({ file: "pop", at: COACH + d, volume: 0.6 })),
  { file: "sparkle", at: COACH + 160, volume: 0.45 },
];

export const FutsalSoundtrack: React.FC = () => (
  <>
    <Audio
      name="Music"
      loop
      src={staticFile("audio/bgm.wav")}
      volume={(f) =>
        interpolate(f, [0, 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) *
        (speaking(f) ? 0.17 : 0.5)
      }
    />
    {NARRATION.map((n) => (
      <Sequence key={n.file} name={`Narration ${n.file}`} from={n.from} layout="none">
        <Audio src={staticFile(`audio/${n.file}.wav`)} volume={1} />
      </Sequence>
    ))}
    {SFX.map((s, i) => (
      <Sequence key={i} name={`SFX ${s.file}`} from={Math.max(0, s.at)} layout="none">
        <Audio src={staticFile(`audio/${s.file}.wav`)} volume={s.volume} />
      </Sequence>
    ))}
  </>
);
