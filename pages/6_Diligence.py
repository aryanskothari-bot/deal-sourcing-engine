"""
pages/6_Diligence.py — FDD-Style Preliminary Diligence View
QoE analysis, adjusted EBITDA bridge, working capital, net debt, red flag panel.
"""

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row, flag_card, score_bar, status_wip, pill
from data_sources.yfinance_loader import fetch_universe
from data_sources.static_loader import get_static_df, get_static_financials
from modules.ranker import score_universe
from utils.charts import waterfall_chart
import plotly.graph_objects as go
from config import COLORS

st.set_page_config(page_title="Diligence View", page_icon="🔍", layout="wide")
inject_css()
# ─── NAV BAR ──────────────────────────────────────────────────────────────────
_c1,_c2,_c3,_c4,_c5,_c6,_c7 = st.columns(7)
with _c1: st.page_link("pages/1_Home.py",        label="🏠 Home",        use_container_width=True)
with _c2: st.page_link("pages/2_Screener.py",    label="🔍 Screener",    use_container_width=True)
with _c3: st.page_link("pages/3_Ranker.py",      label="🎯 Ranker",      use_container_width=True)
with _c4: st.page_link("pages/4_Financials.py",  label="📊 Financials",  use_container_width=True)
with _c5: st.page_link("pages/8_Valuation.py",   label="📈 Valuation",   use_container_width=True)
with _c6: st.page_link("pages/9_Benchmarking.py",label="📐 Comps",       use_container_width=True)
with _c7: st.page_link("pages/7_Signals.py",     label="📡 Signals",     use_container_width=True)
st.markdown("<hr style='margin:4px 0 16px 0;border-color:rgba(155,111,41,.25)'>", unsafe_allow_html=True)
# ──────────────────────────────────────────────────────────────────────────────


page_header(
    "Preliminary <em>Diligence View</em>",
    "Working notes — quality of earnings, normalisation, capital structure"
)

# ─── LOAD UNIVERSE ────────────────────────────────────────────────────────────
with st.spinner("Loading…"):
    try:
        raw = fetch_universe()
    except Exception:
        raw = get_static_df()
df = score_universe(raw)

# ─── COMPANY SELECTOR ─────────────────────────────────────────────────────────
companies = df["Company"].tolist()
selected  = st.selectbox("Company", companies, index=0)
row = df[df["Company"] == selected].iloc[0]
ticker = row.get("Ticker", "N/A")

st.markdown("---")

# ─── SECTION 1: QUALITY OF EARNINGS ─────────────────────────────────────────
sec_label("Quality of Earnings — normalisation adjustments")

col1, col2, col3 = st.columns(3)

# Reported EBITDA — use static financials as reliable source
_fin = get_static_financials(ticker)
_static_ebitda = _fin["ebitda"][-1] if _fin and _fin.get("ebitda") else 0
rep_ebitda = float(row.get("EBITDA (€mn)") or 0) or _static_ebitda or 1000

# QoE adjustments vary by sector — standard normalisation items
# Pharma: higher R&D reclassification, lower restructuring
# Tech/Media: heavy stock comp, one-off transformation costs
# Industrials: lease add-backs, pension normalisation
# Retail/Dist: lease adjustments dominate (IFRS 16 impact)
# Energy: decommissioning provisions, hedging gains/losses
sector = row.get("Sector", "")
if "Healthcare" in sector or "Pharma" in sector:
    mgmt_fees     =  round(rep_ebitda * 0.012, 1)   # low mgmt fees in listed pharma
    one_off_costs = -round(rep_ebitda * 0.028, 1)   # M&A transaction costs (pipeline deals)
    stock_comp    = -round(rep_ebitda * 0.031, 1)   # executive LTIPs, higher in biotech
    earn_out      =  round(rep_ebitda * 0.015, 1)   # milestone payments normalised
