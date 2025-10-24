import logging
import os
import urllib.parse as up

import requests

from src.servicios.http_abstraction import HttpClient

LOGGER = logging.getLogger("imdb")
ALLOWLIST = {"imdb-api.com", "api.themoviedb.org"}


def _https_and_allowed(url: str) -> None:
    u = up.urlparse(url)
    if u.scheme.lower() != "https":
        raise ValueError("Politica OCP : HTTPS requerido")
    host = u.hostname or ""
    if host not in ALLOWLIST:
        raise ValueError(f"Host no permitido: {host}")


class RealHttpClient(HttpClient):
    def __init__(self, timeout: float | None = None):
        self.timeout = timeout or float(os.getenv("HTTP_TIMEOUT", "3.0"))

    def get_json(self, url, headers=None, timeout=None):
        _https_and_allowed(url)
        t = timeout or self.timeout
        resp = requests.get(url, headers=headers or {}, timeout=t)
        if resp.status_code >= 500:
            raise RuntimeError(f"server error {resp.status_code}")
        resp.raise_for_status()
        return resp.json()
