// DarkSlide — dark outro. Big display headline in light text on #393939.
// Used for NOBA way divider and closing slide.

import React from "react";
import { Logo, Arrow, Shell } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function DarkSlide({
  eyebrow = "The NOBA way",
  headline = "Move decisively. Test early. Ship the story.",
  footnote = "",
}) {
  return (
    <section className="slide">
      <Shell tone="dark">
        <Logo variant="light" position="inside" />

        <div style={{
          position: "absolute", top: 52, left: 72, right: 72, bottom: 120,
          fontFamily: font, color: "#FFFFFF",
          display: "flex", flexDirection: "column", justifyContent: "center",
        }}>
          {eyebrow && (
            <div style={{
              fontSize: 12, fontWeight: 400, letterSpacing: "0.08em",
              textTransform: "uppercase", opacity: 0.7, marginBottom: 40,
            }}>{eyebrow}</div>
          )}
          <h2 style={{
            margin: 0, fontSize: 80, fontWeight: 300,
            lineHeight: 1.05, letterSpacing: "-0.015em", maxWidth: 1400,
          }}>
            {headline}
          </h2>
          {footnote && (
            <div style={{
              marginTop: 60, fontSize: 17, lineHeight: 1.62, maxWidth: 900,
              opacity: 0.85,
            }}>{footnote}</div>
          )}
        </div>

        <Arrow variant="light" />
      </Shell>
    </section>
  );
}
