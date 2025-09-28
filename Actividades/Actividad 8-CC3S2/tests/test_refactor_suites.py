from unittest.mock import Mock
from src.shopping_cart import ShoppingCart

class TestPrecisionMonetaria: # pylint: disable=too-few-public-methods,attribute-defined-outside-init
    def setup_method(self):
        self.cart = ShoppingCart()

    def test_suma_pequenas_cantidades(self):
        # Arrange
        self.cart.add_item("x", 1, 0.05)
        self.cart.add_item("x", 1, 0.05)

        # Act
        total = self.cart.calculate_total()

        # Assert
        assert round(total, 2) == 0.1

class TestPasarelaPagoContratos: # pylint: disable=attribute-defined-outside-init
    def setup_method(self):
        self.pago_mock = Mock()
        self.cart = ShoppingCart(payment_gateway=self.pago_mock)

    def configurar_carrito(self, items):
        for name, quantity, price in items:
            self.cart.add_item(name, quantity, price)
        return self.cart.calculate_total()

    def test_pago_exitoso(self):
        # Arrange
        self.pago_mock.process_payment.return_value = True
        total = self.configurar_carrito([("x", 1, 10.0)])

        # Act
        resultado = self.cart.process_payment(total)

        # Assert
        assert resultado is True
        self.pago_mock.process_payment.assert_called_once_with(total)

    def test_pago_fallido(self):
        # Arrange
        self.pago_mock.process_payment.return_value = False
        total = self.configurar_carrito([("x", 1, 20.0)])

        # Act
        resultado = self.cart.process_payment(total)

        # Assert
        assert resultado is False
        self.pago_mock.process_payment.assert_called_once_with(total)
