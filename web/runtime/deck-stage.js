// <deck-stage> — web component runtime for NOBA HTML decks.
//
// Wraps slide markup, fits 1920x1080 stages into the viewport with
// letterboxing, adds keyboard nav (arrows / space / home / end),
// and ensures print snapshots one slide per page.
//
// Usage:
//   <deck-stage>
//     <section class="slide">…</section>
//     <section class="slide">…</section>
//   </deck-stage>

const STAGE_W = 1920;
const STAGE_H = 1080;

const css = `
  :host {
    display: block;
    background: #0A0A0A;
    overflow: hidden;
    height: 100vh;
    width: 100vw;
  }
  .viewport { width: 100%; height: 100%; display: grid; place-items: center; }
  .scaler   { width: ${STAGE_W}px; height: ${STAGE_H}px; position: relative;
              background: #FFFFFF; transform-origin: center center; }
  ::slotted(.slide) {
    position: absolute !important; inset: 0 !important;
    width: ${STAGE_W}px !important; height: ${STAGE_H}px !important;
    display: none;
  }
  ::slotted(.slide.active) { display: block; }

  @media print {
    :host { height: auto; }
    .viewport { display: block; }
    .scaler { transform: none !important; page-break-after: always; }
    ::slotted(.slide) { display: block !important; page-break-after: always; }
  }
`;

class DeckStage extends HTMLElement {
  constructor() {
    super();
    const root = this.attachShadow({ mode: "open" });
    root.innerHTML = `
      <style>${css}</style>
      <div class="viewport"><div class="scaler"><slot></slot></div></div>
    `;
    this.scaler = root.querySelector(".scaler");
    this.index  = 0;
  }

  connectedCallback() {
    this._onResize = () => this.fit();
    this._onKey    = (e) => this.key(e);
    window.addEventListener("resize", this._onResize);
    window.addEventListener("keydown", this._onKey);
    queueMicrotask(() => { this.show(0); this.fit(); });
  }

  disconnectedCallback() {
    window.removeEventListener("resize", this._onResize);
    window.removeEventListener("keydown", this._onKey);
  }

  slides() { return Array.from(this.children).filter(n => n.classList.contains("slide")); }

  show(i) {
    const s = this.slides();
    if (!s.length) return;
    this.index = (i + s.length) % s.length;
    s.forEach((n, k) => n.classList.toggle("active", k === this.index));
  }

  fit() {
    const { clientWidth: w, clientHeight: h } = this;
    const scale = Math.min(w / STAGE_W, h / STAGE_H);
    this.scaler.style.transform = `scale(${scale})`;
  }

  key(e) {
    if (e.key === "ArrowRight" || e.key === " ") this.show(this.index + 1);
    else if (e.key === "ArrowLeft")              this.show(this.index - 1);
    else if (e.key === "Home")                   this.show(0);
    else if (e.key === "End")                    this.show(this.slides().length - 1);
  }
}

customElements.define("deck-stage", DeckStage);
