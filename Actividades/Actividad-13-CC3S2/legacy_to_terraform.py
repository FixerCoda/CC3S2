import json
import os
import re
import subprocess


def parse_config_file(config_path):
    variables = {}

    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                variables[key] = value

    return variables


def parse_run_script(script_path, variables):
    with open(script_path, 'r') as f:
        content = f.read()

    content = re.sub(r'^#!/bin/bash\s*\n?', '', content)

    for var_name in variables.keys():
        content = re.sub(
            rf'\${var_name}\b|\${{\s*{var_name}\s*}}',
            f'${{var.{var_name.lower()}}}',
            content
        )

    return content.strip()


def generate_network_tf_json(variables, output_path):
    tf_variables = []

    for var_name, default_value in variables.items():
        tf_variables.append({
            var_name.lower(): [{
                "type": "string",
                "default": default_value,
                "description": f"Variable migrada desde legacy config: {var_name}"
            }]
        })

    config = {
        "variable": tf_variables
    }

    with open(output_path, 'w') as f:
        json.dump(config, f, indent=4)


def generate_main_tf_json(command, resource_name, output_path):
    config = {
        "resource": [{
            "null_resource": [{
                resource_name: [{
                    "triggers": {
                        "always_run": "${timestamp()}"
                    },
                    "provisioner": [{
                        "local-exec": {
                            "command": command
                        }
                    }]
                }]
            }]
        }]
    }

    with open(output_path, 'w') as f:
        json.dump(config, f, indent=4)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    legacy_dir = os.path.join(base_dir, "legacy")
    output_dir = os.path.join(base_dir, "converted")

    config_path = os.path.join(legacy_dir, "config.cfg")
    script_path = os.path.join(legacy_dir, "run.sh")

    os.makedirs(output_dir, exist_ok=True)

    # 1. Parsear config.cfg
    print(f"1. Leyendo {config_path}")
    variables = parse_config_file(config_path)
    print(f"   Variables encontradas: {variables}")

    # 2. Parsear run.sh
    print(f"\n2. Leyendo {script_path}")
    command = parse_run_script(script_path, variables)
    print(f"   Comando convertido: {command}")

    # 3. Generar network.tf.json
    print("\n3. Generando archivos Terraform")
    network_tf_path = os.path.join(output_dir, "network.tf.json")
    generate_network_tf_json(variables, network_tf_path)

    # 4. Generar main.tf.json
    main_tf_path = os.path.join(output_dir, "main.tf.json")
    generate_main_tf_json(command, "legacy_app", main_tf_path)

    return 0


if __name__ == "__main__":
    exit(main())
