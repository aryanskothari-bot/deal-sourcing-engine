"""
pages/5_Shortlist.py — Deal Shortlist with Excel Export.
"""
import streamlit as st
import pandas as pd
import io
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row, score_bar, pill
from data_sources.yfinance_loader import fetch_universe
from data_sources.static_loader import get_static_df
from modules.ranker import score_universe, get_pillar_scores
from utils.charts import score_bars
from config import EXPORT_FILENAME

st.set_page_config(page_title="Shortlist", page_icon="📋", layout="wide")
inject_css()

_c1,_c2,_c3,_c4,_c5,_c6,_c7 = st.columns(7)
with _c1: st.page_link("pages/1_Home.py",       label="🏠 Home",        use_container_width=True)
with _c2: st.page_link("pages/2_Screener.py",   label="🔍 Screener",    use_container_width=True)
with _c3: st.page_link("pages/3_Ranker.py",     label="🎯 Ranker",      use_container_width=True)
with _c4: st.page_link("pages/4_Financials.py", label="📊 Financials",  use_container_width=True)
with _c5: st.page_link("pages/5_Shortlist.py",  label="📋 Shortlist",   use_container_width=True)
with _c6: st.page_link("pages/6_Diligence.py",  label="🔎 Diligence",   use_container_width=True)
with _c7: st.page_link("pages/7_Signals.py",    label="📡 Signals",     use_container_width=True)
st.markdown("<hr style='margin:4px 0 16px 0;border-color:rgba(155,111,41,.25)'>", unsafe_allow_html=True)

page_header("Deal <em>Shortlist</em>", "Ranked targets · Score breakdown · Inclusion rationale · Excel export")

# ── LOAD & SCORE ──────────────────────────────────────────────────────────────
with st.spinner("Loading shortlist..."):
    try:
        raw = fetch_universe()
    except Exception:
        raw = get_static_df()
df = score_universe(raw)

# ── CONTROLS ──────────────────────────────────────────────────────────────────
col_top, col_min = st.columns([1, 1])
with col_top:
    n_targets = st.slider("Number of targets in shortlist", 3, min(12, len(df)), 5)
with col_min:
    min_score = st.slider("Minimum composite score", 0, 90, 50, step=5)

shortlist = df[df["Score"] >= min_score].head(n_targets).reset_index(drop=True)

if shortlist.empty:
    st.warning("No companies match the current filters. Lower the minimum score.")
    st.stop()

# ── SUMMARY METRICS ────────────────────────────────────────────────────────────
metric_row([
    {"val": str(len(shortlist)),                              "lbl": "Shortlisted Targets"},
    {"val": f"{shortlist['Score'].mean():.0f} / 100",       "lbl": "Avg Score",   "cls": "gold"},
    {"val": f"€{shortlist['Mkt Cap (€bn)'].median():.1f}bn","lbl": "Median Mkt Cap"},
    {"val": f"{shortlist['EV/EBITDA'].median():.1f}×",      "lbl": "Median EV/EBITDA"},
    {"val": f"{shortlist['EBITDA Margin %'].median():.1f}%", "lbl": "Median EBITDA Margin"},
])

st.markdown("---")
sec_label("Score League Table")
st.plotly_chart(score_bars(shortlist, top_n=len(shortlist)), use_container_width=True)

st.markdown("---")

# ── TARGET CARDS ──────────────────────────────────────────────────────────────
sec_label(f"Top {len(shortlist)} Acquisition Targets — Detailed View")

def _build_rationale(row, pillars):
    strengths = sorted(pillars.items(), key=lambda x: x[1], reverse=True)[:2]
    str_text  = " and ".join([f"<b>{p}</b> ({s:.0f}/100)" for p, s in strengths])
    return (
        f"{row['Company']} achieves a composite score of "
        f"<b>{row['Score']:.0f}/100</b>. Strongest pillars: {str_text}. "
        f"EV/EBITDA of {row.get('EV/EBITDA', 'N/A')}× compares favourably to sector peers. "
        f"Net leverage of {row.get('ND/EBITDA', 'N/A')}× is within conventional acquisition parameters."
    )

for rank, (_, row) in enumerate(shortlist.iterrows(), start=1):
    pillars = get_pillar_scores(row)
    expand  = rank <= 2
    label   = f"#{rank}  {row['Company']}   |   Score: {row['Score']:.0f} / 100   |   {row['Sector']}"

    with st.expander(label, expanded=expand):
        c1, c2, c3 = st.columns([1.2, 1, 1.5])

        with c1:
            pills_html = (
                pill(f"EV/EBITDA {row.get('EV/EBITDA', '—')}×",      "gold")  +
                pill(f"Margin {row.get('EBITDA Margin %', '—')}%",    "green") +
                pill(f"ND/EBITDA {row.get('ND/EBITDA', '—')}×",      "muted") +
                pill(f"€{row.get('Mkt Cap (€bn)', '—')}bn mktcap",   "muted")
            )
            st.markdown(f"""
            <div style="background:var(--paper2);padding:16px 18px;border:1px solid rgba(16,14,12,.08);margin-bottom:10px">
                <div style="font-family:var(--mono);font-size:8px;letter-spacing:.22em;text-transform:uppercase;color:var(--faint);margin-bottom:4px">#{rank} Ranked · {row['Ticker']}</div>
                <div style="font-family:var(--serif);font-size:22px;font-weight:600;color:var(--ink);margin-bottom:2px">{row['Company']}</div>
                <div style="font-family:var(--mono);font-size:8.5px;color:var(--muted)">{row['Sector']} · {row.get('Country', 'France')}</div>
            </div>
            {pills_html}
            """, unsafe_allow_html=True)

        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            for pillar, score in pillars.items():
                score_bar(pillar, score)

        with c3:
            rationale = _build_rationale(row, pillars)
            st.markdown(f"""
            <div style="background:var(--paper2);padding:14px 16px;border-left:2px solid var(--gold);margin-top:8px">
                <div style="font-family:var(--mono);font-size:8px;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin-bottom:8px">Inclusion Rationale</div>
                <div style="font-family:var(--sans);font-size:12.5px;color:var(--ink2);line-height:1.7">{rationale}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# ── EXPORT ────────────────────────────────────────────────────────────────────
sec_label("Export Shortlist")

EXPORT_COLS = [
    "Company", "Ticker", "Sector", "Country", "Score",
    "Mkt Cap (€bn)", "EV (€bn)", "Revenue (€mn)",
    "EBITDA Margin %", "Rev Growth %", "ND/EBITDA",
    "EV/EBITDA", "NTM P/E", "ROE %",
    "score_growth", "score_profitability", "score_leverage",
    "score_valuation", "score_balance_sheet", "score_size",
]
export_cols = [c for c in EXPORT_COLS if c in shortlist.columns]
export_df   = shortlist[export_cols].copy()

buf = io.BytesIO()
with pd.ExcelWriter(buf, engine="openpyxl") as writer:
    export_df.to_excel(writer, sheet_name="Shortlist",     index=False)
    df.to_excel(writer,        sheet_name="Full Universe", index=False)
buf.seek(0)

st.download_button(
    label="⬇ Download Shortlist (Excel)",
    data=buf,
    file_name=EXPORT_FILENAME,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
