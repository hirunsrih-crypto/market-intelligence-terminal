"""
tvDatafeed — vendored WebSocket-based TradingView data fetcher.
Authenticates via TradingView username/password using their sign-in API.
Falls back to no-login mode if credentials are not provided.
"""

import datetime
import enum
import json
import logging
import random
import re
import string

import requests
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
    _sign_in_url = "https://www.tradingview.com/accounts/signin/"

    def __init__(self, username: str = None, password: str = None):
        import os
        self._session_id = os.getenv("TV_SESSION_ID", "").strip()
        self._username = username
        self._password = password
        self.token = self._get_token()
        self._token_time = datetime.datetime.now()
        self.ws = None

    def _refresh_token_if_needed(self):
        """Auto-refresh JWT if older than 3 hours."""
        age = (datetime.datetime.now() - self._token_time).total_seconds()
        if age > 3 * 3600:
            logger.info("Token older than 3 hours — refreshing...")
            self.token = self._get_token()
            self._token_time = datetime.datetime.now()

    def _get_token(self) -> str:
        import os

        # Priority 1: pre-fetched JWT token (manual, expires in ~4 hours)
        direct_token = os.getenv("TV_AUTH_TOKEN", "").strip()
        if direct_token:
            logger.info("Using TV_AUTH_TOKEN from environment")
            return direct_token

        # Priority 2: use session ID cookie to fetch fresh JWT (lasts weeks/months)
        if self._session_id:
            token = self._token_from_session(self._session_id)
            if token:
                return token

        # Priority 3: login via API (may be blocked from cloud IPs)
        if self._username and self._password:
            token = self._token_from_login(self._username, self._password)
            if token:
                return token

        logger.warning("No credentials — using no-login mode (limited data)")
        return "unauthorized_user_token"

    def _token_from_session(self, session_id: str) -> str:
        """Use the long-lived sessionid cookie to get a fresh JWT auth token."""
        try:
            resp = requests.get(
                "https://www.tradingview.com/chart/",
                cookies={"sessionid": session_id},
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                },
                timeout=15,
            )
            match = re.search(r'"auth_token":"([^"]+)"', resp.text)
            if match:
                token = match.group(1)
                logger.info("Got fresh JWT from session ID cookie")
                return token

            # Try alternative pattern
            match = re.search(r'authToken\\":\\"([^\\]+)\\"', resp.text)
            if match:
                token = match.group(1)
                logger.info("Got fresh JWT from session ID cookie (alt pattern)")
                return token

            logger.error("Session ID valid but could not extract auth_token from page")
            return None
        except Exception as e:
            logger.error(f"Session-based token refresh failed: {e}")
            return None

    def _token_from_login(self, username: str, password: str) -> str:
        """Login via TradingView API — may be blocked from cloud IPs."""
        try:
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.tradingview.com",
                "Origin": "https://www.tradingview.com",
            })
            resp = session.post(
                self._sign_in_url,
                data={"username": username, "password": password, "remember": "on"},
                timeout=15,
            )
            data = resp.json()
            if "error" in data:
                logger.error(f"TradingView login failed: {data['error']}")
                return None
            token = data.get("user", {}).get("auth_token", "")
            if token:
                logger.info("TradingView login successful")
                return token
            return None
        except Exception as e:
            logger.error(f"TradingView login error: {e}")
            return None

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
        """Parse TradingView WebSocket frames — searches all message types for series data."""
        rows = []
        seen_types = set()

        for line in raw.split("\n"):
            for part in re.split(r"~m~\d+~m~", line):
                part = part.strip()
                if not part:
                    continue
                try:
                    msg = json.loads(part)
                    msg_type = msg.get("m", "")
                    seen_types.add(msg_type)

                    payload = msg.get("p", [])
                    # Search every dict in payload for series data
                    for item in payload:
                        if not isinstance(item, dict):
                            continue
                        for val in item.values():
                            if not isinstance(val, dict) or "s" not in val:
                                continue
                            for bar in val["s"]:
                                v = bar.get("v", [])
                                if len(v) >= 6:
                                    try:
                                        ts = datetime.datetime.fromtimestamp(float(v[0]))
                                        rows.append([ts, float(v[1]), float(v[2]),
                                                     float(v[3]), float(v[4]), float(v[5])])
                                    except (ValueError, TypeError):
                                        continue
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue

        logger.info(f"Parsed {len(rows)} rows for {symbol}. Message types seen: {seen_types}")

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
        self._refresh_token_if_needed()
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

            # Log a sample of raw data to diagnose parsing issues
            sample = raw[:2000] if len(raw) > 2000 else raw
            logger.debug(f"RAW SAMPLE for {full_symbol}: {repr(sample)}")
            logger.info(f"RAW LENGTH for {full_symbol}: {len(raw)} chars, contains 'series_completed': {'series_completed' in raw}, contains '\"s\":[': {'\"s\":[' in raw}")

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
