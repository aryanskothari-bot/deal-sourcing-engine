"""
pages/10_Deal_Memo.py - 1-page investment memo for top target
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from ui.styles import inject_css, page_header, sec_label
import pandas as pd

st.set_page_config(page_title="Deal Memo", page_icon="📋", layout="wide")
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

page_header("Deal <em>Memo</em>", "One-page investment memo — the format an associate uses before an IC presentation")

st.markdown("""
<div style="background:rgba(155,111,41,.06);border-left:2px solid var(--gold);padding:12px 16px;margin-bottom:24px;max-width:800px">
    <span style="font-family:var(--mono);font-size:8px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold)">
    What this is &mdash; </span>
    <span style="font-family:var(--sans);font-size:12.5px;color:var(--muted)">
    A deal memo is the first internal document a junior analyst writes when a target clears Phase 1 screening.
    It goes to the deal team before any approach to management. It answers three questions:
    why this target, why now, and why at this price. The template below is structured around Ipsen,
    the highest-scoring target in this universe.
    </span>
</div>
""", unsafe_allow_html=True)

# Company selector
from data_sources.static_loader import STATIC_COMPANIES

# Map static_loader columns to expected names
def _build_universe():
    rows = []
    for c in STATIC_COMPANIES:
        rows.append({
            "Company":         c.get("name", ""),
            "Ticker":          c.get("ticker", ""),
            "Sector":          c.get("sector", ""),
            "Score":           c.get("acq_score", 0),
            "Mkt Cap (€bn)":   c.get("mktcap_bn", 0),
            "EV/EBITDA":       c.get("ev_ebitda", 0),
            "EBITDA Margin %": c.get("ebitda_margin_pct", 0),
            "ND/EBITDA":       c.get("net_debt_ebitda", 0),
        })
    return rows
UNIVERSE = _build_universe()
import pandas as pd

df = pd.DataFrame(UNIVERSE)
companies = sorted(df["Company"].tolist())
selected = st.selectbox("Generate memo for:", companies, index=companies.index("Ipsen") if "Ipsen" in companies else 0)

row = df[df["Company"] == selected].iloc[0]

# ── MEMO HEADER ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="border:1px solid rgba(16,14,12,.12);border-top:3px solid var(--gold);padding:28px 32px;margin:20px 0;background:var(--paper2)">

    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px">
        <div>
            <div style="font-family:var(--mono);font-size:8px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);margin-bottom:4px">CONFIDENTIAL · INTERNAL ONLY · PHASE 1 ORIGINATION</div>
            <div style="font-family:var(--serif);font-size:26px;font-weight:500;color:var(--ink)">{selected}</div>
            <div style="font-family:var(--mono);font-size:9px;color:var(--muted);margin-top:4px">{row.get("Ticker","")}&nbsp;·&nbsp;{row.get("Sector","")}&nbsp;·&nbsp;Euronext Paris</div>
        </div>
        <div style="text-align:right">
            <div style="font-family:var(--mono);font-size:8px;color:var(--faint)">Prepared by</div>
            <div style="font-family:var(--sans);font-size:13px;color:var(--ink)">Aryan S. Kothari</div>
            <div style="font-family:var(--mono);font-size:8px;color:var(--faint)">March 2026 · SBF 120 Coverage</div>
        </div>
    </div>

    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;padding:16px 0;border-top:1px solid rgba(16,14,12,.08);border-bottom:1px solid rgba(16,14,12,.08);margin-bottom:20px">
        <div>
            <div style="font-family:var(--mono);font-size:7px;letter-spacing:.15em;text-transform:uppercase;color:var(--faint)">Acq. Score</div>
            <div style="font-family:var(--serif);font-size:22px;color:var(--gold)">{row.get("Score",0):.0f}<span style="font-size:12px">/100</span></div>
        </div>
        <div>
            <div style="font-family:var(--mono);font-size:7px;letter-spacing:.15em;text-transform:uppercase;color:var(--faint)">Market Cap</div>
            <div style="font-family:var(--serif);font-size:22px;color:var(--ink)">€{row.get("Mkt Cap (€bn)",0):.1f}bn</div>
        </div>
        <div>
            <div style="font-family:var(--mono);font-size:7px;letter-spacing:.15em;text-transform:uppercase;color:var(--faint)">EV / EBITDA</div>
            <div style="font-family:var(--serif);font-size:22px;color:var(--ink)">{row.get("EV/EBITDA",0):.1f}×</div>
        </div>
        <div>
            <div style="font-family:var(--mono);font-size:7px;letter-spacing:.15em;text-transform:uppercase;color:var(--faint)">EBITDA Margin</div>
            <div style="font-family:var(--serif);font-size:22px;color:var(--ink)">{row.get("EBITDA Margin %",0):.0f}%</div>
        </div>
        <div>
            <div style="font-family:var(--mono);font-size:7px;letter-spacing:.15em;text-transform:uppercase;color:var(--faint)">ND / EBITDA</div>
            <div style="font-family:var(--serif);font-size:22px;color:var(--ink)">{row.get("ND/EBITDA",0):.1f}×</div>
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

# ── MEMO SECTIONS ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

# Pre-written theses for the top targets
THESES = {
    "Ipsen": {
        "situation": "Ipsen is a specialty pharma with an oncology-dominated portfolio (Cabometyx, Somatuline) generating predictable, high-margin revenue. The company is executing an OTC divestiture (Essentiale, Smecta) with estimated proceeds of €600-800M, which will leave a focused, high-quality business trading at a significant discount to pharma peers.",
        "opportunity": "At 6.4× EV/EBITDA with a net cash position (ND/EBITDA -0.5×), the acquirer pays almost nothing for balance sheet risk. Post-OTC, the remaining Ipsen trades at 5.5-6× on restructured revenue — compared to pharma peers at 9-11×. The catalyst is the OTC sale process, which creates a natural re-rating window.",
        "why_now": "OTC sale process is expected to complete H2 2026. An approach before closing — while the capital structure is in flux and the family block may be open to engagement — is the logical timing.",
        "risks": "Family holding (Beaufour family, ~22%) can block any hostile approach. Biosimilar competition for Somatuline post-2027 is the single biggest earnings risk. Cabometyx patent cliff beyond 2030.",
        "comps": "Qiagen (2020, 11× EV/EBITDA), Pierre Fabre (private, 8-9×), Recordati (12×). Ipsen at 6.4× is materially cheap.",
        "recommendation": "PURSUE — initiate approach via financial adviser post-OTC sale announcement. Target entry at 7-8× EV/EBITDA with family rollover.",
    },
    "Vallourec": {
        "situation": "Vallourec makes premium steel pipes for oil & gas (OCTG). Post-restructuring through 2022-2023 (€2.5bn debt reduction), the company has returned to FCF generation. Brazilian operations are the real asset — producing high-margin premium connections for deepwater projects.",
        "opportunity": "At 2.9× EV/EBITDA, Vallourec trades at a 40-50% discount to OCTG peers (Tenaris, TMK). The market is pricing in the commodity cycle rather than the structural position of the Brazilian business. A strategic buyer with a strong balance sheet can acquire a leading position in deepwater connections at distressed pricing.",
        "why_now": "Oil capex cycle is turning up — IEA forecasts upstream investment +7% in 2026. Vallourec's recent FCF generation will attract attention from sector consolidators in H2 2026.",
        "risks": "Commodity price exposure is structural. Any reversal in oil capex would compress EBITDA rapidly. Brazilian FX risk (BRL/EUR). Steel input costs.",
        "comps": "Tenaris (7-8× EBITDA), TMK (4-5× on Russian discount). Vallourec at 2.9× implies significant upside to fair value.",
        "recommendation": "PURSUE — financial buyer angle with Brazilian asset as exit vehicle. IRR case works at current entry; requires commodity cycle not reversing materially.",
    },
}

thesis = THESES.get(selected, {
    "situation": f"{selected} is a {row.get('Sector','')} company listed on Euronext Paris. With an acquisition score of {row.get('Score',0):.0f}/100, it clears the Phase 1 quantitative screen on the key criteria: size compatibility, leverage headroom, and margin profile.",
    "opportunity": f"At {row.get('EV/EBITDA',0):.1f}× EV/EBITDA and {row.get('EBITDA Margin %',0):.0f}% EBITDA margins, the entry case is supported by the valuation. Net leverage of {row.get('ND/EBITDA',0):.1f}× is within conventional acquisition parameters and leaves room for financial engineering.",
    "why_now": "The company is at an inflection point in its sector cycle. Public market valuations for peers suggest the current multiple may not persist, making H2 2026 a natural approach window.",
    "risks": "Execution risk on any strategic pivot. Sector-specific cycle risk. Governance and family holding constraints may limit strategic options.",
    "comps": "Peers in this sector trade at 8-12× EBITDA. See the Benchmarking page for full peer comps.",
    "recommendation": f"MONITOR — add to Phase 2 pipeline. Score of {row.get('Score',0):.0f}/100 justifies continued coverage but not an immediate approach.",
})

with col_left:
    for label, key in [
        ("Business situation", "situation"),
        ("Investment opportunity", "opportunity"),
        ("Why now", "why_now"),
    ]:
        st.markdown(f"""
