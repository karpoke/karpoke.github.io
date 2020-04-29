Title: Póster casero
Date: 2010-12-11 02:52
Author: Nacho Cano
Tags: convert, mapa del software libre, pdfposter, póster, ubuntu one
Slug: poster-casero

Si tenemos una imagen y queremos crear un póster impreso (y montado a
base de folios) por nosotros mismos podemos utilizar un servicio como
[Block posters][]. También podemos utilizar los comandos `convert` y
`pdfposter` para conseguir lo mismo.

![Mapa del Software Libre - 03.02.2010 - René Mérou]({static}/images/Mapa-del-Software-Libre-03.02.2010-René-Mérou-300x211.png)

Primero creamos un PDF a partir de la imagen, en este caso del [mapa del
software libre][]:

    $ convert mapa-del-software-libre.png mapa-del-software-libre.pdf

Ahora ya podemos crear el póster:

    $ pdfposter -mA4 -pA0 mapa-del-software-libre.pdf poster-del-mapa-del-software-libre.pdf

El argumento `-m` indica el tamaño del medio en que se va a imprimir, en
este caso el tamaño es A4. El argumento `-p` indica el tamaño deseado, en
este caso, A0. Hay otras combinaciones comentadas en la página del
manual de `pdfposter`.

La imagen, el PDF y el póster que he utilizado de ejemplo se pueden
encontrar en mi [directorio público][] de [Ubuntu One][].

  [Block posters]: http://www.hogargeek.com/posters-de-hagalo-usted-mismo-con-block-posters/
    "Block posters"
  [mapa del software libre]: http://www.es.gnu.org/~reneme/fsmap/
    "mapa del software libre"
  [directorio público]: {filename}/admin/como-publicar-directorios-en-ubuntu-one-y-dropbox.md
    "directorio público"
  [Ubuntu One]: http://ubuntuone.com/p/NoU/
    "Ubuntu One"
