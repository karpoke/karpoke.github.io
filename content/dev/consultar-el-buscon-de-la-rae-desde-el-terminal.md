Title: Consultar el buscón de la RAE desde el terminal
Date: 2012-02-28 01:41
Author: Nacho Cano
Tags: autocompletado, buscón, cabeceras, complete, completion, curl, diccionario, dig, drae, elinks, host, html2text, iso-8859-1, links, lynx, nslookup, panhispánico, php5-cli, rae, script, time, useragent, utf8
Slug: consultar-el-buscon-de-la-rae-desde-el-terminal

Al realizar consultas al [buscón de la RAE][] desde el terminal, me iba
muy lento. Ésta es una página que todavía usa marcos (wtf!), por lo que
si queremos acceder directamente a la página con el resultado de la
búsqueda deberemos utilizar una de las siguientes URLs:

-   ~~Para el [diccionario de la RAE][]:
    `http://buscon.rae.es/draeI/SrvltGUIBusUsual?origen=RAE&TIPO_BUS=3&LEMA=cederrón`~~
-   ~~Para el [diccionario panhispánico de dudas][]:
    `http://buscon.rae.es/dpdI/SrvltGUIBusDPD?origen=RAE&lema=cederrón`~~

* * * * *

#### Actualización

La RAE ha cambiado la URL de búsqueda, pasando a ser:

-   Para el buscón: [buscón][]:
    <http://www.rae.es/drae/srv/search?origen=RAE&type=3&val=buscador>
-   Para [el panhispánico de dudas][]:
    <http://www.rae.es/dpd/srv/search?origen=RAE&key=terminal>

Además, también se ha cambiado la codificación de la URL de UTF-8 a
ISO-8859-1, por lo que se deberá tener en cuenta para aquellas palabras
que contengan caracteres donde ambas codificaciones son distintas, como
las vocales con tilde o diéresis o la letra eñe.

En el artículo, dejaré las referencias a las URLs antiguas para que
quede un registro de cómo ha ido evolucionando el _script_.

* * * * *

Para descargar y visualizar el contenido de una página desde el
terminal lo podemos hacer de diferentes maneras, por ejemplo:

$ curl -s "http://buscon.rae.es/draeI/SrvltGUIBusUsual?origen=RAE&TIPO_BUS=3&LEMA=cederrón"
$ w3m -dump "http://buscon.rae.es/draeI/SrvltGUIBusUsual?origen=RAE&TIPO_BUS=3&LEMA=cederrón"
$ lynx -dump "http://buscon.rae.es/draeI/SrvltGUIBusUsual?origen=RAE&TIPO_BUS=3&LEMA=cederrón"
$ links -dump "http://buscon.rae.es/draeI/SrvltGUIBusUsual?origen=RAE&TIPO_BUS=3&LEMA=cederrón"
$ elinks -dump "http://buscon.rae.es/draeI/SrvltGUIBusUsual?origen=RAE&TIPO_BUS=3&LEMA=cederrón"

Pero con todas ellas me iba muy lento, incluso si sólo descargamos la
cabecera:

$ time curl -I -s "http://buscon.rae.es/draeI/SrvltGUIBusUsual?origen=RAE&TIPO_BUS=3&LEMA=cederrón"
    HTTP/1.1 200 OK
    Connection: close
    Date: Mon, 27 Feb 2012 23:20:26 GMT
    Server: Microsoft-IIS/6.0
    Server: WebSphere Application Server/5.1
    Content-Type: text/html
    Content-Language: es-ES


    real    0m38.410s
    user    0m0.008s
    sys 0m0.004s

No parece que sea un problema de `User Agent`, porque tanto si
utilizamos `lynx` como si utilizamos `curl` podemos modificarlo (y usar,
por ejemplo, el de Firefox o el de Internet Explorer) y la página sigue
tardando en responder.

$ curl -s --user-agent "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0.2) Gecko/20100101 Firefox/10.0.2" "http://buscon.rae.es/draeI/SrvltGUIBusUsual?origen=RAE&TIPO_BUS=3&LEMA=cederrón"

El problema parece estar en el tiempo que tarda en resolverse el
dominio. Usando `nslookup` podemos ver que tras el dominio buscon.rae.es
hay un balanceador:

