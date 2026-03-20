"""
# v2.1 — shortlist fix

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
with _c1: st.page_link("pages/0_About.py",       label="📝 About",      use_container_width=True)
with _c2: st.page_link("pages/2_Screener.py",    label="🔍 Screener",   use_container_width=True)
with _c3: st.page_link("pages/3_Ranker.py",      label="🎯 Ranker",     use_container_width=True)
with _c4: st.page_link("pages/4_Financials.py",  label="📊 Financials", use_container_width=True)
with _c5: st.page_link("pages/8_Valuation.py",   label="📈 Valuation",  use_container_width=True)
with _c6: st.page_link("pages/9_Benchmarking.py",label="📐 Comps",      use_container_width=True)
with _c7: st.page_link("pages/7_Signals.py",     label="📡 Signals",    use_container_width=True)
st.markdown("<hr style='margin:4px 0 16px 0;border-color:rgba(155,111,41,.25)'>", unsafe_allow_html=True)

page_header("Deal <em>Shortlist</em>", "My current target list — with analyst notes on why each one is in or out")

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

# Company-specific analyst notes — written per target, not templated
_ANALYST_NOTES = {
    "Ipsen": (
        "Ipsen is the clearest buy case in this universe. Net cash position (ND/EBITDA -0.5×) means an acquirer "
        "pays almost nothing for balance sheet risk. The oncology pipeline — Cabometyx, Somatuline — generates "
        "genuinely recurring revenue. Management are executing a disciplined portfolio exit of OTC (€600-800mn "
        "estimated proceeds) which should release capital for reinvestment or return. At 6.4× EV/EBITDA this is "
        "cheap for a pharma with 34% EBITDA margins. Only risk: family block and any regulatory overhang on "
        "Somatuline biosimilar competition post-2027."
    ),
    "Vallourec": (
        "Vallourec is a turnaround story that has actually turned. Steel pipes for oil & gas, restructured through "
        "Covid, now generating meaningful FCF. At 2.9× EV/EBITDA it trades at a significant discount to OCTG peers. "
        "The Brazilian operations are the real value — high-margin premium connections. Risk is commodity cycle "
        "exposure and any reversal in oil capex. But at this multiple the downside is limited and there is strategic "
        "logic for a trade buyer (TenarisOil & Gas services consolidation wave)."
    ),
    "bioMerieux": (
        "bioMerieux is a quietly exceptional business — 24% EBITDA margins in diagnostics, family-controlled "
        "(Institut Merieux 56%), recurring reagent revenue model. The Covid diagnostics boom inflated 2022 numbers "
        "but the base business was already compounding at 6-8% organically. The family holding makes an unsolicited "
        "approach structurally impossible, but a negotiated premium transaction with management alignment is "
        "achievable. Comparable: Qiagen 2020 deal at 11× EV/EBITDA — bioMerieux at 10.6× is not expensive."
    ),
    "Capgemini": (
        "Capgemini is the IT services consolidator, not a target. But at 7.7× EV/EBITDA with 14% margins and "
        "meaningful AI exposure (Invent unit growing 18% YoY), it screens better than most defensive tech names. "
        "The risk is that IT services multiples compress as AI commoditises lower-value delivery. Worth watching "
        "but not a conviction buy at current prices. More interesting as a comps reference than a primary target."
    ),
    "Vivendi": (
        "Vivendi post-Canal+ demerger is essentially a media holding company trading at a 35%+ NAV discount. "
        "Havas (advertising), CNews, Prisma Media — none of these individually justify the complexity premium. "
        "The Bollore family stake (26%+) is the wildcard. A sum-of-parts trade makes academic sense; executing "
        "it against a controlling family shareholder is another matter. Include on the watchlist, not the shortlist."
    ),
    "Legrand": (
        "Legrand is probably the most consistently excellent industrial in France — 25% EBITDA margins, "
        "30%+ ROIC, M&A machine with 100+ acquisitions completed. The problem is valuation: 9.7× EV/EBITDA "
        "for an industrial is not cheap. A strategic buyer (Schneider, ABB) could justify a premium through "
        "synergy, but a financial buyer struggles to make the returns work. Better as a benchmarking reference "
        "than a primary target at current entry prices."
    ),
    "Sanofi": (
        "Sanofi is too large for a conventional M&A transaction (€118bn EV) but relevant as a divestiture "
        "source. The Opella consumer health spin-off process (Doliprane, Essentiale) is worth tracking — "
        "estimated EV €15-18bn, 8-10× EBITDA. That carve-out is a much more interesting entry point than "
        "the parent. Flag for Phase 2 scope when we extend to sub-division level assets."
    ),
    "Bouygues": (
        "Bouygues is a conglomerate discount story — construction + telecom + media under one roof. "
        "Sum-of-parts suggests 20-30% upside to current market cap, but the discount has been structural "
        "for 15 years. Telecom (Bouygues Telecom) is the most attractive asset in isolation; construction "
        "margins are thin but cash generative. Dividend yield (5%+) keeps institutional holders passive. "
        "A private equity sponsored breakup is logistically possible but family governance makes it unlikely."
    ),
    "Saint-Gobain": (
        "Saint-Gobain has re-rated significantly post-Compagnie de Saint-Gobain transformation — divested "
        "distribution, focused on high-performance materials. Margins have structurally improved (12% EBITDA "
        "vs 8% five years ago). Trading at 5.5× which still looks inexpensive for the quality of the "
        "remaining business. A trade buyer in building materials (Kingspan, Owens Corning) could extract "
        "meaningful synergies. The balance sheet (1.0× ND/EBITDA) gives flexibility."
    ),
    "Eurofins": (
        "Eurofins is a roll-up — labs, testing, certifications — that got caught in a short-seller attack "
        "in 2019 and has never fully recovered investor trust. The underlying business is good: 22% margins, "
        "recurring revenue from food/pharma testing mandates. Leverage at 2.9× is manageable but limits "
        "financial buyer optionality. A strategic acquirer with balance sheet capacity (SGS, Bureau Veritas) "
        "could de-lever quickly through synergy. Watch the Gilles Martin founder stake (15%) — he will not "
        "accept a lowball offer."
    ),
}

def _build_rationale(row, pillars):
    company = row["Company"]
    # Use hand-written note if available
    if company in _ANALYST_NOTES:
        return _ANALYST_NOTES[company]
    # Fallback — still more natural than the template
    strengths = sorted(pillars.items(), key=lambda x: x[1], reverse=True)[:2]
    weaknesses = sorted(pillars.items(), key=lambda x: x[1])[:1]
    ev_eb = row.get("EV/EBITDA", 0)
    nd = row.get("ND/EBITDA", 0)
    margin = row.get("EBITDA Margin %", 0)
    top_pillar, top_score = strengths[0]
    weak_pillar, weak_score = weaknesses[0]
    return (
        f"Scores {row['Score']:.0f}/100 — strongest on {top_pillar} ({top_score:.0f}), "
        f"which is the primary inclusion driver. At {ev_eb:.1f}× EV/EBITDA with {margin:.0f}% EBITDA margins "
        f"and {nd:.1f}× net leverage, the entry case is {'straightforward' if nd < 2.5 else 'leveraged but manageable'}. "
        f"Watch {weak_pillar} ({weak_score:.0f}/100) — this is the main diligence focus before LOI."
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
