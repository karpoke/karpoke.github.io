Title: Evitando el hotlinking
Date: 2011-08-16 14:05
Author: Nacho Cano
Tags: apache, hotlinking, HTTP_REFERER, mod_rewrite
Slug: evitando-el-hotlinking

Si tenemos una página web que contiene imágenes, tarde o temprano,
alguien terminará mostrándolas en otro sitio, enlazándolas directamente
y utilizando nuestro ancho de banda. Vamos, lo que se conoce como
_hotlinking_.

La siguiente [técnica se basa en el valor de la variable
`HTTP_REFERER`][técnica se basa en el valor de la variable
HTTP_REFERER], la cual es opcional, por lo que podría ser posible
saltársela. Sin embargo, la mayoría de las veces impedirá el
_hotlinking_. Como contrapartida, si alguien pone un enlace a una
imagen, un usuario no podrá verla pulsando en el enlace, ya que el
navegador incluirá como _referer_ una URL externa y será bloqueada por
el sistema.


Con `mod_rewrite`
-----------------

Utilizando `mod_rewrite` tenemos varias opciones, desde denegar la
petición hasta cambiar la imagen por otra. Las directivas `RewriteCond`
y `RewriteRule` se pueden utilizar en el contexto de configuración del
servidor, `VirtualHost`, `Directory` y `.htaccess`. Deberemos tener
instalado el módulo <cde>mod_rewrite, tenerlo activado—mediante la
directiva `RewriteEngine On`—y reiniciar el servicio para que los
cambios tengan efecto.

Denegar las peticiones:

    RewriteCond %{HTTP_REFERER} !^$
    RewriteCond %{HTTP_REFERER} !www.example.com [NC]
    RewriteRule \.(gif|jpe?g|png)$ - [F,NC]

Mostrar una imagen alternativa:

    RewriteCond %{HTTP_REFERER} !^$
    RewriteCond %{HTTP_REFERER} !www.example.com [NC]
    RewriteRule \.(gif|jpe?g|png)$ /images/go-away.png [R,NC]

Redirigir la petición a una imagen de otro sitio:

    RewriteCond %{HTTP_REFERER} !^$
    RewriteCond %{HTTP_REFERER} !www.example.com [NC]
    RewriteRule \.(gif|jpe?g|png)$ http://other.example.com/image.gif [R,NC]

Si queremos [prevenir el _hotlinking_ de otro tipo de ficheros][], como
por ejemplo vídeos o ficheros de texto, tenemos que cambiar la directiva
`RewriteRule` para incluirlos:

    RewriteRule \.(gif|jpe?g|png|bmp|mov|avi|wmv|mpe?g)$ - [F]

Si queremos que sí se pueda [permitir un _hotlinkg_ desde determinados
sitios][], sólo tenemos que añadirnos con la directiva `RewriteCond`:

    RewriteCond %{HTTP_REFERER} !friendlysite\.com [NC]
    ... rest of RewriteCond’s
    RewriteCond %{HTTP_REFERER} !google\. [NC]
    RewriteCond %{HTTP_REFERER} !search\?q=cache [NC]

Por último, podemos [redirigir estas peticiones a través de un
fichero][permitir un _hotlinkg_ desde determinados sitios]. Esta
redirección se hace de forma transparente, sin que se muestre la ruta
real que incluye el fichero. Con esta técnica evitamos que, si ponen un
enlace a una imagen, luego no se pueda ver si alguien pulsa.

Para poder pasarle la imagen como parámetro al _script_, deberemos
cambiar la forma en que identificamos las imágenes:

    RewriteCond %{REQUEST_FILENAME} .*jpe?g$|.*gif$|.*png$ [NC]
    RewriteRule (.*) /showpic.php?pic=$1

Este fichero muestra una pequeña página web que contiene, además de la
imagen, un enlace a nuestro sitio:

    <?php
      // File:   showpic.php
      // Author: A List Apart
      // Web:    http://www.alistapart.com/articles/hotlinking/
      header("Content-type: text/html");
      header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
      header("Cache-Control: no-store, no-cache, must-revalidate");
      header("Cache-Control: post-check=0, pre-check=0", false);
      header("Pragma: no-cache");
      $pic = strip_tags( $_GET['pic'] );
      if ( ! $pic ) {
        die("No picture specified.");
      }
    ?>
    <html>
      <head>
        <title><?php echo($pic); ?></title>
        <meta http-equiv="Content-Type" encoding="charset=iso-8859-1">
      </head>
      <body>
        <img src="/<?php echo($pic); ?>" alt="Image">
        Image from your web site.
      </body>
    </html>

Sin `mod_rewrite`
-----------------

Si, simplemente, queremos denegar la petición, no es necesario utilizar
`mod_rewrite`:

    SetEnvIf Referer example\.com localreferer
    Order deny,allow
    Deny from all
    Allow from env=localreferer

Podemos probar si la solución funciona como queremos en el siguiente
_[hotlink tester][]_.</cde>

  [técnica se basa en el valor de la variable HTTP_REFERER]: http://httpd.apache.org/docs/2.3/rewrite/access.html
    "técnica se basa en el valor de la variable HTTP_REFERER"
  [prevenir el _hotlinking_ de otro tipo de ficheros]: http://www.besthostratings.com/articles/prevent-hot-linking.html
    "prevenir el _hotlinking_ de otro tipo de ficheros"
  [permitir un _hotlinkg_ desde determinados sitios]: http://www.alistapart.com/articles/hotlinking/
    "permitir un _hotlinkg_ desde determinados sitios"
  [hotlink tester]: http://corz.org/machine/source/php/security/hot-link-test.php
    "hotlink tester"
