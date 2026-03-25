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
During my MSc in Corporate Financial Management at SKEMA Paris, the M&A Strategy coursework and
LBO workshops got me thinking about what Phase 1 origination actually looks like at a deal team level.
At Nuvama Wealth I had done investment analysis and client advisory work — screening products,
building models, running portfolio reviews — but not structured buy-side deal sourcing.

I wanted to build a tool that replicated that Phase 1 workflow: take a defined universe,
apply consistent screening criteria, score every company on the same set of factors,
and produce a shortlist with rationale you could actually defend in a meeting.
Not a black box. Something where every score traces back to a specific metric with an explicit weight.

The SBF 120 / Euronext Paris made sense for Phase 1 — I know the French market from my coursework,
the data is clean, and the universe is genuinely diverse: luxury, pharma, industrials, energy,
real estate — all with different acquisition dynamics and valuation logic.
""")

    st.markdown("### How the scoring works")
    st.markdown("""
Each company gets scored 0-100 across eight pillars. Scores are min-max normalised within
the universe, so a 90 on Profitability means you are near the top of *this* peer group,
not that you have a 90% EBITDA margin.

The weights reflect what I would prioritise when pitching a target to a deal team:
""")

    pillars = [
        ("Revenue Growth", "15%", "Trend matters more than level — a declining business needs a turnaround thesis"),
        ("Profitability", "15%", "EBITDA margin as proxy for operating quality and pricing power"),
        ("Valuation", "15%", "Lower EV/EBITDA = more attractive entry, all else equal"),
        ("Acquisition Fit", "13%", "Blend of size compatibility, leverage headroom, and sector fit"),
        ("Balance Sheet Quality", "12%", "Current ratio and asset coverage — liquidity buffer matters"),
        ("Leverage", "12%", "ND/EBITDA capped at 8x to avoid distortion from outliers like REITs"),
        ("Size Compatibility", "10%", "Mid-cap sweet spot for M&A — penalise very small and mega-cap"),
        ("Geographic Relevance", "8%", "All French in Phase 1, so no dispersion yet — expands in Phase 2"),
    ]
    for pillar, weight, note in pillars:
        st.markdown(f"""
<div style="display:flex;align-items:baseline;gap:12px;padding:8px 0;border-bottom:1px solid rgba(16,14,12,.05)">
    <span style="font-family:var(--mono);font-size:9px;color:var(--gold);letter-spacing:.1em;min-width:36px">{weight}</span>
    <span style="font-family:var(--sans);font-size:13px;font-weight:600;color:var(--ink);min-width:190px">{pillar}</span>
    <span style="font-family:var(--sans);font-size:12px;color:var(--muted)">{note}</span>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
The weights are judgment calls, not calibrated to historical deal outcomes.
I would weight Valuation higher for a PE mandate and Acquisition Fit higher for a strategic
corporate buyer — the right answer depends on who is sitting across the table.
""")

    st.markdown("### What this is not")
    st.markdown("""
This is not a live trading system, an investment recommendation engine, or a substitute for proper
financial due diligence. The QoE adjustments on the Diligence page are illustrative —
sector-typical normalisation items based on what you would commonly see in FDD,
not company-specific audit findings from the actual accounts.

The financial data pulls from Bloomberg/yfinance and public filings. It has the usual
data quality issues: stale prices, missing line items, yfinance rate limits.
The static fallback dataset fills gaps but is fixed at March 2026.

If anything here looks wrong or you would calibrate the model differently,
I am genuinely interested in the debate. The methodology is visible precisely so it can be challenged.
""")

    st.markdown("### What is next")
    st.markdown("""
**Phase 2:** Expand to cross-border universe (DAX 40, FTSE 100, AEX) —
this will finally make the Geography pillar meaningful and test whether French companies
actually screen better than German or UK peers on the same criteria.

**Phase 3:** Proper LBO model — sources and uses, debt tranches (senior / mezzanine / equity),
full debt amortisation schedule, and distribution waterfall —
replacing the simplified IRR model currently on the Valuation page.
""")

    st.markdown("""
<div style="font-family:var(--mono);font-size:9px;letter-spacing:.1em;color:var(--faint);
            margin-top:24px;padding-top:16px;border-top:1px solid rgba(16,14,12,.08)">
    Aryan Shrenick Kothari &middot; MSc Corporate Financial Management, SKEMA Paris 2024&ndash;2026<br>
    Previously: Nuvama Wealth &amp; Investment (Junior Associate) &middot; Prabhudas Lilladher (Equity Research Intern)<br>
    aryanskothari@gmail.com &middot; Available May 2026
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
        ("Built during", "MSc at SKEMA", "2024 - 2026, Paris"),
        ("Universe", "29 companies", "SBF 120 / Euronext Paris"),
        ("Sectors", "8 sectors", "Luxury through Real Estate"),
        ("Modules", "9 pages", "Screener through Benchmarking"),
        ("Scoring", "8-pillar model", "Explicit weights, min-max normalised"),
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
<div style="border-top:1px solid rgba(16,14,12,.08);padding-top:14px;margin-top:14px">
    <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.18em;text-transform:uppercase;
                color:var(--faint);margin-bottom:8px">Links</div>
    <div style="font-family:var(--mono);font-size:9px;line-height:2">
        <a href="https://aryanskothari-bot.github.io/aryanskothari" target="_blank"
           style="color:var(--gold);text-decoration:none">Portfolio Site &#8599;</a><br>
        <a href="https://github.com/aryanskothari-bot/deal-sourcing-engine" target="_blank"
           style="color:var(--gold);text-decoration:none">GitHub Source &#8599;</a>
    </div>
</div>
</div>
""", unsafe_allow_html=True)
