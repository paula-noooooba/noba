// GanttSlide — 2-col: big week-count number + gantt-style phase table.
// Left: "8 weeks" display number + caption. Right: rows of phase name + bar.

import React from "react";
import { Logo, Arrow, Tag } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function GanttSlide({
  tag = "Timings",
  bigNumber = "8",
  bigUnit = "weeks",
  caption = "From kickoff to shareable direction.",
  weeks = 8,
  phases = [
    { name: "Sense",  start: 0, len: 2, color: "#E05820" },
    { name: "Shape",  start: 2, len: 2, color: "#CBDC3A" },
    { name: "Stress", start: 4, len: 2, color: "#BE40BE" },
    { name: "Ship",   start: 6, len: 2, color: "#4A7FC8" },
  ],
}) {
  return (
    <section className="slide" style={{ background: "#FFFFFF" }}>
      <Logo variant="dark" position="inside" />

      <div style={{ position: "absolute", top: 60, left: 72 }}>
        <Tag>{tag}</Tag>
      </div>

      <div style={{
        position: "absolute", top: 208, left: 72, width: 720,
        fontFamily: font, color: "#1A1A1A",
      }}>
        <div style={{
          fontSize: 160, fontWeight: 300, lineHeight: 0.95,
          letterSpacing: "-0.02em",
        }}>
          {bigNumber}
          <span style={{ fontSize: 48, marginLeft: 12 }}>{bigUnit}</span>
        </div>
        <div style={{
          marginTop: 28, fontSize: 23, fontWeight: 400, lineHeight: 1.4,
        }}>{caption}</div>
      </div>

      <div style={{
        position: "absolute", top: 220, right: 72, width: 1000,
        fontFamily: font, color: "#1A1A1A",
      }}>
        <div style={{
          display: "grid",
          gridTemplateColumns: `160px repeat(${weeks}, 1fr)`,
          fontSize: 12, letterSpacing: "0.08em",
          textTransform: "uppercase", opacity: 0.5,
          paddingBottom: 12, borderBottom: "1px solid #DCDCDC",
        }}>
          <div />
          {Array.from({ length: weeks }, (_, i) => (
            <div key={i} style={{ textAlign: "center" }}>W{i + 1}</div>
          ))}
        </div>

        {phases.map((p, i) => (
          <div key={i} style={{
            display: "grid",
            gridTemplateColumns: `160px repeat(${weeks}, 1fr)`,
            alignItems: "center", padding: "20px 0",
            borderBottom: "1px solid #DCDCDC",
          }}>
            <div style={{ fontSize: 17, fontWeight: 700 }}>{p.name}</div>
            <div style={{
              gridColumn: `${p.start + 2} / span ${p.len}`,
              height: 24, borderRadius: 999, background: p.color,
            }} />
          </div>
        ))}
      </div>

      <Arrow variant="dark" />
    </section>
  );
}
