Title: Cifrar un directorio sincronizado en Mega con encfs
Date: 2015-01-28 23:54
Author: Nacho Cano
Tags: AES, cifrado, encfs, fstab, mega, mount, script, umount
Slug: cifrar-un-directorio-sincronizado-en-mega-con-encfs
Related: megasync-y-megatools-para-acceder-a-mega-desde-ubuntu,cifrar-el-contenido-de-dropbox

Ya tenemos cuenta en Mega y las [`megatools` instaladas][megatools instaladas].
Ahora vamos a cifrar el directorio, pero en lugar de [utilizar `ecrypt` tal como
hicimos con Dropbox][utilizar ecrypt tal como hicimos con Dropbox],
esta vez usaremos `encfs`.

Suponemos que tenemos dos directorios, `~/mega` y `~/mega.enc`.
Utilizaremos `encfs`, disponible en los repositorios, para cifrar el
contenido del primero en el segundo, y compartir el segundo en Mega.

Creamos el directorio en Mega:

```bash
$ megamkdir /Root/mega.enc
```

Montamos el directorio cifrado:

```bash
$ encfs --reverse /home/user/mega /home/user/mega.enc
Creando nuevo volumen cifrado.
Por favor, elige una de las siguientes opciones:
 pulsa "x" para modo experto de configuracion,
 pulsa "p" para modo paranoia pre-configurado,
 cualquier otra, o una linea vacia elegira el modo estandar.
?> x

Seleccionado modo de configuración Manual.
Los siguientes algoritmos de cifrado estan disponibles:
1. AES : 16 byte block cipher
 -- Soporta claves de longitud 128 hasta 256 bits
 Soporta bloques de tamaño 64 hasta 4096 bytes
2. Blowfish : Cifrado por bloques de 8 bytes
 -- Soporta claves de longitud 128 hasta 256 bits
 Soporta bloques de tamaño 64 hasta 4096 bytes

Teclee el numero correspondiente a su eleccion: 1

Algoritmo seleccionado "AES"

Por favor, elige un tamaño de clave en bits. El cifrado que  has elegido
soporta tamaños desde 128 a 256 bits en incrementos de 64 bits.
Por ejemplo:
128, 192, 256
Tamaño de clave seleccionada: 256

Usando tamaño de clave de 256 bits

Elige un tamaño de bloque en bytes. El cifrado que tu has elegido
soporta tamaños desde 64 a 4096 bytes en incrementos de 16.
O bien, pulsa Intro para elegir el tamaño por defecto (1024 bytes)

Tamaño de bloque del sistema de ficheros: 4096

Usando tamaño de clave de 4096 bits

Los siguientes algoritmos de cifrado de nombres de archivo estan disponibles:
1. Block : Codificación en bloques, oculta tamaño de los nombres de fichero
2. Null : No encryption of filenames
3. Stream : Codificacion en canal, guarda nombres de fichero tan cortos como sea posible.

Teclee el numero correspondiente a su eleccion: 1

Algoritmo seleccionado "Block""

--reverse especificado, no se está usando unique/chained IV

Configuración finalizada. El sistema de ficheros a ser creado tiene
las siguientes propiedades:
Cifrado del sistema de ficheros: "ssl/aes", versión 3:0:2
Codificacion del nombre de fichero: "nameio/block", versión 3:0:1
Tamaño de la llave: 256 bytes
Tamaño de Bloque: 4096 bytes
Agujeros en archivos pasados a través del ciphertext.

Ahora tendrás que introducir una contraseña para tu sistema de ficheros.
Necesitaras recordar esta contraseña, dado que no hay absolutamente
ningún mecanismo de recuperación. Sin embargo, la contraseña puede ser cambiada
más tarde usando encfsctl.

Nueva contraseña Encfs:
Verifique la contraseña Encfs:
```

Si no queremos tener que introducir la contraseña cada vez que montemos
el directorio, podemos un comando que vuelque el contenido de un fichero
con dicha clave, por ejemplo `~/.encfs_passwd`:

```bash
$ encfs --reverse --extpass="cat ~/.encfs_passwd" /home/user/mega /home/user/mega.enc
```

Y sincronizamos:

```bash
$ megasync -l ~/mega.enc -r /Root/mega.enc
```

* * * * *

#### Actualizado el 17 de mayo de 2015

Si queremos que el directorio se monte al inicio, sin necesidad de que
nos pida la contraseña, necesitaremos crear un _script_ que invocaremos
desde el fichero `/etc/fstab`. El motivo es que en el propio fichero
`fstab` no podemos pasarle opciones al comando `encfs`, por lo que
enmascararemos éstas dentro del _script_:

```bash
#!/usr/bin/env bash
/usr/bin/encfs --public --extpass="cat /home/user/.encfs_passwd" --reverse $*
```

Y en el `fstab`:

```bash
/usr/local/bin/encfs.sh#/home/user/mega /home/user/mega.enc fuse rw,user,auto 0 0
```

Si queremos probarlo antes del próximo reinicio, basta que desmontemos
el directorio y utilicemos el comando `mount` para volver a montarlo:

```bash
$ umount /home/user/mega.enc
$ mount /home/user/mega.enc
```

* * * * *

Referencias
-----------

- [Encrypted filesystem on Mega.co.nz][]

  [megatools instaladas]: {filename}/admin/megasync-y-megatools-para-acceder-a-mega-desde-ubuntu.md
    "MegaSync y Megatools para acceder a Mega desde Ubuntu"
  [utilizar ecrypt tal como hicimos con Dropbox]: {filename}/admin/cifrar-el-contenido-de-dropbox.md
    "Cifrar el contenido de Dropbox"
  [Encrypted filesystem on Mega.co.nz]: https://archimedesden.wordpress.com/2013/05/18/encrypted-filesystem-on-mega-co-nz/
    "Encrypted filesystem on Mega.co.nz"
