"""
tvDatafeed — vendored WebSocket-based TradingView data fetcher.
No Selenium or Chrome required. Uses no-login mode (public data).
"""

import datetime
import enum
import json
import logging
import random
import re
import string

import pandas as pd
from websocket import create_connection

logger = logging.getLogger(__name__)


class Interval(enum.Enum):
    in_1_minute  = "1"
    in_3_minute  = "3"
    in_5_minute  = "5"
    in_15_minute = "15"
    in_30_minute = "30"
    in_45_minute = "45"
    in_1_hour    = "1H"
    in_2_hour    = "2H"
    in_3_hour    = "3H"
    in_4_hour    = "4H"
    in_daily     = "1D"
    in_weekly    = "1W"
    in_monthly   = "1M"


class TvDatafeed:
    _headers = json.dumps({"Origin": "https://data.tradingview.com"})

    def __init__(self, username: str = None, password: str = None):
        # No-login mode — works for all public symbols
        self.token = "unauthorized_user_token"
        if username or password:
            logger.warning(
                "Credential-based login is not supported in this vendored version. "
                "Using no-login mode (public data only)."
            )
        self.ws = None

    # ── WebSocket helpers ──────────────────────────────────────────────────

    def _connect(self):
        self.ws = create_connection(
            "wss://data.tradingview.com/socket.io/websocket",
            headers=self._headers,
        )

    @staticmethod
    def _generate_session(prefix: str) -> str:
        suffix = "".join(random.choices(string.ascii_lowercase, k=12))
        return prefix + suffix

    @staticmethod
    def _prepend_header(text: str) -> str:
        return f"~m~{len(text)}~m~{text}"

    @staticmethod
    def _build_message(func: str, params: list) -> str:
        return json.dumps({"m": func, "p": params}, separators=(",", ":"))

    def _send(self, func: str, params: list):
        msg = self._prepend_header(self._build_message(func, params))
        self.ws.send(msg)

    # ── Data parsing ───────────────────────────────────────────────────────

    @staticmethod
    def _parse_data(raw: str, symbol: str) -> pd.DataFrame:
        """Parse TradingView WebSocket frames using JSON — no fragile regex splits."""
        rows = []
        for line in raw.split("\n"):
            # Each frame: ~m~<len>~m~<json>
            for part in re.split(r"~m~\d+~m~", line):
                part = part.strip()
                if not part:
                    continue
                try:
                    msg = json.loads(part)
                    if msg.get("m") not in ("timescale_update", "du"):
                        continue
                    payload = msg.get("p", [])
                    if len(payload) < 2 or not isinstance(payload[1], dict):
                        continue
                    for series in payload[1].values():
                        if not isinstance(series, dict) or "s" not in series:
                            continue
                        for bar in series["s"]:
                            v = bar.get("v", [])
                            if len(v) >= 6:
                                ts = datetime.datetime.fromtimestamp(float(v[0]))
                                rows.append([ts, float(v[1]), float(v[2]),
                                             float(v[3]), float(v[4]), float(v[5])])
                except (json.JSONDecodeError, KeyError, TypeError, ValueError):
                    continue

        if not rows:
            logger.error(f"No data parsed for {symbol}. Check exchange/symbol.")
            return None

        df = pd.DataFrame(
            rows, columns=["datetime", "open", "high", "low", "close", "volume"]
        ).set_index("datetime")
        df.insert(0, "symbol", symbol)
        return df

    @staticmethod
    def _format_symbol(symbol: str, exchange: str, contract: int = None) -> str:
        if ":" in symbol:
            return symbol
        if contract is None:
            return f"{exchange}:{symbol}"
        if isinstance(contract, int):
            return f"{exchange}:{symbol}{contract}!"
        raise ValueError("contract must be an int or None")

    # ── Public API ─────────────────────────────────────────────────────────

    def get_hist(
        self,
        symbol: str,
        exchange: str = "NSE",
        interval: Interval = Interval.in_daily,
        n_bars: int = 10,
        fut_contract: int = None,
        extended_session: bool = False,
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV bars from TradingView.

        Args:
            symbol:           TradingView symbol name
            exchange:         Exchange code (e.g. 'NSE', 'SET', 'NASDAQ')
            interval:         Bar interval (Interval enum)
            n_bars:           Number of bars to fetch (max ~5000)
            fut_contract:     None for spot, 1 for front month futures
            extended_session: Include pre/post market if True

        Returns:
            pd.DataFrame with columns: symbol, open, high, low, close, volume
        """
        full_symbol = self._format_symbol(symbol, exchange, fut_contract)
        chart_session = self._generate_session("cs_")
        quote_session = self._generate_session("qs_")

        try:
            self._connect()

            self._send("set_auth_token",      [self.token])
            self._send("chart_create_session",[chart_session, ""])
            self._send("quote_create_session",[quote_session])
            self._send("quote_set_fields", [
                quote_session, "ch", "chp", "current_session", "description",
                "local_description", "language", "exchange", "fractional",
                "is_tradable", "lp", "lp_time", "minmov", "minmove2",
                "original_name", "pricescale", "pro_name", "short_name",
                "type", "update_mode", "volume", "currency_code",
            ])
            self._send("quote_add_symbols",  [quote_session, full_symbol, {"flags": ["force_permission"]}])
            self._send("quote_fast_symbols", [quote_session, full_symbol])
            self._send("resolve_symbol", [
                chart_session,
                "symbol_1",
                '={"symbol":"' + full_symbol + '","adjustment":"splits","session":'
                + ('"regular"' if not extended_session else '"extended"') + "}",
            ])
            self._send("create_series",   [chart_session, "s1", "s1", "symbol_1", interval.value, n_bars])
            self._send("switch_timezone", [chart_session, "exchange"])

            raw = ""
            while True:
                try:
                    result = self.ws.recv()
                    raw += result + "\n"
                except Exception as e:
                    logger.error(f"WebSocket recv error: {e}")
                    break
                if "series_completed" in result:
                    break

            return self._parse_data(raw, full_symbol)

        except Exception as e:
            logger.error(f"get_hist failed for {full_symbol}: {e}")
            return None
        finally:
            if self.ws:
                try:
                    self.ws.close()
                except Exception:
                    pass
                self.ws = None
