from src.shopping_cart import ShoppingCart

def test_mre_precision():
    # Arrange
    carrito = ShoppingCart()
    carrito.add_item("x", 1, 0.1)
    carrito.add_item("x", 1, 0.2)

    # Act
    total = carrito.calculate_total()

    # Assert
    assert round(total, 2) == 0.30
