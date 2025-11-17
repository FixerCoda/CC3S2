# Ejercicio 1: Estrategia de "pruebas unitarias" y "pruebas de contrato" combinadas

## 1. Diseño de módulos declarativos

- Módulo Network

  - `variables.tf`
  
    ```tf
    variable "network_name" {
        description = "Nombre de la red"
        type = string
        validation {
            condition = length(var.network_name) > 0
            error_message = "El nombre de la red no puede estar vacío"
        }
    }

    variable "cidr" {
        description = "CIDR de la red principal"
        type = string
    }

    variable "subnet_count" {
        description = "Número de subredes a crear"
        type = number
        default = 3
    }
    ```

  - `outputs.tf`

    ```tf
    output "network_id" {
        description = "ID de la red creada"
        value = local.network_id
    }

    output "network_cidr" {
        description = "CIDR de la red"
        value = var.cidr
    }

    output "subnet_ids" {
        description = "Lista de IDs de subredes creadas"
        value = local.subnet_ids
    }

    output "subnet_cidrs" {
        description = "Lista de bloques CIDR de las subredes"
        value = local.subnet_cidrs
    }
    ```

- Módulo Compute

  - `variables.tf`
  
    ```tf
    variable "instance_name" {
        description = "Nombre de la instancia"
        type = string
    }

    variable "network_id" {
        description = "ID de la red donde se desplegará la instancia"
        type = string
    }

    variable "subnet_id" {
        description = "ID de la subred donde se desplegará la instancia"
        type = string
    }

    variable "storage_id" {
        description = "ID del almacenamiento adjunto"
        type = string
        default = null
    }
    ```

  - `outputs.tf`

    ```tf
    output "instance_id" {
        description = "ID de la instancia creada"
        value = local.instance_id
    }

    output "instance_state" {
        description = "Estado de la instancia"
        value = local.state
    }
    ```

- Módulo Storage

- `variables.tf`
  
    ```tf
    variable "storage_name" {
    description = "Nombre del recurso de almacenamiento"
    type = string
    }

    variable "storage_type" {
        description = "Tipo de almacenamiento"
        type = string
        default = "block"
        validation {
            condition = contains(["block", "object", "file"], var.storage_type)
            error_message = "El tipo debe ser: block, object o file"
        }
    }

    variable "size_gb" {
        description = "Tamaño del almacenamiento en GB"
        type = number
        default = 10
    }
    ```

  - `outputs.tf`

    ```tf
    output "storage_id" {
        description = "ID del recurso de almacenamiento"
        value = local.storage_id
    }

    output "storage_endpoint" {
        description = "Endpoint de acceso al almacenamiento"
        value = local.endpoint
    }

    output "storage_size_gb" {
        description = "Tamaño configurado en GB"
        value = var.size_gb
    }
    ```
