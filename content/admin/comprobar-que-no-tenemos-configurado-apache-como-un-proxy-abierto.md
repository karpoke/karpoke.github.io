Title: Comprobar que no tenemos configurado Apache como un proxy abierto
Date: 2012-09-21 16:53
Author: Nacho Cano
Tags: apache, proxy, telnet
Slug: comprobar-que-no-tenemos-configurado-apache-como-un-proxy-abierto
Related: ssh-over-http-proxy,mejorando-la-seguridad-de-apache-con-varnish

Revistando _logs_ de Apache, he visto que tenía algunas entradas del
tipo:

```bash
93.174.93.52 - - [18/Sep/2012:02:23:11 +0200] "GET http://myproxylists.com/my-http-headers HTTP/1.1" 404 1046 "-" "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.28) Gecko/20120306 Firefox/3.6.28 (.NET CLR 3.5.30729)"
93.174.93.52 - - [20/Sep/2012:08:21:08 +0200] "GET http://myproxylists.com/my-http-headers HTTP/1.1" 404 1046 "-" "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.28) Gecko/20120306 Firefox/3.6.28 (.NET CLR 3.5.30729)"
```

Este suele ser el resultado de peticiones maliciosas que buscan
encontrar servidores _proxy_ abiertos. Si encontramos entradas de este
tipo, lo primero que deberíamos hacer es comprobar que tenemos
configurado el servidor correctamente, para no permitir hacer de _proxy_
a peticiones de anónimos. De hecho, si no necesitamos un servidor
_proxy_, lo mejor es asegurarnos que la directiva `ProxyRequests` no
está inicializada a `on`.

Si el servidor está bien configurado, este tipo de peticiones fallarán,
y se verá un código 404 en el _log_. Un código 200 no significa
necesariamente que esté mal configurado. Si no hemos configurado el
nombre del servidor, Apache aceptará peticiones de URLs absolutas, ya
que no tiene forma de saber bajo qué nombres de dominio se ejecuta. Para
prevenirlo, podemos utilizar las directivas `ServerName` y `ServerAlias`
para que las peticiones de otros dominios sean rechazadas.

Si queremos comprobar si nuestro servidor está haciendo de _proxy_
podemos ejecutar:

```bash
$ telnet localhost 80
GET http://www.google.com HTTP/1.1
Host: www.google.com
```

Referencias
-----------

» [Apache Server Frequently Asked Questions][]
» [HTTP Wiki - Proxy abuse][]

  [Apache Server Frequently Asked Questions]: https://httpd.apache.org/docs/1.3/misc/FAQ.html#proxyscan
    "Apache Server Frequently Asked Questions"
  [HTTP Wiki - Proxy abuse]: https://wiki.apache.org/httpd/ProxyAbuse
    "HTTP Wiki - Proxy abuse"
