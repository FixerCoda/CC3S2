from unittest.mock import Mock
import pytest
from src.shopping_cart import ShoppingCart

def test_pago_exitoso():
    # Arrange
    pago_mock = Mock()
    pago_mock.process_payment.return_value = True
    cart = ShoppingCart(payment_gateway=pago_mock)
    cart.add_item("x", 1, 10.0)
    total = cart.calculate_total()

    # Act
    resultado = cart.process_payment(total)

    # Assert
    assert resultado is True
    pago_mock.process_payment.assert_called_once_with(total)

def test_pago_timeout_sin_reintento_automatico():
    # Arrange
    pago_mock = Mock()
    pago_mock.process_payment.side_effect = TimeoutError("timeout")
    cart = ShoppingCart(payment_gateway=pago_mock)
    cart.add_item("x", 1, 10.0)
    total = cart.calculate_total()

    # Act / Assert
    with pytest.raises(TimeoutError):
        cart.process_payment(total)

    # El SUT no debe reintentar automáticamente
    assert pago_mock.process_payment.call_count == 1

    # Reintento manual desde el test para documentar el contrato
    pago_mock.process_payment.side_effect = None
    pago_mock.process_payment.return_value = True
    assert pago_mock.process_payment() is True  # Reintento manual exitoso

def test_pago_rechazo_definitivo():
    # Arrange
    pago_mock = Mock()
    pago_mock.process_payment.return_value = False
    cart = ShoppingCart(payment_gateway=pago_mock)
    cart.add_item("x", 1, 10.0)
    total = cart.calculate_total()

    # Act
    resultado = cart.process_payment(total)

    # Assert
    assert resultado is False
    pago_mock.process_payment.assert_called_once_with(total)
