Title: CDE, creando aplicaciones portables en GNU/Linux
Date: 2012-06-11 00:47
Author: Nacho Cano
Tags: cde, portable
Slug: cde-creando-aplicaciones-portables-en-gnulinux

[CDE][] es un programa desarrollado por Philip Guo que permite crear
versiones portables de aplicaciones GNU/Linux, automatizando el proceso
de empaquetado de código, datos y dependencias requeridos para
ejecutarlas en otros equipos, sin que su uso requiera instalación ni
configuración.

Instalación
-----------

Si queremos instalar la última versión en desarrollo:

```bash
$ git clone git://github.com/pgbovine/CDE.git
$ cd CDE
$ make
```

Una vez que termine de compilar, tendremos el programa ejecutable,
`cde`.

Creando aplicaciones portables
------------------------------

Si queremos crear un versión portable, sólo tenemos que llamar al
ejecutable que hemos creado pasándole como parámetro el nombre del
programa. Por ejemplo, para crear una versión portable de `gimp`:

```bash
$ ~/CDE/cde gimp
```

Esto creará el directorio `cde-package`, que será el que podamos copiar
a otro equipo, y que contiene la versión portable de `gimp`: `gimp.cde`.

Podemos crear un repositorio con las aplicaciones que prefiramos,
simplemente ejecutando `cde` desde el mismo directorio.

```bash
$ mkdir portable
$ cd portable
$ ~/CDE/cde gimp
$ ~/CDE/cde lowriter
$ ~/CDE/cde firefox
```

Referencias
-----------

» [pgbovine.net][CDE]
- Via [linuxzone.es][]

  [CDE]: http://www.pgbovine.net/cde.html
    "CDE"
  [linuxzone.es]: http://www.linuxzone.es/2012/06/04/creando-aplicaciones-portables-en-gnulinux/
    "linuxzone.es"
