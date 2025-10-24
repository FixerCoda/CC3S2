"""
Casos de prueba para validar inyección de dependencias con FakeClient sin red.
Enfoque: Contrato de URLs con y sin encoding de títulos.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import Mock

import pytest

from src.models.imdb import TIMEOUT, ImdbService


class TestDIWithFakeClientNoNetwork:
    """Casos de prueba para DI con cliente fake sin acceso a red"""

    @pytest.fixture(autouse=True)
    def setup_class(self, imdb_data):
        """Configuración inicial para cargar los datos de IMDb"""
        self.imdb_data = imdb_data

    def test_search_titles_with_spaces_no_encoding(self):
        """
        Prueba búsqueda con título que contiene espacios.
        DECISION: Congela comportamiento SIN encoding.
        La URL se pasa tal cual sin urllib.parse.quote().
        """
        http_client = Mock()
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = self.imdb_data["search_title_spaces"]
        http_client.get.return_value = mock_response

        imdb = ImdbService(apikey="test_key", http_client=http_client)
        result = imdb.search_titles("Star Wars Episode IV")

        assert result == self.imdb_data["search_title_spaces"]
        http_client.get.assert_called_once_with(
            "https://imdb-api.com/API/SearchTitle/test_key/Star Wars Episode IV",
            timeout=TIMEOUT,
        )

    def test_search_titles_with_symbols_no_encoding(self):
        """
        Prueba búsqueda con título que contiene símbolos especiales.
        DECISION: Congela comportamiento SIN encoding.
        Caracteres como ':' se pasan literales en la URL.
        """
        http_client = Mock()
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = self.imdb_data["search_title_colon"]
        http_client.get.return_value = mock_response

        imdb = ImdbService(apikey="test_key", http_client=http_client)
        result = imdb.search_titles("Star Wars: Episode IV")

        assert result == self.imdb_data["search_title_colon"]
        http_client.get.assert_called_once_with(
            "https://imdb-api.com/API/SearchTitle/test_key/Star Wars: Episode IV",
            timeout=TIMEOUT,
        )

    def test_search_titles_with_ampersand_no_encoding(self):
        """
        Prueba búsqueda con título que contiene '&'.
        DECISION: Congela comportamiento SIN encoding.
        """
        http_client = Mock()
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = self.imdb_data["search_title_ampersand"]
        http_client.get.return_value = mock_response

        imdb = ImdbService(apikey="test_key", http_client=http_client)
        result = imdb.search_titles("Star Wars & Episode IV")

        assert result == self.imdb_data["search_title_ampersand"]
        http_client.get.assert_called_once_with(
            "https://imdb-api.com/API/SearchTitle/test_key/Star Wars & Episode IV",
            timeout=TIMEOUT,
        )
