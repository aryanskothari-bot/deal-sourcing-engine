"""
pages/7_Signals.py — Deal Signal Monitor
"""
import streamlit as st
import plotly.graph_objects as go
import sys, os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from ui.styles import inject_css, page_header, sec_label, metric_row, pill
from config import COLORS

st.set_page_config(page_title="Deal Signal Monitor", page_icon="📡", layout="wide")
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

page_header("Deal <em>Signal Monitor</em>",
            "Live M&A watch · Takeover filings · Stake disclosures · Strategic reviews")

SIGNALS = [
    {"date":"Mar 18, 2026","company":"Kering","ticker":"KER.PA","type":"Strategic Review","severity":"high",
     "headline":"Kering confirms strategic review of Bottega Veneta amid portfolio restructuring",
     "detail":"Board mandated review covers potential partial disposal or JV structure. Gucci revenue decline 12% YoY accelerating pressure on portfolio allocation.",
     "source":"Financial Times","tags":["Disposal","Luxury","Portfolio Review"]},
    {"date":"Mar 17, 2026","company":"Atos","ticker":"ATO.PA","type":"Restructuring","severity":"high",
     "headline":"Atos creditor group submits binding 3.2bn debt-to-equity restructuring proposal",
     "detail":"Ad hoc creditor group holding 68% of senior debt submits binding offer. Existing equity faces near-total dilution.",
     "source":"Les Echos","tags":["Debt Restructuring","Distressed","Tech"]},
    {"date":"Mar 15, 2026","company":"Vivendi","ticker":"VIV.PA","type":"Stake Disclosure","severity":"medium",
     "headline":"Vincent Bollore family vehicle discloses 26.3% stake via AMF filing",
     "detail":"Compagnie de Cornouaille crossed 25% threshold triggering mandatory AMF disclosure. Squeeze-out scenario flagged.",
     "source":"AMF Regulatory Filing","tags":["Stake Disclosure","Squeeze-Out","Media"]},
    {"date":"Mar 14, 2026","company":"Remy Cointreau","ticker":"RCO.PA","type":"M&A Rumour","severity":"medium",
     "headline":"Pernod Ricard reportedly evaluating approach to Remy Cointreau",
     "detail":"Bloomberg sources cite preliminary internal analysis by Pernod M&A team. Family holding (72%) makes unsolicited approach structurally complex.",
     "source":"Bloomberg","tags":["Takeover Approach","Spirits","Luxury Consumer"]},
    {"date":"Mar 12, 2026","company":"Ipsen","ticker":"IPN.PA","type":"Strategic Review","severity":"medium",
     "headline":"Ipsen activates strategic review process for Consumer Healthcare division",
     "detail":"Pharma-focused board opts to exit non-core OTC segment to fund oncology pipeline. Estimated division EV 600-800mn.",
     "source":"Reuters","tags":["Carve-out","Healthcare","PE Target"]},
    {"date":"Mar 11, 2026","company":"Bouygues","ticker":"EN.PA","type":"Acquisition","severity":"low",
     "headline":"Bouygues Telecom completes bolt-on acquisition of regional fibre operator for 180mn",
     "detail":"Acquisition adds 420,000 homes connectable in Normandy and Bretagne. Net leverage remains comfortable at 2.1x post-deal.",
     "source":"Bouygues Press Release","tags":["Acquisition","Telecom","Bolt-on"]},
    {"date":"Mar 10, 2026","company":"Carrefour","ticker":"CA.PA","type":"Stake Disclosure","severity":"low",
     "headline":"Norges Bank Investment Management raises Carrefour stake to 4.2%",
     "detail":"NBIM filing indicates ongoing accumulation since Q4 2025. No activist agenda disclosed.",
     "source":"AMF Regulatory Filing","tags":["Passive Stake","Retail","Institutional"]},
    {"date":"Mar 09, 2026","company":"Capgemini","ticker":"CAP.PA","type":"Acquisition","severity":"low",
     "headline":"Capgemini acquires AI consulting boutique, bolsters GenAI capabilities",
     "detail":"50-person specialist firm focused on enterprise LLM deployment. Talent acquisition rationale primary driver.",
     "source":"Capgemini IR","tags":["Acqui-hire","Tech","AI"]},
    {"date":"Mar 07, 2026","company":"bioMerieux","ticker":"BIM.PA","type":"M&A Rumour","severity":"low",
     "headline":"bioMerieux cited as potential target as US diagnostics majors survey European consolidation",
     "detail":"Jefferies flags bioMerieux as attractive M&A target given 24% EBITDA margins. Family ownership (56%) complicates hostile approach.",
     "source":"Jefferies Research","tags":["M&A Target","Healthcare","Diagnostics"]},
    {"date":"Mar 06, 2026","company":"Legrand","ticker":"LR.PA","type":"Acquisition","severity":"low",
     "headline":"Legrand acquires US smart building software provider for USD 320mn",
     "detail":"Strategic bolt-on in digital building infrastructure. Reinforces Legrand software recurring revenue strategy. Deal adds ~USD 45mn ARR at 7x revenue multiple. EV/EBITDA remains comfortable at 2.3x post-deal.",
     "source":"Legrand IR","tags":["Acquisition","Industrials","Software"]},
    {"date":"Mar 05, 2026","company":"Pernod Ricard","ticker":"RI.PA","type":"Strategic Review","severity":"medium",
     "headline":"Pernod Ricard activates portfolio review amid continued US market softness",
     "detail":"Board exploring disposal of non-core regional spirits brands. US volumes -7% in H1 FY2026. Activist pressure from Elliott Management (5.2% stake) accelerating strategic action timeline.",
     "source":"Reuters","tags":["Portfolio Review","Spirits","Activist"]},
    {"date":"Mar 03, 2026","company":"Saint-Gobain","ticker":"SGO.PA","type":"Acquisition","severity":"low",
     "headline":"Saint-Gobain completes acquisition of European insulation specialist for 450mn",
     "detail":"Acquisition strengthens Saint-Gobain high-performance solutions segment. Target generates 180mn revenue with 22% EBITDA margin. Deal EV/EBITDA of 8.5x in line with sector comps.",
     "source":"Saint-Gobain Press Release","tags":["Acquisition","Industrials","Building Materials"]},
]

