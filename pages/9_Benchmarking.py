"""
pages/9_Benchmarking.py — Comparable Companies Benchmarking
Sector peer table with quartile positioning, ranking, and gap analysis.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row
from data_sources.yfinance_loader import fetch_universe
from data_sources.static_loader import get_static_df
from modules.ranker import score_universe

st.set_page_config(page_title="Peer Benchmarking", page_icon="📐", layout="wide")
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

page_header("Comparable Companies <em>Benchmarking</em>",
            "How does this company look against its peer group?")

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
with st.spinner("Loading universe..."):
    try:
        raw = fetch_universe()
    except Exception:
        raw = get_static_df()
df = score_universe(raw)

# ── SELECTORS ─────────────────────────────────────────────────────────────────
sel_col, sec_col = st.columns([1, 1])
with sel_col:
    selected = st.selectbox("Company", df["Company"].tolist(), index=0)
with sec_col:
    all_sectors = ["All Sectors"] + sorted(df["Sector"].dropna().unique().tolist())
    target_sector = df[df["Company"]==selected]["Sector"].values[0]
    sector_filter = st.selectbox("Peer Sector", all_sectors,
                                  index=all_sectors.index(target_sector) if target_sector in all_sectors else 0)

row = df[df["Company"] == selected].iloc[0]
peers = df[df["Sector"] == sector_filter].copy() if sector_filter != "All Sectors" else df.copy()
peers_excl = peers[peers["Company"] != selected]

st.markdown("---")

# ── POSITIONING METRICS ───────────────────────────────────────────────────────
sec_label(f"01 · {selected} vs {sector_filter} Peers")

METRICS = [
    ("EV/EBITDA",       "EV/EBITDA (×)",      "lower_better"),
    ("EBITDA Margin %", "EBITDA Margin (%)",   "higher_better"),
    ("Rev Growth %",    "Revenue Growth (%)",  "higher_better"),
    ("ND/EBITDA",       "ND/EBITDA (×)",       "lower_better"),
    ("Score",           "Acquisition Score",   "higher_better"),
]

def quartile_label(val, series, higher_better):
    if pd.isna(val): return "N/A", "var(--muted)"
    q25, q50, q75 = series.quantile([0.25, 0.5, 0.75])
    if higher_better:
        if val >= q75: return "Top Quartile", "var(--green)"
        if val >= q50: return "Above Median", "var(--gold)"
        if val >= q25: return "Below Median", "var(--muted)"
        return "Bottom Quartile", "var(--red)"
    else:
        if val <= q25: return "Top Quartile", "var(--green)"
        if val <= q50: return "Above Median", "var(--gold)"
        if val <= q75: return "Below Median", "var(--muted)"
        return "Bottom Quartile", "var(--red)"

cards = st.columns(len(METRICS))
for col, (col_key, label, direction) in zip(cards, METRICS):
    val = row.get(col_key)
    series = peers[col_key].dropna()
    qlabel, qcolor = quartile_label(val, series, direction == "higher_better")
    median = series.median()
    with col:
        val_display = f"{val:.1f}" if pd.notna(val) else "N/A"
        suffix = "×" if "EBITDA" in col_key and "Margin" not in col_key else ("%" if "%" in col_key or "Growth" in col_key else "")
        st.markdown(f"""
        <div style="background:var(--paper2);padding:14px 16px;border:1px solid rgba(16,14,12,.08);border-top:2px solid {qcolor}">
            <div style="font-family:var(--mono);font-size:7px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);margin-bottom:6px">{label}</div>
            <div style="font-family:var(--serif);font-size:22px;font-weight:500;color:var(--ink)">{val_display}{suffix}</div>
            <div style="font-family:var(--mono);font-size:8px;color:var(--muted);margin-top:2px">Peer median: {median:.1f}{suffix}</div>
            <div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.1em;color:{qcolor};margin-top:4px">{qlabel}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── FULL PEER TABLE ───────────────────────────────────────────────────────────
sec_label("02 · Full Comparable Companies Table")

SHOW_COLS = ["Company","Sector","Mkt Cap (€bn)","EV (€bn)","EV/EBITDA",
             "EBITDA Margin %","Rev Growth %","ND/EBITDA","NTM P/E","Score"]
show_cols = [c for c in SHOW_COLS if c in peers.columns]
peer_table = peers[show_cols].copy().sort_values("Score", ascending=False).reset_index(drop=True)
peer_table.index = peer_table.index + 1

# Highlight the selected company
def highlight_target(row):
    if row["Company"] == selected:
        return ["background-color: rgba(155,111,41,0.08); font-weight:600"] * len(row)
    return [""] * len(row)