$ nslookup buscon.rae.es
    Server:     208.67.222.222
    Address:    208.67.222.222#53

    Non-authoritative answer:
    buscon.rae.es   canonical name = buscon.balanceo.rae.es.
    Name:   buscon.balanceo.rae.es
    Address: 85.62.96.169

Podría ser que la primera vez que se hace una consulta en Firefox
también tarde, y que las siguientes consultas sean instantáneas porque
se guarde la IP, y sin embargo con `curl` estemos resolviendo la IP cada
vez, pero tampoco podría asegurarlo dado no he hecho muchas más pruebas
y lo siguiente me ha funcionado.

Si utilizamos la IP en lugar del dominio,obtenemos una repuesta
inmediata. Probad lo siguiente, si acaso con la IP que os devuelva
`nslookup`:

$ curl -s "http://85.62.96.169/draeI/SrvltGUIBusUsual?LEMA=cederrón&origen=RAE&TIPO_BUS=3"

He probado con otros comandos en lugar de `nslookup`, como `host` o
`dig`, pero con `nslookup` parece que se tarda menos en obtener la
respuesta.

El problema es que esta IP va cambiando, pero podemos utilizar
`nslookup` en el _script_, cuyo resultado es instantáneo, y filtrar el
resultado de `curl` tal como se ha comentado en este [foro de Ubuntu][]:

    #!/bin/bash -

    set -o nounset                              # Treat unset variables as an error

    WORD="$1"
    if [ -z "$WORD" ]; then
        echo "Usage: ${0##*/} word"
        exit 1
    fi

    CURL=/usr/bin/curl
    HTML2TEXT=/usr/bin/html2text
    NSLOOKUP=/usr/bin/nslookup

    for p in $CURL $HTML2TEXT $NSLOOKUP; do
        if [ ! -x $p ]; then
            echo "[+] $p not found. You must install it first."
            exit 1
        fi
    done

    DOMAIN=buscon.rae.es
    IP=$($NSLOOKUP $DOMAIN | tail -2 | head -1 | awk '{print $2}')
    URL="http://$IP/draeI/SrvltGUIBusUsual?LEMA=$WORD&origen=RAE&TIPO_BUS=3"

    RESET_TEXT='\e[0m'         # reset
    HIGHLIGHT_TEXT='\e[0;31m'  # red

    echo -e "[+] ${HIGHLIGHT_TEXT}${WORD}${RESET_TEXT} $URL\n"
$CURL -s "$URL" | $HTML2TEXT | head -n-2 | sed -e 's/\[Ver_artículo_enmendado\]/*\ /g'

Aquí se puede descargar el _script_ `rae.sh`.

Por último, un ejemplo de uso, suponiendo que el _script_ tiene permisos
de ejecución y se encuentra en el directorio actual:

$ ./rae.sh cederrón
    [+] cederrón http://85.62.96.169/draeI/SrvltGUIBusUsual?LEMA=cederrón&origen=RAE&TIPO_BUS=3

    cederrón.
    (De CD-ROM, y este sigla del ingl. CompactDiscRead-OnlyMemory).
    1. m.Inform. CD-ROM.

* * * * *

#### Actualizado el 12 de marzo de 2012

He realizado unas pequeñas modificaciones en el _script_:

-   ya no acepta únicamente una palabra, sino una lista de ellas. Por
    ejemplo: `./rae.sh cederrón dvd disquete`
-   se puede utilizar el argumento `-p` para que busque también en el
    panhispánico de dudas.
-   he cambiado el uso de `curl` por `lynx`, así no hay necesidad de
    parsear el resultado.
-   he añadido autocompletado para las palabras. No están todas las que
    son ni son todas las que están, pero es bastante útil en la mayoría
    de las ocasiones.

* * * * *

#### Actualizado el 30 de abril de 2012

Ha habido cambios en la página de la RAE, de tal manera que usar la IP
directamente en la URL ya no sirve; la página devuelve un error
`400 Bad Request (Invalid Hostname)`. Una manera de resolver este
inconveniente es añadir la IP y el dominio en el archivo `/etc/hosts`,
para que podamos utilizar el dominio en la URL y no sea necesario
resolver su IP:

$ grep buscon.rae.es /etc/hosts
    193.145.222.107 buscon.rae.es

El _script_ vuelve a funcionar como la seda, por ahora.

* * * * *

#### Actualizado el 3 de julio de 2012

