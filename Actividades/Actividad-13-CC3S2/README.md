# Actividad 13 - Escribiendo infraestructura como código en un entorno local con Terraform

- Nombre: Diego Edson Bayes Santos
- Fecha: 08/12/2025
- Tiempo total: 6h
- Entorno usado: WSL en laptop personal Windows, en el IDE Visual Studio Code

## Fase 0: Preparación

```bash
terraform init
```

![Terraform Init](./capturas/terraform-init.png)

```bash
terraform plan
```

![Terraform Plan](./capturas/terraform-plan.png)

```bash
terraform apply
```

![Terraform Apply](./capturas/terraform-apply.png)

## Fase 1: Expresando el cambio de infraestructura

```bash
terraform plan
```

![Terraform Plan Fase 1](./capturas/terraform-plan-fase-1.png)

- ¿Cómo interpreta Terraform el cambio de variable?

Terraform lee los valores de las variables en los archivos .tfvars, en las variables de entorno, o en los valores por defecto de su definición, tal como este caso. Luego, los sustituye con los valores resueltos para generar la configuración final.

- ¿Qué diferencia hay entre modificar el JSON vs. parchear directamente el recurso?

Al modificar el JSON, se mantiene un registro de este cambio, lo que convierte al proceso en reproducible y versionable, lo cual no se logra al ejecutar un comando específico para cambiar dicho estado.

- ¿Por qué Terraform no recrea todo el recurso, sino que aplica el cambio "in-place"?

Terraform puede aplicar cambios *in-place* para evitar destruir y crear el recurso en casos específicos y siempre que sea posible. Esto permite actualizaciones eficientes y más rápidas.

- ¿Qué pasa si editas directamente main.tf.json en lugar de la plantilla de variables?

Si se edita main.tf.json directamente, se perdería la separación de configuración y valores, lo que afecta la reutilización de estos y favocere el acoplamiento del código.

## Fase 2: Entendiendo la inmutabilidad

```bash
python legacy_to_terraform.py
cd converted
terraform init
terraform plan
terraform apply
```

![Legacy to Transform](./capturas/legacy-to-transform.png)

## Fase 3: Escribiendo código limpio en IaC

- Al ejecutar `jq`, se formatea el archivo json según los ajustes estándar. En este caso, se cambió el tamaño de las indentaciones a 2.

- Se añadió la variable `port` a la configuración.

![Terraform Network Port](./capturas/terraform-port.png)

- Se lee la variable de entorno `api_key` y se muestra como información sensible.

![Terraform Api Key](./capturas/terraform-api-key.png)

## Fase 4: Integración final y discusión

- ¿Cómo extenderías este patrón para 50 módulos y 100 entornos?

Para escalar este patrón a 50 módulos y 100 entornos, se consideraría una estructura de directorios jerárquica y versionamiento de módulos para mejor trazabilidad, así como mantener un archivo de configuración específico para los entornos. Además, se puede implementar un `Makefile` para orquestar la generación y aplicación.

- ¿Qué prácticas de revisión de código aplicarías a los `.tf.json`?

Algunas de las prácticas de revisión de código incluyen el `linting` y formateo con `jq` y `terraform fmt-check`, la validación semántica con `terraform validate`, escaneos de seguridad on `tfsec` o `checkov`, y el uso de `hooks` para automatizar las verificaciones `pre-commit`.

- ¿Cómo gestionarías secretos en producción (sin Vault)?

Se puede implementar una herramienta integrada con el control de versiones, como Github Actions Secrets, o con el proveedor en nube de ser el caso, como AWS Secrets Manager.

- ¿Qué workflows de revisión aplicarías a los JSON generados?

Se pueden incluir `pre-commit hooks` que ejecuten las revisiones previamente descritas en el segundo inciso, de manera automática, antes de cada `commit`. Además, se implementa estas validaciones automáticas y análisis de seguridad dentro del pipeline CI/Cd, de tal forma que no se acepte ningún cambio que no pase los `gates` definidos o qu genere `drift`. Por último, se adjunta el `output` del `terraform plan` en cada PR para mantener un registro adicional.

