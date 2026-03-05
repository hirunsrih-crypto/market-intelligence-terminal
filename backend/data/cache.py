"""
SQLite cache layer.
Data is refreshed by the scheduler and served from cache on every API request.
"""

import aiosqlite
import json
from datetime import datetime

DB_PATH = "market_cache.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS market_snapshot (
                key        TEXT PRIMARY KEY,
                data       TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        await db.commit()


async def set_cache(key: str, data):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO market_snapshot VALUES (?, ?, ?)",
            (key, json.dumps(data), datetime.utcnow().isoformat())
        )
        await db.commit()


async def get_cache(key: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT data, updated_at FROM market_snapshot WHERE key = ?", (key,)
        )
        row = await cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None


async def get_cache_with_timestamp(key: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT data, updated_at FROM market_snapshot WHERE key = ?", (key,)
        )
        row = await cursor.fetchone()
        if row:
            return json.loads(row[0]), row[1]
        return None, None
