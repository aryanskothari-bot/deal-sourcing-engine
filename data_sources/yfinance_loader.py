"""
yfinance_loader.py — Fetch live financial data from Yahoo Finance.
Falls back to static_loader if data is unavailable / rate-limited.
"""

import pandas as pd
import numpy as np
import streamlit as st
from typing import Optional

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False

from data_sources.static_loader import get_static_df, STATIC_COMPANIES, get_static_financials
from config import SBF120_TICKERS, TICKER_SECTOR_MAP


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_universe() -> pd.DataFrame:
    """
    Fetch market data for the full SBF 120 sample.
    Returns a DataFrame with key screening metrics.
    Falls back to static data if yfinance unavailable.
    """
    if not YF_AVAILABLE:
        return _enrich_static()

    rows = []
    for name, ticker in SBF120_TICKERS.items():
        try:
            info = yf.Ticker(ticker).info
            if not info or info.get("regularMarketPrice") is None:
                continue

            mktcap   = (info.get("marketCap") or 0) / 1e9
            ev       = (info.get("enterpriseValue") or 0) / 1e9
            revenue  = (info.get("totalRevenue") or 0) / 1e6
            ebitda   = (info.get("ebitda") or 0) / 1e6
            net_debt = ((info.get("totalDebt") or 0) - (info.get("totalCash") or 0)) / 1e6

            ebitda_margin = (ebitda / revenue * 100) if revenue > 0 else None
            nd_ebitda     = (net_debt / ebitda) if ebitda > 0 else None
            ev_ebitda     = (ev * 1000 / ebitda) if ebitda > 0 else None
            ev_revenue    = (ev * 1000 / revenue) if revenue > 0 else None
            rev_growth    = (info.get("revenueGrowth") or 0) * 100

            rows.append({
                "Company":          name,
                "Ticker":           ticker,
                "Sector":           TICKER_SECTOR_MAP.get(ticker, "Other"),
                "Country":          "France",
                "Mkt Cap (€bn)":    round(mktcap, 2),
                "EV (€bn)":         round(ev, 2),
                "Revenue (€mn)":    round(revenue),
                "EBITDA (€mn)":     round(ebitda),
                "EBITDA Margin %":  round(ebitda_margin, 1) if ebitda_margin else None,
                "Rev Growth %":     round(rev_growth, 1),
                "Net Debt (€mn)":   round(net_debt),
                "ND/EBITDA":        round(nd_ebitda, 2) if nd_ebitda else None,
                "EV/EBITDA":        round(ev_ebitda, 1) if ev_ebitda else None,
                "EV/Revenue":       round(ev_revenue, 2) if ev_revenue else None,
                "NTM P/E":          info.get("forwardPE"),
                "ROE %":            round((info.get("returnOnEquity") or 0) * 100, 1),
                "ROIC %":           None,
                "Current Ratio":    info.get("currentRatio"),
                "Score":            None,   # filled by ranker
            })
        except Exception:
            continue

    if not rows:
        return _enrich_static()

    df = pd.DataFrame(rows)
    return df


def _enrich_static() -> pd.DataFrame:
    """Return static dataset with sector from map."""
    df = get_static_df()
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_financials(ticker: str) -> Optional[dict]:
    """
    Fetch 5-year historical income statement for a single ticker.
    Returns dict with lists: years, revenue, ebitda, ebit, net_income, margins.
    """
    if not YF_AVAILABLE:
        return get_static_financials(ticker)

    try:
        t = yf.Ticker(ticker)
        is_annual = t.financials

        if is_annual is None or is_annual.empty:
            return get_static_financials(ticker)

        # Transpose so rows = years
        df = is_annual.T.sort_index()
        df.index = pd.to_datetime(df.index)
        df = df.tail(5)

        years      = df.index.year.tolist()
        revenue    = _safe_col(df, ["Total Revenue"])
        ebitda_raw = _safe_col(df, ["EBITDA"])
        ebit       = _safe_col(df, ["EBIT", "Operating Income"])
        net_income = _safe_col(df, ["Net Income"])

        # Compute margins
        em = [round(e / r * 100, 1) if r and r != 0 else None for e, r in zip(ebitda_raw, revenue)]
        im = [round(e / r * 100, 1) if r and r != 0 else None for e, r in zip(ebit, revenue)]

        return {
            "years":         years,
            "revenue":       [int(v / 1e6) if v else 0 for v in revenue],
            "ebitda":        [int(v / 1e6) if v else 0 for v in ebitda_raw],
            "ebit":          [int(v / 1e6) if v else 0 for v in ebit],
            "net_income":    [int(v / 1e6) if v else 0 for v in net_income],
            "ebitda_margin": em,
            "ebit_margin":   im,
        }
    except Exception:
        return get_static_financials(ticker)


def _safe_col(df: pd.DataFrame, candidates: list) -> list:
    for col in candidates:
        if col in df.columns:
            return df[col].fillna(0).tolist()
    return [0] * len(df)
