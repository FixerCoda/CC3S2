# Fase 1: Exploración y Análisis

## Singleton

Para garantiza una sola instancia, la clase `SingletonMeta` sobrescribe el método `__call__` que se ejecuta al crear una instancia. Se mantiene un diccionario `_instances` de tipo `ConfigSingleton` que almacena la única instancia por clase. Cuando se intenta crear un objeto, se verifica si ya existe en `_instances`. En caso exista, se devuelve la instancia existente, y si no, crea una nueva y la guarda. El `threading.Lock` se emplea para evitar condiciones de carrera en entornos con múltiples hilos. Sin el lock, dos hilos podrían ejecutar simultáneamente la verificación y ambos podrían crear instancias separadas, rompiendo el patrón Singleton.