Ha vuelto a haber cambios en la página de la RAE. El dominio ha
cambiado, pasando a ser `lema.rae.es`, y las rutas relativas para el
Diccionario de la RAE y el Panhispánico de dudas también han cambiado.
Ahora son algo así:

    # DRAE: http://lema.rae.es/drae/srv/search?type=3&val_aux=&origen=RAE&val=cederrón
    # DPD:  http://lema.rae.es/dpd/srv/search?origen=RAE&key=cederrón

La IP sigue siendo la misma por lo que basta cambiar el dominio en el
fichero `/etc/hosts`:

$ grep lema.rae.es /etc/hosts
    193.145.222.107 lema.rae.es

Aunque lo bueno es que vuelve a funcionar el truco de poner la IP en
lugar del dominio en la URL, y la respuesta es incluso más rápida :)

* * * * *

#### Actualizado el 7 de septiembre de 2012

Ha habido un nuevo cambio en la página del buscón de la RAE. Las nuevas
URLs pasan a ser:

-   Para el buscón: <http://www.rae.es/drae>
-   Para el panhispánico de dudas: <http://www.rae.es/dpd>

Además, la URL se debe codificar en formato Western (ISO-8859-1). Se ven
afectadas aquellas palabras que tengan vocales con tilde, la u con
diéresis o la letra eñe. Una manera de cambiar la codificación de la
palabra es utilizar las funciones `utf8_decode` y `urlencode` de PHP,
por lo que deberemos tener instalado el paquete `php5-cli`:

$ php -r 'echo urlencode(utf8_decode("áéíóúüñ"));'
    %E1%E9%ED%F3%FA%FC%F1

* * * * *

Añadir autocompletado
---------------------

Una de las características más útiles en la línea de comandos es el
autocompletado. Empezamos a escribir un comando, un alias, un nombre de
archivo o directorio, etc, y pulsamos el tabulador. Si sólo hay una
opción posible cuyo prefijo coincida con lo que hemos escrito, ésta se
completa _mágicamente_. Si hay más de una opción posible, no pasará
nada, lo que nos indica que podemos pulsar el tabulador una vez más para
que entonces nos muestre una lista de las opciones disponibles.

Teniendo esto en cuenta, podríamos añadir autocompletado a nuestro
_script_ para que busque en el diccionario instalado en local. Realmente
no es un diccionario, sino una lista de palabras en castellano ordenadas
alfabéticamente que no tiene por qué ser completa. Para instalar este
listado:

$ sudo aptitude install wspanish

El autocompletado se consigue mediante una función que especifica los
resultados a mostrar, en función de diferentes factores. Por ejemplo, si
estamos usando el comando `ping` es útil que autocomplete con los
nombres de los _hosts_ del fichero `/etc/hosts`, o si estamos matando un
proceso, que utilice el PID de los procesos que hay en ejecución, si es
con `kill`, o en los nombres de estos procesos, si es jhb `pkill`. Luego
asociamos esta función con nuestro _script_. Crearemos un fichero que
incluya dicha función, y luego la asocie a nuestro _script_. En Ubuntu,
este fichero debe estar en `/etc/bash_completion.d/`.

Crearemos esta asociación mediante el comando `complete`. Este comando
nos permite, además, consultar y modificar estas asociaciones. Por
ejemplo, para ver la lista de asociaciones actual ejecutamos:

$ complete -p

El fichero es algo así:

    _foo()
    {
        local cur prev opts
        COMPREPLY=()
        cur="${COMP_WORDS[COMP_CWORD]}"
        prev="${COMP_WORDS[COMP_CWORD-1]}"
        opts="--help --verbose --version"

        if [[ ${cur} == -* ]] ; then
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            return 0
        fi
    }
    complete -F _foo foo

`_foo` es la función que se encarga de crear la lista de opciones
disponibles. En este caso, permite seleccionar entre tres opciones
posibles, `--help`, `--verbose` y `--version`. Las variables `cur` y
`prev` contienen el argumento anterior y el actual (o lo que llevamos
escrito de él), y se pueden utilizar para crear reglas de asociación más
complejas. Por último, el comando `compgen` selecciona las candidatas de
entre el listado de opciones disponibles. En las referencias al final se
puede encontrar información más detallada.

En el fichero `/etc/bash_completion` se pueden encontrar algunas de las
expansiones más comunes como, por ejemplo, obtener un listado de
directorios en el directorio actual, señales, direcciones MAC,
interfaces de red, _hosts_, PIDs, UIDs, GIDs, servicios, módulos,
módulos instalados, grupos a los que pertenece un usuario, usuarios
autorizados, grupos autorizados, _shells_, tipos de sistemas de
ficheros, etc.

