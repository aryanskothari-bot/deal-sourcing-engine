"""
static_loader.py — 30-company SBF 120 static dataset.
Balanced scoring spread across sectors. Used as fallback when yfinance unavailable.
"""
import pandas as pd

STATIC_COMPANIES = [
    # ── LUXURY & CONSUMER ──────────────────────────────────────────────────────
    {"name":"Kering",          "ticker":"KER.PA","sector":"Luxury & Consumer",         "country":"France","mktcap_bn":28.4, "ev_bn":31.2, "revenue_mn":17640,"ebitda_mn":4120,"ebitda_margin_pct":23.4,"revenue_growth_pct":-11.3,"net_debt_mn":2800, "net_debt_ebitda":0.68,"ev_ebitda":7.6, "ev_revenue":1.77,"pe_ntm":14.2,"roe_pct":18.4,"roic_pct":11.2,"current_ratio":1.32,"acq_score":74},
    {"name":"LVMH",            "ticker":"MC.PA", "sector":"Luxury & Consumer",         "country":"France","mktcap_bn":290.0,"ev_bn":310.0,"revenue_mn":86153,"ebitda_mn":22836,"ebitda_margin_pct":26.5,"revenue_growth_pct":8.0, "net_debt_mn":14200,"net_debt_ebitda":0.62,"ev_ebitda":13.6,"ev_revenue":3.60,"pe_ntm":21.8,"roe_pct":22.1,"roic_pct":14.8,"current_ratio":0.88,"acq_score":45},
    {"name":"Rémy Cointreau",  "ticker":"RCO.PA","sector":"Luxury & Consumer",         "country":"France","mktcap_bn":3.8,  "ev_bn":4.8,  "revenue_mn":1236, "ebitda_mn":300, "ebitda_margin_pct":24.3,"revenue_growth_pct":-18.2,"net_debt_mn":940,  "net_debt_ebitda":3.13,"ev_ebitda":16.0,"ev_revenue":3.88,"pe_ntm":32.1,"roe_pct":9.2, "roic_pct":6.8, "current_ratio":2.45,"acq_score":48},
    {"name":"Pernod Ricard",   "ticker":"RI.PA", "sector":"Luxury & Consumer",         "country":"France","mktcap_bn":28.6, "ev_bn":38.2, "revenue_mn":11598,"ebitda_mn":3248,"ebitda_margin_pct":28.0,"revenue_growth_pct":-5.8, "net_debt_mn":8620, "net_debt_ebitda":2.65,"ev_ebitda":11.8,"ev_revenue":3.29,"pe_ntm":14.6,"roe_pct":12.0,"roic_pct":8.4, "current_ratio":1.92,"acq_score":60},
    {"name":"Hermès",          "ticker":"RMS.PA","sector":"Luxury & Consumer",         "country":"France","mktcap_bn":195.0,"ev_bn":192.0,"revenue_mn":13427,"ebitda_mn":6040,"ebitda_margin_pct":45.0,"revenue_growth_pct":12.6,"net_debt_mn":-3200,"net_debt_ebitda":-0.53,"ev_ebitda":31.8,"ev_revenue":14.30,"pe_ntm":42.0,"roe_pct":38.2,"roic_pct":32.1,"current_ratio":3.20,"acq_score":38},

    # ── HEALTHCARE & PHARMA ────────────────────────────────────────────────────
    {"name":"Ipsen",           "ticker":"IPN.PA","sector":"Healthcare & Pharma",        "country":"France","mktcap_bn":7.8,  "ev_bn":7.2,  "revenue_mn":3304, "ebitda_mn":1124,"ebitda_margin_pct":34.0,"revenue_growth_pct":8.2, "net_debt_mn":-420, "net_debt_ebitda":-0.52,"ev_ebitda":6.4,"ev_revenue":2.18,"pe_ntm":11.2,"roe_pct":24.6,"roic_pct":18.2,"current_ratio":2.84,"acq_score":96},
    {"name":"bioMérieux",      "ticker":"BIM.PA","sector":"Healthcare & Pharma",        "country":"France","mktcap_bn":9.8,  "ev_bn":10.1, "revenue_mn":3960, "ebitda_mn":950, "ebitda_margin_pct":24.0,"revenue_growth_pct":5.4, "net_debt_mn":230,  "net_debt_ebitda":0.24,"ev_ebitda":10.6,"ev_revenue":2.55,"pe_ntm":24.8,"roe_pct":14.2,"roic_pct":10.8,"current_ratio":2.12,"acq_score":78},
    {"name":"Sanofi",          "ticker":"SAN.PA","sector":"Healthcare & Pharma",        "country":"France","mktcap_bn":110.0,"ev_bn":118.0,"revenue_mn":40598,"ebitda_mn":9840,"ebitda_margin_pct":24.2,"revenue_growth_pct":11.4,"net_debt_mn":7200, "net_debt_ebitda":0.73,"ev_ebitda":12.0,"ev_revenue":2.91,"pe_ntm":14.4,"roe_pct":12.8,"roic_pct":9.2, "current_ratio":1.45,"acq_score":62},
    {"name":"Eurofins",        "ticker":"ERF.PA","sector":"Healthcare & Pharma",        "country":"France","mktcap_bn":9.2,  "ev_bn":13.8, "revenue_mn":6710, "ebitda_mn":1475,"ebitda_margin_pct":22.0,"revenue_growth_pct":3.8, "net_debt_mn":4250, "net_debt_ebitda":2.88,"ev_ebitda":9.4,"ev_revenue":2.06,"pe_ntm":18.2,"roe_pct":10.4,"roic_pct":7.6, "current_ratio":1.18,"acq_score":68},

    # ── TECHNOLOGY & MEDIA ─────────────────────────────────────────────────────
    {"name":"Capgemini",       "ticker":"CAP.PA","sector":"Technology & Media",         "country":"France","mktcap_bn":22.4, "ev_bn":23.8, "revenue_mn":22065,"ebitda_mn":3088,"ebitda_margin_pct":14.0,"revenue_growth_pct":5.2, "net_debt_mn":1200, "net_debt_ebitda":0.39,"ev_ebitda":7.7,"ev_revenue":1.08,"pe_ntm":14.8,"roe_pct":20.4,"roic_pct":14.2,"current_ratio":1.22,"acq_score":82},
    {"name":"Dassault Systèmes","ticker":"DSY.PA","sector":"Technology & Media",        "country":"France","mktcap_bn":38.4, "ev_bn":42.6, "revenue_mn":6020, "ebitda_mn":1626,"ebitda_margin_pct":27.0,"revenue_growth_pct":8.4, "net_debt_mn":3600, "net_debt_ebitda":2.21,"ev_ebitda":26.2,"ev_revenue":7.08,"pe_ntm":31.4,"roe_pct":16.8,"roic_pct":11.2,"current_ratio":1.48,"acq_score":54},
    {"name":"Atos",            "ticker":"ATO.PA","sector":"Technology & Media",         "country":"France","mktcap_bn":0.4,  "ev_bn":3.2,  "revenue_mn":10694,"ebitda_mn":428, "ebitda_margin_pct":4.0, "revenue_growth_pct":-8.4, "net_debt_mn":2820, "net_debt_ebitda":6.59,"ev_ebitda":7.5,"ev_revenue":0.30,"pe_ntm":None,"roe_pct":-42.0,"roic_pct":-8.4,"current_ratio":0.72,"acq_score":22},
    {"name":"Vivendi",         "ticker":"VIV.PA","sector":"Technology & Media",         "country":"France","mktcap_bn":6.2,  "ev_bn":7.4,  "revenue_mn":9600, "ebitda_mn":1344,"ebitda_margin_pct":14.0,"revenue_growth_pct":-4.2, "net_debt_mn":740,  "net_debt_ebitda":0.55,"ev_ebitda":5.5,"ev_revenue":0.77,"pe_ntm":12.4,"roe_pct":6.8, "roic_pct":4.4, "current_ratio":0.94,"acq_score":70},
    {"name":"Worldline",       "ticker":"WLN.PA","sector":"Technology & Media",         "country":"France","mktcap_bn":1.8,  "ev_bn":5.6,  "revenue_mn":4604, "ebitda_mn":829, "ebitda_margin_pct":18.0,"revenue_growth_pct":2.2, "net_debt_mn":3480, "net_debt_ebitda":4.20,"ev_ebitda":6.8,"ev_revenue":1.22,"pe_ntm":5.8, "roe_pct":2.4, "roic_pct":1.8, "current_ratio":0.84,"acq_score":40},

    # ── INDUSTRIALS & ENGINEERING ──────────────────────────────────────────────
    {"name":"Bouygues",        "ticker":"EN.PA", "sector":"Industrials & Engineering",  "country":"France","mktcap_bn":9.8,  "ev_bn":14.2, "revenue_mn":54604,"ebitda_mn":3286,"ebitda_margin_pct":6.0, "revenue_growth_pct":3.4, "net_debt_mn":4380, "net_debt_ebitda":1.33,"ev_ebitda":4.3,"ev_revenue":0.26,"pe_ntm":8.4, "roe_pct":10.2,"roic_pct":6.8, "current_ratio":0.96,"acq_score":65},
    {"name":"Saint-Gobain",    "ticker":"SGO.PA","sector":"Industrials & Engineering",  "country":"France","mktcap_bn":26.8, "ev_bn":34.2, "revenue_mn":51910,"ebitda_mn":6229,"ebitda_margin_pct":12.0,"revenue_growth_pct":4.8, "net_debt_mn":6400, "net_debt_ebitda":1.03,"ev_ebitda":5.5,"ev_revenue":0.66,"pe_ntm":9.8, "roe_pct":14.2,"roic_pct":9.6, "current_ratio":1.08,"acq_score":74},
    {"name":"Legrand",         "ticker":"LR.PA", "sector":"Industrials & Engineering",  "country":"France","mktcap_bn":17.8, "ev_bn":20.4, "revenue_mn":8392, "ebitda_mn":2098,"ebitda_margin_pct":25.0,"revenue_growth_pct":2.8, "net_debt_mn":2480, "net_debt_ebitda":1.18,"ev_ebitda":9.7,"ev_revenue":2.43,"pe_ntm":17.4,"roe_pct":18.8,"roic_pct":12.4,"current_ratio":1.42,"acq_score":78},
    {"name":"Safran",          "ticker":"SAF.PA","sector":"Industrials & Engineering",  "country":"France","mktcap_bn":68.4, "ev_bn":72.8, "revenue_mn":23688,"ebitda_mn":5450,"ebitda_margin_pct":23.0,"revenue_growth_pct":17.2,"net_debt_mn":3800, "net_debt_ebitda":0.70,"ev_ebitda":13.4,"ev_revenue":3.07,"pe_ntm":22.8,"roe_pct":22.4,"roic_pct":16.2,"current_ratio":1.28,"acq_score":56},
    {"name":"Schneider Electric","ticker":"SU.PA","sector":"Industrials & Engineering", "country":"France","mktcap_bn":118.0,"ev_bn":128.0,"revenue_mn":35880,"ebitda_mn":7892,"ebitda_margin_pct":22.0,"revenue_growth_pct":13.6,"net_debt_mn":8400, "net_debt_ebitda":1.06,"ev_ebitda":16.2,"ev_revenue":3.57,"pe_ntm":22.4,"roe_pct":18.4,"roic_pct":14.2,"current_ratio":1.12,"acq_score":50},
    {"name":"Vallourec",       "ticker":"VK.PA", "sector":"Industrials & Engineering",  "country":"France","mktcap_bn":1.8,  "ev_bn":2.4,  "revenue_mn":4680, "ebitda_mn":842, "ebitda_margin_pct":18.0,"revenue_growth_pct":6.2, "net_debt_mn":580,  "net_debt_ebitda":0.69,"ev_ebitda":2.9,"ev_revenue":0.51,"pe_ntm":4.2, "roe_pct":16.8,"roic_pct":11.4,"current_ratio":1.62,"acq_score":85},

    # ── RETAIL & DISTRIBUTION ──────────────────────────────────────────────────
    {"name":"Carrefour",       "ticker":"CA.PA", "sector":"Retail & Distribution",      "country":"France","mktcap_bn":11.2, "ev_bn":19.8, "revenue_mn":94128,"ebitda_mn":3294,"ebitda_margin_pct":3.5, "revenue_growth_pct":3.6, "net_debt_mn":7400, "net_debt_ebitda":2.25,"ev_ebitda":6.0,"ev_revenue":0.21,"pe_ntm":8.2, "roe_pct":11.4,"roic_pct":5.8, "current_ratio":0.74,"acq_score":55},
    {"name":"Sodexo",          "ticker":"SW.PA", "sector":"Retail & Distribution",      "country":"France","mktcap_bn":8.4,  "ev_bn":12.2, "revenue_mn":23650,"ebitda_mn":1656,"ebitda_margin_pct":7.0, "revenue_growth_pct":8.4, "net_debt_mn":3540, "net_debt_ebitda":2.14,"ev_ebitda":7.4,"ev_revenue":0.52,"pe_ntm":13.4,"roe_pct":18.4,"roic_pct":10.2,"current_ratio":0.88,"acq_score":62},

    # ── ENERGY & UTILITIES ─────────────────────────────────────────────────────
    {"name":"TotalEnergies",   "ticker":"TTE.PA","sector":"Energy & Utilities",         "country":"France","mktcap_bn":148.0,"ev_bn":172.0,"revenue_mn":232988,"ebitda_mn":32200,"ebitda_margin_pct":13.8,"revenue_growth_pct":-12.4,"net_debt_mn":22800,"net_debt_ebitda":0.71,"ev_ebitda":5.3,"ev_revenue":0.74,"pe_ntm":7.8,"roe_pct":16.4,"roic_pct":12.2,"current_ratio":1.22,"acq_score":42},
    {"name":"Engie",           "ticker":"ENGI.PA","sector":"Energy & Utilities",        "country":"France","mktcap_bn":36.4, "ev_bn":72.4, "revenue_mn":82584,"ebitda_mn":7810,"ebitda_margin_pct":9.5, "revenue_growth_pct":-8.2, "net_debt_mn":34800,"net_debt_ebitda":4.46,"ev_ebitda":9.3,"ev_revenue":0.88,"pe_ntm":9.4, "roe_pct":12.8,"roic_pct":5.8, "current_ratio":0.94,"acq_score":38},
    {"name":"Veolia",          "ticker":"VIE.PA","sector":"Energy & Utilities",         "country":"France","mktcap_bn":12.8, "ev_bn":28.4, "revenue_mn":42885,"ebitda_mn":5788,"ebitda_margin_pct":13.5,"revenue_growth_pct":6.8, "net_debt_mn":15200,"net_debt_ebitda":2.63,"ev_ebitda":4.9,"ev_revenue":0.66,"pe_ntm":9.8, "roe_pct":8.4, "roic_pct":5.6, "current_ratio":0.82,"acq_score":60},

    # ── FINANCIAL SERVICES ─────────────────────────────────────────────────────
    {"name":"BNP Paribas",     "ticker":"BNP.PA","sector":"Financial Services",         "country":"France","mktcap_bn":64.8, "ev_bn":None, "revenue_mn":47212,"ebitda_mn":None,"ebitda_margin_pct":None,"revenue_growth_pct":8.4,"net_debt_mn":None, "net_debt_ebitda":None,"ev_ebitda":None,"ev_revenue":None,"pe_ntm":6.8,"roe_pct":10.2,"roic_pct":None,"current_ratio":None,"acq_score":30},
    {"name":"AXA",             "ticker":"CS.PA", "sector":"Financial Services",         "country":"France","mktcap_bn":70.2, "ev_bn":None, "revenue_mn":104502,"ebitda_mn":None,"ebitda_margin_pct":None,"revenue_growth_pct":6.2,"net_debt_mn":None, "net_debt_ebitda":None,"ev_ebitda":None,"ev_revenue":None,"pe_ntm":9.4,"roe_pct":14.4,"roic_pct":None,"current_ratio":None,"acq_score":28},

    # ── REAL ESTATE ────────────────────────────────────────────────────────────
    {"name":"Unibail-Rodamco", "ticker":"URW.AS","sector":"Real Estate",                "country":"France","mktcap_bn":9.6,  "ev_bn":28.4, "revenue_mn":2420, "ebitda_mn":1694,"ebitda_margin_pct":70.0,"revenue_growth_pct":4.2, "net_debt_mn":17200,"net_debt_ebitda":10.15,"ev_ebitda":16.8,"ev_revenue":11.73,"pe_ntm":4.8,"roe_pct":4.2,"roic_pct":2.8,"current_ratio":0.48,"acq_score":18},
    {"name":"Covivio",         "ticker":"COV.PA","sector":"Real Estate",                "country":"France","mktcap_bn":3.2,  "ev_bn":10.8, "revenue_mn":648,  "ebitda_mn":454, "ebitda_margin_pct":70.1,"revenue_growth_pct":2.4, "net_debt_mn":6820, "net_debt_ebitda":15.02,"ev_ebitda":23.8,"ev_revenue":16.67,"pe_ntm":6.2,"roe_pct":2.8,"roic_pct":1.8,"current_ratio":0.42,"acq_score":15},
]


