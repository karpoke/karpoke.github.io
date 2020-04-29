Title: Servicio de SSH con Latch en Ubuntu
Date: 2015-03-22 02:01
Author: Nacho Cano
Tags: 2FA, latch, latch-ssh-cmd, OTP, ssh, ubuntu
Slug: servicio-de-ssh-con-latch-en-ubuntu
Related: servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal, conectarse-por-ssh-solo-usando-la-clave

Mediante [Latch][], podemos añadir una capa extra de seguridad a nuestro
servicio SSH, limitando la ventana de tiempo durante la cual permitimos
iniciar sesión en el servidor.


Instalación
-----------

Descargamos los paquetes que vamos a necesitar:

    $ sudo aptitude install gcc make
    $ sudo aptitude install libpam0g-dev libcurl4-gnutls-dev libssl-dev

(Si ya teníamos instalado el paquete `libcurl4-openssl-dev`, podemos
usar éste en lugar de `libcurl4-gnutls-dev`.)

Descargamos el código de github y compilamos:

    $ git clone https://github.com/ElevenPaths/latch-plugin-unix.git
    $ cd latch-plugin-unix
    $ ./configure prefix=/usr sysconfdir=/etc && make && sudo make install

Antes de continuar, vamos al [área de desarrolladores][] y creamos una
cuenta para este servicio. Ahí obtenemos el identificador de aplicación
y la contraseña.

Configuración
-------------

La instalación se puede hacer bien con un módulo PAM o bien configurando
SSH.

### Módulo PAM

Si vamos a configurar un módulo PAM, en la configuración del servicio
que hemos creado en el área de desarrolladores, añadiremos una nueva
"operación", por ejemplo "sshd-login", con lo que obtendremos una
contraseña para esta operación en particular.

Editamos el fichero `/etc/latch/latch.conf` para añadir nuestro
identificador de aplicación, la contraseña. Especificamos la acción por
defecto si el servicio de Latch no estuviera disponible (_open_ o
_close_) y añadirmos las diferentes contraseñas para las operaciones que
hayamos definido en la cuenta.

Movemos el fichero `.so` a su destino:

    $ sudo mv /usr/lib/pam_latch.so /lib/security/

Editamos el fichero `/etc/pam.d/sshd`, y añadimos al final:

    auth required pam_latch.so config=/etc/latch/latch.conf accounts=/etc/latch/latch.accounts operation=sshd-login otp=yes

Igual que en el caso del [servicio de SSH con sistema de verificación en
dos pasos de Google][], podemos añadir una regla justo antes de la que
acabamos de definir para que las conexiones desde la misma red no sean
examinadas:

    auth [success=1 default=ignore] pam_access.so accessfile=/etc/security/access-local.conf

El contenido del fichero `/etc/security/access-local.conf`:

    + : ALL : 192.168.50.0/24
    + : ALL : LOCAL
    - : ALL : ALL

Por último, sólo queda parear cada usuario que queramos utilizar. Desde
la aplicación en el móvil, generamos un código de pareado. Utilizaremos
el token proporcionado y ejecutaremos el siguiente comando:

    $ latch -p
    Account successfully paired to the user myuser

Si queremos _desparear_ un usuario:

    $ latch -u

### Configuración de SSH

Si en lugar de añadir el módulo PAM, queremos configurar el servidor de
SSH, editamos el fichero de configuración `/etc/ssh/sshd_config` y nos
aseguramos de que contenga:

    UsePAM yes
    ChallengeResponseAuthentication yes
    PasswordAuthentication no

Para proteger las claves de autorización, editamos el fichero de
configuración de los usuario `~/.ssh/authorized_keys`:

    command="latch-ssh-cmd -o sshd-keys" ssh-rsa AAA...HP5 someone@host

En este caso, hemos definido una nueva operación "sshd-keys" en la
configuración de nuestra cuenta. También hay que tener en cuenta que si
optamos por la opción de configurar el servicio SSH, mediante el comando
`latch-ssh-cmd` no está disponible la opción de claves de un solo uso
(OTP).

### Desinstalación

Si queremos desinstalar Latch, basta que eliminemos los cambios que
hemos hecho en `/etc/pam.d/sshd`, o `/etc/ssh/sshd_config` y
`~/.ssh/authorized_keys`, en caso de haber optado por la opción de
configurar el servicio de SSH.

A continuación, desde el directorio donde habíamos descargado el código,
ejecutamos:

    $ ./configure prefix=/usr sysconfdir=/etc && make && sudo make uninstall

  [Latch]: https://latch.elevenpaths.com/
    "Latch"
  [área de desarrolladores]: https://latch.elevenpaths.com/www/developers/editapplication
    "área de desarrolladores"
  [servicio de SSH con sistema de verificación en dos pasos de Google]: {filename}/admin/servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal.md
    "servicio de SSH con sistema de verificación en dos pasos de Google"
