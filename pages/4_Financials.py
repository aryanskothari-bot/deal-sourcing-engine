"""
pages/4_📊_Financials.py — Financial Statement Standardisation.
5-year IS history, common-size, key ratios, trend charts.
"""

import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row
from data_sources.yfinance_loader import fetch_universe, fetch_financials
from data_sources.static_loader import get_static_df
from modules.ranker import score_universe
from utils.charts import financials_bar, margin_line

st.set_page_config(page_title="Financials", page_icon="📊", layout="wide")
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
# ──────────────────────────────────────────────────────────────────────────────


nav_bar("Financials")

page_header("Financial Statement <em>Standardisation</em>", "5-year IS history · Common-size · Key ratios · Trend charts")

# ─── LOAD UNIVERSE ────────────────────────────────────────────────────────────
with st.spinner("Loading…"):
    try:
        raw = fetch_universe()
    except Exception:
        raw = get_static_df()
df = score_universe(raw)

# ─── COMPANY SELECTOR ────────────────────────────────────────────────────────
companies = df["Company"].tolist()
selected  = st.selectbox("Select Company", companies, index=0)
ticker    = df[df["Company"] == selected]["Ticker"].values[0]

# ─── LOAD FINANCIALS ─────────────────────────────────────────────────────────
with st.spinner(f"Loading financials for {selected}…"):
    fin = fetch_financials(ticker)

if not fin:
    st.error("Financials unavailable for this company.")
    st.stop()

years      = fin["years"]
revenue    = fin["revenue"]
ebitda     = fin["ebitda"]
ebit       = fin["ebit"]
net_income = fin["net_income"]
em         = fin["ebitda_margin"]
im         = fin["ebit_margin"]

# ─── SUMMARY METRICS ─────────────────────────────────────────────────────────
latest_rev  = revenue[-1]  if revenue  else 0
latest_em   = em[-1]       if em       else 0
latest_ni   = net_income[-1] if net_income else 0
rev_cagr    = ((revenue[-1] / revenue[0]) ** (1 / max(len(years) - 1, 1)) - 1) * 100 if revenue[0] else 0

metric_row([
    {"val": f"€{latest_rev/1000:.1f}bn",          "lbl": f"FY{years[-1]} Revenue"},
    {"val": f"{latest_em:.1f}%",                  "lbl": "EBITDA Margin", "cls": "gold"},
    {"val": f"€{latest_ni/1000:.1f}bn",           "lbl": "Net Income"},
    {"val": f"{rev_cagr:+.1f}%",                  "lbl": f"{years[0]}–{years[-1]} Rev CAGR", "cls": "up" if rev_cagr >= 0 else "down"},
])

st.markdown("---")

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["Income Statement", "Common-Size IS", "Ratio Analysis"])

with tab1:
    sec_label("Standardised Income Statement (€mn)")
    is_data = {
        "Metric":       ["Revenue", "EBITDA", "EBIT", "Net Income"],
    }
    for i, yr in enumerate(years):
        is_data[str(yr)] = [
            f"€{revenue[i]:,.0f}"    if i < len(revenue)    else "N/A",
            f"€{ebitda[i]:,.0f}"     if i < len(ebitda)     else "N/A",
            f"€{ebit[i]:,.0f}"       if i < len(ebit)       else "N/A",
            f"€{net_income[i]:,.0f}" if i < len(net_income) else "N/A",
        ]
    st.dataframe(pd.DataFrame(is_data), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(financials_bar(years, revenue, ebitda, selected), use_container_width=True)
    with col2:
        st.plotly_chart(margin_line(years, em, im, selected), use_container_width=True)

with tab2:
    sec_label("Common-Size Income Statement (% of Revenue)")
    def pct(lst, base):
        return [f"{v/b*100:.1f}%" if b else "N/A" for v, b in zip(lst, base)]

    cs_data = {"Metric": ["Revenue", "EBITDA %", "EBIT %", "Net Income %"]}
    for i, yr in enumerate(years):
        rev = revenue[i] if i < len(revenue) else 1
        cs_data[str(yr)] = [
            "100.0%",
            f"{ebitda[i]/rev*100:.1f}%"     if i < len(ebitda)     else "N/A",
            f"{ebit[i]/rev*100:.1f}%"        if i < len(ebit)       else "N/A",
            f"{net_income[i]/rev*100:.1f}%"  if i < len(net_income) else "N/A",
        ]
    st.dataframe(pd.DataFrame(cs_data), use_container_width=True, hide_index=True)

with tab3:
    sec_label("Key Financial Ratios")
    row = df[df["Company"] == selected].iloc[0]
    ratios = {
        "EV/EBITDA":        f"{row.get('EV/EBITDA', 'N/A'):.1f}×" if pd.notna(row.get('EV/EBITDA')) else "N/A",
        "EV/Revenue":       f"{row.get('EV/Revenue', 'N/A'):.2f}×" if pd.notna(row.get('EV/Revenue')) else "N/A",
        "NTM P/E":          f"{row.get('NTM P/E', 'N/A'):.1f}×"   if pd.notna(row.get('NTM P/E'))    else "N/A",
        "ND/EBITDA":        f"{row.get('ND/EBITDA', 'N/A'):.2f}×"  if pd.notna(row.get('ND/EBITDA'))  else "N/A",
        "EBITDA Margin":    f"{row.get('EBITDA Margin %', 0):.1f}%",
        "ROE":              f"{row.get('ROE %', 0):.1f}%",
        "ROIC":             f"{row.get('ROIC %', 0):.1f}%" if pd.notna(row.get('ROIC %')) else "N/A",
        "Current Ratio":    f"{row.get('Current Ratio', 0):.2f}×"  if pd.notna(row.get('Current Ratio')) else "N/A",
    }
    metric_row([
        {"val": v, "lbl": k}
        for k, v in list(ratios.items())[:5]
    ])
    metric_row([
        {"val": v, "lbl": k}
        for k, v in list(ratios.items())[5:]
    ])
