"""
config.py — Deal Sourcing & Preliminary Diligence Engine
Central configuration: tickers, scoring weights, UI constants.
"""

APP_TITLE    = "Deal Sourcing & Preliminary Diligence Engine"
APP_SUBTITLE = "European M&A · Phase 1 — Euronext Paris / SBF 120"
APP_VERSION  = "1.0.0-alpha"
APP_AUTHOR   = "Aryan Shrenick Kothari"

# ─── 30-COMPANY SBF 120 UNIVERSE ────────────────────────────────────────────
SBF120_TICKERS = {
    # Luxury & Consumer
    "Kering":           "KER.PA",
    "LVMH":             "MC.PA",
    "Remy Cointreau":   "RCO.PA",
    "Pernod Ricard":    "RI.PA",
    "Hermes":           "RMS.PA",
    # Healthcare & Pharma
    "Ipsen":            "IPN.PA",
    "bioMerieux":       "BIM.PA",
    "Sanofi":           "SAN.PA",
    "Eurofins":         "ERF.PA",
    # Technology & Media
    "Capgemini":        "CAP.PA",
    "Dassault Systemes":"DSY.PA",
    "Atos":             "ATO.PA",
    "Vivendi":          "VIV.PA",
    "Worldline":        "WLN.PA",
    # Industrials & Engineering
    "Bouygues":         "EN.PA",
    "Saint-Gobain":     "SGO.PA",
    "Legrand":          "LR.PA",
    "Safran":           "SAF.PA",
    "Schneider Electric":"SU.PA",
    "Vallourec":        "VK.PA",
    # Retail & Distribution
    "Carrefour":        "CA.PA",
    "Sodexo":           "SW.PA",
    # Energy & Utilities
    "TotalEnergies":    "TTE.PA",
    "Engie":            "ENGI.PA",
    "Veolia":           "VIE.PA",
    # Financial Services
    "BNP Paribas":      "BNP.PA",
    "AXA":              "CS.PA",
    # Real Estate
    "Unibail-Rodamco":  "URW.AS",
    "Covivio":          "COV.PA",
}

TICKER_SECTOR_MAP = {
    "KER.PA":  "Luxury & Consumer",
    "MC.PA":   "Luxury & Consumer",
    "RCO.PA":  "Luxury & Consumer",
    "RI.PA":   "Luxury & Consumer",
    "RMS.PA":  "Luxury & Consumer",
    "IPN.PA":  "Healthcare & Pharma",
    "BIM.PA":  "Healthcare & Pharma",
    "SAN.PA":  "Healthcare & Pharma",
    "ERF.PA":  "Healthcare & Pharma",
    "CAP.PA":  "Technology & Media",
    "DSY.PA":  "Technology & Media",
    "ATO.PA":  "Technology & Media",
    "VIV.PA":  "Technology & Media",
    "WLN.PA":  "Technology & Media",
    "EN.PA":   "Industrials & Engineering",
    "SGO.PA":  "Industrials & Engineering",
    "LR.PA":   "Industrials & Engineering",
    "SAF.PA":  "Industrials & Engineering",
    "SU.PA":   "Industrials & Engineering",
    "VK.PA":   "Industrials & Engineering",
    "CA.PA":   "Retail & Distribution",
    "SW.PA":   "Retail & Distribution",
    "TTE.PA":  "Energy & Utilities",
    "ENGI.PA": "Energy & Utilities",
    "VIE.PA":  "Energy & Utilities",
    "BNP.PA":  "Financial Services",
    "CS.PA":   "Financial Services",
    "URW.AS":  "Real Estate",
    "COV.PA":  "Real Estate",
}

# ─── 8-PILLAR SCORING WEIGHTS ───────────────────────────────────────────────
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

COLORS = {
    "gold":   "#9B6F29",
    "gold3":  "#D5A944",
    "green":  "#1B4B2B",
    "ink":    "#100E0C",
    "paper":  "#F6F1E7",
    "muted":  "#7B7368",
    "red":    "#8C1B1B",
}

EXPORT_FILENAME = "deal_sourcing_shortlist.xlsx"
