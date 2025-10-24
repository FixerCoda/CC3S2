"""
Casos de prueba para validar que assert_called_once_with falla correctamente
cuando falta el kwarg timeout=TIMEOUT
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import Mock

import pytest

from src.models.imdb import TIMEOUT, ImdbService


class TestAssertTimeoutKwarg:
    """Casos de prueba que validan la presencia del kwarg timeout en las llamadas HTTP"""

    @pytest.fixture(autouse=True)
    def setup_class(self, imdb_data):
        """Configuración inicial para cargar los datos de IMDb"""
        self.imdb_data = imdb_data

    def test_assert_called_once_with_timeout_success(self):
        """
        Prueba que verifica que assert_called_once_with pasa cuando
        se proporciona el timeout correcto en la llamada HTTP
        """
        http_client = Mock()
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = self.imdb_data["search_title"]
        http_client.get.return_value = mock_response

        imdb = ImdbService(apikey="test_key", http_client=http_client)
        result = imdb.search_titles("Bambi")

        assert result == self.imdb_data["search_title"]
        http_client.get.assert_called_once_with(
            "https://imdb-api.com/API/SearchTitle/test_key/Bambi",
            timeout=TIMEOUT,
        )

    def test_assert_called_once_with_timeout_without_kwarg_fails(self):
        """
        Prueba que demuestra que assert_called_once_with falla cuando
        no se incluye el kwarg timeout en la llamada al mock
        """
        http_client = Mock()
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = self.imdb_data["search_title"]
        http_client.get.return_value = mock_response

        http_client.get("https://imdb-api.com/API/SearchTitle/test_key/Bambi")

        with pytest.raises(AssertionError):
            http_client.get.assert_called_once_with(
                "https://imdb-api.com/API/SearchTitle/test_key/Bambi",
                timeout=TIMEOUT,
            )

    def test_assert_called_once_with_different_timeout_fails(self):
        """
        Prueba que demuestra que assert_called_once_with falla cuando
        se proporciona un timeout diferente al esperado
        """
        http_client = Mock()
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = self.imdb_data["search_title"]
        http_client.get.return_value = mock_response

        http_client.get(
            "https://imdb-api.com/API/SearchTitle/test_key/Bambi", timeout=TIMEOUT + 1
        )

        with pytest.raises(AssertionError):
            http_client.get.assert_called_once_with(
                "https://imdb-api.com/API/SearchTitle/test_key/Bambi",
                timeout=TIMEOUT,
            )
