Title: Nombres de fichero con espacios en Bash
Date: 2011-05-11 20:47
Author: Nacho Cano
Tags: find
Slug: nombres-de-fichero-con-espacios-en-bash

Si queremos recorrer un directorio y hacer algo con cada fichero o
subdirectorio contenido en él, podemos ejecutar algo como:

    $ for f in *; do
    echo "$f";
    done

En lugar de utilizar un `for`, también podríamos usar el comando `find`
con el parámetro `exec`:

    $ find . -maxdepth 1 \( -name '*' ! -name '.' \) -exec echo {} \;

O en lugar del `exec` con un `while`:

    $ find . -maxdepth 1 \( -name '*' ! -name '.' \) | while read f; do
    echo "$f";
    done

Un par de cosas:

-   es importante que el asterisco esté entre comillas simples, `'*'`, o
    escaparlo con una barra invertida, `\*`, para que Bash no lo
    expanda,
-   utilizar comillas dobles cuando usamos la variable, `"$f"`, para que
    al expandirla, se trate el nombre entero incluyendo los espacios, y
-   mediante `-name '*' ! -name '.'`, `find` devolverá todos los
    ficheros y directorios menos el directorio especial `.`.

También podríamos usar el comando `ls` con el argumento `-b`, que escapa
los espacios:

    $ ls -b * | while read f; do
    echo "$f";
    done
