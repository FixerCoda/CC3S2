from src.carrito import Carrito
from src.factories import ProductoFactory

def test_invariante_agregar_remover_y_actualizar():
    # Arrange
    carrito = Carrito()
    producto = ProductoFactory(nombre="x", precio=5.0)
    carrito.agregar_producto(producto=producto, cantidad=3)
    total_inicial = carrito.calcular_total()

    # Act
    carrito.remover_producto(producto=producto, cantidad=3)
    total_despues_remover = carrito.calcular_total()
    items_despues_remover = carrito.contar_items()

    carrito.agregar_producto(producto=producto, cantidad=3)
    carrito.actualizar_cantidad(producto=producto, nueva_cantidad=0)
    total_despues_actualizar = carrito.calcular_total()
    items_despues_actualizar = carrito.contar_items()

    # Assert
    assert total_inicial == 15.0
    assert total_despues_remover == 0.0
    assert items_despues_remover == 0
    assert total_despues_actualizar == 0.0
    assert items_despues_actualizar == 0
