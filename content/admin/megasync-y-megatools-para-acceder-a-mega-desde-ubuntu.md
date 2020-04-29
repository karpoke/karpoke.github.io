Title: MegaSync y Megatools para acceder a Mega desde Ubuntu
Date: 2015-01-27 21:43
Author: Nacho Cano
Tags: 14.04, apt-key, checkinstall, fuse, gpg, importar claves públicas, ldconfig, libcrypto++9, mega, megadf, megadl, megafs, megaget, megals, megamkdir, megamv, megaput, megareg, megarm, megastream, megasync, megatools, megaupload, nube, ppa, ubuntu trusty tahr, verificar un paquete firmado
Slug: megasync-y-megatools-para-acceder-a-mega-desde-ubuntu
Related: copia-de-seguridad-de-gmail-con-getmail,importar-un-volcado-de-datos-en-mysql,cifrar-el-contenido-de-dropbox,owncloud-con-mysql-en-ubuntu-lucid-lynx-10-04,multiples-cuentas-de-dropbox-en-ubuntu-maverick-meerkat,crear-paquetes-deb-con-checkinstall

El servicio de almacenamiento en la nube de Mega ofrece hasta 50 GB de
espacio gratuito (10 GB de transferencia al mes), cifrado,
multiplataforma, con sincronizado selectivo y está disponible desde el
navegador. Con 50 GB da para guardar algunas copias de seguridad de
nuestros archivos, [correos][] o [bases de datos][].

A continuación, veremos cómo instalar el cliente y acceder desde el
terminal de nuestro servidor.


Instalación en el escritorio
----------------------------

Aunque vayamos a instalarlo en el servidor, no he querido dejar de
comentar la instalación de escritorio, que es realmente sencilla.
Instalamos la librería `libcrypto++9` desde los repositorios y, a
continuación, [descargamos el paquete][], en este caso para Ubuntu
Trusty Tahr 14.04 32 bits, y lo instalamos:

    $ wget https://mega.nz/linux/MEGAsync/xUbuntu_14.04/i386/megasync-xUbuntu_14.04_i386.deb
    $ sudo dpkg -i megasync-xUbuntu_14.04_i386.deb

* * * * *

#### Actualizado el 2 de mayo de 2015

Si al realizar la actualización del sistema nos aparece el error:

    W: Se produjo un error durante la verificación de las firmas. El repositorio no está actualizado y se utilizarán los ficheros de índice antiguos. El error GPG es: http://mega.nz ./ Release: Las firmas siguientes no se pudieron verificar porque su llave pública no está disponible: NO_PUBKEY AC025B14069B6221
    W: Fallo al renombrar http://mega.nz/linux/MEGAsync/xUbuntu_14.10/./Release:
    W: Algunos archivos de índice fallaron al descargar. Se han ignorado, o se han utilizado unos antiguos en su lugar

Comprobamos si está disponible la clave:

    $ gpg --keyserver keyserver.ubuntu.com --recv-keys AC025B14069B6221
    gpg: solicitando clave 069B6221 de hkp servidor keyserver.ubuntu.com
    gpg: clave 069B6221: «MEGAsync OBS Project » sin cambios
    gpg: Cantidad total procesada: 1
    gpg:              sin cambios: 1

Y la actualizamos:

    $ sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com AC025B14069B6221

Ahora ya podremos actualizar normalmente.

* * * * *

Hay que tener en cuenta que nuestra contraseña se utiliza para cifrar el
contenido, por lo que si la perdemos, lo perdemos todo. Cabe recordar
que también tenemos la opción de [exportar la clave principal][] y
tenerla a buen recaudo.

Instalación en el servidor
--------------------------

Si queremos instalarlo en nuestro servidor, podemos recurrir a las
[megatools][] desde el [repositorio][megatools] y compilarlas, o bien
hacerlo desde el [PPA][], aunque éste último [ya no está mantenido][]
desde Quantal.

Lo que haremos esta vez será bajar una de las [compilaciones ya
preparadas][]:

    $ wget http://megatools.megous.com/builds/megatools-1.9.94.tar.gz
    $ wget http://megatools.megous.com/builds/megatools-1.9.94.tar.gz.asc

* * * * *

#### Actualizado el 26 de abril de 2015

Lo había dado por hecho, pero no está demás comentar que es altamente
recomendable que comprobemos la firma:

    $ gpg --verify megatools-1.9.94.tar.gz.asc
    gpg: Signature made vie 02 ene 2015 08:43:50 CET using DSA key ID A7BB2AC1
    gpg: Can’t check signature: public key not found

En este caso, aún no la tenemos, así que la buscamos, y tras confirmar
que corresponde al [creador del paquete][megatools], la instalamos:

    $ gpg --search-keys A7BB2AC1
    gpg: searching for "A7BB2AC1" from hkp server keys.gnupg.net
    (1) Ondrej Jirman
          1024 bit DSA key A7BB2AC1, created: 2003-08-24
    Keys 1-1 of 1 for "A7BB2AC1".  Enter number(s), N)ext, or Q)uit > 1
    gpg: requesting key A7BB2AC1 from hkp server keys.gnupg.net
    gpg: key A7BB2AC1: public key "Ondrej Jirman " imported
    gpg: Total number processed: 1
    gpg:               imported: 1

