"""
pages/0_About.py
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ui.styles import inject_css, page_header

st.set_page_config(page_title="About", page_icon="📝", layout="wide")
inject_css()

_c1,_c2,_c3,_c4,_c5,_c6,_c7 = st.columns(7)
with _c1: st.page_link("pages/0_About.py",        label="📝 About",      use_container_width=True)
with _c2: st.page_link("pages/2_Screener.py",      label="🔍 Screener",   use_container_width=True)
with _c3: st.page_link("pages/3_Ranker.py",        label="🎯 Ranker",     use_container_width=True)
with _c4: st.page_link("pages/4_Financials.py",    label="📊 Financials", use_container_width=True)
with _c5: st.page_link("pages/8_Valuation.py",     label="📈 Valuation",  use_container_width=True)
with _c6: st.page_link("pages/9_Benchmarking.py",  label="📐 Comps",      use_container_width=True)
with _c7: st.page_link("pages/7_Signals.py",       label="📡 Signals",    use_container_width=True)
st.markdown("<hr style='margin:4px 0 16px 0;border-color:rgba(155,111,41,.25)'>", unsafe_allow_html=True)

page_header("About this <em>project</em>", "Why I built it, how the model works, what it is and is not")

col_main, col_aside = st.columns([2, 1])

with col_main:

    st.markdown("### Why I built this")
    st.markdown("""
At Nuvama Wealth in Mumbai, most of my Phase 1 origination work was manual — pulling Bloomberg data
into Excel, applying filters, writing one-line rationales for 40+ companies, then presenting a shortlist
to the senior team. It worked, but it was slow and the logic was not reproducible across analysts.

When I started the MSc at SKEMA, I wanted to build a version of that workflow that was systematic,
transparent, and could be explained to anyone. Not a black box that spits out rankings — something
where every score can be traced back to a specific financial metric with an explicit weight.
This is that tool.

It covers 29 companies across the Euronext Paris / SBF 120. I chose France for Phase 1 because
I know the market, the data is clean, and the universe is diverse enough to be interesting:
luxury, pharma, industrials, energy, real estate — all with different acquisition dynamics.
""")

    st.markdown("### How the scoring works")
    st.markdown("""
Each company gets scored 0-100 across eight pillars. The scores are min-max normalised within
the universe, so a 90 on Profitability means you are near the top of *this* universe —
not that you have a 90% EBITDA margin.

The weights reflect what I would actually care about when pitching a target to a deal team:
""")

    pillars = [
        ("Revenue Growth", "15%", "Trend matters more than level"),
        ("Profitability", "15%", "EBITDA margin as proxy for operating quality"),
        ("Valuation", "15%", "Lower EV/EBITDA = more attractive entry, all else equal"),
        ("Acquisition Fit", "13%", "Blend of size, leverage headroom, sector fit"),
        ("Balance Sheet Quality", "12%", "Current ratio, asset coverage"),
        ("Leverage", "12%", "ND/EBITDA, capped at 8x to avoid distortion from outliers"),
        ("Size Compatibility", "10%", "Mid-cap sweet spot, penalise extremes"),
        ("Geographic Relevance", "8%", "All French in Phase 1 — will differentiate in Phase 2"),
    ]
    for pillar, weight, note in pillars:
        st.markdown(f"""
<div style="display:flex;align-items:baseline;gap:12px;padding:7px 0;border-bottom:1px solid rgba(16,14,12,.05)">
    <span style="font-family:var(--mono);font-size:9px;color:var(--gold);letter-spacing:.1em;min-width:36px">{weight}</span>
    <span style="font-family:var(--sans);font-size:13px;font-weight:600;color:var(--ink);min-width:180px">{pillar}</span>
    <span style="font-family:var(--sans);font-size:12px;color:var(--muted)">{note}</span>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
The weights are not calibrated to historical M&A outcomes. They reflect judgment, not regression.
I would welcome a debate on whether Valuation should be weighted higher than Leverage
for PE vs strategic buyers — the answer changes meaningfully depending on the mandate.
""")

    st.markdown("### What this is not")
    st.markdown("""
This is not a live trading system, an investment recommendation engine, or a substitute for
proper financial due diligence. The QoE adjustments on the Diligence page are illustrative —
sector-typical normalisation items, not company-specific audit findings. The financial data comes
from Bloomberg/yfinance and public filings; it has the usual data quality issues you would
expect from any automated pull.

If anything here looks wrong or you would calibrate the model differently, I am genuinely
interested in the conversation. The whole point is that the methodology is visible and debatable.
""")

    st.markdown("### What is next")
    st.markdown("""
**Phase 2:** expand to cross-border (DAX, FTSE, AEX) which will finally make the Geography
pillar meaningful and create real dispersion across the universe.

**Phase 3:** a proper LBO model — sources and uses, debt tranches (senior / mezzanine / equity),
debt schedule, and a full distribution waterfall — to replace the back-of-envelope IRR model
currently on the Valuation page.
""")

    st.markdown("""
<div style="font-family:var(--mono);font-size:9px;letter-spacing:.1em;color:var(--faint);
            margin-top:24px;padding-top:16px;border-top:1px solid rgba(16,14,12,.08)">
    Aryan Shrenick Kothari &middot; MSc Corporate Financial Management, SKEMA Paris &middot; March 2026<br>
    aryanskothari@gmail.com &middot; Previously: Nuvama Wealth, Prabhudas Lilladher
</div>
""", unsafe_allow_html=True)

with col_aside:
    st.markdown("""
<div style="background:var(--paper2);padding:22px;border:1px solid rgba(16,14,12,.08);
            border-top:2px solid var(--gold);margin-top:4px">
    <div style="font-family:var(--mono);font-size:8px;letter-spacing:.22em;text-transform:uppercase;
                color:var(--faint);margin-bottom:18px">Quick facts</div>
""", unsafe_allow_html=True)

    facts = [
        ("Universe", "29 companies", "SBF 120 / Euronext Paris"),
        ("Sectors", "8 sectors", "Luxury through Real Estate"),
        ("Modules", "9 pages", "Screener through Benchmarking"),
        ("Scoring", "8-pillar", "Explicit weights, min-max normalised"),
        ("Data", "Bloomberg / yfinance", "Company filings, March 2026"),
    ]
    for label, value, sub in facts:
        st.markdown(f"""
<div style="margin-bottom:14px">
    <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--faint)">{label}</div>
    <div style="font-family:var(--serif);font-size:17px;color:var(--ink);margin:2px 0">{value}</div>
    <div style="font-family:var(--mono);font-size:8.5px;color:var(--muted)">{sub}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("""
<div style="border-top:1px solid rgba(16,14,12,.08);padding-top:14px;margin-top:4px">
    <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.18em;text-transform:uppercase;
                color:var(--faint);margin-bottom:8px">Stack</div>
    <div style="font-family:var(--mono);font-size:9px;color:var(--muted);line-height:2">
        Python &middot; Streamlit &middot; Pandas<br>
        Plotly &middot; yfinance &middot; openpyxl<br>
        GitHub &middot; Streamlit Cloud
    </div>
</div>
</div>
""", unsafe_allow_html=True)
