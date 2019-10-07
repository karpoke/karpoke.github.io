Title: Crear un repositorio espejo de Ubuntu
Date: 2014-05-18 21:48
Author: Nacho Cano
Tags: apache2, apt, apt-mirror, repositorio espejo, ubuntu
Slug: crear-un-repositorio-espejo-de-ubuntu
Related: cache-de-paquetes-descargados-en-ubuntu-trusty-tahr

Si tenemos un gran número de equipos con Ubuntu en nuestra LAN, nos
puede interesar tener un espejo local del repositorio de paquetes de
Ubuntu. Una diferencia entre esta opción y [utilizar un _proxy/caché_ de
paquetes][] es que, en el primer caso, ya tendremos todos los paquetes
disponibles cuando los vayamos a necesitar.


Clonar el repositorio en local
------------------------------

Para crear un repositorio local, podemos usar el comando `apt-mirror`,
disponible en los repositorios. Una vez instalado, podemos editar el
fichero de configuración en `/etc/apt/mirror.list` para, por ejemplo,
cambiar el directorio donde se guardarán los paquetes (por defecto
`/var/spool/apt-mirror`), añadir o eliminar fuentes a incluir en el
repositorio, etc. Con las fuentes por defecto, hay que tener en cuenta
que serán necesarios más de 100 GB para alojar el repositorio. Si
optásemos sólo por incluir el "main", se queda en 10 GB.

Luego, lo ejecutamos:

```bash
$ sudo apt-mirror

Downloading 162 index files using 20 threads...
Begin time: Sat May 17 12:31:22 2014
[20]... [19]... [18]... [17]... [16]... [15]... [14]... [13]... [12]... [11]... [10]... [9]... [8]... [7]... [6]... [5]... [4]... [3]... [2]... [1]... [0]...
End time: Sat May 17 12:32:02 2014

Processing tranlation indexes: [TTT]

Downloading 185 translation files using 20 threads...
Begin time: Sat May 17 12:32:02 2014
[20]... [19]... [18]... [17]... [16]... [15]... [14]... [13]... [12]... [11]... [10]... [9]... [8]... [7]... [6]... [5]... [4]... [3]... [2]... [1]... [0]...
End time: Sat May 17 12:33:13 2014

Processing indexes: [SSSPPP]

110.1 GiB will be downloaded into archive.
Downloading 111238 archive files using 20 threads...
Begin time: Sat May 17 12:33:28 2014
[20]...
```

### Actualizar el repositorio local

Para mantener el repositorio actualizado, bastará editar el fichero de
configuración del `cron` para que se ejecute periódicamente:

```bash
$ sudo vim /etc/cron.d/apt-mirror
0 4 * * * apt-mirror /usr/bin/apt-mirror > /var/spool/apt-mirror/var/cron.log
```

### Actualizaciones del propio servidor

Si queremos que el propio servidor utilice el espejo local, deberemos
cambiar las fuentes del `/etc/apt/sources.list` para que, en lugar de
consultar el repositorio remoto, consulte el fichero local. Algo, así:

```bash
#deb http://archive.ubuntu.com/ubuntu/ trusty main universe
deb file:/var/spool/apt-mirror/mirror/archive.ubuntu.com/ubuntu trusty main universe
```

### Configurar el servidor web

Por último, sólo queda que el repositorio sea accesible para los
clientes a través del servidor web. En este caso, crearemos un nuevo
_host_ virtual para Apache2, por ejemplo,
`/etc/apache2/sites-available/deb.example.com.conf`:

```bash
ServerName deb.example.com
DocumentRoot /var/spool/apt-mirror/mirror/archive.ubuntu.com

Options Indexes FollowSymLinks MultiViews
AllowOverride Limit Options FileInfo Indexes
Require all granted

ErrorLog ${APACHE_LOG_DIR}/deb.example.com-error.log
CustomLog ${APACHE_LOG_DIR}/deb.example.com-access.log combined

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```

Lo activamos y reiniciamos apache:

```bash
$ sudo a2ensite deb.example.com.conf
$ sudo apache2ctl configtest && sudo apache2ctl graceful
```

Si todo ha ido bien, veremos dos directorios listados en la URL
http://deb.example.com/ubuntu/.

### Configuración de los clientes

Para que el resto de equipos comiencen a utilizar el repositorio local,
deberemos editar el fichero de fuentes (`/etc/apt/sources.list`) y
sustituir las que había por las del repositorio que acabamos de crear:

```bash
#deb http://archive.ubuntu.com/ubuntu/ trusty main universe
deb http://deb.example.com/ubuntu/ trusty main universe
```

Como comentario, las fuentes relativas a actualizaciones de seguridad
las dejaría como está, para que se sigan descargando desde los
repositorios originales:

```bash
deb http://security.ubuntu.com/ubuntu trusty-security main restricted universe multiverse
```

Sólo resta actualizar la lista de paquetes disponibles:

```bash
$ sudo aptitude update
```

Referencias
-----------

» [Creating an Ubuntu repository mirror with apt-mirror][]

  [utilizar un _proxy/caché_ de paquetes]: {filename}/admin/cache-de-paquetes-descargados-en-ubuntu-trusty-tahr.md
    "Caché de paquetes descargados en Ubuntu Trusty Tahr"
  [Creating an Ubuntu repository mirror with apt-mirror]: http://popey.com/blog/2006/10/24/creating_an_ubuntu_repositoryespejowith_apt-mirror/
    "Creating an Ubuntu repository mirror with apt-mirror"
