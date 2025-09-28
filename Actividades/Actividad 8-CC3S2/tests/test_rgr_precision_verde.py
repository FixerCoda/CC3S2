import pytest
from src.shopping_cart import ShoppingCart

@pytest.mark.skip(reason="Contrato: Precisión binaria no se corrige en esta versión")
def test_total_precision_decimal_skip():
    # Arrange
    cart = ShoppingCart()
    cart.add_item("x", 1, 0.2)
    cart.add_item("x", 1, 0.1)

    # Act
    total = cart.calculate_total()

    # Assert
    assert total == 0.30
