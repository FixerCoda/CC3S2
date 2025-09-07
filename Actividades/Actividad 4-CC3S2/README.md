## Actividad 4: Introducción a herramientas CLI en entornos Unix-like para DevSecOps

-   Nombre: Diego Edson Bayes Santos
-   Fecha: 03/09/2025
-   Tiempo total: 3h
-   Entorno usado: WSL en laptop personal Windows, en el IDE Visual Studio Code

### Sección 1: Manejo sólido de CLI

-   Mediante el comando _cd_, se cambió el directorio a `/etc`. Se listó todos los archivos con el comando _ls_ y se añadió el flag _a_ para incluir archivos ocultos. El operador _>_ permite almacenar el stdout resultante del comando en el archivo en la ruta indicada.

```
cd /etc
ls -a > ~/etc_lista.txt
```

-   Se usó el comando _find_ para buscar archivos dentro en la ruta `tmp` (sin entrar dentro de subdirectorios) usando el patrón indicado (nombres que terminen en _.txt_ o _.doc_). El resultado es una lista con todas los nombres de archivos que cumplen la expresión. Se ordena alfabéticamente mediante _sort_ y se conecta con el comando _wc_, el cual cuenta la cantidad de líneas y arroja como resultado el número de archivos que cumplen con el patrón de _find_.

```
find /tmp -maxdepth 1 -type f \( -name '*.txt' -o -name '*.doc' \) | sort | wc -l
```

-   Con el comando _printf_, se imprime cadenas de texto formateadas. Luego, se almacena en el archivo _test.txt_. Además, se usa _nl_ para mostrar el archivo recién creado con sus números de lineas. Las flags utilizadas especifican que se deben numerar todas las líneas.

```
printf "Línea1\nLínea2\n" > test.txt
nl -ba test.txt
```

-   Para probar almacenar salidas por stderr, se utiliza el error de intentar listar contenidos dentro de un directorio inexistente usando _ls_. El operador _2>>_ indica que se use el canal stderr y se añada el contenido al final (no sobreescribir) del archivo indicado. Además, se añade un _true_ al final de la operación para evitar que el flujo del script continue sin que aparezca error.

```
ls comandoinvalidado 2>> errores.log || true
```

-   Se inicia generando archivos con el comando _touch_. Para verificar la creación, se usa _ls_ para listar uno por línea los archivos que empiecen con _archivo_. Luego, usamos el comando _find_ ya utilizado anteriormente para hallar los archivos que cumplan con la expresión indicada. Este resultado alimenta al input de _xargs_ e imprime en terminal, usando _echo_ cada línea entregada añadiéndole el prefijo _rm --_. Si no se encuentra ningún archivo que cumpla el patrón, no se imprime nada. Con lo impreso, se puede usar ese mismo output para borrar los archivos con el comando _rm_. Se repite el proceso para los archivos creados con extensión _.doc_

```
touch archivo1.txt archivo2.txt archivo3.doc
ls -1 archivo*
find . -maxdepth 1 -name 'archivo*.txt' | xargs -r echo rm --
rm -- ./archivo1.txt ./archivo2.txt
find . -maxdepth 1 -name 'archivo*.doc' | xargs -r echo rm --
rm -- ./archivo3.doc
```

### Sección 2: Administración básica

#### 1. Usuarios y grupos

-   Se procede a añadir un nuevo usuario llamado _devsec_ y un nuevo grupo llamado _ops_. Con el uso de _usermod_, se añade el grupo creado a la lista de grupos suplementarios de _devsec_. La opción _-a_ del comando asegura que el nuevo grupo no reemplace los grupos ya existentes del usuario.

```
sudo adduser devsec
sudo addgroup ops
sudo usermod -aG ops devsec
```

-   Se genera un nuevo archivo vacío con el comando _touch_ y se le asigna la propiedad al usuario _devsec_ del grupo _ops_. Además, al propio archivo se le asignan los siguientes permisos: El 6 indica permisos de escritura y lectura al propietario; el 4 indica permisos de lectura a los usuarios que pertenezcan a la lista de grupos permitidos por el archivo; y 0 para indicar que no hay permisos para otro tipo de usuarios.

```
touch secreto.txt
sudo chown devsec:ops secreto.txt
sudo chmod 640 secreto.txt
```

-   El comando _getent_ se usa para explorar archivos en el sistema. Se usa este comando para explorar en _/etc/passwd/_ si el usuario devsec existe; así como la existencia del grupo _ops_

```
getent passwd devsec | tee evidencia_passwd_devsec.txt
getent group ops | tee evidencia_group_ops.txt
```

-   Se corrobora los permisos utilizando el comando _namei_ e imprimiendo la metadata del archivo (incluyendo los permisos) con el comando _stat_.

```
namei -l secreto.txt | tee evidencia_namei_secreto.txt
stat -c '%A %a %U %G %n' secreto.txt | tee evidencia_stat_secreto.txt
```

#### 2. Procesos

-   Con el comando _whoami_, se puede observar nuestro nombre de usuario. Se lista todos los procesos en ejecución con _ps aux_. Además, con _grep bash_ se puede filtrar todos los procesos con "bash" en sus resultados.

```
whoami | tee evidencia_whoami.txt
ps aux | tee evidencia_ps_aux.txt
ps aux | grep bash | tee evidencia_pid_grep.txt
```

