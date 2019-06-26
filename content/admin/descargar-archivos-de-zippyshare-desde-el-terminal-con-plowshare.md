Title: Descargar archivos de zippyshare desde el terminal con plowshare
Date: 2016-11-26 23:56
Author: Nacho Cano
Tags: descargas, zippyshare, plowdown, plowshare, checkinstall
Slug: descargar-archivos-de-zippyshare-desde-el-terminal-con-plowshare

[plowshare][] es una herramienta diseñada para descargar y subir
ficheros a los sitios de intercambio de ficheros más populares. Hace ya
un tiempo la podíamos usar para [descargar archivos de Megaupload][].

Instalación
-----------

Primero, instalamos las dependencias:

```bash
$ sudo aptitude install curl recode imagemagick tesseract-ocr-eng spidermonkey-bin rhino perlmagick aview
```

Podemos descargar el código fuente desde el repositorio Git y compilarlo:

```bash
$ git clone https://github.com/mcrapet/plowshare.git
$ cd plowshare
```

Podemos instalarlo mediante `sudo make install`, o si no tenemos privilegios de
root, podemos sobreescribir el prefijo `/usr` con
`make install prefix=$home/local`.

También podemos crear un paquete `.deb`:

```bash
$ sudo checkinstall
```

Instalamos los módulos externos mediante la herramienta para gestionar dichos
módulos:

```bash
$ plowmod --install
```

Más adelante podremos actualizarlos ejecutando:

```bash
$ plowmod --update
```

Descargando
-----------

Para descargar un enlace de zippyshare, por ejemplo, escribimos:

```bash
$ plowdown http://www43.zippyshare.com/v/laVpgPTS/file.html
```

También podemos pasarle un fichero que contenga los enlaces:

```bash
$ plowdown links.txt
```

Si queremos que modifique el fichero para que comente los enlaces que se han
descargado correctamente, no tenemos más que pasarle el argumento `-m`.

  [plowshare]: https://github.com/mcrapet/plowshare
    "plowshare"
  [descargar archivos de Megaupload]: {filename}/admin/descargar-archivos-de-megaupload-desde-el-terminal-con-plowshare.md
    "Descargar archivos de Megaupload desde el terminal con plowshare"
