Title: Evitar el registro de comandos en el historial
Date: 2012-03-16 14:21
Author: Nacho Cano
Tags: .bash_history, HISTCONTROL, HISTFILE, HISTFILESIZE, HISTIGNORE, history, HISTSIZE, HISTTIMEFORMAT
Slug: evitar-el-registro-de-comandos-en-el-historial

Por diferentes motivos, nos puede interesar que lo que escribamos en el
terminal no quede registrado en el historial, por ejemplo, si
necesitamos escribir una contraseña. Esto se puede conseguir de
diferentes maneras. El historial cuenta con una copia en memoria,
accesible mediante el comando `history`, que se vuelca en el fichero
`~/.bash_history` al terminar la sesión.

Las variables involucradas en el historial son:

-   `HISTCONTROL`, contiene una lista de valores separados por coma que
    indican bajo qué condiciones se deben añadir entradas al historial.
    Estos valores pueden ser `ignorespace`, `ignoredups`, `ignoreboth` o
    `erasedups`.
-   `HISTFILE`, contiene el nombre del fichero donde se guardará el
    historial. Por defecto `~/.bash_history`.
-   `HISTFILESIZE`, contiene el número máximo de entradas que se
    guardarán en el fichero. Por defecto, 500.
-   `HISTIGNORE`, contiene una lista separada por dos puntos `:` de los
    comandos que deben ser ignorados. Podemos utilizar `*` para crear
    patrones que deban coincidir.
-   `HISTSIZE`, contiene el número de entradas en memoria que debe
    contener el historial. Por defecto, 500.
-   `HISTTIMEFORMAT`, puede contener el formato utilizado para guardar
    la fecha y hora asociada a cada entrada en el historial.


Espacio al inicio
-----------------

Una opción es especificar que se ignoren las entradas que comiencen con
un espacio. Para activar esta opción de forma permanente, la variable
`HISTCONTROL` debe contener el valor `ignorespace` o `ignoreboth`
(`ignoreboth` incluye `ignorespace` e `ignoredups`, ésta última es para
ignorar duplicados) en nuestro archivo de configuración `~/.bashrc`.

Si sólo queremos que sea efectivo para la sesión actual podemos
modificar el valor de la variable en el terminal.

```bash
HISTCONTROL=ignoreboth
```

Tamaño del historial
--------------------

Otra opción es poner modificar el valor de la variable `HISTSIZE`, que
contiene el tamaño del historial en memoria. Por ejemplo, le asignamos
un valor de 0 a la variable:

```bash
HISTSIZE=0
```

Asignarle un valor vacío parece que provoca que sólo se guarde el último
comando introducido y eliminar la variable con `unset` tampoco funciona,
al menos en `bash`, ya que entonces toma el valor por defecto de 500.

El fichero del historial
------------------------

Podemos modificar el valor de la variables `HISTFILE` o `HISTFILESIZE`
para evitar que el historial de la sesión se guarde en disco al
terminal. Hay que tener en cuenta que lo que escribamos seguirá
disponible en memoria y será accesible con el comando `history`.
