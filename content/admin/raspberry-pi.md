Title: Raspberry Pi
Date: 2012-06-21 13:47
Author: Nacho Cano
Tags: arduino, debian, fedora, parted, raspberry pi, squeeze, tarjeta SD, ubuntu
Slug: raspberry-pi

En pocas palabras, [Raspberry Pi][] es un ordenador del tamaño de una
tarjeta de crédito que puede reproducir vídeo en alta definición (HDMI)
y cuesta, dependiendo del modelo, 25&#36; sin _ethernet_ o 35&#36; con
_ethernet_ [1].

![Raspi Colour]({static}/images/Raspi_Colour_R-248x300.png)

Cuenta con un procesador ARM11 a 700Mhz, 256MB RAM, USB 2.0, conectores
de audio y RCA. Se alimenta a través de un puerto mini-USB y tiene una
ranura para una tarjeta SD (de hasta 32GB) que es donde se instala el
sistema operativo. No tiene WiFi, pero se le puede añadir una antena
WiFi USB.

![Raspi Iso Blue]({static}/images/Raspi_Iso_Blue-300x220.png)

_Diagrama de Paul Beech_

Detrás de este proyecto está la fundación Raspberry Pi [2], una entidad
sin ánimo de lucro cuyo objetivo es proporcionar un ordenador sencillo y
barato a niños de todo el mundo, enfocado a un uso educacional. Una gran
cantidad de voluntarios y otras entidades sin ánimo de lucro se están
involucrando en este proyecto. La única pega es que tanto la GPU como su
controlador es de código cerrado. Las aplicaciones usan llamadas a unas
librerías de código privativo que son las que llaman a su vez al
controlador libre incluido en el *kernel*. La API del *driver* del _kernel_
es específica para éstas.

Las primeras unidades se comenzaron a ofrecer a finales de febrero, pero
el reducido número de unidades iniciales y la alta demanda han provocado
que, por ahora, sólo se pueda comprar una Raspberry Pi por persona,
siendo necesario haberse apuntado previamente en lista de espera ya que
con cada nueva remesa se sirven según este orden. En mi caso, lo pedí en
[RS-Online][] y han pasado unos dos meses hasta que pude hacer el
pedido, más otras tres semanas de envío. Hay mucha gente queriendo
probarlo :)

El pedido básico viene sólo con la placa, ni fuente de alimentación, ni
tarjeta SD, ni nada. Todo esto está disponible en RS-Online si queremos,
pero realmente no será necesario. Se puede utilizar prácticamente
cualquier cargador de móvil con conector mini-USB de fuente de
alimentación, que proporcione 5V y, al menos, 700mA para el modelo B (o
300mA en caso del modelo A) [3].

En principio, las tarjetas SD de clase 10 son las que tienen un mejor
rendimiento de escritura, aunque la diferencia de una marca a otra puede
ser importante [4], pero parece ser que hay algunos problemas con
algunos modelos concretos [5]. Para estar seguros de que la tarjeta que
utilicemos es compatible, así como otros periféricos USB, podemos
consultar esta página [6].

Instalación de debian squeeze
-----------------------------

Existen varias distribuciones que podremos utilizar como sistema
operativo, como fedora, debian o arch, y posiblemente aparecerán más
[7]. Debian incluye gcc, Python y algunas aplicaciones de ejemplo.
Parece que Ubuntu no va a estar, por ahora, debido a que no da soporte
al ARM11 que lleva la placa.

En la página de [descargas][] podemos escoger entre las distribuciones
adaptadas. Para no sobrecargar el servidor de descargas, podemos
descargar el _torrent_. Si queremos descargar el código fuente, así como
las herramientas para compilación cruzada, podemos hacerlo desde la
página de GitHub [8].

Una vez que tengamos la imagen, procederemos a instalarla en la tarjeta
SD [9]. El proceso es sencillo. Por ejemplo, para instalar debian,
después de haber descargado la imagen, comprobamos que es correcta:

