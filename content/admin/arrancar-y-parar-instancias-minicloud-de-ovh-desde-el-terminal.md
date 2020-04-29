Title: Arrancar y parar instancias minicloud de OVH desde el terminal
Date: 2012-04-20 03:05
Author: Nacho Cano
Tags: at, cron, crontab, máquina virtual, minicloud, ovh
Slug: arrancar-y-parar-instancias-minicloud-de-ovh-desde-el-terminal
Related: obteniendo-la-ip-publica-la-ip-privada-y-la-direccion-mac-en-bash,asignar-la-ip-que-queramos-a-un-dominio-de-dyndns,dyndns-e-inadyn

Si tenemos un _minicloud_ con OVH, podemos gestionar las instancias
(máquinas vituales) con un _script_ creado por [Dominique Gallot][]. El
_script_ utiliza la [API SOAP de OVH][], de tal manera que permite
obtener información sobre las instancias, arrancarlas y pararlas desde
el terminal, sin tener que hacerlo desde el panel de administración.

En la página de OVH tienen el _script_
[`ovhclud`, para gestionar la nube (Public Cloud)][ovhclud, para gestionar la nube (Public Cloud)],
pero parece que todavía no soporta las instancias de _minicloud_.


Instalación
-----------

Para descargar el _script_ de la página de Gallot:

    $ wget -q http://svn.gallot.be/blog/ovh-cloud-api/ovh.pm
    $ wget -q http://svn.gallot.be/blog/ovh-cloud-api/ovh.pl
    $ chmod a+x ovh.pl

El _script_ utiliza la librería `libsoap-lite-perl`, por lo que deberá
estar instalada en el sistema.

Acciones
--------

Para obtener un listado de los servicios que tenemos:

    $ ./ovh.pl -u ab12345-ovh -p mypassword -a listservice
    Services
    name : ab12345-cloud0
    title : Cloud
    zone : ab1c2.project.ovh.net

Para listar las instancias:

    $ ./ovh.pl -u ab12345-ovh -p mypassword -q -a listvm
    cloud1  12345   running 211.58.125.116

Para listar una instancia concreta:

    $ ./ovh.pl -u ab12345-ovh -p mypassword -q -a listvm -s cloud1
    cloud1  12345   running 211.58.125.116

En este caso, hay una instancia encendida. Si queremos pararla sólo
tenemos que especifica el nombre de la misma:

    $ ./ovh.pl -u ab12345-ovh -p mypassword -a stopvm -m cloud1

Podemos comprobar que está parada:

    $ ./ovh.pl -u ab12345-ovh -p mypassword -a listvm
    name : cloud1
    id : 12345
    state : stopped
    ip :
    ipDns :

Para arrancar la instancia también debemos especificar el nombre:

    $ ./ovh.pl -u ab12345-ovh -p mypassword -a startvm -m cloud1

Si acto seguido comprobamos la instancia, vemos que ya tiene asignada
una IP (distinta a la anterior), aunque está marcada como _stopped_:

    $ ./ovh.pl -u ab12345-ovh -p mypassword -a listvm
    name : cloud1
    id : 12345
    state : stopped
    ip : 136.125.58.211
    ipDns : mc-136-125-58-211.ovh.net

Transcurrido el tiempo que la instancia tarda en arrancar, ya queda
marcada como encendida:

    $ ./ovh.pl -u ab12345-ovh -p mypassword -a listvm
    name : cloud1
    id : 12345
    state : running
    ip : 136.125.58.211
    ipDns : mc-136-125-58-211.ovh.net

También podemos reiniciarla:

    $ ./ovh.pl -u ab12345-ovh -p mypassword -a rebootvm

Si queremos seguir el intercambios de mensajes SOAP podemos añadir el
argumento `-t`.

Parar una instancia proporcionando su URL o su IP
-------------------------------------------------

Teniendo esto en cuenta, el siguiente _script_ `stop-cloud-url.sh`
detiene la instancia dada su URL:

    #!/bin/bash -
    USERNAME=ab12345-ovh
    PASSWORD=mypassword
    DOMAIN="$1"
    IP=$(host "$DOMAIN" | awk '{print $NF}')
    VMNAME=$(ovh.pl -u $USERNAME -p $PASSWORD -q -a listvm | grep $IP | awk '{print $1}')
    ovh.pl -u $USERNAME -p $PASSWORD -a stopvm -m $VMNAME

Si, en lugar de un dominio, tenemos su IP, podemos detener la instancia
usando el _script_ `stop-cloud-ip.sh`:

    #!/bin/bash -
    USERNAME=ab12345-ovh
    PASSWORD=mypassword
    IP="$1"
    VMNAME=$(ovh.pl -u $USERNAME -p $PASSWORD -q -a listvm | grep $IP | awk '{print $1}')
    ovh.pl -u $USERNAME -p $PASSWORD -a stopvm -m $VMNAME

#### Can’t locate ovh.pm in @INC

El _script_ `ovh.pl` hace uso del paquete `ovh.pm`. Si no ejecutamos
`ovh.pl` desde el mismo directorio en el que está `ovh.pm` [se quejará
de que no lo encuentra][]. Para solucionarlo, podemos copiar el paquete
a una ruta incluido en el @INC (más o menos como el CLASSPATH de Java o
el PYTHONPATH de Python):

    $ perl -e 'print "@INC";'
    /etc/perl /usr/local/lib/perl/5.12.4 /usr/local/share/perl/5.12.4 /usr/lib/perl5 /usr/share/perl5 /usr/lib/perl/5.12 /usr/share/perl/5.12 /usr/local/lib/site_perl .

También podemos incluir la siguiente directiva, en `ovh.pl`, para que
incluya el directorio donde se encuentra `ovh.pm`:

    use lib '/home/myuser/modules';

Programar el encendido o apagado de una instancia
-------------------------------------------------

Programar el encendido o apagado de la instancia se vuelve muy sencillo.

Si queremos programar un encendido o apagado a una hora concreta, o
dentro de un tiempo determinado:

    $ at 08:00
    $ at midnight
    $ at noon
    $ at now
    $ at now + 5 minutes
    $ at midnight + 2 weeks

Después, introducimos la ruta del _script_ y terminamos con `^D`
(control+D).

Si queremos que sea algo periódico, por ejemplo, de lunes a viernes de
7am a 5pm, utilizaremos el `cron`:

    $ crontab -e
    # m h d mon dow(0=sunday)
    0  7 * * 1-5 /path/to/start-cloud.sh
    0 17 * * 1-5 /path/to/stop-cloud-url.sh sub.domain.com

  [Dominique Gallot]: http://www.gallot.be/?p=124
    "Dominique Gallot"
  [API SOAP de OVH]: http://www.ovh.com/soapi/es/
    "API SOAP de OVH"
  [ovhclud, para gestionar la nube (Public Cloud)]: http://www.ovh.com/fr/cloud/api/ovhcloud
    "ovhclud, para gestionar la nube (Public Cloud)"
  [se quejará de que no lo encuentra]: http://www.devdaily.com/blog/post/perl/perl-error-cant-locate-module-in-inc
    "se quejará de que no lo encuentra"