-   La expresión _"$$"_ hace referencia al ID del proceso (PID) del terminal actual. Además, podemos extender esa información con _ps_ para mostrar datos como el ID del proceso padre, el ID numérico del usuario, el tiempo transcurrido desde el inicio del proceso, entre otros. Por último, el comando _kill_ en conjunto con la opción _-0_ permite revisar si el proceso indicado existe y si tenemos permisos.

```
echo "$$" | tee evidencia_shell_pid.txt
ps -p "$$" -o pid,ppid,uid,user,comm,etime | tee evidencia_ps_shell.txt
kill -0 "$$" && echo "Shell vivo (PID $$)" | tee -a evidencia_signal_check.txt
```

-   Se crea un nuevo subshell que estará inactivo por 999 segundos y de fondo. Además, con la expresión _$!_ se captura su PID al ser el más reciente iniciado y se guarda en evidencia. Igual que en la sección anterior, se imprime la información de este proceso.

```
bash -c 'sleep 999' &  # proceso hijo controlado
ECHO_BG_PID=$!
echo "$ECHO_BG_PID" | tee evidencia_pid_bg.txt
ps -p "$ECHO_BG_PID" -o pid,ppid,comm,etime | tee evidencia_ps_bg_antes.txt
```

-   Se utiliza _SIGTERM_ para terminar el proceso con lo que se llama _graceful termination_ para permitir al proceso terminar sus operaciones actuales y liberar recursos antes de terminar. Además, se procede a imprimir y guardar la comprobación de la desaparción del proceso en la lista.

```
kill -SIGTERM "$ECHO_BG_PID"
sleep 0.3
ps -p "$ECHO_BG_PID" -o pid,ppid,comm,etime | tee evidencia_ps_bg_despues.txt || echo "Terminado OK" | tee -a evidencia_ps_bg_despues.txt
```

#### 3. Verificación de estados de servicio

-   Se verifica que contamos con el comando _systemctl_ disponible.

```
if command -v systemctl >/dev/null 2>&1; then
  echo "systemctl OK" | tee evidencia_systemd_detect.txt
else
  echo "systemctl NO disponible" | tee evidencia_systemd_detect.txt
fi
```

-   Con su existencia verificada, usamos _systemctl status_ para revisar si _systemd-logind_, el servicio del sistema que gestiona inicios de sesiones de usuarios, está activo, así como información importante como su PID. Además, con _journalctl_, mostramos los logs de este servicio con algunos filtros como los últimos 10, o los generados en el mismo día.

```
systemctl status systemd-logind --no-pager | tee evidencia_status_logind.txt
journalctl -u systemd-logind -n 10 --no-pager | tee evidencia_journal_logind_ultimos10.txt
journalctl -u systemd-logind --since "today" --no-pager | head -n 50 | tee evidencia_journal_logind_hoy_head50.txt
```

### Sección 3: Utilidades de texto de Unix

-   Se usó _grep_ para buscar _root_ dentro de _/etc/passwd_ y se verifica que su ID es 0.

```
grep root /etc/passwd | tee evidencias_grep_root_passwd.txt
```

-   Para el uso de _sed_ en la búsqueda y reemplazo de cadenas en archivos, primero generamos un archivo _datos.txt_. Luego, reemplazamos "datos1" por "secreto" y lo ubicamos en el archivo _nuevo.txt_. Se puede verifica con el comand _diff_ las diferencias en ambos archivos.

```
echo "datos0 datos1 datos2 datos3 > datos.txt
sed 's/datos1/secreto/' datos.txt > nuevo.txt
diff -u datos.txt nuevo.txt | tee evidencia_diff_datos_nuevo.txt
```

-   El comando _awk_ fue usado para imprimir de manera formateada, y por campos, la lista de usuarios presentes en _/etc/passwd_, de manera ordenada y única. En ambas líneas, se uso solo el primer campo correspondiente al nombre de usuario. Además, en la segunda variante se asegura un orden byte a byte puro (a diferencia de solo caracteres).

```
awk -F: '{print $1}' /etc/passwd | sort | uniq | tee evidencia_usuarios_por_awk_sort_uniq.txt
awk -F: '{print $1}' /etc/passwd | LC_ALL=C sort -u | tee evidencia_usuarios_por_awk_sortu.txt
```

-   Con _tr_ se hace una conversión de caracteres de una expresión a otra. En este caso, se convierte la cadena input de minúsculas a mayúsculas.

```
printf "hola\nunix toolkit\n" | tr 'a-z' 'A-Z' | tee evidencia_mayus.txt
```

-   Se buscó en el directorio _/tmp_ por archivos con menos de 5 días de antigüedad de manera ordenada con el comando _find_. Además se imprimió y guardó el conteo de estos archivos.

```
find /tmp -mtime -5 -type f 2>/dev/null | LC_ALL=C sort | tee evidencia_tmp_mod_5d.txt
wc -l evidencia_tmp_mod_5d.txt | tee evidencia_tmp_mod_5d_conteo.txt
```

-   Por último, con _grep_ obtenemos todas las lineas que contengan "error" o "fail" y las almacenamos en "hallazgos.txt".

```
grep -Ei 'error|fail' evidencias/sesion.txt | tee evidencias/hallazgos.txt
```
