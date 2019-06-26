Title: Robando la identidad del vecino
Date: 2010-12-18 21:22
Author: Nacho Cano
Tags: blacksheep, firesheep, robo de identidad
Slug: robando-la-identidad-del-vecino

[Firesheep][] es un complemento para Firefox que permite [robar la
identidad][] de los usuarios de diferentes redes sociales ([Dropbox][],
[Facebook][], Flickr, [Google][], Twitter, Windows Live,
[Wordpress][]...) que se encuentren conectados a la misma red que el
ladrón. La mejor manera de [evitarlo][] es cifrar el tráfico, por
ejemplo utilizando [HTTPS-everywhere][], otro complemento para Firefox.

![HTTPS Everywhere prefs]({static}/images/https-everywhere-prefs-300x110.png)

Poco después surgió [Blacksheep][], otro complemento más, que nos alerta
si un usuario de la misma red está utilizando FireSheep.

Tanto Firesheep como Blacksheep no están disponibles para Firefox en
GNU/Linux desde el menú de complementos de Firefox, pero podemos
instalarlo si [recompilamos la extensión][]. El ejemplo en el enlace
anterior está pensado para CentOS, pero para Ubuntu Maverick Merkat es
prácticamente igual:


Blacksheep para Firefox en Ubuntu Maverick Meerkat
--------------------------------------------------

Se requiere:

```bash
$ sudo aptitude install autoconf libpcap-dev xulrunner-dev libboost-dev libhal-dev
```

En Ubuntu no habrá problemas con la versión de `autoconf`, ya que es
superior a la 2.61:

```bash
$ autoconf -V
```

```bash
autoconf (GNU Autoconf) 2.67
```

Ni con la de `libpcap-dev`, ya que viene la 1.1.1-2:

```bash
$ aptitude show libpcap-dev
```

```bash
Paquete: libpcap-dev
Estado: instalado
Instalado automáticamente: no
Versión: 1.1.1-2
```

Suponemos que vamos a trabajar en el directorio de usuario. Tenemos que
compilar el _back-end_ de Firesheep. Lo primero será bajarnos el código
de Firesheep:

```bash
$ git clone git://github.com/mickflemm/firesheep.git
```

Y ahora lo compilamos:

```bash
$ cd firesheep
$ git submodule update --init
$ ./autogen.sh --with-xulrunner-sdk=/usr/lib/xulrunner-devel-1.9.2.13/
$ make
```

Vamos a comprobar que el _backend_ funciona correctamente:

```bash
$ cd xpi/platform/Linux_x86-gcc3/
$ sudo ./firesheep-backend --fix-permissions
$ ./firesheep-backend --list-interfaces
```

Nos devuelve algo como:

```bash
{"eth0":{"name":"Networking Interface","type":"ethernet"},
"eth2":{"name":"WLAN Interface","type":"ethernet"},
"lo":{"name":"Loopback device Interface","type":"ethernet"}}
```

Para comprobar que podemos capturar paquetes ejecutamos:

```bash
$ ./firesheep-backend eth2 "tcp port 80"
```

Abrimos una página de internet, o en otra consola ejecutamos algo como:

```bash
$ wget http://www.zscaler.com/
```

Si todo va bien, nos empezará a devolver cosas como:

```bash
{"from":"192.168.0.32:49670",
"to":"72.249.144.174:80",
"method":"GET",
"path":"/",
"query":"",
"host":"www.zscaler.com",
"cookies":"",
"userAgent":"Wget/1.12 (linux-gnu)"}
```

Ahora vamos a incluir el _back-end_ en el complemento BlackSheep:

```bash
cd ~
wget http://www.zscaler.com/research/plugins/firefox/blacksheep/blacksheep-latest.xpi
mkdir blacksheep
unzip blacksheep-latest.xpi -d blacksheep/
cd blacksheep
cp -r ../firesheep/xpi/platform/* platform/
```

Del archivo `install.rdf`, borraremos las líneas:

```xml
Darwin_x86-gcc3
WINNT_x86-msvc
em:updateURL="http://www.zscaler.com/research/plugins/firefox/blacksheep/update.rdf"
```

La última línea es para evitar las actualizaciones automáticas.

Ahora ya podemos crear el `.xpi`:

```bash
$ zip blacksheep-latest-linux.xpi -r *
```

Lo instalamos y reiniciamos Firefox. Nos pedirá permisos de
administrador para poder ejecutar el complemento. Introducimos la
contrseña y listos. Como corolario, he subido el [complemento][] al
[directorio público][].

![Blacksheep prefs]({static}/images/blacksheep-preferences.png)

Firesheep para Firefox en Ubuntu Maverick Meerkat
-------------------------------------------------

Dado que ya nos hemos bajado el código de Firesheep y lo hemos
compilado, tenemos disponible el `.xpi` en el directorio
`~/firesheep/build/firesheep.xpi`. También se encuentra disponible en el
directorio [público][complemento].

Después de instalarlo, será necesario darle permisos manualmente para
que detecte las interfaces:

```bash
$ cd ~/.mozilla/firefox/ygqde9s7.default/extensions/firesheep@codebutler.com/platform/Linux_x86-gcc3/
$ sudo ./firesheep-backend --fix-permissions
```

![Firesheep websites]({static}/images/firesheep-websites-300x227.png)

El menú de Firesheep es accesible a través del panel lateral: *Ver /
Panel lateral / Firesheep* o `Ctrl+Shft+s`.

  [Firesheep]: http://codebutler.com/firesheep "firesheep"
    "Firesheep"
  [robar la identidad]: http://alt1040.com/2010/10/firesheep-facebook-google-twitter-windows-live-wordpress-google
    "robar la identidad"
  [Dropbox]: {filename}/admin/como-publicar-directorios-en-ubuntu-one-y-dropbox.md
    "Dropbox"
    "cómo publicar directorios en ubuntu one y dropbox"
  [Facebook]: {filename}/hack/senoras-que-se-ponen-un-nombre-falso-en-facebook-pero-usan-su-direccion-de-correo-personal.md
    "Facebook"
    "señoras que se ponen un nombre falso en facebook pero usan su dirección de correo personal"
  [Google]: {filename}/hack/csrf-en-las-busquedas-de-google.md
    "Google"
    "csrf en las búsquedas de google"
  [Wordpress]: {filename}/admin/la-infame-actualizacion-de-wordpress-en-15-segundos.md
    "Wordpress"
    "la infame actualización de wordpress en 15 segundos"
  [evitarlo]: http://alt1040.com/2010/11/como-protegerse-de-firesheep
    "evitarlo"
  [HTTPS-everywhere]: http://www.eff.org/https-everywhere
    "HTTPS-everywhere"
    "https everywhere"
  [Blacksheep]: http://www.zscaler.com/blacksheep.html "blacksheep"
    "Blacksheep"
  [recompilamos la extensión]: http://research.zscaler.com/2010/11/blacksheep-for-linux.html
    "recompilamos la extensión"
  [complemento]: http://ubuntuone.com/p/NoU/
    "complemento"
  [directorio público]: {filename}/admin/como-publicar-directorios-en-ubuntu-one-y-dropbox.md
    "directorio público"
