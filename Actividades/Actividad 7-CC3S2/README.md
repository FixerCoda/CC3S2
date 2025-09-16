## Actividad 7 - Explorando estrategias de fusión en Git

-   Nombre: Diego Edson Bayes Santos
-   Fecha: 08/09/2025
-   Tiempo total:
-   Entorno usado: WSL en laptop personal Windows, en el IDE Visual Studio Code

### Ejercicios guiados

#### Evitar (o no) --ff

Por lo general, en un equipo se debe evitar --ff, ya que se pierde la trazabilidad sobre _branchs_ específicos. Se dificulta la revisión de auditorías al no saber quién integró qué _feature_. El historial lineal es recomendable únicamente si una rama no se modifica significativamente de la rama principal y solo en proyectos pequeños.

#### Trabajo en equipo con --no-ff

Con una estrategia sin _fast-forward_, se puede visualizar en el log cuáles son las ramas integradas y cuándo se añadieron, lo que es útil para auditorías y revisiones de código. De esta manera, también se facilita la reversión del _merge_ en cualquier momento. Por otro lado, cuando hay exceso de _merges_, puede tener el efecto contrario al dificultar el seguimiento de la línea principal. Para evitar esto, se debe mantener un acuerdo sobre la calidad y descripción de cada _commit_ para reducir modificaciones y _merges_ innecesarios.

#### Squash con muchos commits

Un _merge squash_ es conveniente para casos de _merges_ excesivos y poco significativos por separado. Esta estrategia los unifica en un solo commit limpio para mantener un historial más legible. Sin embargo, respecto a los _merges_ estándar, se pierde el detalle de _commits_ intermedios y se dificulta la reversión de un _feature_ específico.

### Conflictos reales con no-fast-forward

Para resolver conflictos, se debe usar `git diff` para identificarlos y corregir manualmente según la funcionalidad resultante deseada. En este caso, VS Code con la extensión de Git, te permite visualizar estos conflictos en una interfaz especial para definir qué cambios son los finales. Para evitar este tipo de situaciones, se recomienda atomizar las modificaciones en PRs más pequeñas. De esta manera, cada desarrollador coordina con el equipo para determinar su trabajo actual y paralelizar las responsabilidades en cada entrega, para reducir al máximo el solapamiento (por ejemplo, modificar la misma función en 2 ramas concurrentes).

### Comparar historiales tras cada método

### Revertir una fusión (solo si HEAD es un merge commit)

### Variantes útiles para DevOps/DevSecOps

#### A) Fast-Forward Only (merge seguro)

#### B) Rebase + FF (historial lineal con PRs)

#### C) Merge con validación previa (sin commitear)

#### D) Octopus Merge (varias ramas a la vez)

#### E) Subtree (integrar subproyecto conservando historial)

#### F) Sesgos de resolución y normalización (algoritmo ORT)

#### G) Firmar merges/commits (auditoría y cumplimiento)
