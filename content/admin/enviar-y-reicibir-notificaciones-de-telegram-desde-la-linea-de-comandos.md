Title: Enviar y reicibir notificaciones de Telegram desde la línea de comandos
Date: 2014-05-31 13:27
Author: Nacho Cano
Tags: alias, awk, expect, LUA, notify-send, script, telegram, tg
Slug: enviar-y-reicibir-notificaciones-de-telegram-desde-la-linea-de-comandos

Utilizando [tg][], podemos enviar y recibir mensajes de nuestros
contactos en Telegram, incluyéndonos a nosotros mismos, desde el
terminal.


Envíos programados
------------------

Combinándolo con `expect`, conseguiremos una forma sencilla de programar
notificaciones.

He aquí un pequeño ejemplo:

```bash
#!/usr/bin/env bash

function tg {
    # First argument, if any, must be the receiver
    local to="$1"
    local msg=""
    local cmd=""
    if [ $# -gt 1 ]; then
        shift 1
        msg="$@"
    else
        while read line; do
            if [ -z "$msg" ]; then
                msg=$line
            else
                msg="$msg\n$line"
            fi
        done
        if [ -z "$to" ]; then
            to=$(awk '{print $1}' <<< $msg)
            msg=$(awk '{$1="";print $0}' <<< $msg)
        fi
    fi
    if [[ $msg =~ "\n" ]]; then
        file=$(mktemp)
        echo -e "$msg" > $file
        cmd="send_text $to $file"
    else
        cmd="msg $to $msg"
    fi
    #echo $cmd
    expect -c "
        log_user 0
        match_max 100000
        spawn /path/to/telegram -k /path/to/tg-server.pub
        expect \"User \"
        send -- \"$cmd\r\"
        expect \"Sent\"
        send \"quit\"
    "
}
tg $@
```

Algunos ejemplos de uso:

```bash
# Pasando todos los argumentos directamente
$ tg.sh NombreContacto Lorem impsum dolor sit amet

# Pasando todos los argumentos desde una tubería
$ echo NombreContacto Lorem impsum dolor sit amet | tg.sh

# Pasando el contacto a la función y el mensaje desde una tubería
$ echo Lorem impsum dolor sit amet | tg.sh NombreContacto

# Pasando el resultado de un comando
$ ls | tg.sh NombreContacto
```

Un problema que nos encontraremos es que si enviamos los mensajes al
mismo contacto con el que hemos registrado la aplación al instalarla,
recibiremos el mensaje directamente como leído y no nos lo notificará.

En lugar de utilizar `expect`, tenemos otras alternativas:

### Utilizando el propio `telegram`

El propio cliente acepta el parámetro `-W` que se puede utilizar para
enviar mensajes:

```bash
$ echo -e "msg NombreContacto Lorem impsum dolor sit amet\rquit" | telegram -W
```

### Utilizando `screen`

Podemos [dejar el cliente en ejecución en una sesión de `screen`][dejar el cliente en ejecución en una sesión de screen] y
enviar comandos desde otra:

```bash
$ screen -dmS session_id telegram
```

```bash
$ screen -S session_id -X eval "stuff 'msg NombreContacto Lorem impsum dolor sit amet'\r"
```

### Utilizando tuberías

Podemos crear una tubería que alimente el cliente y enviar comandos a
través de ella:

```bash
$ mkfifo in
$ telegram /dev/null &
$ echo > in
$ echo "msg NombreContacto Lorem impsum dolor sit amet" > in
```

Notificación de mensajes nuevos
-------------------------------

Este cliente permite utilizar _scripts_ en LUA, de tal manera que
podemos llevar a cabo acciones para todo tipo de eventos. Por ejemplo,
podemos ejecutar el comando `notify-send` cada vez que nos llega un
mensaje, para que nos aparezca una notificación en pantalla.

Su uso es sencillo. Nos [bajamos el _script_][bajamos el script],
cortesía de AleixDev, y ejecutamos:

```bash
$ telegram -s /path/to/notify.lua
```

  [tg]: http://github.com/vysheng/tg
    "tg"
  [dejar el cliente en ejecución en una sesión de screen]: https://github.com/vysheng/tg/issues/104#issuecomment-36032821
    "dejar el cliente en ejecución en una sesión de `screen`"
  [bajamos el script]: https://github.com/AleixDev/tg-notify-bash
    "tg-notify-bash"