with st.sidebar:
    st.markdown("### Signal Filters")
    severity_filter = st.multiselect(
        "Severity", ["high","medium","low"], default=["high","medium","low"],
        format_func=lambda x: {"high":"🔴 High","medium":"🟡 Medium","low":"🟢 Low"}[x]
    )
    type_options = sorted(set(s["type"] for s in SIGNALS))
    type_filter  = st.multiselect("Signal Type", type_options, default=type_options)
    st.markdown("---")
    st.markdown(
        f'<div style="font-family:var(--mono);font-size:8px;color:rgba(246,241,231,.4);text-transform:uppercase">Last Updated</div>'
        f'<div style="font-family:var(--mono);font-size:10px;color:rgba(213,169,68,.8);margin-top:4px">{datetime.now().strftime("%d %b %Y · %H:%M CET")}</div>',
        unsafe_allow_html=True
    )

filtered = [s for s in SIGNALS if s["severity"] in severity_filter and s["type"] in type_filter]
high_c   = sum(1 for s in filtered if s["severity"]=="high")
medium_c = sum(1 for s in filtered if s["severity"]=="medium")
low_c    = sum(1 for s in filtered if s["severity"]=="low")

metric_row([
    {"val": str(len(filtered)),  "lbl": "Active Signals"},
    {"val": str(high_c),         "lbl": "High Severity",   "cls": "down"},
    {"val": str(medium_c),       "lbl": "Medium Severity", "cls": "gold"},
    {"val": str(low_c),          "lbl": "Low Severity",    "cls": "up"},
    {"val": str(len(set(s["type"] for s in filtered))), "lbl": "Signal Types"},
])

st.markdown("---")
sec_label("Signal Heatmap by Sector")

sector_map = {
    "KER.PA": "Luxury & Consumer",
    "ATO.PA": "Technology & Media",
    "VIV.PA": "Technology & Media",
    "RCO.PA": "Luxury & Consumer",
    "IPN.PA": "Healthcare & Pharma",
    "EN.PA":  "Industrials & Engineering",
    "CA.PA":  "Retail & Distribution",
    "CAP.PA": "Technology & Media",
    "BIM.PA": "Healthcare & Pharma",
    "LR.PA":  "Industrials & Engineering",
    "RI.PA":  "Luxury & Consumer",
    "SGO.PA": "Industrials & Engineering",
}
sector_data = {}
for s in SIGNALS:
    sec = sector_map.get(s["ticker"], "Other")
    if sec not in sector_data:
        sector_data[sec] = {"high":0,"medium":0,"low":0}
    sector_data[sec][s["severity"]] += 1

