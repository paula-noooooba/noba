// NOBA shared atoms.
//
// Visual primitives reused across every slide component in web/slides/.
// These are the canonical implementations — design/tokens.json mirrors
// their values, and scripts/build_deck.py atom helpers reproduce them
// in python-pptx.
//
// Logo + Arrow assets come from web/assets/*.svg, exported from the
// NOBA PPT Design System Figma file (qqNtw4M8gc3zYRHwKJae7W).

import React from "react";

const ink    = "#1A1A1A";
const paper  = "#FFFFFF";
const dark   = "#393939";
const gray   = "#DCDCDC";
const midInk = "rgba(26,26,26,0.45)";
const midInv = "rgba(255,255,255,0.5)";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

// Cover scale: 2× Figma (Figma frame is 960×540, our render is 1920×1080).
// Figma logo: 184.32×24 → 368.64×48 at slide scale. Keep the halves handy
// for JSX demos at the Figma scale (in web/templates/*.html the slide is
// 1920×1080 via deck-stage so we use the slide-scale values here).
export function Logo({ variant = "dark", position = "inside", width = 368, height = 48 }) {
  const src = variant === "light" ? "../assets/logo-noba-neg.svg"
                                  : "../assets/logo-noba.svg";
  const top = position === "cover" ? 48 : 48;
  return (
    <img src={src} alt="NOBA"
         style={{
           position: "absolute", top, right: 48,
           width, height, display: "block",
         }} />
  );
}

// Stroke-only right arrow. Sits inline before the bottom caption on most
// slides (including the cover), not at bottom-right of the slide.
// Figma: 17.84×17.25 at 960 frame → 36×35 at slide scale.
export function Arrow({ variant = "dark", width = 36, height = 35, opacity = 0.5 }) {
  const src = variant === "light" ? "../assets/arrow-neg.svg"
                                  : "../assets/arrow.svg";
  return (
    <img src={src} alt=""
         style={{
           display: "inline-block", width, height, opacity,
           verticalAlign: "middle",
         }} />
  );
}

export function Tag({ children, tone = "ink" }) {
  const color  = tone === "inv" ? paper : ink;
  const border = tone === "inv" ? midInv : midInk;
  return (
    <span style={{
      display: "inline-block",
      padding: "6px 14px",
      border: `1px solid ${border}`,
      borderRadius: 999,
      fontFamily: font, fontWeight: 400, fontSize: 12,
      letterSpacing: "0.08em", textTransform: "uppercase",
      color,
    }}>
      {children}
    </span>
  );
}

export function Shell({ children, tone = "paper" }) {
  const bg = tone === "dark" ? dark : paper;
  return (
    <div style={{
      position: "absolute", inset: 24, background: bg,
      borderRadius: 24, overflow: "hidden",
    }}>
      {children}
    </div>
  );
}

export function Rule({ y, tone = "ink", left = 72, right = 72 }) {
  const bg = tone === "inv" ? midInv : gray;
  return (
    <div style={{
      position: "absolute", top: y, left, right,
      height: 1, background: bg,
    }} />
  );
}

export function Dot({ x, y, color, size = "md" }) {
  const d = size === "lg" ? 20 : 12;
  return (
    <div style={{
      position: "absolute", left: x, top: y,
      width: d, height: d, borderRadius: "50%", background: color,
    }} />
  );
}
