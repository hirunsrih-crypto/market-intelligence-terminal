"""
APScheduler jobs for periodic cache refresh.

Schedule:
  - Equity indices:   every 1 min
  - FX rates:         every 1 min
  - Commodities:      every 5 min
  - VIX:              every 1 min
  - Bond yields:      every 30 min
  - Intraday bars:    every 5 min
  - Economic calendar: every 15 min
  - Fund flows:       every 60 min
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from data.tv_fetcher import TVFetcher
from data.fred_fetcher import FREDFetcher
from data.calendar_fetcher import get_today_events
from data.flow_fetcher import get_fund_flows
from data.cache import set_cache
import config

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()
_tv: TVFetcher = None
_fred: FREDFetcher = None


def _get_tv() -> TVFetcher:
    global _tv
    if _tv is None:
        _tv = TVFetcher(username=config.TV_USERNAME, password=config.TV_PASSWORD)
    return _tv


def _get_fred() -> FREDFetcher:
    global _fred
    if _fred is None:
        _fred = FREDFetcher()
    return _fred


async def refresh_indices():
    try:
        data = _get_tv().fetch_all_indices()
        await set_cache("indices", data)
        logger.info("Refreshed indices")
    except Exception as e:
        logger.error(f"refresh_indices failed: {e}")


async def refresh_fx():
    try:
        data = _get_tv().fetch_all_fx()
        await set_cache("fx", data)
        logger.info("Refreshed FX")
    except Exception as e:
        logger.error(f"refresh_fx failed: {e}")


async def refresh_commodities():
    try:
        data = _get_tv().fetch_all_commodities()
        await set_cache("commodities", data)
        logger.info("Refreshed commodities")
    except Exception as e:
        logger.error(f"refresh_commodities failed: {e}")


async def refresh_vix():
    try:
        data = _get_tv().fetch_vix()
        await set_cache("vix", {"value": data})
        logger.info("Refreshed VIX")
    except Exception as e:
        logger.error(f"refresh_vix failed: {e}")


async def refresh_crypto():
    try:
        data = _get_tv().fetch_crypto()
        await set_cache("crypto", data)
        logger.info("Refreshed crypto")
    except Exception as e:
        logger.error(f"refresh_crypto failed: {e}")


async def refresh_yields():
    try:
        data = _get_fred().get_us_yields()
        await set_cache("yields", data)
        logger.info("Refreshed yields")
    except Exception as e:
        logger.error(f"refresh_yields failed: {e}")


async def refresh_intraday():
    try:
        data = _get_tv().fetch_all_intraday()
        for sym, bars in data.items():
            await set_cache(f"intraday_{sym}", bars)
        logger.info("Refreshed intraday")
    except Exception as e:
        logger.error(f"refresh_intraday failed: {e}")


async def refresh_calendar():
    try:
        data = get_today_events()
        await set_cache("calendar", data)
        logger.info("Refreshed calendar")
    except Exception as e:
        logger.error(f"refresh_calendar failed: {e}")


async def refresh_flows():
    try:
        data = get_fund_flows()
        await set_cache("flows", data)
        logger.info("Refreshed fund flows")
    except Exception as e:
        logger.error(f"refresh_flows failed: {e}")


async def run_initial_refresh():
    """Run all refreshes once at startup."""
    logger.info("Running initial data refresh...")
    await refresh_indices()
    await refresh_fx()
    await refresh_commodities()
    await refresh_vix()
    await refresh_crypto()
    await refresh_yields()
    await refresh_intraday()
    await refresh_calendar()
    await refresh_flows()
    logger.info("Initial refresh complete.")


def start_scheduler():
    scheduler.add_job(refresh_indices,    "interval", minutes=1,  id="indices")
    scheduler.add_job(refresh_fx,         "interval", minutes=1,  id="fx")
    scheduler.add_job(refresh_vix,        "interval", minutes=1,  id="vix")
    scheduler.add_job(refresh_crypto,     "interval", minutes=1,  id="crypto")
    scheduler.add_job(refresh_commodities,"interval", minutes=5,  id="commodities")
    scheduler.add_job(refresh_intraday,   "interval", minutes=5,  id="intraday")
    scheduler.add_job(refresh_calendar,   "interval", minutes=15, id="calendar")
    scheduler.add_job(refresh_yields,     "interval", minutes=30, id="yields")
    scheduler.add_job(refresh_flows,      "interval", minutes=60, id="flows")
    scheduler.start()
    logger.info("Scheduler started.")
