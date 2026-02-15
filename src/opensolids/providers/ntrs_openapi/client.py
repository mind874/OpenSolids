from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Any

import requests


class NTRSRateLimiter:
    def __init__(self, max_requests: int = 500, window_minutes: int = 15):
        self.max_requests = max_requests
        self.window = timedelta(minutes=window_minutes)
        self._timestamps: deque[datetime] = deque()

    def acquire(self) -> None:
        now = datetime.now(timezone.utc)
        while self._timestamps and now - self._timestamps[0] > self.window:
            self._timestamps.popleft()
        if len(self._timestamps) >= self.max_requests:
            raise RuntimeError(
                f"NTRS rate limit exceeded ({self.max_requests} requests / {self.window})."
            )
        self._timestamps.append(now)


class NTRSOpenAPIClient:
    def __init__(self, base_url: str = "https://ntrs.nasa.gov/api", session: requests.Session | None = None):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.rate_limiter = NTRSRateLimiter()

    def _request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        self.rate_limiter.acquire()
        res = self.session.request(method, f"{self.base_url}{path}", timeout=30, **kwargs)
        res.raise_for_status()
        data = res.json()
        if isinstance(data, dict):
            return data
        return {"results": data}

    def search_citations(self, query: str, *, size: int = 25, offset: int = 0) -> dict[str, Any]:
        if size > 10000:
            raise ValueError("NTRS query size must not exceed 10000 records")
        payload = {"q": query, "size": size, "from": offset}
        return self._request("POST", "/citations/search", json=payload)

    def get_citation(self, citation_id: str) -> dict[str, Any]:
        return self._request("GET", f"/citations/{citation_id}")

    def get_redistributions(self, since_date: str) -> dict[str, Any]:
        params = {"redistributedDate.gt": since_date}
        return self._request("GET", "/citations/redistributions", params=params)

    @staticmethod
    def extract_license_fields(citation: dict[str, Any]) -> dict[str, Any]:
        copyright_obj = citation.get("copyright") or {}
        return {
            "determinationType": copyright_obj.get("determinationType"),
            "containsThirdPartyMaterial": citation.get("containsThirdPartyMaterial"),
            "copyrightOwner": copyright_obj.get("owner"),
            "distribution": citation.get("distribution") or citation.get("disseminated"),
        }
