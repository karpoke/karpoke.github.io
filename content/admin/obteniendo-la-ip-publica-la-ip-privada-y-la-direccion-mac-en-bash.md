Title: Obteniendo la IP pública, la IP privada y la dirección MAC en Bash
Date: 2011-08-14 19:26
Author: Nacho Cano
Tags: alias, curl, dirección MAC, DynDNS, hostname, ifconfig, in-addr.arpa, IP privada, IP pública, ipcalc, mac, oui, perl, php, script, wget
Slug: obteniendo-la-ip-publica-la-ip-privada-y-la-direccion-mac-en-bash

En los _scripts_ que escribimos, a menudo, es necesario conocer la IP pública
de nuestra red, o la IP privada y la dirección MAC de una interfaz de red. Con
el comando `ifconfig` podemos conocer la información de las interfaces de red:

    $ ifconfig
    eth0      Link encap:Ethernet  direcciónHW 00:11:22:33:44:55
              Direc. inet:192.168.0.30  Difus.:192.168.0.255  Másc:255.255.255.0
              Dirección inet6: fe80::203:dff:fe3c:f419/64 Alcance:Enlace
              ACTIVO DIFUSI–N FUNCIONANDO MULTICAST  MTU:1500  Métrica:1
              Paquetes RX:1627 errores:0 perdidos:0 overruns:0 frame:0
              Paquetes TX:1067 errores:0 perdidos:0 overruns:0 carrier:0
              colisiones:0 long.colaTX:1000
              Bytes RX:560137 (560.1 KB)  TX bytes:235094 (235.0 KB)
              Interrupción:19 Dirección base: 0xc800

    eth1      Link encap:Ethernet  direcciónHW 00:11:22:33:44:66
              DIFUSI–N MULTICAST  MTU:1500  Métrica:1
              Paquetes RX:0 errores:0 perdidos:0 overruns:0 frame:0
              Paquetes TX:0 errores:0 perdidos:0 overruns:0 carrier:0 colisiones:0 long.colaTX:1000
              Bytes RX:0 (0.0 B)  TX bytes:0 (0.0 B)
              Interrupción:21 Dirección base: 0x8000 Memoria:ffcfe000-ffcfefff

    lo        Link encap:Bucle local
              Direc. inet:127.0.0.1  Másc:255.0.0.0
              Dirección inet6: ::1/128 Alcance:Anfitrión
              ACTIVO BUCLE FUNCIONANDO  MTU:16436  Métrica:1
              Paquetes RX:3299 errores:0 perdidos:0 overruns:0 frame:0
              Paquetes TX:3299 errores:0 perdidos:0 overruns:0 carrier:0
              colisiones:0 long.colaTX:0
              Bytes RX:355696 (355.6 KB)  TX bytes:355696 (355.6 KB)

Sin embargo, si queremos utilizar el dato en concreto—la IP privada o la
dirección MAC—, necesitaremos trabajar un poco la salida que muestra
`ifconfig`.


IP privada
----------

Para obtener la [IP privada (IPv4)][] de una interfaz concreta, por ejemplo, la
eth0:

    $ ifconfig eth2 | perl -nle'/((\d+\.){3}\d+)/ && print $1'
    192.168.0.30

La expresión regular es suficiente para parsear la salida de `ifconfig` y
obtener la dirección IP de la interfaz. Pero esta expresión regular no la
podríamos emplear para descartar una IP privada no válida.

El rango de IP privadas está definido en el [RFC 1918][] y contempla los
rangos:

    10.0.0.0        -   10.255.255.255  (10/8 prefix)
    172.16.0.0      -   172.31.255.255  (172.16/12 prefix)
    192.168.0.0     -   192.168.255.255 (192.168/16 prefix)

* * * * *

#### Actualizado el 29 de diciembre de 2014

