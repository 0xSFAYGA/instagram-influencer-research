import time
from typing import Any, Dict, Iterable, List, Optional, Tuple

import httpx

from ..config import Settings
from ..types import RunStats
from .cache import HttpCache


class HikerAPIClient:
    """Thin wrapper around HikerAPI with caching and cost tracking."""

    def __init__(
        self,
        settings: Settings,
        stats: Optional[RunStats] = None,
        cache_ttl_seconds: Optional[int] = 86_400,
    ):
        self._settings = settings
        self._stats = stats
        self._cache = (
            HttpCache(settings.cache_db_path, ttl_seconds=cache_ttl_seconds)
            if cache_ttl_seconds is not None
            else None
        )
        self._client = httpx.Client(
            base_url=settings.base_url,
            headers={
                "Authorization": settings.access_key,
                "User-Agent": "hiker-research/0.1",
            },
            timeout=settings.timeout,
        )

    def _extract_request_units(self, response: httpx.Response) -> int:
        info = response.headers.get("x-hiker-info", "")
        if not info:
            return 0
        for part in info.split(";"):
            if part.strip().startswith("reqs="):
                value = part.split("=", 1)[1]
                try:
                    return int(value)
                except ValueError:
                    return 0
        return 0

    def _handle_backoff(self, attempt: int) -> None:
        sleep_seconds = min(2**attempt, 10)
        time.sleep(sleep_seconds)

    def _request(
        self, method: str, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict[str, Any], bool]:
        cache_key = None
        if self._cache:
            cache_key = self._cache.build_key(method, path, params)
            cached = self._cache.get(cache_key)
            if cached is not None:
                if self._stats:
                    self._stats.cache_hits += 1
                return cached, True

        last_response: Optional[httpx.Response] = None
        for attempt in range(3):
            resp = self._client.request(method, path, params=params)
            last_response = resp

            if resp.status_code == 429 and attempt < 2:
                self._handle_backoff(attempt)
                continue

            if resp.status_code == 402:
                resp.raise_for_status()

            resp.raise_for_status()

            units = self._extract_request_units(resp)
            if self._stats:
                if units:
                    self._stats.record_cost(path, units)
                self._stats.cache_misses += 1

            data = resp.json()
            if self._cache and cache_key:
                self._cache.set(cache_key, data)

            return data, False

        raise httpx.HTTPStatusError(
            "Too many 429 responses from HikerAPI.",
            request=last_response.request if last_response else None,
            response=last_response,
        )

    def fetch_profile(self, username: str) -> Dict[str, Any]:
        """
        Fetch profile data for a single handle.
        """

        data, _ = self._request("GET", f"/instagram/{username}")
        return data

    def fetch_recent_posts(
        self, username: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent posts for a handle.
        """

        data, _ = self._request("GET", f"/instagram/{username}/posts", params={"limit": limit})
        if isinstance(data, dict) and "results" in data:
            return list(data["results"])
        if isinstance(data, list):
            return data
        return []

    def fetch_profiles_bulk(self, usernames: Iterable[str]) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for username in usernames:
            results.append(self.fetch_profile(username))
        return results

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
