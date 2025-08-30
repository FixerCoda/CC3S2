## Actividad 1: Introducción a DevOps y DevSecOps

-   Nombre: Diego Edson Bayes Santos
-   Fecha: 30/08/2025
-   Tiempo total: 1h
-   Entorno usado: Esta actividad se realizó en una laptop personal con el sistema operativo Windows, en el IDE Visual Studio Code.

### 1. DevOps vs. Cascada Tradicional (Investigación + Comparación)

![DevOps vs Cascada](./imagenes/devops-vs-cascada.png)

El modelo cascada tradicional o Waterfall aborda el desarrollo de software de manera secuencial, en el cual cada etapa del proyecto se inicia una detrás de otra. Esto genera demoras grandes en las entregas:

-   Los errores se detectan en las etapas finales por lo que se debe reiniciar la secuencia para corregirlos
-   Pequeños cambios en los requerimientos deben esperar a que el desarrollo actual acabe su proceso
-   No se obtiene feedback inmediato, sino hasta el final del despliegue.
    Por otro lado, la metodología DevOps consiste en un desarrollo iterativo, mediante el cual se sigue la secuencia desde planeamiento hasta lanzamiento en pequeños lotes, a diferencia de todo el proyecto. Esto incluye la creación de procesos automatizados de construcción, integración y testing, de tal forma que se pueda detectar inmediatamente cuando un cambio nuevo evita el correcto funcionamiento y despliegue (Kim et al., 2016). Es decir, la detección de errores e implementación del feedback se realiza de manera continua y a corto plazo. Además, uno de sus pilares es la automatización de procesos, la cual disminuye el riesgo del factor humano en distintas etapas del desarrollo.

Adicionalmente, no todos los casos presentan a DevOps como la mejor opción. En el campo de los software embebidos para dispositivos médicos, cada producto debe cumplir con ciertas normativas y regulaciones estrictas. El ciclo de vida está muy regulado y exige que cada fase del desarrollo se documente y se apruebe antes de pasar a la siguiente. Esta conformidad regulatoria está a cargo de auditorías externas como la FDA o las certificadoras ISO y es de caracter obligatorio. Además, el acoplamiento del hardware con el software es crítico y requiere entornos físicos específicos que dificultan la iteración del desarrollo y elevan los costos de reprocesos. En esta situación, se sacrifica la velocidad del DevOps, para adoptar la conformidad y seguridad de la metodología Waterfall.

### 2. Ciclo tradicional de dos pasos y silos (limitaciones y anti-patrones)

![Silos Organizacionales](./imagenes/silos-equipos.jpg)

Existen importantes limitaciones del ciclo "construcción -> operación" sin integración continua:

-   En el entorno tradicional, por lo general, se cuenta con los equipos de Desarrollo, QA y Operaciones. Ellos operan de manera aislada, por lo que las solicitudes se trabajan en un sistema de tickets. Esto genera cuellos de botella que retrasan el desarrollo al cada equipo presentar sus propias responsabilidades y prioridades. Por ejemplo, si el equipo de QA identifica un error crítico que evita el análisis del resto del código, solicita un cambio en el código al equipo de Desarrollo (_handoff_ de tareas). Ahora, deben esperar a su resolución para continuar con el resto de pruebas, alargando así el tiempo total de entrega.
-   Otro gran problema es el desentendimiento de las responsabilidades. Cada equipo cuenta con su propio conjunto de responsabilidades y prioridades. El objetivo del equipo de desarrollo suele ser entregar la mayor cantidad de código al equipo de QA para que este lo valide, lo cual reduce drásticamente la calidad del código y, por ende, incrementa el tiempo en la construcción de código validado y probado. El equipo de operaciones opta por un entorno más estable, debido a que cada cambio conlleva potenciales errores en producción. El ambiente suele estar fuertemente marcado por los elogios al equipo de Desarrollo en casos de éxito y a la responsabilización del equipo de Operaciones en casos de fallos.
    Asimismo, se pueden identificar ciertos anti-patrones:
-   _Throw over the wall_: Hace referencia a la existencia de barreras de comunicación y colaboración entre estos equipos que funcionan como silos organizacionales. Tal como se indicó antes, los equipos se centran en realizar sus actividades y _lanzarlas_ rápidamente al siguiente equipo, lo que dificulta el trabajo de este último al recibir resultados mínimamente viables. Además, estos muros también generan mayor tiempo promedio de reparación (_MTTR_), pues ante la presencia de errores, ralentiza la comunicación y la eficacia en resolución de errores.
-   _Seguridad como auditoría tardía_: Sin integración continua, el análisis de la seguridad se suele desplazar al final del ciclo de desarrollo. Sin embargo, la identificación de fallos tardía genera _retrabajos_ costosos en el rediseño y reconstrucción de componentes previamentes funcionales, muchas veces incluso iniciando el código desde cero.
