from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

from src.utils.rate_limiter import RateLimiter

LOGGER = logging.getLogger(__name__)

@dataclass
class HttpClient:
    base_url: str
    user_agent: str
    timeout: int = 15
    rate_limiter: Optional[RateLimiter] = None
    max_retries: int = 3
    backoff_factor: float = 0.5
    session: Optional[requests.Session] = None

    def __post_init__(self) -> None:
        if self.session is None:
            self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    def get(self, url: str, *, timeout: Optional[int] = None, **kwargs: Any) -> requests.Response:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = self.base_url.rstrip("/") + "/" + url.lstrip("/")

        effective_timeout = timeout or self.timeout
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt < self.max_retries:
            attempt += 1
            if self.rate_limiter is not None:
                self.rate_limiter.acquire()

            try:
                LOGGER.debug("HTTP GET %s (attempt %d)", url, attempt)
                response = self.session.get(url, timeout=effective_timeout, **kwargs)
                if 200 <= response.status_code < 300:
                    return response
                LOGGER.warning(
                    "Non-success status %s for %s (attempt %d)",
                    response.status_code,
                    url,
                    attempt,
                )
                last_error = RuntimeError(f"Unexpected status code {response.status_code}")
            except (requests.RequestException, OSError) as exc:  # noqa: PERF203
                last_error = exc
                LOGGER.warning("Request error for %s (attempt %d): %s", url, attempt, exc)

            sleep_time = self.backoff_factor * (2 ** (attempt - 1))
            time.sleep(sleep_time)

        assert last_error is not None
        LOGGER.error("HTTP GET %s ultimately failed after %d attempts", url, self.max_retries)
        raise last_error