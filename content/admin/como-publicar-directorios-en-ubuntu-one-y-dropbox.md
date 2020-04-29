Title: Cómo publicar directorios en Ubuntu One y Dropbox
Date: 2010-10-31 06:28
Author: Nacho Cano
Tags: almacenamiento en la nube, compartir, dropbox, licencia de uso, privacidad, python, script, software libre, términos del servicio, u1sdtool, ubuntu one
Slug: como-publicar-directorios-en-ubuntu-one-y-dropbox

[Ubuntu One][] es el servicio que ofrece Ubuntu en la nube. Entre otras
cosas, como [sincronizar archivos de configuración o nuestros
favoritos][], permite [compartir archivos y directorios][] de nuestro
espacio en la nube con las personas que queramos de una forma sencilla.

Tambíen permite publicar archivos, para cada uno de los cuales se genera
una URL corta, y que sean accesibles por cualquiera. Sin embargo, [no
permite publicar directorios][], al menos por ahora.


¿Publicar directorios?
----------------------

¿Qué querríamos conseguir publicando un directorio? Pues que todos los
ficheros que contuviera se hicieran públicos, y que se generase un
índice, por ejemplo, un `index.html`, también público, con enlaces a
cada fichero contenido en dicho directorio (recordemos que los enlaces
son URLs cortas, no el nombre del fichero).

¿URLs cortas?
-------------

Cuando se publica un fichero, el sistema le asigna una dirección del
estilo `http://ubuntuone.com/p/N21/`, por lo que no podemos crear un
listado de ficheros basándonos en su nombre y situación relativa al
fichero `index.html`. Es decir, no podemos incluir enlaces como
`<a href="./articles/index.html">articles<a>.`

Alternativa: ¿Dropbox?
----------------------

Un servicio similar a Ubuntu One es Dropbox, que tampoco permite
publicar directorios, al menos directamente, pero el problema anterior
queda resuelto, ya que no tiene el inconveniente de las URLs cortas.
Basta crear un fichero HTML con enlaces relativos a los ficheros que
queramos ofrecer. Se podría crear un [listado][] con el comando
</code>`tree`:

    $ tree -C --charset utf8 --dirsfirst -F -H . -o tree.html

Sin embargo, esto tiene un problema, y es que si se pulsa en el enlace
de un directorio, obtenemos como resultado que el archivo no existe, ya
que `tree` crea los enlaces a directorios como `./articles/` (Dropbox
tampoco permite publicar directorios). Una sencilla solución sería crear
ficheros `index.html` en cada directorio y que los enlaces a los
subdirectorios realmente apuntasen a los ficheros `index.html` que éstos
contienen. Esto es lo que hace [DropboxIndex][], un _script_ creado por
Wojciech 'KosciaK' Pietrzok que genera un archivo `index.html` en la
raíz y en cada subdirectorio, con un aspecto similar al listado de
ficheros de Apache.

El contenido público, por defecto, se encuentra a partir del directorio
`~/Dropbox/Public` y es posible utilizar enlaces simbólicos que apunten
a directorios externos al directorio público.

De todas formas, un __gran inconveniente__ que le veo a Dropbox es que,
para gestionarlo desde el escritorio, es necesario instalarse software
privativo.

Alternativa: ¿Ubunu One?
------------------------

Ubuntu One [también tiene partes del servidor que son software
privativo][], pero parece que, al menos, [el cliente y los protocolos de
comunicación son libres][] (también se dice algo [aquí][]).

¿Y las URLs cortas?
-------------------

Existe un comando, [u1sdtool][], que permite gestionar nuestro espacio
en la nube desde el terminal. Con `u1sdtool` y partiendo del _script_
anterior, he conseguido que se puedan [publicar directorios en Ubuntu
One][]. Lo único que se necesita para acceder al directorio, o jerarquía
de directorios, es conocer la [dirección pública del directorio raíz][]
que hemos publicado.

Podemos tener tantos directorios raíz como queramos, siempre que no esté
contenido uno dentro de otro, ya que sería éste otro el que sería el
directorio raíz. Aún así, se pueden compartir enlaces de directorios
públicos intermedios, pero teniendo en cuenta que aparece un enlace para
ir subiendo en la jerarquía de directorios hasta llegar al directorio
raíz.

