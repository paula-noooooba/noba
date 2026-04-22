// DeliverablesSlide — 2-col: statement + colored-dot list.
// Left: accent-color statement. Right: rows of dot + deliverable name + short body.

import React from "react";
import { Logo, Arrow, Tag } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function DeliverablesSlide({
  tag = "Deliverables",
  statement = "What you walk away with.",
  accent = "#4A7FC8",
  items = [
    { color: "#E05820", title: "Insight report",    body: "One document, decision-ready." },
    { color: "#CBDC3A", title: "Workshop playback", body: "Key moments, captured and shareable." },
    { color: "#BE40BE", title: "Go-to-market brief",body: "The story and the rollout plan." },
  ],
}) {
  return (
    <section className="slide" style={{ background: "#FFFFFF" }}>
      <Logo variant="dark" position="inside" />

      <div style={{ position: "absolute", top: 60, left: 72 }}>
        <Tag>{tag}</Tag>
      </div>

      <h2 style={{
        position: "absolute", top: 208, left: 72, width: 820, margin: 0,
        fontFamily: font, fontSize: 62, fontWeight: 300,
        lineHeight: 1.05, letterSpacing: "-0.015em", color: accent,
      }}>{statement}</h2>

      <div style={{
        position: "absolute", top: 208, right: 72, width: 820,
        fontFamily: font, color: "#1A1A1A",
      }}>
        {items.map((it, i) => (
          <div key={i} style={{
            padding: "28px 0",
            borderTop: i === 0 ? "1px solid #DCDCDC" : "none",
            borderBottom: "1px solid #DCDCDC",
            display: "grid", gridTemplateColumns: "40px 1fr", alignItems: "start",
            gap: 16,
          }}>
            <div style={{
              width: 20, height: 20, borderRadius: "50%", background: it.color,
              marginTop: 8,
            }} />
            <div>
              <div style={{ fontSize: 23, fontWeight: 700, lineHeight: 1.25 }}>
                {it.title}
              </div>
              <div style={{ marginTop: 8, fontSize: 17, lineHeight: 1.62 }}>
                {it.body}
              </div>
            </div>
          </div>
        ))}
      </div>

      <Arrow variant="dark" />
    </section>
  );
}
