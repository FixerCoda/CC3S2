## Actividad 6 - Explorando estrategias de fusión en Git

-   Nombre: Diego Edson Bayes Santos
-   Fecha: 08/09/2025
-   Tiempo total:
-   Entorno usado: WSL en laptop personal Windows, en el IDE Visual Studio Code

### Conceptos básicos de Git: Comienza con una experiencia práctica

#### git --version:

Muestra la versión instalada de Git. También puede ser usado para verificar que tengamos Git instalado.

-   Log: git-version.txt

#### git config: Preséntate a Git

Lista las configuraciones actuales del Git.

-   Log: config.txt

#### git init: Donde comienza tu viaje de código

Crea un nuevo repositorio Git en el directorio actual y muestra el status actual.

-   Log: init-status.txt

#### git add: Preparando tu código

Con _git add_, se agregan cambios al área de _staging_ para incluirlos en el próximo commit.

-   Log: add-commit.txt

#### git commit: registra cambios

Luego, con _git commit_, se guardan estos cambios y se registran en el historial con un mensaje asociado.

-   Log: add-commit.txt

#### git log: Recorrer el árbol de commits

Muestra el historial de commits del proyecto. Se pueden usar _flags_ como _--oneline_ para simplificar el _output_.

-   Log: log-oneline.txt

### Trabajar con ramas: La piedra angular de la colaboración

#### git branch: Entendiendo los conceptos básicos de Git branch

Sirve para listar y crear ramas en el repositorio.

-   Log: branches.txt

#### git checkout/git switch: Cambiar entre ramas

Permite moverse a otra rama o incluso a otro commit.

#### git merge <Branch-Name>: Fusionando ramas

Cuando existen varias ramas, se puede usar _git merge_ para fusionar los cambios entre distintas ramas.

-   Log: merge-o-conflicto.txt

#### git branch -d: Eliminando una rama

Con _git branch -d_, se puede eliminar una rama no principal.

### Preguntas

-   ¿Cómo te ha ayudado Git a mantener un historial claro y organizado de tus cambios?
-   ¿Qué beneficios ves en el uso de ramas para desarrollar nuevas características o corregir errores?
-   Realiza una revisión final del historial de commits para asegurarte de que todos los cambios se han registrado correctamente.
-   Revisa el uso de ramas y merges para ver cómo Git maneja múltiples líneas de desarrollo.

### Ejercicios

#### Manejo avanzado de ramas y resolución de conflictos

Cuando el _git merge_ no puede resolver diferencias automáticamente, se debe resolver manualmente los conflictos en archivos.

-   Log: merge-o-conflicto.txt

#### Exploración y manipulación del historial de commits

Con _git revert HEAD_, se revierte el commit más reciente con un commit automático de reversión de cambios. Además, con _git rebase -i HEAD~_, se puede especificar cuantos commits se desea retroceder.

-   Log: revert.txt, rebase.txt

#### Creación y gestión de ramas desde commits específicos

Se puede visualizar el historial de commits en forma de árbol para identificar mejor la línea de cambios con _git log --graph_.

-   Log: log-graph.txt

#### Manipulación y restauración de commits con git reset y git restore

Con _git reset_, además de mover la rama actual a otro commit, también puedes escoger descartar los cambios. Por otro lado, con _git restore_, puedes restaurar archivos a un estado anterior, por ejemplo desde _staging_.

#### Cherry-Picking y Git Stash

Usando _git stash_ se puede almacenar cambios para despejar el área de trabajo y realizar otros cambios. Se pueden recuperarlos en cualquier momento, aunque puede generar conflictos con cambios no publicados.

-   Log: stash.txt
