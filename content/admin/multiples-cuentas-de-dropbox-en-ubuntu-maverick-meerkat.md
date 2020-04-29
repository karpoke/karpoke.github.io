Title: Múltiples cuentas de Dropbox en Ubuntu Maverick Meerkat
Date: 2011-03-30 14:54
Author: Nacho Cano
Tags: 10.10, dropbox, nautilus-dropbox, script, ubuntu maverick meerkat, ubuntu one
Slug: multiples-cuentas-de-dropbox-en-ubuntu-maverick-meerkat
Related: como-publicar-directorios-en-ubuntu-one-y-dropbox,aplicaciones-en-el-area-de-notificacion-de-ubuntu-natty-narwhal

Una cuenta gratuita de Dropbox permite inicialmente 2 GB de espacio, que
se pueden ir ampliando con algunas sencillas acciones tales como
compartir un directorio, instalar el paquete para Ubuntu o
recomendárselo a un amigo. En principio, sólo se puede tener una cuenta
por dispositivo. Sin embargo, como vamos a ver, gestionar varias cuentas
para obtener más espacio, utilizándolas a la vez y desde la misma
máquina, es algo realmente sencillo y rápido.


Creamos una nueva cuenta
------------------------

Lo mejor es mandarnos una invitación a nosotros mismos y así conseguir
250MB de espacio adicional para cada una. Si nos habíamos registrado con
una cuenta de GMail, podemos poner la misma cuenta de correo,
introduciendo uno o varios puntos en el nombre de usuario, por ejemplo,
`user.name@gmail.com`.

Creamos el directorio para la nueva cuenta:

    $ mkdir ~/.dropbox2

Lanzamos la instalación en este directorio:

    $ HOME=~/.dropbox2 /usr/bin/dropbox start -i

Sin embargo, en Ubuntu Maverick Meerkat da el siguiente error:

    Starting Dropbox...Traceback (most recent call last):
    File "/usr/bin/dropbox", line 259, in handle_ok
    self.dont_show_again_align.hide()
    AttributeError: 'DownloadDialog' object has no attribute 'dont_show_again_align'

Vamos a ver que pasa si comentamos la línea 259 en el fichero
`/usr/bin/dropbox`:

    #self.dont_show_again_align.hide()

* * * * *

#### Actualizado el 4 de febrero de 2012

Este fichero viene con el paquete `nautilus-dropbox`. La versión que tengo
instalada es la 0.6.8, pero actualmente ya van por [la versión 0.7.1][], por lo
que es posible que [el número de línea haya cambiado][].

* * * * *

Lo volvemos a ejecutar, y funciona! Nos aparecerá el asistente y
configuramos la nueva cuenta o creamos una. El directorio de la nueva
cuenta de Dropbox está en `~/.dropbox2/Dropbox`.

Gestionar varias cuentas
------------------------

Ahora, para que sea más sencillo [gestionar todas las cuentas][] y que
se ejecuten al inicio, haremos lo siguiente.

Desactivamos el autoarranque de la cuenta de Dropbox que ya teníamos.

![Dropbox preferences]({static}/images/dropbox-preferences-247x300.png)

Para tenerlo todo un poco más ordenado, vamos a mover las credenciales
de la cuenta que ya teníamos al directorio `~/.dropbox1`:

    $ cd ~
    $ mkdir .dropbox1
    $ mv .dropbox .dropbox-dist Dropbox .dropbox1
    $ ln -s .Xauthority .dropbox
    $ ln -s .Xauthority .dropbox2

