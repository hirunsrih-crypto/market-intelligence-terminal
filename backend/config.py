"""
Symbol registry for tvdatafeed.
Each entry maps a dashboard key to (tv_symbol, tv_exchange).
"""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    from tvDatafeed import Interval
    INTRADAY_INTERVAL = Interval.in_5_minute
    DAILY_INTERVAL    = Interval.in_daily
except ImportError:
    INTRADAY_INTERVAL = None
    DAILY_INTERVAL    = None

TV_USERNAME  = os.getenv("TV_USERNAME", "")
TV_PASSWORD  = os.getenv("TV_PASSWORD", "")
FRED_API_KEY = os.getenv("FRED_API_KEY", "")

INTRADAY_BARS = 500
DAILY_BARS    = 30

# ─── Equity Indices ───────────────────────────────────────
EQUITY_SYMBOLS = {
    "SPX":       ("SPX500USD",  "OANDA"),
    "IXIC":      ("IXIC",       "NASDAQ"),
    "DJI":       ("DJI",        "DJ"),
    "SET":       ("SET",        "SET"),
    "SET50":     ("SET50",      "SET"),
    "NIFTY":     ("NIFTY",      "NSE"),
    "SENSEX":    ("SENSEX",     "BSE"),
    "BANKNIFTY": ("BANKNIFTY",  "NSE"),
    "TA35":      ("TA35",       "TASE"),
    "TA125":     ("TA125",      "TASE"),
    "VNINDEX":   ("VNINDEX",    "HOSE"),
    "VN30":      ("VN30",       "HOSE"),
    "HNX":       ("HNXINDEX",   "HNX"),
    "N225":      ("NI225",      "TVC"),
    "HSI":       ("HSI",        "HKEX"),
    "KS11":      ("KOSPI",      "KRX"),
    "FTSE":      ("UKX",        "FTSE"),
    "DAX":       ("DEU40",      "PEPPERSTONE"),
    "SX5E":      ("SX5E",       "EUREX"),
    "CSI300":    ("CSI300",     "SSE"),
}

EQUITY_META = {
    "SPX":       {"name": "S&P 500",      "region": "US", "currency": "USD"},
    "IXIC":      {"name": "NASDAQ",       "region": "US", "currency": "USD"},
    "DJI":       {"name": "Dow Jones",    "region": "US", "currency": "USD"},
    "SET":       {"name": "SET Index",    "region": "TH", "currency": "THB"},
    "SET50":     {"name": "SET50",        "region": "TH", "currency": "THB"},
    "NIFTY":     {"name": "Nifty 50",     "region": "IN", "currency": "INR"},
    "SENSEX":    {"name": "BSE Sensex",   "region": "IN", "currency": "INR"},
    "BANKNIFTY": {"name": "Nifty Bank",   "region": "IN", "currency": "INR"},
    "TA35":      {"name": "TA-35",        "region": "IL", "currency": "ILS"},
    "TA125":     {"name": "TA-125",       "region": "IL", "currency": "ILS"},
    "VNINDEX":   {"name": "VN-Index",     "region": "VN", "currency": "VND"},
    "VN30":      {"name": "VN30",         "region": "VN", "currency": "VND"},
    "HNX":       {"name": "HNX-Index",    "region": "VN", "currency": "VND"},
    "N225":      {"name": "Nikkei 225",   "region": "JP", "currency": "JPY"},
    "HSI":       {"name": "Hang Seng",    "region": "HK", "currency": "HKD"},
    "KS11":      {"name": "KOSPI",        "region": "KR", "currency": "KRW"},
    "FTSE":      {"name": "FTSE 100",     "region": "UK", "currency": "GBP"},
    "DAX":       {"name": "DAX",          "region": "DE", "currency": "EUR"},
    "SX5E":      {"name": "Euro Stoxx 50","region": "EU", "currency": "EUR"},
    "CSI300":    {"name": "CSI 300",      "region": "CN", "currency": "CNY"},
}

# ─── FX Pairs ─────────────────────────────────────────────
FX_SYMBOLS = {
    "USDTHB": ("USDTHB", "FX_IDC"),
    "EURUSD": ("EURUSD", "FX_IDC"),
    "USDJPY": ("USDJPY", "FX_IDC"),
    "GBPUSD": ("GBPUSD", "FX_IDC"),
    "USDCNY": ("USDCNY", "FX_IDC"),
    "EURTHB": ("EURTHB", "FX_IDC"),
    "USDINR": ("USDINR", "FX_IDC"),
    "USDILS": ("USDILS", "FX_IDC"),
    "USDVND": ("USDVND", "FX_IDC"),
}

# ─── Commodities ──────────────────────────────────────────
COMMODITY_SYMBOLS = {
    "GOLD":   ("XAUUSD", "OANDA"),
    "BRENT":  ("UKOIL",  "TVC"),
    "WTI":    ("USOIL",  "TVC"),
    "SILVER": ("XAGUSD", "OANDA"),
    "COPPER": ("COPPER", "COMEX"),
    "NATGAS": ("NGAS",   "TVC"),
}

COMMODITY_UNITS = {
    "GOLD": "USD/oz", "BRENT": "USD/bbl", "WTI": "USD/bbl",
    "SILVER": "USD/oz", "COPPER": "USD/lb", "NATGAS": "USD/MMBtu",
}

# ─── Volatility ───────────────────────────────────────────
VOLATILITY_SYMBOLS = {
    "VIX": ("VIX", "CBOE"),
}

# ─── Crypto ───────────────────────────────────────────────
CRYPTO_SYMBOLS = {
    "BTC": ("BTCUSD", "COINBASE"),
    "ETH": ("ETHUSD", "COINBASE"),
}

CRYPTO_META = {
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
}

# ─── INTRADAY symbols to track ────────────────────────────
INTRADAY_SYMBOLS = ["SPX", "SET", "NIFTY", "VNINDEX"]
