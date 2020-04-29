Title: Arch en Raspberry Pi
Date: 2012-06-22 20:41
Author: Nacho Cano
Tags: arch, autocompletado, byobu, copia de seguridad, dd, pacman, pbzip2, raspberry pi, sudo, sudoers, tarjeta SD, visudo
Slug: arch-en-raspberry-pi
Related: raspberry-pi,pbzip2-un-bzip2-mas-rapido

Después de haber estado usando la [Raspberry Pi con Debian][], he
querido probar otras distribuciones, en este caso Arch.

Desde la página de [descargas][], nos bajamos el torrent, así no
sobrecargamos el servidor.


Crear una copia de la tarjeta SD
--------------------------------

He estado unos días trasteando con Debian, ya sabéis, modificando la
tabla de particiones para utilizar todo el espacio disponible,
instalando paquetes, configurándola a mi gusto, no mucho, pero si ahora
formateo la tarjeta, es un trabajo perdido. No sólo eso, sino que no
descarto tener que repetirlo de nuevo si posteriormente vuelvo a debian.
Puede que al final me quede con Arch, pero me apetece probar alguna
distribución más, como [Raspbmc][] o [PwnPi][], así que me interesa
guardar una copia de la tarjeta. Quizá sería mejor opción crear una
máquina virtual con `qemu` para probar otras distribuciones, o utilizar
tarjetas SD diferentes, pero dado lo sencillo que es hacer la copia esto
será lo primero que haga.

Para crear una copia de la tarjeta, nos aseguramos de que está
desmontada y ejecutamos:

    $ dd bs=1M if=/dev/mmcblk0 of=my-debian-19-04-2012.img

Comprimiremos la imagen utilizando [pbzip2][]:

    $ pbzip2 my-debian-19-04-2012.img

Sólo para hacer la copia y comprimir la imagen tarda un rato,
[dependiendo de la tarjeta SD][] y del procesador que tengamos. En mi
caso, una tarjeta SD Samsung Class 10 y con un Core 2 Duo todo el
proceso ha tardado algo menos de media hora (un cuarto de hora copiar la
imagen y unos diez minutos comprimirla).

Cuando queramos volcar la imagen a la tarjeta, lo hacemos a la inversa.
Primero, descomprimimos la imagen:

    $ pbzip2 -d my-debian-19-04-2012.img.bz2

Introducimos la tarjeta en el equipo y la desmontamos. En mi caso la
tarjeta es el dispositivo `/dev/mmcblk0`. Lo podemos comprobar
ejecutando:

    $ sudo fdisk -l
    Disco /dev/mmcblk0: 8068 MB, 8068792320 bytes
    4 cabezas, 32 sectores/pista, 123120 cilindros, 15759360 sectores en total
    Unidades = sectores de 1 * 512 = 512 bytes
    Tamaño de sector (lógico / físico): 512 bytes / 512 bytes
    Tamaño E/S (mínimo/óptimo): 512 bytes / 512 bytes
    Identificador del disco: 0x000ee283

       Dispositivo Inicio    Comienzo      Fin      Bloques  Id  Sistema
    /dev/mmcblk0p1            2048      155647       76800    c  W95 FAT32 (LBA)
    /dev/mmcblk0p2          157696    15368063     7605184   83  Linux
    /dev/mmcblk0p3        15368064    15759231      195584   82  Linux swap / Solaris

En la salida del comando, sólo he puesto la parte referente a la tarjeta
SD, por lo que antes de esto nos saldrá la información relativa al disco
duro.

Y, por último, copiamos nuestra imagen a la tarjeta SD, tal como hicimos
la primera vez:

    $ dd bs=1M if=my-debian-19-04-2012.img of=/dev/mmcblk0

Listo, ya la podemos introducir en la Raspberry Pi y encenderla.

Instalando Arch
---------------

Una vez que nos hemos bajado la imagen de Arch y que podemos
sobreescribir el contenido de la tarjeta SD sin remordimientos, vamos a
instalar Arch. Primero, comprobamos que el archivo descargado es
correcto:

    $ sha1sum archlinuxarm-29-04-2012.zip
    b84d1eaba2ec64982da40ccd7dba06b186f69545  archlinuxarm-29-04-2012.zip

Lo descomprimimos:

    $ unzip archlinuxarm-29-04-2012.zip

Comprobamos que la imagen se ha descomprimido correctamente:

    $ cd archlinuxarm-29-04-2012/
    $ cat archlinuxarm-29-04-2012.img.sha1
    19034eb6808a248d30bda99450b03af1a88daf82  archlinuxarm-29-04-2012.img
    $ sha1sum archlinuxarm-29-04-2012.img
    19034eb6808a248d30bda99450b03af1a88daf82  archlinuxarm-29-04-2012.img

Y, ahora ya sí, volcamos la imagen a la tarjeta SD:

    $ dd bs=1M if=archlinuxarm-29-04-2012.img of=/dev/mmcblk0

### Primera actualización

