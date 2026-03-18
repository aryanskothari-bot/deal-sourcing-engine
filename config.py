"""
config.py — Deal Sourcing & Preliminary Diligence Engine
Central configuration: tickers, scoring weights, UI constants, column definitions.
"""

# ─── APP META ────────────────────────────────────────────────────────────────
APP_TITLE       = "Deal Sourcing & Preliminary Diligence Engine"
APP_SUBTITLE    = "European M&A · Phase 1 — Euronext Paris / SBF 120"
APP_VERSION     = "1.0.0-alpha"
APP_AUTHOR      = "Aryan Shrenick Kothari"

# ─── PHASE 1 UNIVERSE — SBF 120 SAMPLE (yfinance tickers) ───────────────────
# Format: {display_name: yfinance_ticker}
SBF120_TICKERS = {
    # Luxury & Consumer
    "LVMH":                "MC.PA",
    "Hermès":              "RMS.PA",
    "Kering":              "KER.PA",
    "L'Oréal":             "OR.PA",
    "Rémy Cointreau":      "RCO.PA",
    "Pernod Ricard":       "RI.PA",

    # Industrials & Engineering
    "Airbus":              "AIR.PA",
    "Safran":              "SAF.PA",
    "Thales":              "HO.PA",
    "Schneider Electric":  "SU.PA",
    "Legrand":             "LR.PA",
    "Saint-Gobain":        "SGO.PA",
    "Vinci":               "DG.PA",
    "Bouygues":            "EN.PA",

    # Energy & Utilities
    "TotalEnergies":       "TTE.PA",
    "Engie":               "ENGI.PA",
    "EDF":                 "EDF.PA",

    # Financial Services
    "BNP Paribas":         "BNP.PA",
    "Société Générale":    "GLE.PA",
    "Crédit Agricole":     "ACA.PA",
    "AXA":                 "CS.PA",

    # Healthcare & Pharma
    "Sanofi":              "SAN.PA",
    "bioMérieux":          "BIM.PA",
    "Ipsen":               "IPN.PA",

    # Technology & Media
    "Capgemini":           "CAP.PA",
    "Dassault Systèmes":   "DSY.PA",
    "Atos":                "ATO.PA",
    "Vivendi":             "VIV.PA",

    # Retail & Distribution
    "Carrefour":           "CA.PA",
    "LVMH (Retail arm)":   "MC.PA",

    # Real Estate
    "Unibail-Rodamco":     "URW.AS",
    "Klepierre":           "LI.PA",
}

# ─── SECTOR MAPPING ──────────────────────────────────────────────────────────
SECTORS = [
    "All Sectors",
    "Luxury & Consumer",
    "Industrials & Engineering",
    "Energy & Utilities",
    "Financial Services",
    "Healthcare & Pharma",
    "Technology & Media",
    "Retail & Distribution",
    "Real Estate",
]

TICKER_SECTOR_MAP = {
    "MC.PA": "Luxury & Consumer",
    "RMS.PA": "Luxury & Consumer",
    "KER.PA": "Luxury & Consumer",
    "OR.PA": "Luxury & Consumer",
    "RCO.PA": "Luxury & Consumer",
    "RI.PA": "Luxury & Consumer",
    "AIR.PA": "Industrials & Engineering",
    "SAF.PA": "Industrials & Engineering",
    "HO.PA": "Industrials & Engineering",
    "SU.PA": "Industrials & Engineering",
    "LR.PA": "Industrials & Engineering",
    "SGO.PA": "Industrials & Engineering",
    "DG.PA": "Industrials & Engineering",
    "EN.PA": "Industrials & Engineering",
    "TTE.PA": "Energy & Utilities",
    "ENGI.PA": "Energy & Utilities",
    "EDF.PA": "Energy & Utilities",
    "BNP.PA": "Financial Services",
    "GLE.PA": "Financial Services",
    "ACA.PA": "Financial Services",
    "CS.PA": "Financial Services",
    "SAN.PA": "Healthcare & Pharma",
    "BIM.PA": "Healthcare & Pharma",
    "IPN.PA": "Healthcare & Pharma",
    "CAP.PA": "Technology & Media",
    "DSY.PA": "Technology & Media",
    "ATO.PA": "Technology & Media",
    "VIV.PA": "Technology & Media",
    "CA.PA": "Retail & Distribution",
    "URW.AS": "Real Estate",
    "LI.PA": "Real Estate",
}

# ─── SCREENER FILTER DEFAULTS ─────────────────────────────────────────────────
SCREENER_DEFAULTS = {
    "mktcap_min_bn":    0.5,    # EUR bn
    "mktcap_max_bn":    50.0,
    "ev_min_bn":        0.5,
    "ev_max_bn":        80.0,
    "revenue_min_mn":   100.0,  # EUR mn
    "ebitda_margin_min": -5.0,  # %
    "net_debt_ebitda_max": 8.0,
    "ev_ebitda_max":    20.0,
}

# ─── 8-PILLAR SCORING WEIGHTS ─────────────────────────────────────────────────
SCORING_PILLARS = {
    "Revenue Growth":           0.15,
    "Profitability":            0.15,
    "Balance Sheet Quality":    0.12,
    "Leverage":                 0.12,
    "Valuation Attractiveness": 0.15,
    "Size Compatibility":       0.10,
    "Geographic Relevance":     0.08,
    "Acquisition Fit":          0.13,
}

# ─── FINANCIAL STATEMENT PERIODS ─────────────────────────────────────────────
HIST_YEARS = 5          # years of history to pull
FORECAST_YEARS = 3      # years to forecast

# ─── DILIGENCE FLAGS ──────────────────────────────────────────────────────────
FLAG_SEVERITY = {
    "HIGH":   "🔴",
    "MEDIUM": "🟡",
    "LOW":    "🟢",
}

# ─── EXPORT ───────────────────────────────────────────────────────────────────
EXPORT_FILENAME = "deal_sourcing_shortlist.xlsx"

# ─── UI ───────────────────────────────────────────────────────────────────────
PAGE_ICON = "⚙️"
SIDEBAR_WIDTH = 320

# Colour palette — mirrors portfolio site
COLORS = {
    "gold":     "#9B6F29",
    "gold3":    "#D5A944",
    "green":    "#1B4B2B",
    "ink":      "#100E0C",
    "paper":    "#F6F1E7",
    "red":      "#8C1B1B",
    "muted":    "#7B7368",
}
