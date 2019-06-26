Title: Facebook y el RSS de las páginas
Date: 2011-10-10 17:05
Author: Nacho Cano
Tags: atom, facebook, feed, rss
Slug: facebook-y-el-rss-de-las-paginas
Related: twitter-y-el-rss-de-las-cuentas-de-usuario

Si queremos [seguir las actualizaciones de una página de Facebook][], no
tenemos más que copiar el ID de la página y sustituirlo en la siguiente
URL, en este caso en formato Atom 1.0:

```bash
http://www.facebook.com/feeds/page.php?format=atom10&id=xxxxxxxxxxxx
```

O la siguiente, para usar el formato RSS 2.0:

```bash
http://www.facebook.com/feeds/page.php?format=rss20&id=xxxxxxxxxxxx
```

Por ejemplo, para añadir el RSS de la página de Amstrad ESP,
[http://www.facebook.com/pages/Amstrad-ESP/__72227918057__][], no
tenemos más que utilizar la siguiente URL:

[http://www.facebook.com/feeds/page.php?format=rss20&id=__72227918057__][]

  [seguir las actualizaciones de una página de Facebook]: http://rubenbaston.org/rss-paginas-facebook/
    "seguir las actualizaciones de una página de Facebook"
  [http://www.facebook.com/pages/Amstrad-ESP/__72227918057__]: http://www.facebook.com/pages/Amstrad-ESP/72227918057
    "Amstrad ESP"
  [http://www.facebook.com/feeds/page.php?format=rss20&id=__72227918057__]:
    http://www.facebook.com/feeds/page.php?format=rss20&id=72227918057
    "Amstrad ESP. Facebook Page RSS"
