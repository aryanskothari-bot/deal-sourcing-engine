"""
ranker.py — 8-Pillar Acquisition Target Ranking Engine.
Scores each company 0–100 across 8 dimensions and produces a composite score.
"""

import pandas as pd
import numpy as np
from config import SCORING_PILLARS


def _normalise(series: pd.Series, higher_is_better: bool = True) -> pd.Series:
    """Min-max normalise to 0–100. NaN → 50 (neutral)."""
    s = series.copy().astype(float)
    mn, mx = s.min(), s.max()
    if mx == mn:
        return pd.Series([50.0] * len(s), index=s.index)
    norm = (s - mn) / (mx - mn) * 100
    if not higher_is_better:
        norm = 100 - norm
    return norm.fillna(50)


def score_universe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply 8-pillar scoring to every company in df.
    Adds columns: score_<pillar>, Score (composite 0–100).
    Returns enriched DataFrame sorted by Score descending.
    """
    out = df.copy()

    # ── Pillar 1: Revenue Growth (higher = better) ────────────────────────────
    out["score_growth"] = _normalise(out["Rev Growth %"], higher_is_better=True)

    # ── Pillar 2: Profitability — EBITDA margin (higher = better) ─────────────
    out["score_profitability"] = _normalise(out["EBITDA Margin %"], higher_is_better=True)

    # ── Pillar 3: Balance Sheet Quality — Current Ratio (higher = better, cap 3) ──
    cr = out["Current Ratio"].clip(upper=3)
    out["score_balance_sheet"] = _normalise(cr, higher_is_better=True)

    # ── Pillar 4: Leverage — ND/EBITDA (lower = better) ──────────────────────
    # Cap at 8x to avoid outlier distortion
    nd = out["ND/EBITDA"].clip(lower=-2, upper=8)
    out["score_leverage"] = _normalise(nd, higher_is_better=False)

    # ── Pillar 5: Valuation Attractiveness — EV/EBITDA (lower = better) ──────
    ev_eb = out["EV/EBITDA"].clip(upper=25)
    out["score_valuation"] = _normalise(ev_eb, higher_is_better=False)

    # ── Pillar 6: Size Compatibility — mid-cap sweet spot ────────────────────
    # Ideal EV: €2bn–€15bn → penalise extremes
    ev_bn = out["EV (€bn)"].fillna(5)
    size_score = ev_bn.apply(_size_score)
    out["score_size"] = size_score

    # ── Pillar 7: Geographic Relevance — all France = full score for Phase 1 ─
    out["score_geography"] = 100.0  # Phase 1: all French → max

    # ── Pillar 8: Acquisition Fit — pre-computed heuristic ───────────────────
    if "acq_score" in out.columns:
        out["score_acq_fit"] = out["acq_score"].fillna(50).clip(0, 100)
    else:
        # Proxy: blend of valuation + leverage
        out["score_acq_fit"] = (out["score_valuation"] * 0.5 + out["score_leverage"] * 0.5)

    # ── Composite weighted score ──────────────────────────────────────────────
    weights = {
        "score_growth":        SCORING_PILLARS["Revenue Growth"],
        "score_profitability": SCORING_PILLARS["Profitability"],
        "score_balance_sheet": SCORING_PILLARS["Balance Sheet Quality"],
        "score_leverage":      SCORING_PILLARS["Leverage"],
        "score_valuation":     SCORING_PILLARS["Valuation Attractiveness"],
        "score_size":          SCORING_PILLARS["Size Compatibility"],
        "score_geography":     SCORING_PILLARS["Geographic Relevance"],
        "score_acq_fit":       SCORING_PILLARS["Acquisition Fit"],
    }

    out["Score"] = sum(out[col] * w for col, w in weights.items())
    out["Score"] = out["Score"].round(1)

    return out.sort_values("Score", ascending=False).reset_index(drop=True)


def _size_score(ev_bn: float) -> float:
    """
    Score size compatibility on a bell curve.
    Sweet spot: €2bn–€15bn EV. Penalise very small (<0.5bn) and very large (>40bn).
    """
    if ev_bn < 0.5:
        return 30.0
    if ev_bn < 2.0:
        return 50.0 + (ev_bn - 0.5) / 1.5 * 30
    if ev_bn <= 15.0:
        return 80.0 + (1 - abs(ev_bn - 7.5) / 7.5) * 20
    if ev_bn <= 30.0:
        return 80.0 - (ev_bn - 15) / 15 * 30
    if ev_bn <= 50.0:
        return 50.0 - (ev_bn - 30) / 20 * 20
    return 30.0


def get_pillar_scores(row: pd.Series) -> dict:
    """Extract the 8 pillar scores for a single company row into a named dict."""
    return {
        "Revenue Growth":           row.get("score_growth", 50),
        "Profitability":            row.get("score_profitability", 50),
        "Balance Sheet Quality":    row.get("score_balance_sheet", 50),
        "Leverage":                 row.get("score_leverage", 50),
        "Valuation Attractiveness": row.get("score_valuation", 50),
        "Size Compatibility":       row.get("score_size", 50),
        "Geographic Relevance":     row.get("score_geography", 50),
        "Acquisition Fit":          row.get("score_acq_fit", 50),
    }
