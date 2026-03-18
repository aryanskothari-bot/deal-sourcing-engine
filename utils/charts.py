"""
charts.py — Plotly chart builders for the Deal Sourcing Engine.
All charts use the portfolio site's warm ivory / gold palette.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from config import COLORS

# ─── SHARED LAYOUT DEFAULTS ──────────────────────────────────────────────────
_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#F6F1E7",
    font=dict(family="DM Mono, Courier New, monospace", color="#100E0C", size=11),
    margin=dict(l=12, r=12, t=36, b=12),
    showlegend=False,
)

_AXIS = dict(
    showgrid=True,
    gridcolor="rgba(16,14,12,.06)",
    zeroline=False,
    tickfont=dict(family="DM Mono", size=10, color="#A19890"),
    linecolor="rgba(16,14,12,.12)",
)


# ─── RADAR CHART — 8-pillar score breakdown ──────────────────────────────────
def radar_chart(pillar_scores: dict, company_name: str) -> go.Figure:
    categories = list(pillar_scores.keys())
    values     = list(pillar_scores.values())
    values_closed = values + [values[0]]
    cats_closed   = categories + [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=cats_closed,
        fill="toself",
        fillcolor="rgba(155,111,41,.12)",
        line=dict(color=COLORS["gold3"], width=2),
        name=company_name,
    ))
    fig.update_layout(
        **_LAYOUT,
        polar=dict(
            bgcolor="#EEE7D7",
            radialaxis=dict(
                visible=True, range=[0, 100], tickfont=dict(size=9, color="#A19890"),
                gridcolor="rgba(16,14,12,.1)", linecolor="rgba(16,14,12,.1)",
            ),
            angularaxis=dict(tickfont=dict(size=10, family="DM Mono", color="#4B4540")),
        ),
        title=dict(text=f"<b>{company_name}</b> — Pillar Breakdown", font=dict(size=13, family="Cormorant Garamond"), x=0.5),
        height=380,
    )
    return fig


# ─── WATERFALL — Revenue/EBITDA bridge ───────────────────────────────────────
def waterfall_chart(items: list, title: str = "EBITDA Bridge") -> go.Figure:
    """
    items = [{"label": "Reported EBITDA", "value": 1200, "type": "absolute"},
             {"label": "+ Mgmt Fees",     "value": 45,   "type": "relative"},
             {"label": "- One-offs",      "value": -80,  "type": "relative"},
             {"label": "Adjusted EBITDA", "value": 0,    "type": "total"}]
    """
    labels  = [i["label"] for i in items]
    values  = [i["value"] for i in items]
    measure = [i.get("type", "relative") for i in items]

    colors = []
    for m, v in zip(measure, values):
        if m == "absolute" or m == "total":
            colors.append(COLORS["ink"])
        elif v >= 0:
            colors.append(COLORS["green"])
        else:
            colors.append(COLORS["red"])

    fig = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        measure=measure,
        x=labels,
        y=values,
        connector=dict(line=dict(color="rgba(16,14,12,.2)", width=1, dash="dot")),
        increasing=dict(marker_color=COLORS["green"]),
        decreasing=dict(marker_color=COLORS["red"]),
        totals=dict(marker_color=COLORS["gold"]),
    ))
    fig.update_layout(
        **_LAYOUT,
        title=dict(text=title, font=dict(size=13, family="Cormorant Garamond"), x=0),
        yaxis=dict(**_AXIS, title="€mn"),
        xaxis=dict(tickfont=dict(size=10, family="DM Mono", color="#4B4540")),
        height=340,
    )
    return fig


# ─── BAR CHART — Historical revenue/EBITDA ───────────────────────────────────
def financials_bar(years: list, revenue: list, ebitda: list, company: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=revenue,
        name="Revenue",
        marker_color=COLORS["ink"],
        opacity=0.85,
        width=0.35,
        offset=-0.2,
    ))
    fig.add_trace(go.Bar(
        x=years, y=ebitda,
        name="EBITDA",
        marker_color=COLORS["gold3"],
        opacity=0.85,
        width=0.35,
        offset=0.2,
    ))
    fig.add_trace(go.Scatter(
        x=years, y=ebitda,
        mode="lines+markers",
        name="EBITDA trend",
        line=dict(color=COLORS["gold"], width=2, dash="dot"),
        marker=dict(size=5, color=COLORS["gold"]),
        showlegend=False,
    ))
    fig.update_layout(
        **_LAYOUT,
        barmode="overlay",
        title=dict(text=f"{company} — Revenue & EBITDA (€mn)", font=dict(size=13, family="Cormorant Garamond"), x=0),
        yaxis=dict(**_AXIS, title="€mn"),
        xaxis=dict(**_AXIS, tickvals=years),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10, family="DM Mono")),
        height=340,
    )
    return fig


# ─── LINE CHART — Margin trend ────────────────────────────────────────────────
def margin_line(years: list, ebitda_margin: list, ebit_margin: list, company: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years, y=ebitda_margin,
        mode="lines+markers",
        name="EBITDA Margin",
        line=dict(color=COLORS["gold3"], width=2.5),
        marker=dict(size=6),
    ))
    fig.add_trace(go.Scatter(
        x=years, y=ebit_margin,
        mode="lines+markers",
        name="EBIT Margin",
        line=dict(color=COLORS["muted"], width=2, dash="dash"),
        marker=dict(size=5),
    ))
    fig.update_layout(
        **_LAYOUT,
        title=dict(text=f"{company} — Margin Trend (%)", font=dict(size=13, family="Cormorant Garamond"), x=0),
        yaxis=dict(**_AXIS, title="Margin %", ticksuffix="%"),
        xaxis=dict(**_AXIS, tickvals=years),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10, family="DM Mono")),
        height=300,
    )
    return fig


# ─── SCATTER — EV/EBITDA vs EBITDA Margin ────────────────────────────────────
def scatter_valuation(df: pd.DataFrame) -> go.Figure:
    dfc = df.dropna(subset=["EV/EBITDA", "EBITDA Margin %", "Score"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dfc["EBITDA Margin %"],
        y=dfc["EV/EBITDA"],
        mode="markers+text",
        text=dfc["Company"],
        textposition="top center",
        textfont=dict(size=9, family="DM Mono", color="#7B7368"),
        marker=dict(
            size=dfc["Score"].fillna(50) / 5 + 6,
            color=dfc["Score"].fillna(50),
            colorscale=[[0, "#8C1B1B"], [0.5, "#D5A944"], [1, "#1B4B2B"]],
            showscale=True,
            colorbar=dict(title="Score", tickfont=dict(size=9, family="DM Mono")),
            line=dict(width=1, color="rgba(16,14,12,.25)"),
        ),
    ))
    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Valuation vs Profitability (bubble = score)", font=dict(size=13, family="Cormorant Garamond"), x=0),
        xaxis=dict(**_AXIS, title="EBITDA Margin %"),
        yaxis=dict(**_AXIS, title="EV/EBITDA"),
        height=420,
    )
    return fig


# ─── HORIZONTAL BAR — Score league table ──────────────────────────────────────
def score_bars(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    dfs = df.nlargest(top_n, "Score")[["Company", "Score", "Sector"]].copy()
    dfs = dfs.sort_values("Score")

    color_map = {
        "Luxury & Consumer":         "#9B6F29",
        "Healthcare & Pharma":       "#1B4B2B",
        "Technology & Media":        "#4B4540",
        "Industrials & Engineering": "#2B2520",
        "Retail & Distribution":     "#A19890",
        "Real Estate":               "#7B7368",
        "Energy & Utilities":        "#6B5B3E",
        "Financial Services":        "#100E0C",
    }
    colors = dfs["Sector"].map(color_map).fillna(COLORS["ink"]).tolist()

    fig = go.Figure(go.Bar(
        x=dfs["Score"],
        y=dfs["Company"],
        orientation="h",
        marker_color=colors,
        text=dfs["Score"].round(1),
        textposition="outside",
        textfont=dict(family="DM Mono", size=10),
    ))
    fig.update_layout(
        **_LAYOUT,
        title=dict(text=f"Top {top_n} Acquisition Targets by Score", font=dict(size=13, family="Cormorant Garamond"), x=0),
        xaxis=dict(**_AXIS, range=[0, 105], title="Composite Score (0–100)"),
        yaxis=dict(tickfont=dict(size=11, family="DM Mono", color="#2B2520")),
        height=max(300, top_n * 36),
    )
    return fig
