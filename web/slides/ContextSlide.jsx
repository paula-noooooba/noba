// ContextSlide — 58/42 split: prose column + photo column.
// Anatomy: section tag top-left, headline, lead paragraph, optional body;
// right 42% is a photo/image placeholder. Logo inside, Arrow bottom-right.

import React from "react";
import { Logo, Arrow, Tag } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

export default function ContextSlide({
  tag = "Context",
  headline = "A single moment of truth",
  lead = "Brief, outcome-oriented framing of the client's situation.",
  body = "Two or three concrete supporting sentences. No hedging, no jargon.",
  image = null,
}) {
  return (
    <section className="slide" style={{ background: "#FFFFFF" }}>
      <Logo variant="dark" position="inside" />

      <div style={{ position: "absolute", top: 60, left: 72 }}>
        <Tag>{tag}</Tag>
      </div>

      <div style={{
        position: "absolute", top: 192, left: 72, width: 1022,
        fontFamily: font, color: "#1A1A1A",
      }}>
        <h2 style={{
          margin: 0, fontSize: 62, fontWeight: 300,
          lineHeight: 1.05, letterSpacing: "-0.015em",
        }}>
          {headline}
        </h2>
        <p style={{
          marginTop: 40, fontSize: 23, fontWeight: 400, lineHeight: 1.4,
        }}>
          {lead}
        </p>
        <p style={{
          marginTop: 28, fontSize: 17, fontWeight: 400, lineHeight: 1.62,
          opacity: 0.75,
        }}>
          {body}
        </p>
      </div>

      <div style={{
        position: "absolute", top: 60, right: 60, bottom: 60, width: 706,
        borderRadius: 24, background: "#F0F0F0", overflow: "hidden",
      }}>
        {image && (
          <img src={image} alt="" style={{
            width: "100%", height: "100%", objectFit: "cover", display: "block",
          }} />
        )}
      </div>

      <Arrow variant="dark" />
    </section>
  );
}
