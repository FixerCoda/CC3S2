## Actividad 5: Construyendo un pipeline DevOps con Make y Bash

-   Nombre: Diego Edson Bayes Santos
-   Fecha: 15/09/2025
-   Tiempo total: 4h
-   Entorno usado: WSL en laptop personal Windows, en el IDE Visual Studio Code

### Resumen del entorno

-   SO: Windows (version 10.0.26100.6584) con WSL (version 2.1.5.0)
-   Ubuntu (WSL): Linux 5.15.146.1-microsoft-standard-WSL2 x86_64
-   Bash: 5.2.21(1)-release (/usr/bin/bash)
-   Make: GNU Make 4.3
-   Python: Python 3.12.3
-   Tar: tar (GNU tar) 1.35
-   SHA256: sha256sum (GNU coreutils) 9.4

### Parte 1: Construir - Makefile y Bash desde cero

#### Crear un Makefile básico

<!-- Entrega: redacta 5-8 líneas explicando qué imprime help, por qué .DEFAULT_GOAL := help muestra ayuda al correr make sin argumentos, y la utilidad de declarar PHONY. -->

-   El target `help` imprime un mensaje de ayuda que describe los targets disponibles en el makefile. Con el uso del comando `grep` y una definición de targets estándar en el código, se establece una expresión regulara para identificar los nombres y las descripciones de cada target. Además, se establece este target como el objetivo por defecto con `.DEFAULT_GOAL`. Esto permite la rápida adopción y entendimiento para nuevos integrantes o desarrolladores que quieran explorar el código. Por último, con la declaración `.PHONY` permite definir targets que no generan archivos físicos y, así, prevenir conflictos con posibles archivos del mismo nombre. Asimismo, mejora el rendimiento al evitar comprobaciones innecesarias del sistema de archivos.

<!-- Entrega: explica en 4-6 líneas la diferencia entre la primera y la segunda corrida, relacionándolo con el grafo de dependencias y marcas de tiempo. -->

-   Las secuencia de dependencias sería la siguiente: `build` -> `out/hello.txt` -> `src/hello.py`. Para la primera ejecución, `make build` llama al target `out/hello.txt`, el cual ejecuta el prerrequisito `src/hello.py`con `python3` y lo almacena en el archivo objetivo del mismo nombre del target (`out/hello.txt`). Como este último archivo fue creado posteriormente al script de python, su marca de tiempo es más reciente. Por esta razón, en la segunda ejecución, `make` detecta esta diferencia en las marcas de tiempo y considera al target ya actualizado, por lo tanto no lo reejecuta. De esta manera, se mantiene el grafo de dependencias consistente y se evita el trabajo redundante.

<!-- Entrega: en 5-7 líneas, comenta cómo -e -u -o pipefail y .DELETE_ON_ERROR evitan estados inconsistentes. -->

-   En primer lugar, el flag `-e` hace que el script se detenga inmediatamente si cualquier comando falla, evitando así la continuación de un proceso que ya ha encontrado un error. El flag `-u` asegura que cualquier variable no inicializada provoque un error, lo que ayuda a detectar errores de programación. El flag `-o pipefail` garantiza que si cualquiera de los comandos en una tubería falla, el estado de salida de la tubería será el del comando fallido, en lugar del último comando exitoso. Por último, la directiva `.DELETE_ON_ERROR` en el Makefile asegura que si un comando falla durante la construcción de un objetivo, cualquier archivo objetivo parcial o corrupto se elimine automáticamente. Ambas estrategias evitan, así, estados inconsistentes en el sistema de archivos.

<!-- Entrega: resume en 6-8 líneas qué significan fragmentos resultantes. -->

-   El ensayo o `dry-run` se realiza con `make -n` confirma la lógica de Makefile mediante una ejecución de prueba que realmente no realiza ningún comando. Con `make -d`, se imprime información adicional para el `debugging` además del procesamiento regular. Esta información incluye la examinación del grafo de dependencias, la comparación de marcas de tiempo y la verificación de los targets que necesiten reconfiguración. Además, con herramientas como `grep`, se puede comprobar si algún archivo en concreto está siendo considerado en el flujo de Makefile. Para el comando ejecutado, se reafirma esta consideración. Incluso, si buscamos la línea específica en el mismo log, podemos observar que el archivo no existe (dado que se aplicó `make clean` previamente), así que procede a analizar su prerrequisito `src/hello.py`.