Podemos utilizar el comando `ipcalc` para ver los rangos privados:

    $ ipcalc 10.0.0.0/8
    Address:   10.0.0.0             00001010. 00000000.00000000.00000000
    Netmask:   255.0.0.0 = 8        11111111. 00000000.00000000.00000000
    Wildcard:  0.255.255.255        00000000. 11111111.11111111.11111111
    =>
    Network:   10.0.0.0/8           00001010. 00000000.00000000.00000000
    HostMin:   10.0.0.1             00001010. 00000000.00000000.00000001
    HostMax:   10.255.255.254       00001010. 11111111.11111111.11111110
    Broadcast: 10.255.255.255       00001010. 11111111.11111111.11111111
    Hosts/Net: 16777214              Class A, Private Internet


    $ ipcalc 172.16.0.0/12
    Address:   172.16.0.0           10101100.0001 0000.00000000.00000000
    Netmask:   255.240.0.0 = 12     11111111.1111 0000.00000000.00000000
    Wildcard:  0.15.255.255         00000000.0000 1111.11111111.11111111
    =>
    Network:   172.16.0.0/12        10101100.0001 0000.00000000.00000000
    HostMin:   172.16.0.1           10101100.0001 0000.00000000.00000001
    HostMax:   172.31.255.254       10101100.0001 1111.11111111.11111110
    Broadcast: 172.31.255.255       10101100.0001 1111.11111111.11111111
    Hosts/Net: 1048574               Class B, Private Internet


    $ ipcalc 192.168.0.0/16
    Address:   192.168.0.0          11000000.10101000. 00000000.00000000
    Netmask:   255.255.0.0 = 16     11111111.11111111. 00000000.00000000
    Wildcard:  0.0.255.255          00000000.00000000. 11111111.11111111
    =>
    Network:   192.168.0.0/16       11000000.10101000. 00000000.00000000
    HostMin:   192.168.0.1          11000000.10101000. 00000000.00000001
    HostMax:   192.168.255.254      11000000.10101000. 11111111.11111110
    Broadcast: 192.168.255.255      11000000.10101000. 11111111.11111111
    Hosts/Net: 65534                 Class C, Private Internet

* * * * *

El siguiente [_script_ realiza la comprobación de una IP privada][], y devuelve
1 si es válida, o 0 en caso contrario:

    #!/bin/bash
    IP="$1"

    # checks for a valid number: 0..255
    function v() {
            n=${1:-300}
            if [ $n -lt 0 ] || [ $n -gt 255 ]; then
                    echo 0
            else
                    echo 1
            fi
    }

    # parse IP
    OLD_IFS=$IFS
    IFS='.'
    IP=($IP)
    IFS=$OLD_IFS

    A=${IP[0]}
    B=${IP[1]}
    C=${IP[2]}
    D=${IP[3]}

    # private ips. rfc 1918 https://tools.ietf.org/html/rfc1918#page-4
    # 10.0.0.0    to 10.255.255.255
    # 172.16.0.0  to 172.31.255.255
    # 192.168.0.0 to 192.168.255.255
    if [ $A -eq 10 -a $(v $B) -eq 1 -a $(v $C) -eq 1 -a $(v $D) -eq 1 ] ||
       [ $A -eq 172 -a $B -ge 16 -a $B -le 31 -a $(v $C) -eq 1 -a $(v $D) -eq 1 ] ||
       [ $A -eq 192 -a $B -eq 168 -a $(v $C) -eq 1 -a $(v $D) -eq 1 ]; then
       echo 1
    else
       echo 0
    fi

* * * * *

#### Actualizado el 11 de enero de 2014

Otra forma de obtener la IP privada es mediante el comando `hostname`:

    $ hostname -I
    192.168.0.30

* * * * *

Dirección MAC
-------------

Para obtener la [dirección MAC][]:

    $ ifconfig eth0 | grep -oE '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'
    00:11:22:33:44:55

La dirección MAC está compuesta por 6 bytes, separados por dos puntos (:) o
guión (-), por ejemplo, 00:11:22:33:44:55. La primera mitad (00:11:22) es el
Identificador Único de Organización (OUI), el fabricante. La segunda mitad
(33:44:55) es una extensión que permite identificar de forma única cada tarjeta
de red para un fabricante concreto. Hay puntos de acceso que ignorarán OUIs
inválidos. Está bien saber esto si vamos a [cambiar la dirección MAC de una
tarjeta][]. En este enlace se encuentra el [listado de OUIs válidos][].

Una dirección MAC válida que tiene [el último bit del primer byte a 0][], se
corresponde con una dirección _unicast_. Si es 1, indica una dirección de
grupo, lo que se suele reservar para tráfico _multicast_.  Las direcciones MAC
con un origen _multicast_ son invalidas y se ignoran.

