Title: Twitter y el RSS de las cuentas de usuario
Date: 2011-09-30 00:17
Author: Nacho Cano
Tags: rss, shebang, twitter
Slug: twitter-y-el-rss-de-las-cuentas-de-usuario

Desde hace un tiempo, parece que Twitter ha ido [ocultando la
posibilidad de seguir una cuenta a través de RSS][]. Han aparecido
algunos [servicios que intentan corregir este comportamiento][], aunque
realmente no son necesarios.

Para seguir a un usuario a través del RSS lo único que tenemos que hacer
es eliminar el _[shebang][]_ de la URL, es decir, el `#!`. Por ejemplo,
para seguir a [DragonJAR][], muy recomendable, deberíamos usar la URL:
<http://twitter.com/DragonJAR>, en lugar de
<http://twitter.com/#!/DragonJAR>.

Si ponemos esa URL en un navegador, nos redirecciona a la URL con el
_shebang_, pero si la descargamos, podemos ver que ahí están definidos
los enlaces a los RSS de los _tweets_ del usuario y de sus favoritos:

    $ curl -s http://twitter.com/DragonJAR | grep link.*rss+xml

  [ocultando la posibilidad de seguir una cuenta a través de RSS]: http://www.genbeta.com/sindicacion/facebook-y-twitter-eliminan-silenciosamente-sus-canales-de-suscripcion-rss#
    "ocultando la posibilidad de seguir una cuenta a través de RSS"
  [servicios que intentan corregir este comportamiento]: http://www.genbeta.com/sindicacion/sigue-cuentas-de-twitter-en-tu-lector-de-feeds-con-twitter-to-rss
    "servicios que intentan corregir este comportamiento"
  [shebang]: http://en.wikipedia.org/wiki/Shebang_(Unix)
    "shebang"
  [DragonJAR]: http://www.dragonjar.org/
    "DragonJAR"
