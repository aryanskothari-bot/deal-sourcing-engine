"""
pages/8_Valuation.py — Entry Valuation & IRR Model
Quick LBO/acquisition returns model with entry multiples, leverage, exit assumptions.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row
from data_sources.yfinance_loader import fetch_universe
from data_sources.static_loader import get_static_df
from modules.ranker import score_universe

st.set_page_config(page_title="Entry Valuation & IRR", page_icon="📈", layout="wide")
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

page_header("Entry Valuation &amp; <em>IRR Model</em>",
            "Acquisition entry pricing · Leverage structure · Exit assumptions · Returns analysis")

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
with st.spinner("Loading universe..."):
    try:
        raw = fetch_universe()
    except Exception:
        raw = get_static_df()
df = score_universe(raw)

# ── COMPANY SELECTOR ──────────────────────────────────────────────────────────
companies = df["Company"].tolist()
selected  = st.selectbox("Select Acquisition Target", companies, index=0)
row       = df[df["Company"] == selected].iloc[0]

st.markdown("---")

# ── ENTRY ASSUMPTIONS ─────────────────────────────────────────────────────────
sec_label("01 · Entry Assumptions")

col1, col2, col3 = st.columns(3)

# Current metrics
curr_ebitda   = float(row.get("EBITDA (€mn)") or 500)
curr_ev       = float(row.get("EV (€bn)") or 5) * 1000
curr_multiple = float(row.get("EV/EBITDA") or 10)
curr_mktcap   = float(row.get("Mkt Cap (€bn)") or 4) * 1000

with col1:
    st.markdown(f"""
    <div style="background:var(--paper2);padding:18px 20px;border:1px solid rgba(16,14,12,.08);border-top:2px solid var(--gold)">
        <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);margin-bottom:8px">Current EBITDA</div>
        <div style="font-family:var(--serif);font-size:28px;font-weight:500;color:var(--ink)">€{curr_ebitda:,.0f}mn</div>
        <div style="font-family:var(--mono);font-size:9px;color:var(--muted);margin-top:4px">LTM reported</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style="background:var(--paper2);padding:18px 20px;border:1px solid rgba(16,14,12,.08);border-top:2px solid var(--gold)">
        <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);margin-bottom:8px">Current EV</div>
        <div style="font-family:var(--serif);font-size:28px;font-weight:500;color:var(--ink)">€{curr_ev:,.0f}mn</div>
        <div style="font-family:var(--mono);font-size:9px;color:var(--muted);margin-top:4px">Market implied</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div style="background:var(--paper2);padding:18px 20px;border:1px solid rgba(16,14,12,.08);border-top:2px solid var(--gold)">
        <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);margin-bottom:8px">Current EV/EBITDA</div>
        <div style="font-family:var(--serif);font-size:28px;font-weight:500;color:var(--gold)">{curr_multiple:.1f}×</div>
        <div style="font-family:var(--mono);font-size:9px;color:var(--muted);margin-top:4px">Entry reference</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── MODEL INPUTS ──────────────────────────────────────────────────────────────
sec_label("02 · Deal Structure Inputs")

inp1, inp2, inp3 = st.columns(3)

with inp1:
    st.markdown("**Entry Parameters**")
    entry_multiple  = st.slider("Entry EV/EBITDA (×)", 4.0, 20.0, min(curr_multiple * 1.15, 18.0), 0.5)
    acq_premium_pct = st.slider("Acquisition Premium (%)", 0, 50, 20, 5)

with inp2:
    st.markdown("**Capital Structure**")
    debt_ebitda     = st.slider("Debt / EBITDA (×)", 0.0, 6.0, min(float(row.get("ND/EBITDA") or 2.0) + 1.0, 5.5), 0.25)
    cost_of_debt    = st.slider("Cost of Debt (%)", 3.0, 10.0, 5.5, 0.25)

with inp3:
    st.markdown("**Exit & Growth**")
    hold_period     = st.slider("Hold Period (years)", 3, 7, 5)
    ebitda_cagr     = st.slider("EBITDA CAGR (%)", -5, 20, 8, 1)
    exit_multiple   = st.slider("Exit EV/EBITDA (×)", 4.0, 20.0, max(entry_multiple - 1.0, 5.0), 0.5)

# ── IRR CALCULATION ───────────────────────────────────────────────────────────
entry_ev       = curr_ebitda * entry_multiple
entry_premium  = curr_mktcap * (1 + acq_premium_pct / 100)
net_debt       = float(row.get("Net Debt (€mn)") or 0)
equity_value   = max(entry_ev - net_debt, entry_ev * 0.3)
debt_amount    = curr_ebitda * debt_ebitda
equity_in      = max(entry_ev - debt_amount, entry_ev * 0.25)

exit_ebitda    = curr_ebitda * ((1 + ebitda_cagr / 100) ** hold_period)
exit_ev        = exit_ebitda * exit_multiple

# Debt paydown (simplified: 20% of FCF used to pay debt annually)
annual_fcf     = curr_ebitda * 0.55  # ~55% FCF conversion
debt_at_exit   = max(debt_amount - annual_fcf * hold_period * 0.2, 0)
equity_out     = max(exit_ev - debt_at_exit, 0)

# IRR calculation
moic           = equity_out / equity_in if equity_in > 0 else 1
irr            = (moic ** (1 / hold_period) - 1) * 100 if moic > 0 else 0

# ── RESULTS ───────────────────────────────────────────────────────────────────
st.markdown("---")
sec_label("03 · Returns Summary")