Lo primero será actualizar el sistema. Esta chuleta del [gestor de
paquetes de Arch][], `pacman`, nos vendrá bien si estamos acostumbrados
a `aptitude`:

    [root@alarmpi ~]# pacman -Syu

Esto nos advertirá de que hay una actualización del paquete `pacman` y
que si queremos actualizar éste primero.

    :: The following packages should be upgraded first :
    pacman es
    :: Do you want to cancel the current operation
    :: and upgrade these packages now? [Y/n] n

Por ahora le diremos que no, ya que nos puede [evitar algunos
problemas][]. A continuación realizará la actualización del sistema:

    :: Starting full system upgrade...
    :: Replace libusb with core/libusbx? [Y/n]
    :: Replace procps with core/procps-ng? [Y/n]
    :: Replace udev with core/systemd-tools? [Y/n]
    resolving dependencies...
    looking for inter-conflicts...Lo primero será actualizar el sistema. Esta chuleta del gestor de paquetes de Arch, pacman, nos vendrá bien si estamos acostumbrados a aptitude:

    [root@alarmpi ~]# pacman -Syu

Esto nos advertirá de que hay una actualización del paquete `pacman` y
que si queremos actualizar éste primero.

    :: The following packages should be upgraded first :
    pacman es
    :: Do you want to cancel the current operation
    :: and upgrade these packages now? [Y/n] n

Por ahora le diremos que no, ya que nos puede [evitar algunos
problemas][]. A continuación realizará la actualización del sistema:

    :: Starting full system upgrade...
    :: Replace libusb with core/libusbx? [Y/n]
    :: Replace procps with core/procps-ng? [Y/n]
    :: Replace udev with core/systemd-tools? [Y/n]
    resolving dependencies...
    looking for inter-conflicts...

#### error: failed to commit transaction (conflicting files)

    error: failed to commit transaction (conflicting files)
    filesystem: /var/lock exists in filesystem
    filesystem: /var/run exists in filesystem
    Errors occurred, no packages were upgraded.

Por algún motivo, al [actualizar se encontraron archivos que ya
existían][], y en lugar de sobre escribirlos, nos avisa y aborta la
actualización. Lo que podemos hacer en este caso es comprobar si los
archivos pertenecen a algún paquete mediante:

    [root@alarmpi ~]# pacman -Qo /var/lock
    error: No package owns /var/lock

Si el archivo no pertenece a ningún paquete, lo renombraremos y
volveremos a intentar actualizar. Si todo va bien, podemos borrar el
archivo.

    [root@alarmpi ~]# mv /var/lock{,.bak}

### Usuarios, contraseñas, privilegios

Tras arrancar la Raspberry Pi, lo primero que haremos será cambiar la
contraseña de `root`:

    [root@alarmpi ~]# passwd root

La cuenta de `root` sólo se debería utilizar para tareas de
administración, por lo que crearemos un nuevo usuario para uso
cotidiano:

    [root@alarmpi ~]# useradd -m -g users -G audio,lp,optical,storage,video,wheel,games,power,scanner -s /bin/bash archie

Si queremos [utilizar `sudo`][utilizar sudo], para evitar tener que iniciar sesión
como `root`, primero tenemos que instalarlo:

    [root@alarmpi ~]# pacman -S sudo

Una vez instalado, editaremos el fichero `/etc/sudoers` mediante el
comando `visudo`. ES IMPORTANTE utilizar `visudo` y no otro editor,
porque un error podría dejar la cuenta de `root` inaccesible.

    [root@alarmpi ~]# visudo

Al crear nuestro usuario, lo hemos añadido al grupo `wheels`, que será
el que utilicemos para permitir el uso de `sudo`, por lo que buscamos la
siguete linea y la descomentamos:

    %wheel  ALL=(ALL) ALL

Para añadir [autocompletado a `sudo`][autocompletado a sudo],
editamos el fichero `~/.bashrc`
y añadimos:

    complete -cf sudo

Si la cuenta que hemos creado puede utilizar `sudo`, podemos
deshabilitar la cuenta de `root`, aunque ya nos advierten de que esto
podría causar algún problema. Para deshabilitarla:

    [myusername@alarmpi ~]$ sudo passwd -l root
    passwd: password expiry information changed.

Si queremos volver a habilitarla:

    [myusername@alarmpi ~]$ sudo passwd -u root

### Instalando algunos paquetes

Nada más conectarme por SSH, echo en falta algunos paquetes, aunque es
algo que tiene fácil y rápida solución:

    [myusername@alarmpi ~]$ sudo pacman -S htop vim

`byobu` es como `screen` pero mejor, aunque [no se encuentra en los
repositorios oficiales][], sí está en los de usuario, AUR. Si queremos
instalarlo:

    [myusername@alarmpi ~]$ cd /tmp
    [myusername@alarmpi ~]$ wget http://aur.archlinux.org/packages/by/byobu/byobu.tar.gz
    [myusername@alarmpi ~]$ tar zxf byobu.tar.gz
    [myusername@alarmpi ~]$ cd byobu
    [myusername@alarmpi ~]$ makepkg

