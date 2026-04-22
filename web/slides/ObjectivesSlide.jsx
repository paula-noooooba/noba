// ObjectivesSlide — 2-col: statement + numbered borderline list.
// Left: big headline in accent color. Right: 3–5 numbered rows divided by 1px rules.

import React from "react";
import { Logo, Arrow, Tag } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function ObjectivesSlide({
  tag = "Objectives",
  statement = "Decide, fast, on the direction that wins.",
  accent = "#E05820",
  items = [
    { title: "Clarify demand", body: "Which of the three directions resonates most." },
    { title: "Validate claims", body: "Which product claims carry real weight." },
    { title: "Shape the pitch", body: "The story that converts buyer to believer." },
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
      }}>
        {statement}
      </h2>

      <div style={{
        position: "absolute", top: 208, right: 72, width: 820,
        fontFamily: font, color: "#1A1A1A",
      }}>
        {items.map((it, i) => (
          <div key={i} style={{
            padding: "28px 0",
            borderTop: i === 0 ? "1px solid #DCDCDC" : "none",
            borderBottom: "1px solid #DCDCDC",
            display: "grid", gridTemplateColumns: "80px 1fr", alignItems: "baseline",
          }}>
            <div style={{
              fontSize: 12, fontWeight: 400, letterSpacing: "0.08em",
              textTransform: "uppercase", opacity: 0.5,
            }}>{String(i + 1).padStart(2, "0")}</div>
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
