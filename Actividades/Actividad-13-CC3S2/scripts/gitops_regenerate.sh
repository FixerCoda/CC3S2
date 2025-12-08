#!/bin/bash

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Directorios
MODULE_DIR="modules/simulated_app"
ENVIRONMENTS_DIR="environments"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Archivo para rastrear el último hash de cambios
HASH_FILE="$PROJECT_ROOT/.gitops_last_hash"

# Función para calcular hash de los módulos
calculate_module_hash() {
    find "$PROJECT_ROOT/$MODULE_DIR" -type f \( -name "*.tf.json" -o -name "*.json" \) \
        -exec cat {} \; | sha256sum | cut -d' ' -f1
}

# Función para regenerar entornos
regenerate_environments() {
    echo -e "${BLUE}Regenerando entornos...${NC}\n"

    cd "$PROJECT_ROOT"

    # Leer configuración de entornos desde un archivo o usar valores por defecto
    if [ -f ".gitops_config" ]; then
        source .gitops_config
    else
        ENV_COUNT=${ENV_COUNT:-3}
        ENV_PREFIX=${ENV_PREFIX:-"app"}
        ENV_PORT=${ENV_PORT:-8080}
    fi

    echo -e "${YELLOW}Configuración:${NC}"
    echo "- Entornos: $ENV_COUNT"
    echo "- Prefijo: $ENV_PREFIX"
    echo "- Puerto: $ENV_PORT"
    echo ""

    # Ejecutar generate_envs.py con validación
    python3 generate_envs.py \
        --count "$ENV_COUNT" \
        --prefix "$ENV_PREFIX" \
        --port "$ENV_PORT" \
        --validate

    if [ $? -eq 0 ]; then
        echo -e "\n${GREEN}Regeneración completada exitosamente${NC}"
        return 0
    else
        echo -e "\n${RED}Error en la regeneración${NC}"
        return 1
    fi
}

main() {
    echo -e "${BLUE}   GitOps Local - Regeneración Automática${NC}"

    # Verificar que estamos en el directorio correcto
    if [ ! -d "$PROJECT_ROOT/$MODULE_DIR" ]; then
        echo -e "${RED}Error: Directorio $MODULE_DIR no encontrado${NC}"
        echo "Ejecuta este script desde la raíz del proyecto"
        exit 1
    fi

    # Calcular hash actual del módulo
    CURRENT_HASH=$(calculate_module_hash)

    # Leer hash anterior si existe
    if [ -f "$HASH_FILE" ]; then
        PREVIOUS_HASH=$(cat "$HASH_FILE")
    else
        PREVIOUS_HASH=""
    fi

    # Verificar si hay cambios
    if [ "$CURRENT_HASH" != "$PREVIOUS_HASH" ]; then
        echo -e "${YELLOW}Cambios detectados en $MODULE_DIR/${NC}"
        echo "Hash anterior: ${PREVIOUS_HASH:-"<ninguno>"}"
        echo "Hash actual:   $CURRENT_HASH"
        echo ""

        # Regenerar entornos
        if regenerate_environments; then
            # Guardar el nuevo hash
            echo "$CURRENT_HASH" > "$HASH_FILE"
            echo -e "\n${GREEN}Hash actualizado${NC}"
            echo -e "\n${GREEN}GitOps: Sincronización completada${NC}"
        else
            echo -e "\n${RED}GitOps: Falló la sincronización${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}No hay cambios en $MODULE_DIR/${NC}"
        echo "  Hash: $CURRENT_HASH"
        echo -e "\n${BLUE}Los entornos están sincronizados${NC}"
    fi
}

# Modo forzado (regenerar sin importar si hay cambios)
if [ "$1" == "--force" ] || [ "$1" == "-f" ]; then
    echo -e "${YELLOW}Modo FORZADO: Regenerando sin verificar cambios${NC}\n"
    regenerate_environments
    CURRENT_HASH=$(calculate_module_hash)
    echo "$CURRENT_HASH" > "$HASH_FILE"
    exit $?
fi

# Ejecutar main
main