![UbuntuOne Index]({static}/images/ubuntuone-index-300x89.png)

ubuntuone-index.py
------------------

Se utiliza exactamente igual que el _script_ para Dropbox:

    Usage: ubuntuone-index.py [options] directory

    Options:
      -h, --help            Show help message and exit.
      -V, --version         print version information
      -R, --recursive       Include subdirectories (disabled by default).
      -T, --template file   Use HTML file as template.

    ATTENTION:
      Script will overwrite any existing index.html file(s)!

Por ejemplo:

    $ ubuntuone-index.py -R "~/Ubuntu One/pub"

Descarga el _script_ [ubuntuone-index.py][publicar directorios en Ubuntu
One].

Para más información de [cómo crear las plantillas
personalizadas][DropboxIndex] podéis visitar la web del proyecto
DropboxIndex.

Privacidad y términos del servicio
----------------------------------

Si lo he entendido bien, en su [política de privacidad][] advierten de
que obtienen datos del uso que hagamos del servicio, que puede que nos
envíen algun correo electrónico ocasionalmente, que posiblemente le pasarán esa
información a terceros, aunque intentarán que esos terceros sean buena
gente con esos datos, y, lo más interesante, que si violas los términos
del servicio, lo tienen todo registrado.

Se violan los términos del servicio haciendo algo ilegal o en contra de
los derechos o la privacidad de alguien, pudiendo incluso tener que
indemnizar a Canonical por posibles daños y perjuicios, y aquí ya no
dicen nada de sí te avisan o si primero borran los datos y luego te
avisan

La [licencia de uso de Ubuntu One][] advierte de diferentes maneras de
terminar el uso del servicio:

-   por que lo dicen ellos, aunque se supone que te avisan con un mes de
    antelación de que borrarán nuestros datos
-   por que pasamos de su servicio y no lo hemos usado en 3 meses;
    también avisan con antelación
-   por que violas los términos del servicio

Por mi parte, __todo__ lo que he subido a [mi directorio][dirección
pública del directorio raíz] para hacer las pruebas es contenido, muy
bueno, con una licencia libre, que autoriza su redistribución.

  [Ubuntu One]: http://one.ubuntu.com/
    "Ubuntu One"
  [sincronizar archivos de configuración o nuestros favoritos]: http://wiki.ubuntu.com/UbuntuOne/Tutorials/
    "sincronizar archivos de configuración o nuestros favoritos"
  [compartir archivos y directorios]: http://wiki.ubuntu.com/UbuntuOne/Tutorials/FileSharing
    "compartir archivos y directorios"
  [no permite publicar directorios]: http://lists.launchpad.net/ubuntuone-users/msg00523.html
    "no permite publicar directorios"
  [listado]: http://dl.dropbox.com/u/13647978/tree.html
    "listado"
  [DropboxIndex]: http://code.google.com/p/kosciak-misc/wiki/DropboxIndex
    "DropboxIndex"
  [también tiene partes del servidor que son software privativo]: http://www.stefanoforenza.com/what-is-ubuntu-one/
    "también tiene partes del servidor que son software privativo"
  [el cliente y los protocolos de comunicación son libres]: http://es.wikipedia.org/wiki/Ubuntu_One
    "el cliente y los protocolos de comunicación son libres"
  [aquí]: http://one.ubuntu.com/terms/
    "aquí"
  [u1sdtool]: http://manpages.ubuntu.com/manpages/karmic/man1/u1sdtool.1.html
    "u1sdtool"
  [publicar directorios en Ubuntu One]: http://terminus.ignaciocano.com/wp-uploads/linked/ubuntuone-index.py
    "publicar directorios en Ubuntu One"
  [dirección pública del directorio raíz]: http://ubuntuone.com/p/NoU/
    "dirección pública del directorio raíz"
  [política de privacidad]: http://one.ubuntu.com/privacy/
    "ubuntu one privacy politcs"
  [licencia de uso de Ubuntu One]: http://one.ubuntu.com/terms/
    "licencia de uso de Ubuntu One"
