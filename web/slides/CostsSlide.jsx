// CostsSlide — dark shell with overlapping small circles + fee table.
// Bg #393939, inverse logo/arrow, rule in rgba(255,255,255,.5).

import React from "react";
import { Logo, Arrow, Tag, Shell } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function CostsSlide({
  tag = "Investment",
  statement = "One fee. Every moment.",
  rows = [
    { label: "Sense + Shape", amount: "€ 24,000" },
    { label: "Stress",        amount: "€ 18,000" },
    { label: "Ship",          amount: "€ 12,000" },
  ],
  total = { label: "Total", amount: "€ 54,000" },
  circleColors = ["#E05820", "#CBDC3A", "#BE40BE", "#4A7FC8"],
}) {
  const size = 120;
  const overlap = -20;

  return (
    <section className="slide">
      <Shell tone="dark">
        <Logo variant="light" position="inside" />

        <div style={{ position: "absolute", top: 52, left: 72 }}>
          <Tag tone="inv">{tag}</Tag>
        </div>

        <div style={{
          position: "absolute", top: 160, left: 72, width: 820,
          fontFamily: font, color: "#FFFFFF",
        }}>
          <h2 style={{
            margin: 0, fontSize: 62, fontWeight: 300,
            lineHeight: 1.05, letterSpacing: "-0.015em",
          }}>{statement}</h2>
          <div style={{ marginTop: 60, display: "flex" }}>
            {circleColors.map((c, i) => (
              <div key={i} style={{
                width: size, height: size, borderRadius: "50%", background: c,
                marginLeft: i === 0 ? 0 : overlap,
              }} />
            ))}
          </div>
        </div>

        <div style={{
          position: "absolute", top: 160, right: 72, width: 820,
          fontFamily: font, color: "#FFFFFF",
        }}>
          {rows.map((r, i) => (
            <div key={i} style={{
              display: "flex", justifyContent: "space-between", alignItems: "baseline",
              padding: "28px 0", borderTop: i === 0 ? "1px solid rgba(255,255,255,0.5)" : "none",
              borderBottom: "1px solid rgba(255,255,255,0.5)",
            }}>
              <span style={{ fontSize: 23, fontWeight: 400 }}>{r.label}</span>
              <span style={{ fontSize: 23, fontWeight: 700 }}>{r.amount}</span>
            </div>
          ))}
          <div style={{
            display: "flex", justifyContent: "space-between", alignItems: "baseline",
            paddingTop: 40,
          }}>
            <span style={{
              fontSize: 12, fontWeight: 400, letterSpacing: "0.08em",
              textTransform: "uppercase", opacity: 0.7,
            }}>{total.label}</span>
            <span style={{ fontSize: 48, fontWeight: 300, letterSpacing: "-0.01em" }}>
              {total.amount}
            </span>
          </div>
        </div>

        <Arrow variant="light" />
      </Shell>
    </section>
  );
}
