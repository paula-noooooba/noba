// TitleSlide — cover slide.
// Anatomy: paper shell, hero headline in accent color, Logo top-right (cover),
// client/date caption bottom-left, Arrow bottom-right.

import React from "react";
import { Logo, Arrow, Shell } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function TitleSlide({
  eyebrow = "Commercial proposal",
  title = "Next-gen innovation",
  accent = "#BE40BE",
  client = "Client name",
  date = "April 2026",
}) {
  return (
    <section className="slide">
      <Shell>
        <Logo variant="dark" position="cover" />

        <div style={{
          position: "absolute", left: 72, top: 360, right: 72,
          fontFamily: font,
        }}>
          <div style={{
            fontSize: 12, fontWeight: 400, letterSpacing: "0.08em",
            textTransform: "uppercase", color: "#1A1A1A", marginBottom: 40,
          }}>
            {eyebrow}
          </div>
          <h1 style={{
            margin: 0, fontSize: 96, fontWeight: 300,
            lineHeight: 1.05, letterSpacing: "-0.02em", color: accent,
          }}>
            {title}
          </h1>
        </div>

        <div style={{
          position: "absolute", left: 72, bottom: 72,
          fontFamily: font, fontSize: 13, color: "#1A1A1A",
        }}>
          <div style={{ fontWeight: 700 }}>{client}</div>
          <div style={{ opacity: 0.6, marginTop: 4 }}>{date}</div>
        </div>

        <Arrow variant="dark" />
      </Shell>
    </section>
  );
}
