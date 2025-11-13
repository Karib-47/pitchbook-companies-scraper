from __future__ import annotations

import threading
import time
from dataclasses import dataclass

@dataclass
class RateLimiter:
    """
    A simple thread-safe rate limiter for approximate N requests per minute.
    """

    max_per_minute: int
    _lock: threading.Lock = threading.Lock()
    _last_acquire: float = 0.0

    @property
    def min_interval(self) -> float:
        if self.max_per_minute <= 0:
            return 0.0
        return 60.0 / float(self.max_per_minute)

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_acquire
            wait_for = self.min_interval - elapsed
            if wait_for > 0:
                time.sleep(wait_for)
            self._last_acquire = time.monotonic()