irr_color  = "var(--green)" if irr >= 20 else ("var(--gold)" if irr >= 15 else "var(--red)")
moic_color = "var(--green)" if moic >= 2.5 else ("var(--gold)" if moic >= 2.0 else "var(--red)")

metric_row([
    {"val": f"€{entry_ev:,.0f}mn",   "lbl": "Entry EV"},
    {"val": f"€{equity_in:,.0f}mn",  "lbl": "Equity Invested"},
    {"val": f"€{exit_ev:,.0f}mn",    "lbl": "Exit EV"},
    {"val": f"€{equity_out:,.0f}mn", "lbl": "Equity Proceeds"},
    {"val": f"{moic:.2f}×",          "lbl": "MOIC",  "cls": "gold" if moic >= 2.0 else "down"},
    {"val": f"{irr:.1f}%",           "lbl": "IRR",   "cls": "up"   if irr >= 20    else "down"},
])

# IRR sensitivity table
st.markdown("<br>", unsafe_allow_html=True)
sec_label("04 · IRR Sensitivity — Exit Multiple vs EBITDA CAGR")

cagr_range  = [2, 5, 8, 11, 14]
mult_range  = [exit_multiple - 2, exit_multiple - 1, exit_multiple, exit_multiple + 1, exit_multiple + 2]
mult_range  = [max(3.0, m) for m in mult_range]

z_matrix = []
for em in mult_range:
    row_irrs = []
    for cg in cagr_range:
        ex_ebitda = curr_ebitda * ((1 + cg / 100) ** hold_period)
        ex_ev     = ex_ebitda * em
        eq_out    = max(ex_ev - debt_at_exit, 0)
        _moic     = eq_out / equity_in if equity_in > 0 else 1
        _irr      = (_moic ** (1 / hold_period) - 1) * 100 if _moic > 0 else 0
        row_irrs.append(round(_irr, 1))
    z_matrix.append(row_irrs)

fig_sens = go.Figure(go.Heatmap(
    z=z_matrix,
    x=[f"{c}% CAGR" for c in cagr_range],
    y=[f"{m:.1f}× Exit" for m in mult_range],
    text=[[f"{v:.1f}%" for v in row] for row in z_matrix],
    texttemplate="%{text}",
    textfont=dict(size=11, family="DM Mono"),
    colorscale=[[0,"#8C1B1B"],[0.4,"#D5A944"],[1,"#1B4B2B"]],
    zmin=0, zmax=35,
    showscale=True,
    colorbar=dict(title="IRR %", tickfont=dict(size=10, family="DM Mono")),
))
fig_sens.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F6F1E7",
    font=dict(family="DM Mono, Courier New, monospace", color="#100E0C", size=11),
    margin=dict(l=12, r=12, t=40, b=12),
    title=dict(text=f"{selected} — IRR Sensitivity (Hold: {hold_period}y, Entry: {entry_multiple:.1f}×)",
               font=dict(size=13, family="Cormorant Garamond"), x=0),
    height=320,
    xaxis=dict(tickfont=dict(size=11, family="DM Mono")),
    yaxis=dict(tickfont=dict(size=11, family="DM Mono")),
)
st.plotly_chart(fig_sens, use_container_width=True)

# ── VALUE BRIDGE ──────────────────────────────────────────────────────────────
st.markdown("---")
sec_label("05 · Value Creation Bridge")

ebitda_growth_val = (exit_ebitda - curr_ebitda) * exit_multiple
multiple_expansion = curr_ebitda * (exit_multiple - entry_multiple)
debt_paydown_val  = debt_amount - debt_at_exit

fig_bridge = go.Figure(go.Waterfall(
    orientation="v",
    measure=["absolute","relative","relative","relative","total"],
    x=["Equity In","EBITDA Growth","Multiple Δ","Debt Paydown","Equity Out"],
    y=[equity_in, ebitda_growth_val, multiple_expansion, debt_paydown_val, 0],
    text=[f"€{equity_in:,.0f}mn", f"+€{ebitda_growth_val:,.0f}mn",
          f"{'+'if multiple_expansion>=0 else ''}€{multiple_expansion:,.0f}mn",
          f"+€{debt_paydown_val:,.0f}mn", f"€{equity_out:,.0f}mn"],
    textposition="outside",
    connector=dict(line=dict(color="rgba(16,14,12,.2)", width=1, dash="dot")),
    increasing=dict(marker=dict(color="#1B4B2B")),
    decreasing=dict(marker=dict(color="#8C1B1B")),
    totals=dict(marker=dict(color="#9B6F29")),
))
fig_bridge.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F6F1E7",
    font=dict(family="DM Mono, Courier New, monospace", color="#100E0C", size=11),
    margin=dict(l=12, r=12, t=40, b=12),
    title=dict(text=f"{selected} — Equity Value Bridge (€mn)",
               font=dict(size=13, family="Cormorant Garamond"), x=0),
    yaxis=dict(title="€mn", showgrid=True, gridcolor="rgba(16,14,12,.06)", zeroline=False,
               tickfont=dict(family="DM Mono", size=10, color="#A19890")),
    height=340, showlegend=False,
)
st.plotly_chart(fig_bridge, use_container_width=True)

st.markdown("""
<div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.15em;color:var(--faint);text-align:center;padding-top:20px;text-transform:uppercase">
    Entry Valuation &amp; IRR Model · Aryan S. Kothari · SKEMA Paris 2025 · Illustrative only — not investment advice
</div>""", unsafe_allow_html=True)
