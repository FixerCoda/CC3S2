"""Test de validación para Ejercicio 2.1"""

from iac_patterns.singleton import ConfigSingleton

def test_reset():
    c1 = ConfigSingleton("dev")
    created = c1.created_at

    c1.settings["x"] = 1
    c1.settings["y"] = 2
    c1.settings["database"] = "postgresql"

    print("Antes del reset:")
    print(f"Settings: {c1.settings}")
    print(f"created_at: {c1.created_at}")

    c1.reset()

    print("Después del reset:")
    print(f"Settings: {c1.settings}")
    print(f"created_at: {c1.created_at}")

    assert c1.settings == {}, f"Settings debería estar vacío"
    assert c1.created_at == created, f"created_at cambió de {created} a {c1.created_at}"

if __name__ == "__main__":
    test_reset()