Volvemos a comprobar la firma:

    $ gpg --verify megatools-1.9.94.tar.gz.asc
    gpg: Signature made vie 02 ene 2015 08:43:50 CET using DSA key ID A7BB2AC1
    gpg: Good signature from "Ondrej Jirman "
    gpg: WARNING: This key is not certified with a trusted signature!
    gpg:          There is no indication that the signature belongs to the owner.
    Primary key fingerprint: D79E 2F84 317E 26CE 8EFD  A605 BF23 1000 A7BB 2AC1

La criticidad del aviso dependerá de la confianza que pongamos en la
clave pública. Lo ideal sería que hubiéramos recibido la clave
directamente de mano del propietario, pero por lo general se suele bajar
de internet. En este caso, considero que la probabilidad de que la clave
descargada haya sido modificada es prácticamente nula, así que
procedemos confiadamente.

* * * * *

Descomprimimos el paquete:

    $ tar xzvf megatools-1.9.94.tar.gz
    $ cd megatools-1.9.94

Instalamos las dependencias:

    $ sudo aptitude install build-essential libglib2.0-dev libssl-dev libgirepository1.0-dev libcurl4-gnutls-dev glib-networking

He probado `libcurl4-gnutls-dev` en lugar de `libcurl4-openssl-dev` y
parece que no hay problemas.

Instalamos:

    $ ./configure
    $ make
    $ sudo make install  # o sudo checkisntall

Uso
---

Si aún no habíamos resgistrado la cuenta desde la web, podemos hacerlo
con el comando `megareg`.

* * * * *

Si nos aparece un error como el siguiente:

</p>
    megareg: error while loading shared libraries: libmega.so.0: cannot open shared object file: No such file or directory

es que las librerías no están preparadas para utilizarse. Lo resolvemos
ejecutando:

    $ sudo ldconfig

* * * * *

Comandos disponibles:

      megareg      Register and verify a new mega account
      megadf       Show your cloud storage space usage/quota
      megals       List all remote files
      megamkdir    Create remote directory
      megarm       Remove remote file or directory
      megamv       Move and rename remote files
      megaput      Upload individual files
      megaget      Download individual files
      megadl       Download file from a "public" Mega link
                   (doesn't require login)
      megastream   Streaming download of a file
                   (can be used to preview videos or music)
      megasync     Upload or download a directory tree
      megafs       Mount remote filesystem locally.

Por ejemplo, para comprobar el espacio disponible:

    $ megadf -u john@example.com -p password
    Total: 53687091200
    Used:  0
    Free:  53687091200

Para no tener que escribir el usuario y la contraseña en la terminal,
podemos crear el siguiente archivo de configuración (ver `man megarc`):

    $ cat ~/.megarc
    [Login]
    Username = john@example.com
    Password = password

Creamos un directorio remoto:

    $ megamkdir /Root/test  # el prefijo /Root es necesario. ver `man megatools`

Subir un archivo:

    $ megaput file.txt   # se sube a /Root
    $ megaput --path /Root/test file.txt

Subir varios archivos en [paralelo][]:

    $ ls file*.txt | xargs -n1 -P4 megaput

Para sincronizar el directorio `/home/user/mega` con el directorio que
acabamos de crear, podemos subir el directorio:

    $ megasync -l /home/user/mega -r /Root/test

O descargarlo:

    $ megasync -l /home/user/mega -r /Root/test --download

Si habíamos eliminado algún fichero y no se descarga, podemos limpiar la
caché utilizando el argumento `--reload`.

Un problema con la sincronización es que los archivos que hayamos
eliminado a través de otro canal, por ejemplo accediendo a través del
navegador, no se borrarán en nuestro servidor local. Para remediarlo,
podemos consultar los ficheros que no están en el servidor y borrarlos:

    $ megasync --reload -n -l /home/user/mega -r /Root/test 2>/dev/null | sed 's|F /Root/test|/home/user/mega|' | xargs -0 rm

Cifrado del directorio
----------------------

Una buena idea sería sincronizar un [directorio cifrado][]. De esta
forma, no tendríamos que confiar en que nuestros archivos estén
realmente cifrados en los servidores de Mega.

En el siguiente artículo, podemos ver [cómo cifrar un directorio en Mega
con `encfs`][cómo cifrar un directorio en Mega con encfs].

  [correos]: {filename}/admin/copia-de-seguridad-de-gmail-con-getmail.md
    "correos"
  [bases de datos]: {filename}/admin/importar-un-volcado-de-datos-en-mysql.md
    "bases de datos"
  [descargamos el paquete]: https://mega.co.nz/#sync!linux
    "descargamos el paquete"
  [exportar la clave principal]: https://mega.co.nz/#backup
    "exportar la clave principal"
  [megatools]: https://github.com/megous/megatools
    "megatools"
  [PPA]: https://launchpad.net/~megous/+archive/ubuntu/ppa
    "PPA"
  [ya no está mantenido]: http://aplicacionesysistemas.com/feed/
    "ya no está mantenido"
  [compilaciones ya preparadas]: http://megatools.megous.com/builds
    "compilaciones ya preparadas"
  [paralelo]: http://www.exvagos.com/showthread.php?t=530204
    "paralelo"
  [directorio cifrado]: {filename}/admin/cifrar-el-contenido-de-dropbox.md
    "directorio cifrado"
  [cómo cifrar un directorio en Mega con encfs]: {filename}/admin/cifrar-un-directorio-sincronizado-en-mega-con-encfs.md
    "Cifrar un directorio sincronizado en Mega con encfs"
