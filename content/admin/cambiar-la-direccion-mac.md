Title: Cambiar la dirección MAC
Date: 2011-02-09 12:58
Author: Nacho Cano
Tags: ifconfig, ip, ipconfig, kismet, mac, mac aleatoria, macchanger, md5sum, sed
Slug: cambiar-la-direccion-mac
Related: obteniendo-la-ip-publica-la-ip-privada-y-la-direccion-mac-en-bash

A veces, nos puede interesar cambiar la MAC de nuestra tarjeta de red,
ya sea porqué nos conectamos a una red en la que no queremos que quede
registrada nuestra MAC real (todavía se podría ser más paranoico), ya
sea porqué hay un filtrado por MAC y la nuestra no se encuentra en la
lista de las MAC autorizadas para conectarse.

![MAC Address]({static}/images/mac_address-300x252.png)

<small>_Fuente: [wikipedia][]_</small>

Para conocer la MAC de nuestras interfaces de red:

```bash
$ ifconfig  | grep -E "([0-9a-f]{2}:){5}[0-9a-f]{2}"
eth0      Link encap:Ethernet  direcciónHW 00:3c:72:26:3a:22
eth2      Link encap:Ethernet  direcciónHW 00:50:cb:d9:07:79
```

Para cambiar la MAC de la interfaz `eth0`, por ejemplo:

```bash
$ sudo ifconfig eth0 down
$ sudo ifconfig eth0 hw ether 00:00:de:ad:de:ad
$ sudo ifconfig eth0 up
```

En principio, podemos asignar la dirección MAC que queramos, mientras
sean números [hexadecimales][], con la salvedad de que, posiblemente,
necesitaremos que [tenga un identificador válido][]. Aún así, podríamos
asignar una MAC [aleatoria][]:

```bash
$ echo $(cat /proc/interrupts | md5sum | sed -r 's/^(.{10}).*$/00\1/; s/([0-9a-f]{2})/\1:/g; s/:$//;')
00:19:a9:58:2b:14
```

* * * * *

#### Actualizado el 22 de julio de 2014

Utilizando el comando `ip`, el cual vino a [sustituir a ifconfig][],
también podemos consultar las interfaces de red:

</p>
```bash
$ ip addr show
$ ip link show
```

Y cambiar la dirección MAC de la que nos interese:

```bash
$ sudo ip link set dev wlan1 down
$ sudo ip link set dev wlan1 address 00:19:a9:58:2b:14
$ sudo ip link set dev wlan1 up
```

* * * * *

gnu mac changer
---------------

`macchanger` es un programa que nos permite cambiar la MAC de varias
maneras. Por ejemplo:

Poner la MAC que queramos, de la misma manera que el comando anterior:

```bash
$ sudo macchanger -m 00:50:cb:d9:07:79 eth2
```

Cambiar la MAC sin cambiar la información del vendedor, es decir, los
tres primeros bytes:

```bash
$ sudo macchanger -e eth2
Current MAC: 00:50:cb:b4:98:16 (Jetter)
```

De manera aleatoria:

```bash
$ sudo macchanger -r
```

Mostrar un listado de vendedores:

```bash
$ macchanger -l
```

Filtrado de MAC
---------------

Si lo que queremos es usar una MAC autorizada para poder conectarnos,
dependerá de si la conexión es por cable o no. Si es por cable y tenemos
acceso a una consola, simplemente obtenemos la MAC como hemos visto y
enchufamos el cable de red. Si fuese un ordenador con Windows, podemos
obtener la MAC a través de las propiedades de la interfaz de red en el
administrador de redes del panel de control, o ejecutando en una
consola:

```bash
C:> ipconfig /all
```

Si es una conexión inalámbrica, podemos obtener alguna MAC válida de
algún equipo que esté conectado a la red, utilizando algún programa como
`kismet`.

![Kismet Client List WEP]({static}/images/kismet_client_list_wep-300x231.png)

  [wikipedia]: http://en.wikipedia.org/wiki/MAC_address
    "wikipedia"
  [hexadecimales]: http://en.wikipedia.org/wiki/Hexspeak
    "hexadecimales"
  [tenga un identificador válido]: {filename}/admin/obteniendo-la-ip-publica-la-ip-privada-y-la-direccion-mac-en-bash.md
    "obteniendo la IP pública, la IP privada y la dirección MAC en Bash"
  [aleatoria]: {filename}/dev/random-bash.md
    "aleatoriedad en bash"
  [sustituir a ifconfig]: http://www.tty1.net/blog/2010/ifconfig-ip-comparison_en.html
    "sustituir a ifconfig"
