Title: Utilizar SSH para establecer un servidor proxy SOCKS
Date: 2011-08-12 13:07
Author: Nacho Cano
Tags: autossh, firefox, proxy, proxy socks, proxychains, puertos bien conocidos, scp, sftp, SOCKS, ssh, tsocks
Slug: utilizar-ssh-para-establecer-un-servidor-proxy-socks
Related: ssh-over-http-proxy

Un _proxy_ SOCKS es un servidor que permite el acceso, normalmente, a
través de un cortafuegos. Podemos utilizar SSH para crear un _proxy_
SOCKSv5 en local, de tal manera que si configuramos una aplicación para
que se conecte a través de este _proxy_, todo el tráfico vaya a través
del canal seguro creado por SSH, y sea como si la conexión con dicha
aplicación se hiciera en la máquina remota a la cual nos hemos conectado
por SSH. Además, podemos utilizarlo con varias aplicaciones y diferentes
protocolos.

Esto nos permitirá, por ejemplo, navegar por cualquier sitio sin las
restricciones que pudiera tener la red a la cual nos hemos conectado, y
sin que nadie de dicha red pueda conocer qué páginas visitamos. No se
limita únicamente a navegar, también lo podemos utilizar para consultar
el correo electrónico, mensajería instantánea, etc. Se puede aplicar a
cualquier aplicación que pueda utilizar un _proxy_ SOCKS. De hecho,
incluso con aplicaciones que no están pensadas para utilizar este tipo
de _proxies_.


Crear el _proxy_ SOCKS
----------------------

Para crear el _proxy_ SOCKS, ejecutamos:

```bash
$ ssh -f -N -D 1080 user@remotehost
```

Con el argumento `-f` ejecutamos SSH en segundo plano. Con el argumento `-N`
le decimos que no vamos a ejecutar ningún comando, por lo que no nos
dará acceso a la consola. El argumento `-D` es el que crea una redirección
de puertos local a nivel de aplicación. Crea un _socket_ que escucha en
el puerto especificado, en este caso el 1080, en nuestra máquina y
cuando se realiza una conexión a este puerto, la conexión se
redirecciona a través del canal seguro creado.

Están soportadas las versiones SOCKS4 y SOCKS5. La principal diferencia
entre las dos es que la versión 5 incorporando autenticación. Sólo el
`root` puede redirigir puertos bien conocidos.

Configurar las aplicaciones
---------------------------

Una vez creado el _proxy_ SOCKS, deberemos configurar la aplicación para
que haga uso de él. Por ejemplo, para Firefox debemos ir a
Editar > Preferencias > Avanzado > Red > Configuración de la conexión > Configuración manual del _proxy_
y ponemos:

```bash
Servidor SOCKS: localhost
Puerto:         1080
```

`tsocks`, para las aplicaciones que no soportan el uso de _proxies_
-------------------------------------------------------------------

Hay aplicaciones que no están pensadas para utilizar un _proxy_ SOCKS.
En este caso, utilizaremos el comando `tsocks`, que permite que
cualquier aplicación utilice este tipo de _proxies_ de forma
transparente. Después de instalarlo de los repositorios, debemos
configurarlo editando el fichero `/etc/tsocks.conf`:

```bash
server = 127.0.0.1
server_type = 5
server_port = 1080
```

Para conseguir que una aplicación utilice nuestro _proxy_ SOCKS:

```bash
$ tsocks telnet google.com 80
Trying 209.85.148.106...
Connected to google.com.
Escape character is '^]'.
^C
```

[`tsocks` se basa en el concepto de "shared library interceptor"][tsocks se basa en el concepto de "shared library interceptor"].
Mediante el uso de la variable de entorno `LD_PRELOAD`, o del archivo
`/etc/ld.so.preload`, `tsocks` se carga automáticamente en el espacio
del proceso de cada programa ejecutado y sobrescribe la función
`connect()`, de tal manera que cuando una aplicación quiere establecer
una conexión TCP, en su lugar, pasa el control a `tsocks`, quien
determina si la conexión tiene que realizarse a través de un servidor
SOCKS (comprobando `/etc/tsocks.conf`) y, si es así, negocia la conexión
utilizando la función `connect()` real.

Si ejecutamos `tsocks` sin pasarle ningún parámetro, crea una consola en
la que `tsocks` están incluido en la variable `LD_PRELOAD`.

También podemos incluir `tsocks` en la variable de entorno `LD_PRELOAD`
de la sesión actual, eliminarlo o comprobar si ya está incluido:

```bash
$ tsocks -on
$ tsocks -off
$ tsocks -show
```

Por lo visto, las aplicaciones Java no se entienden con `tsocks` y
requieren una configuración especial:

```bash
$ java -DsocksProxyHost=127.0.0.1 -DsocksProxyPort=1080 MiAplicacionJava
```

`autossh`, cuando el _proxy_ se cae
-----------------------------------

Podría pasar que la conexión se corte de vez en cuando. En este caso,
podemos utilizar `autossh`:

```bash
$ autossh -f -N -D 1080 user@remotehost
```

SSH a través del _proxy_ SOCKS
------------------------------