<!-- Entrega: explica en 5-7 líneas por qué cambiar la fuente obliga a rehacer, mientras que tocar el target no forja trabajo extra. -->

-   La comprobación de marcas de tiempo en la ejecución de Makefile se realiza en el orden de origen hacia prerrequisitos. Lo dependencia en el flujo actual es `out/hello.txt` -> `src/hello.py`. Por lo tanto, una marca de tiempo más reciente del prerrequisito ( `src/hello.py`) implica un cambio que se refleja en el target invocado (`out/hello.txt`). Entonces, este cambio obliga a la reconstrucción. Por otro lado, un cambio en el target no genera una diferencia en las marcas de tiempo que active la reconstrucción, pues el prerrequisito sigue siendo menos reciente que el target.

<!-- Entrega: en 4-6 líneas, interpreta advertencias/sugerencias (o comenta la ausencia de herramientas y cómo instalarlas en tu entorno). -->

-   Para esta inciso, se introdujeron algunas modificaciones específicas que generan advertencias en los comandos. El uso de `shellcheck` muestra un error en la sintaxis de la asignación de una variable que se resuelve removiendo los espacios. Además, especifica la línea exacta, el código del error e información adicional en la documentación de la misma herramienta.

```
In scripts/run_tests.sh line 10:
PY = "${PYTHON:-python3}"
   ^-- SC2283 (error): Remove spaces around = to assign (or use [ ] to compare, or quote '=' if literal).

For more information:
  https://www.shellcheck.net/wiki/SC2283 -- Remove spaces around = to assign ...
```

-   Por otro lado, la herramienta de `shfmt` muestra problemas con la indentación. La forma de identificar las advertencias es con los símbolos `-`, el cual indica las líneas que deberían ser modificadas, y `+`, que muestra las sugerencias de modificaciones para aplicar

```
--- scripts/run_tests.sh.orig
+++ scripts/run_tests.sh
@@ -10,19 +10,19 @@
 PY = "${PYTHON:-python3}"

 # Directorio de código fuente
-    SRC_DIR="src"
+SRC_DIR="src"

 # Archivo temporal
 tmp="$(mktemp)"

 # Limpieza segura + posible rollback de hello.py si existiera un .bak
 cleanup() {
-rc="$1"
-rm -f "$tmp"
-if [ -f "${SRC_DIR}/hello.py.bak" ]; then
-    mv -- "${SRC_DIR}/hello.py.bak" "${SRC_DIR}/hello.py"
-fi
-exit "$rc"
+	rc="$1"
+	rm -f "$tmp"
+	if [ -f "${SRC_DIR}/hello.py.bak" ]; then
+		mv -- "${SRC_DIR}/hello.py.bak" "${SRC_DIR}/hello.py"
+	fi
+	exit "$rc"
 }
 trap 'cleanup $?' EXIT INT TERM
```

<!-- Entrega: pega el hash y explica en 5-7 líneas cómo --sort=name, --mtime=@0, --numeric-owner y gzip -n eliminan variabilidad. -->

-   La empaquetación debe entregar resultados iguales para versiones iguales (idempotencia). Para esto, no solo basta con que el contenido sea el mismo, sino que también los metadatos asociados. Las opciones empleadas sirven para eliminar esta variabilidad de información que cambia entre ejecuciones. `--sort=name` asegura un orden consistente de archivos en el TAR. La opción `--mtime=@0` establece todas las marcas de tiempo a un estándar. Además, `--numeric-owner` utiliza IDs para usuarios y grupos numéricos, lo que remueve las dependencias del entorno de sistema de ejecución. En conjunto, con `--owner=0` y `--group=0`, normaliza esta información al asignar el mismo dueño a la raíz. Por último, `gzip -n` excluye el nombre original del archivo y la marca de tiempo del encabezado en la compresión. El resultado generado está garantizado a ser idéntico para versiones iguales.

