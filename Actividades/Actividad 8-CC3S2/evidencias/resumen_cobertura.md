## Resumen de Cobertura - Análisis y Plan de Mejora

### Estado Actual

-   Cobertura Total: 92.31% (supera el mínimo requerido del 90%)
-   Módulos Críticos:
    -   src/carrito.py: 91% (5 líneas sin cubrir)
    -   src/shopping_cart.py: 93% (2 líneas sin cubrir)

### Módulos no cubiertos

-   Representación de la clase Producto
-   Representación de la clase ItemCarrito
-   Evaluación de error al remover una cantidad de un producto mayor a la existente
-   Evaluación de error al remover un producto inexistente
-   Evaluación de error al actualizar un producto en una cantidad negativa
-   Evaluación de error al incluir un descuento fuera del rango (0 - 100)
-   Evaluación de error en la clase ShoppingCart sin pasarela de pago

### Plan para incrementar la cobertura

-   Incluir pruebas específicas para la representación en `string` de las clases
-   Añadir una prueba por cada evaluación de error faltante
