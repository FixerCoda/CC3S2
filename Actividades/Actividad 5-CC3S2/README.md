## Actividad 5: Construyendo un pipeline DevOps con Make y Bash

-   Nombre: Diego Edson Bayes Santos
-   Fecha: 14/09/2025
-   Tiempo total:
-   Entorno usado: WSL en laptop personal Windows, en el IDE Visual Studio Code

### Resumen del entorno

### Parte 1: Construir - Makefile y Bash desde cero

[comment]: # "Explica qué hace build y cómo $(PYTHON) $< > $@ usa $< y $@."
[comment]: # "Menciona el modo estricto (-e -u -o pipefail) y .DELETE_ON_ERROR."
[comment]: # "Diferencia entre la 1.ª y 2.ª corrida de build (idempotencia)."

#### Crear un Makefile básico

[comment]: # "Entrega: redacta 5-8 líneas explicando qué imprime help, por qué .DEFAULT_GOAL := help muestra ayuda al correr make sin argumentos, y la utilidad de declarar PHONY."
[comment]: # "Entrega: explica en 4-6 líneas la diferencia entre la primera y la segunda corrida, relacionándolo con el grafo de dependencias y marcas de tiempo."
[comment]: # "Entrega: en 5-7 líneas, comenta cómo -e -u -o pipefail y .DELETE_ON_ERROR evitan estados inconsistentes."
[comment]: # "Entrega: resume en 6-8 líneas qué significan fragmentos resultantes."
[comment]: # "Entrega: explica en 5-7 líneas por qué cambiar la fuente obliga a rehacer, mientras que tocar el target no forja trabajo extra."
[comment]: # "Entrega: en 4-6 líneas, interpreta advertencias/sugerencias (o comenta la ausencia de herramientas y cómo instalarlas en tu entorno)."
[comment]: # "Entrega: pega el hash y explica en 5-7 líneas cómo --sort=name, --mtime=@0, --numeric-owner y gzip -n eliminan variabilidad."
[comment]: # "Entrega: explica en 4-6 líneas por qué Make exige TAB al inicio de líneas de receta y cómo diagnosticarlo rápido."

#### Crear un script Bash

[comment]: # "Ejecuta ./scripts/run_tests.sh en un repositorio limpio. Observa las líneas "Demostrando pipefail": primero sin y luego con pipefail. Verifica que imprime "Test pasó" y termina exitosamente con código 0 (echo $?)."
[comment]: # "Edita src/hello.py para que no imprima "Hello, World!". Ejecuta el script: verás "Test falló", moverá hello.py a hello.py.bak, y el trap lo restaurará. Confirma código 2 y ausencia de .bak."
[comment]: # "Ejecuta bash -x scripts/run_tests.sh. Revisa el trace: expansión de tmp y PY, llamadas a funciones, here-doc y tuberías. Observa el trap armado al inicio y ejecutándose al final; estado 0."
[comment]: # "Sustituye output=$("$PY" "$script") por ("$PY" "$script"). Ejecuta script. output queda indefinida; con set -u, al referenciarla en echo aborta antes de grep. El trap limpia y devuelve código distinto no-cero."

### Parte 2: Leer - Analizar un repositorio completo

[comment]: # "Qué observaste con make -n y make -d (decisiones de rehacer o no)."
[comment]: # "Rol de .DEFAULT_GOAL, .PHONY y ayuda autodocumentada."

#### Makefile completo (con reproducibilidad y utilidades)

[comment]: # "Ejecuta make -n all para un dry-run que muestre comandos sin ejecutarlos; identifica expansiones $@ y $<, el orden de objetivos y cómo all encadena tools, lint, build, test, package."

[comment]: # "Ejecuta make -d build y localiza líneas "Considerando el archivo objetivo" y "Debe deshacerse", explica por qué recompila o no out/hello.txt usando marcas de tiempo y cómo mkdir -p $(@D) garantiza el directorio."
[comment]: # "Fuerza un entorno con BSD tar en PATH y corre make tools; comprueba el fallo con "Se requiere GNU tar" y razona por qué --sort, --numeric-owner y --mtime son imprescindibles para reproducibilidad determinista."
[comment]: # "Ejecuta make verify-repro; observa que genera dos artefactos y compara SHA256_1 y SHA256_2. Si difieren, hipótesis: zona horaria, versión de tar, contenido no determinista o variables de entorno no fijadas."
[comment]: # "Corre make clean && make all, cronometrando; repite make all sin cambios y compara tiempos y logs. Explica por qué la segunda es más rápida gracias a timestamps y relaciones de dependencia bien declaradas."
[comment]: # "Ejecuta PYTHON=python3.12 make test (si existe). Verifica con python3.12 --version y mensajes que el override funciona gracias a ?= y a PY="${PYTHON:-python3}" en el script; confirma que el artefacto final no cambia respecto al intérprete por defecto."
[comment]: # "Ejecuta make test; describe cómo primero corre scripts/run_tests.sh y luego python -m unittest. Determina el comportamiento si el script de pruebas falla y cómo se propaga el error a la tarea global."
[comment]: # "Ejecuta touch src/hello.py y luego make all; identifica qué objetivos se rehacen (build, test, package) y relaciona el comportamiento con el timestamp actualizado y la cadena de dependencias especificada."
[comment]: # "Ejecuta make -j4 all y observa ejecución concurrente de objetivos independientes; confirma resultados idénticos a modo secuencial y explica cómo mkdir -p $(@D) y dependencias precisas evitan condiciones de carrera."
[comment]: # "Ejecuta make lint y luego make format; interpreta diagnósticos de shellcheck, revisa diferencias aplicadas por shfmt y, si está disponible, considera la salida de ruff sobre src/ antes de empaquetar."

### Parte 3: Extender

[comment]: # "Qué detectó shellcheck/shfmt (o evidencia de que no están instalados)."
[comment]: # "Demostración de rollback con trap (códigos de salida y restauración)."
[comment]: # "Reproducibilidad: factores que la garantizan (--sort, --mtime, --numeric-owner, TZ=UTC) y el resultado de verify-repro."

### Incidencias y mitigaciones

### Conclusión operativa