Si falta alguna dependencia, nos lo hará saber. En este caso, instalé
las siguientes:

    [myusername@alarmpi ~]$ sudo pacman -S fakeroot tmux libnewt python2 patch make

Una vez satisfechas las dependencias, creamos el paquete y lo
instalamos:

    [myusername@alarmpi ~]$ makepkg
    [myusername@alarmpi ~]$ sudo pacman -U *.xz

Si queremos tener la hora del sistema actualizada de forma automática,
instalamos el paquete `openntpd`:

    [myusername@alarmpi ~]$ sudo pacman -S openntpd

Y editamos el fichero `/etc/rc.conf` para comprobar que se ejecuta la
sincronización de `openntpd` al inicio y que el servicio `hwclock` está
bloqueado (tiene una exclamación delante de su nombre):

    # al final del fichero...
    DAEMONS=(!hwclock syslog-ng network openntpd @netfs @crond @sshd)

### _hostname_ e IP estática

Si queremos cambiar el _hostname_ editamos el fichero `/etc/rc.conf` y
modificamos el valor de la variable `HOSTNAME`.

Para cambiar la configuración de red y [asignarle una IP estática][], en
el mismo fichero `/etc/rc.conf` y añadimos nuestra configuración en la
sección correspondiente:

    interface=eth0
    address=192.168.1.51
    netmask=255.255.255.0
    broadcast=192.168.1.255
    gateway=192.168.1.1

Reiniciamos el servicio:

    [myusername@alarmpi ~]$ sudo /etc/rc.d/network restart

Si estábamos conectados por SSH, se cerrará la conexión y tendremos que
volver a conectarnos, entonces nos aparecerá una alerta diciéndonos que
la identificación del equipo remoto ha cambiado. Para solucionarlo,
ejecutamos:

    $ ssh-keygen -f "~/.ssh/known_hosts" -R 192.168.1.51

### Entorno gráfico

Si queremos instalar LXDE para tener un entorno gráfico:

    [myusername@alarmpi ~]$ sudo pacman -S lxde xorg-xinit xf86-video-fbdev

Lo iniciamos:

    [myusername@alarmpi ~]$ xinit /usr/bin/lxsession

Referencias
-----------

» [Raspberry Pi][]
» [Beginners’ Guide][]
» [Arch Linux Arm: First steps][]
» [pacman: gestor de paquetes de Arch][gestor de paquetes de Arch]
» [Arch Linux ARM: Raspberry Pi Forum][]

  [Raspberry Pi con Debian]: {filename}/admin/raspberry-pi.md
    "Raspberry Pi"
  [descargas]: http://www.raspberrypi.org/downloads
    "descargas"
  [Raspbmc]: http://www.raspbmc.com
    "Raspbmc"
  [PwnPi]: http://www.pwnpi.com
    "PwnPi"
  [pbzip2]: {filename}/admin/pbzip2-un-bzip2-mas-rapido.md
    "pbzip2, un bzip2 más rápido"
  [dependiendo de la tarjeta SD]: http://www.sakoman.com/OMAP/microsd-card-perfomance-test-results.html
    "dependiendo de la tarjeta SD"
  [gestor de paquetes de Arch]: http://archlinuxarm.org/support/guides/applications/package-management
    "gestor de paquetes de Arch"
  [evitar algunos problemas]: http://www.raspberrypi.org/phpBB3/viewtopic.php?f=53&t=7435
    "evitar algunos problemas"
  [actualizar se encontraron archivos que ya existían]: https://wiki.archlinux.org/index.php/Pacman#Q:_I_get_an_error_when_updating:_.2%20es%202file_exists_in_filesystem.22.21
    "actualizar se encontraron archivos que ya existían"
  [utilizar sudo]: https://wiki.archlinux.org/index.php/Beginners%27_Guide#Sudo
    "utilizar sudo"
  [autocompletado a sudo]: https://wiki.archlinux.org/index.php/Sudo#Enabling_tab-completion_in_bash
    "autocompletado a sudo"
  [no se encuentra en los repositorios oficiales]: http://ngty.github.com/blog/2011/10/06/installing-the-unofficial-byobu-in-archlinux/
    "no se encuentra en los repositorios oficiales"
  [asignarle una IP estática]: https://wiki.archlinux.org/index.php/Configuring_Network#Static_IP_address
    "asignarle una IP estática"
  [Raspberry Pi]: http://www.raspberrypi.org/
    "Raspberry Pi"
  [Beginners’ Guide]: https://wiki.archlinux.org/index.php/Beginners%27_Guide
    "Beginners’ Guide"
  [Arch Linux Arm: First steps]: http://archlinuxarm.org/support/guides/system/first-steps
    "Arch Linux Arm: First steps"
  [Arch Linux ARM: Raspberry Pi Forum]: http://archlinuxarm.org/forum/viewforum.php?f=31&sid=fa335d78a8c29fc06c45a897216049af
    "Arch Linux ARM: Raspberry Pi Forum"