sectors = sorted(sector_data.keys(), key=lambda x: sum(sector_data[x].values()), reverse=True)
highs   = [sector_data[s]["high"]   for s in sectors]
mediums = [sector_data[s]["medium"] for s in sectors]
lows    = [sector_data[s]["low"]    for s in sectors]

fig_heat = go.Figure()
fig_heat.add_trace(go.Bar(name="High",   x=sectors, y=highs,   marker_color="#8C1B1B", opacity=0.85))
fig_heat.add_trace(go.Bar(name="Medium", x=sectors, y=mediums, marker_color="#D5A944", opacity=0.85))
fig_heat.add_trace(go.Bar(name="Low",    x=sectors, y=lows,    marker_color="#1B4B2B", opacity=0.75))
fig_heat.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#F6F1E7",
    font=dict(family="DM Mono, Courier New, monospace", color="#100E0C", size=11),
    margin=dict(l=12, r=12, t=40, b=80),
    barmode="stack",
    title=dict(text="M&A Signal Distribution by Sector (Stacked by Severity)",
               font=dict(size=13, family="Cormorant Garamond"), x=0),
    xaxis=dict(tickfont=dict(size=10, family="DM Mono", color="#4B4540"), tickangle=-20),
    yaxis=dict(title="Signal Count", tickfont=dict(size=10, family="DM Mono"),
               showgrid=True, gridcolor="rgba(16,14,12,.06)", zeroline=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(size=10, family="DM Mono"),
                title_text="Severity"),
    height=360,
)
st.plotly_chart(fig_heat, use_container_width=True)

st.markdown("---")
sec_label(f"Live Signal Feed — {len(filtered)} Active Signals")

if not filtered:
    st.warning("No signals match the current filters.")
else:
    for signal in filtered:
        sev        = signal["severity"]
        sev_colour = {"high":"var(--red)","medium":"var(--gold)","low":"var(--green)"}[sev]
        sev_bg     = {"high":"rgba(140,27,27,.05)","medium":"rgba(213,169,68,.05)","low":"rgba(27,75,43,.05)"}[sev]
        sev_border = {"high":"rgba(140,27,27,.35)","medium":"rgba(213,169,68,.35)","low":"rgba(27,75,43,.25)"}[sev]
        sev_label  = {"high":"HIGH","medium":"MEDIUM","low":"LOW"}[sev]
        sev_emoji  = {"high":"🔴","medium":"🟡","low":"🟢"}[sev]
        tags_html  = " ".join([
            f'<span style="font-family:var(--mono);font-size:7px;letter-spacing:.1em;text-transform:uppercase;'
            f'padding:2px 8px;border:1px solid rgba(16,14,12,.1);color:var(--muted)">{t}</span>'
            for t in signal["tags"]
        ])
        st.markdown(f"""
<div style="border:1px solid {sev_border};border-left:3px solid {sev_colour};background:{sev_bg};padding:16px 20px;margin-bottom:10px">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
        <div style="display:flex;align-items:center;gap:10px">
            <span style="font-family:var(--mono);font-size:7px;letter-spacing:.18em;text-transform:uppercase;color:{sev_colour};border:1px solid {sev_border};padding:3px 10px">{sev_emoji} {sev_label}</span>
            <span style="font-family:var(--mono);font-size:7px;letter-spacing:.12em;text-transform:uppercase;color:var(--faint);border:1px solid rgba(16,14,12,.08);padding:3px 10px">{signal["type"]}</span>
        </div>
        <div style="text-align:right">
            <div style="font-family:var(--mono);font-size:8px;color:var(--faint)">{signal["date"]}</div>
            <div style="font-family:var(--mono);font-size:8px;color:var(--gold)">{signal["ticker"]}</div>
        </div>
    </div>
    <div style="font-family:var(--serif);font-size:15px;font-weight:600;color:var(--ink);margin-bottom:6px;line-height:1.35">{signal["company"]} — {signal["headline"]}</div>
    <div style="font-family:var(--sans);font-size:12px;color:var(--ink2);line-height:1.7;margin-bottom:10px">{signal["detail"]}</div>
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px">
        <div>{tags_html}</div>
        <div style="font-family:var(--mono);font-size:7px;letter-spacing:.1em;color:var(--faint);text-transform:uppercase">Source: {signal["source"]}</div>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div style="font-family:var(--mono);font-size:7.5px;letter-spacing:.15em;color:var(--faint);text-align:center;padding-top:20px;text-transform:uppercase">
    Deal Signal Monitor · Aryan S. Kothari · SKEMA Paris 2025 · All signals illustrative — not investment advice
</div>""", unsafe_allow_html=True)
