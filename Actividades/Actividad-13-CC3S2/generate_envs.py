import os
import json
import click

# Parámetros de ejemplo para N entornos
def generate_envs(count, prefix):
    """Genera configuración de entornos con dependencias."""
    envs = []
    for i in range(1, count + 1):
        env = {"name": f"{prefix}{i}"}

        if i == count:
            env["network"] = "net2-peered"
        else:
            env["network"] = f"net{i}"

        envs.append(env)
    return envs

MODULE_DIR = "modules/simulated_app"
OUT_DIR    = "environments"

def generate_network_tf_json(env, port):
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
                    "default": str(port),
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

def render_and_write(env, port):
    env_dir = os.path.join(OUT_DIR, env["name"])
    os.makedirs(env_dir, exist_ok=True)

    # 1) Genera network.tf.json dinámicamente (con api_key sensitive)
    network_config = generate_network_tf_json(env, port)
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

@click.command()
@click.option('--count', default=3, help='Número de entornos a generar')
@click.option('--prefix', default='app', help='Prefijo para los nombres de los entornos')
@click.option('--port', default=8080, help='Puerto a usar en los entornos')
def main(count, prefix, port):
    """Genera entornos de Terraform con configuración personalizada."""

    envs = generate_envs(count, prefix)

    # Limpia entornos viejos (si quieres)
    if os.path.isdir(OUT_DIR):
        import shutil
        shutil.rmtree(OUT_DIR)

    click.echo("Generando entornos\n")

    for env in envs:
        render_and_write(env, port)

    click.echo(f"\nGenerados {len(envs)} entornos en '{OUT_DIR}/'")
    click.echo("\nConfiguración generada:")
    for env in envs:
        click.echo(f"   - {env['name']}: network={env['network']}, port={port}")

if __name__ == "__main__":
    main()