```
da0ee78e63abe78a9ea0dd4d8962f2ae636d2fddef082ff9fa115a60df236882
```

<!-- Entrega: explica en 4-6 líneas por qué Make exige TAB al inicio de líneas de receta y cómo diagnosticarlo rápido. -->

-   Make exige el TAB porque estandariza el delimitador sintáctico que distingue las recetas de otros elementos del Makefile, similar al funcionamiento de Python. Los espacios no son válidos por la ambigüedad de su uso (por ejemplo para cierto entorno, un TAB puede representar 4 espacios y para otro, 8). Como se muestra en la reproducción en evidencia, el error correspondiente a este caso es `missing separator`. En la salida, se identifica el número de línea donde ocurre el error y cómo el flujo se detiene inmediatamente.

#### Crear un script Bash

<!-- Ejecuta ./scripts/run_tests.sh en un repositorio limpio. Observa las líneas "Demostrando pipefail": primero sin y luego con pipefail. Verifica que imprime "Test pasó" y termina exitosamente con código 0 (echo $?). -->

-   En el script, la ejecución de `set +o pipefail` hace que el código de salida sea el último comando ejecutado (comportamiento por defecto), por lo que en el flujo condicional, el resultado es exitoso al ser la última ejecución `true`. Sin embargo, al reactivarlo, el código de salida es 0 solo si todos los comandos se ejecutaron exitosamente. Caso contrario, se muestra el resultado del último código de salida erróneo o diferente de 0, tal como se ve en el segundo caso, donde se muestra la salida de la primera ejecución `false`. Por último, luego de esta sección, se verifica la impresión del test con código 0.

```
echo "Demostrando pipefail:"
set +o pipefail
if false | true; then
	echo "Sin pipefail: el pipe se considera exitoso (status 0)."
fi
set -o pipefail
if false | true; then
	:
else
	echo "Con pipefail: se detecta el fallo (status != 0)."
fi
```

```
echo $?
>> 0
```

<!-- Edita src/hello.py para que no imprima "Hello, World!". Ejecuta el script: verás "Test falló", moverá hello.py a hello.py.bak, y el trap lo restaurará. Confirma código 2 y ausencia de .bak. -->

-   El `trap` definido captura los eventos de terminación del script, ya sea regularmente o por interrupción, y activa la funcion de limpieza `cleanup`. Como el test falla, automáticamente la función de prueba realiza un backup del archivo que generó error para su depuración, además de evitar su ejecución, y lanza el código de salida 2. Posteriormente, ya en la limpieza, la función revisa la existencia de este `backup` y lo restaura. Este mecanismo se utiliza para evitar que el código se encuentre en estados que generen errores. Asimismo, vuelve a lanzar el código de salida 2, tal como se puede comprobar en el terminal.

```
echo $?
>> 2
```

<!-- Ejecuta bash -x scripts/run_tests.sh. Revisa el trace: expansión de tmp y PY, llamadas a funciones, here-doc y tuberías. Observa el trap armado al inicio y ejecutándose al final; estado 0. -->

-   El trace muestra la ejecución robusta del script: se inicializan opciones estrictas (`-euo pipefail`), se expanden variables (`PY=python3`, `tmp` con `mktemp`) y se arma el trap para limpieza. Las funciones `check_deps` y `run_tests` se ejecutan correctamente, verificando dependencias y validando la salida del script. Al terminar con estado 0, el trap ejecuta `cleanup` que elimina el archivo temporal y confirma que no existía backup (`.bak`), demostrando una finalización exitosa (estado 0) sin necesidad de `rollback`.

<!-- Sustituye output=$("$PY" "$script") por ("$PY" "$script"). Ejecuta script. output queda indefinida; con set -u, al referenciarla en echo aborta antes de grep. El trap limpia y devuelve código distinto no-cero. -->

-   A pesar de la sustitución y que la variable `output` quede indefinida, la ejecución de los comandos en el condicional se realizan en `subshells`. Por lo tanto, la opción `set -u` no aplica a estos comandos y, así, se ejecuta igualmente, generando arrastre de error al existir inconsistencias en el flujo. Si se ejecuta el comando de impresión de `output` previo al condicional, el flujo se detiene correctamente y se recibe el código de estado 1.

