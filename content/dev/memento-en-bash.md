Title: Memento en Bash
Date: 2010-09-26 16:01
Author: Nacho Cano
Tags: alias, byobu, ficheros ocultos, lista de cosas por hacer, lorem ipsum, memento, post-it, screen, script, terminator
Slug: memento-en-bash

> No me acuerdo de olvidarte.

![Memento Polaroid Natalie Clean]({static}/images/memento_polaroids_natalieclean_18700997-248x300.jpg)

Si lo primero que haces nada más iniciar una sesión es abrir el
terminal. Varias ventanas, varias pestañas. `screen`, `terminator` o
`byobu`. Es posible que, alguna vez, se te haya pasado por la cabeza que
sería interesante guardar una nota sobre algo que estamos haciendo, algo
que quisiéramos recordar más tarde, algo que quisiéramos no olvidar,
algo que está relacionado con el directorio en el que estamos.

Si, por ejemplo, tenemos un directorio con imágenes reducidas a un
tamaño concreto, y queremos que, cuando haya pasado un tiempo y volvamos
a este directorio, podamos recordar dicho tamaño de forma rápida y
directa, de un vistazo, sin tener que (volver a) investigar cual era ese
tamaño. Si estamos editando un fichero, podemos incluir la nota en un
comentario dentro del fichero, pero es posible que no nos acordemos de
dicha nota hasta que vayamos a editar ese fichero nuevamente, quizá por
otro motivo. Si quisiéramos recordar muchas cosas, tenerlas en un único
sitio no es lo más cómodo, ya que la lista en seguida crece. Si tenemos
que enviar un correo electrónico más tarde, el directorio de usuario es
un lugar frecuentemente transitado. Si quieres recordar el comando para
buscar documentos repetidos en el directorio de descargas.

Sería interesante que, nada más llegar a ese directorio, se mostrasen
las notas que habíamos dejado ahí previamente. Como si tuviéramos
_post-it’s_ escritos por toda la casa.

Podemos conseguir esto añadiendo un alias para el comando `cd` que,
además de cambiar de directorio, busque si hay notas y las muestre. Los
alias se definen en el fichero `~/.bash_aliases`:

```bash
alias cd='source /home/user/scripts/memento.sh'
```

El código del _script_ `memento.sh` que nos permite hacer esto es:

```bash
MSGFILE=".msg"
\cd "$@"
if [ -r "$MSGFILE" ]; then
        awk "\$0!~/^#/{ print '>>>',\$0 }" $MSGFILE
fi
```

Para dejar una nota en un directorio:

```bash
$ echo "Lorem ipsus dolor sit amet" >> .msg
```

* * * * *

#### Actualizado el 5 de agosto de 2011

Ahora ya podemos utilizar el propio _script_ para ir añadiendo notas.
También he incluido la opción de que nos informe del número de elementos
ocultos que hay en el directorio. El _script_ debe estar en el PATH del
sistema, o podemos especificar la ruta hasta él, y permisos de
ejecución.

```bash
$ memento.sh "Lorem ipsum dolor sit amet"
```

* * * * *

Cuando visitemos dicho directorio:

```bash
$ cd
19 hidden files and directories found.
>>> Lorem ipsum dolor sit amet
```

Como colofón, comentar que si queremos ver cuáles son esos ficheros y
directorios ocultos podemos ejecutar:

```bash
$ ls -d .* | sed 1,2d
```

Mejor aún, podemos crear un alias:

```bash
$ alias vh='ls -d .* | sed 1,2d'
```

