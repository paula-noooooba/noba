// TimelineSlide — 4 numbered dots on a horizontal axis line.
// Each phase: dot + code name + week range + short descriptor below the line.

import React from "react";
import { Logo, Arrow, Tag } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function TimelineSlide({
  tag = "Methodology",
  title = "A four-phase path to clarity",
  phases = [
    { num: "01", name: "Sense",   range: "Wk 1–2", body: "Map the terrain." },
    { num: "02", name: "Shape",   range: "Wk 3–4", body: "Frame hypotheses." },
    { num: "03", name: "Stress",  range: "Wk 5–6", body: "Test with real users." },
    { num: "04", name: "Ship",    range: "Wk 7–8", body: "Package the direction." },
  ],
}) {
  return (
    <section className="slide" style={{ background: "#FFFFFF" }}>
      <Logo variant="dark" position="inside" />

      <div style={{ position: "absolute", top: 60, left: 72 }}>
        <Tag>{tag}</Tag>
      </div>
      <h2 style={{
        position: "absolute", top: 144, left: 72, right: 72, margin: 0,
        fontFamily: font, fontSize: 48, fontWeight: 300,
        lineHeight: 1.1, letterSpacing: "-0.01em", color: "#1A1A1A",
      }}>{title}</h2>

      <div style={{
        position: "absolute", top: 560, left: 72, right: 72, height: 2,
        background: "#1A1A1A",
      }} />

      <div style={{
        position: "absolute", top: 400, left: 72, right: 72,
        display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 24,
        fontFamily: font, color: "#1A1A1A",
      }}>
        {phases.map((p, i) => (
          <div key={i} style={{ position: "relative", paddingBottom: 200 }}>
            <div style={{
              fontSize: 12, fontWeight: 400, letterSpacing: "0.08em",
              textTransform: "uppercase", opacity: 0.5, marginBottom: 12,
            }}>{p.num} · {p.range}</div>
            <div style={{ fontSize: 28, fontWeight: 700, lineHeight: 1.2 }}>
              {p.name}
            </div>
            <div style={{
              position: "absolute", top: 170, left: 0,
              width: 20, height: 20, borderRadius: "50%", background: "#1A1A1A",
            }} />
            <div style={{
              position: "absolute", top: 220, left: 0, right: 16,
              fontSize: 15, lineHeight: 1.58,
            }}>{p.body}</div>
          </div>
        ))}
      </div>

      <Arrow variant="dark" />
    </section>
  );
}
