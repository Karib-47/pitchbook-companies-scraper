from __future__ import annotations

from typing import Any

from src.clients.pitchbook_client import PitchBookClient
from src.utils.http import HttpClient
from src.utils.rate_limiter import RateLimiter

class _FakeResponse:
    def __init__(self, url: str, text: str, status_code: int = 200) -> None:
        self.url = url
        self.text = text
        self.status_code = status_code

class _FakeSession:
    def __init__(self) -> None:
        self.headers: dict[str, Any] = {}

    def get(self, url: str, timeout: int, **_: Any) -> _FakeResponse:
        # Just echo a tiny HTML snippet back for tests
        html = f"<html><body><h1 data-test='company-name'>Fake Co</h1><p>URL: {url}</p></body></html>"
        return _FakeResponse(url=url, text=html, status_code=200)

def test_pitchbook_client_fetch_uses_http_client_and_normalizes_id():
    fake_session = _FakeSession()
    http_client = HttpClient(
        base_url="https://pitchbook.com",
        user_agent="test-agent",
        timeout=5,
        rate_limiter=RateLimiter(max_per_minute=100),
        session=fake_session,
    )
    client = PitchBookClient(http_client=http_client)

    html = client.fetch_company_profile("361831-87")
    assert "Fake Co" in html
    assert "profiles/company/361831-87" in html

    html2 = client.fetch_company_profile("https://pitchbook.com/profiles/company/123")
    assert "profiles/company/123" in html2