Title: Imágenes embebidas en el código HTML, CSS o JSON
Date: 2011-03-06 18:34
Author: Nacho Cano
Tags: base64, css, data:URI, json, rfc2397, urldec, urlenc
Slug: imagenes-embebidas-en-el-codigo-html-css-o-json

Mediante esquema `data:URI` se pueden [incluir imágenes codificadas][]
en `base64` en el CSS de una página o en el `src` de una etiqueta `img`
como si fueran fuentes externas. También se pueden introducir otro tipo
de datos, como por ejemplo, código HTML.


```html
<img src="data:image/png;base64,iVBORw0KGgo[...]QmCC" title="image" alt="image" />
```

También se puede utilizar en un [JSON][]:

```json
{
 "image":{
  "data_uri":"data:image/png;base64,iVBORw0KGgo[...]QmCC"
 }
}
```

![Google 404]({static}/images/google-404-300x112.png)

Las ventajas de utilizar este método son que no se necesitan abrir
conexiones adicionales para decargar los datos, ya que toda la
información está incluida en el propio archivo, con lo que dejan
recursos disponibles, algo que puede ser especialmente útil en redes
inalámbricas muy saturadas o lentas, como algunas redes de telefonía
móvil, y se crean menos entradas en la caché del navegador. Además, al
estar incluidos en el código se pueden cachear.

Entre los incovenientes, se necesita procesar la imagen para poder
incluirla, los datos codificados en base 64 son hasta un 33% más
grandes, si los datos se utilizan más de una vez en el mismo documento,
deben ser incluidos cada vez, por lo que no se aprovecha la caché del
navegador, la URL tiene un máximo relativamente pequeño y diferente para
cada navegador y, por último, aunque los navegadores más populares lo
soporten, no

Codificar la imagen
-------------------

Para codificar una imagen podemos utilizar el comando `base64`. El
argumento `-w0` es para que devuelva el resultado en una sola línea:

```bash
$ base64 -w0 img.png > img.b64
```

Sin embargo, este formato [no es apropiado para URL][], ya que contiene
caracteres como `+`, `/` o `=`, por lo que [codificaremos][] la salida
del comando anterior para que lo sea:

```bash
$ alias urlenc='furlenc() { perl -MURI::Escape -e "print uri_escape(\"$1\").\"\n\";"; }; furlenc'
$ urlenc $(base64 -w0 img.png) > img.b64
```

Decodificar una imagen
----------------------

Para realizar el paso inverso, obtener la imagen a partir del código en
la página, guardaremos en un fichero, por ejemplo `img.b64`, el código
en `base64` referente a la imagen:

```bash
alias urldec='furldec() { echo "$1" | sed -e'\''s/%\([0-9A-F][0-9A-F]\)/\\\\\x\1/g'\'' | xargs echo -e; }; furldec'
$ urldec $(cat img.b64) | base64 -d > img.png
```

  [incluir imágenes codificadas]: http://mark.koli.ch/2009/07/howto-include-binary-image-data-in-cascading-style-sheets-css.html
    "incluir imágenes codificadas"
  [JSON]: http://mark.koli.ch/2011/01/more-fun-with-rfc-2397----the-data-url-scheme.html
    "JSON"
  [no es apropiado para URL]: http://es.wikipedia.org/wiki/Base64#Aplicaciones_en_URL
    "no es apropiado para URL"
  [codificaremos]: {filename}/dev/urlencode-y-urldecode.md
    "codificaremos"
    "urlencode y urldecode"
