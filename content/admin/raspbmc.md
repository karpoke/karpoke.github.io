Title: Raspbmc
Date: 2012-06-29 04:45
Author: Nacho Cano
Tags: 12.04, compartir conexión, debian, htpc, iptables, nat, raspberry pi, raspbmc, redirección ip, ubuntu precise pangolin, xbmc
Slug: raspbmc
Related: raspberry-pi,arch-en-raspberry-pi

[Raspbmc][] es una distribución basada en debian que permite ejecutar
XBMC en la Raspberry Pi, lo que la transforma en un interesante
reproductor multimedia casero (HTPC).

![Raspbmc logo]({static}/images/raspbmc-logo.png)

Esta distribución recibe actualizaciones constantes que añaden mejoras,
actualizaciones de _drivers_ y nuevas funcionalidades. Además, permite
compartir el contenido multimedia a través de NFS, SMB, FTP y HTTP.
Raspbmc ha sido creada y está siendo mantenida por Sam Nazarko.

![Raspbmc XBMC]({static}/images/raspbmc-xbmc-300x196.jpg)

<small>_Fuente [retrocomputers.eu][]_</small>


Instalación
-----------

La instalación es muy sencilla, ya que existe un _script_ que nos
simplifica el proceso. Lo descargamos:

```bash
$ wget http://svn.stmlabs.com/svn/raspbmc/testing/installers/python/install.py
```

Introducimos la tarjeta SD y nos aseguramos de que esté desmontada antes
de lanzar el _script_. Deberemos saber el nombre de dispositivo que
tiene la tarjeta SD, en este caso `/dev/mmcblk0`:

```bash
$ sudo python install-raspbmc.py
Raspbmc installer for Linux and Mac OS X
http://raspbmc.com
----------------------------------------
Please ensure you've inserted your SD card, and press Enter to continue.

Enter the 'Disk' you would like imaged, from the following list:


Enter your choice here (e.g. 'mmcblk0' or 'sdd'): mmcblk0
It is your own responsibility to ensure there is no data loss! Please backup your system before imaging
Are you sure you want to install Raspbmc to '/dev/mmcblk0'? [y/N] y
Downloading, please be patient...
Downloaded 49.52 of 49.52 MiB (100.00%)

Please wait while Raspbmc is installed to your SD card...
(This may take some time and no progress will be reported until it has finished.)
0+5852 registros leídos
0+5852 registros escritos
198000640 bytes (198 MB) copiados, 21,7791 s, 9,1 MB/s
Installation complete.
Finalising SD card, please wait...


Raspbmc is now ready to finish setup on your Pi, please insert the
SD card with an active internet connection
```

Tras insertar la tarjeta SD en la Raspberry Pi y reiniciar, continuará
la instalación y configuración del sistema. En particular, no tendremos
que preocuparnos de [modificar las particiones para aprovechar al máximo
el espacio de la tarjeta SD][], ya que lo hace de forma automática. Es
necesario que la Raspberry Pi esté conectada a Internet. Una vez que
termine, reiniciará y aparecerá la interfaz de XBMC. La descarga e
instalación puede tardar un rato, entre 15 y 20 minutos. Esto lo comento
especialmente por si hay alguien que el primer arranque lo realiza sin
que la RPi esté conectada a ninguna pantalla, para que no desespere
hasta que por fin pueda conectarse por ssh.

Además, ya está preparada y configurada para que accedamos por SSH y
FTP. El usuario el __pi__ y la contraseña `raspberry`, aunque quizá esta
es una de [las primeras cosas que debamos cambiar nada más terminar la
instalación][].

Conexión a través de otro equipo
--------------------------------

Ya que parece que [la antena WIFI USB no funciona si no es con _hub_ USB
con alimentación][], y ahora mismo no tengo uno a mano, y la conexión
directa por cable al _router_ no es posible (desde donde pensaba colocar
la Raspberry Pi), he probado otra posibilidad, y es [conectarla por
cable a un portátil][] que hará de intermediario y me permitirá
conectarme a y tener conexión en la Raspberry Pi.

En el portátil, en este caso con Ubuntu Precise Pangolin 12.04, vamos a
Configuración de Red > Cableada > Opciones (será accesible cuando
conectemos el cable a la Raspberry Pi estando encendida) > Ajustes de
IPv4:

