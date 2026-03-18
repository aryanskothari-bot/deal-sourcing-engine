"""
app.py — Deal Sourcing & Preliminary Diligence Engine
Main entry point. Redirects to Home page.
Run: streamlit run app.py
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from ui.styles import inject_css, page_header, sec_label
from config import APP_TITLE, APP_SUBTITLE, APP_VERSION, APP_AUTHOR

st.set_page_config(
    page_title="Deal Sourcing Engine",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ─── LANDING ──────────────────────────────────────────────────────────────────
page_header(
    title="Deal Sourcing &amp; Preliminary <em>Diligence Engine</em>",
    subtitle=APP_SUBTITLE,
    badge=f"v{APP_VERSION} · Phase 1 · SBF 120",
)

st.markdown("""
<div style="max-width:680px;font-family:var(--sans);font-size:14px;color:var(--muted);line-height:1.85;margin-bottom:32px">
    A Python-based deal workflow tool replicating early-stage M&amp;A analyst work — from 
    <b style="color:var(--ink)">universe screening</b> through <b style="color:var(--ink)">acquisition 
    target ranking</b>, <b style="color:var(--ink)">financial statement standardisation</b>, and 
    <b style="color:var(--ink)">FDD-style preliminary diligence review</b>. 
    Built on Euronext Paris / SBF 120 public data.
</div>
""", unsafe_allow_html=True)

sec_label("Navigate")

col1, col2, col3, col4, col5 = st.columns(5)

pages = [
    (col1, "🏠", "Home",                 "Universe overview, top targets, quick metrics.",            "pages/1_Home.py"),
    (col2, "🔍", "Universe Screener",    "Filter SBF 120 by sector, size, multiples, margins.",       "pages/2_Screener.py"),
    (col3, "🎯", "Target Ranker",        "8-pillar transparent scoring — 0 to 100.",                  "pages/3_Ranker.py"),
    (col4, "📊", "Financial Statements", "Standardised IS / BS / CF, 5-year history, ratios.",        "pages/4_Financials.py"),
    (col5, "📋", "Shortlist & Export",   "Ranked shortlist with inclusion rationale + Excel export.", "pages/5_Shortlist.py"),
]

for col, icon, title, desc, _ in pages:
    with col:
        st.markdown(f"""
        <div style="background:var(--paper2);padding:20px 16px 18px;border:1px solid rgba(16,14,12,.07);
                    border-top:2px solid var(--gold);height:100%">
            <div style="font-size:24px;margin-bottom:10px">{icon}</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:15px;font-weight:600;
                        color:var(--ink);margin-bottom:6px">{title}</div>
            <div style="font-family:var(--sans);font-size:11.5px;color:var(--muted);line-height:1.55">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(f"""
<div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.15em;color:var(--faint);
            text-align:center;padding-top:20px;border-top:1px solid rgba(16,14,12,.07);text-transform:uppercase">
    {APP_TITLE} · {APP_AUTHOR} · SKEMA Paris 2025 · For demonstration purposes only — not investment advice
</div>
""", unsafe_allow_html=True)
