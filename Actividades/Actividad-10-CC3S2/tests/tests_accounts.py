import pytest

from src.servicios.validators import validate_account


def test_valid_account(stub_valid_account):
    assert validate_account(stub_valid_account) is True


@pytest.mark.parametrize("field", ["id", "email", "role", "active"])
def test_missing_fields(stub_valid_account, field):
    d = dict(stub_valid_account)
    d.pop(field)
    with pytest.raises(ValueError):
        validate_account(d)


def test_corrupt_types(stub_corrupt_account):
    with pytest.raises((ValueError, TypeError)):
        validate_account(stub_corrupt_account)
