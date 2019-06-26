Title: AnonTwi, tweets cifrados
Date: 2012-06-16 13:23
Author: Nacho Cano
Tags: oauth, privacidad, python, script, twitter
Slug: anontwi-tweets-cifrados
Related: random-bash

[AnonTwi][] es un _script_ en Python que permite enviar y recibir
_tweets_ y mensajes cifrados mediante AES y HMAC-SHA1 en Twitter, al que
se conecta mediante SSL. Otras caracterísiticas son la posibilidad de
usar la red TOR, envío de mensajes largos o la falsificación de las
cabeceras que envía.


Instalación
-----------

AnonTwi está todavía en fase _beta_ de desarrollo, algo que se debe
tener en cuenta según el uso que queramos darle, pero si queremos
probarlo, podemos usar la última versión descargándola del repositorio:

```bash

$ hg clone http://hg.code.sf.net/p/anontwi/code anontwi-code
```

Instalamos las dependencias:

```bash

$ sudo aptitude install python-crypto python-httplib2
```

OAuth
-----

Para utilizar OAuth con Twitter, vamos a [dev.twitter.com][], iniciamos
sesión y creamos una App:

-   __Name:** _El que queramos, pero debe ser único._
-   __Description:__ AnonTwi: AES + HMAC-SHA1 encryption on Tweets and
    Direct Messages
-   __Website:__ <http://anontwi.sf.net>

Una vez creada, copiamos las claves `Consumer key` y `Consumer secret`
que utilizaremos más tarde. En la pestaña de configuración, cambiamos
los permisos de la aplicación para que pueda leer, escribir y enviar
mensajes directos.

Vamos al directorio donde nos hemos descargado AnonTwi y editamos el
fichero `config.py` para incluir dichas claves.

Tokens
------

Además de las claves que hemos creado, necesitaremos dos _tokens_ de
acceso, no debemos crearlos desde el panel de administración de la
aplicación que hemos creado, sino con el propio _script_:

```bash

$ ./anontwi --tokens
```

Seguimos el enlace, que nos llevará hasta la página que nos pide que
autoricemos la aplicación, y tras autorizarla nos devolverá el PIN que
deberemos pasarle al _script_.

A continuación se crean los _tokens_ de acceso. AnonTwi no guarda estos
valores, así que para evitar tener que estar continuamente pasándoselos
al _script_ podemos exportar las siguientes variables:

```bash

$ export ANONTWI_TOKEN_KEY=6684922-Foa6b1KShUIWviFHjFfZrASyYKV8fPe9teXZwWllIE
$ export ANONTWI_TOKEN_SECRET=izXb9vG8xWKAgH2GvYzl8EqeJDalSGg2MkrheoasoI
```

Si las copiamos al final del fichero `~/.bashrc` no tendremos que volver
a preocuparnos.

Ejemplos
--------

La sintáxis para utilizar el _script_ es la siguiente:

```bash

$ ./anontwi [-m 'text' | -r 'ID' | -d @user | -f @nick | -u @nick] [OPTIONS] 'token key' 'token secret'
```

Para enviar un mensaje cifrado a un usuario, tenemos que compartir una
clave, que el usuario utilizará para descifrarlo. Podemos utilizar el
_script_ para crear una clave segura y aleatoria:

```bash

$ ./anontwi --gen
PIN key: P/2/QwWyVp48ta8+T4oasd/G6wNWELt9/MjUZlWs53M=
```

Ahora ya podemos enviar un mensaje directo cifrado:

```bash

$ ./anontwi -m "See you later" -d "@nick" --enc --pin "P/2/QwWyVp48ta8+T4oasd/G6wNWELt9/MjUZlWs53M=" ===========================================================================

AnonTwi [0.4] - 2012 - http://anontwi.sf.net -> by psy

===========================================================================
Starting to send your DM (direct message)... :)
===========================================================================

Message [ Number of words: 3 - Number of waves: 1 ]
-------------
"See you later"
-------------
To: "@nick"
------

[Info] DM sended correctly!
```

