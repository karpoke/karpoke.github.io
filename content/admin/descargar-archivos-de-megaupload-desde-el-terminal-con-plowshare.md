Title: Descargar archivos de Megaupload desde el terminal con plowshare
Date: 2011-09-18 03:57
Author: Nacho Cano
Tags: captcha, descargas, megaupload, mega, plowdown, plowshare
Slug: descargar-archivos-de-megaupload-desde-el-terminal-con-plowshare

[plowshare][] es una herramienta diseñada para descargar y subir
ficheros a los sitios de intercambio de ficheros más populares. También
se pueden administrar directorios remotos y borrar enlaces.

Instalación
-----------

Primero, instalamos las dependencias:

    $ sudo aptitude install curl recode imagemagick tesseract-ocr-eng spidermonkey-bin rhino perlmagick aview

Podemos descargar el código fuente desde el repositorio Git, en un
_tarball_ o en un paquete `.deb`:

    $ wget https://plowshare.googlecode.com/files/plowshare_1%7Egit20110914-1_all.deb
    $ sudo dpkg -i plowshare_1~git20110914-1_all.deb

Descargando
-----------

Para descargar un enlace de Megaupload, por ejemplo, escribimos:

    $ plowdown megaupload -a freeuser:password http://www.megaupload.com/?d=7V4SDTC7

También podemos pasarle un fichero que contenga los enlaces:

    $ plowdown links.txt

Incluye un módulo de reconocimiento de caracteres que, para el caso de
Megaupload, funciona perfectamente, por lo que no deberemos preocuparnos
de tener que introducir los caracteres de ningún _captcha_. Si no
pudiera leer el _captcha_, nos aparecerá una ventana mostrándonos dicho
_captcha_ y un campo de texto para que introduzcamos el contenido.


* * * *

#### Actualizado el 9 de diciembre de 2016

A estas alturas, hace tiempo que Megaupload desapareció y, algo más tarde,
apareció en su lugar [Mega][]. plowshare también se ha renovado, por ejemplo lo
podemos utilizar para [descargar de zippyshare][], e incluye `plowdown`, una
herramienta que facilita la actualización del programa así como la instalación
de módulos. Uno de estos módulos es el que necesitaremos si queremos descargar
archivos de Mega, de lo contrario, nos aparecerá un mensaje parecido al
siguiente:

    $ plowdown 'https://mega.nz/#!3tNDHTAT!ZzWFe-rkF-Tli0o7qoEbbyQcO57FRrmErlu5J5jIEEA'
    No module found, try simple redirection
    Skip: no module for URL (https://mega.nz)

La instalación de dicho módulo es muy sencilla:

    $ plowmod -i https://github.com/mcrapet/plowshare-module-mega.git
    $ cd ~/.config/plowshare/modules.d/mega.git
    $ ./autogen.sh
    $ ./configure --enable-local
    $ make

Ahora ya sí que podremos descargar de Mega sin problemas.

Para mantener tanto la herramienta como los módulos actdualizados, basta
ejecutar:

    $ plowdown -u

* * * * *

  [plowshare]: http://code.google.com/p/plowshare/
    "plowshare"
  [Mega]: https://mega.nz/
    "Mega"
  [descargar de zippyshare]: {filename}/admin/descargar-archivos-de-zippyshare-desde-el-terminal-con-plowshare.md
    "Descargar archivos de zippyshare desde el terminal con plowshare"