<div style="margin-bottom:18px">
    <div style="font-family:var(--mono);font-size:8px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin-bottom:6px">{label}</div>
    <div style="font-family:var(--sans);font-size:13px;color:var(--ink2);line-height:1.8">{thesis[key]}</div>
</div>
""", unsafe_allow_html=True)

with col_right:
    for label, key in [
        ("Key risks", "risks"),
        ("Comparable transactions", "comps"),
        ("Recommendation", "recommendation"),
    ]:
        bg = "rgba(27,75,43,.08)" if key == "recommendation" else "transparent"
        border = "1px solid rgba(27,75,43,.25)" if key == "recommendation" else "none"
        st.markdown(f"""
<div style="margin-bottom:18px;padding:{'12px 14px' if key == 'recommendation' else '0'};background:{bg};border:{border}">
    <div style="font-family:var(--mono);font-size:8px;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin-bottom:6px">{label}</div>
    <div style="font-family:var(--sans);font-size:13px;color:var(--ink2);line-height:1.8">{thesis[key]}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="font-family:var(--mono);font-size:8px;letter-spacing:.1em;color:var(--faint);
            margin-top:28px;padding-top:16px;border-top:1px solid rgba(16,14,12,.08)">
    This memo is for illustration purposes only. Data sourced from Bloomberg, yfinance, and public filings.
    Not investment advice. Aryan S. Kothari · SKEMA Paris · March 2026
</div>
""", unsafe_allow_html=True)
