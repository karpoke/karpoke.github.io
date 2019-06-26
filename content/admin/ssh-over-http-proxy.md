Title: SSH over HTTP-Proxy
Date: 2011-08-15 04:29
Author: Nacho Cano
Tags: apache, corkscrew, htc, http, HTTP_PROXY, https, proxy, proxy http, proxy socks, proxytunnel, SOCKS, ssh, varnish
Slug: ssh-over-http-proxy
Related: utilizar-ssh-para-establecer-un-servidor-proxy-socks

A veces, queremos poder navegar o chatear por Internet pero no queremos
que nadie pueda conocer, ni bloquear, las páginas que visitamos o espiar
nuestras conversaciones, bien porque porque estamos en el trabajo, la
universidad o en una red abierta. En la red a la que estamos conectados
puede que utilicen un _proxy_ para controlar y bloquear servicios. Este
[bloqueo podría ser por puerto o por protocolo][].

Es posible que bloqueen algunas URLs, o IPs, pero seguramente tenemos
acceso a la web, es decir, los puertos 80 y 443. Crearemos un túnel
seguro para poder navegar seguros y evitar estas restricciones. Eso sí,
puede que aparezca en algún _log_ que nos hemos conectado a nuestra
máquina remota.


_Proxy_ SOCKS
-------------

Una manera de montar un túnel seguro es mediante un [_proxy_ SOCKS][proxy SOCKS].
Aprovechamos el hecho de que el puerto 443 no está bloqueado.

En nuestro servidor remoto, podemos configurar `openssh` para que
escuche en el puerto 443, añadiendo un `Listen 443` al fichero
`/etc/ssh/sshd_config`. Pero si ya tenemos un servidor web, [por ejemplo
`apache2`, que sirve conexiones seguras][por ejemplo
apache2, que sirve conexiones seguras], podemos hacer uso de `sslh`,
que permite que ambos servicios, [SSL y SSH, compartan el puerto 443][].

En nuestra máquina, lo primero que haremos será configurar `ssh` para
que pueda [pasar a través del _proxy_][pasar a través del proxy]
maligno que nos obligan a usar,
mediante `corkscrew` -está en los repositorios-. Editamos el fichero
`~/.ssh/config`, y añadimos:

```bash
ProxyCommand /usr/local/bin/corkscrew proxy.evil.com 80 %h %p
```

En lugar de `corkscrew`, podríamos utilizar `proxytunnel`:

```bash
ProxyCommand proxytunnel -v -p proxy.evil.com:80 -r remotehost:443 -d %h:%p -H "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Win32)\n"
```

Ahora ya podemos crear el _proxy_ SOCKS desde nuestra máquina local:

```bash
$ ssh -f -N -D 1080 user@remotehost
```

Si no estamos obligados a utilizar un _proxy_, no hace falta que
editemos el fichero `~/.ssh/config`, y el _proxy_ SOCKS se crea
ejecutando el mismo comando que acabamos de lanzar.

Sólo queda configurar alguna aplicación, por ejemplo Firefox. Vamos al
`Menú Editar > Preferencias > Avanzado > Red > Configuración de la conexión > Configuración manual del proxy`
y ponemos:

```bash
Servidor SOCKS: localhost
Puerto:         1080
```

Y listos.

SSH over HTTP-Proxy
-------------------

Otra manera de hacerlo es a través de un _proxy_ HTTP. En nuestra
máquina remota, vamos a configurar Apache para que haga de _proxy_ HTTP.

Activamos el módulo:

```bash
$ sudo a2enmod proxy_http
```

Podemos realizar la configuración a nivel de módulo o de VirtualHost.
Tener un _proxy_ HTTP que redirija peticiones, mediante la directiva
`ProxyRequests`, [puede ser un peligro][], dado que, mal configurado,
podría permitir que cualquiera accediera a través de nosotros ocultando
su identidad. Utilizar un _proxy_ inverso, mediante la directiva
`ProxyPass` y la directiva `ProxyRequests Off`, es menos crítico, porque
los clientes sólo pueden conectar a los sitios que hemos configurado
específicamente.

Limitaremos el acceso para sólo permitirlo desde la propia máquina o
desde una conexión SSH. Editamos el fichero
`/etc/apache2/mods-enabled/proxy.conf`:

```bash
Listen 889
ProxyRequests On
AllowCONNECT 22
ProxyVia On

Order deny,allow
Deny from all
Allow from 127.0.0.1
```

Por un lado, el _proxy_ no está escucha en el puerto por defecto, el
8080, sino que lo hace en el 889. Además, este puerto no está abierto ni
el firewall ni en el router. El motivo de este cambio de puerto es que
en la máquina remota tenía instalado Varnish, que es un acelerador web,
que puede ser utilizado tanto para cachear contenido estático, como para
balancear la carga o para [incrementar la seguridad de nuestro servidor
web][]. Sin embargo, en este caso, esto no supondrá ningún problema.

Por otro, permitimos el método CONNECT al puerto 22, donde corre SSH, y
permitimos el acceso únicamente desde la propia máquina. Una vez hechos
los cambios, no olvidemos reiniciar el servidor web.