def get_static_df() -> pd.DataFrame:
    """Convert STATIC_COMPANIES to a scored DataFrame."""
    df = pd.DataFrame(STATIC_COMPANIES)
    df = df.rename(columns={
        "name":                "Company",
        "ticker":              "Ticker",
        "sector":              "Sector",
        "mktcap_bn":           "Mkt Cap (€bn)",
        "ev_bn":               "EV (€bn)",
        "revenue_mn":          "Revenue (€mn)",
        "ebitda_mn":           "EBITDA (€mn)",
        "ebitda_margin_pct":   "EBITDA Margin %",
        "revenue_growth_pct":  "Rev Growth %",
        "net_debt_mn":         "Net Debt (€mn)",
        "net_debt_ebitda":     "ND/EBITDA",
        "ev_ebitda":           "EV/EBITDA",
        "ev_revenue":          "EV/Revenue",
        "pe_ntm":              "NTM P/E",
        "roe_pct":             "ROE %",
        "roic_pct":            "ROIC %",
        "current_ratio":       "Current Ratio",
        "acq_score":           "Score",
        "country":             "Country",
    })
    return df.reset_index(drop=True)


# ── Static financial data (5-year IS stub) ───────────────────────────────────
_STATIC_FIN = {
    "KER.PA": {"revenue":[17026,17640,20351,21212,18890],"ebitda":[3850,4120,5296,5940,4420],"ebit":[3100,3300,4400,5020,3600],"net_income":[2100,2300,3580,3900,2200],"years":[2020,2021,2022,2023,2024]},
    "MC.PA":  {"revenue":[44651,64215,79184,86153,83964],"ebitda":[10888,18982,25604,22836,21400],"ebit":[8304,17151,22987,20476,18800],"net_income":[4702,12036,14084,11801,10200],"years":[2020,2021,2022,2023,2024]},
    "RCO.PA": {"revenue":[960,1071,1317,1490,1236],"ebitda":[192,268,395,420,300],"ebit":[148,212,320,340,220],"net_income":[90,148,238,260,140],"years":[2020,2021,2022,2023,2024]},
    "RI.PA":  {"revenue":[8824,8824,10701,11598,11028],"ebitda":[2204,2645,3457,3248,2920],"ebit":[1765,2204,2888,2760,2400],"net_income":[1212,1522,2040,2012,1750],"years":[2020,2021,2022,2023,2024]},
    "RMS.PA": {"revenue":[6389,8982,11601,13427,14400],"ebitda":[2042,3273,4930,6040,6840],"ebit":[1822,2987,4556,5653,6400],"net_income":[1385,2445,3367,4311,4800],"years":[2020,2021,2022,2023,2024]},
    "IPN.PA": {"revenue":[2499,2715,3018,3304,3580],"ebitda":[749,868,998,1124,1254],"ebit":[562,650,780,882,980],"net_income":[374,445,550,620,710],"years":[2020,2021,2022,2023,2024]},
    "BIM.PA": {"revenue":[3136,3560,3800,3960,4150],"ebitda":[600,748,856,950,1020],"ebit":[456,580,668,740,810],"net_income":[290,390,460,530,580],"years":[2020,2021,2022,2023,2024]},
    "SAN.PA": {"revenue":[36041,37761,37762,40598,42800],"ebitda":[8000,8980,9200,9840,10200],"ebit":[6200,7100,7400,8000,8400],"net_income":[3854,5481,4996,5870,6200],"years":[2020,2021,2022,2023,2024]},
    "ERF.PA": {"revenue":[5369,5437,6730,6710,6920],"ebitda":[1128,1250,1479,1475,1550],"ebit":[720,840,1020,1050,1100],"net_income":[432,510,620,650,700],"years":[2020,2021,2022,2023,2024]},
    "CAP.PA": {"revenue":[15849,18161,21991,22065,23200],"ebitda":[1759,2052,2856,3088,3360],"ebit":[1268,1568,2180,2380,2600],"net_income":[836,1052,1440,1622,1800],"years":[2020,2021,2022,2023,2024]},
    "DSY.PA": {"revenue":[4452,4894,5740,6020,6380],"ebitda":[1068,1322,1661,1626,1850],"ebit":[804,1010,1280,1240,1440],"net_income":[530,740,900,860,1020],"years":[2020,2021,2022,2023,2024]},
    "ATO.PA": {"revenue":[11184,11304,11345,10694,9400],"ebitda":[1006,900,700,428,320],"ebit":[504,380,240,-120,-280],"net_income":[-1900,-2970,-1044,-3980,-820],"years":[2020,2021,2022,2023,2024]},
    "VIV.PA": {"revenue":[8640,9600,9600,9600,9200],"ebitda":[1210,1344,1344,1344,1290],"ebit":[820,940,940,940,880],"net_income":[280,380,420,480,360],"years":[2020,2021,2022,2023,2024]},
    "WLN.PA": {"revenue":[3779,4264,4596,4604,4680],"ebitda":[698,783,880,829,860],"ebit":[420,486,560,500,520],"net_income":[286,350,380,180,120],"years":[2020,2021,2022,2023,2024]},
    "EN.PA":  {"revenue":[37966,43417,51424,54604,56800],"ebitda":[2278,2604,3085,3286,3420],"ebit":[1518,1780,2140,2260,2350],"net_income":[808,1042,1322,1386,1450],"years":[2020,2021,2022,2023,2024]},
    "SGO.PA": {"revenue":[38140,44283,51172,51910,53200],"ebitda":[4576,5314,6144,6229,6500],"ebit":[2664,3274,4080,4296,4500],"net_income":[1590,2134,2716,2924,3100],"years":[2020,2021,2022,2023,2024]},
    "LR.PA":  {"revenue":[6073,6903,8012,8392,8680],"ebitda":[1518,1898,2204,2098,2250],"ebit":[1094,1400,1660,1588,1720],"net_income":[754,1000,1228,1174,1280],"years":[2020,2021,2022,2023,2024]},
    "SAF.PA": {"revenue":[16495,15884,19033,23688,26800],"ebitda":[2798,2618,4078,5450,6440],"ebit":[1798,1680,2940,4180,5020],"net_income":[1098,952,1820,2990,3600],"years":[2020,2021,2022,2023,2024]},
    "SU.PA":  {"revenue":[25159,28904,34169,35880,38200],"ebitda":[4278,5205,7160,7892,8640],"ebit":[3094,3868,5580,6320,6980],"net_income":[1948,2490,3560,4286,4780],"years":[2020,2021,2022,2023,2024]},
    "VK.PA":  {"revenue":[3280,3900,4380,4680,4820],"ebitda":[492,664,788,842,900],"ebit":[328,468,590,640,680],"net_income":[164,260,350,420,480],"years":[2020,2021,2022,2023,2024]},
    "CA.PA":  {"revenue":[78536,83907,90916,94128,96400],"ebitda":[2826,3024,3183,3294,3400],"ebit":[1356,1504,1644,1744,1820],"net_income":[760,904,1006,1040,1080],"years":[2020,2021,2022,2023,2024]},
    "SW.PA":  {"revenue":[19311,19337,21072,23650,25400],"ebitda":[1158,1546,1655,1656,1780],"ebit":[772,1062,1124,1124,1220],"net_income":[388,634,700,714,800],"years":[2020,2021,2022,2023,2024]},
    "TTE.PA": {"revenue":[119704,184671,263310,232988,212000],"ebitda":[17800,28400,48200,32200,28400],"ebit":[12600,20800,36800,24800,21200],"net_income":[4080,13632,20526,19244,17200],"years":[2020,2021,2022,2023,2024]},
    "ENGI.PA":{"revenue":[55748,57938,93864,82584,76400],"ebitda":[4464,6236,9386,7810,7200],"ebit":[2232,3860,6240,5180,4800],"net_income":[-1522,2784,4200,2440,2200],"years":[2020,2021,2022,2023,2024]},
    "VIE.PA": {"revenue":[25969,28508,42886,42885,45200],"ebitda":[3896,4562,6433,5788,6240],"ebit":[2338,2970,4344,4004,4320],"net_income":[820,1404,1848,1820,2000],"years":[2020,2021,2022,2023,2024]},
    "BNP.PA": {"revenue":[44275,46235,50418,47212,48800],"ebitda":[None,None,None,None,None],"ebit":[None,None,None,None,None],"net_income":[7067,9488,10196,11028,11400],"years":[2020,2021,2022,2023,2024]},
    "CS.PA":  {"revenue":[96210,103676,99916,104502,110000],"ebitda":[None,None,None,None,None],"ebit":[None,None,None,None,None],"net_income":[3161,7290,7284,6847,7200],"years":[2020,2021,2022,2023,2024]},
    "URW.AS": {"revenue":[1624,1890,2180,2420,2560],"ebitda":[1137,1323,1526,1694,1792],"ebit":[780,900,1060,1200,1280],"net_income":[-3500,-1200,600,820,900],"years":[2020,2021,2022,2023,2024]},
    "COV.PA": {"revenue":[440,520,596,648,680],"ebitda":[308,364,417,454,476],"ebit":[220,260,300,330,348],"net_income":[-580,-120,140,180,200],"years":[2020,2021,2022,2023,2024]},
}

