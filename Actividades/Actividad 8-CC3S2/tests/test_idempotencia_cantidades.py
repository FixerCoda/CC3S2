from src.carrito import Carrito
from src.factories import ProductoFactory

def test_actualizacion_idempotente():
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="x", precio=3.25)
    carrito.agregar_producto(producto, 2)
    total_1 = carrito.calcular_total()

    # Act
    for _ in range(5):
        carrito.actualizar_cantidad(producto, 2)
    total_2 = carrito.calcular_total()

    # Assert
    assert total_1 == total_2
    assert sum(i.cantidad for i in carrito.items) == 2