Ahora ya podemos crear el túnel desde nuestra máquina; redirigiremos el
puerto remoto 889 a nuestro puerto local 8080, realizando la conexión
por SSH en el puerto remoto 443:

```bash
$ ssh -L 8080:localhost:889 user@server.at.home -p 443
```

Igual que en el caso anterior, si tenemos que utilizar de forma
obligatoria el _proxy_ maligno, editamos el fichero `~/.ssh/config`:

```bash
ProxyCommand /usr/local/bin/corkscrew proxy.evil.com 80 %h %p
```

Para configurar Firefox, vamos al
Menú Editar > Preferencias > Avanzado > Red > Configuración de la conexión > Configuración manual del _proxy_
y ponemos:

```bash
HTTP Proxy: localhost (Usar este servidor proxy para todos los protocolos)
Puerto:     8080
```

Si queremos configurar que se use el _proxy_ desde el terminal, en
aquellos programas que utilizan la variable de entorno `HTTP_PROXY`:

```bash
$ export HTTP_PROXY='http://localhost:8080/'
```

Y para quitarlo:

```bash
$ export HTTP_PROXY=''
```

Tanto desde Firefox como desde el terminal, podríamos haber puesto la
IP, o el nombre, de un equipo remoto que tenga abierto un _proxy_ HTTP.

Sin utilizar el método CONNECT
------------------------------

Si no podemos utilizar el método [CONNECT][] para conectarnos al puerto
443 de nuestra máquina remota, podemos probar a cambiar de puerto, por
si hubiera alguno permitido.

Si no encontramos ninguno, todavía podemos establecer un túnel
utilizando HTTP mediante `httptunnel` -también está en los
repositorios-. Consta de dos programas, un cliente y un servidor. En
nuestra máquina remota, ejecutamos el servidor, redirigiendo el puerto
80 al 22. En este caso, si ya teníamos instalado Varnish, deberemos
utilizar otro puerto, y abrirlo en el firewall.

```bash
$ hts -F localhost:22 80
```

En nuestra máquina local ejecutaremos el cliente, que redirige el puerto
local 8080 al puerto remoto 80, que a su vez es redirigido al puerto 22
remoto, utilizando el _proxy_ maligno obligatorio de la red a la que nos
conectamos:

```bash
$ htc -P proxy.evil.com:80 -F 8080 remotehost:80
```

Referencias
-----------

- [SSH Through or Over Proxy][]
- [Accessing Trillian Pro Remotely and Through an Encrypted
Tunnel][bloqueo podría ser por puerto o por protocolo]
- [Using Corkscrew to tunnel SSH over HTTP][pasar a través del
proxy]
- [Tunneling SSH over HTTP(S)][]
- [Bypass Any Firewall][]
- [SSHThroughHTTPProxy][]
- [Tunneling SSH over an HTTP-Proxy Server][]
- [Apache Module mod_proxy][]

  [bloqueo podría ser por puerto o por protocolo]: http://ha.ckers.org/trillianremote.html
    "bloqueo podría ser por puerto o por protocolo"
  [proxySOCKS]: {filename}/admin/utilizar-ssh-para-establecer-un-servidor-proxy-socks.md
    "Utilizar SSH para establecer un servidor proxy SOCKS"
  [por ejemplo apache2, que sirve conexiones seguras]: {filename}/admin/configurar-apache-para-servir-conexiones-seguras.md
    "configurar Apache para servir conexiones seguras"
  [SSL y SSH, compartan el puerto 443]: {filename}/admin/sslh-compartiendo-el-puerto-443.md
    "sslh, compartiendo el puerto 443"
  [pasar a través del proxy]: http://www.techrepublic.com/blog/opensource/using-corkscrew-to-tunnel-ssh-over-http/962
    "pasar a través del _proxy_"
  [puede ser un peligro]: http://httpd.apache.org/docs/2.4/mod/mod_proxy.html#access
    "puede ser un peligro"
  [incrementar la seguridad de nuestro servidor web]: {filename}/admin/mejorando-la-seguridad-de-apache-con-varnish.md
    "mejorando la seguridad de apache con varnish"
  [CONNECT]: http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html
    "CONNECT"
  [SSH Through or Over Proxy]: http://daniel.haxx.se/docs/sshproxy.html
    "SSH Through or Over Proxy"
  [Tunneling SSH over HTTP(S)]: http://dag.wieers.com/howto/ssh-http-tunneling/
    "Tunneling SSH over HTTP(S)"
  [Bypass Any Firewall]: http://www.saulchristie.com/how-to/bypass-firewalls
    "Bypass Any Firewall"
  [SSHThroughHTTPProxy]: http://shsc.info/SSHThroughHTTPProxy
    "SSHThroughHTTPProxy"
  [Tunneling SSH over an HTTP-Proxy Server]: http://www.mtu.net/~engstrom/ssh-proxy.php
    "Tunneling SSH over an HTTP-Proxy Server"
  [Apache Module mod_proxy]: http://httpd.apache.org/docs/2.0/mod/mod_proxy.html
    "Apache Module mod_proxy"
