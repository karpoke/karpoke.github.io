Title: Mejorando la seguridad de Apache con Varnish
Date: 2011-05-26 19:39
Author: Nacho Cano
Tags: apache, cabeceras HTTP, seguridad por oscuridad, servidor http, varnish, w00tw00t
Slug: mejorando-la-seguridad-de-apache-con-varnish

[Varnish][] es un acelerador web, que puede ser utilizado tanto para
cachear contenido estático de nuestro servidor, para balancear la carga
o [para incrementar la seguridad][], por ejemplo, bloqueando cierto tipo
de peticiones u ocultando cierto tipo de información.

Se instala directamente de los repositorios:

```bash
$ sudo aptitude install varnish
```

Ahora lo configuraremos para utilizarlo como capa intermedia, delante de
nuestro Apache. Editamos el fichero `/etc/default/varnish` y cambiamos:

```bash
DAEMON_OPTS="-a :6081
            -T localhost:6082
            -f /etc/varnish/default.vcl
            -S /etc/varnish/secret
            -s file,/var/lib/varnish/$INSTANCE/varnish_storage.bin,1G"
```

por:

```bash
DAEMON_OPTS="-a :80
            -T localhost:6082
            -f /etc/varnish/000-default.vcl
            -S /etc/varnish/secret
            -s file,/var/lib/varnish/$INSTANCE/varnish_storage.bin,1G"
```

En el fichero `/etc/varnish/000-default.vcl` específicamos las reglas
que queremos aplicar a las peticiones que le van a llegar a Apache.
Podemos [eliminar][] [cabeceras][] o [modificarlas][], por ejemplo,
[cambiando el nombre][] y la versión de Apache. Conviene recordar que
cambiar el nombre del servidor, no lo hace más seguro.

También podemos descartar peticiones que cumplan algún criterio, por
ejemplo que contenga la cadena ["w00tw00t"][].

```bash
## Redirect requests to Apache, running on port 8000 on localhost
backend apache {
        .host = "127.0.0.1";
        .port = "8080";
}
## Fetch
sub vcl_fetch {
        ## Change server signature
        unset obj.http.Server;
        set obj.http.Server = "Unknown";

    ## Remove the X-Forwarded-For header if it exists.
        remove req.http.X-Forwarded-For;

    ## insert the client IP address as X-Forwarded-For. This is the normal IP address of the user.
        set req.http.X-Forwarded-For = req.http.rlnclientipaddr;

    ## Added security, the "w00tw00t" attacks are pretty annoying so lets block it before it reaches our webserver
        if (req.url ~ "^/w00tw00t") {
               error 403 "Not permitted";
        }

    ## Deliver the content
        return(deliver);
}

## Deliver
sub vcl_deliver {
    ## We'll be hiding some headers added by Varnish. We want to make sure people are not seeing we're using Varnish.
        ## Since we're not caching (yet), why bother telling people we use it?
        remove resp.http.X-Varnish;
        remove resp.http.Via;
        remove resp.http.Age;

    ## We'd like to hide the X-Powered-By headers. Nobody has to know we can run PHP and have version xyz of it.
        remove resp.http.X-Powered-By;
}
```

Ahora, cambiamos el puerto en el que escucha Apache, editando el fichero
`/etc/apache2/ports.conf`:

```bash
NameVirtualHost *:8080
Listen 127.0.0.1:8080
```

También debemos editamos nuestros _hosts_ virtuales, por ejemplo,
`/etc/apache2/sites-enabled/default`, y cambiamos:

```bash
```

por:

```bash
```

Tras hacer este cambio, el único que «hablará» con Apache será Varnish,
por lo que la única IP que veremos será la `127.0.0.1`. Instalaremos un
módulo extra de Apache para asegurarnos de que la IP es la correcta:

```bash
$ sudo aptitude install libapache2-mod-rpaf
$ sudo a2enmod rpaf
```

RPAF (Reverse Proxy Add Forward) reemplazará la IP por la que Varnish
habrá puesto en la cabecera `X-Forwarded-For`.

Reiniciamos los servicios:

```bash
$ sudo service apache2 restart
$ sudo service varnish restart
```

Si todo ha ido bien, Varnish deberá estar escuchando en el puerto 80 y
Apache en el 8080:

```bash
$ sudo netstat -lp | grep apache2
tcp        0      0 localhost:http-alt      _:_                ESCUCHAR    2587/apache2
```

```bash
$ sudo netstat -lp | grep varnishd
tcp        0      0 _:www                   *:_                ESCUCHAR    9452/varnishd
tcp        0      0 localhost:6082          _:_                ESCUCHAR    9451/varnishd
tcp6       0      0 [::]:www                [::]:*             ESCUCHAR    9452/varnishd
```

_Previously_
------------

» [Cabeceras HTTP][]
» [Ocultando cabeceras][]
» [Cabeceras HTTPS personalizadas en Apache2][]
» [w00tw00t]["w00tw00t"] en los logs de Apache

  [Varnish]: http://www.varnish-cache.org/docs/2.1/
    "Varnish"
  [para incrementar la seguridad]: http://www.howtoforge.com/putting-varnish-in-front-of-apache-on-ubuntu-debian
    "para incrementar la seguridad"
  [eliminar]: {filename}/admin/ocultando-cabeceras.md
    "eliminar"
    "ocultando cabeceras en Apache"
  [cabeceras]: {filename}/admin/cabeceras-http-personalizadas-en-apache2.md
    "cabeceras"
    "cabeceras http"
  [modificarlas]: {filename}/admin/cabeceras-http-personalizadas-en-apache2.md
    "modificarlas"
    "Cabeceras HTTP personalizadas en Apache2"
  [cambiando el nombre]: http://www.varnish-cache.org/trac/wiki/VCLExampleDisguiseServer
    "cambiando el nombre"
  ["w00tw00t"]: {filename}/admin/w00t-w00t.md
    ""w00tw00t""
    "w00tw00t"
  [Cabeceras HTTP]: {filename}/admin/cabeceras-http-personalizadas-en-apache2.md
    "Cabeceras HTTP"
    "Cabeceras HTTP"
  [Ocultando cabeceras]: {filename}/admin/ocultando-cabeceras.md
    "Ocultando cabeceras"
    "Ocultando cabeceras"
  [Cabeceras HTTPS personalizadas en Apache2]: {filename}/admin/cabeceras-http-personalizadas-en-apache2.md
    "Cabeceras HTTPS personalizadas en Apache2"
    "Cabeceras HTTPS personalizadas en Apache2"