## Ejercicio 1: Drift avanzado

Se creó una arquitectura modular con dos servidores y un load balancer:

**Estructura del módulo:**

- [modules/simulated_app/main.tf.json](modules/simulated_app/main.tf.json): Define `server1` y `server2`
- [modules/simulated_app/load_balancer.tf.json](modules/simulated_app/load_balancer.tf.json): Define el `load_balancer` que depende de ambos servidores

**Entorno de prueba:**

Se creó el directorio [drift-demo/](drift-demo/) que consume el módulo `simulated_app`:

```json
{
    "module": {
        "simulated_app": {
            "source": "../modules/simulated_app",
            "name": "drift-demo",
            "network": "demo-net",
            "port": "8080"
        }
    }
}
```

**Simulación de drift:**

Se modificó manualmente el archivo [drift-demo/terraform.tfstate](drift-demo/terraform.tfstate) cambiando el puerto de `server1` de `8080` a `9090` para simular un cambio manual en la infraestructura.

**Detección de drift con terraform plan:**

```bash
terraform plan
```

**Resultado:**

```text
module.simulated_app.null_resource.server1: Refreshing state... [id=8724138018635079543]
module.simulated_app.null_resource.server2: Refreshing state... [id=5805898956846702577]
module.simulated_app.null_resource.load_balancer: Refreshing state... [id=803614368377729302]

Terraform will perform the following actions:

  # module.simulated_app.null_resource.load_balancer must be replaced
-/+ resource "null_resource" "load_balancer" {
      ~ id       = "803614368377729302" -> (known after apply)
      ~ triggers = { # forces replacement
          ~ "backend_servers" = "8724138018635079543,5805898956846702577" -> (known after apply)
            # (1 unchanged element hidden)
        }
    }

  # module.simulated_app.null_resource.server1 must be replaced
-/+ resource "null_resource" "server1" {
      ~ id       = "8724138018635079543" -> (known after apply)
      ~ triggers = { # forces replacement
          ~ "port"    = "9090" -> "8080"
            # (2 unchanged elements hidden)
        }
    }

Plan: 2 to add, 0 to change, 2 to destroy.
```

## Ejercicio 2: CLI Interactiva

Se refactorizó el script [generate_envs.py](generate_envs.py) para usar la librería `click` y aceptar argumentos de línea de comandos.

**Argumentos disponibles:**

- `--count`: Número de entornos a generar (default: 3)
- `--prefix`: Prefijo para los nombres de los entornos (default: 'app')
- `--port`: Puerto a usar en los entornos (default: 8080)

**Uso:**

```bash
python generate_envs.py --count 3 --prefix staging --port 3000
```

**Salida:**

```text
Generando entornos

✓ Generado: environments/staging1/ (network=net1)
✓ Generado: environments/staging2/ (network=net2)
✓ Generado: environments/staging3/ (network=net2-peered)

Generados 3 entornos en 'environments/'

Configuración generada:
   - staging1: network=net1, port=3000
   - staging2: network=net2, port=3000
   - staging3: network=net2-peered, port=3000
```

**Ayuda:**

```bash
python generate_envs.py --help
```

**Características:**

- ✅ Interfaz CLI amigable con `click`
- ✅ Argumentos configurables con valores por defecto
- ✅ Generación dinámica de entornos con parámetros personalizados
- ✅ Validación automática de argumentos
- ✅ Mensaje de ayuda integrado

## Ejercicio 3: Validación de Esquema JSON

Se implementó un sistema completo de validación de esquemas JSON usando la librería `jsonschema`.

### Estructura de Schemas

Se crearon dos JSON Schemas en el directorio [schemas/](schemas/):

