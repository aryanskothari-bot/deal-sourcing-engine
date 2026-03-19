"""
pages/1_Home.py — Deal Sourcing Engine Home Page.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row
from data_sources.yfinance_loader import fetch_universe
from data_sources.static_loader import get_static_df
from modules.ranker import score_universe

st.set_page_config(page_title="Engine — Home", page_icon="⚙️", layout="wide", initial_sidebar_state="expanded")
inject_css()

# ─── NAV BAR ──────────────────────────────────────────────────────────────────
c1,c2,c3,c4,c5,c6,c7 = st.columns(7)
with c1: st.page_link("pages/1_Home.py",       label="🏠 Home",        use_container_width=True)
with c2: st.page_link("pages/2_Screener.py",   label="🔍 Screener",    use_container_width=True)
with c3: st.page_link("pages/3_Ranker.py",     label="🎯 Ranker",      use_container_width=True)
with c4: st.page_link("pages/4_Financials.py", label="📊 Financials",  use_container_width=True)
with c5: st.page_link("pages/5_Shortlist.py",  label="📋 Shortlist",   use_container_width=True)
with c6: st.page_link("pages/6_Diligence.py",  label="🔎 Diligence",   use_container_width=True)
with c7: st.page_link("pages/7_Signals.py",    label="📡 Signals",     use_container_width=True)
st.markdown("<hr style='margin:4px 0 16px 0;border-color:rgba(155,111,41,.25)'>", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
page_header("Deal Sourcing &amp; Preliminary <em>Diligence Engine</em>",
            "European M&amp;A · Phase 1 — Euronext Paris / SBF 120")

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
with st.spinner("Loading universe…"):
    try:
        raw = fetch_universe()
    except Exception:
        raw = get_static_df()
df = score_universe(raw)

# ─── METRICS ──────────────────────────────────────────────────────────────────
top = df.iloc[0] if len(df) > 0 else None
metric_row([
    {"val": str(len(df)),                                               "lbl": "Companies in Universe"},
    {"val": f"{df['Score'].mean():.0f} / 100",                         "lbl": "Avg Acquisition Score", "cls": "gold"},
    {"val": f"€{df['Mkt Cap (€bn)'].median():.1f}bn",                  "lbl": "Median Market Cap"},
    {"val": f"{df['EV/EBITDA'].median():.1f}×",                    "lbl": "Median EV/EBITDA"},
    {"val": f"{df['EBITDA Margin %'].median():.1f}%",                  "lbl": "Median EBITDA Margin"},
])

# ─── TOP TARGET ───────────────────────────────────────────────────────────────
if top is not None:
    st.markdown("---")
    sec_label("Top Acquisition Target — #1 Ranked")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown(f"""
        <div style="background:var(--ink);color:var(--paper);padding:20px 22px;border-top:2px solid var(--gold3)">
            <div style="font-family:var(--mono);font-size:8px;letter-spacing:.25em;color:var(--gold3);text-transform:uppercase;margin-bottom:6px">#1 Ranked Target</div>
            <div style="font-family:var(--serif);font-size:28px;font-weight:600">{top.get("Company","—")}</div>
            <div style="font-family:var(--mono);font-size:10px;color:rgba(246,241,231,.5);margin-top:4px">{top.get("Ticker","—")} · {top.get("Sector","—")}</div>
        </div>""", unsafe_allow_html=True)
    with t2:
        st.markdown(f"""
        <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08)">
            <div style="font-family:var(--mono);font-size:8px;letter-spacing:.2em;color:var(--faint);text-transform:uppercase;margin-bottom:6px">Composite Score</div>
            <div style="font-family:var(--serif);font-size:32px;font-weight:500;color:var(--gold)">{top.get("Score",0):.0f}</div>
        </div>""", unsafe_allow_html=True)
    with t3:
        st.markdown(f"""
        <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08)">
            <div style="font-family:var(--mono);font-size:8px;letter-spacing:.2em;color:var(--faint);text-transform:uppercase;margin-bottom:6px">EV / EBITDA</div>
            <div style="font-family:var(--serif);font-size:32px;font-weight:500;color:var(--ink)">{top.get("EV/EBITDA",0):.1f}×</div>
        </div>""", unsafe_allow_html=True)
    with t4:
        st.markdown(f"""
        <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08)">
            <div style="font-family:var(--mono);font-size:8px;letter-spacing:.2em;color:var(--faint);text-transform:uppercase;margin-bottom:6px">EBITDA Margin</div>
            <div style="font-family:var(--serif);font-size:32px;font-weight:500;color:var(--green)">{top.get("EBITDA Margin %",0):.1f}%</div>
        </div>""", unsafe_allow_html=True)

# ─── TOP 5 TABLE ──────────────────────────────────────────────────────────────
st.markdown("---")
sec_label("Universe Ranking — Top 5 Targets")
cols_show = ["Company", "Sector", "Score", "Mkt Cap (€bn)", "EV/EBITDA", "EBITDA Margin %", "ND/EBITDA"]
top5 = df[cols_show].head(5).reset_index(drop=True)
top5.index = top5.index + 1
st.dataframe(top5, use_container_width=True, height=220)

# ─── NAVIGATE ─────────────────────────────────────────────────────────────────
st.markdown("---")
sec_label("Navigate the Engine")
n1,n2,n3,n4,n5 = st.columns(5)
nav_items = [
    (n1, "pages/2_Screener.py",   "🔍", "Universe Screener",    "Filter SBF 120 by sector, size, multiples, margins."),
    (n2, "pages/3_Ranker.py",     "🎯", "Target Ranker",        "8-pillar transparent scoring — 0 to 100."),
    (n3, "pages/4_Financials.py", "📊", "Financial Statements", "Standardised IS / BS / CF, 5-year history, ratios."),
    (n4, "pages/6_Diligence.py",  "🔎", "Diligence View",       "QoE, EBITDA bridge, WC, net debt, red flags."),
    (n5, "pages/7_Signals.py",    "📡", "Deal Signals",         "Live M&A signal watch across SBF 120 companies."),
]
for col, pg, icon, title, desc in nav_items:
    with col:
        st.markdown(f"""
        <div style="background:var(--paper2);padding:18px 16px 12px;border:1px solid rgba(16,14,12,.07);border-top:2px solid var(--gold)">
            <div style="font-size:22px;margin-bottom:8px">{icon}</div>
            <div style="font-family:var(--serif);font-size:14px;font-weight:600;color:var(--ink);margin-bottom:6px">{title}</div>
            <div style="font-family:var(--sans);font-size:11px;color:var(--muted);line-height:1.5;margin-bottom:10px">{desc}</div>
        </div>""", unsafe_allow_html=True)
        st.page_link(pg, label=f"→ Open {title}", use_container_width=True)

st.markdown("""
<div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.15em;color:var(--faint);text-align:center;padding:24px 0 8px;text-transform:uppercase">
    Deal Sourcing &amp; Preliminary Diligence Engine · Aryan S. Kothari · SKEMA Paris 2025 · For demonstration purposes only — not investment advice
</div>""", unsafe_allow_html=True)
