Title: Copia de seguridad de GMail con getmail
Date: 2011-07-08 15:52
Author: Nacho Cano
Tags: copia de seguridad, getmail, gmail, google, maildir, mbox
Slug: copia-de-seguridad-de-gmail-con-getmail

Hay otras maneras de realizar una [copia de seguridad de GMail][], como
por ejemplo, usar Thunderbird, pero utilizar `getmail` tiene la ventaja
de que es sencillo, puede realizar la copia en formato Maildir y no
necesitamos utilizar ningún gestor de correo electrónico.

Maildir y mbox
--------------

Básicamente, en GNU/Linux hay dos maneras de guardar el correo
electrónico, [Maildir y mbox][].

### Maildir

Cada correo se guarda en un fichero por separado. Añadir, buscar y
eliminar correos es rápido, no se necesita bloqueo en ninguna operación,
se puede usar en sistemas de ficheros de red y no hay corrupción
(exceptuando fallos de hardware). El inconveniente viene dado porque
algunos sistemas de ficheros no gestionan eficientemente grandes
cantidades de ficheros pequeños, además de que la búsqueda de texto, que
requiere abrir todos los ficheros puede ser lenta.

![Maildir]({static}/images/maildir-300x270.png)

<small>Fuente: [www.mattcutss.com][copia de seguridad de GMail]</small>


### mbox

Todo el correo se guarda en un único fichero. La ventaja que tiene es
que ampliamente soportado. Añadir y buscar un correo es rápido. Entre
los inconvenientes están los problemas de bloqueo del fichero para cada
operación (añadir, borrar y buscar), problemas cuando se usa en sistemas
de ficheros de red y que el formato se corrompe fácilmente.

![mbox]({static}/images/mbox.png)

<small>Fuente: [www.mattcutss.com][copia de seguridad de GMail]</small>

Realizar el backup
------------------

Instalamos `getmail`:

```bash
$ sudo aptitude install getmail4
```

[Activamos POP3 en GMail][]. Vamos a *Configuración del correo >
Reenvío y POP > Activar POP para todo el correo*.

![POP]({static}/images/pop-300x166.gif)

<small>Fuente: [mail.google.com][Activamos POP3 en GMail]</small>

Creamos el directorio de configuración de `getmail`:

```bash
$ mkdir ~/.getmail
```

Y creamos el fichero `~/.getmail/getmail.gmail`:

```bash
[retriever]
type = SimplePOP3SSLRetriever
server = pop.gmail.com
username = bob@gmail.com
password = mypass

[destination]
type = Maildir
path = ~/gmail-archive/

[options]
# print messages about each action (verbose = 2)
# Other options:
# 0 prints only warnings and errors
# 1 prints messages about retrieving and deleting messages only
verbose = 2provocado por un cambio en las lib
message_log = ~/.getmail/gmail.log
```

Creamos los directorios donde se guardará el correo descargado:

```bash
$ mkdir -p ~/gmail-archive/{cur,new,tmp}
```

Ya podemos empezar con la copia `getmail`:

```bash
$ getmail -r ~/.getmail/getmail.gmail
```

El correo se bajará en tandas de pocos cientos, dado que GMail sólo
permite descargar eso cada vez, por lo que deberemos repetir la
operación unas cuantas veces.

* * * * *

#### Actualización a 1 de diciembre de 2015

Desde hace un tiempo, cuando voy a realizar la descarga de nuevos
correos, empiezo a recibir errores del tipo:

```bash
    Retrieval error: server for SimplePOP3SSLRetriever:bob@gmail.com@pop.gmail.com:995 is broken; offered message GmailId3af2edcdc36d18d2 but failed to provide it.  Please notify the administrator of the server.  Skipping message...
```

Al parece, se debe a un [fallo][] que ha sido corregido a partir de la
versión 4.48.0.

* * * * *

Referencias
-----------

- [getmail documentation][]

  [copia de seguridad de GMail]: http://www.mattcutts.com/blog/backup-gmail-in-linux-with-getmail/
    "copia de seguridad de GMail"
  [Maildir y mbox]: http://www.linuxmail.info/mbox-maildir-mail-storage-formats/
    "Maildir y mbox"
  [Activamos POP3 en GMail]: http://mail.google.com/support/bin/answer.py?hl=en&answer=13273
    "Activamos POP3 en GMail"
  [fallo]: http://permalink.gmane.org/gmane.mail.getmail.user/5375
    "fallo"
  [getmail documentation]: http://pyropus.ca/software/getmail/configuration.html
    "getmail documentation"
