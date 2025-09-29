import pytest
from src.carrito import Carrito

@pytest.mark.xfail(reason="Esperamos mensaje con pista accionable")
def test_mensaje_error_contiene_contexto():
    carrito = Carrito()
    with pytest.raises(ValueError) as e:
        carrito.actualizar_cantidad("inexistente", 1)
    assert "inexistente" in str(e.value)
