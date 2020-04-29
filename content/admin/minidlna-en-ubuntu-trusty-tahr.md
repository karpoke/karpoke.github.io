Title: MiniDLNA en Ubuntu Trusty Tahr
Date: 2014-11-11 15:23
Author: Nacho Cano
Tags: 14.04, android, checkinstall, código fuente, dlna, init, mediahouse, minidlna, ubuntu trusty tahr, ufw
Slug: minidlna-en-ubuntu-trusty-tahr
Related: instalar-deluge-en-ubuntu-lucid-lynx,owncloud-con-mysql-en-ubuntu-lucid-lynx-10-04

DLNA define las especificaciones para compartir contenido multimedia
entre diferentes dispositivos mediante el uso de protocolos UPnP.
Instalaremos un servidor DLNA en Ubuntu Trusty Tahr, MiniDLNA (ahora se
llama ReadyMedia), que nos permitirá, por ejemplo, ver películas,
escuchar música o ver fotos en el portátil, el móvil o la televisión.
Actualmente, no se encuentra en los repositorios, así que lo
instalaremos a partir del código fuente. (Otra alternativa sería usar
algún repositorio PPA que ya contenga el paquete compilado.)


Compilación
-----------

Antes de compilarlo, nos aseguramos de que tenemos las herramientas
necesarias instaladas:

    $ sudo aptitude install autoconf g++ subversion linux-source linux-headers-`uname -r` build-essential tofrodos git-core subversion dos2unix make gcc automake cmake checkinstall git-core dpkg-dev fakeroot pbuilder dh-make debhelper devscripts patchutils quilt git-buildpackage pristine-tar git yasm checkinstall cvs mercurial

También nos aseguraremos de que tenemos las dependencias instaladas:

    $ sudo aptitude install libexif12 libexif-dev libjpeg8-dev libjpeg-dev libjpeg-turbo8 libjpeg-turbo8-dev libid3tag0 libid3tag0-dev libflac8 libflac-dev libvorbis0a libvorbisenc2 libvorbisfile3 libvorbis-dev libsqlite3-0 libsqlite3-dev libavformat54 libavformat-dev

Descargamos el código fuente y lo compilamos:

    $ git clone git://git.code.sf.net/p/minidlna/git minidlna-git
    $ cd minidlna-git
    $ ./autogen.sh
    $ ./configure
    $ make

Ahora podemos, o bien instalarlo directamente:

    $ sudo make install

o bien [crear un paquete `.deb` con `checkinstall`][crear un paquete .deb con checkinstall]:

    $ sudo checkinstall

Configuración
-------------

Creamos el directorio donde guardaremos la configuración:

    $ mkdir ~/.minidlna

Partiremos del fichero de configuración que viene en el código:

    $ cp minidlna.conf ~/.minidlna/minidlna.conf

En el fichero de configuración, deberemos especificar con qué usuario se
debe ejecutar el servicio, qué directorio contiene los archivos
multimedia y dónde deberá guardar la base de datos que utiliza:

    user=user
    media_dir=/media/share
    db_dir=/home/user/.minidlna

Ejecución
---------

Para lanzar el servicio:

    $ /usr/local/sbin/minidlnad -f ~/.minidlna/minidlna.conf

Si vemos que necesitamos que reindexe los contenidos:

    $ /usr/local/sbin/minidlnad -R -f ~/.minidlna/minidlna.conf

Cortafuegos
-----------

Deberemos asegurarnos de que el puerto que hayamos configurado, por
defecto el 8200, sea accesible. También [el puerto UDP 1900][]. Por
ejemplo, si queremos permitir únicamente el acceso dentro de la propia
LAN y usamos `ufw`:

    $ sudo ufw allow proto tcp from 192.168.50.0/24 to any port 8200
    $ sudo ufw allow proto udp from 192.168.50.0/24 to any port 1900

Clientes
--------

En cualquier PC de escritorio, mediante VLC podemos reproducir el
contenido servido a través de MiniDLNA. Basta que vayamos al menú *Red
local > Universal Plug'n'Play*. De hecho, si tenemos los archivos de
subtítulos en el servidor, también es capaz de incluirlos
automáticamente.

