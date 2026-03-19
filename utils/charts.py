"""
charts.py — Plotly chart builders for the Deal Sourcing Engine.
"""
import plotly.graph_objects as go
import pandas as pd
from config import COLORS

_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#F6F1E7",
    font=dict(family="DM Mono, Courier New, monospace", color="#100E0C", size=11),
    margin=dict(l=12, r=12, t=40, b=12),
)
_AXIS = dict(
    showgrid=True,
    gridcolor="rgba(16,14,12,.06)",
    zeroline=False,
    tickfont=dict(family="DM Mono", size=10, color="#A19890"),
    linecolor="rgba(16,14,12,.12)",
)

def radar_chart(pillar_scores: dict, company_name: str) -> go.Figure:
    categories = list(pillar_scores.keys())
    values     = list(pillar_scores.values())
    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(155,111,41,.12)",
        line=dict(color=COLORS["gold3"], width=2),
        name=company_name,
    ))
    fig.update_layout(
        **_LAYOUT,
        polar=dict(
            bgcolor="#EEE7D7",
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=9, color="#A19890"),
                            gridcolor="rgba(16,14,12,.1)", linecolor="rgba(16,14,12,.1)"),
            angularaxis=dict(tickfont=dict(size=10, family="DM Mono", color="#4B4540")),
        ),
        title=dict(text=f"<b>{company_name}</b> — Pillar Breakdown",
                   font=dict(size=13, family="Cormorant Garamond"), x=0.5),
        height=380,
    )
    return fig


def waterfall_chart(items: list, title: str = "EBITDA Bridge") -> go.Figure:
    """
    items = [{"label": str, "value": float, "type": "absolute"|"relative"|"total"}]
    """
    labels  = [i["label"] for i in items]
    values  = [i["value"] for i in items]
    measure = [i.get("type", "relative") for i in items]

    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=measure,
        x=labels,
        y=values,
        textposition="outside",
        text=[f"€{v:,.0f}mn" if v != 0 else "" for v in values],
        connector=dict(line=dict(color="rgba(16,14,12,.2)", width=1, dash="dot")),
        increasing=dict(marker=dict(color=COLORS["green"])),
        decreasing=dict(marker=dict(color=COLORS["red"])),
        totals=dict(marker=dict(color=COLORS["gold"])),
    ))
    fig.update_layout(
        **_LAYOUT,
        title=dict(text=title, font=dict(size=13, family="Cormorant Garamond"), x=0),
        yaxis=dict(**_AXIS, title="€mn"),
        xaxis=dict(tickfont=dict(size=10, family="DM Mono", color="#4B4540")),
        height=360,
        showlegend=False,
    )
    return fig


def financials_bar(years: list, revenue: list, ebitda: list, company: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=revenue, name="Revenue",
        marker_color=COLORS["ink"], opacity=0.85,
    ))
    fig.add_trace(go.Bar(
        x=years, y=ebitda, name="EBITDA",
        marker_color=COLORS["gold3"], opacity=0.90,
    ))
    fig.update_layout(
        **_LAYOUT,
        barmode="group",
        title=dict(text=f"{company} — Revenue & EBITDA (€mn)",
                   font=dict(size=13, family="Cormorant Garamond"), x=0),
        yaxis=dict(**_AXIS, title="€mn"),
        xaxis=dict(**_AXIS, tickvals=years),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=10, family="DM Mono")),
        height=340,
    )
    return fig


def margin_line(years: list, ebitda_margin: list, ebit_margin: list, company: str) -> go.Figure:
    # Filter out None values — pair years with valid margin values
    def clean(yrs, vals):
        paired = [(y, v) for y, v in zip(yrs, vals) if v is not None]
        if not paired:
            return [], []
        return [p[0] for p in paired], [p[1] for p in paired]

    em_years, em_vals = clean(years, ebitda_margin)
    im_years, im_vals = clean(years, ebit_margin)

    fig = go.Figure()
    if em_vals:
        fig.add_trace(go.Scatter(
            x=em_years, y=em_vals, mode="lines+markers",
            name="EBITDA Margin",
            line=dict(color=COLORS["gold3"], width=2.5),
            marker=dict(size=7, symbol="circle"),
        ))
    if im_vals:
        fig.add_trace(go.Scatter(
            x=im_years, y=im_vals, mode="lines+markers",
            name="EBIT Margin",
            line=dict(color=COLORS["muted"], width=2, dash="dash"),
            marker=dict(size=5, symbol="circle"),
        ))
    fig.update_layout(
        **_LAYOUT,
        title=dict(text=f"{company} — Margin Trend (%)",
                   font=dict(size=13, family="Cormorant Garamond"), x=0),
        yaxis=dict(**_AXIS, title="Margin %", ticksuffix="%"),
        xaxis=dict(**_AXIS, tickvals=years),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(size=10, family="DM Mono")),
        height=300,
    )
    return fig


def scatter_valuation(df: pd.DataFrame) -> go.Figure:
    dfc = df.dropna(subset=["EV/EBITDA", "EBITDA Margin %", "Score"])
    fig = go.Figure(go.Scatter(
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
        title=dict(text="Valuation vs Profitability (bubble = score)",
                   font=dict(size=13, family="Cormorant Garamond"), x=0),
        xaxis=dict(**_AXIS, title="EBITDA Margin %"),
        yaxis=dict(**_AXIS, title="EV/EBITDA"),
        height=420,
    )
    return fig


def score_bars(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    dfs = df.nlargest(top_n, "Score")[["Company", "Score", "Sector"]].copy()
    dfs = dfs.sort_values("Score")
    color_map = {
        "Luxury & Consumer": "#9B6F29", "Healthcare & Pharma": "#1B4B2B",
        "Technology & Media": "#4B4540", "Industrials & Engineering": "#2B2520",
        "Retail & Distribution": "#A19890",
    }
    colors = dfs["Sector"].map(color_map).fillna(COLORS["ink"]).tolist()
    fig = go.Figure(go.Bar(
        x=dfs["Score"], y=dfs["Company"], orientation="h",
        marker_color=colors,
        text=dfs["Score"].round(1), textposition="outside",
        textfont=dict(family="DM Mono", size=10),
    ))
    fig.update_layout(
        **_LAYOUT,
        title=dict(text=f"Top {top_n} Acquisition Targets by Score",
                   font=dict(size=13, family="Cormorant Garamond"), x=0),
        xaxis=dict(**_AXIS, range=[0, 110], title="Composite Score (0–100)"),
        yaxis=dict(tickfont=dict(size=11, family="DM Mono", color="#2B2520")),
        height=max(300, top_n * 36),
        showlegend=False,
    )
    return fig


def score_bars_vertical(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Alias kept for backward compatibility."""
    return score_bars(df, top_n)
