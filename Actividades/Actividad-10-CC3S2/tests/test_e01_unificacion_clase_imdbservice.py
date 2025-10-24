"""
Casos de prueba para el mocking
"""

import json
import os
import sys

# Agregar el directorio raíz al sys.path ANTES de importar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import Mock, patch

import pytest
from requests import Response

from src.models.imdb import TIMEOUT, ImdbService, _enforce_policies


class TestIMDbDatabase:
    """Casos de prueba para la base de datos de IMDb"""

    @pytest.fixture(autouse=True)
    def setup_class(self, imdb_data):
        """Configuración inicial para cargar los datos de IMDb"""
        self.imdb_data = imdb_data

    #  Casos de prueba

    @patch("src.models.imdb.requests.get")
    def test_search_titles_success(self, mock_get):
        """Prueba que la búsqueda de títulos retorna datos correctamente"""
        # Configurar el mock para devolver una respuesta exitosa
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = self.imdb_data["search_title"]
        mock_get.return_value = mock_response

        imdb = ImdbService(apikey="fake_api_key")
        resultado = imdb.search_titles("Bambi")

        assert resultado == self.imdb_data["search_title"]
        mock_get.assert_called_once_with(
            "https://imdb-api.com/API/SearchTitle/fake_api_key/Bambi",
            timeout=TIMEOUT,
        )

    @patch("src.models.imdb.requests.get")
    def test_search_titles_failure(self, mock_get):
        """Prueba que la búsqueda de títulos maneja errores correctamente"""
        # Configurar el mock para devolver una respuesta fallida con json retornando {}
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        imdb = ImdbService(apikey="fake_api_key")
        resultado = imdb.search_titles("TituloInexistente")

        assert resultado == {}
        mock_get.assert_called_once_with(
            "https://imdb-api.com/API/SearchTitle/fake_api_key/TituloInexistente",
            timeout=TIMEOUT,
        )

    @patch("src.models.imdb.requests.get")
    def test_movie_reviews_success(self, mock_get):
        """Prueba que la obtención de reseñas retorna datos correctamente"""
        # Configurar el mock para devolver una respuesta exitosa
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = self.imdb_data["movie_reviews"]
        mock_get.return_value = mock_response

        imdb = ImdbService(apikey="fake_api_key")
        resultado = imdb.movie_reviews("tt1375666")

        assert resultado == self.imdb_data["movie_reviews"]
        mock_get.assert_called_once_with(
            "https://imdb-api.com/API/Reviews/fake_api_key/tt1375666",
            timeout=TIMEOUT,
        )

    @patch("src.models.imdb.requests.get")
    def test_movie_reviews_failure(self, mock_get):
        """Prueba que la obtención de reseñas maneja casos fallidos"""
        # Configurar el mock para devolver una respuesta fallida
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        imdb = ImdbService(apikey="fake_api_key")
        resultado = imdb.movie_reviews("tt1375666")

        assert resultado == {}
        mock_get.assert_called_once_with(
            "https://imdb-api.com/API/Reviews/fake_api_key/tt1375666",
            timeout=TIMEOUT,
        )

    @patch("src.models.imdb.requests.get")
    def test_movie_ratings_success(self, mock_get):
        """Prueba que la obtención de calificaciones maneja casos fallidos"""
        # Configurar el mock para devolver una respuesta fallida
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        imdb = ImdbService(apikey="fake_api_key")
        resultado = imdb.movie_ratings("tt1375666")

        assert resultado == {}
        mock_get.assert_called_once_with(
            "https://imdb-api.com/API/Ratings/fake_api_key/tt1375666",
            timeout=TIMEOUT,
        )

    @patch("src.models.imdb.requests.get")
    def test_movie_ratings_failure(self, mock_get):
        """Prueba que la obtención de calificaciones retorna datos correctamente"""
        # Configurar el mock para devolver una respuesta exitosa
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = self.imdb_data["movie_ratings"]
        mock_get.return_value = mock_response

        imdb = ImdbService(apikey="fake_api_key")
        resultado = imdb.movie_ratings("tt1375666")

        assert resultado == self.imdb_data["movie_ratings"]
        mock_get.assert_called_once_with(
            "https://imdb-api.com/API/Ratings/fake_api_key/tt1375666",
            timeout=TIMEOUT,
        )

    @patch("src.models.imdb.requests.get")
    def test_search_by_title_failed(self, mock_get):
        """Prueba de búsqueda por título fallida"""
        # Configurar el mock para devolver una respuesta con API Key inválida
        mock_response = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=self.imdb_data["INVALID_API"]),
        )
        mock_get.return_value = mock_response

        imdb = ImdbService(apikey="bad-key")
        resultados = imdb.search_titles("Bambi")

        assert resultados is not None
        assert resultados["errorMessage"] == "Invalid API Key"

    @patch("src.models.imdb.requests.get")
    def test_movie_ratings_good(self, mock_get):
        """Prueba de calificaciones de películas con buenas calificaciones"""
        # Configurar el mock para devolver una respuesta exitosa con buenas calificaciones
        mock_response = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=self.imdb_data["movie_ratings"]),
        )
        mock_get.return_value = mock_response

        imdb = ImdbService(apikey="fake_api_key")
        resultados = imdb.movie_ratings("tt1375666")

        assert resultados is not None
        assert resultados["title"] == "Bambi"
        assert resultados["filmAffinity"] == 3
        assert resultados["rottenTomatoes"] == 5

    def test_politica_rechaza_host_no_permitido(self):
        with pytest.raises(ValueError):
            _enforce_policies("https://malicioso.evil/xx")

    @patch("src.models.imdb.requests.get")
    def test_search_titles_con_cliente_inyectado(self, imdb_data):
        http = Mock()
        mock_resp = Mock(status_code=200)
        mock_resp.json.return_value = imdb_data["search_title"]
        http.get.return_value = mock_resp

        imdb = ImdbService(apikey="fake_api_key", http_client=http)
        out = imdb.search_titles("Bambi")

        http.get.assert_called_once_with(
            "https://imdb-api.com/API/SearchTitle/fake_api_key/Bambi",
            timeout=TIMEOUT,
        )
        assert out == imdb_data["search_title"]
