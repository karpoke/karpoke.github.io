Title: CSRF en las búsquedas de Google
Date: 2010-12-13 14:31
Author: Nacho Cano
Tags: csrf, google
Slug: csrf-en-las-busquedas-de-google

> No se ha encontrado ningún resultado

![No injury is acceptable]({static}/images/no-injury-is-acceptable-300x233.jpg)


Si ahora mismo tienes una sesión de Google iniciada, puedes ir al
[histórico de búsquedas de Google][] y verás que aparece una búsqueda
que no has realizado... conscientemente.

El truco, un ataque [CSRF][] comentado por [Jeremiah Grossman][],
consiste en añadir en el código HTML de la página una imagen cuyo `src`
sea la URL de la búsqueda que queramos que realice el que visite la
página. Por ejemplo:

<img src="http://www.google.es/search?q=%22terminus.ignaciocano.com%22" border="0" height="0" width="0">

```html
<img src="http://www.google.es/search?q=%22terminus.ignaciocano.com%22" border="0" height="0" width="0">
```

  [histórico de búsquedas de Google]: http://google.com/history
    "histórico de búsquedas de Google"
  [CSRF]: http://en.wikipedia.org/wiki/Cross-site_request_forgery
    "CSRF"
  [Jeremiah Grossman]: http://jeremiahgrossman.blogspot.com/2010/12/spoofing-google-search-history-with.html
    "Jeremiah Grossman"
