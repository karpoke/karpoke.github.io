Title: Random Bash
Date: 2010-09-25 00:54
Author: Nacho Cano
Tags: /dev/random, /dev/urandom, /proc/interrupts, aleatoriedad, contraseña aleatoria, dd, generar entropía, mac aleatoria, makepasswd, md5sum, mkpasswd, od, openssl, pwgen, rng-tools, sha1sum, sha224sum, sha256sum, sha384sum, sha512sum, shuf, strings, tr, xxd
Slug: random-bash

<cite>"Los números aleatorios no deberían ser generados por un método
elegido aleatoriamente". _Donald E. Knuth_</cite>

En Bash, podemos obtener números enteros [aleatorios][]:

    $ echo $RANDOM
    20684

![Random number]({static}/images/random_number-300x107.jpg)

Cada vez que se referencia el parámetro [RANDOM][], éste devuelve un
valor entre 0 y 32767, es decir, 2^15^-1. Podemos inicializar la
secuencia de números aleatorios asignando un valor a RANDOM. Debemos
tener en cuenta que si le asignamos un valor vacío a RANDOM se pierden
sus propiedades especiales, aunque después lo inicialicemos.

Podemos poner a prueba la calidad de esos números aleatorios:

    $ a=()
    $ freq=10
    $ max=327680
    $ for ((i=0; i < $max; i++)); do
    >    # progress bar
    >    test $((i%($max/$freq))) -eq 0 && echo -n "."
    >    j=$RANDOM
    >    a[$j]=$((a[$j]+1))
    > done
    $ for ((i=0; i < $max/$freq; i++)); do
    >    echo "$i: ${a[$i]}";
    > done | less

Más números
-----------

Podemos obtener el módulo aleatorio de un número aleatorio.

    $ echo $((RANDOM%RANDOM))
    4530

¿Afectará de alguna manera realizar el módulo aleatorio sobre un número
aleatorio como variable aleatoria?

![Dilbert]({static}/images/Dilbert-Oct_25_001-300x117.jpg)

Sí, ya que en el mejor caso, el módulo será mayor que el primer número
y, por lo tanto, no afecta al resultado. Pero en el peor caso, el módulo
será menor que el primer número, con lo que es mayor la probabilidad de
obtener un número menor.

    $ a=()
    $ freq=10
    $ max=327680
    $ for ((i=0; i < $max; i++)); do
    >    # progress bar
    >    test $((i%($max/$freq))) -eq 0 && echo -n "."
    >    j=$((RANDOM%RANDOM))
    >    a[$j]=$((a[$j]+1))
    > done
    $ for ((i=0; i < $max/$freq; i++)); do echo "$i: ${a[$i]}"; done

