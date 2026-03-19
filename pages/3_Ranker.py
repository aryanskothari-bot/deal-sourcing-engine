"""
pages/3_🎯_Ranker.py — Acquisition Target Ranker.
8-pillar transparent scoring with radar chart and league table.
"""

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row, score_bar, nav_bar
from data_sources.yfinance_loader import fetch_universe
from data_sources.static_loader import get_static_df
from modules.ranker import score_universe, get_pillar_scores, SCORING_PILLARS
from utils.charts import radar_chart, score_bars

st.set_page_config(page_title="Target Ranker", page_icon="🎯", layout="wide")
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

nav_bar("Ranker")

page_header("Acquisition Target <em>Ranker</em>", "8-Pillar transparent scoring — 0 to 100 per company")

# ─── LOAD & SCORE ─────────────────────────────────────────────────────────────
with st.spinner("Scoring universe…"):
    try:
        raw = fetch_universe()
    except Exception:
        raw = get_static_df()
df = score_universe(raw)

# ─── PILLAR WEIGHTS EXPLAINER ─────────────────────────────────────────────────
with st.expander("📐 Scoring Methodology — 8 Pillars & Weights"):
    cols = st.columns(4)
    for i, (pillar, weight) in enumerate(SCORING_PILLARS.items()):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:var(--paper2);padding:12px 14px;border:1px solid rgba(16,14,12,.07);margin-bottom:8px">
                <div style="font-family:var(--mono);font-size:8px;letter-spacing:.15em;text-transform:uppercase;color:var(--gold);margin-bottom:3px">{int(weight*100)}% weight</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:14px;font-weight:600;color:var(--ink)">{pillar}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ─── LEAGUE TABLE ─────────────────────────────────────────────────────────────
sec_label("Ranked Universe — All Companies")
st.plotly_chart(score_bars(df, top_n=min(12, len(df))), use_container_width=True)

st.markdown("---")

# ─── SINGLE COMPANY DEEP DIVE ─────────────────────────────────────────────────
sec_label("Company Deep Dive — Pillar Breakdown")

companies = df["Company"].tolist()
selected = st.selectbox("Select a company", companies, index=0)

row = df[df["Company"] == selected].iloc[0]
pillars = get_pillar_scores(row)

c1, c2 = st.columns([1, 1])

with c1:
    # Score bars for all pillars
    st.markdown(f"""
    <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08);margin-bottom:16px">
        <div style="font-family:var(--mono);font-size:8px;letter-spacing:.25em;text-transform:uppercase;color:var(--faint);margin-bottom:8px">Composite Score</div>
        <div style="font-family:'Cormorant Garamond',serif;font-size:52px;font-weight:500;color:var(--gold);line-height:1">{row['Score']:.0f}</div>
        <div style="font-family:var(--mono);font-size:9px;color:var(--muted);letter-spacing:.1em;margin-top:4px">out of 100</div>
    </div>
    """, unsafe_allow_html=True)

    for pillar, score in pillars.items():
        score_bar(pillar, score)

with c2:
    st.plotly_chart(radar_chart(pillars, selected), use_container_width=True)

# ─── KEY METRICS TABLE ────────────────────────────────────────────────────────
st.markdown("---")
sec_label(f"{selected} — Key Financial Metrics")

metric_row([
    {"val": f"€{row.get('Mkt Cap (€bn)', 0):.1f}bn",    "lbl": "Market Cap"},
    {"val": f"€{row.get('EV (€bn)', 0):.1f}bn",         "lbl": "Enterprise Value"},
    {"val": f"{row.get('EBITDA Margin %', 0):.1f}%",    "lbl": "EBITDA Margin", "cls": "gold"},
    {"val": f"{row.get('ND/EBITDA', 0):.2f}×",          "lbl": "ND/EBITDA"},
    {"val": f"{row.get('EV/EBITDA', 0):.1f}×",          "lbl": "EV/EBITDA"},
])

# ─── FULL RANKING TABLE ───────────────────────────────────────────────────────
st.markdown("---")
sec_label("Full Ranked Table")

RANK_COLS = ["Company", "Sector", "Score",
             "score_growth", "score_profitability", "score_valuation",
             "score_leverage", "score_balance_sheet"]
show = [c for c in RANK_COLS if c in df.columns]

styler = (
    df[show].head(20)
    .style
    .format({c: "{:.0f}" for c in show if c.startswith("score_")}, na_rep="N/A")
    .format({"Score": "{:.0f}"})
    .background_gradient(subset=["Score"], cmap="YlOrBr")
)
st.dataframe(styler, use_container_width=True, height=460)
