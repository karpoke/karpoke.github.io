Title: Ocultando cabeceras
Date: 2011-03-12 14:26
Author: Nacho Cano
Tags: cabeceras HTTP, expose_php, php, seguridad por oscuridad, serversignature, servertokens
Slug: ocultando-cabeceras

Tras instalar Apache, tanto en las [cabeceras de la página][]:

    $ curl -I localhost
    HTTP/1.1 200 OK
    Date: Sat, 12 Mar 2011 11:55:12 GMT
    Server: Apache/2.2.16 (Ubuntu)
    Last-Modified: Sat, 02 Jan 2010 00:00:23 GMT
    ETag: "aa34-b1-47c232cbc0633"
    Accept-Ranges: bytes
    Content-Length: 177
    Vary: Accept-Encoding
    Content-Type: text/html

como en las páginas de error:

    <!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">

    404 Not Found

    Not Found
    The requested URL /terminus was not found on this server.

    Apache/2.2.16 (Ubuntu) Server at localhost Port 80

se muestra la versión de Apache, y de PHP si también lo hemos instalado.
Ocultar este tipo de información se conoce como seguridad por oscuridad,
por lo que no es realmente seguridad, pero puede ayudar a evitar ataques
automatizados.

Modificaremos las directivas `ServerTokens`, que por defecto es `OS`, y
`ServerSignature`, que por defecto es `On`. En el fichero
`/etc/apache2/cond.d/security` modificamos:

    ServerTokens ProductOnly
    ServerSignature Off

La directiva `ServerTokens` acepta varias opciones:

    ServerTokens Prod[uctOnly]
    Server sends (e.g.): Server: Apache
    ServerTokens Major
    Server sends (e.g.): Server: Apache/2
    ServerTokens Minor
    Server sends (e.g.): Server: Apache/2.0
    ServerTokens Min[imal]
    Server sends (e.g.): Server: Apache/2.0.41
    ServerTokens OS
    Server sends (e.g.): Server: Apache/2.0.41 (Unix)
    ServerTokens Full (or not specified)
    Server sends (e.g.): Server: Apache/2.0.41 (Unix) PHP/4.2.2 MyMod/1.2

Esta directiva también controla la información que proporciona la
directiva `ServerSignature`:

    Syntax: ServerSignature On|Off|EMail

Para ocultar la cabecera que muestra si tenemos instalado PHP y su
versión editamos el fichero `/etc/php5/apache2/php.ini` y mofidificamos
la variable:

    expose_php = Off

Sin embargo, después de todo esto, las cabeceras siguen mostrando que es
un Apache:

    $ curl -I localhost
    HTTP/1.1 200 OK
    Date: Sat, 12 Mar 2011 12:20:39 GMT
    Server: Apache
    Last-Modified: Sat, 02 Jan 2010 00:00:23 GMT
    ETag: "aa34-b1-47c232cbc0633"
    Accept-Ranges: bytes
    Content-Length: 177
    Vary: Accept-Encoding
    Content-Type: text/html

Una opción para evitar que aparezca es [compilar Apache][]. En el
archivo `includes/ap_release.h`, deberíamos cambiar:

    #define AP_SERVER_BASEVENDOR "Apache Software Foundation"
    #define AP_SERVER_BASEPROJECT "Apache HTTP Server"
    #define AP_SERVER_BASEPRODUCT "Apache"

* * * * *

#### Actualizado el 14 de abril de 2012

Otras opciones para modificar la cabecera `ServerTokens` o evitar que
aparezca, sin tener que compilar, son:

» [utilizar el módulo `mod_security`][utilizar el módulo mod_security]
» [utilizar Varnish][]

* * * * *

  [cabeceras de la página]: {filename}/admin/cabeceras-http-personalizadas-en-apache2.md
    "cabeceras HTTP"
  [compilar Apache]: http://www.flu-project.com/seguridad-en-los-banner-de-los-servidores-web-apache-ocultando-informacion.html
    "compilar Apache"
  [utilizar el módulo mod_security]: {filename}/admin/apache2-y-mod_security-en-ubuntu-lucid-lynx-10-04.md
    "Apache 2 y mod_security en Ubuntu Lucid Lynx 10.04"
  [utilizar Varnish]: {filename}/admin/mejorando-la-seguridad-de-apache-con-varnish.md
    "Mejorando la seguridad en Apache con Varnish"
