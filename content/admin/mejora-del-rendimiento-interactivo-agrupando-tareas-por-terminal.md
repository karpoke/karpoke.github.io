Title: Mejora del rendimiento interactivo agrupando tareas por terminal
Date: 2010-12-16 02:03
Author: Nacho Cano
Tags: kernel, parche, rendimiento
Slug: mejora-del-rendimiento-interactivo-agrupando-tareas-por-terminal

El [parche de 200 líneas][] para el kernel, o su versión en [espacio de
usuario][], [mejora el rendimiento interactivo][] agrupando los procesos
por `tty`. La mejora sólo será notable si tenemos varios procesos
asociados a un terminal que tengan un consumo importante de CPU, ya que
la potencia de ésta no se repartirá entre el número de procesos sino
entre el número de grupos de procesos. De ahí que sea una mejora
_interactiva_, el ordenador no irá más rápido, pero sí tendremos la
sensación de que responde más rápido. Este parche requiere un kernel
superior al 2.6.36 con soporte a grupos de tareas.

Para saber los procesos que están asociados a una terminal podemos
ejecutar:

```bash
$ ps -e | grep -v ?
```

(Los procesos que tienen un interrogante no están asociados a ninguna
terminal.)

Para aplicar el parche, en Ubuntu:

-   editamos el archivo `/etc/rc.local` y añadimos, antes del `exit 0`:

    ```bash
$ mkdir -p /dev/cgroup/cpu
$ mount -t cgroup cgroup /dev/cgroup/cpu -o cpu
$ mkdir -m 0777 /dev/cgroup/cpu/user
$ echo "/usr/local/sbin/cgroup_clean" > /dev/cgroup/cpu/release_agent
    ```

-   lo hacemos ejecutable, por si acaso no lo estuviera ya:

    ```bash
$ sudo chmod +x /etc/rc.local
    ```

-   editamos nuestro `~/.bashrc` y añadimos:

    ```bash
     if [ "$PS1" ]; then
       mkdir -p -m 0700 /dev/cgroup/cpu/user/$$
       echo $$ > /dev/cgroup/cpu/user/$$/tasks
       echo "1" > /dev/cgroup/cpu/user/$$/notify_on_release
    fi
    ```

-   creamos el archivo `/usr/local/sbin/cgroup_clean` y añadimos:

    ```bash
     #!/bin/sh
    if [ "$*" != "/user" ]; then
       rmdir /dev/cgroup/cpu/$*
    fi
    ```

-   le damos permisos de ejecución:

    ```bash
$ sudo chmod +x /usr/local/sbin/cgroup_clean
    ```

-   y, por último, ejecutamos el _script_:

    ```bash
$ sudo /etc/rc.local
    ```

-   o reiciniamos:

    ```bash
$ sudo reboot
    ```

  [parche de 200 líneas]: http://lkml.org/lkml/2010/10/19/123
    "parche de 200 líneas"
  [espacio de usuario]: http://usemoslinux.blogspot.com/2010/11/foto-resumen-tras-haber-realizado-el.html
    "espacio de usuario"
  [mejora el rendimiento interactivo]: http://ubuntulife.wordpress.com/2010/11/20/el-parche-milagro-de-linux-de-200-lineas-implementado-en-4-lineas-de-bash/#comment-43848
    "mejora el rendimiento interactivo"
