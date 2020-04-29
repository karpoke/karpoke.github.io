Title: setuid y setgid
Date: 2011-02-28 14:33
Author: Nacho Cano
Tags: c, chmod, find, gcc, getegid, geteuid, getgid, getuid, gid efectivo, gid real, id, sticky bit, uid efectivo, uid real
Slug: setuid-y-setgid

`setuid` y `setgid` son unos permisos especiales, también llamados los
_sticky bits_, que se les pueden asignar a los programas ejecutables
para que se ejecuten con los permisos del propietario y no del usuario
que los ejecuta. Esto sirve para, por ejemplo, que cualquier usuario
ejecute el comando `ping` aunque éste necesite privilegios de
administrador, que es el propietario. En GNU/Linux, y en Unix, estos
bits se ignoran cuando se aplican a directorios.

Ejecutar un comando como si fuésemos otro usuario, especialmente como si
fuésemos el administrador, suena peligroso... para el administrador. El
problema viene porque si uno de éstos programas sufre un *buffer
overflow*, el usuario podría ejecutar código arbitrario con privilegios
de administrador.

Para cambiar estos permisos con `chmod` debemos utilizar el *byte
alto*. El valor en octal que debemos usar es 4 para el `setuid` y 2 para
el `setgid`. Si queremos poner los dos utilizaremos el 6.

Por ejemplo, activar el `setuid` (4) y darle permisos de ejecución,
lectura y escritura para el propietario (7), y sólo de lectura para el
grupo y el resto (4) sería:

    $ chmod 4744 myelf

Si sólo quisiéramos cambiarle los permisos a un archivo para que tenga
alguno de estos bits activados:

    $ chmod u+s myelf
    $ chmod g+s myelf
    $ chmod ug+s myelf

Para quitárselos:

    $ chmod u-s myelf
    $ chmod g-s myelf
    $ chmod ug-s myelf

Para mostrar los archivos con `setuid` o `setgid` que hay en el sistema,
accesibles para el usuario con el que estamos, evitando mostrar los
avisos de que no tenemos permisos de entrar en según qué direcctorios,
ejecutamos:

    $ find / -type f \( -perm -4000 -o -perm -2000 \) -print 2>/dev/null 1>stickybit.txt &
    $ tail -f stickybit.txt

    /bin/mount
    /bin/fusermount
    /bin/su
    /bin/umount
    /bin/ping6
    /bin/ping
    ...

En la [Wikipedia][], podemos ver un pequeño programa en C que nos muestra
esta diferencia entre el `uid` del usuario y del propietario:

    #include <sys/types.h>
    #include <unistd.h>
    #include <stdio.h>
    int main(void) {
        printf(
            "Real      UID = %d\n"
            "Effective UID = %d\n"
            "Real      GID = %d\n"
            "Effective GID = %d\n",
            getuid (),
            geteuid(),
            getgid (),
            getegid()
        );
        return 0;
    }

Vamos a probarlo. El código de este programa está en el archivo
`printid.c`:

    $ id -u
    1000
    $ sudo id -u
    0
    $ sudo gcc -Wall printid.c -o printid
    $ sudo chmod ug+s printid
    $ ls -l printid
    -rwsr-sr-x 1 root root 7249 2011-02-28 13:17 printid
    $ ./printid
    Real      UID = 1000
    Effective UID = 0
    Real      GID = 1000
    Effective GID = 0

  [Wikipedia]: http://en.wikipedia.org/wiki/Setuid
    "Wikipedia"
