Title: Abrir archivos .tec en GNU/Linux
Date: 2012-06-23 13:41
Author: Nacho Cano
Tags: android, copia de seguridad, dd, ghex, hexer, ice cream sandwich, ics, imágenes en miniatura, jfif, modo infierno, privacidad, tec, thumbnails
Slug: abrir-archivos-tec-en-gnulinux

Haciendo una copia de seguridad de los datos de un móvil con Android
ICS, he visto que existe un directorio llamado `cache` en el mismo
directorio donde se guardan las fotos, `/sdcard/DCIM/Camera`, que
contiene archivos cuya extensión es `.tec`.

Echando un vistazo al contenido de estos archivos con `hexer`, parece
ser que se trata de un archivo JFIF:

```bash
 00000000:  ff d9 66 b3 00 00 ff d8  ff e0 00 10 4a 46 49 46  ..f.........JFIF
 00000010:  00 01 01 00 00 01 00 01  00 00 ff db 00 43 00 05  .............C..
 00000020:  03 04 04 04 03 05 04 04  04 05 05 05 06 07 0c 08  ................
```

Por el nombre del directorio y por el tamaño de las fotos, menos de
100K, parece que [deben ser imágenes en miniatura][].

Aunque no he encontrado ninguna aplicación que las pueda abrir
directamente, he encontrado un [vídeo donde se explica cómo abrirlas][].
La técnica consiste en eliminar los 6 primeros _bytes_ y el último.
Podemos confirmar que funciona con `GHex`, un editor hexadecimal para
Gnome. He intentado eliminar los _bytes_ con `hexer` pero no hay manera,
siempre se me pone en "modo infierno" y no termina de salir bien.

Si queremos recuperar todas esas imágenes en miniatura, hacer el cambio
archivo a archivo es algo impensable, sobre todo si tenemos un gran
número de ellas. Utilizando `dd` podemos conseguir [eliminar los 6
primeros _bytes_][eliminar los 6 primeros bytes] de todas las imágenes:

```bash
$ for f in *.tec; do
     dd bs=6 skip=1 if=$f of=$f.jfif
  done
```

Aunque en este caso no eliminamos el último _byte_, los archivos creados
se pueden abrir sin problemas.

Como comentario final, si queremos borrar las fotos del móvil,
deberíamos borrar también las imágenes en miniatura que están en el
directorio `/sdcard/DCIM/Camera/cache`, o directamente el propio
directorio.

Referencias
-----------

- [Recover deleted photos from an Android device][vídeo donde se explica
cómo abrirlas]
- [Best way to remove bytes from the start of a file?][eliminar los 6
primeros bytes]
- [JPEG File Interchange Format (JFIF)][]

  [deben ser imágenes en miniatura]: http://androidforums.com/samsung-galaxy-s2-international/427146-dcim-camera-cache.html
    "deben ser imágenes en miniatura"
  [vídeo donde se explica cómo abrirlas]: http://www.arab-androidian.com/2012/04/how-to-recover-deleted-photos-from-an-android-device-tutorial/
    "vídeo donde se explica cómo abrirlas"
  [eliminar los 6 primeros bytes]: http://unix.stackexchange.com/questions/6852/best-way-to-remove-bytes-from-the-start-of-a-file/6865#6865
    "eliminar los 6 primeros _bytes_"
  [JPEG File Interchange Format (JFIF)]: http://www.ecma-international.org/publications/techreports/E-TR-098.htm
    "JPEG File Interchange Format (JFIF)"
