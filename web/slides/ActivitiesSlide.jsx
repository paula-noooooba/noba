// ActivitiesSlide — 3 big cards w/ colored dots + entregables strip.
// Cards are F0F0F0 with accent-colored dot + activity title + body.
// Bottom strip: "ENTREGABLES" label + deliverable chips.

import React from "react";
import { Logo, Arrow, Tag, Dot } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function ActivitiesSlide({
  tag = "Activities",
  title = "Three tracks, one proof point",
  cards = [
    { color: "#E05820", title: "Track one", body: "Concrete activity." },
    { color: "#CBDC3A", title: "Track two", body: "Concrete activity." },
    { color: "#BE40BE", title: "Track three", body: "Concrete activity." },
  ],
  deliverables = ["Insight report", "Workshop playback", "Go-to-market brief"],
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
        position: "absolute", top: 360, left: 72, right: 72, height: 480,
        display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 24,
      }}>
        {cards.map((c, i) => (
          <div key={i} style={{
            background: "#F0F0F0", borderRadius: 24, padding: 36,
            fontFamily: font, color: "#1A1A1A",
            position: "relative",
          }}>
            <div style={{
              width: 20, height: 20, borderRadius: "50%", background: c.color,
              marginBottom: 40,
            }} />
            <div style={{
              fontSize: 28, fontWeight: 700, lineHeight: 1.2, marginBottom: 20,
            }}>{c.title}</div>
            <div style={{
              fontSize: 17, fontWeight: 400, lineHeight: 1.62,
            }}>{c.body}</div>
          </div>
        ))}
      </div>

      <div style={{
        position: "absolute", bottom: 72, left: 72, right: 72,
        paddingTop: 28, borderTop: "1px solid #DCDCDC",
        fontFamily: font, color: "#1A1A1A",
        display: "flex", alignItems: "baseline", gap: 40,
      }}>
        <div style={{
          fontSize: 12, fontWeight: 400, letterSpacing: "0.08em",
          textTransform: "uppercase", opacity: 0.5, whiteSpace: "nowrap",
        }}>Deliverables</div>
        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          {deliverables.map((d, i) => (
            <span key={i} style={{
              padding: "6px 14px", border: "1px solid rgba(26,26,26,0.45)",
              borderRadius: 999, fontSize: 13,
            }}>{d}</span>
          ))}
        </div>
      </div>

      <Arrow variant="dark" />
    </section>
  );
}