Si generamos la dirección MAC de forma [aleatoria][], deberíamos poner el
primer byte a 0, para asegurarnos:

    $ echo $(cat /proc/interrupts | md5sum | sed -r 's/^(.{10}).*$/00\1/; s/([0-9a-f]{2})/\1:/g; s/:$//;')
    00:1f:7a:2e:ef:c7

Podemos comprobar si el OUI es válido ejecutando:

    $ mac=$(ifconfig eth0 | grep -oE '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}')
    $ oui=${mac:0:8}
    $ oui=${oui//:/-}
    $ test ! -r oui.txt && wget http://standards.ieee.org/develop/regauth/oui/oui.txt  # 2.3 MB
    $ grep -i $oui oui.txt && echo "Valid OUI" || echo "Not valid OUI"

IP Pública
----------

Si queremos obtener nuestra IP pública (IPv4), podemos recurrir a servicios
como el de DynDNS:

    $ curl -s checkip.dyndns.org | grep -Eo "[0-9\.]+"
    1.2.3.4

Otros servicios:

- checkip.dyndns.org
- fmbip.com
- icanhazip.com
- ifconfig.me
- ip.appspot.com
- ipecho.net/plain
- ipinfo.io
- ip.u3mx.com
- myip.dnsomatic.com
- myip.opendns.com
- snar.co/ip/
- whatismyip.org
- www.check-my-ip.net
- www.ipchicken.com

* * * * *

#### Actualización a 11 de enero de 2014

Si no queremos depender de terceros y tenemos acceso a algún servidor web, el
siguiente código PHP nos devolverá nuestra IP:

    <?php echo $_SERVER['REMOTE_ADDR']; ?>

* * * * *

Si en lugar de estar conectados en una LAN, estamos conectados directamente a
Internet, en lugar de recurrir a servicios externos, podemos ejecutar:

    $ ifconfig  | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}'
    1.2.3.4

* * * * *

#### Actualizado el 24 de agosto de 2012

Direcciones .arpa
-----------------

Las direcciones .arpa se utilizan para la resolución inversa de DNS. Así por
ejemplo, la IP 1.2.3.4 se asocia al dominio 4.3.2.1.in-addr.arpa.

Si queremos obtener las IP asociadas a dominios .arpa para utilizarlas, por
ejemplo, en un _script_, podemos usar el siguiente _alias_:

    $ alias arpa2ip='(type farpa2ip >/dev/null 2>&1) || farpa2ip() { echo "$1" | awk '\''BEGIN{FS="."}{print $4"."$3"."$2"."$1;}'\''; }; farpa2ip'

Un ejemplo de uso:

    $ arpa2ip 12.108.52.65.in-addr.arpa
    65.52.108.12

El proceso inverso, obtener una dirección .arpa a partir de una IP, se puede
conseguir mediante el siguiente _alias_:

    $ alias ip2arpa='(type fip2arpa >/dev/null 2>&1) || fip2arpa() { echo "$1" | awk '\''BEGIN{FS="."}{print $4"."$3"."$2"."$1".in-addr.arpa";}'\''; }; fip2arpa'

Un ejemplo de uso:

    $ ip2arpa 65.52.108.12
    12.108.52.65.in-addr.arpa

* * * * *

  [IP privada (IPv4)]: http://www.commandlinefu.com/commands/view/2825/get-all-ips-via-ifconfig
    "IP privada (IPv4)"
  [RFC 1918]: http://tools.ietf.org/html/rfc1918#page-4
    "RFC 1918"
  [_script_ realiza la comprobación de una IP privada]: http://terminus.ignaciocano.com/wp-uploads/linked/is-valid-private-ip.sh
    "is-valid-private-ip.sh"
  [dirección MAC]: http://www.commandlinefu.com/commands/view/4974/get-all-mac-address
    "dirección MAC"
  [cambiar la dirección MAC de una tarjeta]: {filename}/admin/cambiar-la-direccion-mac.md
    "cambiar la dirección MAC de una tarjeta"
  [listado de OUIs válidos]: http://standards.ieee.org/develop/regauth/oui/oui.txt
    "listado de OUIs válidos"
  [el último bit del primer byte a 0]: http://www.streamreader.org/superuser/questions/91699/spoof-mac-address-from-ip-command
    "el último bit del primer byte a 0"
  [aleatoria]: {filename}/dev/random-bash.md
    "aleatoriedad en bash"
