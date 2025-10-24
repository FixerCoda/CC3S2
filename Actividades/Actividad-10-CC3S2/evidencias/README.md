# Reporte de Pruebas - Parte 2

Este directorio contiene la evidencia de las pruebas ejecutadas para la Actividad 10-CC3S2, incluyendo reportes de cobertura y logs.

## Pruebas Ejecutadas

### 1. test_imdb.py

Archivo con casos de prueba para la clase `IMDb` y validación de políticas de seguridad.

#### Pruebas de Búsqueda de Títulos

- **test_search_titles_success**: Verifica que la búsqueda de títulos retorna datos correctamente cuando la API responde con éxito (status 200).
- **test_search_titles_failure**: Valida que se maneja correctamente una búsqueda fallida (status 404), retornando un diccionario vacío.
- **test_search_titles_con_cliente_inyectado**: Prueba la inyección de un cliente HTTP mock para verificar que se realizan las llamadas correctas con el timeout configurado.

#### Pruebas de Reseñas de Películas

- **test_movie_reviews_success**: Comprueba que la obtención de reseñas retorna datos cuando la respuesta es exitosa (status 200).
- **test_movie_reviews_failure**: Valida el manejo de errores cuando no se encuentran reseñas (status 404).

#### Pruebas de Calificaciones de Películas

- **test_movie_ratings_success**: Verifica que las calificaciones se obtienen correctamente cuando la API responde exitosamente.
- **test_movie_ratings_failure**: Comprueba el manejo de errores en la obtención de calificaciones.
- **test_movie_ratings_good**: Valida específicamente las calificaciones "buenas" retornadas por IMDb (filmAffinity y rottenTomatoes).

#### Pruebas de Validación de Políticas

- **test_politica_rechaza_host_no_permitido**: Verifica que la función `_enforce_policies()` rechaza URLs de hosts no permitidos lanzando una excepción `ValueError`.

#### Pruebas de Errores de API

- **test_search_by_title_failed**: Simula una respuesta con API Key inválida y verifica el manejo correcto del error.

### 2. test_resilience.py

Archivo con casos de prueba para validar la resiliencia y logging de la aplicación.

- **test_timeout_logged_redacted**: Verifica que cuando ocurre un timeout en la solicitud HTTP, se registra un log con los datos sensibles (Authorization headers) redactados correctamente como `<REDACTED>`.
- **test_http_500_branch**: Comprueba que la aplicación maneja correctamente un error HTTP 500 lanzando una excepción `RuntimeError`.
- **test_malformed_payload_branch**: Valida que cuando el payload es malformado, la aplicación lo devuelve y deja que capas posteriores lo rechacen.

### 3. tests_accounts.py

Archivo con pruebas de validación de datos de cuentas de usuario.

- **test_valid_account**: Verifica que una cuenta válida con todos los campos correctos pasa la validación.
- **test_missing_fields**: Prueba parametrizada que valida que si falta cualquier campo requerido (id, email, role, active), se lanza una excepción `ValueError`.
- **test_corrupt_types**: Verifica que cuando los tipos de datos son incorrectos, se lanzan excepciones `ValueError` o `TypeError`.

## Reportes de Cobertura

### Ubicación

Los reportes de cobertura de código están disponibles en: `evidencias/coverage/`

### Acceso

Para ver el reporte interactivo de cobertura:

1. Abre el archivo `evidencias/coverage/index.html` en un navegador web
2. El reporte mostrará:
   - Porcentaje de cobertura por módulo
   - Líneas cubiertas vs no cubiertas
   - Índices de clases y funciones

### Módulos Cubiertos

- `src/models/__init__.py`: Inicializador del módulo
- `src/models/imdb.py`: Clase principal IMDb y funciones de validación

## Logs de Ejecución

Los logs de las ejecuciones están disponibles en: `evidencias/logs/`

## Comandos Ejecutados

### Ejecución de Pruebas con Captura de Logs

A continuación se detallan los comandos ejecutados para generar los logs con evidencia de redacción de secretos:

#### 1. Ejecutar test_resilience.py con captura de logs

```bash
python3 -m pytest tests/test_resilience.py -v --log-cli-level=INFO --log-file=evidencias/logs/test_resilience.log 2>&1 | tee evidencias/logs/test_resilience_console.log
```

#### 2. Ejecutar test_accounts.py con captura de logs

```bash
python3 -m pytest tests/tests_accounts.py -v --log-cli-level=INFO --log-file=evidencias/logs/test_accounts.log 2>&1 | tee evidencias/logs/test_accounts_console.log
```

#### 3. Ejecutar test_imdb.py con captura de logs

```bash
python3 -m pytest tests/test_imdb.py -v --log-cli-level=INFO --log-file=evidencias/logs/test_imdb.log 2>&1 | tee evidencias/logs/test_imdb_console.log
```
