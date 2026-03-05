"""
Fetch US Treasury yields from FRED (Federal Reserve Economic Data).
Get a free API key at: https://fred.stlouisfed.org/docs/api/api_key.html
"""

import logging
import os

logger = logging.getLogger(__name__)

FRED_SERIES = {
    "US 2Y":  "DGS2",
    "US 5Y":  "DGS5",
    "US 10Y": "DGS10",
    "US 30Y": "DGS30",
}


class FREDFetcher:
    def __init__(self):
        api_key = os.getenv("FRED_API_KEY", "")
        self.fred = None
        if api_key:
            try:
                from fredapi import Fred
                self.fred = Fred(api_key=api_key)
            except Exception as e:
                logger.error(f"Failed to initialize FRED: {e}")

    def get_us_yields(self) -> list:
        if not self.fred:
            return self._fallback()

        results = []
        for name, sid in FRED_SERIES.items():
            try:
                data = self.fred.get_series(sid, observation_start="2024-01-01")
                clean = data.dropna()
                if len(clean) < 2:
                    continue
                current  = float(clean.iloc[-1])
                previous = float(clean.iloc[-2])
                results.append({
                    "name":   name,
                    "yield":  round(current, 3),
                    "change": round(current - previous, 4),
                    "maturity": int(name.split()[1].replace("Y", "")),
                })
            except Exception as e:
                logger.error(f"FRED fetch error for {sid}: {e}")
        return results

    def _fallback(self) -> list:
        """Return empty list when FRED is unavailable."""
        return []
