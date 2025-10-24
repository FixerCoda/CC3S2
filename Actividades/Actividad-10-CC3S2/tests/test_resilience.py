import logging

import pytest

from Actividades.pruebas_fixtures.conftest import SecretRedactor
from src.servicios.fake_http import FakeHttpClient

LOGGER = logging.getLogger("imdb")


def test_timeout_logged_redacted(imdb_fixtures, caplog):
    caplog.set_level(logging.INFO)
    LOGGER.addFilter(SecretRedactor())
    client = FakeHttpClient(imdb_fixtures, delay_ms=0, fail_mode="timeout")
    with pytest.raises(TimeoutError):
        client.get_json(
            "https://imdb-api.com/API/Ratings/KEY/tt0111161",
            headers={"Authorization": "Bearer AAA.BBB"},
        )
    msgs = " ".join(m for _, _, m in caplog.record_tuples)
    assert "Bearer <REDACTED>" in msgs


def test_http_500_branch(imdb_fixtures):
    client = FakeHttpClient(imdb_fixtures, fail_mode="500")
    with pytest.raises(RuntimeError):
        client.get_json("https://imdb-api.com/API/Ratings/KEY/tt0111161")


def test_malformed_payload_branch(imdb_fixtures):
    client = FakeHttpClient(imdb_fixtures)
    data = client.get_json("https://imdb-api.com/API/Ratings/KEY/malformed")
    assert "oops" in data  # downstream should reject later
