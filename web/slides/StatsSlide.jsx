// StatsSlide — 4 overlapping colored circles with big numbers.
// Used for expertise stats / headline metrics.

import React from "react";
import { Logo, Arrow, Tag } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function StatsSlide({
  tag = "Our expertise",
  title = "Four numbers, one story",
  stats = [
    { num: "120+", label: "Projects shipped", color: "#E05820" },
    { num: "20",   label: "Countries",        color: "#CBDC3A" },
    { num: "40+",  label: "Active brands",    color: "#BE40BE" },
    { num: "10y",  label: "Track record",     color: "#4A7FC8" },
  ],
}) {
  const size = 220;
  const overlap = -32;
  const totalWidth = size * stats.length + overlap * (stats.length - 1);

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
        position: "absolute", top: 440, left: "50%", transform: "translateX(-50%)",
        width: totalWidth, display: "flex",
        fontFamily: font,
      }}>
        {stats.map((s, i) => (
          <div key={i} style={{
            width: size, height: size, borderRadius: "50%",
            background: s.color,
            marginLeft: i === 0 ? 0 : overlap,
            display: "flex", flexDirection: "column",
            justifyContent: "center", alignItems: "center",
            color: "#1A1A1A", textAlign: "center",
            position: "relative", zIndex: stats.length - i,
          }}>
            <div style={{ fontSize: 56, fontWeight: 400, lineHeight: 1 }}>{s.num}</div>
            <div style={{
              marginTop: 12, fontSize: 13, fontWeight: 400, letterSpacing: "0.06em",
              textTransform: "uppercase", maxWidth: 160,
            }}>{s.label}</div>
          </div>
        ))}
      </div>

      <Arrow variant="dark" />
    </section>
  );
}