styled = peer_table.style.apply(highlight_target, axis=1).format({
    "Mkt Cap (€bn)": "{:.1f}",
    "EV (€bn)": "{:.1f}",
    "EV/EBITDA": "{:.1f}",
    "EBITDA Margin %": "{:.1f}%",
    "Rev Growth %": "{:.1f}%",
    "ND/EBITDA": "{:.2f}",
    "NTM P/E": "{:.1f}",
    "Score": "{:.0f}",
}, na_rep="N/A")

st.dataframe(styled, use_container_width=True, height=min(60 + len(peer_table) * 36, 520))

st.markdown("---")

# ── VISUAL BENCHMARKING CHARTS ────────────────────────────────────────────────
sec_label("03 · Visual Benchmarking")

ch1, ch2 = st.columns(2)

# Chart 1: EV/EBITDA vs Margin scatter
with ch1:
    dfc = peers.dropna(subset=["EV/EBITDA","EBITDA Margin %"])
    colors = ["#D5A944" if c == selected else "#4B4540" for c in dfc["Company"]]
    sizes  = [16 if c == selected else 8 for c in dfc["Company"]]

    fig1 = go.Figure()
    # Peers
    peer_df = dfc[dfc["Company"] != selected]
    fig1.add_trace(go.Scatter(
        x=peer_df["EBITDA Margin %"], y=peer_df["EV/EBITDA"],
        mode="markers+text", text=peer_df["Company"],
        textposition="top center", textfont=dict(size=8, family="DM Mono", color="#7B7368"),
        marker=dict(size=8, color="#4B4540", opacity=0.7),
        name="Peers",
    ))
    # Target
    tgt = dfc[dfc["Company"] == selected]
    if len(tgt) > 0:
        fig1.add_trace(go.Scatter(
            x=tgt["EBITDA Margin %"], y=tgt["EV/EBITDA"],
            mode="markers+text", text=tgt["Company"],
            textposition="top center", textfont=dict(size=10, family="DM Mono", color="#9B6F29", weight=700),
            marker=dict(size=16, color="#D5A944", symbol="star"),
            name=selected,
        ))
    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F6F1E7",
        font=dict(family="DM Mono", color="#100E0C", size=10),
        margin=dict(l=12, r=12, t=40, b=12),
        title=dict(text="EV/EBITDA vs EBITDA Margin — Peer Map",
                   font=dict(size=12, family="Cormorant Garamond"), x=0),
        xaxis=dict(title="EBITDA Margin %", showgrid=True, gridcolor="rgba(16,14,12,.06)", zeroline=False),
        yaxis=dict(title="EV/EBITDA", showgrid=True, gridcolor="rgba(16,14,12,.06)", zeroline=False),
        legend=dict(font=dict(size=9, family="DM Mono")),
        height=360,
    )
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Score ranking bar
with ch2:
    rank_df = peers[["Company","Score","Sector"]].dropna(subset=["Score"]).sort_values("Score")
    bar_colors = ["#D5A944" if c == selected else "#4B4540" for c in rank_df["Company"]]
    fig2 = go.Figure(go.Bar(
        x=rank_df["Score"], y=rank_df["Company"], orientation="h",
        marker_color=bar_colors,
        text=rank_df["Score"].round(0).astype(int),
        textposition="outside",
        textfont=dict(family="DM Mono", size=9),
    ))
    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F6F1E7",
        font=dict(family="DM Mono", color="#100E0C", size=10),
        margin=dict(l=12, r=12, t=40, b=12),
        title=dict(text="Acquisition Score Ranking — Sector Peers",
                   font=dict(size=12, family="Cormorant Garamond"), x=0),
        xaxis=dict(range=[0,110], title="Score", showgrid=True, gridcolor="rgba(16,14,12,.06)", zeroline=False),
        yaxis=dict(tickfont=dict(size=10, family="DM Mono")),
        height=360, showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── QUARTILE SUMMARY TABLE ────────────────────────────────────────────────────
sec_label("04 · Peer Statistics Summary")

stats_rows = []
for col_key, label, direction in METRICS:
    if col_key not in peers.columns: continue
    s = peers[col_key].dropna()
    val = row.get(col_key)
    ql, _ = quartile_label(val, s, direction == "higher_better")
    stats_rows.append({
        "Metric":        label,
        "Target":        f"{val:.1f}" if pd.notna(val) else "N/A",
        "Peer Min":      f"{s.min():.1f}",
        "Peer Q1 (25%)": f"{s.quantile(0.25):.1f}",
        "Peer Median":   f"{s.median():.1f}",
        "Peer Q3 (75%)": f"{s.quantile(0.75):.1f}",
        "Peer Max":      f"{s.max():.1f}",
        "Positioning":   ql,
    })
st.dataframe(pd.DataFrame(stats_rows), use_container_width=True, hide_index=True)

st.markdown("""
<div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.15em;color:var(--faint);text-align:center;padding-top:20px;text-transform:uppercase">
    Peer Benchmarking · Aryan S. Kothari · SKEMA Paris 2025 · Illustrative — not investment advice
</div>""", unsafe_allow_html=True)
