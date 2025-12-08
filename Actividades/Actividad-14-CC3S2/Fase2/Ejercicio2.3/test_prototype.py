"""Tests para mutaciones avanzadas con Prototype"""

import json
import os
from iac_patterns.builder import InfrastructureBuilder
from iac_patterns.singleton import ConfigSingleton


def test_mutator_adds_local_file():
    """Verifica que el mutator agrega correctamente el local_file"""
    config = ConfigSingleton(env_name="app_0")
    config.set("proyecto", "patrones_iac_locales")

    builder = InfrastructureBuilder(env_name=config.env_name)

    builder.build_null_with_mutator()

    builder.export(path=os.path.join(".", "main.tf.json"))

    with open("main.tf.json", "r") as main_file:
        main_file = json.load(main_file)
        resources = main_file["resource"][0]
        assert "local_file" in resources, "Debe existir el recurso local_file"
        assert "welcome_txt" in resources["local_file"], "Debe existir welcome_txt"


if __name__ == "__main__":
    test_mutator_adds_local_file()
