import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, Optional


class HttpCache:
    """Simple SQLite-backed response cache."""

    def __init__(self, path: Path, ttl_seconds: Optional[int] = 86_400):
        self.path = path
        self.ttl_seconds = ttl_seconds
        self._init_db()

    def _init_db(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS responses (
                    cache_key TEXT PRIMARY KEY,
                    body TEXT NOT NULL,
                    created_at INTEGER NOT NULL
                )
                """
            )
            conn.commit()

    def build_key(self, method: str, url: str, params: Optional[Dict[str, Any]]) -> str:
        payload = json.dumps(
            {"method": method.upper(), "url": url, "params": params or {}},
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()

    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        if self.ttl_seconds == 0:
            return None

        now = int(time.time())
        with sqlite3.connect(self.path) as conn:
            row = conn.execute(
                "SELECT body, created_at FROM responses WHERE cache_key = ?", (cache_key,)
            ).fetchone()

        if not row:
            return None

        body, created_at = row
        if self.ttl_seconds and now - created_at > self.ttl_seconds:
            with sqlite3.connect(self.path) as conn:
                conn.execute("DELETE FROM responses WHERE cache_key = ?", (cache_key,))
                conn.commit()
            return None

        return json.loads(body)

    def set(self, cache_key: str, body: Dict[str, Any]) -> None:
        now = int(time.time())
        payload = json.dumps(body)
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO responses (cache_key, body, created_at)
                VALUES (?, ?, ?)
                """,
                (cache_key, payload, now),
            )
            conn.commit()

