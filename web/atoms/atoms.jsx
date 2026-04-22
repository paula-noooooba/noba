// NOBA shared atoms.
//
// Visual primitives reused across every slide component in web/slides/.
// These are the canonical implementations — design/tokens.json mirrors
// their values, and scripts/build_deck.py atom helpers reproduce them
// in python-pptx.

import React from "react";

const ink    = "#1A1A1A";
const paper  = "#FFFFFF";
const dark   = "#393939";
const gray   = "#DCDCDC";
const midInk = "rgba(26,26,26,0.45)";
const midInv = "rgba(255,255,255,0.5)";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export function Logo({ variant = "dark", position = "inside" }) {
  const color = variant === "light" ? paper : ink;
  const top   = position === "cover" ? 60 : 48;
  const right = position === "cover" ? 72 : 60;
  return (
    <div style={{
      position: "absolute", top, right,
      fontFamily: font, fontWeight: 700, fontSize: 24,
      letterSpacing: "-0.01em", color,
    }}>
      noba
      <div style={{
        fontWeight: 400, fontSize: 11, letterSpacing: "0.04em",
        color, opacity: 0.7, marginTop: 2,
      }}>
        a gellify company
      </div>
    </div>
  );
}

export function Arrow({ variant = "dark" }) {
  const stroke = variant === "light" ? paper : ink;
  return (
    <svg style={{ position: "absolute", right: 60, bottom: 48 }}
         width="80" height="24" viewBox="0 0 80 24" fill="none">
      <line x1="0" y1="12" x2="74" y2="12" stroke={stroke} strokeWidth="1.5" />
      <polyline points="66,4 74,12 66,20" stroke={stroke} strokeWidth="1.5" fill="none" />
    </svg>
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
