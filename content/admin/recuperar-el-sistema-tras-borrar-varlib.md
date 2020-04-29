Title: Recuperar el sistema tras borrar «/var/lib»
Date: 2014-12-26 21:37
Author: Nacho Cano
Tags: 14.04, apt-get, aptitude, copias de seguridad, dpkg, jerarquía de directorios, mysql, nc, ssh, ubuntu trusty tahr, ufw, virtualbox
Slug: recuperar-el-sistema-tras-borrar-varlib
Related: etckeeper-control-de-versiones-del-directorio-etc,importar-un-volcado-de-datos-en-mysql

Si por casualidad acabamos ejecutando un `rm -fr /var/lib`, tendremos un
pequeño problema. El directorio /var/lib está pensado para que los
programas instalados guarden información variable (ver `man hier`).
Puestos a suponer, supongamos que esto es exactamente lo que acaba de
pasar, que aún no hemos reiniciado la máquina y que seguimos teniendo
acceso por SSH.


Copias de seguridad
-------------------

En este momento, ya es tarde para pensar en copias de seguridad si no
las habíamos hecho antes. Habrá información que hayamos perdido y que
sea imposible recuperar, por ejemplo, [las bases de datos MySQL][].
Probablemente, perderemos información importante para los programas y es
posible que recuperar el sistema en lugar de reinstalar favorezca que
haya toda clase de errores extraños.

Además, tras borrar el directorio `/var/lib`, programas como `dpkg` y
`apt-get` o aptitude no funcionarán, ya que guardan información de los
programas instalados en directorios como `/var/lib/dpkg`, `/var/lib/apt`
o `/var/lib/aptitude`, lo que provoca que la recuperación del sistema
sea tediosa.

Recuperar el instalador
-----------------------

El primer paso es poder ejecutar el instalador de paquetes de nuevo,
para poder reinstalar todos los paquetes. Para esto, partiremos de un
livecd de la misma versión que tengamos instalada y copiaremos el
directorio `/var/lib/dpkg`, en este caso, [Ubuntu Server 14.04.1 de 32
bits][]:

    $ wget http://releases.ubuntu.com/14.04/ubuntu-14.04.1-server-i386.iso

Podemos utilizar `unetbootin` para instalar la distribución en un USB, o
como en este caso, ejecutar una máquina virtual con `virtualbox` y
especificando que el disco contenga esa ISO. Arrancamos la máquina
virtual y seleccionamos el "Modo rescate".

Desde la consola de rescate, copiaremos el contenido del directorio
`/var/lib` a la máquina en la que hemos sufrido el percance, cuya IP
pongamos que sea 192.168.1.100:

    (virtualbox)$ cd /tmp
    (virtualbox)$ tar -cf lib.tar /var/lib
    (virtualbox)$ cat lib.tar | nc 192.168.1.100 9090

En la máquina a reparar debemos ejecutar:

    $ mkdir /tmp/recover
    $ cd /tmp/recover
    $ sudo ufw allow proto tcp from 192.168.50.0/24 to any port 9090
    $ nc -l 9090 | tar x
    $ sudo ufw delete allow proto tcp from 192.168.50.0/24 to any port 9090
    $ sudo chown -R root:root var/lib
    $ sudo mv var/lib /var

Si todo ha ido bien, deríamos poder ejecutar algunos comandos:

    $ sudo dpkg --audit
    $ sudo apt-get update
    $ sudo apt-get check
    $ sudo dpkg --configure -a
    $ sudo apt-get install -f
    $ sudo apt-get upgrade

Reinstalar todos los programas
------------------------------

Podemos encontrar una copia del fichero `/var/lib/dpkg/status` con toda
la información de los paquetes instalados en
`/var/backups/dpkg.status.0`. También podemos revisar el fichero
`/var/log/apt.log` para [reinstalar los últimos paquetes][] añadidos o
eliminados:

    $ /var/tmp/packages0.list
    $ sudo apt-get --reinstall install `cat /var/tmp/packages0.list`

Es posible que algunos paquetes den error debido a alguna depedencia que
no está correctamente instalada, pero conforme se van reinstalando
todos, deberían quedar todos correctamente instalados. Ej:

    E: Couldn't configure pre-depend dpkg:i386 for mountall:i386, probably a dependency cycle.

También iremos viendo avisos como el siguiente, especialmente de
aquellos paquetes que necesitaremos reinstalar:

    dpkg: aviso: falta el fichero de lista de ficheros del paquete `python-lxml', se supondrá que el paquete no tiene ningún fichero actualmente instalado

Una vez que termine, nos aseguramos que [los ficheros base quedaron bien
instalados][]:

    $ sudo apt-get download base-files
    $ sudo apt-get install --reinstall base-files

Recuperar MySQL
---------------

MySQL guarda los ficheros de la base de datos en `/var/lib/mysql/`. Si
tuviéramos una copia, recuperar la base de datos sería tan sencillo como
ejecutar:

    $ mysql -uroot -p < mysql_backup.sql

  [las bases de datos MySQL]: http://dev.mysql.com/doc/refman/4.1/en/installation-layouts.html
    "las bases de datos MySQL"
  [Ubuntu Server 14.04.1 de 32 bits]: http://releases.ubuntu.com/14.04/
    "Ubuntu Server 14.04.1 de 32 bits"
  [reinstalar los últimos paquetes]: http://unix.stackexchange.com/a/123841
    "reinstalar los últimos paquetes"
  [los ficheros base quedaron bien instalados]: http://askubuntu.com/a/383588
    "los ficheros base quedaron bien instalados"