elif "Technology" in sector or "Media" in sector:
    mgmt_fees     =  round(rep_ebitda * 0.008, 1)   # minimal mgmt fees
    one_off_costs = -round(rep_ebitda * 0.062, 1)   # restructuring / transformation heavy
    stock_comp    = -round(rep_ebitda * 0.048, 1)   # highest stock comp in universe
    earn_out      =  round(rep_ebitda * 0.006, 1)
elif "Industrials" in sector or "Engineering" in sector:
    mgmt_fees     =  round(rep_ebitda * 0.022, 1)   # operating lease add-backs
    one_off_costs = -round(rep_ebitda * 0.035, 1)   # capex-heavy restructuring
    stock_comp    = -round(rep_ebitda * 0.014, 1)   # lower SBC than tech
    earn_out      =  round(rep_ebitda * 0.011, 1)   # project completion bonuses
elif "Retail" in sector or "Distribution" in sector:
    mgmt_fees     =  round(rep_ebitda * 0.031, 1)   # IFRS 16 lease add-back (significant)
    one_off_costs = -round(rep_ebitda * 0.021, 1)   # store closure costs
    stock_comp    = -round(rep_ebitda * 0.009, 1)   # minimal SBC
    earn_out      =  round(rep_ebitda * 0.004, 1)
elif "Energy" in sector or "Utilities" in sector:
    mgmt_fees     =  round(rep_ebitda * 0.008, 1)
    one_off_costs = -round(rep_ebitda * 0.019, 1)   # decommissioning charges
    stock_comp    = -round(rep_ebitda * 0.007, 1)
    earn_out      =  round(rep_ebitda * 0.025, 1)   # hedging gain normalisation
elif "Luxury" in sector:
    mgmt_fees     =  round(rep_ebitda * 0.014, 1)
    one_off_costs = -round(rep_ebitda * 0.038, 1)   # brand repositioning / store refits
    stock_comp    = -round(rep_ebitda * 0.018, 1)
    earn_out      =  round(rep_ebitda * 0.007, 1)
else:
    mgmt_fees     =  round(rep_ebitda * 0.015, 1)
    one_off_costs = -round(rep_ebitda * 0.035, 1)
    stock_comp    = -round(rep_ebitda * 0.020, 1)
    earn_out      =  round(rep_ebitda * 0.008, 1)
adj_ebitda = round(rep_ebitda + mgmt_fees + one_off_costs + stock_comp + earn_out, 1)
qoe_quality    = min(100, max(0, 100 - abs((adj_ebitda - rep_ebitda) / max(rep_ebitda, 1)) * 300))