Nos debería quedar así:

    $ ls -lan .dropbox1
    total 28
    drwxr-xr-x   5 1000 1000  4096 2011-03-30 14:13 .
    drwxr-xr-x 157 1000 1000 12288 2011-03-30 14:16 ..
    drwxr-xr-x   3 1000 1000  4096 2011-03-30 13:45 .dropbox
    drwxr-xr-x   6 1000 1000  4096 2011-03-30 13:02 Dropbox
    drwxr-xr-x   4 1000 1000  4096 2010-10-28 11:43 .dropbox-dist
    lrwxrwxrwx   1 1000 1000    14 2011-03-30 14:13 .Xauthority -> ../.Xauthority

    $ ls -lan .dropbox2
    total 28
    drwxr-xr-x   5 1000 1000  4096 2011-03-30 14:13 .
    drwxr-xr-x 157 1000 1000 12288 2011-03-30 14:16 ..
    drwxr-xr-x   3 1000 1000  4096 2011-03-30 13:46 .dropbox
    drwxr-xr-x   5 1000 1000  4096 2011-03-30 13:36 Dropbox
    drwxr-xr-x   5 1000 1000  4096 2011-03-30 13:33 .dropbox-dist
    lrwxrwxrwx   1 1000 1000    14 2011-03-30 14:13 .Xauthority -> ../.Xauthority

El siguiente _script_, `MultipleDropboxInstances.sh`, se encarga de
lanzar una instancia de Dropbox por cada cuenta que tengamos instalada:

    #!/bin/bash

    #__***************************__
    # Multiple dropbox instances
    #__***************************__

    dropboxes=".dropbox .dropbox2"

    for dropbox in $dropboxes
    do
        HOME=/home/$USER
        if ! [ -d $HOME/$dropbox ];then
            mkdir $HOME/$dropbox 2> /dev/null
            ln -s $HOME/.Xauthority $HOME/$dropbox/ 2> /dev/null
        fi

        HOME=$HOME/$dropbox /usr/bin/dropbox start -i 2> /dev/null &
    done

Le damos permisos de ejecución:

    $ chmod +x MultipleDropboxInstances.sh

Lo ejecutamos:

    $ ./MultipleDropboxInstances.sh
    Starting Dropbox...Starting Dropbox...Done!
    Done!

En la barra superior nos aparecerán dos iconos de Dropbox, uno por cada
cuenta. Si utilizamos Unity y no nos aparece, podemos recurrir a un
truco para [añadir el icono de Dropbox al área de notificación][].

* * * * *

#### Actualizado el 17 de marzo de 2012

La versión actual de Dropbox, 0.7.1, es compatible con Unity, por lo que no es
necesario recurrir al truco mencionado.

* * * * *

Para que se ejecute cada vez al inicio, en el fichero `/etc/rc.local`,
añadimos:

    su username /home/username/MultipleDropboxInstances.sh

Referencias
------------

- En el directorio público de mi cuenta de Dropbox tengo subidos varios [_ezines_ sobre GNU/Linux, software libre, programación y seguridad][].
- En el directorio público de Ubuntu One tengo subidos varios [libros y artículos sobre GNU/Linux, software libre, programación y seguridad][].

  [la versión 0.7.1]: http://www.dropbox.com/install?os=lnx
    "la versión 0.7.1"
  [el número de línea haya cambiado]: {filename}/admin/multiples-cuentas-de-dropbox-en-ubuntu-maverick-meerkat.md
    "el número de línea haya cambiado"
  [gestionar todas las cuentas]: http://wiki.dropbox.com/TipsAndTricks/MultipleInstancesOnUnix
    "gestionar todas las cuentas"
  [añadir el icono de Dropbox al área de notificación]: {filename}/admin/aplicaciones-en-el-area-de-notificacion-de-ubuntu-natty-narwhal.md
    "Añadir el icono de Dropbox al área de notificación"
  [_ezines_ sobre GNU/Linux, software libre, programación y seguridad]: http://dl.dropbox.com/u/13647978/index.html
    "ezines sobre GNU/Linux, software libre, programación y seguridad"
  [libros y artículos sobre GNU/Linux, software libre, programación y seguridad]: http://ubuntuone.com/p/NoU/
    "libros y artículos sobre GNU/Linux, software libre, programación y seguridad"
