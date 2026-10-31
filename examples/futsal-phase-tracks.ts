import { Easing } from "remotion";
import { N } from "./nesTheme";
import type { Kit } from "./nes";

/**
 * Futsal corner routine, driven by the same positions as futsal-corner-drill.json
 * so the video and the tactic-board code never drift apart.
 *
 * Court is 40 x 20 m. Normalised drill coordinates: x 0 = left touchline,
 * 1 = right; y 0 = attacking goal line, 1 = own goal line (so y 0.25 = 10 m out).
 */
export const COURT_W = 20; // metres
export const COURT_L = 40; // metres
export const S = 9.5; // pixels per metre — the SAME on both axes
export const CX = 104; // centre of the pitch region on screen
export const TOP = 34; // screen y of the attacking goal line (room for the corner taker above it)

export type NP = { x: number; y: number };

/** Normalised drill coordinate -> screen pixel. */
export const toScreen = (p: NP) => ({
  x: CX + (p.x - 0.5) * COURT_W * S,
  y: TOP + p.y * COURT_L * S,
});
export const snap = (p: NP) => {
  const s = toScreen(p);
  return { x: Math.round(s.x), y: Math.round(s.y) };
};

/** The few named places the drill JSON uses. */
export const PLACES: Record<string, NP> = {
  "attacking-corner-right": { x: 0.98, y: 0.02 },
  "attacking-top-of-d": { x: 0.5, y: 0.22 },
  "attacking-goal": { x: 0.5, y: 0.012 },
};

export type Side = "home" | "away";
export const KITS: Record<Side | "keeper", Kit> = {
  home: { hair: N.hairBlack, jersey: N.red, trim: N.white, shorts: N.white },
  away: { hair: N.brown, jersey: N.blue, trim: N.white, shorts: N.white },
  keeper: { hair: N.gold, jersey: N.yellow, trim: N.black, shorts: N.black },
};

export type Actor = { id: number; side: Side; keeper?: boolean };
export const ACTORS: Actor[] = [
  { id: 5, side: "home" },
  { id: 7, side: "home" },
  { id: 9, side: "home" },
  { id: 10, side: "home" },
  { id: 1, side: "away", keeper: true },
  { id: 2, side: "away" },
  { id: 3, side: "away" },
  { id: 4, side: "away" },
  { id: 6, side: "away" }, // near-post zonal defender
];
const key = (a: Actor) => `${a.side}${a.id}`;

/** Per phase: only the actors that move, exactly as the drill JSON lists them. */
type PhaseDef = {
  hold: number; // frames this phase occupies
  moves: Record<string, NP>;
  ballTo?: number; // home shirt number the ball ends with
  caption: string;
};

export const BALL_START = 5;

export const PHASES: PhaseDef[] = [
  {
    hold: 110,
    caption: "右路角球",
    moves: {
      home5: PLACES["attacking-corner-right"],
      home7: { x: 0.82, y: 0.15 },
      home9: { x: 0.62, y: 0.13 },
      home10: PLACES["attacking-top-of-d"],
      // every defender starts goal-side of the man they mark
      away1: { x: 0.5, y: 0.06 },
      away2: { x: 0.76, y: 0.11 },
      away3: { x: 0.55, y: 0.1 },
      away4: { x: 0.5, y: 0.17 },
      away6: { x: 0.6, y: 0.07 }, // guards the near post
    },
  },
  {
    hold: 100,
    caption: "開短波",
    moves: { home7: { x: 0.86, y: 0.12 }, away2: { x: 0.81, y: 0.11 } },
    ballTo: 7,
  },
  {
    hold: 100,
    caption: "九號擋人",
    moves: {
      home9: { x: 0.55, y: 0.19 },
      away3: { x: 0.52, y: 0.15 },
      home10: { x: 0.62, y: 0.21 },
      away4: { x: 0.54, y: 0.18 }, // screened off laterally, still goal-side
      away6: { x: 0.59, y: 0.11 }, // steps off the post as the ball comes back
    },
  },
  {
    hold: 100,
    caption: "十號射門",
    moves: { away1: { x: 0.55, y: 0.06 }, away4: { x: 0.58, y: 0.19 } },
    ballTo: 10,
  },
  {
    hold: 120,
    caption: "遠柱補射",
    // the shot comes from the right, so the far post is the LEFT one
    moves: { home9: { x: 0.45, y: 0.08 }, away3: { x: 0.5, y: 0.11 }, away6: { x: 0.58, y: 0.09 } },
    ballTo: 9,
  },
];

export const PHASE_START = PHASES.reduce<number[]>((acc, p, i) => {
  acc.push(i === 0 ? 0 : acc[i - 1] + PHASES[i - 1].hold);
  return acc;
}, []);
export const ROUTINE_LEN = PHASE_START[PHASES.length - 1] + PHASES[PHASES.length - 1].hold;

const MOVE = 45; // frames a player takes to travel between phases
const PASS = 16; // frames the ball takes

const ease = Easing.inOut(Easing.sin);

/** Where an actor stands at a given frame, carrying positions forward. */
export const actorAt = (a: Actor, frame: number): NP => {
  const k = key(a);
  let cur = PHASES[0].moves[k];
  for (let i = 0; i < PHASES.length; i++) {
    const target = PHASES[i].moves[k];
    if (!target) continue;
    const t0 = PHASE_START[i];
    if (i === 0 || frame >= t0 + MOVE) {
      cur = target;
      continue;
    }
    if (frame <= t0) break;
    const u = ease((frame - t0) / MOVE);
    return { x: cur.x + (target.x - cur.x) * u, y: cur.y + (target.y - cur.y) * u };
  }
  return cur;
};

/** Which shirt has the ball before a given phase. */
const holderBefore = (i: number) => {
  let h = BALL_START;
  for (let k = 1; k <= i; k++) if (PHASES[k].ballTo !== undefined) h = PHASES[k].ballTo!;
  return h;
};

/** Ball position: with its holder, or in flight between two of them. */
export const ballAt = (frame: number): NP => {
  let holder = BALL_START;
  for (let i = 1; i < PHASES.length; i++) {
    const to = PHASES[i].ballTo;
    if (to === undefined) continue;
    const t0 = PHASE_START[i];
    if (frame < t0) break;
    if (frame < t0 + PASS) {
      const from = holderBefore(i - 1);
      const a = actorAt(ACTORS.find((x) => x.side === "home" && x.id === from)!, frame);
      const b = actorAt(ACTORS.find((x) => x.side === "home" && x.id === to)!, frame);
      const u = Easing.out(Easing.quad)((frame - t0) / PASS);
      return { x: a.x + (b.x - a.x) * u, y: a.y + (b.y - a.y) * u };
    }
    holder = to;
  }
  const h = ACTORS.find((x) => x.side === "home" && x.id === holder)!;
  const p = actorAt(h, frame);
  return { x: p.x + 0.018, y: p.y + 0.004 };
};

/** True while the ball is travelling — used to draw the pass line. */
export const passInFlight = (frame: number) => {
  for (let i = 1; i < PHASES.length; i++) {
    if (PHASES[i].ballTo === undefined) continue;
    const t0 = PHASE_START[i];
    if (frame >= t0 && frame < t0 + PASS + 10) {
      return { from: holderBefore(i - 1), to: PHASES[i].ballTo! };
    }
  }
  return null;
};

export const phaseIndexAt = (frame: number) => {
  let idx = 0;
  PHASE_START.forEach((t, i) => {
    if (frame >= t) idx = i;
  });
  return idx;
};