### Parte 2: Leer - Analizar un repositorio completo

#### Makefile completo (con reproducibilidad y utilidades)

<!-- Ejecuta make -n all para un dry-run que muestre comandos sin ejecutarlos; identifica expansiones $@ y $<, el orden de objetivos y cómo all encadena tools, lint, build, test, package. -->

-   El comando muestra la secuencia de ejecución sin realizarla: primero `tools` (verifica dependencias), luego `lint` (análisis estático), `build` (genera `out/hello.txt`), `test` (ejecuta pruebas) y finalmente `package` (crea el `tarball`). Las variables automáticas `$@` (target) y `$<` (primer prerrequisito) se expanden a sus rutas respectivas, por ejemplo, de `$(PYTHON) $< > $@` a `$(PYTHON) src/hello.py > out/hello.txt`.

<!-- Ejecuta make -d build y localiza líneas "Considerando el archivo objetivo" y "Debe deshacerse", explica por qué recompila o no out/hello.txt usando marcas de tiempo y cómo mkdir -p $(@D) garantiza el directorio. -->

-   Make compara las marcas de tiempo de `out/hello.txt` y `src/hello.py`. Si la fuente es más reciente, marca el target como "must remake" y recompila; de lo contrario, omite la acción. `mkdir -p $(@D)` asegura que el directorio `out/` exista antes de escribir el archivo, evitando errores de escritura.

<!-- Fuerza un entorno con BSD tar en PATH y corre make tools; comprueba el fallo con "Se requiere GNU tar" y razona por qué --sort, --numeric-owner y --mtime son imprescindibles para reproducibilidad determinista. -->

-   Al forzar BSD tar, `make tools` falla porque GNU tar es esencial para opciones como `--sort=name` (orden consistente de archivos), `--numeric-owner` (UIDs/GIDs numéricos) y `--mtime` (timestamp fijo). Estas opciones eliminan variabilidad y garantizan que el tarball sea idéntico en cada build.

```
PATH="/tmp/fake-bin/:$PATH" make tools
>> Se requiere GNU tar
>> make: *** [Makefile:50: tools] Error 1
```

<!-- Ejecuta make verify-repro; observa que genera dos artefactos y compara SHA256_1 y SHA256_2. Si difieren, hipótesis: zona horaria, versión de tar, contenido no determinista o variables de entorno no fijadas. -->

-   Genera dos tarballs independientes y compara sus hashes `SHA256`. Dado que se excluyeron posibles causas como la zona horaria no UTC, metadatos de archivos no normalizados, o herramientas no deterministas. El target asegura que el entorno esté limpio antes de cada build para evitar contaminación.

```
make verify-repro
>> SHA256_1=ad917bfc2c042f07c8de4ef70fcbff91a49977d589de88932da474592ba1c545
>> SHA256_2=ad917bfc2c042f07c8de4ef70fcbff91a49977d589de88932da474592ba1c545
>> OK: reproducible
```

<!-- Corre make clean && make all, cronometrando; repite make all sin cambios y compara tiempos y logs. Explica por qué la segunda es más rápida gracias a timestamps y relaciones de dependencia bien declaradas. -->

-   La primera ejecución (`make all`) construye todo desde cero. La segunda es más rápida porque make verifica que los timestamps de los targets sean más recientes que los de sus dependencias y omite regenerarlos. Esto demuestra la optimización mediante el grafo de dependencias.

```
make clean
time make all 2>&1
>> real    0m0.284s

time make all 2>&1
>> real    0m0.201s
```

<!-- Ejecuta PYTHON=python3.12 make test (si existe). Verifica con python3.12 --version y mensajes que el override funciona gracias a ?= y a PY="${PYTHON:-python3}" en el script; confirma que el artefacto final no cambia respecto al intérprete por defecto. -->

-   El override funciona gracias a `?=` en el Makefile (asigna solo si no está definida) y a `PY="${PYTHON:-python3}"` en el script, que usa la variable correcta. El artefacto final no cambia porque el contenido de `hello.txt` es idéntico independientemente del intérprete.

