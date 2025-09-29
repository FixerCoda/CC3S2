### A1. Descuentos parametrizados

| Entrada (Precio, Cantidad, Descuento) | Total esperado |
| ------------------------------------- | -------------- |
| 10.00, 1, 0                           | 10.00          |
| 10.00, 1, 1                           | 9.90           |
| 10.01, 1, 33.33                       | 6.67           |
| 100.00, 1, 50                         | 50.00          |
| 1.00, 1, 99.99                        | 0.00           |
| 50.00, 1, 100                         | 0.00           |

### A4. Redondeos acumulados vs. final

| Suma por ítem                       | Redondeo final | Diferencia |
| ----------------------------------- | -------------- | ---------- |
| 0.3333 \* 3 = 0.9999                | 1.0            | 0.0001     |
| 0.6666 \* 3 + 1.7777 \* 9 = 17.9991 | 18.0           | 0.0009     |

### B1. Rojo (falla esperada)- precisión financiera

El test en este inciso falla de manera esperada. Al usar la anotación `xfail`, se evita romper el flujo de pruebas cuando se tiene una limitación o error ya conocido o cuya solución falte implementar. Además, permite especificar la razón para su rápida identificación posterior.

### B2. Verde (exclusión documentada)

El uso de `skip` permite mapear posibles errores o fallos que no vayan a ser atendidos por contrato (ya sea de manera general o para la versión actual). A diferencia del `xfail`, no es importante el análisis de si esta prueba pasa o falla, por lo que se ahorran recursos sin perder el monitoreo de estos casos.

### B3. Refactor de suites

Los casos que incluyan una misma situación específica y requieran recursos similares, tales como los referentes a la pasarela de pago, pueden ser definidos dentro de una clase con varias pruebas. De esta manera, se evita la duplicación de lógica y se aprovecha la reutilización de recursos con métodos que aporta `pytest`.

### C1. Contratos de pasarela de pago con mock

| Evento                  | Expectativa                   |
| ----------------------- | ----------------------------- |
| Pago exitoso            | True                          |
| Excepción sin reintento | TimeoutError, call_count == 1 |
| Pago fallido            | False                         |

### C2. Marcadores de humo y regresión

Los marcadores `smoke` sirven para pruebas iniciales y rápidas que verifican el funcionamiento básico del software. Son un punto importante de partida durante el CI porque permite aterrizar las pruebas más críticas y construir el resto a partir de estas. Asimismo, los marcadores `regression` sirven para verificar que un cambio reciente de código no impacte funcionalidad existente, lo que apoya a los cambios ágiles y robustos.

### C4. MREs para defectos

**Problema:** Error de precisión al agregar múltiples items del mismo producto

**Pasos para reproducir:**

-   Crear carrito y agregar producto `x` con precio 0.1
-   Agregar el mismo producto `x` con precio 0.2
-   Calcular total esperando 0.30 (0.1 + 0.2)
-   El total real es 0.20 (último precio sobrescribe el anterior)

**Expectativa vs Realidad:**

-   Esperado: add_item debería sumar cantidades y mantener precios
-   Actual: add_item sobrescribe completamente el precio unitario anterior
