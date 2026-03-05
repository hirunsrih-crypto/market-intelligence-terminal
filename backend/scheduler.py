"""
APScheduler jobs for periodic cache refresh.
All blocking tvdatafeed/FRED calls run in a thread pool via asyncio.to_thread()
so the event loop (and healthcheck) are never blocked.
"""

import asyncio
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
        data = await asyncio.to_thread(_get_tv().fetch_all_indices)
        await set_cache("indices", data)
        logger.info("Refreshed indices")
    except Exception as e:
        logger.error(f"refresh_indices failed: {e}")


async def refresh_fx():
    try:
        data = await asyncio.to_thread(_get_tv().fetch_all_fx)
        await set_cache("fx", data)
        logger.info("Refreshed FX")
    except Exception as e:
        logger.error(f"refresh_fx failed: {e}")


async def refresh_commodities():
    try:
        data = await asyncio.to_thread(_get_tv().fetch_all_commodities)
        await set_cache("commodities", data)
        logger.info("Refreshed commodities")
    except Exception as e:
        logger.error(f"refresh_commodities failed: {e}")


async def refresh_vix():
    try:
        data = await asyncio.to_thread(_get_tv().fetch_vix)
        await set_cache("vix", {"value": data})
        logger.info("Refreshed VIX")
    except Exception as e:
        logger.error(f"refresh_vix failed: {e}")


async def refresh_crypto():
    try:
        data = await asyncio.to_thread(_get_tv().fetch_crypto)
        await set_cache("crypto", data)
        logger.info("Refreshed crypto")
    except Exception as e:
        logger.error(f"refresh_crypto failed: {e}")


async def refresh_yields():
    try:
        data = await asyncio.to_thread(_get_fred().get_us_yields)
        await set_cache("yields", data)
        logger.info("Refreshed yields")
    except Exception as e:
        logger.error(f"refresh_yields failed: {e}")


async def refresh_intraday():
    try:
        data = await asyncio.to_thread(_get_tv().fetch_all_intraday)
        for sym, bars in data.items():
            await set_cache(f"intraday_{sym}", bars)
        logger.info("Refreshed intraday")
    except Exception as e:
        logger.error(f"refresh_intraday failed: {e}")


async def refresh_calendar():
    try:
        data = await asyncio.to_thread(get_today_events)
        await set_cache("calendar", data)
        logger.info("Refreshed calendar")
    except Exception as e:
        logger.error(f"refresh_calendar failed: {e}")


async def refresh_flows():
    try:
        data = await asyncio.to_thread(get_fund_flows)
        await set_cache("flows", data)
        logger.info("Refreshed fund flows")
    except Exception as e:
        logger.error(f"refresh_flows failed: {e}")


async def run_initial_refresh():
    """Run all refreshes concurrently at startup — non-blocking."""
    logger.info("Running initial data refresh...")
    await asyncio.gather(
        refresh_calendar(),
        refresh_flows(),
        refresh_yields(),
        return_exceptions=True,
    )
    # TV data in background — don't wait for slow WebSocket calls
    asyncio.create_task(refresh_indices())
    asyncio.create_task(refresh_fx())
    asyncio.create_task(refresh_commodities())
    asyncio.create_task(refresh_vix())
    asyncio.create_task(refresh_crypto())
    asyncio.create_task(refresh_intraday())
    logger.info("Initial refresh scheduled.")


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
