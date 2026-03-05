"""
Economic calendar data.
Uses a static JSON file for MVP. Replace with Trading Economics API when available.

Expected schema per event:
{
    "time": "08:30",
    "event": "US Initial Jobless Claims",
    "actual": "215K",
    "forecast": "220K",
    "previous": "218K",
    "impact": "high",
    "country": "US"
}
"""

import json
import os
import logging
from datetime import date

logger = logging.getLogger(__name__)

CALENDAR_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "calendar.json")


def get_today_events() -> list:
    """Load today's economic calendar events from static JSON file."""
    today = date.today().isoformat()
    try:
        if os.path.exists(CALENDAR_FILE):
            with open(CALENDAR_FILE) as f:
                data = json.load(f)
            return data.get(today, data.get("default", _sample_events()))
    except Exception as e:
        logger.error(f"Calendar load error: {e}")
    return _sample_events()


def _sample_events() -> list:
    return [
        {
            "time": "08:30",
            "event": "US Initial Jobless Claims",
            "actual": "-",
            "forecast": "220K",
            "previous": "218K",
            "impact": "medium",
            "country": "US",
        },
        {
            "time": "14:00",
            "event": "BOT Policy Rate Decision",
            "actual": "-",
            "forecast": "2.50%",
            "previous": "2.50%",
            "impact": "high",
            "country": "TH",
        },
        {
            "time": "09:00",
            "event": "India CPI Inflation",
            "actual": "-",
            "forecast": "4.8%",
            "previous": "4.9%",
            "impact": "high",
            "country": "IN",
        },
    ]
