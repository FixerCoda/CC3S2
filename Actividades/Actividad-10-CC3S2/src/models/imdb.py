"""
Acceso a la base de datos de películas de Internet Movie Database
Implementa las APIs SearchTitle, Reviews y Ratings
"""

import logging
import os
import urllib.parse
from typing import Any, Dict

import requests

logger = logging.getLogger(__name__)

ALLOWED_HOSTS = {"imdb-api.com"}
TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "2.0"))


def _enforce_policies(url: str):
    host = urllib.parse.urlparse(url).hostname
    if host not in ALLOWED_HOSTS:
        raise ValueError(f"Host no permitido: {host}")
    if not url.startswith("https://"):
        raise ValueError("Se requiere HTTPS")


class IMDb:
    """Acceso a la base de datos de películas de Internet Movie Database"""

    def __init__(self, apikey: str, http_client=None):
        self.apikey = apikey
        self.http = http_client or requests

    def get_url(self, url: str) -> Dict[str, Any]:
        _enforce_policies(url)
        response = self.http.get(url, timeout=TIMEOUT)

        if response.status_code == 200:
            return response.json()
        return {}

    def search_titles(self, title: str) -> Dict[str, Any]:
        """Busca una película por título"""
        logger.info("Buscando en IMDb el título: %s", title)
        url = f"https://imdb-api.com/API/SearchTitle/{self.apikey}/{title}"  # noqa: E231

        return self.get_url(url)

    def movie_reviews(self, imdb_id: str) -> Dict[str, Any]:
        """Obtiene reseñas para una película"""
        logger.info("Buscando en IMDb las reseñas: %s", imdb_id)
        url = f"https://imdb-api.com/API/Reviews/{self.apikey}/{imdb_id}"  # noqa: E231

        return self.get_url(url)

    def movie_ratings(self, imdb_id: str) -> Dict[str, Any]:
        """Obtiene calificaciones para una película"""
        logger.info("Buscando en IMDb las calificaciones: %s", imdb_id)
        url = f"https://imdb-api.com/API/Ratings/{self.apikey}/{imdb_id}"  # noqa: E231

        return self.get_url(url)
