Title: Conectar a un servidor SSH desde Android mediante ConnectBot utilizando claves
Date: 2012-07-24 13:06
Author: Nacho Cano
Tags: android, clave pública, connectbot, generar claves ssh, rsa, ssh
Slug: conectar-a-un-servidor-ssh-desde-android-mediante-connectbot-utilizando-claves
Related: conectarse-por-ssh-solo-usando-la-clave,servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal,sslh-compartiendo-el-puerto-443

[ConnectBot][] es, en mi humilde opinión, el mejor cliente SSH para
Android. Nos permite conectarnos de forma segura a nuestro servidor SSH,
ya sea directamente o mediante la creación de un túnel SSH que sirva de
_proxy_ al resto de aplicaciones.

La manera más segura de conectarnos es mediante la utilización de
claves. Este es un sistema de autenticación basado en criptografía
asimétrica, más seguro que utilizar _simples_ contraseñas.

ConnectBot no sólo permite utilizar claves, sino que también nos permite
crearlas e importarlas. Para poder conectarnos a nuestro servidor sin
necesidad de utilizar contraseñas, lo primero será que éste esté
[configurado para aceptar claves][]. En particular, en el fichero
`/etc/ssh/sshd_config`, debemos tener la directiva:

    PubkeyAuthentication yes

Si queremos importar una clave para ser utilizada por ConnectBot, lo
único que tendremos que hacer es guardarla en la raíz de la tarjeta de
memoria e ir a Menú > Administrar claves públicas > Menú > Importar.

Otra opción es generar un par de claves. Para ello, vamos a Menú >
Administrar claves públicas > Menú > Generar, y utilizamos los
siguientes datos:

-   Nombre para la clave: keyname (podemos usar el nombre que queramos
    para poder identificarla)
-   Tipo: RSA
-   Bits: 4096
-   Contraseña: si queremos, podemos optar por dejarla en blanco,
    sabiendo que si la clave cae en malas manos puede tener una puerta
    abierta hacia nuestro servidor.
-   Cargar al inicio: lo marcamos si queremos que la clave se cargue en
    memoria nada más arrancar el teléfono. Si la clave no está cargada
    en memoria, ConnectBot no intentará utilizarla.
-   Confirmar antes de cargar: lo marcamos si queremos que nos pida
    confirmación cuando se vaya a utilizar la clave.

El siguiente paso es copiar la clave pública al listado de claves
autorizadas para el usuario en el servidor. La forma más rápida y
sencilla y es ir al gestor de claves y copiamos la __clave pública__ de
la clave en cuestión (realizando una pulsación larga sobre la misma).
Luego, nos conectamos al servidor normalmente, mediante usuario y
contraseña, y añadimos la clave mediante el siguiente comando (aquí
pegamos la clave pública que habíamos copiado):

    username@remote:~$ echo "ssh-rsa AAAA.....(resto de la clave)" >> .ssh/authorized_keys

La próxima vez que nos conectemos mediante ConnectBot ya no
necesitaremos utilizar usuario ni contraseña. Si no hemos seleccionado
cargar la clave al inicio, y la clave no está cargada en memoria en el
momento de hacer el intento de conexión, ConnectBot nos pedirá que nos
autentiquemos mediante usuario y contraseña. Si hemos marcado que nos
avise antes de usar la clave, y la clave está cargada en memoria, nos
pedirá confirmación antes de usarla.

Denegar el acceso
-----------------

Si, por cualquier motivo, queremos denegar el acceso a dicha clave al
servidor, lo único que tenemos que hacer es borrarla del fichero
`~/.ssh/authorized_keys`. Una sencilla forma de hacerlo es mediante el
nombre que hemos utilizado para la clave:

    username@remote:~$ sed -i '/keyname$/d' ~/.ssh/authorized_keys

Referencias
-----------

» [ConnectBot][1] en el _market_

  [ConnectBot]: http://code.google.com/p/connectbot/
    "ConnectBot"
  [configurado para aceptar claves]: {filename}/admin/conectarse-por-ssh-solo-usando-la-clave.md
    "conectarse por ssh usando claves"
  [1]: http://play.google.com/store/apps/details?id=org.connectbot
    "ConnectBot en Play Store"
