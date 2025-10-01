## Actividad 9 - pytest + coverage + fixtures + factories + mocking + TDD

-   Nombre: Diego Edson Bayes Santos
-   Fecha: 29/09/2025
-   Tiempo total:
-   Entorno usado: WSL en laptop personal Windows, en el IDE Visual Studio Code

### Aserciones Pruebas

Se escribió 1 prueba para cada uno de los 4 métodos de `stack.py`:

-   `is_empty()`

-   `pop()`

-   `peek()`

-   `push(data)`

El reporte del coverage muestra que se cubrió el 100% del código.

### Pruebas Pytest

Las pruebas de `pytest` en esta actividad cubren casos para distintos tipos de inputs (como `int` o `float`), casos frontera (como lados que miden 0 o negativo) y que activen los errores esperados.

El reporte del coverage muestra que se cubrió el 100% del código.

### Pruebas Fixtures

Se implementaron 7 nuevas pruebas para alcanzar la cobertura completa:

-   Representación de la cuenta en `str`

-   Serialización de una cuenta en un diccionario

-   Establecimiento de atributos de una cuenta desde un diccionario

-   Actualización de una columna de una cuenta

-   Validación de error en la actualización de un id de cuenta inexistente

-   Búsqueda de una cuenta con su id

-   Eliminación de una cuenta

El reporte del coverage muestra que se cubrió el 100% del código.

### Coverage Pruebas

### Factories Fakes

Se mejoró el caso de `fixtures` con el uso de `factories` para reemplazar los datos fabricados manualmente de cuentas en un archivo `json`.

### Mocking Objetos

### Practica TDD

Se comenzó refactorizando el código existente para mejorar el funcionamiento. El principal cambio fue la implementación del decorador `require_counter`, el cual corrobora la existencia de un contador como precondición para los métodos que lo requieran.

Se implementaron 4 nuevas pruebas:

-   Incrementar un contador en 1

-   Establecer valor específico

-   Listar todos los contadores

-   Reiniciar un contador