-   seleccionamos "Compartida con otros equipos"
-   marcamos "Requiere dirección IPv4 para que esta conexión se
    complete"

Esto nos asigna por defecto la dirección IP 10.42.0.1, máscara
255.255.255.0 y ruta predeterminada 0.0.0.0. Parece que no es
configurable.

Debemos prestar atención al cortafuegos, y permitir la compartición de la
conexión. Por ejemplo, con Firestarter, vamos a Cortafuegos > Ejecutar
asistente:

-   Dispositivo(s) detectado(s): seleccionamos "Dipositivo inalámbrico
    (wlan1)"
-   Marcamos "Activar la compartición de la conexión a Internet"
-   Dispositivo de red de área local: seleccionamos "Dispositivo
    ethernet (eth0)"

También podemos hacerlo a mano con `iptables`. Si estamos seguros de que
no utilizamos ninguna otra regla en la NAT, la podemos limpiar:

```bash
$ sudo iptables -F -t nat
```

Ahora deberemos crear una regla para indicar la otra interfaz que hará
de puente, en este caso `wlan1`:

```bash
$ sudo iptables --table nat --append POSTROUTING --out-interface wlan1 -j MASQUERADE
```

Y por último, activamos la redirección IP:

```bash
$ sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
```

Si optamos por el método manual, y queremos que se ejecute cada vez que
arranca el portátil (algo que puede no ser necesario), añadimos al final
del fichero `/etc/rc.local`:

```bash
iptables -F -t nat
iptables --table nat --append POSTROUTING --out-interface wlan1 -j MASQUERADE
echo 1 > /proc/sys/net/ipv4/ip_forward
```

Con esto el portátil ya está configurado, ahora sólo queda configurar la
Rasperry Pi para que tenga IP estática de la misma red que tenemos en la
interfaz del portátil. Vamos a Programs > Raspbmc Settings > Wired
Network:

-   IP address: 10.42.0.50
-   Netmask: 255.255.255.0
-   Gateway: 10.42.0.1 (la IP del portátil)
-   DNS Server: 208.67.222.222
-   Search domain: local

Esta es una solución temporal y tiene sus inconvenientes, ya que
necesitamos conectar otro equipo por cable a la Raspberry Pi para
conectarnos "remotamente" por SSH, ya sea para llevar a cabo
actualizaciones, instalar programas, instalar complementos o copiar
archivos multimedia. Además, mientras no esté conectada al portátil no
podremos hacer uso de los complementos que necesitan acceso a Internet y
con este método tampoco podremos utilizar la [aplicación para Android
para controlar XBMC][].

  [Raspbmc]: http://www.raspbmc.com/
    "Raspbmc"
  [retrocomputers.eu]: http://www.retrocomputers.eu/2012/06/20/watching-micro-men-via-xbmc-on-the-raspberry-pi/
    "retrocomputers.eu"
  [modificar las particiones para aprovechar al máximo el espacio de la tarjeta SD]: {filename}/admin/raspberry-pi.md
    "modificar las particiones para aprovechar al máximo el espacio de la tarjeta SD"
  [comment]: # (fragment eliminado del enlace anterior #aprovechando-todo-el-espacio-de-la-tarjeta-sd)
  [las primeras cosas que debamos cambiar nada más terminar la instalación]: {filename}/admin/raspberry-pi.md
    "las primeras cosas que debamos cambiar nada más terminar la instalación"
  [comment]: # (fragment eliminado del enlace anterior #despues-de-instalar-debian)
  [la antena WIFI USB no funciona si no es con _hub_ USB con alimentación]: {filename}/admin/raspberry-pi.md
    "la antena WIFI USB no funciona si no es con _hub_ USB con alimentación"
  [comment]: # (fragment eliminado del enlace anterior #conexion-inalambrica-con-una-antena-wifi-usb)
  [conectarla por cable a un portátil]: http://www.raspberrypi.org/phpBB3/viewtopic.php?t=6997&p=94689
    "conectarla por cable a un portátil"
  [aplicación para Android para controlar XBMC]: https://play.google.com/store/apps/details?id=org.xbmc.android.remote
    "aplicación para Android para controlar XBMC"
