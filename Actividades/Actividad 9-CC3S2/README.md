## Actividad 9 - pytest + coverage + fixtures + factories + mocking + TDD

-   Nombre: Diego Edson Bayes Santos
-   Fecha: 29/09/2025
-   Tiempo total:
-   Entorno usado: WSL en laptop personal Windows, en el IDE Visual Studio Code

### Aserciones Pruebas

### Pruebas Pytest

Las pruebas de `pytest` en esta actividad cubren casos para distintos tipos de inputs (como `int` o `float`), casos frontera (como lados que miden 0 o negativo) y que activen los errores esperados.

El reporte del coverage muestra que se cubrió el 100% del código.

### Pruebas Fixtures

### Coverage Pruebas

### Factories Fakes

### Mocking Objetos

### Practica TDD

Se comenzó refactorizando el código existente para mejorar el funcionamiento. El principal cambio fue la implementación del decorador `require_counter`, el cual corrobora la existencia de un contador como precondición para los métodos que lo requieran.

Se implementaron 4 nuevas pruebas:

-   Incrementar un contador en 1

-   Establecer valor específico

-   Listar todos los contadores

-   Reiniciar un contador
