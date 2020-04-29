Title: Cifrar el contenido de Dropbox
Date: 2011-04-21 13:37
Author: Nacho Cano
Tags: AES, cifrado, dropbox, ecryptfs, fstab, mount, setuid, ssl
Slug: cifrar-el-contenido-de-dropbox
Related: como-publicar-directorios-en-ubuntu-one-y-dropbox

A raíz del cambio en los términos del servicio de Dropbox, en el cual se
afirma que le [entregará tus ficheros al gobierno de Estados Unidos][],
si éste se lo pide, o la noticia de que es posible [saltarse las
restricciones][], y que nuestra cuenta sea usada en otra máquina sin
necesidad de conocer nuestra contraseña, se nos podría ocurrir cifrar
los datos que subimos a nuestra cuenta.

Utilizaremos `ecryptfs` para cifrar un directorio, y todo su contenido,
dentro del directorio de [una de nuestras cuentas de Dropbox][].

![ecryptfs]({static}/images/ecryptfs-300x224.jpg)

_<small>Fuente: [Linux Journal][]</small>_

Supongamos que el directorio Dropbox se encuentra en
`/home/user/.dropbox/Dropbox`. Crearemos dos directorios, uno dentro de
este directorio, con el contenido [cifrado][], y otro fuera, donde lo
montaremos:

    $ mkdir -m 500 ~/ecryptDropbox
    $ mkdir -m 700 ~/.dropbox/Dropbox/ecryptDropbox
    $ sudo mount -t ecryptfs ~/.dropbox/Dropbox/ecryptDropbox ~/ecryptDropbox

    Passphrase:
    Select cipher:
     1) aes: blocksize = 16; min keysize = 16; max keysize = 32 (not loaded)
     2) blowfish: blocksize = 16; min keysize = 16; max keysize = 56 (not loaded)
     3) des3_ede: blocksize = 8; min keysize = 24; max keysize = 24 (not loaded)
     4) twofish: blocksize = 16; min keysize = 16; max keysize = 32 (not loaded)
     5) cast6: blocksize = 16; min keysize = 16; max keysize = 32 (not loaded)
     6) cast5: blocksize = 8; min keysize = 5; max keysize = 16 (not loaded)
    Selection [aes]:

    Select key bytes:
     1) 16
     2) 32
     3) 24
    Selection [16]: 2
        "16"

    Enable plaintext passthrough (y/n) [n]:

    Enable filename encryption (y/n) [n]: y
        "n"

    Filename Encryption Key (FNEK) Signature [f873fb2794e1bb82]:

    Attempting to mount with the following options:
      ecryptfs_unlink_sigs
      ecryptfs_fnek_sig=f873fb2794e1bb82
      ecryptfs_key_bytes=32
      ecryptfs_cipher=aes
      ecryptfs_sig=f873fb2794e1bb82

    WARNING: Based on the contents of [/root/.ecryptfs/sig-cache.txt],
    it looks like you have never mounted with this key
    before. This could mean that you have typed your
    passphrase wrong.

    Would you like to proceed with the mount (yes/no)? : yes

    Would you like to append sig [f873fb2794e1bb82] to
    [/root/.ecryptfs/sig-cache.txt]
    in order to avoid this warning in the future (yes/no)? : yes
    Mounted eCryptfs

La `passphrase` es la contraseña utilizada para montar el directorio.
Luego especificamos el algoritmo de cifrado y la longitud de la clave.
La opción `passthrought` permite guardar ficheros sin cifrar. Luego
podemos escoger cifrar también los nombres de fichero, e incluso escoger
una clave distinta para el nombre y para el fichero.

Este es el contenido que tendremos en nuestra cuenta de Dropbox:

    $ touch ~/ecryptDropbox/myfile
    $ ls ~/.dropbox/Dropbox/ecryptDropbox
    ECRYPTFS_FNEK_ENCRYPTED.FWbsAyi5CB4yVkY0czFjSWaXh52n0e59-VIQYq1x1vpJm6ZBDtj-4PILQwWaU--

[!Dropbox ecryptfs]({static}/images/dropbox-ecryptfs-300x97.png)

Para que el directorio se monte al arrancar el sistema deberemos añadir
al fichero `/etc/fstab`, pasándole las opciones directamente:

    /home/user/.dropbox/Dropbox/ecryptDropbox /home/user/ecryptDropbox ecryptfs user,rw,ecryptfs_sig=f873fb2794e1bb82,ecryptfs_fnek_sig=f873fb2794e1bb82,ecryptfs_key_bytes=32,ecryptfs_cipher=aes,ecryptfs_unlink_sigs,ecryptfs_passthrough=no,key=passphrase:passwd=UsedPasswordToEncrypt 0 0

