// ContextSlide — the project-context layout.
//
// Figma source of truth: qqNtw4M8gc3zYRHwKJae7W, node 1:230
// https://www.figma.com/design/qqNtw4M8gc3zYRHwKJae7W/NOBA-PPT-Design-System?node-id=1-230
//
// Anatomy:
// - Full-bleed white background, 48 px padding (24 at Figma 960 → 48 at
//   slide scale).
// - A photo is pinned flush to the right edge, full slide height, 768
//   px wide, rounded on its left corners only.
// - Top row: inline arrow + uppercase "CONTEXT" label on the left,
//   smaller NOBA wordmark (228×30) on the right.
// - Body: a single long rich-text block with multiple paragraphs and
//   bold emphasis inside paragraphs. 456 px (Figma) / 912 px (slide)
//   max width, 14/20 px body type at Figma scale.
//
// No big headline, no pill tag, no lead paragraph — this layout leans
// into dense copy + imagery.

import React from "react";
import { Logo, Arrow } from "../atoms/atoms.jsx";

const font = "'Helvetica Neue', Helvetica, Arial, sans-serif";

function RichParagraph({ runs }) {
  return (
    <p style={{ margin: 0, marginBottom: 16 }}>
      {runs.map((run, i) => (
        <span key={i} style={{ fontWeight: run.bold ? 700 : 400 }}>
          {run.text}
        </span>
      ))}
    </p>
  );
}

export default function ContextSlide({
  tag = "CONTEXT",
  image = "../assets/photos/placeholder.jpg",
  body = [
    [
      { text: "Lavazza aims to expand its vending presence by crafting a distinctive coffee experience that resonates with consumers, aligns with market trends, and reflects the brand’s heritage. ", bold: true },
      { text: "The goal is to elevate the vending experience through meaningful innovation—enhancing relevance and memorability without altering the core product portfolio." },
    ],
    [
      { text: "BEYOND SIMPLE TRANSACTIONS\n", bold: true },
      { text: "Vending is evolving across industries. From TOUS jewelry machines to Selfridges champagne lockers, new models are turning functional moments into emotional ones." },
    ],
    [
      { text: "Lavazza has the opportunity to tap into this momentum by reimagining vending—" },
      { text: "not just as a point of sale, but as a platform for brand storytelling and elevated coffee rituals.", bold: true },
      { text: " Whether through souvenir-ready vacuum-packed blends or premium on-the-go brewing, the ambition is to deliver memorable experiences that celebrate Lavazza’s quality and authenticity." },
    ],
  ],
}) {
  return (
    <section className="slide" style={{
      background: "#FFFFFF", position: "relative",
      width: 1920, height: 1080,
      overflow: "hidden",
    }}>
      {/* Photo pinned right, rounded left corners only */}
      <img src={image} alt=""
           style={{
             position: "absolute", top: 0, right: 0,
             width: 768, height: 1080, objectFit: "cover",
             borderTopLeftRadius: 32, borderBottomLeftRadius: 32,
           }} />

      {/* Top row — arrow + tag on left, logo on right */}
      <div style={{
        position: "absolute", top: 48, left: 48, right: 48,
        display: "flex", alignItems: "center", justifyContent: "space-between",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <Arrow variant="dark" width={36} height={35} />
          <span style={{
            fontFamily: font, fontWeight: 400, fontSize: 26,
            letterSpacing: "1.76px", textTransform: "uppercase",
            color: "#1A1A1A",
          }}>
            {tag}
          </span>
        </div>
        <Logo variant="dark" position="inside" width={228} height={30} />
      </div>

      {/* Body rich text */}
      <div style={{
        position: "absolute", top: 160, left: 48, width: 912,
        fontFamily: font, fontSize: 28, lineHeight: 1.43,
        color: "#1A1A1A",
      }}>
        {body.map((runs, i) => <RichParagraph key={i} runs={runs} />)}
      </div>
    </section>
  );
}
