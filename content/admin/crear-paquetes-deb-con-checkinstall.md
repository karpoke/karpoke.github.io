Title: Crear paquetes .deb con checkinstall
Date: 2014-05-10 18:40
Author: Nacho Cano
Tags: checkinstall, deb, dnscrypt, dpkg, libsodium, rpm
Slug: crear-paquetes-deb-con-checkinstall
Related: cifrando-el-trafico-dns

Una forma sencilla de crear un paquete .deb a partir del código fuente
es mediante la utilidad `checkinstall`, disponible en los respositorios.

Para aquellos casos en los que la compilación del código y la
instalación sigue los conocidos comandos:

```bash
$ ./configure
$ make
$ sudo make install
```

Bastará sustituir el último paso por:

```bash
$ sudo checkinstall
```

Como ejemplo, podemos crear un .deb a partir del código fuente de
[libsodium][], una librería necesaria para compilar dnscrypt.

Descargamos la última versión y comprobamos la firma:

```bash
$ wget https://download.libsodium.org/libsodium/releases/libsodium-0.4.5.tar.gz
$ dig +dnssec +short txt libsodium-0.4.5.tar.gz.download.libsodium.org
"7ad5202df53eeac0eb29b064ae5d05b65d82b2fc1c082899c9c6a09b0ee1ac32"
$ shasum -a 256 libsodium-0.4.2.tar.gz
7ad5202df53eeac0eb29b064ae5d05b65d82b2fc1c082899c9c6a09b0ee1ac32  libsodium-0.4.5.tar.gz
```

(Otra opción sería comprobar el fichero .sig disponible también para
descargar desde su página.)

Descomprimimos el fichero y lo compilamos:

```bash
$ tar xzf libsodium-0.4.5.tar.gz
$ cd libsodium-0.4.5/
$ ./configure
$ make -j2
$ make check
```

Ahora es cuando creamos el paquete .deb:

```bash
$ sudo checkinstall
```

Nos pedirá que añadamos una pequeña descripción del paquete y que
confirmemos una serie de datos relacionados con el mismo. Si quisiéramos
apadrinar un paquete, sería tan sencillo como poner nuestro nombre,
forma de contacto y dirección de descarga.

```bash
checkinstall 1.6.2, Copyright 2009 Felipe Eduardo Sanchez Diaz Duran
           Este software es distribuído de acuerdo a la GNU GPL


The package documentation directory ./doc-pak does not exist.
Should I create a default set of package docs?  [y]: n

Por favor escribe una descripción para el paquete.
Termina tu descripcion con una linea vacia o con EOF.
>> libsodium is an easy-to-use crypto library. Its goal is to provide all of the core operations needed to build higher-level cryptographic tools.
>>

*****************************************
**** Debian package creation selected ***
*****************************************

Este paquete será creado de acuerdo a estos valores:

0 -  Maintainer: [ nacho AT ignaciocano DOT com ]
1 -  Summary: [ libsodium is an easy-to-use crypto library. Its goal is to provide all of the core operations needed to build higher-level cryptographic tools. ]
2 -  Name:    [ libsodium ]
3 -  Version: [ 0.4.5 ]
4 -  Release: [ 1 ]
5 -  License: [ GPL ]
6 -  Group:   [ checkinstall ]
7 -  Architecture: [ i386 ]
8 -  Source location: [ libsodium-0.4.5 ]
9 -  Alternate source location: [  ]
10 - Requires: [  ]
11 - Provides: [ libsodium ]
12 - Conflicts: [  ]
13 - Replaces: [  ]

Introduce un número para cambiar algún dato u oprime ENTER para continuar:
```

Si todo ha ido bien, ya tendremos el paquete creado e instalado. Si
quisiéramos eliminarlo:

```bash
$ sudo dpkg -r libsodium
```

* * * * *

#### Actualizado el 26 de abril de 2015

Si no queremos que se instale justo después de crear el paquete, tenemos
varias [opciones][]:

-   Utilizar el argumento `--install=no`
-   Editar el fichero de configuración `/etc/checkinstallrc` y cambiar
    `INSTALL=1` por `INSTALL=0`

Alternativamente, podemos crear el paquete de forma automatizada,
pasando la información en forma de argumentos. Por ejemplo:

```bash
$ sudo checkinstall
--default
--install=no
--maintainer="nacho AT ignaciocano DOT com"
--pkgname=libsodium
--pkgversion=0.4.5
--pkgrelease=1
--pkglicense=GPL
--pkggroup=checkinstall
--pkgarch=i386
--pkgsource=libsodium-0.4.5
--pkgaltsource=
--requires=
--provides=libsodium
```

La descripción del paquete se toma del contenido del fichero
`description-pak`, que deberemos crear previamente.

Podemos comprobar la información del paquete mediante `dpkg -I` (o
`rpm -qi` si es un `.rpm`):

```bash
$ dpkg -I libsodium_0.4.5-1_i386.deb
 paquete debian nuevo, versión 2.0.
 tamaño 388804 bytes: archivo de control= 383 bytes.
       0 bytes,     0 líneas     conffiles
     332 bytes,     9 líneas     control
 Package: libsodium
 Priority: extra
 Section: checkinstall
 Installed-Size: 2492
 Maintainer: nacho AT ignaciocano DOT com
 Architecture: i386
 Version: 0.4.5-1
 Provides: libsodium
 Description: libsodium is an easy-to-use crypto library. Its goal is to provide all of the core operations needed to build higher-level cryptographic tools.
```

* * * * *

Ya que estamos, también he creado un .deb para dnscrypt. Si queréis
ahorraros el trabajo, aquí tenéis ambos paquetes .deb:

-   [libsodium_0.4.5-1_i386.deb][]
-   [dnscrypt-proxy_1.4.0-1_i386.deb][]

Referencias
-----------

- [Checkinstall, crear paquetes .deb fácilmente a partir del código][]
- [How to compile and install DNScrypt][]
- [Checkinstall README][opciones]

  [libsodium]: https://download.libsodium.org/libsodium/releases/
    "libsodium"
  [opciones]: http://www.asic-linux.com.mx/~izto/checkinstall/docs/README
    "opciones"
  [libsodium_0.4.5-1_i386.deb]: {filename}/deb/libsodium_0.4.5-1_i386.deb
    "libsodium_0.4.5-1_i386.deb"
  [dnscrypt-proxy_1.4.0-1_i386.deb]: {filename}/deb/dnscrypt-proxy_1.4.0-1_i386.deb
    "dnscrypt-proxy_1.4.0-1_i386.deb"
  [Checkinstall, crear paquetes .deb fácilmente a partir del código]: http://ubuntulife.wordpress.com/2010/08/05/checkinstall-crear-paquetes-deb-facilmente-a-partir-del-codigo/
    "Checkinstall, crear paquetes .deb fácilmente a partir del código"
  [How to compile and install DNScrypt]: http://askubuntu.com/questions/330589/how-to-compile-and-install-dnscrypt/330611#330611
    "How to compile and install DNScrypt"