```bash
$ sha1sum ~/debian6-19-04-2012.zip
1852df83a11ee7083ca0e5f3fb41f93ecc59b1c8  debian6-19-04-2012.zip
```

Extraemos la imagen:

```bash
$ unzip debian6-19-04-2012.zip
```

Montamos la tarjeta, si no está montada ya, y anotamos qué nombre tiene
el dispositivo:

```bash
$ df | grep mmc
/dev/mmcblk0p1            7871488        32    7871456   1% /media/FC30-3DA9
```

En este caso el sufijo `p1` indica que está montada la primera
partición, pero nosotros queremos la ruta a la tarjeta, no sólo una
partición, ya que la imagen creará las particiones, así que nos quedamos
con el nombre `mmcblk0`. También podría ser que el nombre del
dispositivo fuese, por ejemplo, `/dev/sdd1`, en cuyo caso el `1` es la
partición y el nombre del dispositivo `sdd`.

Desmontamos la tarjeta SD:

```bash
$ umount /media/FC30-3DA9
```

Volcamos la imagen en la tarjeta SD:

```bash
$ dd bs=1M if=debian6-19-04-2012/debian6-19-04-2012.img of=/dev/mmcblk0
1859+1 registros leídos
1859+1 registros escritos
1950000000 bytes (2,0 GB) copiados, 151,45 s, 12,9 MB/s
```

<a name="aprovechando-todo-el-espacio-de-la-tarjeta-sd"></a>

Aprovechando todo el espacio de la tarjeta SD
---------------------------------------------

La imagen está preparada para una tarjeta de 2 GB, si nuestra tarjeta es
de un tamaño mayor, podemos redimensionar las particiones creadas por la
imagen para utilizar todo el espacio disponible. Esto lo podríamos hacer
directamente desde la debian en Raspberry Pi, pero ahora lo haremos
desde el terminal de la Ubuntu.

Utilizaremos `parted` con la tarjeta, de 8 GB, aún desmontada:

```bash
$ sudo parted /dev/mmcblk0
(parted) unit chs
(parted) print
Modelo: SD 00000 (sd/mmc)
Disco /dev/mmcblk0: 123119,3,31
Tamaño de sector (lógico/físico): 512B/512B
Geometría cilindro,cabeza,sector de BIOS: 123120,4,32. Cada cilindro es 65,5kB.
Tabla de particiones. msdos

Numero  Inicio     Fin         Tipo     Sistema de archivos  Banderas
 1      16,0,0     1215,3,31   primary  fat32                lba
 2      1232,0,0   26671,3,31  primary  ext4
 3      26688,0,0  29743,3,31  primary  linux-swap(v1)
```

Aquí vemos las particiones que se han creado tras el volcado de la
imagen, y que no se usa el espacio desde el cilindro 29743 hasta el
último cilindro 123119.

La primera partición es la de arranque (_boot_). La segunda es la
partición de `root` y será la que aumentaremos todo lo posible. La
tercera partición es la `swap`, que tenemos que mover hasta al final de
la tarjeta.

Para mover la partición de `swap`, primero debemos calcular el número de
cilindro a partir del cual la vamos a poner. Para calcular este número
utilizamos la siguiente fórmula:

```bash
inicio = (máximo - (final partición 3 - inicio partición 3) - 1
```

Por ejemplo:

```bash
inicio = (123119 - ( 29743 - 26688)) - 1 = 120063
```

Seguimos con `parted` y la movemos:

```bash
(parted) move 3 120063,0,0
```

Ahora ampliaremos el tamaño de la partición de `root`, sin que perdamos
los datos en ella:

```bash
(parted) rm 2
(parted) mkpart primary 1232,0,0 120062,3,31
(parted) quit
```

El inicio de la partición de `root` es el mismo que ya tenía y el último
es justo antes del de la partición de _swap_.

