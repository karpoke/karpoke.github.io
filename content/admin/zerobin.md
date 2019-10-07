Title: ZeroBin
Date: 2012-04-21 17:31
Author: Nacho Cano
Tags: cifrado, open source, pastebin, zerobin
Slug: zerobin

ZeroBin es una aplicación web de código abierto que permite subir
textos, al estilo [pastebin.com][], pero cifrados, de tal manera que
nadie que no conozca la clave puede tener acceso, ni siquiera el
servidor. Los datos se cifran y descifran en el navegador usando una
clave AES de 256 bits, utilizando la [librería de cifrado y descifrado
en JavaScript][] de la universidad de Standford.

Es rápido, fácil de utilizar y no necesita una base de datos, tan solo
un servidor de páginas PHP (5.2.6+) y un navegador moderno con soporte
JavaScript habilitado. Permite configurar que el contenido expire en un
tiempo determinado o comenzar una conversación entorno a él, entre
algunas de sus características, y otras que vendrán en futuras
versiones.

Instalación
-----------

Cabe recordar que es una versión _alpha_, susceptible de contener
fallos.

Para instalar la aplicación, sólo tenemos que descargar el archivo y
descomprimirlo en un directorio accesible por nuestro servidor web:

```bash
$ mkdir zerobin
$ cd zerobin
$ wget http://sebsauvage.net/files/zerobin_0.15_alpha.zip
$ unzip zerobin_0.15_alpha.zip
```

Le asignamos el propietario y los permisos necesarios. Por ejemplo:

```bash
$ sudo chown -R www-data:www-data zerobin
```

Un ejemplo de uso lo tenemos en [anonpaste.tk/][].

Referencias
-----------

» [ZeroBin][]
» [Stanford Javascript Crypto Library][librería de cifrado y descifrado
en JavaScript]

  [pastebin.com]: http://pastebin.com/
    "pastebin.com"
  [librería de cifrado y descifrado en JavaScript]: http://crypto.stanford.edu/sjcl/
    "librería de cifrado y descifrado en JavaScript"
  [anonpaste.tk/]: http://anonpaste.tk/
    "anonpaste.tk/"
  [ZeroBin]: http://sebsauvage.net/wiki/doku.php?id=php:zerobin
    "ZeroBin"