En Android, la aplicación [Media House][] nos permitirá reproducir el
contenido.

Ejecución al inicio
-------------------

Si queremos que el servicio arranque al inicio, podemos utilizar el
siguiente _script_:

    #!/bin/sh
    # Mini DLNA
    ### BEGIN INIT INFO
    # Provides:          scriptname
    # Required-Start:    $remote_fs $syslog
    # Required-Stop:     $remote_fs $syslog
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: Start daemon at boot time
    # Description:       Enable service provided by daemon.
    ### END INIT INFO

    case "$1" in
    'start')
            /usr/local/sbin/minidlnad -f /home/user/.minidlna/minidlna.conf
        echo Started
            ;;
    'stop')
        PID=`/bin/pidof minidlnad`
        if [ ${PID} ]; then sudo kill -SIGTERM ${PID}
        else echo Already Stopped
        fi
            ;;
    'restart')
        PID=`/bin/pidof minidlnad`
        if [ ${PID} ]; then sudo kill -SIGTERM ${PID}
        fi
        /usr/local/sbin/minidlnad -f /home/user/.minidlna/minidlna.conf
        echo Restarted
        ;;
    'status')
        PID=`/bin/pidof minidlnad`
        if [ ${PID} ]; then echo Running. Process ${PID}
        else echo Stopped
        fi
        ;;
    'rescan')
        PID=`/bin/pidof minidlnad`
        if [ ${PID} ]; then sudo kill -SIGTERM ${PID}
        fi
        /usr/local/sbin/minidlnad -R -f /home/user/.minidlna/minidlna.conf
        echo Rescanning
        ;;
    *)
            echo "Usage: $0 { start | stop | restart | status | rescan }"
            ;;
    esac
    exit 0

Lo guardamos en `/etc/init.d/minidlna` y configuramos el arranque:

    $ sudo chmod +x /etc/init.d/minidlna
    $ sudo update-rc.d minidlna defaults
     Adding system startup for /etc/init.d/minidlna ...
       /etc/rc0.d/K20minidlna -> ../init.d/minidlna
       /etc/rc1.d/K20minidlna -> ../init.d/minidlna
       /etc/rc6.d/K20minidlna -> ../init.d/minidlna
       /etc/rc2.d/S20minidlna -> ../init.d/minidlna
       /etc/rc3.d/S20minidlna -> ../init.d/minidlna
       /etc/rc4.d/S20minidlna -> ../init.d/minidlna
       /etc/rc5.d/S20minidlna -> ../init.d/minidlna

Actualizaciones
---------------

Cuando haya actualizaciones del código, podemos repetir el proceso de
compilación:

    $ cd minidlna-git
    $ make distclean
    $ git pull
    $ ./configure
    $ make
    $ sudo checkinstall

Desinstalación
--------------

Si queremos desinstalarlo, no tenemos más que:

    $ sudo aptitude purge minidlna
    $ sudo update-rc.d -f minidlna remove
    $ sudo rm /etc/init.d/minidlna
    $ sudo rm -r /home/user/.minidlna

Referencias
-----------

- Anand Subramanian | [The Ultimate Guide to Compile and Install MiniDLNA on Ubuntu][]
- Justin Maggard | [MiniDLNA (ReadyMedia)][]

  [crear un paquete .deb con checkinstall]: {filename}/admin/crear-paquetes-deb-con-checkinstall.md
    "Crear paquetes .deb con checkinstall"
  [el puerto UDP 1900]: http://en.wikipedia.org/wiki/Simple_Service_Discovery_Protocol
    "el puerto UDP 1900"
  [Media House]: https://play.google.com/store/apps/details?id=com.dbapp.android.mediahouse&hl=en
    "Media House"
  [The Ultimate Guide to Compile and Install MiniDLNA on Ubuntu]: http://www.htpcbeginner.com/install-minidlna-on-ubuntu-ultimate-guide/
    "The Ultimate Guide to Compile and Install MiniDLNA on Ubuntu"
  [MiniDLNA (ReadyMedia)]: http://sourceforge.net/projects/minidlna/
    "MiniDLNA (ReadyMedia)"
