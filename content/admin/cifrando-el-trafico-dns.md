Title: Cifrando el tráfico DNS
Date: 2013-01-17 19:44
Author: Nacho Cano
Tags: cloudns, dig, dns, dnscrypt, dnscrypt-proxy, dnssec, drill, gpg, importar claves públicas, ldnsutils, mitm, nslookup, opendns, opennic, phishing, proxy, unbound, verificar un paquete firmado
Slug: cifrando-el-trafico-dns
Related: hphosts-evitando-la-navegacion-por-dominios-maliciosos,saltandonos-el-portal-cautivo-de-una-biblioteca,utilizar-ssh-para-establecer-un-servidor-proxy-socks,encontrar-los-dominios-que-comparten-ip-con-otro-dado,tunel-ssh-inverso,sslh-compartiendo-el-puerto-443,ssh-over-http-proxy

[DNSCrypt][] proporciona un servicio local para resolver nombres de
dominio que permite cifrar el tráfico entre nuestro equipo y el servidor
DNS primario, por defecto OpenDNS, lo que ayuda a protegerse de ataques
MitM y _phishing_ y proporciona cierta confidencialidad en las
peticiones DNS.


Instalación
-----------

Para instalarlo, basta que nos decarguemos el paquete con el código
fuente:

    $ wget http://download.dnscrypt.org/dnscrypt-proxy/dnscrypt-proxy-1.2.0.tar.bz2
    $ wget http://download.dnscrypt.org/dnscrypt-proxy/dnscrypt-proxy-1.2.0.tar.bz2.sig

Comprobamos el paquete:

    $ gpg --verify dnscrypt-proxy-1.2.0.tar.bz2.sig dnscrypt-proxy-1.2.0.tar.bz2
    gpg: Firmado el vie 12 oct 2012 01:28:27 CEST usando clave DSA ID 1CDEA439
    gpg: Imposible comprobar la firma: Clave pública no encontrada

Para poder comprobar la firma, buscamos la clave y la añadimos:

    $ gpg --search-keys 1CDEA439
    gpg: buscando ;`1CDEA439;' de hkp servidor keys.gnupg.net
    (1) Jedi/Sector One
        Frank DENIS (Jedi/Sector One)
        Frank DENIS (Jedi/Sector One) <0daydigestATpureftpd.org>
          1024 bit DSA key 1CDEA439, creado: 2002-03-10
    Keys 1-1 of 1 for "1CDEA439".  Introduzca número(s), O)tro, o F)in > 1
    gpg: solicitando clave 1CDEA439 de hkp servidor keys.gnupg.net
    gpg: clave 1CDEA439: clave pública "Jedi/Sector One " importada

Ahora volvemos a realizar la comprobación:

    $ gpg --verify dnscrypt-proxy-1.2.0.tar.bz2.sig dnscrypt-proxy-1.2.0.tar.bz2
    gpg: Firmado el vie 12 oct 2012 01:28:27 CEST usando clave DSA ID 1CDEA439
    gpg: Firma correcta de ;`Jedi/Sector One ;'
    gpg:                 alias ;`Frank DENIS (Jedi/Sector One) ;'
    gpg:                 alias ;`Frank DENIS (Jedi/Sector One) <0daydigestATpureftpd.org>;'
    gpg: AVISO: ¡Esta clave no está certificada por una firma de confianza!
    gpg:          No hay indicios de que la firma pertenezca al propietario.
    Huellas dactilares de la clave primaria: 89F7 B830 0E87 E03C 52B0  5289 926B C517 1CDE A439

Descomprimimos el paquete y lo compilamos:

    $ tar xvjf dnscrypt-proxy-1.2.0.tar.bz2
    $ cd dnscrypt-proxy-1.2.0
    $ ./configure
    $ make -j2

Antes de instalarlo podemos realizar algunos tests:

    $ cd src/libnacl
    $ make -j2 test
    $ cd ../..

Lo instalamos:

    $ sudo make install

Uso
---

La forma más sencilla de utilizarlo es ejecutar:

    $ sudo dnscrypt-proxy --daemonize

Acto seguido modificamos la dirección IP del servidor DNS en los
parámetros de la conexión. Podemos editar el fichero `/etc/resolv.con` y
poner:

    nameserver 127.0.0.1

Si vemos un aviso dentro del fichero que nos dice que los cambios no
serán permanentes, y queremos que lo sean, deberemos modificar la IP del
servidor DNS desde la configuración de la red en propiedades del
sistema.

Probamos que el servicio funciona:

    $ dig opendns.com

    ; <<>> DiG 9.8.1-P1 <<>> opendns.com
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 630
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 8192
    ;; QUESTION SECTION:
    ;opendns.com.           IN  A

    ;; ANSWER SECTION:
    opendns.com.        30  IN  A   67.215.92.211

    ;; Query time: 91 msec
    ;; SERVER: 127.0.0.1#53(127.0.0.1)
    ;; WHEN: Thu Jan 17 17:35:51 2013
    ;; MSG SIZE  rcvd: 56

    $ nslookup opendns.com
    Server:     127.0.0.1
    Address:    127.0.0.1#53
    Non-authoritative answer:
    Name:   opendns.com
    Address: 67.215.92.211

    $ nslookup opendns.com localhost
    Server:     localhost
    Address:    127.0.0.1#53
    Non-authoritative answer:
    Name:   opendns.com
    Address: 67.215.92.211

    $ drill opendns.com
    ;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 31633
    ;; flags: qr rd ra ; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0
    ;; QUESTION SECTION:
    ;; opendns.com. IN  A

    ;; ANSWER SECTION:
    opendns.com.    23  IN  A   67.215.92.211

    ;; AUTHORITY SECTION:

    ;; ADDITIONAL SECTION:

    ;; Query time: 76 msec
    ;; SERVER: 127.0.0.1
    ;; WHEN: Thu Jan 17 18:43:31 2013
    ;; MSG SIZE  rcvd: 45

