Title: Actualizar nuestra IP en el panel de OpenDNS
Date: 2016-12-03 14:32
Author: Nacho Cano
Tags: ddclient, OpenDNS, OpenDNS Home, IP dinámica, dnsomatic
Slug: actualizar-nuestra-ip-en-el-panel-de-opendns
Related: asignar-la-ip-que-queramos-a-un-dominio-de-dyndns,dyndns-e-inadyn,iniciar-sesion-en-dyndns-desde-el-terminal,obteniendo-la-ip-publica-la-ip-privada-y-la-direccion-mac-en-bash

Si estamos usando el servicio [OpenDNS Home][] y tenemos una IP dinámica,
podemos utilizar `ddclient`, disponible en los repositorios, para actualizar
la IP registrada en dicho servicio cada vez que [cambie nuestra IP].

Para ello, lo único que necesitamos es editar el fichero de configuración en
`/etc/ddclient.conf`:

    ##
    ## OpenDNS.com account-configuration
    ##
    use=web, web=myip.dnsomatic.com
    ssl=yes
    server=updates.opendns.com
    protocol=dyndns2
    login=username@example.com
    password=opendns_password
    opendns_network_label

Los espacios en el nombre dado a la red se deben sustituir por guiones bajos
"_" y si la contraseña contiene caracteres especiales, se debe encerrar entre
comillas simples "'".

Si lo acabamos de instalar y seguimos el asistente, el archivo resultante no
será exactamente igual:

  Proveedor de servicio: updates.opendns.com
  Protocolo: dyndns2
  Nombre de usuario: username@example.com
  Contraseña: opendns_password
  Interfaz de red: eth0
  Nombres completos de dominios: opendns_network_label

Esto genera el siguiente archivo de configuración:

    protocol=dyndns2
    use=if, if=eth0
    server=updates.opendns.com
    login=username@example.com
    password=opendns_password
    opendns_network_label

Para especificar que la IP la coja de un servicio externo en lugar de una
interfaz de red, tendremos que cambiar:

    use=if, if=eth0

por:

    use=web, web=myip.dnsomatic.com

y añadimos que use `ssl`:

    ssl=yes

Probamos la configuración:

    sudo ddclient -daemon=0 -debug -verbose -noquiet

Para que se ejecute al inicio:

    sudo /sbin/chkconfig ddclient on

Para lanzarlo:

    sudo /sbin/service ddclient start

  [OpenDNS Home]: https://signup.opendns.com/homefree/
    "OpenDNS Home"
  [cambie nuestra IP]: https://support.opendns.com/hc/en-us/articles/227987727-Linux-IP-Updater-for-Dynamic-Networks
    "Linux IP Updater"
