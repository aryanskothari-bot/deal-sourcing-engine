"""
pages/7_Signals.py — Deal Signal Monitor
Live M&A signal watch: public takeover filings, restructuring events, stake disclosures, strategic reviews.
"""

import streamlit as st
import pandas as pd
import sys, os
from datetime import datetime, timedelta
import random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row, pill
from data_sources.static_loader import get_static_df
from config import COLORS

st.set_page_config(page_title="Deal Signal Monitor", page_icon="📡", layout="wide")
inject_css()
# ─── NAV BAR ──────────────────────────────────────────────────────────────────
_c1,_c2,_c3,_c4,_c5,_c6,_c7 = st.columns(7)
with _c1: st.page_link("pages/1_Home.py",       label="🏠 Home",        use_container_width=True)
with _c2: st.page_link("pages/2_Screener.py",   label="🔍 Screener",    use_container_width=True)
with _c3: st.page_link("pages/3_Ranker.py",     label="🎯 Ranker",      use_container_width=True)
with _c4: st.page_link("pages/4_Financials.py", label="📊 Financials",  use_container_width=True)
with _c5: st.page_link("pages/5_Shortlist.py",  label="📋 Shortlist",   use_container_width=True)
with _c6: st.page_link("pages/6_Diligence.py",  label="🔎 Diligence",   use_container_width=True)
with _c7: st.page_link("pages/7_Signals.py",    label="📡 Signals",     use_container_width=True)
st.markdown("<hr style='margin:4px 0 16px 0;border-color:rgba(155,111,41,.25)'>", unsafe_allow_html=True)
# ──────────────────────────────────────────────────────────────────────────────


("Signals")

page_header(
    "Deal <em>Signal Monitor</em>",
    "Live M&A watch · Takeover filings · Stake disclosures · Strategic reviews · Restructuring events"
)

# ─── SIGNAL DATABASE (illustrative — SBF 120 / European M&A signals) ─────────
SIGNALS = [
    {
        "date": "Mar 18, 2026", "company": "Kering", "ticker": "KER.PA",
        "type": "Strategic Review", "severity": "high",
        "headline": "Kering confirms strategic review of Bottega Veneta amid portfolio restructuring",
        "detail": "Board mandated review covers potential partial disposal or JV structure. Gucci revenue decline of 12% YoY accelerating pressure on portfolio allocation. Lazard mandated as financial adviser.",
        "source": "Financial Times", "tags": ["Disposal", "Luxury", "Portfolio Review"]
    },
    {
        "date": "Mar 17, 2026", "company": "Atos", "ticker": "ATO.PA",
        "type": "Restructuring", "severity": "high",
        "headline": "Atos creditor group submits binding €3.2bn debt-to-equity restructuring proposal",
        "detail": "Ad hoc creditor group holding 68% of senior debt submits binding offer. Existing equity faces near-total dilution. French State evaluating strategic IT assets carve-out under national security provisions.",
        "source": "Les Echos", "tags": ["Debt Restructuring", "Distressed", "Tech"]
    },
    {
        "date": "Mar 15, 2026", "company": "Vivendi", "ticker": "VIV.PA",
        "type": "Stake Disclosure", "severity": "medium",
        "headline": "Vincent Bolloré family vehicle discloses 26.3% stake via AMF filing",
        "detail": "Compagnie de Cornouaille crossed 25% threshold triggering mandatory AMF disclosure. Market participants flagging potential squeeze-out scenario given post-Canal+ separation NAV discount of ~35%.",
        "source": "AMF Regulatory Filing", "tags": ["Stake Disclosure", "Squeeze-Out", "Media"]
    },
    {
        "date": "Mar 14, 2026", "company": "Rémy Cointreau", "ticker": "RCO.PA",
        "type": "M&A Rumour", "severity": "medium",
        "headline": "Pernod Ricard reportedly evaluating approach to Rémy Cointreau as spirits consolidation accelerates",
        "detail": "Bloomberg sources cite preliminary internal analysis by Pernod M&A team. Rémy family holding (72%) makes unsolicited approach structurally complex. EV/EBITDA of 14.6× suggests meaningful premium required.",
        "source": "Bloomberg", "tags": ["Takeover Approach", "Spirits", "Luxury Consumer"]
    },
    {
        "date": "Mar 12, 2026", "company": "Ipsen", "ticker": "IPN.PA",
        "type": "Strategic Review", "severity": "medium",
        "headline": "Ipsen activates strategic review process for Consumer Healthcare division",
        "detail": "Pharma-focused board opts to exit non-core OTC segment to fund oncology pipeline. Process expected to attract PE and strategic buyers. Estimated division EV €600–800mn based on 8–10× EBITDA.",
        "source": "Reuters", "tags": ["Carve-out", "Healthcare", "PE Target"]
    },
    {
        "date": "Mar 11, 2026", "company": "Bouygues", "ticker": "EN.PA",
        "type": "Acquisition", "severity": "low",
        "headline": "Bouygues Telecom completes bolt-on acquisition of regional fibre operator for €180mn",
        "detail": "Acquisition adds 420,000 homes connectable in Normandy and Bretagne regions. EV/subscriber of €429 in line with recent French fibre M&A comps. Net leverage remains comfortable at 2.1× post-deal.",
        "source": "Bouygues Press Release", "tags": ["Acquisition", "Telecom", "Bolt-on"]
    },
    {
        "date": "Mar 10, 2026", "company": "Carrefour", "ticker": "CA.PA",
        "type": "Stake Disclosure", "severity": "low",
        "headline": "Norges Bank Investment Management raises Carrefour stake to 4.2% via open market purchases",
        "detail": "NBIM filing indicates ongoing accumulation since Q4 2025. No activist agenda disclosed. Carrefour current ratio of 0.75× and thin margins remain focus of investor scrutiny.",
        "source": "AMF Regulatory Filing", "tags": ["Passive Stake", "Retail", "Institutional"]
    },
    {
        "date": "Mar 09, 2026", "company": "Capgemini", "ticker": "CAP.PA",
        "type": "Acquisition", "severity": "low",
        "headline": "Capgemini acquires AI consulting boutique for undisclosed sum, bolsters GenAI capabilities",
        "detail": "50-person specialist firm focused on enterprise LLM deployment. Talent acquisition rationale primary driver. Immaterial to Capgemini financials (€22bn revenue). Signals continued buy-and-build in AI services.",
        "source": "Capgemini IR", "tags": ["Acqui-hire", "Tech", "AI"]
    },
    {
        "date": "Mar 07, 2026", "company": "bioMérieux", "ticker": "BIM.PA",
        "type": "M&A Rumour", "severity": "low",
        "headline": "bioMérieux cited as potential target as US diagnostics majors survey European consolidation",
        "detail": "Analyst note from Jefferies flags bioMérieux as attractive M&A target given 24% EBITDA margins and €9.8bn EV. Family ownership (56%) via Institut Mérieux complicates any hostile approach.",
        "source": "Jefferies Research", "tags": ["M&A Target", "Healthcare", "Diagnostics"]
    },
]

