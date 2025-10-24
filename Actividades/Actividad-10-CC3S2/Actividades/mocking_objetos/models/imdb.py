from typing import Any

from src.servicios.http_abstraction import HttpClient


class ImdbService:
    BASE = "https://imdb-api.com/API"

    def __init__(self, client: HttpClient, apikey: str):
        self.client = client
        self.apikey = apikey

    def search_titles(self, title: str) -> Any:
        url = f"{self.BASE}/SearchTitle/{self.apikey}/{title}"
        return self.client.get_json(url)

    def movie_ratings(self, imdb_id: str) -> Any:
        url = f"{self.BASE}/Ratings/{self.apikey}/{imdb_id}"
        return self.client.get_json(url)
