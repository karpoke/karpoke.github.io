Title: Recuperando los vídeos Flash borrados por el plugin de Adobe
Date: 2011-03-04 18:58
Author: Nacho Cano
Tags: adobe, chromium, copiar vídeos de youtube, cut, find, firefox, flashplayer, readlink, recuperación de información
Slug: recuperando-los-videos-flash-borrados-por-el-plugin-de-adobe

La nueva versión del plugin de Adobe borra los archivos termporales de
vídeo justo después de abrirlos para evitar que tengamos la tentación de
copiar el vídeo simplemente copiando el archivo `/tmp/FlashXXXX`.
`hons`, un [usuario de commandlinefu.com][] ha publicado un comando que
crea un enlace simbólico al controlador del archivo con el nombre del
archivo borrado:

```bash
$ for h in $(find /proc/_/fd -ilname "/tmp/Flash_" 2>/dev/null); do
>    ln -s "$h" $(readlink "$h" | cut -d' ' -f1);
> done
```

![Youtbe targeted]({static}/images/youtube-targeted-298x300.jpg)

Vamos a probarlo con un vídeo cualquiera, por ejemplo este: [IT Crowd -
Fire][].

Con `find` podemos encontrar estos archivos borrados:

```bash
$ find /proc/_/fd -ilname "/tmp/Flash_" 2>/dev/null
/proc/21204/fd/36
```

y con `readlink` podemos saber el nombre que tenían.

```bash
$ readlink /proc/21204/fd/36
/tmp/FlashXX3Jmbxp (deleted)
```

Tras ejecutar el comando, tendremos un enlace como el siguiente:

```bash
$ ls -nl /tmp/Flash*
lrwxrwxrwx 1 1000 1000 17 2011-03-04 17:42 FlashXX3Jmbxp -> /proc/21204/fd/36
```

Para copiarlo basta hacer:

```bash
$ cp /tmp/FlashXX3Jmbxp ~/it-crowd-fire.flv
```

* * * * *

#### Actualizado el 22 de marzo de 2012

Actualmente, parece que esto ya no funciona. Los vídeos ya no se guardan
en en el directorio `/tmp`. Sin embargo, es posible que podamos
encontrar el vídeo en la caché del navegador.

En Firefox, la caché se encuentra en
`~/.mozilla/firefox/userprofile/Cache`, donde `userprofile` es algo como
`lwx2hgoq.default`.

Para encontrar los archivos que sean vídeos Flash, podemos ejecutar algo
como esto para encontrarlos:

```bash
$ find . -type f -exec file {} \; | grep -i flash | grep -iv compressed | awk -F: '{print $1}'
./2/2F/929B0d01
./E/B3/307B6d01
./C/B5/E5137d01
./3/86/C1069d01
./D/7B/DFE3Dd01
./F/42/414E2d01
```

Excluyo los archivos _compressed_ porque no he podido abrirlos con
ningún programa. Al intentarlo, devolvía un error de
`Compressed SWF format not supported`.

En Chromium la caché se guarda en `~/.cache/chromium/Cache`.

* * * * *

  [usuario de commandlinefu.com]: http://www.commandlinefu.com/commands/view/7991/recover-tmp-flash-videos-deleted-immediately-by-the-browser-plugin
    "usuario de commandlinefu.com"
  [IT Crowd - Fire]: https://www.youtube.com/watch?v=1EBfxjSFAxQ
    "IT Crowd - Fire"
