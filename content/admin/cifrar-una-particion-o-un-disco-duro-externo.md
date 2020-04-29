Title: Cifrar una partición o un disco duro externo
Date: 2011-07-08 02:48
Author: Nacho Cano
Tags: AES, badblocks, cifrado, cryptsetup, dd, disco duro, luks, mount, partición, sha-256, shred, tamaño de bloque, tune2fs, umount
Slug: cifrar-una-particion-o-un-disco-duro-externo

Tenemos [un disco duro externo y queremos cifrarlo][]. El comando
`cryptsetup`, que se encuentra en los repositorios, hace uso de
DM-Crypt, que es la parte del kernel que se encarga del cifrado de
discos, y LUKS, un estándar independiente de la plataforma y del
software para acceder a volúmenes cifrados.


Requisitos
----------

El primer paso, después de instalar el comando, es tener claro qué
dispositivo es nuestro disco duro. Un vistazo mediante `fdisk` debería
ser suficiente. Además, si está montado, lo desmontamos.

Vamos a comprobar que el disco no tiene errores. Primero, averiguamos el
tamaño de bloque:

    $ sudo tune2fs -l /dev/sdb1 | grep -i 'Block size'
    Block size:               4096

Lanzamos el comando `badblocks` para comprobar los errores:

    $ sudo badblocks -s -w /dev/sdb1 -b 4096

Este comando se dedica a escribir una serie de patrones en el disco y
después leerlos para asegurarse de que no hay problemas, y por este
motivo es muy lento. Con el argumento `-t` se utiliza una sola pasada con
un patrón [aleatorio][]: más rápido pero menos preciso.
    "aleatorio]["

El siguiente paso es llenar el disco de datos aleatorios para protegerse
de ataques criptográficos. El siguiente comando realiza 3 pasadas sobre
el disco:

    $ sudo shred -n 3 -v /dev/sdb1

El número de pasadas dependerá de la paranoia de cada uno. En lugar de
`shred`, que toma los datos pseudoaleatorios de `/dev/urandom`,
podríamos utilizar `dd`, que es realmente aleatorio ya que los toma de
`/dev/random`, y también tarda más:

    $ sudo dd if=/dev/random of=/dev/sdb1 bs=4096

Cifrado
-------

Ya estamos listos para cifrar la partición:

    $ sudo cryptsetup --verify-passphrase -c aes -h sha256 -y -s 256 luksFormat /dev/sdb1

Las opciones pasadas indican que pida la contraseña dos veces, un
cifrado AES con clave de 256 bits y algoritmo SHA-256. Si nos da el
error:

    Check kernel for support for the aes-cbc-plain cipher spec and verify that /dev/sdb6 contains at least 258 sectors

es que debemos cargar el módulo `dm-crypt`:

    $ sudo modprobe dm-crypt

Para que se cargue cada vez que arranque el sistema, nos aseguramos de
que el fichero `/etc/modules` contiene la línea:

    dm-crypt

Particionado
------------

Para montar la interfaz al disco cifrado ejecutamos:

    $ sudo cryptsetup luksOpen /dev/sdb1 crypthd

Esto no es lo mismo que montar el disco. Este comando crea un
dispositivo que hará de interfaz al disco cifrado y que se encuentra en
`/dev/mapper/crypthd`. El nombre `crythd` lo escogemos nosotros.

Formateamos:

    $ sudo mkfs.ext4 -L crypthd -m 1 /dev/mapper/cryptd

Con el argumento `-L` especificamos la etiqueta para la unidad, con lo que
al montarlo automáticamente se utilizará este nombre. El argumento `-m` es
el tanto por cierto de espacio reservado para el administrador.

Para desmontar la interfaz:

    $ sudo cryptsetup luksClose /dev/mapper/crypthd

Montando y desmontando
----------------------

### En el terminal

Para usar el disco, primero hay que montar la interfaz y luego el disco.
Suponemos que el directorio `/media/crypthd` ya ha sido creado. También
cambiaremos los permisos para que pueda ser usado por nuestro usuario:

    $ sudo cryptsetup luksOpen /dev/sdb1 crypthd
    $ sudo mount /dev/mapper/crypthd /media/crypthd
    $ sudo chown -R $USER:$USER /media/crypthd

Para desmontar el disco hay que hacerlo en el orden inverso:

    $ sudo umount /media/crypthd
    $ sudo cryptsetup luksClose /dev/mapper/crypthd

### En el escritorio

Si lo usamos en un entorno de escritorio, podemos aprovecharnos de que
el disco se montará automáticamente. No será necesario haber creado el
directorio `/media/crypthd` por lo que, con el disco desmontado, lo
podemos borrar.

Cada vez que conectemos el disco nos saldrá el cuadro de diálogo que nos
pedirá la contraseña para montar la inferfaz al disco y si introducimos
la correcta, lo montará en el directorio esperado.

![Disco cifrado con contraseña]({static}/images/contrasena-disco-cifrado-300x204.png)

La primera vez que lo montemos de esta manera, habrá que modificar los
permisos del directorio para que tengamos permisos de escritura:

    $ sudo chmod 775 /media/crypthd
    $ sudo chgrp adm /media/crypthd

  [un disco duro externo y queremos cifrarlo]: http://conocimientoabierto.es/traducir-automaticamente-ficheros-po/207/
    "un disco duro externo y queremos cifrarlo"
  [aleatorio]: {filename}/dev/random-bash.md
    "random bash"
