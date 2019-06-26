Title: Creando y leyendo códigos QR desde Python
Date: 2011-03-27 19:46
Author: Nacho Cano
Tags: 10.10, curl, egg, google chart api, imaging, jcc, make, oneliner, pyqrcode, python, qr, qrcode, qrencode, setuptools, ubuntu maverick meerkat, ubuntu one
Slug: creando-y-leyendo-codigos-qr-desde-python

Un código QR (Quick Response Barcode) permite almacenar información en
un código de barras de dos dimensiones.

![cc.qr.code.capacity`]({static}/images/cc.qr_.code_.capacity-300x166.jpg)

Hay bastantes servicios en la web que nos permiten crear nuestros
propios códigos, por ejemplo [el de Google][], que podemos emplear desde
la línea de comandos:

```bash
$ curl http://chart.apis.google.com/chart?chs=150x150&cht=qr&chld=H|0&chl=texto -o qr.png
```

![QR Code Python]({static}/images/qrcode-python.png)

Un pequeño alias para tenerlo siempre a mano:

```bash
$ alias qrurl='qrurl() { curl http://chart.apis.google.com/chart?chs=150x150&cht=qr&chld=H|0&chl=${@// /%20} -o qr.$(date +%Y%m%d%H%M%S).png; }; qrurl'
$ qrurl una ranita iba caminando
```

Esto creará un fichero con un nombre parecido a `qr.20110325161706.png`.

Hay un paquete que nos permite hacer esto desde la línea de comandos, es
`qrencode`:

```bash
$ qrencode
qrencode version 3.1.1
Copyright (C) 2006, 2007, 2008, 2009 Kentaro Fukuchi
Usage: qrencode [OPTION]... [STRING]
Encode input data in a QR Code and save as a PNG image.

  -h           display this message.
  --help       display the usage of long options.
  -o FILENAME  write PNG image to FILENAME. If '-' is specified, the result
               will be output to standard output. If -S is given, structured
               symbols are written to FILENAME-01.png, FILENAME-02.png, ...;
               if specified, remove a trailing '.png' from FILENAME.
  -s NUMBER    specify the size of dot (pixel). (default=3)
  -l {LMQH}    specify error collectin level from L (lowest) to H (highest).
               (default=L)
  -v NUMBER    specify the version of the symbol. (default=auto)
  -m NUMBER    specify the width of margin. (default=4)
  -S           make structured symbols. Version must be specified.
  -k           assume that the input text contains kanji (shift-jis).
  -c           encode lower-case alphabet characters in 8-bit mode. (default)
  -i           ignore case distinctions and use only upper-case characters.
  -8           encode entire data in 8-bit mode. -k, -c and -i will be ignored.
  -V           display the version number and copyrights of the qrencode.
  [STRING]     input data. If it is not specified, data will be taken from
               standard input.
```

También hay aplicaciones para el móvil, como el Kaywa Reader, pero ahora
vamos a ver cómo podemos crear y leer un código QR desde Python.

pyqrcode
--------

`pyqrcode` es una extensión para poder codificar y decodificar códigos
QR en Python. Para la codificación se ha basado en la librería
`libqrencode` de Fukuchi Kentaro, y para la decodificación utiliza la
librería de [qrcode][] de Yusuke Yanbe.

Para instalarlo se necesita:

```bash
$ sudo aptitude install jcc openjdk-6-jdk openjdk-6-jre python-imaging python-setuptools python-dev
```

En su página pone el Java de Sun, pero a mi también me ha ido bien con
el OpenJDK.

Una vez que nos hayamos descargado el código, toca compilarlo:

```bash
$ tar xvzf pyqrcode-0.2.1.tar.gz
$ cd pyqrcode-0.2.1
$ make
```

Si tenemos una versión de Python superior a la 2.6, nos aparecerá el
siguiente error:

```bash
python -m jcc --jar qrcode/qrcode.jar  --build
/usr/bin/python: jcc is a package and cannot be directly executed
make: *** [lib] Error 1
```

La [solución][] pasa por cambiar `-m jcc` por `-m jcc.__main__` en el
`Makefile`. Quedaría así:

```bash
#GENERATE=python -m jcc --jar $(LIBFILE)
GENERATE=python -m jcc.__main__ --jar $(LIBFILE)
```

Ahora ya podemos instalarlo:

```bash
$ sudo make install
```

También podemos crear un binario a partir de la extensión:

```bash
$ sudo make egg
```

e instalarlo:

```python
$ cd dist
$ sudo easy_install qrcode-0.2.1-py2.6-linux-i686.egg
```

Para comprobar que está correctamente instalado, podemos hacer la
siguiente prueba:

```python
$ ipython
>>> import qrcode
```

En Ubuntu Maverick Meerkat es posible que nos salga el siguiente
[error][]:

```python
In [1]: import qrcode
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)

/home/karpoke/ in ()

/usr/local/lib/python2.6/dist-packages/qrcode-0.2.1-py2.6-linux-i686.egg/qrcode/__init__.py in ()
     19     pass
     20
---> 21 _qrcode._setExceptionTypes(JavaError, InvalidArgsError)
     22
     23 VERSION = "0.2.1"

AttributeError: 'module' object has no attribute '_setExceptionTypes'
```

Después de ver el código que da este error, una posible solución es
comentar la línea del fichero `qrcode/__init__.py` que da el error.

```python
# _qrcode._setExceptionTypes(JavaError, InvalidArgsError)
```

Volvemos a generar el huevo y lo volvemos a instalar:

```bash
$ sudo make egg
$ sudo easy_install qrcode-0.2.1-py2.6-linux-i686.egg
```

Este [python egg][] se puede descargar desde el [directorio
público][].

Ya podemos hacer una prueba para crear un código QR:

```python
import sys, qrcode
e = qrcode.Encoder()
image = e.encode('ando con la mirada fija en el cielo', version=3, mode=e.mode.BINARY, eclevel=e.eclevel.H)
image.save('out.png')
```

Para decodificar:

```python
import sys, qrcode
d = qrcode.Decoder()
print d.result if d.decode("out.png") else "error"
```

En el terminal
--------------

Para hacer aún más cómoda la decodificación desde el terminal, vamos a
crear un alias, `qrdecode`:

```bash
# $1 filename
alias qrdecode='fqrdecode() { python -c "import qrcode;d=qrcode.Decoder();print d.result if d.decode('\''$1'\'') else '\''Error'\''"; }; fqrdecode'
```

Para crear un QR desde la línea de comandos ya tenemos el paquete
`qrencode` comentado anteriormente.

```bash
$ qrencode "texto a poner en el código qr" -o out.png
$ qrdecode out.png
texto a poner en el código qr
```

Usando la webcam
----------------

La biblioteca `libdecodeqr` contiene un lector de códigos QR usando la
webcam. Para utilizarlo, ejecutamos:

```bash
$ libdecodeqr-webcam
```

  [el de Google]: http://code.google.com/apis/chart/infographics/docs/qr_codes.html
    "el de Google"
  [qrcode]: http://qrcode.sourceforge.jp/
    "qrcode"
  [solución]: http://sourceforge.net/projects/pyqrcode/forums/forum/886787/topic/3805055
    "solución"
  [error]: http://sourceforge.net/projects/pyqrcode/forums/forum/886787/topic/3897537
    "error"
  [python egg]: http://ubuntuone.com/p/jig/
    "python egg para crear y leer códigos QR"
  [directorio público]: {filename}/admin/como-publicar-directorios-en-ubuntu-one-y-dropbox.md
    "cómo publicar directorios en ubuntu one y dropbox"
