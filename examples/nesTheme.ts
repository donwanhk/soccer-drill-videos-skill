/**
 * Palette and metrics for the 熱血足球 (Technōs, 1990) look: a top-down pitch
 * drawn on a low-resolution grid with a hard NES colour set — flat fills,
 * black outlines, no gradients and no anti-aliasing.
 */

// Virtual framebuffer: 320 x 180 "pixels" blown up 6x to 1920 x 1080.
export const VW = 320;
export const VH = 180;
export const PX = 6;

// The pitch is a true square seen from directly above, so it needs a square
// region: the pitch takes the left of the frame, the info panel the right.
export const PANEL_X = 208;

/** Colours taken from the NES master palette. */
export const N = {
  black: "#000000",
  white: "#fcfcfc",
  grey: "#bcbcbc",
  darkGrey: "#7c7c7c",
  grassLight: "#00b800",
  grassDark: "#009400",
  grassShade: "#007800",
  skin: "#fcbcb0",
  skinDark: "#d88070",
  red: "#f83800",
  redDark: "#a81000",
  salmon: "#fc7460",
  orange: "#fc9838",
  yellow: "#fcd8a8",
  gold: "#f8b800",
  blue: "#0058f8",
  blueDark: "#0000bc",
  blueLight: "#3cbcfc",
  purple: "#6844fc",
  brown: "#a84400",
  hairBlack: "#1c1c1c",
} as const;

export const FONT_PX = '"Press Start 2P", monospace';
/** GNU Unifont: a true 16x16 bitmap face, so Chinese stays 8-bit. */
export const FONT_CN = '"Unifont", monospace';

/** Per-player kit + hair, in the two-team NES style (red squad vs white squad). */
export const NES_PLAYER: Record<number, { hair: string; jersey: string; trim: string; shorts: string }> = {
  1: { hair: N.hairBlack, jersey: N.red, trim: N.white, shorts: N.white },
  2: { hair: N.brown, jersey: N.red, trim: N.white, shorts: N.white },
  3: { hair: N.gold, jersey: N.red, trim: N.white, shorts: N.white },
  4: { hair: N.hairBlack, jersey: N.white, trim: N.red, shorts: N.blue },
  5: { hair: N.orange, jersey: N.white, trim: N.red, shorts: N.blue },
};
