Title: Solucionado el error «prelink: ... is not an ELF file»
Date: 2013-03-21 21:15
Author: Nacho Cano
Tags: 12.04, error, md5sum, parche, prelink, quantal, quetzal, tiger, tigercron, ubuntu
Slug: solucionado-el-error-prelink-is-not-an-elf-file

`tiger` es una herramienta que comprueba la integridad de ciertos
ficheros del sistema.

En Ubuntu 12.04.2, la versión instalada es la 3.2.3, y si además estamos
usando `prelink`, puede que `tigercron` arroje errores del estilo:

```bash
prelink: "/usr/share/vim/vim73/doc/help.txt" is not an ELF file
```

El problema parece estar en un uso incorrecto de `prelink`, ya que no
maneja bien la salida de `md5sum`. Este error creo que todavía no está
solucionado, pero en [este hilo][] se incluye un parche que parece que
funciona.

Descargamos el parche y lo aplicamos, guardando una copia del fichero
modificado:

```bash
$ wget -O tiger.patch "http://bugs.debian.org/cgi-bin/bugreport.cgi?msg=5;filename=tiger.patch;att=1;bug=505906"
$ sudo patch -b /usr/lib/tiger/systems/Linux/2/deb_checkmd5sums < tiger.patch
patching file /usr/lib/tiger/systems/Linux/2/deb_checkmd5sums
```

Una vez actualizado, recibiremos un aviso del propio `tiger` diciendo
que el fichero ha sido modificado:

```bash
NEW: --FAIL-- [lin005f] Installed file `/usr/lib/tiger/systems/Linux/2/deb_checkmd5sums' checksum differs from installed package 'tiger'.
```

  [este hilo]: http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=505906
    "este hilo"
