Title: Saltándonos el portal cautivo de una biblioteca
Date: 2012-05-15 14:06
Author: Nacho Cano
Tags: firefox, nslookup, portal cautivo, proxy socks, socksv5, ssh
Slug: saltandonos-el-portal-cautivo-de-una-biblioteca
Related: utilizar-ssh-para-establecer-un-servidor-proxy-socks,conectarse-por-ssh-solo-usando-la-clave,servicio-de-ssh-con-sistema-de-verificacion-en-dos-pasos-de-google-en-ubuntu-natty-narwhal,fwknop-single-packet-authorization-y-port-knocking,tunel-ssh-inverso,ssh-over-http-proxy,sslh-compartiendo-el-puerto-443,compartiendo-una-conexion-por-ssh,secuencias-de-escape-en-ssh

El portal cautivo es el sistema que utilizan algunos establecimientos
como bibliotecas u hoteles en el que la conexión inalámbrica está
abierta (sin cifrar) pero para conectarse a Internet es necesario
aceptar las condiciones de uso, o introducir una contraseña, en la
página de pasarela que aparece cuando intentamos navegar.

Este no es un artículo exhaustivo que muestre como saltarse cualquier
portal cautivo sino más bien aquél que permite el paso de tráfico TCP
por el puerto 53 (DNS). Lo que veremos aquí NO es un túnel DNS, que
permite encapsular el tráfico TCP en paquetes de DNS.

Además, necesitaremos tener acceso a un equipo remoto con el servicio de
SSH y en el que esté redirigido el puerto externo 53 (DNS) al puerto del
equipo interno donde corre SSH.

En muchas ocasiones, el portal cautivo permitirá el tráfico DNS al
exterior, incluso sin haber introducido la contraseña o haber aceptado
las condiciones de uso del servicio, ya que suele haber un servidor DNS
en la misma red, y éste necesita acceso al exterior. Para probar si está
permitido el tráfico DNS, nos conectamos a la red (sin pasar por la
pasarela web) y comprobamos si resuelve el dominio que apunta a nuestro
equipo remoto.

```bash
$ nslookup mydomain.com
Server:     10.28.28.28
Address:    10.28.28.28#53

Non-authoritative answer:
Name:   mydomain.com
Address: 1.2.3.4
```

Si no tenemos un dominio pero sabemos la IP, utilizaremos la IP en su
lugar. Si no obtenemos respuesta, difícilmente vamos a poder
conectarnos. Si obtenemos respuesta sabemos que, al menos, se permite el
tráfico UDP por el puerto 53 (las peticiones de DNS van por UDP, no
utilizan TCP), y hay posibilidades de que también permita el tráfico
TCP.

Crearemos un [_proxy_ SOCKS][]. Por ejemplo, ejecutamos:

```bash
$ ssh -p53 -D 8080 mydomain.com
```

Si no conecta es que el puerto TCP está filtrado. Todavía podríamos
probar con un túnel DNS o encontrar algún fallo en la pasarela del
portal cautivo. Si todo ha ido bien, ya tenemos el _proxy_ corriendo en
el puerto 8080 de nuestra máquina, y que podemos utilizar para:

-   navegar de forma segura,
-   navegar de forma anónima para el administrador de la red,
-   evitar las continuas desconexiones que se producen en el portal
    cautivo y que obligan a estar continuamente volviendo a conectar (en
    algunos casos, como el que inspiró la creación de este artículo),
-   saltarnos las restricciones del portal cautivo, por ejemplo
    direcciones censuradas como facebook, etc,
-   asegurar cualquier tipo de conexión,
-   etc.

Como ejemplo. para que Firefox utilice este _proxy_ vamos a Editar >
Preferencias > Avanzado > Red > Configuración de la Conexión >
Seleccionamos Proxy Manual y ponemos:

-   SOCKS Host: localhost
-   Puerto: 8080
-   Seleccionamos SOCKSv5

Nunca se sabe quién puede estar escuchando nuestra conexión y los datos
que viajan por ella, como contraseñas, _cookies_ de sesión, mensajes,
correos...

  [_proxy_ SOCKS]: {filename}/admin/utilizar-ssh-para-establecer-un-servidor-proxy-socks.md
    "Utilizar SSH para establecer un servidor proxy SOCKS"
