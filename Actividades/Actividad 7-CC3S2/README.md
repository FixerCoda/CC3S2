## Actividad 7 - Explorando estrategias de fusión en Git

-   Nombre: Diego Edson Bayes Santos
-   Fecha: 08/09/2025
-   Tiempo total:
-   Entorno usado: WSL en laptop personal Windows, en el IDE Visual Studio Code

### Ejercicios guiados

#### Evitar (o no) --ff

<!-- ¿Cuándo evitarías --ff en un equipo y por qué? -->

Por lo general, en un equipo se debe evitar --ff, ya que se pierde la trazabilidad sobre _branchs_ específicos. Se dificulta la revisión de auditorías al no saber quién integró qué _feature_. El historial lineal es recomendable únicamente si una rama no se modifica significativamente de la rama principal y solo en proyectos pequeños.

#### Trabajo en equipo con --no-ff

<!-- ¿Qué ventajas de trazabilidad aporta? ¿Qué problemas surgen con exceso de merges -->

Con una estrategia sin _fast-forward_, se puede visualizar en el log cuáles son las ramas integradas y cuándo se añadieron, lo que es útil para auditorías y revisiones de código. De esta manera, también se facilita la reversión del _merge_ en cualquier momento. Por otro lado, cuando hay exceso de _merges_, puede tener el efecto contrario al dificultar el seguimiento de la línea principal. Para evitar esto, se debe mantener un acuerdo sobre la calidad y descripción de cada _commit_ para reducir modificaciones y _merges_ innecesarios.

#### Squash con muchos commits

<!-- ¿Cuándo conviene? ¿Qué se pierde respecto a merges estándar? -->

Un _merge squash_ es conveniente para casos de _merges_ excesivos y poco significativos por separado. Esta estrategia los unifica en un solo commit limpio para mantener un historial más legible. Sin embargo, respecto a los _merges_ estándar, se pierde el detalle de _commits_ intermedios y se dificulta la reversión de un _feature_ específico.

### Conflictos reales con no-fast-forward

<!-- ¿Qué pasos adicionales hiciste para resolverlo?
¿Qué prácticas (convenciones, PRs pequeñas, tests) lo evitarían? -->

Para resolver conflictos, se debe usar `git diff` para identificarlos y corregir manualmente según la funcionalidad resultante deseada. En este caso, VS Code con la extensión de Git, te permite visualizar estos conflictos en una interfaz especial para definir qué cambios son los finales. Para evitar este tipo de situaciones, se recomienda atomizar las modificaciones en PRs más pequeñas. De esta manera, cada desarrollador coordina con el equipo para determinar su trabajo actual y paralelizar las responsabilidades en cada entrega, para reducir al máximo el solapamiento (por ejemplo, modificar la misma función en 2 ramas concurrentes).

### Comparar historiales tras cada método

<!-- ¿Cómo se ve el DAG en cada caso?
¿Qué método prefieres para: trabajo individual, equipo grande, repos con auditoría estricta? -->

En el caso de `fast-forward`, se observa un DAG simple y linear, en el cual no existe divergencia del historial, pues tanto `main` como la rama ejemplo apuntan al mismo commit. Esta estrategia es perfecta para un trabajo individual, pues no hay seguimiento de responsabilidades y la auditoría suele ser más directa. Por otro lado, sin `fast-forward` (`no-ff`) existe un merge explícito que une las 2 ramas y preserva el historial completo, tal como se observa en el log. En un equipo grande, es crucial la preservación del historial y el contexto completo de cada cambio, por lo que se preferien los `merges` sin `fast-forward` para auditorías más claras. Por último, usando el método `squash`, se genera un único commit en `main` con todos los cambios y mantiene el historial completo en la rama ejemplo. Cuando se requiere una auditoría más estrica, se puede emplear `squash` para situaciones de commits poco sustanciales o con arreglos pequeños que pueden ser unificados en un solo commit. Así, se mantiene un historial principal más limpio y menos complejo.

### Revertir una fusión (solo si HEAD es un merge commit)

Se usa `git revert` cuando se necesita deshacer commits en historial público compartido, ya que crea nuevos commits que revierten cambios sin reescribir historial, evitando conflictos con otros colaboradores. Por otra parte, `git reset` reescribe commits y puede causar conflictos en repos remotos si el historial ya fue publicado. Entonces, `git revert` es más seguro para trabajo colaborativo porque preserva el historial existente y permite un deshacer no destructivo.

### Variantes útiles para DevOps/DevSecOps

#### A) Fast-Forward Only (merge seguro)

#### B) Rebase + FF (historial lineal con PRs)

#### C) Merge con validación previa (sin commitear)

#### D) Octopus Merge (varias ramas a la vez)

#### E) Subtree (integrar subproyecto conservando historial)

#### F) Sesgos de resolución y normalización (algoritmo ORT)

#### G) Firmar merges/commits (auditoría y cumplimiento)
