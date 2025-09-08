import pytest
from app.app import summarize

@pytest.fixture
def sample():
    return ["1", "2", "3"]

def test_ok(sample):
    """Caso normal: Una lista válida de números"""
    result = summarize(sample)

    assert result["count"] == 3
    assert result["sum"] == 6.0
    assert result["avg"] == 2.0

def test_empty():
    """Caso borde: Una lista vacía"""
    with pytest.raises(ValueError):
        summarize([])

def test_single():
    result = summarize([1])

    assert result["count"] == 1
    assert result["sum"] == 1.0
    assert result["avg"] == 1.0

def test_non_numeric():
    """Caso error: Una lista con un elemento con letra"""
    with pytest.raises(ValueError):
        summarize(["a", "2"])
        