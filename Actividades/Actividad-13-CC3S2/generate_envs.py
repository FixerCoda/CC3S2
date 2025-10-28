import os
import json

# Parámetros de ejemplo para N entornos
def generate_envs():
    """Genera configuración de entornos con dependencias."""
    envs = []
    for i in range(1, 4):
        env = {"name": f"app{i}"}

        if i == 3:
            env["network"] = "net2-peered"
        else:
            env["network"] = f"net{i}"

        envs.append(env)
    return envs

ENVS = generate_envs()
MODULE_DIR = "modules/simulated_app"
OUT_DIR    = "environments"

def generate_network_tf_json(env):
    return {
        "variable": [
            {
                "name": [{
                    "type": "string",
                    "default": env["name"],
                    "description": "Nombre del servidor"
                }]
            },
            {
                "network": [{
                    "type": "string",
                    "default": env["network"],
                    "description": "Red del servidor"
                }]
            },
            {
                "port": [{
                    "type": "string",
                    "default": "8080",
                    "description": "Puerto del servidor"
                }]
            },
            {
                "api_key": [{
                    "type": "string",
                    "sensitive": True,
                    "description": "API Key sensible (leer desde ENV: TF_VAR_api_key)"
                }]
            }
        ]
    }

def render_and_write(env):
    env_dir = os.path.join(OUT_DIR, env["name"])
    os.makedirs(env_dir, exist_ok=True)

    # 1) Genera network.tf.json dinámicamente (con api_key sensitive)
    network_config = generate_network_tf_json(env)
    with open(os.path.join(env_dir, "network.tf.json"), "w") as fp:
        json.dump(network_config, fp, indent=4)

    # 2) Genera main.tf.json con referencias a variables (incluyendo api_key)
    config = {
        "resource": [
            {
                "null_resource": [
                    {
                        env["name"]: [
                            {
                                "triggers": {
                                    "name":    "${var.name}",
                                    "network": "${var.network}"
                                },
                                "provisioner": [
                                    {
                                        "local-exec": {
                                            "command": (
                                                "echo 'Arrancando servidor ${var.name} "
                                                "en red ${var.network} puerto ${var.port} "
                                                "con API_KEY=${var.api_key}'"
                                            )
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with open(os.path.join(env_dir, "main.tf.json"), "w") as fp:
        json.dump(config, fp, indent=4)

    print(f"✓ Generado: {env_dir}/ (network={env['network']})")

if __name__ == "__main__":
    # Limpia entornos viejos (si quieres)
    if os.path.isdir(OUT_DIR):
        import shutil
        shutil.rmtree(OUT_DIR)

    print("=== Generando entornos ===\n")

    for env in ENVS:
        render_and_write(env)

    print(f"\n✅ Generados {len(ENVS)} entornos en '{OUT_DIR}/'")
    print("\n📝 Nota: api_key es SENSITIVE y NO se escribe en disco.")
    print("   Para usarla, exporta: export TF_VAR_api_key='your-secret-key'")
    print("\n📋 Configuración generada:")
    for env in ENVS:
        print(f"   - {env['name']}: network={env['network']}")