# ─── FILTERS ──────────────────────────────────────────────────────────────────
# ─── SIGNAL HEATMAP BY SECTOR ─────────────────────────────────────────────────
sec_label("Signal Heatmap by Sector")

sector_signals = {}
sector_map = {
    "KER.PA": "Luxury & Consumer", "ATO.PA": "Technology & Media",
    "VIV.PA": "Technology & Media", "RCO.PA": "Luxury & Consumer",
    "IPN.PA": "Healthcare & Pharma", "EN.PA": "Industrials & Engineering",
    "CA.PA": "Retail & Distribution", "CAP.PA": "Technology & Media",
    "BIM.PA": "Healthcare & Pharma",
}
for s in SIGNALS:
    sector = sector_map.get(s["ticker"], "Other")
    if sector not in sector_signals:
        sector_signals[sector] = {"high": 0, "medium": 0, "low": 0, "total": 0}
    sector_signals[sector][s["severity"]] += 1
    sector_signals[sector]["total"] += 1

heatmap_rows = ""
for sector, counts in sorted(sector_signals.items(), key=lambda x: -x[1]["total"]):
    high_boxes   = '<div style="width:14px;height:14px;background:var(--red);opacity:.8;display:inline-block;margin-right:3px"></div>' * counts["high"]
    medium_boxes = '<div style="width:14px;height:14px;background:var(--gold);opacity:.8;display:inline-block;margin-right:3px"></div>' * counts["medium"]
    low_boxes    = '<div style="width:14px;height:14px;background:var(--green);opacity:.7;display:inline-block;margin-right:3px"></div>' * counts["low"]
    total        = counts["total"]
    heatmap_rows += (
        "<div style='display:grid;grid-template-columns:200px 1fr 80px;align-items:center;"
        "padding:10px 0;border-bottom:1px solid rgba(16,14,12,.06)'>"
        f"<div style='font-family:var(--mono);font-size:9px;letter-spacing:.1em;color:var(--muted)'>{sector}</div>"
        f"<div style='display:flex;gap:3px;align-items:center'>{high_boxes}{medium_boxes}{low_boxes}</div>"
        f"<div style='font-family:var(--serif);font-size:16px;font-weight:500;color:var(--ink);text-align:right'>{total}</div>"
        "</div>"
    )

st.markdown(f"""
<div style="background:var(--paper2);padding:20px 24px;border:1px solid rgba(16,14,12,.08)">
    <div style="display:grid;grid-template-columns:200px 1fr 80px;margin-bottom:10px;
                padding-bottom:8px;border-bottom:1px solid rgba(16,14,12,.1)">
        <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.25em;color:var(--faint);text-transform:uppercase">Sector</div>
        <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.25em;color:var(--faint);text-transform:uppercase">Signal Distribution</div>
        <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.25em;color:var(--faint);text-transform:uppercase;text-align:right">Count</div>
    </div>
    {heatmap_rows}
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"""
<div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.15em;color:var(--faint);text-align:center;padding-top:20px;text-transform:uppercase">
    Deal Signal Monitor · Deal Sourcing &amp; Preliminary Diligence Engine · Aryan S. Kothari · SKEMA Paris 2025 ·
    All signals illustrative — for demonstration purposes only · Not investment advice
</div>
""", unsafe_allow_html=True)
