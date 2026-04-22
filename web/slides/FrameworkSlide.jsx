// FrameworkSlide — spectrum axis + 4 colored cards.
// Top: two-end axis labels on a line. Bottom: 4 cards, each a colored pill
// with short hypothesis title and body.

import React from "react";
import { Logo, Arrow, Tag } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function FrameworkSlide({
  tag = "Framework",
  title = "Four directions on the spectrum",
  axisLeft = "Functional",
  axisRight = "Emotional",
  cards = [
    { color: "#E05820", title: "Direction A", body: "Shortest sentence that earns its place." },
    { color: "#D4D830", title: "Direction B", body: "Shortest sentence that earns its place." },
    { color: "#9898B8", title: "Direction C", body: "Shortest sentence that earns its place." },
    { color: "#BE40BE", title: "Direction D", body: "Shortest sentence that earns its place." },
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
        position: "absolute", top: 360, left: 72, right: 72,
        fontFamily: font, color: "#1A1A1A",
      }}>
        <div style={{
          display: "flex", justifyContent: "space-between",
          fontSize: 12, fontWeight: 400, letterSpacing: "0.08em",
          textTransform: "uppercase", opacity: 0.5, marginBottom: 12,
        }}>
          <span>{axisLeft}</span><span>{axisRight}</span>
        </div>
        <div style={{ height: 2, background: "#1A1A1A" }} />
      </div>

      <div style={{
        position: "absolute", top: 448, left: 72, right: 72, bottom: 140,
        display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 24,
        fontFamily: font,
      }}>
        {cards.map((c, i) => (
          <div key={i} style={{
            background: c.color, borderRadius: 24, padding: 28,
            color: "#1A1A1A", display: "flex", flexDirection: "column",
          }}>
            <div style={{
              fontSize: 23, fontWeight: 700, lineHeight: 1.25, marginBottom: 20,
            }}>{c.title}</div>
            <div style={{ fontSize: 15, lineHeight: 1.58 }}>{c.body}</div>
          </div>
        ))}
      </div>

      <Arrow variant="dark" />
    </section>
  );
}
