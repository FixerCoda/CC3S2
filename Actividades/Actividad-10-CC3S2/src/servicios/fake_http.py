import logging
import time
from typing import Any, Dict

LOGGER = logging.getLogger("imdb")


class FakeHttpClient:
    """No network. Serves preloaded fixtures; can simulate errors/timeouts."""

    def __init__(
        self, fixtures: Dict[str, Any], delay_ms: int = 0, fail_mode: str | None = None
    ):
        self._fx = fixtures
        self._delay = delay_ms / 1000.0
        self._fail_mode = fail_mode

    def get_json(self, url: str, headers=None, timeout=2.0):
        if self._delay:
            time.sleep(min(self._delay, timeout + 0.05))
        if self._fail_mode == "timeout":
            # Simulate exceeding timeout
            time.sleep(timeout + 0.1)
            # Format headers for logging in a way that SecretRedactor can parse
            headers_str = ""
            if headers:
                headers_str = " ".join(f"{k}: {v}" for k, v in headers.items())
            LOGGER.warning(f"Request timeout for {url} with headers: {headers_str}")
            raise TimeoutError("request timed out")
        if self._fail_mode == "500":
            raise RuntimeError("HTTP 500 simulated")
        if "malformed" in url:
            return self._fx["malformed_payload"]
        if "Ratings" in url:
            return self._fx["ratings_ok"]
        return self._fx["search_titles_ok"]