Sin embargo, en nuestro caso hay algo que deberemos tener en cuenta a la
hora de crear el listado de opciones, y es que estas opciones son
palabras que pueden contener espacios, comillas o barras invertidas,
que puede que [deban ser escapadas primero][] para poder ser utilizadas.
Utilizaremos el siguiente código el el fichero de autocompletado `rae`:

```bash
    # http://stackoverflow.com/a/1146716
    _find_words()
    {
        search=$(eval echo "$cur" 2>/dev/null || eval echo "$cur'" 2>/dev/null || eval echo "$cur\"" 2>/dev/null || "")
        grep -- "^$search" /usr/share/dict/spanish | sed -e "{" -e 's#\\#\\\\#g' -e "s#'#\\\'#g" -e 's#"#\\\"#g' -e "}"
    }

    _words_complete()
    {
        local IFS=$'\n'

        COMPREPLY=()
        local cur="${COMP_WORDS[COMP_CWORD]}"

        COMPREPLY=( $( compgen -W "$(_find_words)" -- "$cur" ) )

        local escaped_single_qoute="'\''"
        local i=0
        for entry in ${COMPREPLY[*]}
        do
            if [[ "${cur:0:1}" == "'" ]]
            then
                # started with single quote, escaping only other single quotes
                # [']bla'bla"bla\bla bla --> [']bla'\''bla"bla\bla bla
                COMPREPLY[$i]="${entry//\'/${escaped_single_qoute}}"
            elif [[ "${cur:0:1}" == "\"" ]]
            then
                # started with double quote, escaping all double quotes and all backslashes
                # ["]bla'bla"bla\bla bla --> ["]bla'bla\"bla\\bla bla
                entry="${entry//\\/\\\\}"
                COMPREPLY[$i]="${entry//\"/\\\"}"
            else
                # no quotes in front, escaping _everything_
                # [ ]bla'bla"bla\bla bla --> [ ]bla\'bla\"bla\\bla\ bla
                entry="${entry//\\/\\\\}"
                entry="${entry//\'/\'}"
                entry="${entry//\"/\\\"}"
                COMPREPLY[$i]="${entry// /\\ }"
            fi
            (( i++ ))
        done
    }
    complete -F _words_complete rae.sh
```

Hay que tener en cuenta que el _script_ `rae.sh` debe ser accesible
desde el _path_ del sistema. Ahora, guardamos este fichero en
`/etc/bash_completion.d/rae` y lo cargamos:

    . /etc/bash_completion.d/rae

Ya podemos probarlo:

$ rae.sh line[TAB][TAB]
    lineal       lineamento   lineamiento  linear       linera       linero

Referencias
-----------

- [DuckDuckGo » User Agent][]
- [Foro de Ubuntu-es][foro de Ubuntu]
- [Bash manual > Programmable Completion][]
- [An introduction to bash completion][]
- [Handling spaces and quotes in autocompletion][deban ser escapadas primero]

  [buscón de la RAE]: http://buscon.rae.es/draeI/
    "buscón de la RAE"
  [diccionario de la RAE]: http://buscon.rae.es/draeI/ "drae"
    "diccionario de la RAE"
  [diccionario panhispánico de dudas]: http://buscon.rae.es/dpdI/ "dpd"
    "diccionario panhispánico de dudas"
  [buscón]: http://www.rae.es/drae
    "buscón"
  [el panhispánico de dudas]: http://www.rae.es/dpd
    "el panhispánico de dudas"
  [foro de Ubuntu]: http://www.ubuntu-es.org/node/125850
    "foro de Ubuntu"
  [deban ser escapadas primero]: http://stackoverflow.com/questions/1146098/properly-handling-spaces-and-quotes-in-bash-completion
    "Handling spaces and quotes in autocompletion"
  [DuckDuckGo » User Agent]: http://duckduckgo.com/html?q=User%20Agent
    "DuckDuckGo » User Agent"
  [Bash manual > Programmable Completion]: http://www.gnu.org/software/bash/manual/bash.html#Programmable-Completion
    "Bash manual > Programmable Completion"
  [An introduction to bash completion]: http://www.debian-administration.org/articles/316
    "An introduction to bash completion"