<!-- Ejecuta make test; describe cómo primero corre scripts/run_tests.sh y luego python -m unittest. Determina el comportamiento si el script de pruebas falla y cómo se propaga el error a la tarea global. -->

-   El orden de ejecución está dictado por su definición en el Makefile. Si el script falla, termina con código de error y `make` aborta, propagando el fallo al target `test` y deteniendo la ejecución de targets dependientes.

<!-- Ejecuta touch src/hello.py y luego make all; identifica qué objetivos se rehacen (build, test, package) y relaciona el comportamiento con el timestamp actualizado y la cadena de dependencias especificada. -->

-   `touch src/hello.py` actualiza su marca de tiempo. Al correr `make all`, los targets `build`, `test` y `package` se rehacen porque dependen del archivo modificado. Esto refleja la cascada de dependencias definidas en el Makefile.

<!-- Ejecuta make -j4 all y observa ejecución concurrente de objetivos independientes; confirma resultados idénticos a modo secuencial y explica cómo mkdir -p $(@D) y dependencias precisas evitan condiciones de carrera. -->

-   Los targets independientes (como `lint` y `tools`) se ejecutan en paralelo. `mkdir -p $(@D)` es seguro en concurrencia porque crea directorios de forma idempotente. Las dependencias precisas evitan condiciones de carrera, asegurando que los targets se construyan en el orden correcto.

<!-- Ejecuta make lint y luego make format; interpreta diagnósticos de shellcheck, revisa diferencias aplicadas por shfmt y, si está disponible, considera la salida de ruff sobre src/ antes de empaquetar. -->

-   El target `make lint` ejecuta `shellcheck` (análisis de bugs en Bash) y `shfmt` (verificación de formato). Además, con `make format`, se aplica el formateo automático con `shfmt -w`. Por último, `ruff` analiza el código Python, asegurando calidad antes del empaquetado.

### Parte 3: Extender

<!-- Qué detectó shellcheck/shfmt (o evidencia de que no están instalados). -->

-   La herramienta `shellCheck` detectó un error de quoting (`SC2283`) al usar espacios adicionales alrededor de una asignación. Además, `shfmt` aplicó formato consistente (indentación de 2 espacios, alineación).

<!-- Demostración de rollback con trap (códigos de salida y restauración). -->

-   Al ejecutarse un error, el script lo detecta y lo interrumpe (`exit 2`), ejecuta el trap y restaura `hello.py` desde `.bak`. El `cleanup` preserva el código de salida original (2) y garantiza que no queden artefactos parciales, demostrando robustez ante fallos inesperados.

<!-- Reproducibilidad: factores que la garantizan (--sort, --mtime, --numeric-owner, TZ=UTC) y el resultado de verify-repro. -->

-   El primer `make benchmark` construye todo (≈0.20s). El segundo es ligeramente más rápido (≈0.18s) gracias a la caché de `make`. Tras `touch src/hello.py`, se rehacen `build`, `test` y `package`, demostrando que el grafo de dependencias reconstruye solo lo necesario basado en marcas de tiempo.

### Incidencias y mitigaciones

-   En el último inciso de la primera parte, la ejecución no se dio como lo esperado debido a que la ejecución de los comandos se realizó en un subshell (dentro del condicional), por lo que no se interrumpió el error incluso con el uso de `set -u pipefail`. Para solucionar esto, se introdujo una verificación redundante y previa al condicional que detiene el flujo dentro del shell principal y resulta en el código de salida 1, como se planeó para el ejercicio.

```
    local output
	("$PY" "$script")
    echo "$output"
	if ! echo "$output" | grep -Fq "Hello, World!"; then
```

### Conclusión operativa

Este pipeline de CI/CD es robusto por su estricto control de errores (`set -euo pipefail`, `.DELETE_ON_ERROR`) y `builds` deterministas (reproducibilidad con GNU tar). Su diseño incremental optimiza tiempos y recursos, mientras las validaciones de `lint`, `tests` y `rollback` automático garantizan entregas consistentes y confiables.