1. **[network_schema.json](schemas/network_schema.json)**: Valida archivos `network.tf.json`
   - Verifica estructura de variables
   - Valida tipos de datos (string, number, bool, list, map)
   - Comprueba campos requeridos (type, description)
   - Permite campos opcionales (default, sensitive)

2. **[main_schema.json](schemas/main_schema.json)**: Valida archivos `main.tf.json`
   - Verifica estructura de recursos
   - Valida configuración de null_resource
   - Comprueba triggers requeridos (name, network)
   - Valida provisioners y comandos

### Integración en generate_envs.py

La validación está integrada en el método `validate_json` de [generate_envs.py](generate_envs.py):

**Uso con validación:**

```bash
python generate_envs.py --count 2 --prefix test --port 5000 --validate
```

## Ejercicio 4: GitOps Local

Se implementó un sistema GitOps local que detecta cambios en los módulos y regenera automáticamente los entornos.

### Script de Regeneración Automática

Se creó [scripts/gitops_regenerate.sh](scripts/gitops_regenerate.sh), un script bash que:

- **Detecta cambios**: Calcula un hash SHA256 de todos los archivos en `modules/simulated_app/`
- **Compara estados**: Compara el hash actual con el anterior guardado en `.gitops_last_hash`
- **Regenera automáticamente**: Si detecta cambios, regenera todos los entornos
- **Actualiza hash**: Guarda el nuevo hash para futuras comparaciones

**Uso básico:**

```bash
# Detectar cambios y regenerar si es necesario
source ./scripts/gitops_regenerate.sh

# Forzar regeneración sin verificar cambios
source ./scripts/gitops_regenerate.sh --force
```

### Hooks de Pre-commit

Se creó [.pre-commit-config.yaml](.pre-commit-config.yaml) con múltiples hooks de validación:

**Hooks incluidos:**

1. **check-json**: Valida sintaxis JSON básica
2. **pretty-format-json**: Formatea JSON con indentación consistente (4 espacios)
3. **jq-check**: Ejecuta `jq --check` en archivos `.tf.json`
4. **terraform-validate-json**: Valida contra schemas personalizados
5. **terraform-fmt-check**: Verifica formato Terraform
6. **shellcheck**: Analiza scripts bash
7. **trailing-whitespace**: Elimina espacios al final de líneas
8. **end-of-file-fixer**: Asegura línea final en archivos

**Ejecutar manualmente:**

```bash
# Ejecutar todos los hooks en todos los archivos
pre-commit run --all-files

# Ejecutar un hook específico
pre-commit run jq-check --all-files
```

## Ejercicio 5: Compartición Segura de Secretos

### Ubicación del Archivo de Secretos

**Archivo**: `~/.config/secure.json`

Este archivo almacena secretos localmente y nunca debe ser versionado en Git. Debe estar ubicado en el directorio home del usuario.

**Estructura del archivo:**

```json
{
  "terraform": {
    "api_key": "prod-secret-key-abc123xyz789",
    "aws_access_key": "AKIAIOSFODNN7EXAMPLE",
    "aws_secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
  },
  "metadata": {
    "created": "2025-01-15",
    "owner": "diego.bayes@example.com",
    "expires": "2025-12-31"
  }
}
```

### Workflow de Distribución Segura

Se emplea una herramienta de gestión de secretos como `1Password`, `LastPass` o `Bitwarden`

```text
1. Administrador crea entrada en bóveda compartida del equipo
   - Nombre: "Terraform API Key - Proyecto CC3S2"
   - Contenido: JSON completo para secure.json
   - Expira: 2025-12-31

2. Desarrollador accede a la bóveda compartida
   - Copia contenido seguro desde la herramienta
   - Pega en ~/.config/secure.json local

3. Rotación automática
   - 1Password genera nuevo secreto cada 90 días
   - Notifica al equipo vía integración Slack
```

**Ventajas:**

- Cifrado end-to-end
- Auditoría de accesos
- Rotación automática
- Revocación inmediata
- Integración con CI/CD
