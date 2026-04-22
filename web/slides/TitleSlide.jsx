// TitleSlide — cover slide.
//
// Figma source of truth: qqNtw4M8gc3zYRHwKJae7W, node 3:5
// https://www.figma.com/design/qqNtw4M8gc3zYRHwKJae7W/NOBA-PPT-Design-System?node-id=3-5
//
// Anatomy:
// - Full-bleed white background, 48px padding on all sides (24px at
//   Figma 960×540 scale → 48px at our 1920×1080 slide scale).
// - Logo atom pinned top-right (368×48 image, the N[capsule]BA wordmark).
// - Left-aligned title group: 140px title (ink), 36px subtitle (ink,
//   Light). Title box is 1094px wide so long titles wrap at the same
//   point regardless of content.
// - Bottom-left caption row: the arrow glyph inline, then a single
//   "Prepared for <client> | <date>" line at 24px, 50% black.
//
// No shell, no accent colour on the title, no eyebrow — those belong
// to earlier iterations and are intentionally removed.

import React from "react";
import { Logo, Arrow } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function TitleSlide({
  title = "Next-Generation Coffee Innovation",
  subtitle = "Identifying and testing new growth opportunities",
  client = "lavazza",
  date = "september 2025",
}) {
  return (
    <section className="slide" style={{
      background: "#FFFFFF", position: "relative",
      width: 1920, height: 1080,
      padding: 48, boxSizing: "border-box",
    }}>
      <Logo variant="dark" position="cover" />

      <div style={{
        position: "absolute", left: 48, top: 322, width: 1094,
        display: "flex", flexDirection: "column", gap: 20,
      }}>
        <h1 style={{
          margin: 0,
          fontFamily: font, fontWeight: 300, fontSize: 140,
          lineHeight: 1, letterSpacing: "-0.3px", color: "#1A1A1A",
        }}>
          {title}
        </h1>
        <div style={{
          fontFamily: font, fontWeight: 300, fontSize: 36,
          lineHeight: 1.2, color: "#1A1A1A",
        }}>
          {subtitle}
        </div>
      </div>

      <div style={{
        position: "absolute", left: 48, bottom: 48,
        display: "flex", alignItems: "center", gap: 20,
        fontFamily: font, fontWeight: 400, fontSize: 24,
        color: "#1A1A1A",
      }}>
        <Arrow variant="dark" />
        <span>Prepared for {client} | {date}</span>
      </div>
    </section>
  );
}
