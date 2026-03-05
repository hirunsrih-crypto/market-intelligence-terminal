"""
Fund flow data.
For MVP, returns static/manually-updated JSON.
Replace with SETTRADE scrape or EPFR API for live data.

Sources:
  - Thailand: https://www.settrade.com/en/market-data/overview (Foreign net buy/sell)
  - India: https://www.fpi.nsdl.co.in/ (FPI equity flows)
  - Vietnam: SSC / HOSE daily trading summary
  - Global: EPFR Global (paid)
"""

import json
import os
import logging
from datetime import date

logger = logging.getLogger(__name__)

FLOWS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "flows.json")


def get_fund_flows() -> dict:
    today = date.today().isoformat()
    try:
        if os.path.exists(FLOWS_FILE):
            with open(FLOWS_FILE) as f:
                data = json.load(f)
            return data.get(today, data.get("latest", _sample_flows()))
    except Exception as e:
        logger.error(f"Flow data load error: {e}")
    return _sample_flows()


def _sample_flows() -> dict:
    return {
        "date": date.today().isoformat(),
        "markets": [
            {
                "market": "Thailand SET",
                "region": "TH",
                "foreign_net": -1250.5,
                "foreign_buy": 8430.2,
                "foreign_sell": 9680.7,
                "unit": "MB",
                "note": "Million Baht",
            },
            {
                "market": "India NSE",
                "region": "IN",
                "foreign_net": 3200.0,
                "foreign_buy": 15400.0,
                "foreign_sell": 12200.0,
                "unit": "Cr",
                "note": "Crore INR",
            },
            {
                "market": "Vietnam HOSE",
                "region": "VN",
                "foreign_net": -120.3,
                "foreign_buy": 540.1,
                "foreign_sell": 660.4,
                "unit": "Bn VND",
                "note": "Billion VND",
            },
            {
                "market": "Israel TASE",
                "region": "IL",
                "foreign_net": 45.0,
                "foreign_buy": 230.0,
                "foreign_sell": 185.0,
                "unit": "M ILS",
                "note": "Million ILS",
            },
        ],
        "global": {
            "em_equity_flows": -800,
            "dm_equity_flows": 1200,
            "bond_flows": 500,
            "unit": "M USD",
            "source": "EPFR (Weekly)",
        },
    }
