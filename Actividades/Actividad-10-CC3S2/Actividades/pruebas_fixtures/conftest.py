import json
import logging
import os
import re

import pytest


class SecretRedactor(logging.Filter):
    """Redact tokens, apikeys, and Authorization headers in logs."""

    SECRET_PAT = re.compile(
        r"(Authorization:\s*Bearer\s+)[A-Za-z0-9\-\._~\+\/]+=*", re.I
    )
    KEY_PAT = re.compile(r"(api[_-]?key|token|secret)\s*=\s*[^&\s]+", re.I)

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        msg = self.SECRET_PAT.sub(r"\1<REDACTED>", msg)
        msg = self.KEY_PAT.sub(lambda m: m.group(1) + "=<REDACTED>", msg)
        record.msg = msg
        return True


@pytest.fixture(scope="session")
def imdb_data():
    """Carga las respuestas de IMDb necesarias para las pruebas"""
    current_dir = os.path.dirname(__file__)
    fixture_path = os.path.join(
        current_dir, "../Actividades/pruebas_fixtures/fixtures", "imdb_responses.json"
    )
    with open(fixture_path) as json_data:
        data = json.load(json_data)
        return data

@pytest.fixture(autouse=True)
def _redacted_logging(caplog):
    logger = logging.getLogger()
    logger.addFilter(SecretRedactor())
    caplog.set_level(logging.INFO)
    yield
    logger.filters.clear()


@pytest.fixture
def stub_valid_account():
    return {
        "id": "u_001",
        "email": "user@example.com",
        "role": "reader",
        "active": True,
    }


@pytest.fixture
def stub_corrupt_account():
    return {"id": None, "email": "bad@@", "role": 123, "active": "yes"}


@pytest.fixture
def imdb_fixtures():
    base = os.path.dirname(__file__)
    with open(
        os.path.join(base, "fixtures", "imdb_responses.json"), "r", encoding="utf-8"
    ) as f:
        return json.load(f)
