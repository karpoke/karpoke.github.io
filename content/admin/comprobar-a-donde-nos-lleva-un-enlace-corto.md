Title: Comprobar a dónde nos lleva un enlace corto
Date: 2011-05-07 12:54
Author: Nacho Cano
Tags: curl
Slug: comprobar-a-donde-nos-lleva-un-enlace-corto

Un enlace corto es útil, por ejemplo, para incluir la dirección de una
página web en servicios como [Twitter][], donde el número de caracteres
está limitado. Sin embargo, se pueden utilizar para engañarnos y
llevarnos a una página que no queramos, o incluso que [distribuya
_malware_][distribuya malware].

![Firefox Seguridad Filtro Web](/images/firefox_seguridad_filtro_web.jpg)

Para comprobar hacia dónde apunta un enlaces cortos podemos:

-   utilizar un servicio como [urlxray][]
-   utilizar el comando `curl`:

    $ curl -sI http://goo.gl/GPb7Z | grep Location
    Location: http://terminus.homelinux.com/k/

-   utilizar un complemento para [Firefox][]

  [Twitter]: {filename}/hack/robando-la-identidad-del-vecino.md
    "robando la identidad del vecino"
  [distribuya malware]: http://www.worsttech.com/hack/hacker-attack/malware-spreading-via-shortened-urls-1102581.html
    "distribuya malware"
  [urlxray]: http://urlxray.com/
    "urlxray"
  [Firefox]: http://addons.mozilla.org/en-US/firefox/search/?q=short+url+expand
    "Firefox"