Para conectarnos a un servidor SSH a través de otro, no es necesario que
creemos un _proxy_ SOCKS. Podemos conectarnos utilizando uno de
intermediario:

```bash
$ ssh -t remotehost ssh otherremotehost
```

Esto se suele utilizar si, desde donde estamos, `remotehost` es
accesible pero `otherremotehost` no lo es, pero éste sí es accesible
desde el primero. Sin embargo, esta opción no va del todo bien si lo que
queremos es utilizar `scp` o `sftp`.

Podríamos utilizar `tsocks` para crear una [conexión SSH a través del
_proxy_ SOCKS][conexión SSH a través del proxy SOCKS] que tenemos:

```bash
$ tsocks ssh otherremotehost
```

Pero `ssh` también dispone de sus propios métodos. La opción
`ProxyCommand` sirve para conectar a un servidor SSH a través de un
_proxy_:

```bash
$ ssh -o "ProxyCommand /bin/nc.openbsd -x localhost %h %p" user@otherremotethost
```

También podríamos añadir la configuración de [`ProxyCommand` a nuestro
archivo `~/.ssh/config`][ProxyCommand a nuestro archivo ~/.ssh/config]:

```bash
Host otherremotehost
     ProxyCommand ssh remotehost exec nc %h %p
```

Ahora, para conectarnos a `otherremotehost` se puede hacer de forma
directa, sin pasarle ningún parámetro demás a `ssh`. Ojo, necesitamos
tener instalado `netcat` (`nc`) en ambos casos.

```bash
$ ssh otherremotehost
```

Con algún que otro truco, también se puede conseguir utilizar
[`ProxyCommand` sin utilizar `netcat`][ProxyCommand sin utilizar netcat].
Se trata de utilizar el fichero especial `/dev/tcp`:

```bash
ProxyCommand ssh remotehost 'exec 3<>/dev/tcp/otherremotehost/22; cat < &3 & cat >&3;kill $!'
```

Para [comprobar que esta funcionalidad está soportada][], deberemos
ejecutar lo siguiente en `remotehost`, lo que nos devolverá la página de
inicio de Google:

```bash
$ exec 3<>/dev/tcp/www.google.com/80
$ echo -e "GET / HTTP/1.1\n\n">&3
$ cat < &3
```

Si queremos estar seguros de que utilizamos `bash`, podemos poner:

```bash
ProxyCommand ssh remotehost "/bin/bash -c 'exec 3<>/dev/tcp/otherremotehost/22; cat < &3 & cat >&3;kill $!'"
```

Los ficheros `/dev/tcp` y `/dev/udp` no existen, sino que son
interpretados por Bash directamente.

```bash
$ strings /bin/bash | grep -iE "tcp|udp"
/dev/tcp/_/_
/dev/udp/_/_
```

Encadenar _proxies_ mediante `proxychains`
------------------------------------------

Por último, podemos utilizar `proxychains` para encadenar varios
_proxies_. `proxychains` acepta _proxies_ SOCKS4, SOCKS4 y HTTP
_proxies_. Los ficheros de configuración que se comprueban, en orden,
son:

-   `./proxychains.conf`
-   `$HOME/.proxychains/proxychains.conf`
-   `/etc/proxychains.conf`

Lo más sencillo es editar el fichero `/etc/proxychains.conf`. Algunos
ejemplos de configuración:

```bash
socks5  192.168.67.78   1080    lamer   secret
http    192.168.89.3    8080    justu   hidden
socks4  192.168.1.49    1080
http    192.168.39.93   8080
```

En nuestro caso, tendríamos únicamente el _proxy_ SOCKS que hemos creado
nosotros:

```bash
socks5  127.0.0.1       1080
```

Para ejecutarlo, es similar a `tsocks`:

```bash
$ proxychains telnet google.com 80
ProxyChains-3.1 (http://proxychains.sf.net)
|DNS-request| google.com
|S-chain|-<>-127.0.0.1:9050-<><>-4.2.2.2:53-<><>-OK
|DNS-response| google.com is 209.85.148.106
Trying 209.85.148.106...
|S-chain|-<>-127.0.0.1:1080-<><>-209.85.148.106:80-<><>-OK
Connected to google.com.
Escape character is '^]'.
^C
```

  [tsocks se basa en el concepto de "shared library interceptor"]: http://rubensa.wordpress.com/2006/03/22/ubuntu-tsocks/
    "`tsocks` se basa en el concepto de "shared library interceptor""
  [conexión SSH a través del proxy SOCKS]: http://crysol.org/es/node/1355
    "conexión SSH a través del _proxy_ SOCKS"
  [ProxyCommand a nuestro archivo ~/.ssh/config]: http://www.statusq.org/archives/2008/07/03/1916/
    "`ProxyCommand` a nuestro archivo `~/.ssh/config`"
  [ProxyCommand sin utilizar netcat]: http://www.rschulz.eu/2008/09/ssh-proxycommand-without-netcat.html
    "`ProxyCommand` sin utilizar `netcat`"
  [comprobar que esta funcionalidad está soportada]: http://bugs.launchpad.net/ubuntu/+source/bash/+bug/215034/comments/15
    "comprobar que esta funcionalidad está soportada"