Números aleatorios binarios, octales y hexadecimales:

    $ b=2
    $ for ((i=0; i < RANDOM%RANDOM; i=i+RANDOM%b)); do echo -n $((i%b)); done
    000010001111101001010001111101001011111
    $ b=8
    $ for ((i=0; i < RANDOM%RANDOM; i=i+RANDOM%b)); do echo -n $((i%b)); done
    04743654506265435353610222054150
    $ a="01234566789ABCDEF"
    $ for ((i=0; i < RANDOM%RANDOM; i++ )); do echo -n ${a:$RANDOM%${#a}:1}; done
    0150633894AD8DEF81671B06694C6B5

Debemos tener en cuenta que si queremos utilizar estos números, el
prefijo, en Bash, para los números binarios es `2#`, para los números
octales es `0` y para los números hexadecimales, `0x`. Por ejemplo, el
número 10 es `2#1010`, `012` y `0x10`.

Y letras
--------

Podemos crear una secuencia de números y letras aleatoria:

    $ a=$(echo $((echo -n {a..z}; echo -n {A..Z}; echo -n {0..9};) | sed 's/ //g'))
    $ for ((i=0; i < RANDOM%RANDOM; i++)); do echo -n ${a:$RANDOM%${#a}:1}; done
    3keV1cLFGdxO2S5nvJGzoq9EyZeryLjkVgP64Dn0z

Fuentes de aleatoriedad
-----------------------

-   /dev/random
-   /dev/urandom
-   /proc/interrupts

Los dos primeros son ficheros especiales que permiten acceso al
[generador de números aleatorios][] del kernel. El kernel recoge ruido
ambiental desde los controladores de dispositivos (como por ejemplo, el
ratón) y otras fuentes y lo usa como fuente de aleatoriedad. También
tiene en cuenta el número de bits que se pueden crear aleatoriamente con
un nivel de entropía tal que no sean vulnerables a ataques
criptográficos. `/dev/random` se debería utilizar para crear claves
criptográficas, para todo lo demás, podemos usar `/dev/urandom`.

Estas fuentes proporcionan bits aleatorios, no caracteres, por lo que
antes de utilizarlos para mostrar una cadena de caracteres deberemos
pasarlos por alguna función como:

-   `md5sum`
-   `shasum`
-   `sha1sum`
-   `sha224sum`
-   `sha256sum`
-   `sha384sum`
-   `sha512sum`
-   `grep -o '[[:alnum:]]'`
-   `tr -dc a-zA-Z0-9`
-   `xxd -ps`
-   `od -An -td | sed 's/\s_\(._\)\s/\1/g'`
-   o cualquier otra combinación que filtre los caracteres

`/proc/interrupts` registra el número de interrupciones de cada
dispotivo de entrada/salida, por lo que debería funcionar bien como
fuente de aleatoriedad.

Cadenas de caracteres aleatorios:

    $ strings /dev/urandom | grep -o '[[:alnum:]]' | head -n 12 | tr -d '\n'; echo
    tUqWq9fqem9C1gKbTpCcVJg6DNvxMG
    $ < /dev/urandom tr -dc _a-zA-Z0-9 | head -c12
    1G0gNNXM3RkT
    $ dd if=/dev/random bs=1 count=5 2>/dev/null | xxd -ps
    3e3206ff95

Generando entropía
------------------

Si la fuente de entropía no da abasto y necesitamos generar más entropía
más rápido, por ejemplo, cuando creamos claves RSA muy largas, poner a
trabajar el equipo podría servir. Algo como:

    $ ls -lRh /
    $ find / -name \*

Sin embargo, existe un programa que sirve para esto. `rng-tools` ayuda a
[generar entropía][]. Una vez instalado desde los respositorios,
modificamos el fichero `/etc/default/rng-tools` para que contenga:

    HRNGDEVICE=/dev/urandom

Y reiniciamos el servicio:

    $ sudo service rng-tools restart

Si ahora volvemos a crear una clave, notaremos que el tiempo necesario
para conseguir la entropía necesaria es mucho menor.

* * * * *

#### Actualizado el 25 de septiembre de 2016

Otro servicio que sirve para esto es `haveged`:
    systemctl enable haveged
    systemctl start haveged

* * * * *

Otros programas
---------------

Podemos instalar estos programas desde los repositorios.

### makepasswd

Para crear contraseñas.

    $ makepasswd --char=12

### mkpasswd

Otro para crear contraseñas.

    $ mkpasswd

### openssl

Permite obtener una serie de bytes hexadecimales aleatorios; por cada
byte hexadecimal se imprimen dos caracteres hexadecimales:

    $ openssl rand -hex 16
    5666b2215534c6d4c3be4101219cd0b1

También permite obtener caracteres en base64:

    $ openssl rand -base64 12
    ymwU0wtOZ6wMgAfr

### pwgen

Otro más para crear contraseñas

    $ pwgen 12

### rand

Trabaja con números y caracteres. Por ejemplo, podemos obtener números
decimales aleatorios.

    $ rand -f
    0.04691

No sólo letras y números
------------------------

Podemos crear una dirección MAC aleatoria:

    $ echo $(cat /proc/interrupts | md5sum | sed -r 's/^(.{10}).*$/00\1/; s/([0-9a-f]{2})/\1:/g; s/:$//;')
    00:6d:b6:2f:46:1d
    $ openssl rand -hex 6 | sed -r 's/^(.{10}).*$/00\1/; s/([0-9a-f]{2})/\1:/g; s/:$//;'
    00:8d:e6:98:ca:d2

Podemos crear un fichero o un directorio temporal, cuyo nombre es
aleatorio:

    $ mktemp
    /tmp/tmp.WBABktXDHZ
    $ mktemp -d
    /tmp/tmp.lHuPARC0YC

Podemos mostrar un fichero aleatorio:

    $ find ~ -maxdepth 1 | shuf -n1 --random-source=/dev/random
    ./bash_aliases

Podemos poner una imagen de fondo de escritorio aleatoria en Gnome:

    $ f=$(find ~/Imágenes/ | shuf -n1 | egrep 'gif|jpe?g|png')
    $ while test -n "$f"; do f=$(find ~/Imágenes/ | shuf -n1); done
    $ gconftool-2 -t str --set /desktop/gnome/background/picture_filename "$f"

Podemos generar una contraseña [a partir de 4 palabras aleatorias][]:

    $ printf '%s %s %s %s' $(\grep -v "'" /usr/share/dict/american-english | shuf -n 4 | tr '[:upper:]' '[:lower:]')
    meters haven backtracking subordinates

Podemos mostrar una línea aleatoria de un fichero:

    $ shuf -n1 /etc/passwd

O también podemos mostrar un número de líneas aleatorio de un archivo
aleatorio del código fuente de Linux:

    $ f=$(find /usr/src/linux-source-2.6.32 -type f -name \* | shuf -n1)
    $ n=$(wc -l $f | awk '{print $1}')
    $ cat $f | sed -n $((RANDOM%n)),$((RANDOM%n))p

            if (!zalloc_cpumask_var(&vec->mask, gfp))
                goto cleanup;
        }

        for_each_possible_cpu(i)
            cp->cpu_to_pri[i] = CPUPRI_INVALID;
        return 0;

    cleanup:
        for (i--; i >= 0; i--)
            free_cpumask_var(cp->pri_to_cpu[i].mask);
        return -ENOMEM;
    }

Internet
--------

En Internet, hay servicios cuyas respuestas aleatorias podemos utilizar
en nuestra vida cotidiana:

Obtener una excusa de BOFH aleatoria:

    $ telnet towel.blinkenlights.nl 666
    === The BOFH Excuse Server ===
    We didn't pay the Internet bill and it's been cut off.

Obtener un hecho aleatorio:

    $ curl -s http://randomfunfacts.com | grep -Eo ".*" | sed -r 's/([^< ]+)<\/i>< \/strong>/\1/'
    Donkeys kill more people annually than plane crashes.

Obtener un mensaje aleatorio para un _commit_:

    $ curl -s http://whatthecommit.com | grep "" | sed -r 's/([^$]+)$/\1/'
    Fucking egotistical bastard. adds expandtab to vimrc

Obtener una [frase de Futurama][] aleatoria desde Slashdot:

    $ curl -Is slashdot.org | sed -n '5p' | sed 's/^X-//'
    Bender: I'm one of those lazy, homeless bums I've been hearing about.

Obtener una [excusa de programador][] aleatoria:

    curl -s https://api.githunt.io/programmingexcuses

Además de números y letras, también podemos obtener números de lotería,
imágenes, secuencias, fechas, horas, coordenadas geográficas, música,
testimonios... todo aleatorio en [random.org][]

    $ curl -s "https://www.random.org/passwords/?num=1&len=8&format=html&rnd=new"

- Imágenes: [xkcd][], [dilbert][]
- Comandos relacionados con la aleatoriedad en [commandlinefu][]

  [aleatorios]: http://es.wikipedia.org/wiki/Aleatoriedad
    "aleatorios"
  [RANDOM]: http://linux.die.net/man/1/bash
    "RANDOM"
  [generador de números aleatorios]: http://www.kernel.org/doc/man-pages/online/pages/man4/random.4.html
    "generador de números aleatorios"
  [generar entropía]: http://dajul.com/2010/12/18/generar-mas-entropia/
    "generar entropía"
  [a partir de 4 palabras aleatorias]: https://xkcd.com/936/
    "Password Strength"
  [frase de Futurama]: http://www.commandlinefu.com/commands/view/6656/get-futurama-quotations-from-slashdot.org-servers
    "frase de Futurama"
  [excusa de programador]: https://api.githunt.io/programmingexcuses
    "excusa de programador"
  [random.org]: http://www.random.org/
    "random.org"
  [xkcd]: http://xkcd.com/
    "xkcd"
  [dilbert]: http://www.dilbert.com/
    "dilbert"
  [commandlinefu]: http://www.commandlinefu.com/commands/matching/random/cmFuZG9t/sort-by-votes
    "commandlinefu"
