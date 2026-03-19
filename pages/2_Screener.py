"""
pages/2_🔍_Screener.py — Universe Screener.
Filter the SBF 120 universe by sector, size, multiples, and margins.
"""

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row, nav_bar
from data_sources.yfinance_loader import fetch_universe
from data_sources.static_loader import get_static_df
from modules.screener import apply_filters, summary_stats
from modules.ranker import score_universe
from utils.charts import scatter_valuation
from config import SECTORS, SCREENER_DEFAULTS

st.set_page_config(page_title="Screener", page_icon="🔍", layout="wide")
inject_css()

# ─── TOP NAV BAR (works in embed mode — no sidebar needed) ───────────────────
_nav_cols = st.columns(7)
_nav_pages = [
    ("pages/1_Home.py",       "Home"),
    ("pages/2_Screener.py",   "Screener"),
    ("pages/3_Ranker.py",     "Ranker"),
    ("pages/4_Financials.py", "Financials"),
    ("pages/5_Shortlist.py",  "Shortlist"),
    ("pages/6_Diligence.py",  "Diligence"),
    ("pages/7_Signals.py",    "Signals"),
]
for _col, (_pg, _lbl) in zip(_nav_cols, _nav_pages):
    with _col:
        st.page_link(_pg, label=_lbl, use_container_width=True)
st.markdown("<hr style='margin:0 0 8px 0;border-color:rgba(155,111,41,.3)'>", unsafe_allow_html=True)
# ─────────────────────────────────────────────────────────────────────────────

nav_bar("Screener")

page_header("Universe <em>Screener</em>", "Filter the SBF 120 by sector, size, multiples &amp; margins")

# ─── LOAD ────────────────────────────────────────────────────────────────────
with st.spinner("Loading universe…"):
    try:
        raw = fetch_universe()
    except Exception:
        raw = get_static_df()
df_scored = score_universe(raw)

# ─── SIDEBAR FILTERS ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Screener Filters")

    sector = st.selectbox("Sector", SECTORS, index=0)

    st.markdown("**Market Cap (€bn)**")
    mktcap_range = st.slider("", 0.0, 100.0,
        (SCREENER_DEFAULTS["mktcap_min_bn"], SCREENER_DEFAULTS["mktcap_max_bn"]),
        step=0.5, key="mktcap", label_visibility="collapsed")

    st.markdown("**EV (€bn)**")
    ev_range = st.slider("", 0.0, 150.0,
        (SCREENER_DEFAULTS["ev_min_bn"], SCREENER_DEFAULTS["ev_max_bn"]),
        step=0.5, key="ev", label_visibility="collapsed")

    revenue_min = st.slider("Min Revenue (€mn)", 0, 5000,
        int(SCREENER_DEFAULTS["revenue_min_mn"]), step=50)

    ebitda_margin_min = st.slider("Min EBITDA Margin %", -20, 40,
        int(SCREENER_DEFAULTS["ebitda_margin_min"]), step=1)

    nd_ebitda_max = st.slider("Max ND/EBITDA", 0.0, 10.0,
        SCREENER_DEFAULTS["net_debt_ebitda_max"], step=0.5)

    ev_ebitda_max = st.slider("Max EV/EBITDA", 0.0, 30.0,
        SCREENER_DEFAULTS["ev_ebitda_max"], step=0.5)

    rev_growth_min = st.slider("Min Rev Growth %", -30, 30, -20, step=1)

    st.markdown("---")
    if st.button("Reset Filters"):
        st.rerun()

# ─── APPLY FILTERS ───────────────────────────────────────────────────────────
filtered = apply_filters(
    df_scored,
    sector=sector,
    mktcap_range=mktcap_range,
    ev_range=ev_range,
    revenue_min=revenue_min,
    ebitda_margin_min=ebitda_margin_min,
    nd_ebitda_max=nd_ebitda_max,
    ev_ebitda_max=ev_ebitda_max,
    rev_growth_min=rev_growth_min,
)

# ─── SUMMARY METRICS ─────────────────────────────────────────────────────────
stats = summary_stats(filtered)
all_stats = summary_stats(df_scored)

metric_row([
    {"val": f"{stats.get('count', 0)} / {all_stats.get('count', 0)}", "lbl": "Companies Passing Filters"},
    {"val": f"€{stats.get('median_mktcap', 0):.1f}bn",               "lbl": "Median Mkt Cap"},
    {"val": f"{stats.get('median_ev_ebitda', 0):.1f}×",              "lbl": "Median EV/EBITDA"},
    {"val": f"{stats.get('median_margin', 0):.1f}%",                 "lbl": "Median EBITDA Margin"},
    {"val": f"{stats.get('avg_score', 0):.0f}",                      "lbl": "Avg Score", "cls": "gold"},
])

# ─── RESULTS TABLE ────────────────────────────────────────────────────────────
st.markdown("---")
sec_label(f"Filtered Universe — {len(filtered)} Companies")

DISPLAY_COLS = [
    "Company", "Ticker", "Sector",
    "Mkt Cap (€bn)", "EV (€bn)", "Revenue (€mn)",
    "EBITDA Margin %", "Rev Growth %",
    "ND/EBITDA", "EV/EBITDA", "NTM P/E",
    "Score",
]
show_cols = [c for c in DISPLAY_COLS if c in filtered.columns]

if filtered.empty:
    st.warning("No companies match the current filters. Try relaxing your criteria.")
else:
    # Style the dataframe
    def style_score(val):
        if pd.isna(val): return ""
        if val >= 70: return "color: #1B4B2B; font-weight: 600"
        if val >= 50: return "color: #9B6F29"
        return "color: #8C1B1B"

    def style_growth(val):
        if pd.isna(val): return ""
        return "color: #1B4B2B" if val >= 0 else "color: #8C1B1B"

    styler = (
        filtered[show_cols]
        .style
        .format({
            "Mkt Cap (€bn)":  "€{:.1f}",
            "EV (€bn)":       "€{:.1f}",
            "Revenue (€mn)":  "€{:,.0f}",
            "EBITDA Margin %":"{:.1f}%",
            "Rev Growth %":   "{:+.1f}%",
            "ND/EBITDA":      "{:.2f}×",
            "EV/EBITDA":      "{:.1f}×",
            "NTM P/E":        "{:.1f}×",
            "Score":          "{:.0f}",
        }, na_rep="N/A")
        .applymap(style_score,  subset=["Score"])
        .applymap(style_growth, subset=["Rev Growth %"])
        .set_table_styles([
            {"selector": "thead th", "props": [
                ("background-color", "#100E0C"), ("color", "#F6F1E7"),
                ("font-family", "DM Mono"), ("font-size", "10px"),
                ("letter-spacing", "0.15em"), ("text-transform", "uppercase"),
                ("padding", "10px 14px"),
            ]},
            {"selector": "tbody td", "props": [("padding", "9px 14px"), ("font-size", "13px")]},
            {"selector": "tbody tr:hover td", "props": [("background-color", "#EEE7D7")]},
        ])
    )
    st.dataframe(styler, use_container_width=True, height=460)

# ─── SCATTER ─────────────────────────────────────────────────────────────────
st.markdown("---")
sec_label("Valuation vs Profitability Map")
if not filtered.empty:
    st.plotly_chart(scatter_valuation(filtered), use_container_width=True)
