"""
pages/1_🏠_Home.py — Deal Sourcing Engine Home Page.
Overview dashboard: universe summary, top targets, quick nav.
"""

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row, score_bar, pill, nav_bar
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

nav_bar("Home")

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
