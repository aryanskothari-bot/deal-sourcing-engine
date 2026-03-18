"""
screener.py — Universe Screener logic.
Applies sidebar filters to the raw universe DataFrame.
"""

import pandas as pd
from typing import Optional


def apply_filters(
    df: pd.DataFrame,
    sector: str = "All Sectors",
    mktcap_range: tuple = (0, 200),
    ev_range: tuple = (0, 300),
    revenue_min: float = 0,
    ebitda_margin_min: float = -50,
    nd_ebitda_max: float = 10,
    ev_ebitda_max: float = 30,
    rev_growth_min: float = -50,
) -> pd.DataFrame:
    """
    Filter the universe DataFrame by user-defined criteria.
    Returns filtered DataFrame, preserving all columns.
    """
    out = df.copy()

    # Sector
    if sector and sector != "All Sectors":
        out = out[out["Sector"] == sector]

    # Market cap
    if "Mkt Cap (€bn)" in out.columns:
        out = out[
            (out["Mkt Cap (€bn)"].fillna(0) >= mktcap_range[0]) &
            (out["Mkt Cap (€bn)"].fillna(0) <= mktcap_range[1])
        ]

    # EV
    if "EV (€bn)" in out.columns:
        out = out[
            (out["EV (€bn)"].fillna(0) >= ev_range[0]) &
            (out["EV (€bn)"].fillna(0) <= ev_range[1])
        ]

    # Revenue minimum
    if "Revenue (€mn)" in out.columns:
        out = out[out["Revenue (€mn)"].fillna(0) >= revenue_min]

    # EBITDA margin floor
    if "EBITDA Margin %" in out.columns:
        out = out[out["EBITDA Margin %"].fillna(-999) >= ebitda_margin_min]

    # ND/EBITDA ceiling
    if "ND/EBITDA" in out.columns:
        out = out[out["ND/EBITDA"].fillna(0) <= nd_ebitda_max]

    # EV/EBITDA ceiling
    if "EV/EBITDA" in out.columns:
        out = out[out["EV/EBITDA"].fillna(99) <= ev_ebitda_max]

    # Revenue growth floor
    if "Rev Growth %" in out.columns:
        out = out[out["Rev Growth %"].fillna(-999) >= rev_growth_min]

    return out.reset_index(drop=True)


def get_benchmark_badges(df: pd.DataFrame, col: str) -> pd.Series:
    """
    Return a Series of labels: 'Above Median', 'Below Median', 'Top Quartile'.
    Useful for decorating screener table cells.
    """
    median = df[col].median()
    q75    = df[col].quantile(0.75)

    def label(v):
        if pd.isna(v):
            return "N/A"
        if v >= q75:
            return "Top Quartile"
        if v >= median:
            return "Above Median"
        return "Below Median"

    return df[col].apply(label)


def summary_stats(df: pd.DataFrame) -> dict:
    """Return summary statistics for the filtered universe."""
    if df.empty:
        return {}
    return {
        "count":           len(df),
        "median_mktcap":   df["Mkt Cap (€bn)"].median(),
        "median_ev_ebitda": df["EV/EBITDA"].median(),
        "median_margin":   df["EBITDA Margin %"].median(),
        "median_growth":   df["Rev Growth %"].median(),
        "avg_score":       df["Score"].mean() if "Score" in df.columns else None,
    }
