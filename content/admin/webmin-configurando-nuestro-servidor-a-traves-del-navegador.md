Title: webmin, configurando nuestro servidor a través del navegador
Date: 2012-06-12 20:05
Author: Nacho Cano
Tags: firewall, ubuntu, ufw, webmin
Slug: webmin-configurando-nuestro-servidor-a-traves-del-navegador

[Webmin][] es una interfaz web para la administración de un servidor,
compatible con cualquier navegador moderno, mediante la que podemos
configurar cuentas de usuario, Apache, DNS, intercambio de ficheros,
etc. Es una alternativa a la configuración manual de ficheros.

Instalación
-----------

Instalamos las dependencias:

    $ sudo aptitude install perl libnet-ssleay-perl openssl libauthen-pam-perl libpam-runtime libio-pty-perl apt-show-versions

Descargamos el paquete para Ubuntu y lo instalamos:

    $ wget http://downloads.sourceforge.net/webadmin/webmin_1.580_all.deb
    $ md5sum webmin_1.580_all.deb
    093c720a988125a536fa9fda16080fe6
    $ sudo dpkg -i webmin_1.580_all.deb

Para usar Webmin, accedemos al servidor en el puerto 10000. El usuario y
la contraseña son los mismos que utilizamos para iniciar sesión en el
servidor.

Si fuese el caso, activamos la regla en el cortafuegos. Por ejemplo, si
usamos `ufw` y queremos permitir el acceso únicamente desde la misma
red:

    $ sudo ufw allow proto tcp from 192.168.50.0/24 to any port 10000

  [Webmin]: http://www.webmin.com/
    "Webmin"