Para enviar un _tweet_ cifrado:

```bash
$ ./anontwi -m "Hello World" --enc --pin "mystrongpassword"
```

Para descifrar un _tweet_ podemos hacerlo incluyendo directamente el
contenido del _tweet_:

```bash
$ ./anontwi --dec "7asNGpFFDKQl7ku9om9CQfEKDq1ablUW+srgaFiEMa+YK0no8pXsx8pR" --pin "friend's key"
```

O introduciendo la URL del _tweet_:

```bash
$ ./anontwi --dec "http://twitter.com/encrypted_message_path" --pin "friend's key"
```

Se pueden ver muchos más ejemplos de uso en el archivo `README.txt`.

Interfaz gráfica
----------------

Hay disponible un módulo, Simple Decript Tool, que permite utilizar una
herramienta gráfica en lugar del terminal para descifrar los mensajes.
Si queremos probarla, antes instalaremos las dependencias:

```bash
$ sudo aptitude install gambas2
```

Descargamos el paquete, lo descomprimimos y lo instalamos:

```bash
$ wget http://freesoftwareando.com/gambas-anontwi_all.deb.tar.gz
$ tar xzvf gambas-anontwi_all.deb.tar.gz
$ sudo dpkg -i gambas-anontwi_0.0.10-1_all.deb
```

Al instalarlo, me ha surgido el siguiente error:

```bash
En el fichero ;`/usr/share/menu/gambas-anontwi;', en (o en la defición que termina en) la línea 4:
?package(gambas-anontwi):needs="X11" section "Applications/Network/Communication" title="AnonTwi Simple Decrypt Tool" command="/usr/bin/gambas-anontwi.gambas" icon="/usr/share/pixmaps/gambas-anontwi.png"
                                            ^
Esperaba: ;`=;'
```

Parece ser debido a una pequeña errata en el fichero
`/usr/share/menu/gambas-anontwi`. Si queremos corregirlo, descomprimimos
el fichero `gambas-anontwi_0.0.10-1_all.deb`:

```bash
$ mkdir temp
$ dpkg-deb --extract gambas-anontwi_0.0.10-1_all.deb temp
$ dpkg-deb --control gambas-anontwi_0.0.10-1_all.deb temp/DEBIAN
```

Modificamos el fichero `temp/usr/share/menu/gambas-anontwi` para incluir
el `=` que falta, de tal manera que quede así:

```bash
?package(gambas-anontwi):needs="X11"
section="Applications/Network/Communication"
title="AnonTwi Simple Decrypt Tool"
command="/usr/bin/gambas-anontwi.gambas"
icon="/usr/share/pixmaps/gambas-anontwi.png"
```

Volvemos a crear el paquete:

```bash
$ dpkg --build temp
$ mv temp.deb gambas-anontwi_0.0.10-1_all.deb
```

Y lo instalamos:

```bash
$ sudo dpkg -i gambas-anontwi_0.0.10-1_all.deb
```

Para lanzar la aplicación podemos hacerlo desde el menú, o lanzando el
siguiente comando en el terminal

```bash
$ anontwi.gambas
```

Referencias
-----------

- [anontwi.sourceforge.net][AnonTwi]
- [AnonTwi: cliente de Twitter que permite cifrar tweets y mensajeria
privada][]
- [Como cambiar las dependencias de un paquete (.deb)][]

  [AnonTwi]: http://anontwi.sourceforge.net/
    "AnonTwi"
  [dev.twitter.com]: https://dev.twitter.com
    "dev.twitter.com"
  [AnonTwi: cliente de Twitter que permite cifrar tweets y mensajeria privada]: http://www.kriptopolis.com/anontwi
    "AnonTwi: cliente de Twitter que permite cifrar tweets y mensajeria privada"
  [Como cambiar las dependencias de un paquete (.deb)]: http://inetsurvivalguide.blogspot.com.es/2007/04/como-cambiar-las-dependencias-de-un.html
    "Como cambiar las dependencias de un paquete (.deb)"