Ya podemos limpiar y redimensionar la partición con `e2fsck` (como es la
segunda añadimos `p2`):

```bash
$ sudo e2fsck -f /dev/mmcblk0p2 # (permitimos añadir lost-and-found)
e2fsck 1.42 (29-Nov-2011)
Paso 1: Verificando nodos-i, bloques y tamaños
Paso 2: Verificando la estructura de directorios
Paso 3: Revisando la conectividad de directorios
No se encontró /lost+found.  Crear? si

Paso 4: Revisando las cuentas de referencia
Paso 5: Revisando el resumen de información de grupos

/dev/mmcblk0p2: __*** EL SISTEMA DE FICHEROS FUE MODIFICADO ***__
/dev/mmcblk0p2: 59389/101920 files (0.0% non-contiguous), 310435/407040 blocks
```

```bash
$ sudo resize2fs /dev/mmcblk0p2
resize2fs 1.42 (29-Nov-2011)
Resizing the filesystem on /dev/mmcblk0p2 to 1901296 (4k) blocks.
The filesystem on /dev/mmcblk0p2 is now 1901296 blocks long.
```

Sacamos la tarjeta y la introducimos en Raspberry Pi. El usuario por
defecto es __pi** y la contraseña **raspberry__. Esto será lo primero
que cambiaremos.

<a name="despues-de-instalar-debian"></a>

Después de instalar debian
--------------------------

Tras arrancar por primera vez la Raspberry Pi, una de las primeras
acciones que debemos llevar a cabo, sobre todo si pensamos que se pueda
acceder desde fuera de la red, es cambiar la contraseña que viene por
defecto.

Ejecutamos el comando `passwd` e introducimos la nueva contraseña.

Lo siguiente, actualizar el sistema:

```bash
pi@raspberrypi:~$ sudo apt-get install aptitude
pi@raspberrypi:~$ sudo aptitude update && sudo aptitude safe-upgrade
```

Si nuestro teclado no es inglés, podemos configurarlo para nuestro
idioma ejecutando:

```bash
pi@raspberrypi:~$ sudo dpkg-reconfigure keyboard-configuration
```

Y para que los cambios tengan efecto:

```bash
pi@raspberrypi:~$ sudo setupcon
```

Instalamos algunos paquetes "básicos":

```bash
pi@raspberrypi:~$ sudo aptitude install byobu htop locate vim vlc
```

Añadimos algunos _alias_, por ejemplo:

```bash
pi@raspberry:~$ cat > .bash_aliases << EOF
alias api="sudo aptitude install"
alias apu="sudo aptitude update"
alias apg="sudo aptitude safe-upgrade"
alias ..="cd .."
alias vim="vim.tiny"
EOF
```

Si queremos acceder mediante SSH, ya viene con un _script_ que se
encarga de arrancar el servidor SSH al inicio. Lo único que tenemos que
hacer es renombrar el fichero `boot_enable_ssh.rc`:

```bash
pi@raspberry:~$ sudo mv /boot/boot_enable_ssh.rc /boot/boot.rc
```

Por defecto, la configuración de SSH es demasiado permisiva. Podemos
endurecerla, por ejemplo, cambiando el número de puerto en el que
escucha el demonio, [utilizando claves para conectarnos][], impidiento
que el usuario `root` pueda iniciar sesión (`PermitRootLogin no`), etc.

Reiniciamos el servicio para que los cambios tengan efecto:

```bash
pi@raspberry:~$ sudo service ssh restart
```

Antes de cerrar la sesión SSH que tenemos abierta, deberíamos comprobar
que podemos acceder de forma remota tras aplicar los cambios, ya que, de
lo contrario, nos quedaremos sin poder conectar. Si desde el equipo que
nos conectamos, hemos configurado la [reutilización de la conexión
SSH][], estas pruebas se deberán llevar a cabo en otro terminal.

