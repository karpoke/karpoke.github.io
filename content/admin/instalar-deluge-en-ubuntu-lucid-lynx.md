Title: Instalar deluge en Ubuntu Lucid Lynx
Date: 2012-02-09 02:31
Author: Nacho Cano
Tags: 10.04, bittorrent, daemon, deluge, p2p, script, torrent, ubuntu lucid lyns, ufw, web
Slug: instalar-deluge-en-ubuntu-lucid-lynx

`deluge` es un cliente de BitTorrent en el que la interfaz está separada
del núcleo, que corre como un servicio, lo que posibilita usarlo de
forma remota a través de una interfaz web.


Instalación
-----------

Podemos instalar `deluge` y su interfaz web desde los repositorios:

    $ sudo aptitude install deluged deluge-webui

Crearemos el usuario "deluge" para ejecutar este servicio:

    $ sudo adduser --disabled-password --system --home /var/lib/deluge --gecos "SamRo Deluge server" --group deluge

Creamos el _script_ `/etc/default/deluge-daemon`:

    # Configuration for /etc/init.d/deluge-daemon
    # The init.d script will only run if this variable non-empty.
    DELUGED_USER="deluge"
    # Should we run at startup?
    RUN_AT_STARTUP="YES"

Copiamos el _script_ [`deluge-daemon`][deluge-daemon]
a `/etc/init.d` y nos aseguramos de que tenga permisos de ejecución.

Configuramos el _script_ para ejecutarse al inicio:

    $ sudo update-rc.d deluge-daemon defaults

Lo ejecutamos, para no tener que esperar al próximo reinicio:

    $ sudo invoke-rc.d deluge-daemon start

Ya podemos acceder a la interfaz web: http://localhost:8112. La
contraseña por defecto es "deluge". Nada más iniciar sesión deberíamos
cambiarla. También tendremos la opción de usar SSL.

### El cortafuegos

Si hemos instalado `deluge` en otro equipo de la red y [tiene activado
un cortafuegos][] deberemos permitir el acceso para poder acceder a la
interfaz web. Por ejemplo, si usamos `ufw` y queremos que pueda acceder
cualquier equipo dentro de la misma red deberíamos añadir la regla:

    $ sudo ufw allow proto tcp from 192.168.1.0/24 to any port 8112

_Logging_
---------

Si queremos que se recojan mensajes de _log_, deberemos crear los
siguientes directorios para el usuario `deluge`:

    $ sudo mkdir -p /var/log/deluge/daemon
    $ sudo mkdir -p /var/log/deluge/web
    $ sudo chmod -R 755 /var/log/deluge
    $ sudo chown -R deluge /var/log/deluge

Modificamos las opciones del _script_ `/etc/init.d/deluge-daemon` para
que contenga las líneas:

    DAEMON1_ARGS="-d -L warning -l /var/log/deluge/daemon/warning.log"             # Consult `man deluged` for more options
    DAEMON2_ARGS="-L warning -l /var/log/deluge/web/warning.log"

Y reiniciamos el servicio:

    $ sudo invoke-rc.d deluge-daemon restart

Para rotar los ficheros de _log_:

    sudo cat > /etc/logrotate.d/deluge << EOF
    /var/log/deluge/_/_.log {
            weekly
            missingok
            rotate 7
            compress
            notifempty
            copytruncate
            create 600
    }
    EOF

Referencias
-----------

» [How to install Deluge (v1.2.x/v1.3.x) headless on Ubuntu Server][]
» [Ubuntu Init Script][]
» [Bandwith Tweaking][]
» [Deluge FAQ][]

  [deluge-daemon]: http://terminus.ignaciocano.com/wp-uploads/linked/deluge-daemon
    "deluge-daemon"
  [tiene activado un cortafuegos]: {filename}/admin/detectando-intrusos-en-ubuntu-maverick-meerkat.md
    "tiene activado un cortafuegos"
    "cortafuegos"
  [How to install Deluge (v1.2.x/v1.3.x) headless on Ubuntu Server]: http://www.havetheknowhow.com/Install-the-software/Install-Deluge-Headless.html
    "How to install Deluge (v1.2.x/v1.3.x) headless on Ubuntu Server"
  [Ubuntu Init Script]: http://dev.deluge-torrent.org/wiki/UserGuide/InitScript/Ubuntu
    "Ubuntu Init Script"
  [Bandwith Tweaking]: http://dev.deluge-torrent.org/wiki/UserGuide/BandwidthTweaking
    "Bandwith Tweaking"
  [Deluge FAQ]: http://dev.deluge-torrent.org/wiki/Faq#Howtostartthevarioususer-interfaces
    "Deluge FAQ"
