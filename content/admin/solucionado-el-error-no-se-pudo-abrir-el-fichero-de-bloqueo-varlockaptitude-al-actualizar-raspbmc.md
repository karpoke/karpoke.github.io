Title: Solucionado el error "No se pudo abrir el fichero de bloqueo «/var/lock/aptitude»" al actualizar Raspbmc
Date: 2012-09-06 13:44
Author: Nacho Cano
Tags: aptitude, fichero de bloqueo, raspberry pi, raspbmc
Slug: solucionado-el-error-no-se-pudo-abrir-el-fichero-de-bloqueo-varlockaptitude-al-actualizar-raspbmc

Tengo una Raspbmc instalada en la Raspberry Pi. Al utilizar `aptitude`
para instalar cualquier paquete o actualizar el sistema, recibo el
siguiente error:

    $ sudo aptitude update
    [ ERR] Leyendo la información de estado
    E: No se pudo abrir el fichero de bloqueo "/var/lock/aptitude" - open (2: No existe el fichero o el directorio)
    W: No se pudo bloquear el fichero de almacén. Esto significa habitualmente que dpkg u otra herramienta apt está instalando paquetes. Se abrirá en modo de sólo lectura, ¡se PERDERÁN todos los cambios que realice al estado de los paquetes!

En realidad, lo que sucede es que `/var/lock` es un enlace simbólico que
apunta a `/run/lock`, que no existe, y de ahí que no lo encuentre.
Creando el directorio en cuestión, se soluciona el problema:

    $ sudo mkdir /run/lock
