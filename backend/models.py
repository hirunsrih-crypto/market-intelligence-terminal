"""Pydantic response schemas for the Market Intelligence API."""

from pydantic import BaseModel
from typing import Optional, List


class PriceItem(BaseModel):
    ticker: str
    name: str
    region: str
    currency: str
    value: Optional[float]
    change: Optional[float]


class FXItem(BaseModel):
    pair: str
    ticker: str
    rate: Optional[float]
    change: Optional[float]


class CommodityItem(BaseModel):
    name: str
    ticker: str
    value: Optional[float]
    unit: str
    change: Optional[float]


class YieldItem(BaseModel):
    name: str
    maturity: int
    yield_: Optional[float]
    change: Optional[float]

    class Config:
        populate_by_name = True
        fields = {"yield_": "yield"}


class CryptoItem(BaseModel):
    name: str
    ticker: str
    value: Optional[float]
    change: Optional[float]


class CalendarEvent(BaseModel):
    time: str
    event: str
    actual: str
    forecast: str
    previous: str
    impact: str
    country: str


class IntradayBar(BaseModel):
    time: str
    open: float
    high: float
    low: float
    price: float
    volume: int


class MarketDataResponse(BaseModel):
    indices: List[dict]
    fx: List[dict]
    commodities: List[dict]
    vix: Optional[float]
    yields: List[dict]
    crypto: List[dict]
    calendar: List[dict]
    flows: dict
    intraday: dict
    last_updated: Optional[str]
