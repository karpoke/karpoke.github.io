Title: Limitando el número de procesos por usuario
Date: 2011-08-01 19:23
Author: Nacho Cano
Tags: bash, bomba fork, c, limits.conf, perl, python, ubuntu, ulimit
Slug: limitando-el-numero-de-procesos-por-usuario

Mediante el comando `ulimit` podemos consultar y controlar el valor de los
recursos disponibles para la consola y los [procesos que puedan ser iniciados
desde ella][].

Las diferentes opciones que acepta este comando son:

```bash
-a     All current limits are reported
-b     The maximum socket buffer size
-c     The maximum size of core files created
-d     The maximum size of a process’s data segment
-e     The maximum scheduling priority ("nice")
-f     The maximum size of files written by the shell and its children
-i     The maximum number of pending signals
-l     The maximum size that may be locked into memory
-m     The maximum resident set size (many systems do not honor this limit)
-n     The maximum number of open file descriptors (most systems do not allow this value to be set)
-p     The pipe size in 512-byte blocks (this may not be set)
-q     The maximum number of bytes in POSIX message queues
-r     The maximum real-time scheduling priority
-s     The maximum stack size
-t     The maximum amount of cpu time in seconds
-u     The maximum number of processes available to a single user
-v     The maximum amount of virtual memory available to the shell and, on some systems, to its children
-x     The maximum number of file locks
-T     The maximum number of threads
```

Para consultar todos los valores asignados actualmente:

```bash
$ ulimit -a
core file size          (blocks, -c) 0
data seg size           (kbytes, -d) unlimited
scheduling priority             (-e) 20
file size               (blocks, -f) unlimited
pending signals                 (-i) 16382
max locked memory       (kbytes, -l) 64
max memory size         (kbytes, -m) unlimited
open files                      (-n) 1024
pipe size            (512 bytes, -p) 8
POSIX message queues     (bytes, -q) 819200
real-time priority              (-r) 0
stack size              (kbytes, -s) 8192
cpu time               (seconds, -t) unlimited
max user processes              (-u) unlimited
virtual memory          (kbytes, -v) unlimited
file locks                      (-x) unlimited
```

Denegación de servicio
----------------------

Uno de los problemas que podemos encontrar es que el número máximo de procesos
no está limitado, por defecto, en algunas distribuciones, entre ellas Ubuntu.
Esto hace el equipo vulnerable a un ataque de denegación de servicio (DoS),
como por ejemplo una [bomba fork_][bombafork], y a aplicaciones que no están
bien programadas o no funcionan correctamente.

La vulnerabilidad consiste en que un proceso comienza a crear una gran cantidad
de procesos, que consumen tiempo de proceso y memoria, y que saturan la lista
de procesos a ejecutar mantenida por el sistema operativo, impidiendo que se
ejecuten nuevos programas hasta que no se cierre alguno, provocando que la
máquina deje de responder. Un solo [usuario][] podría dejar el sistema sin
respuesta.

![Fork bomb]({static}/images/fork-bomb.png)

<small>_Fuente: [Wikipedia][bomba fork]_</small>

En sencillo obtener un programa de este tipo. Algunos ejemplos típicos de
bombas _fork_, en Bash:

```bash
$ :(){ :|:& };: # ":" es el nombre de la función
```

En Python:

```python

import os
while True:
     os.fork()
```

En Perl:

```perl
fork while fork
```

En C:

```c
#include
int main()
{
  while(1)
    fork();
}
```

Prevención
----------

Dado que una vez iniciada la bomba _fork_ es prácticamente imposible crear
procesos nuevos y para eliminar los procesos creados por la propia bomba _fork_
se necesita a su vez otra proceso que lo haga, la única solución pasa por el
reinicio de la máquina.

Sin embargo, podemos prevenir que un ataque de este tipo se apodere de los
recursos de la máquina, [limitando el número máximo de procesos que se puedan
ejecutar por usuario][].

Podemos especificar un limite para la sesión acutal:

```bash
$ ulimit -u 240
```

Si ahora lanzamos la bomba _fork_:

```bash
$ :(){ :|:& };:
bash: fork: Recurso no disponible temporalmente
...
```

Podremos eliminar el proceso pulsando `Ctrl+C`.

Para que los cambios tengan efecto permanente, editamos el fichero
`/etc/security/limits.conf` y añadimos la siguiente línea:

    username          hard    nproc           240

En el próximo reinicio, o si cerramos todas las sesiones y volvemos a entrar,
los cambios tendrán efecto.

  [procesos que puedan ser iniciados desde ella]: {filename}/admin/mejora-del-rendimiento-interactivo-agrupando-tareas-por-terminal.md
    "mejora del rendimiento interactivo agrupando tareas por terminal"
  [bomba fork]: http://secure.wikimedia.org/wikipedia/es/wiki/Bomba_fork
    "bomba fork"
  [usuario]: {filename}/admin/controlando-la-actividad-de-los-usuarios-conectados.md
    "controlando la actividad de los usuarios conectados"
  [limitando el número máximo de procesos que se puedan ejecutar por usuario]: http://stolowski.blogspot.com/2011/04/protect-your-linux-box-against-fork.html
    "limitando el número máximo de procesos que se puedan ejecutar por usuario"
