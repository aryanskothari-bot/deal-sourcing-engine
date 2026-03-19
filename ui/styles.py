"""
styles.py — Global CSS for the Deal Sourcing Engine Streamlit app.
Matches the portfolio site's editorial aesthetic: warm ivory, gold accents, DM Mono.
"""

import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,600&family=DM+Mono:wght@300;400;500&family=Jost:wght@300;400;500;600&display=swap');

    /* ── ROOT PALETTE ── */
    :root {
        --paper:  #F6F1E7;
        --paper2: #EEE7D7;
        --paper3: #E5DBCB;
        --ink:    #100E0C;
        --ink2:   #2B2520;
        --muted:  #7B7368;
        --faint:  #A19890;
        --gold:   #9B6F29;
        --gold2:  #B98533;
        --gold3:  #D5A944;
        --green:  #1B4B2B;
        --red:    #8C1B1B;
        --eng-bg: #0D2518;
        --serif:  'Cormorant Garamond', Georgia, serif;
        --mono:   'DM Mono', 'Courier New', monospace;
        --sans:   'Jost', 'Helvetica Neue', sans-serif;
    }

    /* ── GLOBAL ── */
    html, body, [class*="css"] {
        font-family: var(--sans) !important;
        background-color: var(--paper) !important;
        color: var(--ink) !important;
    }

    /* ── HIDE STREAMLIT DEFAULT CHROME ── */
    #MainMenu { visibility: hidden; } footer { visibility: hidden; } [data-testid="stToolbar"] { display: none !important; } [data-testid="stMainMenu"] { display: flex !important; visibility: visible !important; } [data-testid="stMainMenuButton"] { visibility: visible !important; }
    .block-container { padding-top: 1.8rem !important; padding-bottom: 2rem !important; max-width: 1320px !important; } [data-testid="stSidebarCollapsedControl"] { visibility: visible !important; display: flex !important; opacity: 1 !important; } [data-testid="collapsedControl"] { visibility: visible !important; display: flex !important; }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: var(--eng-bg) !important;
        border-right: 1px solid rgba(213,169,68,.18) !important;
    }
    [data-testid="stSidebar"] * { color: rgba(246,241,231,.75) !important; }

    [data-testid="stSidebar"] .stMarkdown h3 {
        font-family: var(--mono) !important;
        font-size: 8px !important;
        letter-spacing: .3em !important;
        text-transform: uppercase !important;
        color: var(--gold3) !important;
        margin-bottom: 10px !important;
        padding-bottom: 8px !important;
        border-bottom: 1px solid rgba(213,169,68,.2) !important;
    }
    [data-testid="stSidebar"] label {
        font-family: var(--mono) !important;
        font-size: 9px !important;
        letter-spacing: .18em !important;
        text-transform: uppercase !important;
        color: rgba(246,241,231,.45) !important;
    }
    [data-testid="stSidebar"] .stSlider > div > div {
        background: rgba(213,169,68,.25) !important;
    }
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [role="slider"] {
        background: var(--gold3) !important;
        border-color: var(--gold3) !important;
    }
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background: rgba(255,255,255,.06) !important;
        border-color: rgba(213,169,68,.25) !important;
    }
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] * {
        color: rgba(246,241,231,.75) !important;
        background: var(--eng-bg) !important;
    }

    /* ── TOP HEADER ── */
    .eng-header {
        background: var(--eng-bg);
        padding: 22px 32px 18px;
        border-bottom: 1px solid rgba(213,169,68,.2);
        margin-bottom: 28px;
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 16px;
    }
    .eng-header-title {
        font-family: var(--serif);
        font-size: 28px;
        font-weight: 400;
        font-style: italic;
        color: #F6F1E7;
        letter-spacing: -.01em;
    }
    .eng-header-title em { color: var(--gold3); font-style: italic; }
    .eng-header-sub {
        font-family: var(--mono);
        font-size: 8px;
        letter-spacing: .28em;
        text-transform: uppercase;
        color: rgba(213,169,68,.6);
    }
    .eng-header-badge {
        font-family: var(--mono);
        font-size: 8px;
        letter-spacing: .2em;
        text-transform: uppercase;
        color: var(--gold3);
        border: 1px solid rgba(213,169,68,.3);
        padding: 5px 12px;
        white-space: nowrap;
        display: flex;
        align-items: center;
        gap: 7px;
    }
    .eng-header-badge::before {
        content: '';
        width: 5px; height: 5px;
        border-radius: 50%;
        background: var(--gold3);
        flex-shrink: 0;
        animation: blink 2s infinite;
    }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

    /* ── SECTION LABEL ── */
    .sec-label {
        font-family: var(--mono);
        font-size: 8px;
        letter-spacing: .35em;
        text-transform: uppercase;
        color: var(--gold);
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sec-label::before {
        content: '';
        display: inline-block;
        width: 18px; height: 1px;
        background: var(--gold);
        flex-shrink: 0;
    }

    /* ── METRIC CARDS ── */
    .metric-row { display: flex; gap: 1px; background: rgba(16,14,12,.08); margin-bottom: 24px; }
    .metric-card {
        flex: 1;
        background: var(--paper2);
        padding: 18px 20px;
        border-right: 1px solid rgba(16,14,12,.06);
    }
    .metric-card:last-child { border-right: none; }
    .metric-card-val {
        font-family: var(--serif);
        font-size: 30px;
        font-weight: 500;
        color: var(--ink);
        line-height: 1;
        margin-bottom: 5px;
        letter-spacing: -.02em;
    }
    .metric-card-lbl {
        font-family: var(--mono);
        font-size: 8px;
        letter-spacing: .2em;
        text-transform: uppercase;
        color: var(--faint);
    }
    .metric-card-val.up   { color: var(--green); }
    .metric-card-val.down { color: var(--red);   }
    .metric-card-val.gold { color: var(--gold);  }

    /* ── DATA TABLE ── */
    .stDataFrame { border: 1px solid rgba(16,14,12,.08) !important; }
    .stDataFrame thead th {
        background: var(--ink) !important;
        color: var(--paper) !important;
        font-family: var(--mono) !important;
        font-size: 8.5px !important;
        letter-spacing: .15em !important;
        text-transform: uppercase !important;
        padding: 10px 14px !important;
        border: none !important;
    }
    .stDataFrame tbody td {
        font-family: var(--sans) !important;
        font-size: 13px !important;
        padding: 9px 14px !important;
        border-bottom: 1px solid rgba(16,14,12,.05) !important;
        vertical-align: middle !important;
    }
    .stDataFrame tbody tr:hover td { background: var(--paper2) !important; }

    /* ── SCORE BAR ── */
    .score-bar-wrap { margin-bottom: 6px; }
    .score-bar-top { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }
    .score-bar-label { font-family: var(--mono); font-size: 8.5px; letter-spacing: .12em; color: var(--muted); text-transform: uppercase; }
    .score-bar-value { font-family: var(--serif); font-size: 16px; font-weight: 600; color: var(--ink); }
    .score-bar-track { height: 3px; background: rgba(16,14,12,.08); }
    .score-bar-fill  { height: 3px; background: var(--gold3); transition: width .6s; }

    /* ── FLAGS ── */
    .flag-card {
        padding: 12px 16px;
        border-left: 3px solid;
        margin-bottom: 8px;
        background: var(--paper2);
    }
    .flag-card.high   { border-color: var(--red); }
    .flag-card.medium { border-color: var(--gold3); }
    .flag-card.low    { border-color: var(--green); }
    .flag-title { font-family: var(--serif); font-size: 14px; font-weight: 600; color: var(--ink); margin-bottom: 3px; }
    .flag-desc  { font-family: var(--sans); font-size: 12px; color: var(--muted); line-height: 1.55; }
    .flag-tag   { font-family: var(--mono); font-size: 7.5px; letter-spacing: .15em; text-transform: uppercase; margin-top: 5px; }
    .flag-tag.high   { color: var(--red); }
    .flag-tag.medium { color: var(--gold); }
    .flag-tag.low    { color: var(--green); }

    /* ── STATUS BOX ── */
    .status-wip {
        border: 1px solid rgba(213,169,68,.3);
        background: rgba(213,169,68,.05);
        padding: 14px 18px;
        font-family: var(--mono);
        font-size: 9px;
        letter-spacing: .15em;
        color: var(--gold2);
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 8px;
    }
    .status-wip::before {
        content: '';
        width: 5px; height: 5px;
        border-radius: 50%;
        background: var(--gold3);
        flex-shrink: 0;
        animation: blink 2s infinite;
    }

    /* ── BUTTONS ── */
    .stButton > button {
        font-family: var(--mono) !important;
        font-size: 9px !important;
        letter-spacing: .18em !important;
        text-transform: uppercase !important;
        background: var(--ink) !important;
        color: var(--paper) !important;
        border: none !important;
        padding: 10px 22px !important;
        border-radius: 0 !important;
        transition: background .2s !important;
    }
    .stButton > button:hover { background: var(--gold) !important; }

    /* ── TABS ── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid rgba(16,14,12,.1) !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: var(--mono) !important;
        font-size: 9px !important;
        letter-spacing: .2em !important;
        text-transform: uppercase !important;
        color: var(--faint) !important;
        background: transparent !important;
        padding: 10px 18px !important;
        border-radius: 0 !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--ink) !important;
        border-bottom: 2px solid var(--gold) !important;
        background: transparent !important;
    }

    /* ── EXPANDER ── */
    .stExpander { border: 1px solid rgba(16,14,12,.08) !important; border-radius: 0 !important; }
    .stExpander summary { font-family: var(--mono) !important; font-size: 9.5px !important; letter-spacing: .15em !important; text-transform: uppercase !important; }

    /* ── DIVIDER ── */
    hr { border: none; border-top: 1px solid rgba(16,14,12,.08); margin: 24px 0; }

    /* ── SELECTBOX / MULTISELECT ── */
    [data-baseweb="select"] { border-radius: 0 !important; }
    [data-baseweb="select"] > div { border-radius: 0 !important; font-family: var(--sans) !important; }

    /* ── SPINNER ── */
    .stSpinner > div { border-top-color: var(--gold) !important; }

    /* ── TOOLTIP ── */
    .tooltip-pill {
        display: inline-block;
        font-family: var(--mono);
        font-size: 7.5px;
        letter-spacing: .12em;
        text-transform: uppercase;
        padding: 3px 9px;
        border: 1px solid;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    .tooltip-pill.green { color: var(--green); border-color: rgba(27,75,43,.3); background: rgba(27,75,43,.06); }
    .tooltip-pill.gold  { color: var(--gold);  border-color: rgba(155,111,41,.3); background: rgba(155,111,41,.05); }
    .tooltip-pill.red   { color: var(--red);   border-color: rgba(140,27,27,.3);  background: rgba(140,27,27,.05); }
    .tooltip-pill.muted { color: var(--muted); border-color: rgba(16,14,12,.12);  background: transparent; }
    </style>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str, badge: str = "Phase 1 · SBF 120"):
    st.markdown(f"""
    <div class="eng-header">
        <div>
            <div class="eng-header-title">{title}</div>
            <div class="eng-header-sub">{subtitle}</div>
        </div>
        <div class="eng-header-badge">{badge}</div>
    </div>
    """, unsafe_allow_html=True)


def sec_label(text: str):
    st.markdown(f'<div class="sec-label">{text}</div>', unsafe_allow_html=True)


def metric_row(metrics: list):
    """
    metrics = [{"val": "€8.05", "lbl": "Blended IV", "cls": "gold"}, ...]
    """
    cards = ""
    for m in metrics:
        cls = m.get("cls", "")
        cards += f"""
        <div class="metric-card">
            <div class="metric-card-val {cls}">{m['val']}</div>
            <div class="metric-card-lbl">{m['lbl']}</div>
        </div>"""
    st.markdown(f'<div class="metric-row">{cards}</div>', unsafe_allow_html=True)


def score_bar(label: str, score: float, max_score: float = 100):
    pct = min(100, (score / max_score) * 100)
    st.markdown(f"""
    <div class="score-bar-wrap">
        <div class="score-bar-top">
            <span class="score-bar-label">{label}</span>
            <span class="score-bar-value">{score:.0f}</span>
        </div>
        <div class="score-bar-track">
            <div class="score-bar-fill" style="width:{pct}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def flag_card(title: str, desc: str, severity: str = "medium"):
    sev = severity.lower()
    icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    icon = icons.get(sev, "⚪")
    st.markdown(f"""
    <div class="flag-card {sev}">
        <div class="flag-title">{icon} {title}</div>
        <div class="flag-desc">{desc}</div>
        <div class="flag-tag {sev}">{sev.upper()} SEVERITY</div>
    </div>
    """, unsafe_allow_html=True)


def status_wip(text: str = "Module in Development — Coming in Next Sprint"):
    st.markdown(f'<div class="status-wip">{text}</div>', unsafe_allow_html=True)


def pill(text: str, color: str = "muted"):
    return f'<span class="tooltip-pill {color}">{text}</span>'
