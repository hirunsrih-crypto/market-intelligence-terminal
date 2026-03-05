"""
Core data fetcher using tvdatafeed.
Handles connection management, retries, and data normalization.
"""

import logging
from typing import Optional
import pandas as pd

logger = logging.getLogger(__name__)


class TVFetcher:
    """
    Wrapper around tvdatafeed.
    Initializes a persistent TvDatafeed session and fetches normalized market data.
    """

    def __init__(self, username: str = None, password: str = None):
        try:
            from tvDatafeed import TvDatafeed
            if username and password:
                self.tv = TvDatafeed(username, password)
            else:
                self.tv = TvDatafeed()
        except Exception as e:
            logger.error(f"Failed to initialize TvDatafeed: {e}")
            self.tv = None

    def _fetch(self, symbol: str, exchange: str, interval, n_bars: int) -> Optional[pd.DataFrame]:
        if not self.tv:
            return None
        try:
            df = self.tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=n_bars)
            if df is None or df.empty:
                logger.warning(f"No data for {symbol}:{exchange}")
                return None
            return df
        except Exception as e:
            logger.error(f"Error fetching {symbol}:{exchange}: {e}")
            return None

    def get_latest_price(self, symbol_key: str, registry: dict) -> dict:
        from config import DAILY_INTERVAL, DAILY_BARS
        if symbol_key not in registry:
            return {"value": None, "change": None}

        tv_symbol, tv_exchange = registry[symbol_key]
        df = self._fetch(tv_symbol, tv_exchange, DAILY_INTERVAL, 2)

        if df is None or len(df) < 2:
            return {"value": None, "change": None}

        current  = df.iloc[-1]["close"]
        previous = df.iloc[-2]["close"]
        change_pct = ((current - previous) / previous) * 100

        return {"value": round(float(current), 2), "change": round(float(change_pct), 2)}

    def get_intraday(self, symbol_key: str, registry: dict) -> list:
        from config import INTRADAY_INTERVAL, INTRADAY_BARS
        if symbol_key not in registry:
            return []

        tv_symbol, tv_exchange = registry[symbol_key]
        df = self._fetch(tv_symbol, tv_exchange, INTRADAY_INTERVAL, INTRADAY_BARS)

        if df is None:
            return []

        records = []
        for idx, row in df.iterrows():
            records.append({
                "time":   idx.strftime("%H:%M"),
                "open":   round(float(row["open"]),  2),
                "high":   round(float(row["high"]),  2),
                "low":    round(float(row["low"]),   2),
                "price":  round(float(row["close"]), 2),
                "volume": int(row["volume"]) if pd.notna(row["volume"]) else 0,
            })
        return records

    def fetch_all_indices(self) -> list:
        from config import EQUITY_SYMBOLS, EQUITY_META
        results = []
        for key in EQUITY_SYMBOLS:
            price_data = self.get_latest_price(key, EQUITY_SYMBOLS)
            info = EQUITY_META.get(key, {"name": key, "region": "??", "currency": "??"})
            results.append({"ticker": key, **info, **price_data})
        return results

    def fetch_all_fx(self) -> list:
        from config import FX_SYMBOLS
        results = []
        for key in FX_SYMBOLS:
            data = self.get_latest_price(key, FX_SYMBOLS)
            results.append({
                "pair":   key[:3] + "/" + key[3:],
                "ticker": key,
                "rate":   data["value"],
                "change": data["change"],
            })
        return results

    def fetch_all_commodities(self) -> list:
        from config import COMMODITY_SYMBOLS, COMMODITY_UNITS
        results = []
        for key in COMMODITY_SYMBOLS:
            data = self.get_latest_price(key, COMMODITY_SYMBOLS)
            results.append({
                "name":   key.title(),
                "ticker": key,
                "value":  data["value"],
                "unit":   COMMODITY_UNITS.get(key, ""),
                "change": data["change"],
            })
        return results

    def fetch_vix(self) -> Optional[float]:
        from config import VOLATILITY_SYMBOLS
        data = self.get_latest_price("VIX", VOLATILITY_SYMBOLS)
        return data["value"]

    def fetch_crypto(self) -> list:
        from config import CRYPTO_SYMBOLS, CRYPTO_META
        results = []
        for key in CRYPTO_SYMBOLS:
            data = self.get_latest_price(key, CRYPTO_SYMBOLS)
            results.append({
                "name":   CRYPTO_META.get(key, key),
                "ticker": key,
                "value":  data["value"],
                "change": data["change"],
            })
        return results

    def fetch_all_intraday(self) -> dict:
        from config import INTRADAY_SYMBOLS, EQUITY_SYMBOLS
        result = {}
        for sym in INTRADAY_SYMBOLS:
            result[sym] = self.get_intraday(sym, EQUITY_SYMBOLS)
        return result
