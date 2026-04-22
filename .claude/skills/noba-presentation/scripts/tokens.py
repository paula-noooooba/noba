"""Token bridge.

Loads design/tokens.json and exposes it as Python objects usable by
scripts/build_deck.py. All raw hex and pixel math is confined here so
slide builders can stay semantic (C.accent_pink, S.block, T.display()).

Update design/tokens.json — never edit values here.
"""
from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor

REPO_ROOT = Path(__file__).resolve().parents[4]
TOKENS_PATH = REPO_ROOT / "design" / "tokens.json"
_RAW = json.loads(TOKENS_PATH.read_text())

EMU_PER_PX = 9525  # python-pptx standard at 96 DPI


def px_to_emu(px: float) -> int:
    return int(px * EMU_PER_PX)


def hex_to_rgb(value: str) -> RGBColor:
    h = value.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _flatten(prefix: str, group: dict) -> dict[str, RGBColor]:
    out = {}
    for k, v in group.items():
        key = f"{prefix}_{k}".replace("-", "_")
        if isinstance(v, str) and v.startswith("#"):
            out[key] = hex_to_rgb(v)
    return out


_colors = {}
_colors.update(_flatten("neutral", _RAW["color"]["neutral"]))
_colors.update(_flatten("accent", _RAW["color"]["accent"]))
C = SimpleNamespace(**_colors)

_spacing = {k.replace("-", "_"): px_to_emu(v) for k, v in _RAW["spacing"].items()}
_shape = {k.replace("-", "_"): (px_to_emu(v) if v >= 0 else -px_to_emu(-v)) for k, v in _RAW["shape"].items()}
S = SimpleNamespace(**_spacing, **_shape)


class T:
    """Typography accessor. Each classmethod returns {size: Pt, weight, leading, tracking, uppercase}."""

    @staticmethod
    def _scale(name: str) -> dict:
        s = _RAW["typography"]["scale"][name]
        return {
            "size": Pt(s["size"] * 0.75),
            "size_px": s["size"],
            "weight": s["weight"],
            "leading": s["leading"],
            "tracking": s.get("tracking", 0),
            "uppercase": s.get("uppercase", False),
        }

    hero        = staticmethod(lambda: T._scale("hero"))
    display     = staticmethod(lambda: T._scale("display"))
    headline    = staticmethod(lambda: T._scale("headline"))
    title       = staticmethod(lambda: T._scale("title"))
    stat_number = staticmethod(lambda: T._scale("stat-number"))
    lead        = staticmethod(lambda: T._scale("lead"))
    body        = staticmethod(lambda: T._scale("body"))
    body_sm     = staticmethod(lambda: T._scale("body-sm"))
    caption     = staticmethod(lambda: T._scale("caption"))
    label       = staticmethod(lambda: T._scale("label"))
    micro       = staticmethod(lambda: T._scale("micro"))

    family = _RAW["typography"]["family"].split(",")[0].strip().strip("'\"")


class SLIDE:
    width_px = _RAW["slide"]["width"]
    height_px = _RAW["slide"]["height"]
    width = px_to_emu(width_px)
    height = px_to_emu(height_px)