`unbound`: caché DNS
--------------------

DNSCrypt únicamente cifra las peticiones DNS hasta nuestro DNS primario,
pero no mantiene una caché de las mismas. Podemos optimizar las
consultas utilizando un sistema de caché DNS como `unbound`. Su
instalación es sencilla, ya que se encuentra en los repositorios.

Una vez instalado, necesitaremos hacer dos cambios.

Primero, ejecutar DNSCrypt en otro puerto, por ejemplo el 40:

    $ sudo dnscrypt-proxy --daemonize --local-address=127.0.0.1:40

Y segundo, configuramos `unbound` para que las consultas sean
redirigidas a través de `dnscrypt-proxy` en ese puerto. Añadimos al
archivo de configuración `/etc/unbound/unbound.conf`:

    username: "unbound"
    directory: "/etc/unbound"
    use-syslog: yes
    do-not-query-localhost: no

    forward-zone:
      name: "."
      forward-addr: 127.0.0.1@40

Comprobamos que la caché funciona correctamente haciendo dos consultas
seguidas al mismo dominio, veremos que la segunda vez tarda 0 ms:

    $ dig opendns.com
    ...
    ;; Query time: 0 msec

* * * * *

#### Actualizado el 15 de septiembre de 2013

Si queremos utilizar otros servidores DNS tenemos algunas alternativas
más:

[ClouDNS][] es un proveedor australiano que admite el cifrado de DNS
para conectarse a sus servidores. Ejecutamos `dnscrypt-proxy`:

    $ sudo dnscrypt-proxy -d -a 127.0.0.1:40 -r 113.20.6.2:443
    $ sudo dnscrypt-proxy -d -a 127.0.0.2:41 -r 113.20.8.17:443

Configuración de `unbound`:

    do-not-query-localhost: no
    forward-zone:
    name: "."
    forward-addr: 127.0.0.1@40
    forward-addr: 127.0.0.2@41

Por otro lado, [OpenNIC project][] nos dice los servidores DNS abiertos
y seguros más cercanos.

* * * * *

#### Actualizado el 10 de mayo de 2014

Para instalar dnscrypt en Ubuntu Trusty Tahr (14.04) necesitaremos
[instalar previamente la librería libsodium][]. Para facilitar la
instalación en varios equipos, [he creado los paquetes `.deb` para
libsodium y dnscrypt][he creado los paquetes .deb para
libsodium y dnscrypt].

* * * * *

### DNSSEC

`unbound` está configurado por defecto para utilizar DNSSEC, pero parece
que [OpenDNS aún no lo soporta][], por lo que deberemos comentar la
siguiente línea en el fichero `/etc/unbound/unbound.conf`:

    auto-trust-anchor-file: "/var/lib/unbound/root.key"

Sólo queda reiniciar el servicio:

    $ sudo service unbound restart

Referencias
-----------

» [dnscrypt-proxy][]
» [Introducing DNSCrypt (Preview Release)][]
» [Como cifrar el trafico DNS y saltarse algunos filtros de navegacion web implementados por algunos ISP][]

  [DNSCrypt]: https://github.com/opendns/dnscrypt-proxy
    "DNSCrypt"
  [ClouDNS]: https://cloudns.com.au
    "ClouDNS"
  [OpenNIC project]: http://www.opennicproject.org/
    "OpenNIC project"
  [instalar previamente la librería libsodium]: http://askubuntu.com/questions/330589/how-to-compile-and-install-dnscrypt/330611#330611
    "instalar previamente la librería libsodium"
  [he creado los paquetes .deb para libsodium y dnscrypt]: {filename}/admin/crear-paquetes-deb-con-checkinstall.md
    "he creado los paquetes .deb para libsodium y dnscrypt"
  [OpenDNS aún no lo soporta]: http://forums.opendns.com/comments.php?DiscussionID=15361#Item_9
    "OpenDNS aún no lo soporta"
  [dnscrypt-proxy]: http://github.com/opendns/dnscrypt-proxy
    "dnscrypt-proxy"
  [Introducing DNSCrypt (Preview Release)]: http://www.opendns.com/technology/dnscrypt/
    "Introducing DNSCrypt (Preview Release)"
  [Como cifrar el trafico DNS y saltarse algunos filtros de navegacion web implementados por algunos ISP]: http://www.rinconinformatico.net/como-cifrar-el-trafico-dns-y-saltarse-algunos-filtros-de-navegacion-web/
    "Como cifrar el trafico DNS y saltarse algunos filtros de navegacion web implementados por algunos ISP"
