Title: Caché de paquetes descargados en Ubuntu Trusty Tahr
Date: 2014-05-17 01:30
Author: Nacho Cano
Tags: 14.04, apt-cacher, apt-cacher-ng, aptproxy, cache, proxy, ubuntu trusty tahr, ufw, w3m
Slug: cache-de-paquetes-descargados-en-ubuntu-trusty-tahr

Si tenemos una LAN con varios equipos, podemos utilizar `apt-cacher-ng`
para no tener que descargar las actualizaciones desde los repostiorios
en cada uno de ellos, ya que nos permite reutilizar los paquetes que
hayamos descargado. Otras opciones, como AptProxy parece que han quedado
algo obsoletas.

`apt-cacher-ng` es un _proxy/caché_ enfocado a gestores de paquetes, que
soporta las distribuciones Debian y Ubuntu, entre otras. Es una buena
alternativa a montar un espejo para pequeñas LANs.


Servidor
--------

El equipo en que se instale es el que hará de servidor y el resto serán
los clientes. Se puede instalar desde los repositorios. Una vez
instalado, editaremos el fichero `/etc/services` para añadir los puertos
que utiliza (esto no será útil cuando, por ejemplo, analicemos el
tráfico de red):

```bash
# Local services
apt-cacher-ng   3142/tcp
apt-cacher-ng   3142/udp
```

Para arrancar el servicio:

```bash
$ sudo service apt-cacher-ng start
```

Si tenemos un cortafuegos activo, deberemos abrir dicho puerto. Por
ejemplo, si usamos `ufw`:

```bash
$ sudo ufw allow from 192.168.0.0/24 to any port 3142
```

Podemos importar los paquetes que ya tengamos descargados. Tal como
sugiere la documentación en la página de mantenimiento, creamos el
directorio `_import`, añadimos un enlace simbólico a la caché de
paquetes de `apt` y pulsamos en el botón de importar:

```bash
$ cd /var/cache/apt-cacher-ng/
$ sudo mkdir _import
$ sudo chown apt-cacher-ng:apt-cacher-ng _import/
$ cd _import/
$ sudo ln -s /var/cache/apt/archives
```

Ahora sólo queda pulsar en el botón de Importar, o visitar el siguiente
enlace:

```bash
$ w3m "http://192.168.0.50:3142/acng-report.html?abortOnErrors=aOe&doImport=Start+Import&calcSize=cs&asNeeded=an#bottom"
```

Clientes
--------

En los clientes, lo único que hay que hacer es añadir un archivo de
configuración para apt, por ejemplo `/etc/apt/apt.conf.d/02proxy` que
apunte al servidor:

```bash
Acquire::http::Proxy "http://192.168.0.50:3142";
```

192.168.0.50 es la IP del servidor, aunque también podríamos poner un
nombre de dominio.

Sólo queda actualizar los paquetes:

```bash
$ sudo aptitude update
```

Mantenimiento
-------------

En la URL http://192.168.0.50:3142/acng-report.html nos muestra una
página donde se pueden ver algunas estadísticas y realizar algunas
acciones, como vaciar la caché.

Referencias
-----------

- [apt-cacher-ng][]
- [Apt-Cacher-NG User Manual][]
- [Install Apt-Cacher-NG – Ubuntu][]

  [apt-cacher-ng]: http://alioth.debian.org/projects/apt-cacher-ng/
    "apt-cacher-ng"
  [Apt-Cacher-NG User Manual]: http://www.unix-ag.uni-kl.de/~bloch/acng/html/index.html
    "Apt-Cacher-NG User Manual"
  [Install Apt-Cacher-NG – Ubuntu]: http://www.distrogeeks.com/install-apt-cacher-ng-ubuntu/
    "Install Apt-Cacher-NG – Ubuntu"
