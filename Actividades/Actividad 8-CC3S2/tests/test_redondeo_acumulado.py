from src.carrito import Carrito
from src.factories import ProductoFactory

def test_redondeo_acumulado_vs_final():
    # Arrange
    carrito_1 = Carrito()
    carrito_2 = Carrito()
    producto_a = ProductoFactory(nombre="a", precio=0.3333)
    producto_b = ProductoFactory(nombre="b", precio=0.6666)
    producto_c = ProductoFactory(nombre="c", precio=1.7777)
    carrito_1.agregar_producto(producto_a, 3)
    carrito_2.agregar_producto(producto_b, 3)
    carrito_2.agregar_producto(producto_c, 9)

    # Act
    total_1 = carrito_1.calcular_total()
    suma_por_item_1 = sum(i.producto.precio * i.cantidad for i in carrito_1.items)
    total_2 = carrito_2.calcular_total()
    suma_por_item_2 = sum(i.producto.precio * i.cantidad for i in carrito_2.items)

    # Assert
    assert round(total_1, 2) == round(suma_por_item_1, 2)
    assert round(total_2, 2) == round(suma_por_item_2, 2)
