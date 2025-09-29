import pytest
from src.carrito import Carrito
from src.factories import ProductoFactory

@pytest.mark.smoke
def test_smoke_agregar_producto_y_calcular_total():
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="x", precio=1000.0)
    carrito.agregar_producto(producto=producto)

    # Act
    total = carrito.calcular_total()

    # Assert
    assert total == 1000.0

@pytest.mark.smoke
def test_smoke_aplicar_descuento_basico():
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="x", precio=500.0)
    carrito.agregar_producto(producto=producto, cantidad=2)

    # Act
    total_con_descuento = carrito.aplicar_descuento(10.0)

    # Assert
    assert round(total_con_descuento, 2) == round(900.0, 2)

@pytest.mark.smoke
def test_smoke_carrito_vacio():
    # Arrange
    carrito = Carrito()

    # Act
    monto_total = carrito.calcular_total()
    items_total = carrito.contar_items()

    # Assert
    assert monto_total == 0
    assert items_total == 0

@pytest.mark.regression
def test_regression_agregar_producto_existente():
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="x", precio=25.0)
    carrito.agregar_producto(producto, 1)
    carrito.agregar_producto(producto, 2)

    # Act
    monto_total = carrito.calcular_total()
    items_total = carrito.contar_items()

    # Assert
    assert round(monto_total, 2) == round(75.0, 2)
    assert items_total == 3

@pytest.mark.regression
def test_regression_remover_producto_parcial():
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="x", precio=75.0)
    carrito.agregar_producto(producto, 3)
    carrito.remover_producto(producto, 1)

    # Act
    monto_total = carrito.calcular_total()
    items_total = carrito.contar_items()

    # Assert
    assert round(monto_total, 2) == round(150.0, 2)
    assert items_total == 2

@pytest.mark.regression
def test_regression_remover_producto_completo():
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="x", precio=300.0)
    carrito.agregar_producto(producto, 1)
    carrito.remover_producto(producto, 1)

    # Act
    monto_total = carrito.calcular_total()
    items_total = carrito.contar_items()

    # Assert
    assert monto_total == 0
    assert items_total == 0
