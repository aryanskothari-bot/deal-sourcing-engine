"""
pages/0_About.py — About this tool, in plain English.
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ui.styles import inject_css, page_header, sec_label

st.set_page_config(page_title="About", page_icon="📝", layout="wide")
inject_css()

_c1,_c2,_c3,_c4,_c5,_c6,_c7 = st.columns(7)
with _c1: st.page_link("pages/1_Home.py",        label="🏠 Home",       use_container_width=True)
with _c2: st.page_link("pages/2_Screener.py",    label="🔍 Screener",   use_container_width=True)
with _c3: st.page_link("pages/3_Ranker.py",      label="🎯 Ranker",     use_container_width=True)
with _c4: st.page_link("pages/4_Financials.py",  label="📊 Financials", use_container_width=True)
with _c5: st.page_link("pages/8_Valuation.py",   label="📈 Valuation",  use_container_width=True)
with _c6: st.page_link("pages/9_Benchmarking.py",label="📐 Comps",      use_container_width=True)
with _c7: st.page_link("pages/7_Signals.py",     label="📡 Signals",    use_container_width=True)
st.markdown("<hr style='margin:4px 0 16px 0;border-color:rgba(155,111,41,.25)'>", unsafe_allow_html=True)

page_header("About this <em>project</em>", "Why I built it, how the model works, what it is and is not")

col_main, col_aside = st.columns([2, 1])

with col_main:
    st.markdown("""
    <div style="font-family:var(--sans);font-size:14px;color:var(--ink2);line-height:1.9;max-width:640px">

    <h3 style="font-family:var(--serif);font-size:22px;font-weight:500;color:var(--ink);margin-bottom:12px">Why I built this</h3>
    <p>
        At Nuvama Wealth in Mumbai, most of my Phase 1 origination work was manual — pulling Bloomberg data
        into Excel, applying filters, writing one-line rationales for 40+ companies, then presenting a shortlist
        to the senior team. It worked, but it was slow and the logic wasn't reproducible across analysts.
    </p>
    <p>
        When I started the MSc at SKEMA, I wanted to build a version of that workflow that was systematic,
        transparent, and could be explained to anyone. Not a black box that spits out rankings, but something
        where every score can be traced back to a specific financial metric with an explicit weight.
        This is that tool.
    </p>
    <p>
        It covers 29 companies across the Euronext Paris / SBF 120. I chose France for Phase 1 because
        I know the market, the data is clean, and the universe is diverse enough to be interesting
        (luxury, pharma, industrials, energy, real estate — all with different acquisition dynamics).
    </p>

    <h3 style="font-family:var(--serif);font-size:22px;font-weight:500;color:var(--ink);margin:24px 0 12px">How the scoring works</h3>
    <p>
        Each company gets scored 0–100 across eight pillars. The scores are min-max normalised within the universe,
        so a 90 on Profitability means you're near the top of <em>this</em> universe — not that you have a 90%
        EBITDA margin. The weights reflect what I'd actually care about when pitching a target to a deal team:
    </p>
    <ul style="color:var(--ink2);line-height:2">
        <li><b>Revenue Growth (15%)</b> — trend matters more than level</li>
        <li><b>Profitability (15%)</b> — EBITDA margin as proxy for operating quality</li>
        <li><b>Valuation (15%)</b> — lower EV/EBITDA = more attractive entry, all else equal</li>
        <li><b>Acquisition Fit (13%)</b> — blend of size, leverage headroom, sector fit</li>
        <li><b>Balance Sheet Quality (12%)</b> — current ratio, asset coverage</li>
        <li><b>Leverage (12%)</b> — ND/EBITDA, capped at 8× to avoid distortion from outliers</li>
        <li><b>Size Compatibility (10%)</b> — mid-cap sweet spot, penalise extremes</li>
        <li><b>Geographic Relevance (8%)</b> — all French in Phase 1, so this doesn't differentiate yet</li>
    </ul>
    <p>
        The weights are not calibrated to historical M&A outcomes. They reflect judgment, not regression.
        I'd welcome a debate on whether Valuation should be weighted higher than Leverage for PE vs strategic buyers.
    </p>

    <h3 style="font-family:var(--serif);font-size:22px;font-weight:500;color:var(--ink);margin:24px 0 12px">What this is not</h3>
    <p>
        This is not a live trading system, an investment recommendation engine, or a substitute for proper
        financial due diligence. The QoE adjustments on the Diligence page are illustrative — sector-typical
        normalisation items, not company-specific audit findings. The financial data comes from Bloomberg/yfinance
        and public filings; it has the usual data quality issues you'd expect from any automated pull.
    </p>
    <p>
        If anything here looks wrong or you'd calibrate the model differently, I'm genuinely interested
        in the conversation. The whole point is that the methodology is visible and debatable.
    </p>

    <h3 style="font-family:var(--serif);font-size:22px;font-weight:500;color:var(--ink);margin:24px 0 12px">What's next</h3>
    <p>
        Phase 2: expand to cross-border (DAX, FTSE, AEX) which will finally make the Geography pillar meaningful.
        Also planning a proper LBO model page — sources & uses, debt tranches, full distribution waterfall —
        to replace the back-of-envelope IRR model currently on the Valuation page.
    </p>
    <p style="color:var(--faint);font-family:var(--mono);font-size:10px;margin-top:20px">
        Built by Aryan Shrenick Kothari · MSc Corporate Financial Management, SKEMA Paris · March 2026 ·
        aryanskothari@gmail.com · Previously: Nuvama Wealth, Prabhudas Lilladher
    </p>

    </div>
    """, unsafe_allow_html=True)

with col_aside:
    st.markdown("""
    <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08);border-top:2px solid var(--gold);margin-top:8px">
        <div style="font-family:var(--mono);font-size:8px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);margin-bottom:14px">Quick facts</div>

        <div style="margin-bottom:12px">
            <div style="font-family:var(--mono);font-size:8px;color:var(--faint);letter-spacing:.12em;text-transform:uppercase">Universe</div>
            <div style="font-family:var(--serif);font-size:18px;color:var(--ink)">29 companies</div>
            <div style="font-family:var(--mono);font-size:9px;color:var(--muted)">SBF 120 / Euronext Paris</div>
        </div>

        <div style="margin-bottom:12px">
            <div style="font-family:var(--mono);font-size:8px;color:var(--faint);letter-spacing:.12em;text-transform:uppercase">Sectors</div>
            <div style="font-family:var(--serif);font-size:18px;color:var(--ink)">8 sectors</div>
            <div style="font-family:var(--mono);font-size:9px;color:var(--muted)">Luxury to Real Estate</div>
        </div>

        <div style="margin-bottom:12px">
            <div style="font-family:var(--mono);font-size:8px;color:var(--faint);letter-spacing:.12em;text-transform:uppercase">Modules</div>
            <div style="font-family:var(--serif);font-size:18px;color:var(--ink)">9 pages</div>
            <div style="font-family:var(--mono);font-size:9px;color:var(--muted)">Screener through benchmarking</div>
        </div>

        <div style="margin-bottom:12px">
            <div style="font-family:var(--mono);font-size:8px;color:var(--faint);letter-spacing:.12em;text-transform:uppercase">Scoring model</div>
            <div style="font-family:var(--serif);font-size:18px;color:var(--ink)">8-pillar</div>
            <div style="font-family:var(--mono);font-size:9px;color:var(--muted)">Explicit weights, min-max norm.</div>
        </div>

        <div style="margin-bottom:12px">
            <div style="font-family:var(--mono);font-size:8px;color:var(--faint);letter-spacing:.12em;text-transform:uppercase">Data</div>
            <div style="font-family:var(--serif);font-size:16px;color:var(--ink)">Bloomberg / yfinance</div>
            <div style="font-family:var(--mono);font-size:9px;color:var(--muted)">Company filings · March 2026</div>
        </div>

        <div style="border-top:1px solid rgba(16,14,12,.08);padding-top:12px;margin-top:4px">
            <div style="font-family:var(--mono);font-size:8px;color:var(--faint);letter-spacing:.12em;text-transform:uppercase;margin-bottom:6px">Stack</div>
            <div style="font-family:var(--mono);font-size:9px;color:var(--muted);line-height:1.8">
                Python · Streamlit · Pandas<br>
                Plotly · yfinance · openpyxl<br>
                Deployed: Streamlit Cloud
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
