// ContentSlide — section tag + big title + 3-card grid.
// Each card: numbered heading (01/02/03), bold title, body copy.

import React from "react";
import { Logo, Arrow, Tag } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function ContentSlide({
  tag = "Approach",
  title = "Three moves that matter",
  cards = [
    { num: "01", title: "First", body: "Short sentence." },
    { num: "02", title: "Second", body: "Short sentence." },
    { num: "03", title: "Third", body: "Short sentence." },
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
      }}>
        {title}
      </h2>

      <div style={{
        position: "absolute", top: 424, left: 72, right: 72, bottom: 140,
        display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 24,
      }}>
        {cards.map((c, i) => (
          <div key={i} style={{
            background: "#F0F0F0", borderRadius: 24, padding: 36,
            fontFamily: font, color: "#1A1A1A",
            display: "flex", flexDirection: "column",
          }}>
            <div style={{
              fontSize: 12, fontWeight: 400, letterSpacing: "0.08em",
              textTransform: "uppercase", opacity: 0.5, marginBottom: 28,
            }}>{c.num}</div>
            <div style={{
              fontSize: 23, fontWeight: 700, lineHeight: 1.25, marginBottom: 16,
            }}>{c.title}</div>
            <div style={{
              fontSize: 17, fontWeight: 400, lineHeight: 1.62,
            }}>{c.body}</div>
          </div>
        ))}
      </div>

      <Arrow variant="dark" />
    </section>
  );
}