with col1:
    st.markdown(f"""
    <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08);border-top:2px solid var(--gold)">
        <div style="font-family:var(--mono);font-size:8px;letter-spacing:.25em;text-transform:uppercase;color:var(--faint);margin-bottom:8px">Reported EBITDA</div>
        <div style="font-family:var(--serif);font-size:32px;font-weight:500;color:var(--ink)">€{rep_ebitda:,.0f}mn</div>
        <div style="font-family:var(--mono);font-size:9px;color:var(--muted);margin-top:4px">Last reported period</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    colour = "var(--green)" if adj_ebitda >= rep_ebitda else "var(--red)"
    diff = adj_ebitda - rep_ebitda
    sign = "+" if diff >= 0 else ""
    st.markdown(f"""
    <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08);border-top:2px solid var(--gold)">
        <div style="font-family:var(--mono);font-size:8px;letter-spacing:.25em;text-transform:uppercase;color:var(--faint);margin-bottom:8px">Adjusted EBITDA</div>
        <div style="font-family:var(--serif);font-size:32px;font-weight:500;color:{colour}">€{adj_ebitda:,.0f}mn</div>
        <div style="font-family:var(--mono);font-size:9px;color:var(--muted);margin-top:4px">{sign}{diff:,.0f}mn vs reported</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    qoe_col = "var(--green)" if qoe_quality >= 75 else ("var(--gold)" if qoe_quality >= 50 else "var(--red)")
    st.markdown(f"""
    <div style="background:var(--paper2);padding:20px 22px;border:1px solid rgba(16,14,12,.08);border-top:2px solid var(--gold)">
        <div style="font-family:var(--mono);font-size:8px;letter-spacing:.25em;text-transform:uppercase;color:var(--faint);margin-bottom:8px">QoE Score</div>
        <div style="font-family:var(--serif);font-size:32px;font-weight:500;color:{qoe_col}">{qoe_quality:.0f}/100</div>
        <div style="font-family:var(--mono);font-size:9px;color:var(--muted);margin-top:4px">Earnings quality rating</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── SECTION 2: ADJUSTED EBITDA BRIDGE ───────────────────────────────────────
sec_label("EBITDA bridge — reported to normalised")

bridge_items = [
    {"label": "Reported EBITDA",      "value": rep_ebitda,    "type": "absolute"},
    {"label": "+ Mgmt Fee Add-back",  "value": mgmt_fees,     "type": "relative"},
    {"label": "− One-off Costs",      "value": one_off_costs, "type": "relative"},
    {"label": "− Stock Compensation", "value": stock_comp,    "type": "relative"},
    {"label": "+ Earn-out Normalise", "value": earn_out,      "type": "relative"},
    {"label": "Adjusted EBITDA",      "value": adj_ebitda,    "type": "total"},
]

st.plotly_chart(waterfall_chart(bridge_items, "EBITDA Bridge — Reported to Adjusted (€mn)"), use_container_width=True)

st.markdown(f"""
<div style="background:var(--paper2);padding:14px 18px;border-left:2px solid var(--gold);margin-bottom:24px">
    <div style="font-family:var(--mono);font-size:8px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:6px">Bridge Summary</div>
    <div style="font-family:var(--sans);font-size:12.5px;color:var(--ink2);line-height:1.7">
        Reported EBITDA of <b>€{rep_ebitda:,.0f}mn</b> adjusted to <b>€{adj_ebitda:,.0f}mn</b> after normalising 
        for management fees (+€{mgmt_fees:,.0f}mn), one-off restructuring charges (€{one_off_costs:,.0f}mn), 
        stock-based compensation (€{stock_comp:,.0f}mn), and earn-out provisions (+€{earn_out:,.0f}mn). 
        Net adjustment: <b>{"+" if diff>=0 else ""}{diff:,.0f}mn ({sign}{diff/max(rep_ebitda,1)*100:.1f}%)</b>.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── SECTION 3: WORKING CAPITAL ANALYSIS ─────────────────────────────────────
sec_label("Working capital — cash conversion cycle")

revenue = row.get("Revenue (€mn)", 1000) or 1000
# Illustrative WC components (days-based)
dso   = round(45 + (row.get("EBITDA Margin %", 15) or 15) * 0.5, 0)   # days sales outstanding
dpo   = round(38 + (row.get("ND/EBITDA", 1) or 1) * 2, 0)             # days payable outstanding
dio   = round(52 - (row.get("EBITDA Margin %", 15) or 15) * 0.8, 0)   # days inventory outstanding
ccc   = dso + dio - dpo                                                  # cash conversion cycle
nwc   = round(revenue * ccc / 365, 1)

wc_col1, wc_col2, wc_col3, wc_col4 = st.columns(4)
wc_metrics = [
    (wc_col1, "DSO (Days)", f"{dso:.0f}d", "Receivables collection"),
    (wc_col2, "DPO (Days)", f"{dpo:.0f}d", "Payables payment"),
    (wc_col3, "DIO (Days)", f"{dio:.0f}d", "Inventory holding"),
    (wc_col4, "Cash Conv. Cycle", f"{ccc:.0f}d", "DSO + DIO − DPO"),
]
for col, label, val, sub in wc_metrics:
    with col:
        colour = "var(--green)" if (label == "DPO (Days)") else ("var(--red)" if ccc > 60 and label == "Cash Conv. Cycle" else "var(--ink)")
        st.markdown(f"""
        <div style="background:var(--paper2);padding:16px 18px;border:1px solid rgba(16,14,12,.07)">
            <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);margin-bottom:6px">{label}</div>
            <div style="font-family:var(--serif);font-size:26px;font-weight:500;color:{colour}">{val}</div>
            <div style="font-family:var(--mono);font-size:8px;color:var(--muted);margin-top:3px">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f"""
<div style="margin-top:16px;background:var(--paper2);padding:14px 18px;border-left:2px solid {'var(--red)' if ccc > 60 else 'var(--green)'}">
    <div style="font-family:var(--sans);font-size:12.5px;color:var(--ink2);line-height:1.7">
        Net Working Capital requirement: <b>€{nwc:,.0f}mn</b> ({ccc:.0f} days of revenue). 
        {'⚠ Extended cash conversion cycle may indicate liquidity pressure or collection risk.' if ccc > 60 else '✓ Working capital cycle is within acceptable parameters.'}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── SECTION 4: NET DEBT ANALYSIS ────────────────────────────────────────────
sec_label("Net debt & capital structure")

net_debt  = row.get("Net Debt (€mn)", 0) or 0
nd_ebitda = row.get("ND/EBITDA", 0) or 0
ev        = (row.get("EV (€bn)", 0) or 0) * 1000
mktcap    = (row.get("Mkt Cap (€bn)", 0) or 0) * 1000

# Illustrative debt components
gross_debt   = round(net_debt * 1.22, 0)
cash         = round(gross_debt - net_debt, 0)
lease_liab   = round(net_debt * 0.18, 0)
eco_nd       = net_debt + lease_liab

nd_col1, nd_col2, nd_col3, nd_col4 = st.columns(4)
nd_metrics = [
    (nd_col1, "Net Debt",         f"€{net_debt:,.0f}mn",  "Gross debt − cash"),
    (nd_col2, "ND/EBITDA",        f"{nd_ebitda:.2f}×",    "Leverage ratio"),
    (nd_col3, "IFRS 16 Leases",   f"€{lease_liab:,.0f}mn","Operating lease obligations"),
    (nd_col4, "Economic Net Debt",f"€{eco_nd:,.0f}mn",    "Net debt incl. IFRS 16"),
]
for col, label, val, sub in nd_metrics:
    with col:
        lev_colour = "var(--red)" if nd_ebitda > 4 else ("var(--gold)" if nd_ebitda > 2.5 else "var(--green)")
        colour = lev_colour if "EBITDA" in label else "var(--ink)"
        st.markdown(f"""
        <div style="background:var(--paper2);padding:16px 18px;border:1px solid rgba(16,14,12,.07)">
            <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);margin-bottom:6px">{label}</div>
            <div style="font-family:var(--serif);font-size:22px;font-weight:500;color:{colour}">{val}</div>
            <div style="font-family:var(--mono);font-size:8px;color:var(--muted);margin-top:3px">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ─── SECTION 5: RED FLAG PANEL ────────────────────────────────────────────────
sec_label("Key risks to flag before LOI")

# Generate flags based on actual metrics
flags = []

if nd_ebitda > 5:
    flags.append(("High Leverage Risk", f"ND/EBITDA of {nd_ebitda:.1f}× exceeds conventional acquisition parameters (>5×). Debt service capacity may be constrained under stress scenarios.", "high"))
elif nd_ebitda > 3:
    flags.append(("Elevated Leverage", f"ND/EBITDA of {nd_ebitda:.1f}× is above mid-market comfort zone (2.5–3×). Monitor covenant headroom and refinancing timeline.", "medium"))
else:
    flags.append(("Leverage Within Parameters", f"ND/EBITDA of {nd_ebitda:.1f}× is within conventional acquisition parameters. Balance sheet supports deal structure.", "low"))

margin = row.get("EBITDA Margin %", 0) or 0
if margin < 5:
    flags.append(("Thin Profitability", f"EBITDA margin of {margin:.1f}% leaves limited buffer for cost inflation or revenue shortfall. QoE adjustments may compress margin further.", "high"))
elif margin < 12:
    flags.append(("Below-Average Margin", f"EBITDA margin of {margin:.1f}% is below sector median. Identify margin improvement levers before LOI.", "medium"))
else:
    flags.append(("Healthy Profitability", f"EBITDA margin of {margin:.1f}% provides adequate buffer. Verify sustainability vs. one-off items.", "low"))

growth = row.get("Rev Growth %", 0) or 0
if growth < -10:
    flags.append(("Significant Revenue Decline", f"Revenue contracted {growth:.1f}% YoY. Requires detailed volume/price/mix analysis and market share assessment.", "high"))
elif growth < 0:
    flags.append(("Revenue Contraction", f"Revenue declined {growth:.1f}% YoY. Identify structural vs. cyclical drivers. Verify pipeline/backlog.", "medium"))
else:
    flags.append(("Positive Revenue Momentum", f"Revenue grew {growth:.1f}% YoY. Validate sustainability of growth drivers and customer concentration.", "low"))

cr = row.get("Current Ratio", 0) or 0
if cr < 0.8:
    flags.append(("Liquidity Risk", f"Current ratio of {cr:.2f}× signals potential short-term liquidity pressure. Review revolving credit facility and cash runway.", "high"))
elif cr < 1.2:
    flags.append(("Tight Liquidity", f"Current ratio of {cr:.2f}× is below comfortable threshold (>1.2×). Monitor working capital cycle closely.", "medium"))
else:
    flags.append(("Adequate Liquidity", f"Current ratio of {cr:.2f}× indicates sufficient short-term coverage.", "low"))

if ccc > 70:
    flags.append(("Extended Cash Conversion Cycle", f"CCC of {ccc:.0f} days is above sector norms. Investigate receivables ageing and inventory obsolescence.", "medium"))

if abs(diff / max(rep_ebitda, 1)) > 0.08:
    flags.append(("Material QoE Adjustments", f"Adjusted EBITDA differs from reported by {abs(diff/max(rep_ebitda,1))*100:.1f}%. Scrutinise normalisation assumptions with management.", "medium"))

# Sort: high → medium → low
order = {"high": 0, "medium": 1, "low": 2}
flags.sort(key=lambda x: order[x[2]])

high_count   = sum(1 for f in flags if f[2] == "high")
medium_count = sum(1 for f in flags if f[2] == "medium")
low_count    = sum(1 for f in flags if f[2] == "low")

st.markdown(f"""
<div style="display:flex;gap:12px;margin-bottom:20px">
    <div style="font-family:var(--mono);font-size:8px;letter-spacing:.15em;text-transform:uppercase;padding:6px 14px;border:1px solid rgba(140,27,27,.4);background:rgba(140,27,27,.06);color:var(--red)">
        🔴 {high_count} HIGH
    </div>
    <div style="font-family:var(--mono);font-size:8px;letter-spacing:.15em;text-transform:uppercase;padding:6px 14px;border:1px solid rgba(213,169,68,.4);background:rgba(213,169,68,.06);color:var(--gold)">
        🟡 {medium_count} MEDIUM
    </div>
    <div style="font-family:var(--mono);font-size:8px;letter-spacing:.15em;text-transform:uppercase;padding:6px 14px;border:1px solid rgba(27,75,43,.4);background:rgba(27,75,43,.06);color:var(--green)">
        🟢 {low_count} LOW
    </div>
</div>
""", unsafe_allow_html=True)

for title, desc, severity in flags:
    flag_card(title, desc, severity)

st.markdown("---")

# ─── FOOTER DISCLAIMER ───────────────────────────────────────────────────────
st.markdown(f"""
<div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.12em;color:var(--faint);text-align:center;padding-top:20px;border-top:1px solid rgba(16,14,12,.07)">
    QoE adjustments are illustrative — based on sector-typical normalisation items, not company-specific audit findings.
    Verify against full annual report and management accounts before LOI. · Data: Bloomberg, company filings, yfinance · March 2026 ·
    Aryan S. Kothari · SKEMA Paris · Not investment advice.
</div>
""", unsafe_allow_html=True)
