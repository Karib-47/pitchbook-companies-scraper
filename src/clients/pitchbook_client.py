from __future__ import annotations

import logging
from typing import Optional
from urllib.parse import urljoin

from src.utils.http import HttpClient

LOGGER = logging.getLogger(__name__)

class PitchBookClient:
    """
    A small wrapper around HttpClient for PitchBook company profile pages.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    def _normalize_url(self, url_or_id: str) -> str:
        if url_or_id.startswith("http://") or url_or_id.startswith("https://"):
            return url_or_id
        # Treat as an ID fragment and build a canonical URL.
        path = f"/profiles/company/{url_or_id}"
        return urljoin(self.http_client.base_url, path)

    def fetch_company_profile(self, url_or_id: str, *, timeout: Optional[int] = None) -> str:
        url = self._normalize_url(url_or_id)
        LOGGER.debug("Fetching PitchBook profile from %s", url)
        response = self.http_client.get(url, timeout=timeout)
        LOGGER.info("Fetched %s with status %s", response.url, response.status_code)
        return response.text