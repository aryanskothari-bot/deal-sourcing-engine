"""
pages/1_🏠_Home.py — Deal Sourcing Engine Home Page.
Overview dashboard: universe summary, top targets, quick nav.
"""

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row, score_bar, pill
from data_sources.yfinance_loader import fetch_universe
from data_sources.static_loader import get_static_df
from modules.screener import summary_stats
from modules.ranker import score_universe
from utils.charts import score_bars, scatter_valuation

st.set_page_config(
    page_title="Engine — Home",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ─── HEADER ──────────────────────────────────────────────────────────────────
page_header(
    title="Deal Sourcing & Preliminary <em>Diligence Engine</em>",
    subtitle="European M&A · Phase 1 — Euronext Paris / SBF 120",
    badge="Phase 1 · Live",
)

# ─── LOAD & SCORE ─────────────────────────────────────────────────────────────
with st.spinner("Loading universe…"):
    try:
        raw = fetch_universe()
    except Exception:
        raw = get_static_df()

df = score_universe(raw)

# ─── SUMMARY METRICS ──────────────────────────────────────────────────────────
stats = summary_stats(df)
top1 = df.iloc[0] if len(df) > 0 else None

metric_row([
    {"val": str(stats.get("count", "—")),              "lbl": "Companies in Universe"},
    {"val": f"{stats.get('avg_score', 0):.0f} / 100",  "lbl": "Avg Acquisition Score", "cls": "gold"},
    {"val": f"€{stats.get('median_mktcap', 0):.1f}bn", "lbl": "Median Market Cap"},
    {"val": f"{stats.get('median_ev_ebitda', 0):.1f}×","lbl": "Median EV/EBITDA"},
    {"val": f"{stats.get('median_margin', 0):.1f}%",   "lbl": "Median EBITDA Margin"},
])

# ─── TOP TARGET CALLOUT ───────────────────────────────────────────────────────
if top1 is not None:
    st.markdown("---")
    sec_label("Top Acquisition Target")
    c1, c2, c3 = st.columns([2, 2, 3])
    with c1:
        st.markdown(f"""
        <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08)">
            <div style="font-family:var(--mono);font-size:8px;letter-spacing:.25em;text-transform:uppercase;color:var(--gold);margin-bottom:6px">#{1} Ranked Target</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:600;color:var(--ink);margin-bottom:2px">{top1['Company']}</div>
            <div style="font-family:var(--mono);font-size:9px;color:var(--muted);letter-spacing:.1em">{top1['Ticker']} · {top1['Sector']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        score_bar("Composite Score",       top1.get("Score", 0))
        score_bar("Profitability",         top1.get("score_profitability", 0))
        score_bar("Valuation",             top1.get("score_valuation", 0))
        score_bar("Leverage",              top1.get("score_leverage", 0))
    with c3:
        pills_html = (
            pill(f"EV/EBITDA {top1.get('EV/EBITDA','—')}×", "gold") +
            pill(f"Margin {top1.get('EBITDA Margin %','—')}%", "green") +
            pill(f"ND/EBITDA {top1.get('ND/EBITDA','—')}×", "muted") +
            pill(top1["Sector"], "muted")
        )
        st.markdown(f"""
        <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08);height:100%">
            <div style="font-family:var(--mono);font-size:8px;letter-spacing:.25em;text-transform:uppercase;color:var(--faint);margin-bottom:12px">Key Metrics</div>
            {pills_html}
            <div style="margin-top:14px;font-family:var(--sans);font-size:13px;color:var(--muted);line-height:1.7">
                Mkt Cap <b style="color:var(--ink)">€{top1.get("Mkt Cap (€bn)","—")}bn</b> · 
                EV <b style="color:var(--ink)">€{top1.get("EV (€bn)","—")}bn</b> · 
                Revenue <b style="color:var(--ink)">€{top1.get("Revenue (€mn)",0)/1000:.1f}bn</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ─── SCORE LEAGUE TABLE CHART ─────────────────────────────────────────────────
sec_label("Top 10 Targets by Composite Score")
st.plotly_chart(score_bars(df, top_n=10), use_container_width=True)

st.markdown("---")

# ─── VALUATION SCATTER ────────────────────────────────────────────────────────
sec_label("Valuation vs Profitability — Universe Map")
st.plotly_chart(scatter_valuation(df), use_container_width=True)

st.markdown("---")

# ─── QUICK NAV ────────────────────────────────────────────────────────────────
sec_label("Navigate the Engine")
cols = st.columns(5)
pages = [
    ("🔍", "Universe Screener",     "Filter the SBF 120 by sector, size, multiples, and margins."),
    ("🎯", "Target Ranker",         "8-pillar transparent scoring — 0 to 100 per company."),
    ("📊", "Financial Statements",  "Standardised IS / BS / CF with 5-year history and ratios."),
    ("🔬", "Diligence View",        "QoE, adjusted EBITDA, WC, net debt, red flag panel."),
    ("📋", "Shortlist",             "Ranked export-ready shortlist with Excel download."),
]
for col, (icon, title, desc) in zip(cols, pages):
    with col:
        st.markdown(f"""
        <div style="background:var(--paper2);padding:18px 16px;border:1px solid rgba(16,14,12,.07);border-top:2px solid var(--gold);height:100%">
            <div style="font-size:22px;margin-bottom:8px">{icon}</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:15px;font-weight:600;color:var(--ink);margin-bottom:6px">{title}</div>
            <div style="font-family:var(--sans);font-size:11.5px;color:var(--muted);line-height:1.55">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.15em;color:var(--faint);text-align:center;padding-top:24px;border-top:1px solid rgba(16,14,12,.07);text-transform:uppercase">
    Deal Sourcing &amp; Preliminary Diligence Engine · Aryan S. Kothari · SKEMA Paris 2025 · For demonstration purposes only — not investment advice
</div>
""", unsafe_allow_html=True)