def get_static_financials(ticker: str) -> dict:
    """Return 5-year income statement for a given ticker."""
    data = _STATIC_FIN.get(ticker)
    if not data:
        # Generic fallback
        rev = 2000
        return {
            "years": [2020,2021,2022,2023,2024],
            "revenue":    [int(rev*0.8), int(rev*0.88), int(rev*0.94), rev, int(rev*1.06)],
            "ebitda":     [int(rev*0.14), int(rev*0.15), int(rev*0.16), int(rev*0.17), int(rev*0.18)],
            "ebit":       [int(rev*0.10), int(rev*0.11), int(rev*0.12), int(rev*0.13), int(rev*0.14)],
            "net_income": [int(rev*0.06), int(rev*0.07), int(rev*0.08), int(rev*0.08), int(rev*0.09)],
            "ebitda_margin": [14.0, 15.0, 16.0, 17.0, 18.0],
            "ebit_margin":   [10.0, 11.0, 12.0, 13.0, 14.0],
        }
    rev = data["revenue"]
    ebitda = data["ebitda"]
    ebit   = data["ebit"]
    em = [round(e/r*100, 1) if e and r else None for e, r in zip(ebitda, rev)]
    im = [round(e/r*100, 1) if e and r else None for e, r in zip(ebit, rev)]
    return {
        "years":        data["years"],
        "revenue":      rev,
        "ebitda":       ebitda,
        "ebit":         ebit,
        "net_income":   data["net_income"],
        "ebitda_margin": em,
        "ebit_margin":   im,
    }