A la hora de montarlo, deberemos especificar las opciones que hemos
escogido a la hora de crearlo:

-   `ecryptfs_sig`: es la clave que se utiliza para cifrar los ficheros.
-   `ecryptfs_fnek_sig`: es la clave que se utiliza para cifrar los
    nombres de los ficheros.
-   `ecryptfs_cipher`: es el algoritmo de cifrado a utilizar.
-   `ecryptfs_key_bytes`: es la longitud de la clave para cifrar.
-   `ecryptfs_passthrough`: especifica si se va a permitir guardar
    ficheros sin cifrar.
-   `ecryptfs_unlink_sigs`: especifica que se vacie el anillo de claves
    cada vez que se desmonta el directorio,
-   `key=tipo:opciones`. especifica el tipo de contraseña que vamos a
    utilizar y algunas opciones. El tipo se corresponde con uno de los
    módulos instalados en `/usr/lib*/ecryptfs/`, como mínimo suelen ser
    `passphrase` y `ssl`. Las opciones pueden ser:
    -   `passwd` para especificar la contraseña directamente,
    -   `passwd_file` para utilizar un fichero que contiene la
        contraseña en la forma `passwd=contraseña`,
    -   `passwd_fd` para utilizar un descriptor de fichero,
    -   `passstdin` para pedir la contraseña al usuario,
    -   `salt` para especificar un valor hexadecimal de 16 bits como la
        sal,
    -   `keyfile` para especificar el fichero que contiene una clave SSL
        o RSA.

Si queremos que nos pida la contraseña cada vez que se monte, en lugar
de la línea anterior, pondríamos:

    /home/user/.dropbox/Dropbox/ecryptDropbox /home/user/ecryptDropbox ecryptfs user,rw,noauto,ecryptfs_sig=f873fb2794e1bb82,ecryptfs_fnek_sig=f873fb2794e1bb82,ecryptfs_key_bytes=32,ecryptfs_cipher=aes,ecryptfs_unlink_sigs,ecryptfs_passthrough=no 0 0

Para comprobar que funciona correctamente, desmontamos previamente el
directorio y lo volvemos a montar:

    $ sudo umount ~/ecryptDropbox
    $ mount ~/ecryptDropbox -o ecryptfs_sig=f873fb2794e1bb82,ecryptfs_fnek_sig=f873fb2794e1bb82,ecryptfs_key_bytes=32,ecryptfs_cipher=aes,ecryptfs_unlink_sigs,ecryptfs_passthrough=no
    Passphrase:

Si esto nos devuelve el siguiente error:

    Error attempting to evaluate mount options: [-22] Invalid argument
    Check your system logs for details on why this happened.
    Try updating your ecryptfs-utils package, and/or
    submit a bug report on https://launchpad.net/ecryptfs

Tenemos dos [opciones][], o bien añadimos el [bit de `sutuid`][] al
comando `mount.ecryptfs`, o bien lo montamos como `root`.

Referencias
------------

- En el directorio público de mi cuenta de Dropbox tengo subidos varios [ezines sobre GNU/Linux, software libre, programación y seguridad][].
- En el directorio público de Ubuntu One tengo subidos varios [libros y artículos sobre GNU/Linux, software libre, programación y seguridad][].

  [entregará tus ficheros al gobierno de Estados Unidos]: http://www.businessinsider.com/dropbox-updates-security-terms-of-service-to-say-it-can-decrpyt-files-if-the-government-asks-it-to-2011-4?op=1
    "entregará tus ficheros al gobierno de Estados Unidos"
  [saltarse las restricciones]: http://www.hispasec.com/unaaldia/4558
    "saltarse las restricciones"
  [una de nuestras cuentas de Dropbox]: {filename}/admin/multiples-cuentas-de-dropbox-en-ubuntu-maverick-meerkat.md
    "múltiples cuentas de dropbox en ubuntu maverick meerkat"
  [Linux Journal]: http://www.linuxjournal.com/article/9400
    "Linux Journal"
  [cifrado]: http://manpages.ubuntu.com/manpages/intrepid/man7/ecryptfs.7.html
    "cifrado"
  [opciones]: http://wiki.archlinux.org/index.php/System_Encryption_with_eCryptfs#Mounting
    "opciones"
  [bit de `sutuid`]: {filename}/admin/setuid-y-setgid.md
    "setuid y setgid"
  [ezines sobre GNU/Linux, software libre, programación y seguridad]: http://dl.dropbox.com/u/13647978/index.html
    "ezines sobre GNU/Linux, software libre, programación y seguridad"
  [libros y artículos sobre GNU/Linux, software libre, programación y seguridad]: http://ubuntuone.com/p/NoU/
    "libros y artículos sobre GNU/Linux, software libre, programación y seguridad"
