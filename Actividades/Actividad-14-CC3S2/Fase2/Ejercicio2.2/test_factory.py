import json
from iac_patterns.factory import TimestampedNullResourceFactory

def test_format_yyyymmdd():
    """Prueba con formato YYYYMMDD"""
    resource = TimestampedNullResourceFactory.create(
        name="app_server",
        fmt='%Y%m%d'
    )

    print("\nRecurso con formato '%Y%m%d'")
    print(json.dumps(resource, indent=2))

    triggers = resource["resource"][0]["null_resource"][0]["app_server"][0]["triggers"]
    formatted_ts = triggers["formatted_timestamp"]

    assert len(formatted_ts) == 8, f"Formato esperado: YYYYMMDD (8 dígitos), obtenido: {formatted_ts}"
    assert formatted_ts.isdigit(), f"Debería contener solo dígitos, obtenido: {formatted_ts}"


def test_format_iso():
    """Prueba con formato ISO (YYYY-MM-DD)"""
    resource = TimestampedNullResourceFactory.create(
        name="database",
        fmt='%Y-%m-%d'
    )

    print("\nRecurso con formato '%Y-%m-%d'")
    print(json.dumps(resource, indent=2))

    triggers = resource["resource"][0]["null_resource"][0]["database"][0]["triggers"]
    formatted_ts = triggers["formatted_timestamp"]

    parts = formatted_ts.split('-')
    assert len(parts) == 3, f"Formato esperado: YYYY-MM-DD, obtenido: {formatted_ts}"
    assert len(parts[0]) == 4, "Año debe tener 4 dígitos"
    assert len(parts[1]) == 2, "Mes debe tener 2 dígitos"
    assert len(parts[2]) == 2, "Día debe tener 2 dígitos"


def generate_terraform_file():
    """Genera un archivo .tf.json para prueba con Terraform"""
    resource = TimestampedNullResourceFactory.create(
        name="deployment",
        fmt='%Y%m%d',
        triggers={
            "app_name": "my_app",
            "region": "us-east-1"
        }
    )

    with open("main.tf.json", "w") as f:
        json.dump(resource, f, indent=2)


if __name__ == "__main__":
    test_format_yyyymmdd()
    test_format_iso()
    generate_terraform_file()
