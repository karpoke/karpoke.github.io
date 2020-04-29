Title: Conectarse por SSH sólo usando la clave
Date: 2011-03-03 21:22
Author: Nacho Cano
Tags: authorized_keys, cambiar contraseña, clave pública, contraseña, fingerprint, generar claves ssh, id_rsa, id_rsa.pub, openssh, randomart, rsa, ssh, ssh-copy-id, ssh-keygen
Slug: conectarse-por-ssh-solo-usando-la-clave
Related: servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal,sslh-compartiendo-el-puerto-443,compartiendo-una-conexion-por-ssh,conectarse-por-ssh-utilizando-expect

Conectarnos a nuestro servidor de SSH utilizando una clave RSA en lugar
de una contraseña es más seguro, dado que la clave RSA será bastante más
larga y difícil de comprometer que nuestra contraseña, y más cómodo,
dado que ya no tendremos que escribir la contraseña para iniciar sesión.


Configuración
-------------

En el equipo local, creamos la clave. Cuando nos pida contraseña, le
asignamos una, que nos será requerida cada vez que queramos usar dicha
clave. Si estuviéramos creando las claves en el servidor la [dejaríamos
en blanco][].

    $ ssh-keygen -b 4096 -t rsa
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/username/.ssh/id_rsa):
    Enter passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved in /home/username/.ssh/id_rsa.
    Your public key has been saved in /home/username/.ssh/id_rsa.pub.
     The key fingerprint is:
     b5:51:c4:64:51:d6:d5:98:38:a6:0d:f1:ae:25:10:fb username@host
     The key's randomart image is:
     +--[ RSA 4096]----+
     |           ==*o+.|
     |          =oO . .|
     |        =.o* o   |
     |    .    . oo    |
     |   . o  S ..     |
     |  E o  .  .      |
     |     . . .       |
     |      . .        |
     |                 |
     +-----------------+

La copiamos al servidor:

    $ ssh-copy-id username@remotehost
    username@remotehost's password:
    Now try logging into the machine, with "ssh 'username@remotehost'", and check in:
    .ssh/authorized_keys
    to make sure we haven't added extra keys that you weren't expecting.

Si tenemos SSH corriendo en un puerto distinto, deberemos incluirlo todo
entre comillas simples, algo como:

    $ ssh-copy-id '-p1234 username@remotehost'

Hacemos lo que nos sugiere, y nos conectamos al servidor para comprobar
que en el fichero `~/.ssh/authorized_keys` están únicamente las claves
que hemos autorizado nosotros:

    $ ssh username@remotehost

![OpenSSH]({static}/images/openssh.png)

_<small>Fuente: [openssh.com][]</small>_

En el servidor, editamos el fichero `/etc/ssh/sshd_config` y nos
aseguramos de que:

    PubkeyAuthentication yes
    PasswordAuthentication no
    AllowUsers username

Reiniciamos el servicio `ssh` y listos:

    $ sudo service ssh restart

Si nos intentamos conectar desde un ordenador el cual no contiene la
clave, o con un usuario para el cual no está permitido el acceso:

    other@otherhost:~$ ssh user@remotehost
    Permission denied (publickey).

Cambiar o eliminar la frase de paso de la clave privada
-------------------------------------------------------

Si habíamos introducido una contraseña para usar la clave al crearla y
más tarde queremos cambiarla o eliminarla, por ejemplo, para conectarnos
por `ssh` en un _script_:

    $ ssh-keygen -p -f ~/.ssh/id_rsa
    Enter old passphrase:
    Key has comment '/home/unsername/.ssh/id_rsa'
    Enter new passphrase (empty for no passphrase):
    Enter same passphrase again:
    Your identification has been saved with the new passphrase.

Si hemos dejado en blanco el campo para la nueva contraseña, ya no nos
la pedirá al conectarnos.

Permitir que otro usuario se conecte usando sólo la clave
---------------------------------------------------------

Para que nos podamos conectar al servidor de la misma manera pero desde
otro equipo, deberemos seguir los mismos pasos descritos arriba, pero
antes, deberemos volver a permitir la autenticación con contraseña, ya
que de lo contrario el nuevo usuario no podrá copiar su clave al
servidor.

Nos conectamos al servidor con el usuario que con el que ya tenemos
acceso y editamos el fichero `/etc/ssh/sshd_config`:

    PasswordAuthentication yes

Si el nuevo usuario se conecta al servidor con un usuario distinto al de
antes, deberemos añadirlo a la lista de usuarios permitidos:

    AllowUser username otherusername

Reiniciamos el servicio:

    $ sudo service ssh restart

En el nuevo equipo, seguimos los pasos descritos arriba para crear la
clave y copiarla al servidor.

    $ ssh-keygen -b 4096 -t rsa

Una vez copiada, podemos probar de conectarnos:

    $ ssh otherusername@remotehost
    $ ssh-copy-id otherusername@remotehost
    $ ssh otherusername@remotehost

Si todo ha ido bien, y nos hemos conectado al servidor con el nuevo
usuario, ya podemos deshabilitar la autenticación por contraseña, en el
fichero `/etc/ssh/sshd_config`:

    PasswordAuthentication no

Y volvemos a reiniciar el servicio:

    $ sudo service ssh restart

  [dejaríamos en blanco]: http://marc.info/?l=secure-shell&m=91703263608458&w=2
    "dejaríamos en blanco"
  [openssh.com]: http://www.openssh.com/
    "openssh.com"