Por último, si nos vamos a conectar de forma remota, lo mejor sería
asignarle una IP estática. Editamos el fichero `/etc/network/interfaces`
y modificamos la configuración de la tarjeta:

```bash
auto eth0
iface eth0 inet static
   address 192.168.1.51
   netmaks 255.255.255.0
   gateway 192.168.1.1
   broadcast 192.168.1.255
   network 192.168.1.0
```

Reiniciamos el servicio para que los cambios tengan efecto:

```bash
pi@raspberry:~$ sudo service networking restart
```

Si queremos arrancar el entorno gráfico LXDE:

```bash
pi@raspberrypi:~$ startx
```

<a name="conexion-inalambrica-con-una-antena-wifi-usb"></a>

Conexión inalámbrica con una antena WIFI USB
--------------------------------------------

En mi caso, tengo [antena WiFi USB][] con chip ZyDAS que se necesita
configurar.

Conectamos la antena y comprobamos que la reconoce:

```bash
pi@raspberrypi:~$ lsusb
Bus 001 Device 004: ID 0ace:1211 ZyDAS ZD1211 802.11g
```

El controlador para esta antena no es libre, así que para instalarlo
deberemos activar los repositorios `non-free`. Editamos el fichero
`/etc/apt/sources.list` y la añadimos, para que quede:

```bash
deb http://ftp.uk.debian.org/debian/ squeeze main non-free
```

Actualizamos los repositorios:

```bash
pi@raspberrypi:~$ sudo aptitude update
```

Instalamos el controlador:

```bash
pi@raspberrypi:~$ sudo aptitude install zd1211-firmware
```

Si el siguiente comando nos funciona, sólo quedará configurar la
conexión:

```bash
pi@raspberrypi:~$ sudo iwlist wlan0 scan
```

### Conexión WPA2

Si queremos configurar la conexión inalámbrica a una red cifrada con
WPA2, lo primero será asegurarnos de que tenemos el paquete necesario:

```bash
pi@raspberrypi:~$ sudo aptitude install wpasupplicant
```

Creamos el fichero con el nombre de la red y la contraseña:

```bash
pi@raspberrypi:~$ wpa_passphrase MYESSID mypassphrase | sudo tee /etc/wpa_supplicant/wpa_supplicant.conf
pi@raspberrypi:~$ sudo chmod 600 /etc/wpa_supplicant/wpa_supplicant.conf
```

Editamos el fichero para añadirle los siguientes campos:

```bash
network {
   ssid="MYSSID"
   #psk="mypassphrase"
   psk=ce4d0c6d7585a8432e2205c2b8d2ec5439dab5d9185f4b6f4c41d4120eb36161
   proto=RSN # "RSN" para WPA2, "WPA" para WPA
   key_mgmt=WPA-PSK
   pairwise=CCMP TKIP # CCMP==AES
   group=CCMP TKIP
}
```

Editamos el fichero de configuración de la red,
`/etc/network/interfaces`, y le asignamos una IP estática, por ejemplo:

```bash
auto wlan0
iface wlan0 inet static
   address 192.168.1.51
   gateway 192.168.1.1
   broadcast 192.168.1.255
   network 192.168.1.0
   wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
```

Sólo queda reiniciar la red:

```bash
pi@raspberrypi:~$ sudo service networking restart
```

Aunque todo parecía ir bien, al final no logro que establecer la
conexión. Mirando en los _logs_ he podido encontrar:

```bash
pi@raspberrypi:~$ dmesg | grep zd1211rw
zd1211rw 1-1.2:1.0: phy0
usbcore: registered new interface driver zd1211rw
zd1211rw 1-1.2:1.0: firmware version 4605
zd1211rw 1-1.2:1.0: zd1211 chip 0ace:1211 v4330 high 00-02-e3 RF2959_RF pa0 g----
zd1211rw 1-1.2:1.0: TX-stall detected, reseting device...
```

