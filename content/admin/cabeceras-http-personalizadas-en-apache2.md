Title: Cabeceras HTTP personalizadas en Apache2
Date: 2011-02-28 20:28
Author: Nacho Cano
Tags: barrapunto, curl, header, mod_headers, requestheader, virtualhost, wordpress, X-Robots-Tag
Slug: cabeceras-http-personalizadas-en-apache2

Podemos modificar las cabeceras que devuelve el Apache usando el módulo
`mod_headers`. Por ejemplo, añadiendo a nuestro _virtualhost_:

    Header set X-MyHeader "It took %D microseconds to serve this page."

Se pueden modificar tanto las cabeceras que van a ser enviadas, con la
directiva `Header`, como las que vienen con una petición, con la
directiva `RequestHeader`. Las acciones que se pueden llevar a cabo son:

-   `set`, especifica el valor de la cabecera, la crea si no existía o
    la modifica en caso contrario
-   `append`, añade el valor al final de la cabecera existente, y separa
    los valores por comas
-   `add`, añade una cabecera, duplicando la cabecera si ésta ya existía
-   `unset`, elimina una cabecera
-   `echo`, sólo en el caso de la directiva `Header`, y permite utilizar
    el valor de una cabecera en el `request`

Este es el resultado:

    $ curl -I localhost

    HTTP/1.1 200 OK
    Date: Mon, 28 Feb 2011 18:01:45 GMT
    Server: Apache/2.2.14 (Ubuntu)
    X-Powered-By: PHP/5.3.2-1ubuntu4.7
    X-MyHeader: It took D=632 microsecons to serve this page.
    Vary: Accept-Encoding
    Content-Type: text/html

Hay algunas páginas web que incluyen [cabeceras no estándar][], como la
mostrada arriba, tales como:

    $ curl -I http://ww.barrapunto.com
    ...
    X-Bender: Hey Fry, I’m steering with my ass!

    $ curl -I wordpress.com
    ...
    X-hacker: If you’re reading this, you should visit automattic.com/jobs and apply to join the fun, mention this header.
    X-nananana: Batcache

* * * * *

#### Actualizado el 10 de febrero de 2015

Una cabecera que nos puede resultar interesante añadir es la de
`X-Robots-Tag`, por ejemplo para [evitar que los buscadores indexen el
contenido del fichero robots.txt][]:

    Header set X-Robots-Tag "noindex"

En esta página, podemos encontrar [las especificaciones de esta
cabecera][].

* * * * *

  [cabeceras no estándar]: {filename}/admin/cabeceras-http-personalizadas-en-apache2.md
    "cabeceras no estándar"
  [evitar que los buscadores indexen el contenido del fichero robots.txt]: http://www.elladodelmal.com/2015/02/como-eliminar-la-indexacion-de.html
    "evitar que los buscadores indexen el contenido del fichero robots.txt"
  [las especificaciones de esta cabecera]: https://developers.google.com/webmasters/control-crawl-index/docs/robots_meta_tag
    "las especificaciones de esta cabecera"
