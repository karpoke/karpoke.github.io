Title: Mostrar las aplicaciones ocultas que se ejecutan al inicio
Date: 2012-06-28 12:42
Author: Nacho Cano
Tags: 12.04, aplicaciones ocultas, ubuntu precise pangolin
Slug: mostrar-las-aplicaciones-ocultas-que-se-ejecutan-al-inicio

Las aplicaciones que se ejecutan al inicio tienen un archivo de
configuración en el directorio `/etc/xdg/autostart`. Algunos de estos
archivos de configuración tienen la variable `NoDisplay=true`, por lo
que no aparecen en el listado de Aplicaciones al inicio, y por tanto no
se pueden desactivar a golpe de ratón.

Si queremos que [estas aplicaciones se muestren][] y así poder
desactivarlas mediante la interfaz gráfica, ejecutamos:

```bash
$ sudo sed -i 's/NoDisplay=true/NoDisplay=false/' /etc/xdg/autostart/*
```

Si además queremos que [cada vez que instalamos un programa se ejecute
este comando][], podemos incluirlo en el archivo `/etc/apt.conf`:

```bash
sed -i 's/NoDisplay=true/NoDisplay=false/' /etc/xdg/autostart/*
```

Referencias
-----------

- [Tip: Como ver las aplicaciones que se ejecutan al inicio en
Ubuntu][estas aplicaciones se muestren]

  [estas aplicaciones se muestren]: http://linuxzone.es/2012/06/07/tip-como-ver-las-aplicaciones-que-se-ejecutan-al-inicio-en-ubuntu/
    "estas aplicaciones se muestren"
  [cada vez que instalamos un programa se ejecute este comando]: http://linuxzone.es/2012/06/07/tip-como-ver-las-aplicaciones-que-se-ejecutan-al-inicio-en-ubuntu/#comment-23800
    "cada vez que instalamos un programa se ejecute este comando"
