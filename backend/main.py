"""
Market Intelligence Terminal — FastAPI Backend
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from data.cache import init_db, get_cache, get_cache_with_timestamp
from scheduler import start_scheduler, run_initial_refresh
import config

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    # Run initial refresh in background — don't block startup if data fetch fails
    asyncio.create_task(_safe_initial_refresh())
    start_scheduler()
    yield
    logger.info("Shutting down...")


async def _safe_initial_refresh():
    try:
        await run_initial_refresh()
    except Exception as e:
        logger.error(f"Initial refresh failed (non-fatal): {e}")


app = FastAPI(
    title="Market Intelligence Terminal API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/market-data")
async def get_market_data():
    """Full dashboard payload — served from cache."""
    intraday = {}
    for sym in config.INTRADAY_SYMBOLS:
        bars = await get_cache(f"intraday_{sym}")
        intraday[sym] = bars or []

    vix_data = await get_cache("vix")

    return {
        "indices":     await get_cache("indices")     or [],
        "fx":          await get_cache("fx")          or [],
        "commodities": await get_cache("commodities") or [],
        "vix":         vix_data.get("value") if vix_data else None,
        "yields":      await get_cache("yields")      or [],
        "crypto":      await get_cache("crypto")      or [],
        "calendar":    await get_cache("calendar")    or [],
        "flows":       await get_cache("flows")       or {},
        "intraday":    intraday,
    }


@app.get("/api/intraday/{symbol}")
async def get_intraday(symbol: str):
    bars = await get_cache(f"intraday_{symbol.upper()}")
    if bars is None:
        raise HTTPException(status_code=404, detail=f"No intraday data for {symbol}")
    return {"symbol": symbol.upper(), "bars": bars}


@app.get("/api/yield-curve")
async def get_yield_curve():
    data = await get_cache("yields")
    return {"yields": data or []}


@app.get("/api/eco-calendar")
async def get_eco_calendar():
    data = await get_cache("calendar")
    return {"events": data or []}


@app.get("/api/fund-flows")
async def get_fund_flows():
    data = await get_cache("flows")
    return data or {}


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