Parece ser que ese _TX-stall detected_ es debido a que [la Raspberry Pi
no aporta suficiente potencia para la antena WIFI][], por lo que la
única solución parece que es utilizar una _hub_ USB con alimentación.

Proyectos relacionados
----------------------

Algunos proyectos que ya están en marcha, relacionados con Raspberry Pi:

-   __[expEYES][]__: una herramienta, sofware y hardware, para
    desarrollo y experimentación de proyectos científicos [10]
-   __módulo con cámara__: un prototipo de cámara que puede ser
    conectada a Raspberry Pi [11]
-   __Raspberry Pi y Arduino__: algunos ejemplos [12][13][14] de
    comunicación entre ambos dispositivos [15]
-   __Pwnpi__: distribución enfocada a tests de penetración [16]
-   __[raspbmc][]__: distribución enfocada a utilizar la Raspberry Pi
    como Media Center [17]

Otros enlaces interesantes:

» [Carcasas][]
» [Placas de expansión][]
» [Periféricos de bajo nivel][]
» [Especificaciones de hardware][]

Referencias
-----------

1.  <http://www.raspberrypi.org/faqs>
2.  <http://www.raspberrypi.org/about>
3.  <http://www.raspberrypi.org/archives/260>
4.  <http://www.sakoman.com/OMAP/microsd-card-perfomance-test-results.html>
5.  <http://www.raspberrypi.org/phpBB3/viewtopic.php?f=2&t=4076>
6.  <http://elinux.org/RPi_VerifiedPeripherals>
7.  <http://www.raspberrypi.org/downloads>
8.  <http://github.com/raspberrypi>
9.  <http://elinux.org/RPi_Easy_SD_Card_Setup>
10. <http://www.raspberrypi.org/archives/1228>
11. <http://www.raspberrypi.org/archives/1254>
12. <http://www.doctormonk.com/2012/04/raspberry-pi-and-arduino.html>
13. <http://www.doctormonk.com/2012/05/gpio-led-blink-from-python-using-slice.html>
14. <http://omer.me/2012/05/introducing-ponte/>
15. <http://www.raspberrypi.org/archives/1171>
16. <http://www.pwnpi.com/>
17. <http://www.raspbmc.com/about/>

  [Raspberry Pi]: http://www.raspberrypi.org/
    "Raspberry Pi"
  [RS-Online]: http://uk.rs-online.com/web/generalDisplay.html?id=raspberrypi
    "RS-Online"
  [descargas]: http://www.raspberrypi.org/downloads
    "descargas"
  [utilizando claves para conectarnos]: {filename}/admin/conectarse-por-ssh-solo-usando-la-clave.md
    "Conectarse por SSH sólo usando la clave"
  [reutilización de la conexión SSH]: {filename}/admin/compartiendo-una-conexion-por-ssh.md
    "reutilización de la conexión SSH"
  [antena WiFi USB]: http://omer.me/2012/04/setting-up-wireless-networks-under-debian-on-raspberry-pi/
    "antena WiFi USB"
  [la Raspberry Pi no aporta suficiente potencia para la antena WIFI]: http://www.raspberrypi.org/phpBB3/viewtopic.php?t=7241&p=99068
    "la Raspberry Pi no aporta suficiente potencia para la antena WIFI"
  [expEYES]: http://expeyes.in/
    "expEYES"
  [raspbmc]: http://www.raspbmc.com/
    "raspbmc"
  [Carcasas]: http://elinux.org/RPi_Cases
    "Carcasas"
  [Placas de expansión]: http://elinux.org/RPi_Expansion_Boards
    "Placas de expansión"
  [Periféricos de bajo nivel]: http://elinux.org/RPi_Low-level_peripherals
    "Periféricos de bajo nivel"
  [Especificaciones de hardware]: http://elinux.org/RPi_Hardware
    "Especificaciones de hardware"
